# Lawful auction backrunning — independent risk specification

Date: 2026-10-29. Status: **not risk-certified; admission, atomicity and downside-cost evidence missing**.

Apply all eight scenarios and both loss gates in the [shared review](../../risk/README.md). Only permitted backrunning is in scope; no user front-running, sandwiching or exploit paths.

## Candidate-specific failure paths

- Atomic backrunning is not equivalent to an inventory strategy. A reverted atomic sequence may protect the trade principal but still produce costs, especially if the venue charges for failures or bids. Submission semantics must be proven for the actual auction, not assumed.
- Data access, refunds, exclusivity, payment rules and admission can change or disappear. A larger competitor can reduce accessible revenue while server/RPC costs continue.
- Prefunded execution contracts, balances, bonds and inventory introduce protocol/chain/issuer exposure distinct from a zero-inventory bundle.

## Required tests and mitigations

Account for every submitted, rejected, losing and included bid. Lose unproven ties. Separate conditional bid payments, refunds and gas from captured trade surplus. Test stale hints, gas shocks, access removal, parameter changes, chain halt and competitor entry. Reprice any stablecoin balance and deny any bridge/CEX replenishment used by the design.

Bound capital in execution contracts and eliminate unneeded standing inventory. Enforce contract/quote validity and all-in profitability locally; this specification does not authorize a contract deployment. Sequencer disruption can impede ordinary execution and subsequent exits ([S04](https://docs.chain.link/data-feeds/l2-sequencer-feeds)).

**Reassessment inputs:** published venue rules, actual entrant eligibility, executable atomicity/failure-cost evidence, wallet capital reconciliation and lawful auction replay/paper outputs. Ethereum L1 builder-dominated opportunities remain excluded absent demonstrated contestability. No calibrated event probability or monthly risk bound is available.
