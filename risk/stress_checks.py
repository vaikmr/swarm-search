"""T4 arithmetic only. No network access, trading, fills, forecasts or certificates."""

from decimal import Decimal, InvalidOperation
import json
import math


DOMAINS = ("chain", "protocol", "stablecoin", "bridge", "cex", "shared_dependency")


def amount(value):
    """Parse a finite nonnegative decimal without silently accepting booleans."""
    if isinstance(value, bool):
        raise ValueError("boolean is not an amount")
    try:
        number = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError("invalid amount") from exc
    if not number.is_finite() or number < 0:
        raise ValueError("amount must be finite and nonnegative")
    return number


def concentration(positions, capital="50000", cap_fraction="0.30", max_chains=3):
    """Sum declared gross domain exposures, separately from allocated equity.

    Inputs must declare all domain categories, even when empty. This does not
    establish completeness, independence or correct wrapper look-through.
    Exposures may exceed equity, e.g. leveraged or contingent liabilities.
    """
    capital, fraction = amount(capital), amount(cap_fraction)
    if capital <= 0 or fraction > 1:
        raise ValueError("positive capital and cap fraction <= 1 required")
    if isinstance(max_chains, bool) or not isinstance(max_chains, int) or max_chains < 1:
        raise ValueError("max_chains must be a positive integer")
    allocated = Decimal(0)
    totals = {domain: {} for domain in DOMAINS}
    ids = set()
    for position in positions:
        name = position["id"]
        if not isinstance(name, str) or not name or name in ids:
            raise ValueError("position ids must be distinct nonempty strings")
        ids.add(name)
        allocated += amount(position["equity_usd"])
        exposures = position["exposures_usd"]
        if set(exposures) != set(DOMAINS):
            raise ValueError("all and only known domain categories required")
        for category, entries in exposures.items():
            if not isinstance(entries, dict):
                raise ValueError("domain entries must be maps")
            for domain, value in entries.items():
                if not isinstance(domain, str) or not domain.strip():
                    raise ValueError("nonempty domain names required")
                value = amount(value)
                if value:
                    totals[category][domain] = totals[category].get(domain, Decimal(0)) + value
    if allocated != capital:
        raise ValueError("allocated equity must exactly equal total capital")
    limit = capital * fraction
    breaches = [
        {"category": category, "domain": domain, "exposure_usd": str(value)}
        for category, entries in totals.items()
        for domain, value in entries.items()
        if value > limit
    ]
    chain_count = len(totals["chain"])
    return {
        "evidence_tier": "T4",
        "input_kind": "declared exposures; completeness not verified",
        "capital_usd": str(capital),
        "domain_cap_usd": str(limit),
        "chain_count": chain_count,
        "chain_count_breach": chain_count > max_chains,
        "domain_breaches": breaches,
        "exposures_usd": {
            category: {domain: str(value) for domain, value in entries.items()}
            for category, entries in totals.items()
        },
        "risk_certificate": False,
    }


def conditional_loss(exposure, severity, capital="50000"):
    exposure, severity, capital = amount(exposure), amount(severity), amount(capital)
    if severity > 1 or capital <= 0:
        raise ValueError("severity <= 1 and positive capital required")
    loss = exposure * severity
    return {
        "evidence_tier": "T4",
        "exposure_usd": str(exposure),
        "severity_fraction": str(severity),
        "conditional_loss_usd": str(loss),
        "portfolio_loss_fraction": str(loss / capital),
        "exceeds_monthly_severity_limit": loss > capital * Decimal("0.10"),
        "exceeds_annual_scenario_severity_limit": loss > capital * Decimal("0.20"),
        "annual_probability": None,
        "annual_kill_gate_established": False,
        "risk_certificate": False,
    }


def zero_breach_upper_bound(months, alpha=0.05):
    """Exact one-sided binomial bound for zero IID monthly breaches (T4)."""
    if isinstance(months, bool) or not isinstance(months, int) or months <= 0:
        raise ValueError("months must be a positive integer")
    if isinstance(alpha, bool) or not isinstance(alpha, (int, float)) or not 0 < alpha < 1:
        raise ValueError("alpha must lie strictly between zero and one")
    return -math.expm1(math.log(alpha) / months)


def example_position(name, equity, **domains):
    return {
        "id": name,
        "equity_usd": str(equity),
        "exposures_usd": {category: domains.get(category, {}) for category in DOMAINS},
    }


def example_output():
    """Fictional names avoid implying current protocol/coin eligibility."""
    example = [
        example_position("chain-a", 15000, chain={"A": "15000"}, protocol={"Lender-A": "15000"}, stablecoin={"Coin-A": "15000"}),
        example_position("chain-b", 15000, chain={"B": "15000"}, protocol={"Lender-B": "15000"}, stablecoin={"Coin-B": "15000"}),
        example_position("chain-c", 15000, chain={"C": "15000"}, protocol={"Lender-C": "15000"}, stablecoin={"Coin-C": "15000"}),
        example_position("offchain-usd", 5000, cex={"Venue-D": "5000"}),
    ]
    cap, chain_limit, per_chain = Decimal("50000"), 3, Decimal("0.30")
    n = math.ceil(math.log(0.05) / math.log(0.99))
    return {
        "purpose": "T4 deterministic arithmetic and hypothetical input fixture; NOT replay or a portfolio recommendation",
        "risk_certificate": False,
        "allocation_arithmetic": {
            "max_onchain_fraction": str(chain_limit * per_chain),
            "max_onchain_usd": str(cap * chain_limit * per_chain),
            "min_offchain_usd": str(cap * (1 - chain_limit * per_chain)),
        },
        "hypothetical_declared_allocation": concentration(example),
        "stresses": {
            "source_context_usdc_0_87_mark_applied_to_hypothetical_15000": conditional_loss("15000", "0.13"),
            "assumed_total_loss_of_hypothetical_15000_bucket": conditional_loss("15000", "1"),
        },
        "iid_statistical_illustrations_not_empirical_estimates": {
            "zero_breach_months_for_one_sided_95pct_upper_bound_below_1pct": n,
            "upper_bound_at_that_sample_size": zero_breach_upper_bound(n),
            "annual_probability_given_iid_1pct_monthly": 1 - 0.99**12,
            "monthly_probability_given_iid_1pct_annual": 1 - 0.99**(1 / 12),
        },
        "probability_source": "No observed frequency model. Illustrative IID assumptions only.",
    }


if __name__ == "__main__":
    print(json.dumps(example_output(), indent=2, sort_keys=True))
