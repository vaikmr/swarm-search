"""Pure, paper-only USD accounting helpers. No network, signing, or execution.

All output is T4 arithmetic until callers supply independently verified evidence.
Decimal inputs must be strings, integers, or Decimals, never binary floats.
See analysis/costs.md for the gross-PnL boundary and required evidence.
"""

from dataclasses import dataclass
from decimal import Decimal, localcontext
from typing import Iterable


ZERO = Decimal("0")
TIERS = {"T1", "T2", "T3", "T4"}
COST_CATEGORIES = (
    "execution_success",
    "execution_failed",
    "data_operator_fees",
    "auction_payments",
    "dex_cex_fees",
    "bridge_rebalance",
    "slippage",
    "borrow_interest",
    "funding_paid",
    "hedge_costs",
    "lp_lvr",
    "custody_withdrawal",
    "infrastructure",
)


def decimal(value: str | int | Decimal) -> Decimal:
    if isinstance(value, (bool, float)):
        raise TypeError("Use decimal strings, integers, or Decimal, not bool/float")
    result = Decimal(value)
    if not result.is_finite():
        raise ValueError("Values must be finite")
    return result


def nonnegative(value: str | int | Decimal) -> Decimal:
    result = decimal(value)
    if result < ZERO:
        raise ValueError("Value cannot be negative")
    return result


@dataclass(frozen=True)
class Evidence:
    """Reference identifies a public URL or an auditable local research artifact.

    The class validates bookkeeping, not whether the claimed tier is deserved.
    A documentation URL does not become T1 simply because its inputs are real.
    """

    tier: str
    reference: str
    note: str

    def __post_init__(self) -> None:
        if self.tier not in TIERS or not self.reference.strip() or not self.note.strip():
            raise ValueError("Evidence requires T1/T2/T3/T4, reference, and note")


@dataclass(frozen=True)
class CostLine:
    category: str
    amount_usd: Decimal | None
    evidence: Evidence
    included_in_gross: bool = False

    def __post_init__(self) -> None:
        if self.category not in COST_CATEGORIES:
            raise ValueError(f"Unknown cost category: {self.category}")
        if not isinstance(self.evidence, Evidence):
            raise TypeError("Each cost needs Evidence, including explicit zeros")
        if not isinstance(self.included_in_gross, bool):
            raise TypeError("included_in_gross must be boolean")
        if self.amount_usd is not None:
            object.__setattr__(self, "amount_usd", nonnegative(self.amount_usd))


@dataclass(frozen=True)
class NetPnl:
    net_economic_pnl_usd: Decimal | None
    total_capital_return: Decimal | None
    excess_over_benchmark_usd: Decimal | None
    additional_costs_usd: Decimal
    already_included_costs_usd: Decimal
    missing_costs: tuple[str, ...]
    benchmark_missing: bool
    infrastructure_within_budget: bool | None
    evidence_tiers: tuple[str, ...]


def net_pnl(
    *,
    total_capital_usd: str | int | Decimal,
    gross_strategy_pnl_usd: str | int | Decimal,
    gross_evidence: Evidence,
    idle_contribution_usd: str | int | Decimal,
    idle_evidence: Evidence,
    costs: Iterable[CostLine],
    benchmark_net_usd: str | int | Decimal | None,
    benchmark_evidence: Evidence | None,
    infrastructure_budget_usd: str | int | Decimal = "500",
) -> NetPnl:
    """Marked economic net and benchmark excess are distinct outputs.

    Every category must be provided, even when explicitly inapplicable/zero.
    Unknown/missing costs suppress net results rather than becoming zero.
    Gross includes marked strategy inventory and hedge PnL, not separate idle
    contributions; transfer principal is not PnL. Signed idle contribution must
    include negative yields and idle-sleeve price/default losses not in gross.
    If the caller instead supplies whole-portfolio equity PnL including idle,
    separate idle MUST be zero and paid/embedded costs MUST be audit-only.
    Callers declare their boundary: component overlap is not inferred here.
    This function cannot infer realized cash receipts or withdrawable liquidity.
    Funding received and rebates go in gross; funding paid is a cost once only.
    The budget is for one month; prorate inputs before calling for other periods.
    """
    capital = nonnegative(total_capital_usd)
    if capital == ZERO:
        raise ValueError("Total capital must be positive")
    gross = decimal(gross_strategy_pnl_usd)
    idle = decimal(idle_contribution_usd)
    budget = nonnegative(infrastructure_budget_usd)
    if not isinstance(gross_evidence, Evidence) or not isinstance(idle_evidence, Evidence):
        raise TypeError("Gross and signed idle contribution require explicit evidence")
    if (benchmark_net_usd is None) != (benchmark_evidence is None):
        raise ValueError("Benchmark value and evidence must both be present or absent")
    if benchmark_evidence is not None and not isinstance(benchmark_evidence, Evidence):
        raise TypeError("Benchmark requires Evidence")
    lines = list(costs)
    if not all(isinstance(line, CostLine) for line in lines):
        raise TypeError("costs must contain CostLine records")
    categories = [line.category for line in lines]
    if len(set(categories)) != len(categories):
        raise ValueError("Aggregate each category once; duplicate category found")
    by_category = {line.category: line for line in lines}
    missing = tuple(
        category
        for category in COST_CATEGORIES
        if category not in by_category or by_category[category].amount_usd is None
    )
    additional = sum(
        (
            line.amount_usd
            for line in lines
            if not line.included_in_gross and line.amount_usd is not None
        ),
        ZERO,
    )
    included = sum(
        (
            line.amount_usd
            for line in lines
            if line.included_in_gross and line.amount_usd is not None
        ),
        ZERO,
    )
    net = None if missing else gross + idle - additional
    benchmark = None if benchmark_net_usd is None else decimal(benchmark_net_usd)
    excess = None if net is None or benchmark is None else net - benchmark
    infra = by_category.get("infrastructure")
    infra_ok = None if infra is None or infra.amount_usd is None else infra.amount_usd <= budget
    evidence = [gross_evidence, idle_evidence] + [line.evidence for line in lines]
    if benchmark_evidence is not None:
        evidence.append(benchmark_evidence)
    return NetPnl(
        net_economic_pnl_usd=net,
        total_capital_return=None if net is None else net / capital,
        excess_over_benchmark_usd=excess,
        additional_costs_usd=additional,
        already_included_costs_usd=included,
        missing_costs=missing,
        benchmark_missing=benchmark is None,
        infrastructure_within_budget=infra_ok,
        evidence_tiers=tuple(sorted({item.tier for item in evidence})),
    )


