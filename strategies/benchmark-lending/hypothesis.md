# Stablecoin lending benchmark — provisional, gross only

**Stage:** 0/1. **Evidence:** T4 rate arithmetic. **T1/T2/T3:** not established.
No net benchmark or deployable portfolio is certified by this package.

The first benchmark is passive, unlevered stablecoin lending, not an attempt to
earn the stretch target through trading. Protocol supply APY is a market input:
it is not a depositor's realized net return, a fork replay, or a seven-day paper
run. Incentive-token APY is excluded from the primary base-yield calculation.

## Nominal-cap candidate

| Position | Capital | Pool identifier |
| --- | ---: | --- |
| Aave V3, Ethereum, DAI | $15,000 | `3665ee7e-6c5d-49d9-abb7-c47ab5d9d4ac` |
| Compound V3, Arbitrum, USDT | $15,000 | `85247b13-8180-44e7-b38c-4d324cc68a92` |
| Morpho, Base, SparkUSDC vault | $15,000 | `a5fab52f-73fa-4f44-9c09-9af1eb20996c` |
| Off-chain cash, counterparty unspecified | $5,000 | Not an on-chain stablecoin |

Each named protocol, chain and stablecoin has a nominal 30% exposure, and 10%
remains outside those chain domains. This is a cap-matching candidate, **not
verified issuer/wrapper/settlement independence**. DAI reserve exposure can
overlap USDC; Arbitrum and Base depend on Ethereum settlement and bridges. The
exact SparkUSDC vault deployment, market allocation, curator, collateral/oracle
and audit linkage need verification. Do not substitute an aggregator's number of
observations for the vault's age. Even an individually capped total loss can
breach the separate monthly drawdown requirement.

The official Morpho app identifies the Base SparkUSDC vault as
[`0x7BfA7C4f149E7415b73bdeDfe609237e29CBF34A`](https://app.morpho.org/base/vault/0x7BfA7C4f149E7415b73bdeDfe609237e29CBF34A/spark-usdc-vault).
The pool-to-vault mapping is a name/chain/asset lead, not an independently
reconciled mapping of the aggregator adapter's accounting.

## Reproducible gross outputs

Source histories end at a common **2026-10-29 06:01:03.674 UTC**. The model
carries each observed base APY forward to the next observation, compounds using
an ACT/365 year, refuses gaps longer than 36 hours, and checks full coverage.
Cash earns zero in this explicit scenario. It does not optimize allocations
using future rates.

| Window | Start UTC | Gross USD, T4 | Net USD |
| --- | --- | ---: | --- |
| Trailing 30 days | 2026-09-29 06:01:03.674 | $119.90 | Unknown |
| Trailing 90 days | 2026-07-31 06:01:03.674 | $346.38 | Unknown |
| Current base rates persist for 30 days, scenario only | Snapshot dated 2026-10-29 | $136.63 | Unknown |

Exact amounts, time weights, source URLs, component math and `null` costs are in
[`candidate-allocation.json`](evidence/candidate-allocation.json). These are
gross historical-rate illustrations, not forecasts or risk-adjusted returns.
Costs, default loss and stablecoin mark-to-market are not assumed zero.

Three chains capped at 30% can hold no more than 90% of total capital. A fully
invested three-chain portfolio is impossible under those literal limits without
an off-chain allocation or a changed rule. No rule is relaxed here.

## Remaining evidence

- Obtain specific deployed-market/vault eligibility and look-through exposure.
- Reconcile a real depositor's opening/closing inventory, deposits/withdrawals,
  borrowing liabilities if any, rebasing/index accrual and every cost over at
  least fourteen days.
- Price the same candidate's entry/exit, bridging and operation costs with the
  accountant; net remains unavailable until these are known or explicit scenarios.
- Complete actual fork replay and qualifying forward paper trading, plus
  independent risk/judge review. This package supplies neither.

Protocol-wide age, TVL and public-audit leads are in
[`protocol-eligibility-snapshot.json`](evidence/protocol-eligibility-snapshot.json).
They do not establish market-level eligibility or withdrawal availability.

## Lower-deployment follow-up

The maximum 90% deployment is not a goal. A later
[single-chain low-exposure study](lower-deployment.md) preserves this prototype
and tests $4,000 of Aave Ethereum USDC against explicit monthly and annual
full-sleeve-loss/cost budgets. Off-chain cash risks and current audit-build
coverage remain unresolved; neither iteration is certified compliant.
