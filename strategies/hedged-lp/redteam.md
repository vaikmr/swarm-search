# Hedged concentrated-liquidity LP — independent risk specification

Date: 2026-10-29. Status: **not risk-certified; dynamic inventory, LVR and hedge-failure evidence missing**.

Apply all eight scenarios and both loss gates in the [shared review](../../risk/README.md). CEX dependence must be flagged if the hedge uses one.

## Candidate-specific failure paths

- LP delta is state dependent. A fixed opening hedge does not neutralize changing inventory. At a range boundary the position can become one-sided; a depeg can increase holdings of the impaired asset rather than merely apply a haircut to the initial allocation.
- Fees are not net profit: LVR/adverse selection, inventory mark-to-market, range exits, rebalances, funding/borrow, gas and hedge slippage must all be included without double counting.
- A halted venue or auto-deleveraged hedge can break an otherwise neutral portfolio ([S08](https://docs.dydx.xyz/concepts/trading/contract-loss-mechanism), [S09](https://www.dydx.xyz/blog/october-2025-dydx-chain-incident-review-community-update)).

## Required tests and mitigations

Replay pool state and actual active liquidity with the exact range/rehedge policy, not terminal prices only. Stress both directions through range boundaries, depeg, bridge-wrapper loss, stale oracle/reference data, gas shocks, reward/fee changes, chain halt and a larger LP/searcher competitor. Freeze any CEX transfers or hedge access.

Recompute concentration through time as assets accumulate. Budget adverse exit depth and externally accessible margin; bound protocol and issuer exposure across the LP and hedge together. Do not claim deterministic downside protection from concentrated-liquidity math alone.

**Reassessment inputs:** actual pool/hedge paths, fee ownership, active depth, execution/rebalance costs, LVR attribution, dynamic exposure ledger and joint failure output. No event probability, actor return or statistically estimated monthly bound is supplied.