def transaction_fee_usd(
    *,
    gas_used: str | int | Decimal,
    effective_gas_price_wei: str | int | Decimal,
    native_usd: str | int | Decimal,
    extra_l1_fee_wei: str | int | Decimal,
    extra_operator_fee_wei: str | int | Decimal,
    extra_auction_payment_wei: str | int | Decimal,
    native_decimals: int = 18,
) -> Decimal:
    """Price paid gas, not gasLimit/maxFee. Included/reverted txs both pay.

    effective_gas_price already includes a paid priority fee: do not add it again.
    Extra fees MUST be zero with explanation if already embedded in gas_used,
    as can happen with Arbitrum poster fees. Unsigned/dropped txs are separate.
    If this all-in helper result is booked under execution, its L1/operator/
    auction components must not also be deducted as additional cost lines.
    Alternatively book execution-only here and those extra components separately.
    Use historical chain/fork receipt semantics, not today's defaults.
    """
    if isinstance(native_decimals, bool) or not isinstance(native_decimals, int) or native_decimals < 0:
        raise ValueError("native_decimals must be a nonnegative integer")
    native_fee = (
        nonnegative(gas_used) * nonnegative(effective_gas_price_wei)
        + nonnegative(extra_l1_fee_wei)
        + nonnegative(extra_operator_fee_wei)
        + nonnegative(extra_auction_payment_wei)
    )
    return native_fee / (Decimal(10) ** native_decimals) * nonnegative(native_usd)


def notional_fee_usd(
    notional_usd: str | int | Decimal, fee_bps: str | int | Decimal
) -> Decimal:
    """One filled leg. Rebate is separate revenue, not a negative expense."""
    return nonnegative(notional_usd) * nonnegative(fee_bps) / Decimal("10000")


def lending_income_usd(
    principal_usd: str | int | Decimal,
    annual_rate: str | int | Decimal,
    days: str | int | Decimal,
    *,
    rate_kind: str,
) -> Decimal:
    """Constant-rate conversion, not a forecast. Percent inputs use fractions.

    Piecewise variable-rate histories need one call per interval. Actual token
    indexes/cashflows supersede this APY conversion. Fees are charged separately.
    """
    principal = nonnegative(principal_usd)
    rate = decimal(annual_rate)
    interval = nonnegative(days)
    if rate <= Decimal("-1"):
        raise ValueError("Annual rate must exceed -100%")
    if rate_kind == "apr":
        return principal * rate * interval / Decimal("365")
    if rate_kind == "apy":
        with localcontext() as context:
            context.prec = 40
            return principal * ((Decimal("1") + rate) ** (interval / Decimal("365")) - 1)
    raise ValueError("rate_kind must be apr or apy")


def equity_pnl_usd(
    opening_equity_usd: str | int | Decimal,
    closing_equity_usd: str | int | Decimal,
    external_deposits_usd: str | int | Decimal,
    external_withdrawals_usd: str | int | Decimal,
) -> Decimal:
    """Reconciliation includes marked inventory, liabilities and receivables.

    Pair internal transfers across wallets/chains; they are not external flows.
    This net equity PnL already contains paid costs. Never subtract them twice.
    """
    return (
        decimal(closing_equity_usd)
        - decimal(opening_equity_usd)
        - nonnegative(external_deposits_usd)
        + nonnegative(external_withdrawals_usd)
    )


def required_return(
    net_target_usd: str | int | Decimal, total_capital_usd: str | int | Decimal
) -> Decimal:
    capital = nonnegative(total_capital_usd)
    if capital == ZERO:
        raise ValueError("Capital must be positive")
    return nonnegative(net_target_usd) / capital


def required_gross_usd(
    net_target_usd: str | int | Decimal,
    cash_costs_usd: str | int | Decimal,
    separate_idle_contribution_usd: str | int | Decimal,
) -> Decimal:
    """Requirement only; a signed idle loss increases the required gross."""
    return (
        nonnegative(net_target_usd)
        + nonnegative(cash_costs_usd)
        - decimal(separate_idle_contribution_usd)
    )


if __name__ == "__main__":
    import json

    print(json.dumps({
        "evidence_tier": "T4",
        "status": "requirement arithmetic, not attainable-return evidence",
        "total_capital_usd": "50000",
        "targets": [
            {
                "net_target_usd": str(target),
                "required_simple_monthly_net_return": str(required_return(target, "50000")),
                "gross_required_at_500_infra_before_variable_costs_usd": str(
                    required_gross_usd(target, "500", "0")
                ),
            }
            for target in ("2000", "5000")
        ],
    }, indent=2))
