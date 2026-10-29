# Long-tail DEX arbitrage — independent risk specification

Date: 2026-10-29. Status: **not risk-certified; token eligibility and safe unwind evidence missing**.

All eight scenarios and both gates in the [shared review](../../risk/README.md) apply. This is not a verdict, vulnerability investigation or performance study.

## Candidate-specific failure paths

- Thin liquidity and token-specific transfer restrictions can turn quoted spreads into unexitable inventory. New, unaudited or undersized protocols are outside the ordinary eligibility rules and must be explicitly higher risk; niche status is not an exemption.
- Pool turnover and gross wallet receipts are not realized net profit. Tokens and pools requiring live probes, exploit investigation or manipulation are not research opportunities in this study.
- Atomic legitimate swaps limit partial-leg exposure only if all actions truly revert together; preexisting inventory, approvals, gas and local software remain separate exposures.

## Required tests and mitigations

Use a predeclared eligible-asset universe, public contract/version metadata and historical execution evidence. Model lawful atomic revert versus asynchronous failure distinctly. Apply depeg, bridge-representation loss, stale oracle/data, gas shocks, chain halt, parameter changes and larger-competitor capture. No probability or executable depth is inferred from a chart or quoted reserve.

For non-atomic inventory, measure adverse unwind using actual depth and accessible venues. A CEX hedge/rebalance adds custody and freeze risk ([CFTC context S06](https://www.cftc.gov/PressRoom/PressReleases/8638-22)). Do not rely on a stop-loss to trade through a halt ([Arbitrum context S03](https://status.arbitrum.io/clq6te1l142387b8n5bmllk9es)).

**Reassessment inputs:** eligible market/token list, independent audit scope, ordinary trading permissions, token behavior metadata, depth/unwind output and proven accessible trade selection. Unknown safety or missing profitable actors means unverified, not proof that the niche is unprofitable. No tail-frequency estimate is supplied.
