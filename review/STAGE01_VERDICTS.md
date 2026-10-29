# Independent Stage 0/1 package verdicts

Date: 2026-10-29. **Benchmark and all eleven strategy candidates: NOT READY.**
No investment recommendation, permission to trade, or portfolio risk certificate is issued.

This is a review of delivered discovery packages, not a completed week-long strategy study. Missing evidence is not a finding of zero profit or proof a strategy is impossible.

## Immutable review basis

- Scout A yield package: [`0767bcc1cb2b01d3dfc732fc7ed3c8b9f625652f`](https://github.com/vaikmr/swarm-search/commit/0767bcc1cb2b01d3dfc732fc7ed3c8b9f625652f). Reviewed the four hypothesis documents, source-register scope, nominal allocation and stored histories.
- Lower-deployment follow-up: [`18370d81039303e86263dc998c87164d8d75226e`](https://github.com/vaikmr/swarm-search/commit/18370d81039303e86263dc998c87164d8d75226e). Reviewed its study note and stored deployment-identity metadata; the judge did not rerun the public RPC collector or independently certify its recorded identity/audit assertions.
- Scout B execution package: [`de66cf76787cbc731b85cb4b9513b7ebbfd6bb55`](https://github.com/vaikmr/swarm-search/commit/de66cf76787cbc731b85cb4b9513b7ebbfd6bb55). Reviewed all eight hypotheses, source registers, discovery summary and collector tests.
- Entrant capacity: [`7f8dfae10f8816a3686ec79e5d7aecc64915ed54`](https://github.com/vaikmr/swarm-search/commit/7f8dfae10f8816a3686ec79e5d7aecc64915ed54). Reviewed access versus capture distinctions, capital bounds and reproducible tests.
- Risk tools and accounting/simulator corrections: exact checked revisions and limits are recorded in [the simulator review](SIMULATOR_REVIEW.md) and [follow-up dispositions](FOLLOWUP_DISPOSITIONS.md).
- Decisions use the independent [G0–G8 rubric](AUDIT_RUBRIC.md). Scout/capacity priority suggestions do not determine the judge's verdict.

The judge independently reran seven yield tests, seven execution-collector tests and nine capacity tests at their separate immutable revisions. The nominal lending allocation's stored component and aggregate gross arithmetic was reproduced offline from its histories; its net and benchmark excess remained `null`. This validates that specific T4 calculation, not a depositor's return.

The judge also independently retrieved the official [CoW bonding-pool documentation](https://docs.cow.fi/cow-protocol/reference/core/auctions/bonding-pools), confirming the documented stable-asset components of the standalone and reduced self-funded routes. Even the reduced route exceeds the study's single-protocol capital cap before its COW requirement. This excludes those routes, **not all solver admission models**.

## Gate disposition

| Gate | Independent disposition |
| --- | --- |
| G0 safety/scope | Supplied work is discovery/offline research. No live trading authorization is inferred; excluded chain/strategy paths cannot be reintroduced by a promising lead. |
| G1 provenance/claims | Public samples, documentation and T4 arithmetic are useful inputs only. Paper-reported PnL, contract labels, source timestamps and metadata flags do not establish performance tiers. |
| G2 benchmark/capital | No executable, net-priced and look-through-compliant benchmark allocation is established. Nominal chain/protocol/coin caps are insufficient. |
| G3 actor integrity | No delivered actor package reconciles qualifying opening/closing equity, external flows, all related inventory/hedges and costs. T1 is preferred, not a substitute for mandatory T2 plus T3. |
| G4 replay/capacity | No genuine qualifying fork/state replay exists. Entrant admission, realistically won flow, full portfolio carryover and every required latency/gas/competition stress remain unestablished. |
| G5 economics | Complete candidate net PnL and comparable net benchmark are unknown. No strategy's required net-excess hurdle is established. Correct helper arithmetic is not supplied strategy cost provenance. |
| G6 risk | Look-through exposures, collateral/exit paths and required monthly/tail-risk evidence are incomplete. Conditional severity or an empirical percentile is not an event-probability certificate. |
| G7 forward paper | No genuinely elapsed, frozen-logic qualifying forward-paper package is delivered. One-shot observations, synthetic fills and elapsed timestamp metadata do not suffice. |
| G8 final review | No candidate is eligible for recommendation; unresolved noncompensatory gates cannot be offset by a score or optimistic model. |

The benchmark is a comparator, not a strategy required to beat itself. Its own feasibility, net cost and risk evidence still must be established before a candidate can pass a comparable-net-excess test.

The lower-deployment follow-up narrows the lending study and supplies stronger recorded deployment-identity inputs, but still leaves actual reserve custody, current audited-build equivalence, all-in costs and portfolio paths unresolved. Its annual principal-plus-cost scenario is a **conditional component budget**, not satisfaction or failure of the separate annual tail gate: arithmetic alone supplies no occurrence probability. Likewise, an opening-capital loss fraction does not prove a running-peak monthly drawdown bound. The follow-up changes neither the benchmark verdict nor the absence of qualifying T2/T3.

## Individual dispositions

All rows share the absent qualifying T2/T3 and unestablished risk/economic gates above.

| Package | Verdict | Distinct next evidence gate |
| --- | --- | --- |
| [Lending benchmark](../strategies/benchmark-lending/verdict.md) | NOT READY; nominal-cap arithmetic only | Specific vault/market eligibility, dated look-through and reserve custody; same allocation's complete net entry/exit and inventory marks. |
| [Cross-chain relaying](../strategies/cross-chain-relaying/verdict.md) | NOT READY; attributable fill leads only | Complete fill-to-refund actor ledger, outstanding claims and actually accessible open/step-in flow. |
| [Cross-chain arbitrage](../strategies/cross-chain-arbitrage/verdict.md) | NOT READY; historical receipt pointers only | Both-leg inventory, failed/partial legs, rebalancing and entrant timing on an allowed route. |
| [Long-tail arbitrage](../strategies/long-tail-arbitrage/verdict.md) | NOT READY; infrastructure-contract lead only | Current eligible pool/token universe and caller-attributed rewards/costs, not dashboard labels. |
| [Auction backrunning](../strategies/auction-backrunning/verdict.md) | NOT READY; mechanism/dataset leads only | Allowed contestable niche, real executors and decision-time hints; user refunds are not searcher income. |
| [Liquidations](../strategies/liquidations/verdict.md) | NOT READY; actor-contract leads only | Qualifying market events, actual liquidator versus protocol cleanup, collateral disposal and losing races. |
| [Intent solvers](../strategies/intent-solvers/verdict.md) | NOT READY; specific self-funded routes excluded | Accepted permitted admission or demonstrably accessible public fills; actual executor/reward attribution. |
| [Funding/basis](../strategies/funding-basis/verdict.md) | NOT READY; signed funding component only | Spot/perp capital and collateral ledger, basis/marks, changing funding, liquidation path and all trading/rebalancing costs. |
| [Hedged LP](../strategies/hedged-lp/verdict.md) | NOT READY; bounded venue screen only | Specific eligible LP with an identified hedge account; tick/inventory/funding/fee total equity, not fee APY. |
| [Fixed/variable yield](../strategies/fixed-variable-yield/verdict.md) | NOT READY; market/rate quote history only | Actual PT/SY prices, redemption units, holdings, underlying eligibility and early-exit/default/mark risks. |
| [Keeper bounties](../strategies/keeper-bounties/verdict.md) | NOT READY; registration/admission documentation only | Current paid-operator access, funded eligible jobs and actual operator rewards versus reimbursements/costs. |
| [CEX–DEX arbitrage](../strategies/cex-dex-arbitrage/verdict.md) | NOT READY; off-chain leg unobserved | Permitted contestable niche and actual CEX access, depth, fees, fills and inventory; requires CEX access. |

## Interpretation and bounded next work

- The nominal three-chain maximum is a ceiling, not a requirement to deploy all possible capital or a proof of independence. More idle cash is permitted; its actual custody/freeze/issuer exposure must be specified.
- Shared Ethereum settlement and stablecoin/wrapper exposure are unresolved, not universally assumed to cause total loss. Do not invent a backing coefficient, joint-loss probability or independence assumption.
- A below-threshold venue screen excludes that ordinary-eligibility route unless properly labeled higher risk; it does not show the strategy family unprofitable, and a higher-risk label does not waive concentration or drawdown rules.
- Empty open-order snapshots do not negate actual filled-order samples. Neither counts as entrant capture or future profit.
- CoW sponsorship, public UniswapX filling and delegated 1inch admission are distinct routes. No access, sponsorship, delegation or CEX account was obtained.
- Historical APY/funding/PT quotes and successful receipts are not realized economic returns. No numerical target probability, risk-adjusted return ranking or attainable market share is certified.

The useful next work is to establish a genuinely feasible net benchmark and obtain a complete actor/accessible-flow ledger before commissioning qualifying historical replay and elapsed paper work. Existing discovery leads may guide that collection; they are not approved strategies. **The target remains unsupported by this package, not disproven for every possible implementation.**
