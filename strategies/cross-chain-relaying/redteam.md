# Cross-chain relaying — independent risk specification

Date: 2026-10-29. Status: **not risk-certified; outstanding-claim and settlement-tail evidence missing**. No verdict or performance evidence.

Apply all eight scenarios and both loss gates in the [shared review](../../risk/README.md). Sources are [registered separately](../../risk/sources.json).

## Candidate-specific failure paths

- A completed destination fill exchanges liquid inventory for a repayment claim. Across explicitly documents capital fronting, reimbursement lock-up, finality/software risks and exclusive fill rights ([S05](https://docs.across.to/introduction/actors)). Its approximate timing is not a guaranteed settlement deadline or empirical delay distribution.
- Sum all unsettled fills, bonds, protocol deposits and bridge-backed inventory across chains under the corresponding protocol/bridge domain. A repayment-chain choice changes inventory placement, not necessarily its underlying common trust dependencies.
- An origin reorganization, invalid local fill decision, reimbursement dispute, halt or settlement pause can leave cash unavailable or an impaired claim. Historical bridge restoration is not an enforceable reimbursement guarantee ([S10](https://www.reuters.com/technology/crypto-site-wormhole-tells-users-all-funds-are-safe-after-320-mln-hack-2022-02-03)).

## Required tests and mitigations

Replay only publicly eligible fills and respect exclusivity. Halt settlement, deny rebalancing, depeg inventory/claims, spike gas and invalidate stale quotes in a local decision model. Remove opportunities lost to a larger competitor without fabricating a capture fraction. Freeze CEX-funded rescue paths when applicable. Stress protocol fee/bond/repayment-rule changes and oracle unavailability.

Cap **outstanding exposed principal**, not just fill size; stop new fills on aged or unreconciled claims. Pre-position fee reserves that remain accessible on each allowed chain. The three-chain concentration limit still applies when claims are repaid elsewhere.

**Reassessment inputs:** fill-to-repayment reconciliations, p-tail settlement ages, refund/finality dependencies, projected maximum outstanding claims and genuine T2/T3 runs. Delay loss, principal impairment and total-capital PnL must be separated; frequencies remain unquantified.
