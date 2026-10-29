# Delta-neutral funding/basis — research candidate, not approved

**Stage:** 0/1. **Highest performance evidence:** T4 constant-notional funding
arithmetic. **T1/T2/T3:** not established.

Long spot and short the corresponding perpetual to collect positive funding,
while accepting execution/basis risk, negative funding and liquidation risk.
Delta neutrality is not absence of loss. A short marked against fixed collateral
can be liquidated even while spot appreciates elsewhere; the spot gain may not
be transferable in time.

## Actual public history, deliberately incomplete economics

Public Hyperliquid `fundingHistory` was paginated over a complete ninety-day
hourly window ending immediately before 2026-10-29 07:00 UTC. Each asset has
2,160 ninety-day observations and 720 thirty-day observations, with no detected
gap exceeding 3,700 seconds. Exact times, page request bodies/hashes and rate
samples are in [`evidence/`](evidence/).

| Asset | 30d funding sum | 30d receipts on constant $30k short notional, T4 | 90d receipts on same notional, T4 | Negative hours in 30d |
| --- | ---: | ---: | ---: | ---: |
| ETH | 0.63427053% | $190.28 | $647.04 | 71 |
| BTC | 0.70643530% | $211.93 | $633.41 | 45 |

This is **only** `notional * sum(hourly funding fractions)`: not actor PnL,
not a backtest, not replay and not fill simulation. Constant USD notional implies
rebalancing whose costs and spot/mark-to-market changes are unmodeled. Entry/exit
fees, basis, hedge error, gas/bridges, funding on collateral, failed fills,
infrastructure and liquidation are excluded, not assumed zero. A small endpoint
choice or revised hourly sample can change the result; use the stored times.

A spot/perp implementation entirely on Hyperliquid may violate the single-chain
and protocol cap even if leverage is low. A nominal construction with $30k spot
split across two chains and $15k margin on a third would put the short at 2x
collateral, reserve $5k cash and require separate settlement/issuer look-through.
This is a constraint illustration, not a risk-certified construction. No CEX is
intrinsically required for a DEX-only route; **any spot or hedge leg on a CEX
requires CEX access** and adds withdrawal/custody/jurisdiction risks.

## Actual operator leads, not observed net PnL

- [Neutral Trade, Hyperliquid Funding Arb](https://docs.neutral.trade/for-capital-allocators/market-neutral/hyperliquid-funding-arb.md)
  explicitly describes spot/perp hedges and a separate HLP allocation, live since
  June 11, 2025. Its [app](https://www.neutral.trade/strategies/hlfundingarb)
  exposes monthly performance, but account/bridge/fee reconciliation is absent
  here and HLP mixes another strategy into returns. Public protocol-screen TVL
  was about $23.14M, below the ordinary $50M venue requirement if using the vault
  provider. A dashboard does not qualify as T1.
- [OK-BITOK](https://www.ok-bitok.com/) identifies vault
  `0xD772A28caf98cCF3c774c704cA9514A4914b50A0`, claims daily contract NAV data,
  and says operation began December 11, 2025. This is a public actor/address
  lead, not independently verified custody or returns. At the study date it
  fails the twelve-month rule and advertises very small TVL; its
  [security page](https://docs.ok-bitok.com/vault-infrastructure/security/)
  does not itself supply the required third-party public audit.
- Ethena's [backing explanation](https://docs.ethena.fi/backing-assets/overview)
  confirms delta-hedged backing as an institutional strategy lead, but its
  off-chain hedges and custodian books cannot be reconstructed from on-chain
  USDe mint/redeem flows alone. USDe/sUSDe holder yield is not the operator's
  pure funding/basis PnL or a new entrant's capture.

Do not infer that no profitable actors exist. The bounded search has not
produced a fully reconciled fourteen-day account package.

## Next evidence gate

Select one venue/asset/fee tier and real operator with public complete ledgers.
Reconcile spot inventory, perp fills, funding, transfers, entry/exit marks and
capital including margin. Then test historical executable depth and adverse
margin/basis scenarios with actual fees before any seven-day paper run.
No measured net return or risk-adjusted ranking can yet be assigned.
