# Independent cost-model review

Reviewed immutable revision: [`43cda27e6e4a9d8fe828e75edcb1c244b7f78739`](https://github.com/vaikmr/swarm-search/commit/43cda27e6e4a9d8fe828e75edcb1c244b7f78739), 2026-10-29.

Scope: `research_tools/costs.py`, `analysis/costs.md`, and `tests/test_costs.py`. The judge did not author or modify those files. This is an independent arithmetic/reporting-contract review, not an economic outcome, risk certification, or strategy verdict.

## Conclusion

Benchmark separation, signed gross losses, cost-inclusion flags and explicit unknown handling passed the inspected tests. Two medium-priority reporting/adapter issues should be addressed before downstream study reports rely on the output names or feed signed idle returns directly. A separate integration caution needs explicit examples to avoid counting income or receipt components twice.

All example amounts and rates below are **T4 synthetic reviewer fixtures**, not market observations, attainable returns, real costs, or probability estimates.

## Findings

### C1 — Medium: marked-equity PnL is labeled cash PnL

References: [`costs.py` lines 78–83, 108–113, 156–168](https://github.com/vaikmr/swarm-search/blob/43cda27e6e4a9d8fe828e75edcb1c244b7f78739/research_tools/costs.py#L78-L168); [`costs.md` lines 31–39 and 54–67](https://github.com/vaikmr/swarm-search/blob/43cda27e6e4a9d8fe828e75edcb1c244b7f78739/analysis/costs.md#L31-L67).

The documented gross boundary includes inventory/hedge mark-to-market and earned but unclaimed income. `net_pnl` nevertheless returns `net_cash_pnl_usd`. A synthetic input consisting solely of 123 USD of unrealized appreciation produces `net_cash_pnl_usd = 123` despite stipulated cash receipts of zero.

The total-equity arithmetic is not wrong; the label is. This can cause an accrued gain or unsettled receivable to be presented as cash available for withdrawal, fill capital, or realized actor PnL. T1 actor evidence and the user's monthly net-profit goal must distinguish realized receipts, accrued income and unrealized changes.

Requested owner remedy: rename/document the output as total marked/net-equity PnL, or provide separate cash-realized and mark-to-market fields with reconciliation. Add a fixture proving an entirely unrealized gain is not represented as a cash receipt. No code was changed by the judge.

### C2 — Medium: signed idle contribution lacks a direct accepted path

References: [`costs.py` lines 119–120](https://github.com/vaikmr/swarm-search/blob/43cda27e6e4a9d8fe828e75edcb1c244b7f78739/research_tools/costs.py#L119-L120) and [`lending_income_usd`, lines 211–235](https://github.com/vaikmr/swarm-search/blob/43cda27e6e4a9d8fe828e75edcb1c244b7f78739/research_tools/costs.py#L211-L235).

The lending helper intentionally accepts negative annual rates above its lower bound, but `net_pnl` applies `nonnegative` to `idle_yield_usd`. A synthetic 1,000 USD principal, negative 0.01 APR and 30-day interval produces `-0.8219178082191780821917808219` USD in the lending helper; passing that value as idle yield raises `ValueError: Value cannot be negative`.

Gross strategy losses are already supported and tested. The problem is narrower: the natural signed output of an idle/lending adapter cannot be passed directly to the idle field. An adapter can route idle losses into gross PnL instead, but that alternative must be explicit and tested, including idle asset depeg/default marks, to avoid aborting the run or omitting a loss. No observed loss has been dropped in this study.

Requested owner remedy: accept a signed separately accounted idle contribution, or document/test a loss-routing boundary into total gross marked PnL exactly once. Never clamp negative idle values to zero.

### C3 — Integration caution, not a demonstrated current double-counting bug

References: [`equity_pnl_usd`, lines 238–254](https://github.com/vaikmr/swarm-search/blob/43cda27e6e4a9d8fe828e75edcb1c244b7f78739/research_tools/costs.py#L238-L254); [`net_pnl`, lines 140–158](https://github.com/vaikmr/swarm-search/blob/43cda27e6e4a9d8fe828e75edcb1c244b7f78739/research_tools/costs.py#L140-L158); [`transaction_fee_usd`, lines 177–202](https://github.com/vaikmr/swarm-search/blob/43cda27e6e4a9d8fe828e75edcb1c244b7f78739/research_tools/costs.py#L177-L202).

The documentation correctly calls idle yield **separate**, and inclusion flags correctly prevent a listed cost already in gross from being deducted again. They cannot detect overlapping caller-supplied income or costs:

- Whole-portfolio `equity_pnl_usd` already includes separate idle-account accrual. A synthetic portfolio equity rise of 100 USD, passed as gross, plus that same 100 USD passed again as idle yield returns 200 USD. The valid separate-income path excludes the idle accrual from gross and returns 100 USD. This demonstrates caller-boundary misuse, not that current strategy adapters perform it.
- The fee helper can return execution plus L1/operator/auction totals. If a caller puts that all-in number in execution and then repeats its components as separate cost categories, the ledger cannot infer their overlap. The category-uniqueness check only catches the same category being repeated.

Requested integration guard: document/test mutually exclusive raw-strategy-versus-whole-equity and execution-only-versus-all-in-receipt adapters. In a whole-equity path, separate idle must be zero if already included; each already-paid cost must be audit-only. Preserve cost identity/component provenance so each expense is deducted exactly once. This caution alone is not a failing arithmetic result.

## Verified behavior

Independently ran:

```sh
python3 -m unittest discover -s tests -p 'test_costs.py' -v
python3 -m research_tools.costs
python3 review/evidence/cost_model_probe.py
```

Observed: all 19 original synthetic tests passed. The requirement-arithmetic CLI ran and labeled outputs T4. Reviewer probes reproduced C1/C2/C3 and confirmed:

- Changing the benchmark changes excess, not net PnL.
- Negative gross contributions remain negative; they are not floored to zero.
- Missing/unknown costs suppress net PnL instead of silently becoming zero.
- A missing benchmark suppresses benchmark excess, not an otherwise known net PnL.
- A cost flagged as already included is displayed without being deducted again.

These results support only the specified arithmetic behavior. They do not validate source histories, account ownership, strategy profitability, execution, a risk bound, T1, T2, or T3. Existing tests do not cover the C1/C2 reporting and signed-idle boundaries.

## Source-convention spot checks

Re-fetched the primary public pages on 2026-10-29, independently of the accountant:

- [Kraken fee schedule](https://www.kraken.com/features/fee-schedule): the displayed entry spot row matches the package's 0.40% maker / 0.80% taker inputs, and the entry futures row matches 0.02% / 0.05%. Other products/tiers have different schedules. These are sourced current schedule inputs; modeled use stays T4, not actor returns or confirmation of operator eligibility.
- [Alchemy pricing](https://www.alchemy.com/pricing): the displayed free allowance, PAYG all-usage unit pricing and separately priced additional capacity agree with the package's stated convention. Free-plan allowance must not also be subtracted from PAYG usage.

This spot check is not an archival proof of charges on historical dates. The review did not independently replay OP/Arbitrum receipts, Across settlements, historical CEX tiers, account-specific withdrawal quotes, provider performance or an actual production invoice. Those remain source/data requirements for strategy packages. The current documentation's explicit unknown benchmark and exclusion of setup/labor/taxes from verified steady-state costs must remain visible.

## Disposition

**Accounting scaffolding only; economic outcome NOT CERTIFIED.** Return C1/C2 to the cost-model owner for response and targeted regression coverage. Require explicit adapter boundaries from C3 at integration. No strategy evidence tier or NOT READY strategy status is upgraded by this review.
