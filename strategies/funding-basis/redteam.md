# Delta-neutral funding/basis — independent risk specification

Date: 2026-10-29. Status: **not risk-certified; cross-venue margin and joint-tail evidence missing**.

Apply all eight scenarios and both loss gates in the [shared review](../../risk/README.md). **CEX access is required if any leg/collateral is on a CEX**; a DEX-only variant has its own dependencies and is not automatically equivalent.

## Candidate-specific failure paths

- Spot and perp delta can cancel economically while each venue independently liquidates. Mark/index/basis divergence, collateral depeg, borrow recall and funding reversal can force a close at a loss.
- CEX cash, margin, spot and unsettled transfers share the same custody domain. The historical FTX complaint illustrates why account-level marks do not guarantee accessible assets ([S06](https://www.cftc.gov/PressRoom/PressReleases/8638-22)).
- Automatic deleveraging can close the profitable hedge leg and leave residual exposure ([S08](https://docs.dydx.xyz/concepts/trading/contract-loss-mechanism)). Halt/oracle recovery risks exist even without CEX custody ([S09](https://www.dydx.xyz/blog/october-2025-dydx-chain-incident-review-community-update)).

## Required tests and mitigations

Replay both legs, funding, borrow accrual, liquidation fees, collateral prices, basis and margin rules in time order. Freeze transfers from the profitable venue while the losing venue demands margin; deny the assumed rescue. Stress reversed funding, haircut/parameter changes, larger competitor/capital inflow, depeg, stale oracles, gas, bridge delay and a chain halt.

Use only the charter-permitted delta-neutral leverage, measured transparently using gross notional and actual collateral. Pre-position survival margin inside each allowed failure-domain cap. A stop-loss or emergency rehedge is not guaranteed during a venue halt.

**Reassessment inputs:** exact margin/ADL rules, borrow source, funding/price path, venue access eligibility, allocation and worst joint cashflow. No annual failure frequency or 99% monthly pathwise drawdown bound is established.
