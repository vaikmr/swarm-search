# Strategy board

**Search closed at the user's request, 2026-10-29.** No qualifying T1/T2/T3 performance package or strategy recommendation was established. The missing evidence below is not scheduled work. See the [early closeout](FINAL_REPORT.md); the [interim report](STAGE01_REPORT.md) is a historical checkpoint.

States distinguish `unverified`, `keep-for-testing`, `killed`, and `evidence-qualified`. A candidate with missing data stays unverified unless an independent hard-constraint failure establishes rejection. Returning no qualifying strategy is valid.

| Slug | Candidate | Current state | Missing evidence / unscheduled gate |
| --- | --- | --- | --- |
| `benchmark-lending` | Blue-chip stablecoin lending baseline | Unverified | Current and 30/90-day rates, eligible markets, net total-capital benchmark |
| `cross-chain-relaying` | Cross-chain relaying and intent filling | Unverified | Identified actors, realized capital-adjusted PnL, competition and bond/lock requirements |
| `cross-chain-arbitrage` | Inventory-based cross-chain DEX arbitrage | Unverified | Pre-positioned inventory, no hot-path bridging; rebalancing and lost-race costs |
| `long-tail-arbitrage` | Long-tail DEX arbitrage | Unverified | Contestable legitimate niche, liquidity, token risk, observed actor economics |
| `auction-backrunning` | Lawful order-flow auction backrunning | Unverified | Access rules, win rates, refunds, failed/losing bids and incumbent advantage |
| `liquidations` | Smaller-market legitimate liquidations | Unverified | Eligibility, competition, execution costs; no oracle manipulation |
| `intent-solvers` | CoW, UniswapX, Fusion and other solvers | Unverified | Admission/bond requirements, realistic fills, capital lock and settlement risk |
| `funding-basis` | Delta-neutral funding/basis | Unverified | Funding history, borrow, mark-to-market, margin/liquidation and CEX dependence |
| `hedged-lp` | Hedged concentrated-liquidity LP | Unverified | LVR/impermanent loss, hedge costs, turnover, fee attribution |
| `fixed-variable-yield` | Yield tokenization and rate arbitrage | Unverified | Executable depth, maturity/exit, basis and protocol dependencies |
| `keeper-bounties` | Keeper and automation bounties | Unverified | Available work, payout attribution, access, gas and competition |
| `cex-dex-arbitrage` | CEX-DEX arbitrage | Unverified | Slower-than-incumbent capture, CEX fees/access/withdrawals and inventory risk |

No claim of attainable monthly profit, proven drawdown protection, or profitability ranking is made by this initial board.

Each candidate now has a `strategies/<slug>/hypothesis.md`, independent `redteam.md` and judge-owned `verdict.md`. The [consolidated independent verdicts](review/STAGE01_VERDICTS.md) preserve all twelve NOT READY decisions. Evidence directories contain source notes, bounded public samples or explicit gaps. Unknown net returns are not zero.

Route-level finding: CoW's documented self-funded bonding routes exceed this capital budget. This does not reject all intent solving or establish that the separate sponsored route is accessible. Across and UniswapX have useful attributable discovery samples, not demonstrated entrant profit.
