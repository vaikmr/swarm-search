# Fixed/variable yield — public quotes, no return recommendation

**Stage:** 0/1. **Evidence:** T4 market snapshots and historical quoted APYs.
**T1/T2/T3:** not established.

Buy a Pendle principal token below its eventual redemption claim and hold to
maturity, or compare implied fixed yield to the matching floating underlying
yield. A quoted spread is not free arbitrage. The redemption unit, maturity,
underlying credit/depeg risk, liquidity, fees and mark-to-market must match.
Levered rate trades add borrowing-rate, liquidation and roll risk.

## Retrieved markets and historical rates

The official [cross-chain market API](https://api-v2.pendle.finance/core/v2/markets/all?limit=100&skip=0)
was paginated across all 833 reported records, including expired markets.
The evidence filters **unexpired**, API `stables` category, and Ethereum,
Arbitrum or Base. This category is provider metadata, not proof that the
underlying is safe or itself eligible.

The snapshot includes actual market addresses. Examples of T4 quoted implied APY:

| Market | Chain and market address | Expiry | Implied APY |
| --- | --- | --- | ---: |
| sUSDS | Ethereum `0x9c560ebaf78e596cbcc27411d633a74d628dd7dc` | 2026-11-26 | 5.6394% |
| sUSDe | Ethereum `0x47ad2cd1dd15739a7a035b9d3b7828d916fef77e` | 2026-11-26 | 4.7292% |
| siUSD | Ethereum `0xd44f2630260ff3805d7cb317d4f6740b0044c408` | 2027-01-07 | 9.3681% |
| reUSDe | Ethereum `0x90b70c407f1077f8eb92bf423b44cd92329b737a` | 2026-12-10 | 18.8292% |

These quotes are not executable fills, net annual returns, or established
eligibility of newer/riskier underlying issuers. Protocol-wide Pendle TVL was
about $1.071B in the timestamped protocol API snapshot. Public
[audit records](https://www.chainsecurity.com/security-audit/pendle-v2-core/)
exist; exact live market/SY/underlying coverage still must be linked.

The official sUSDS market endpoint returned **91 daily observations** from
2026-07-31 through 2026-10-29 00:00 UTC. Historical implied/underlying APY and TVL
are preserved. Historical quoted APYs are not a PT total-return series; this
package does not integrate changing implied APY as if a PT position earned
that changing rate. Needed instead: actual entry/exit PT/SY prices, units,
exchange rates, fees, claims and maturity redemption.

## Actor search and missing economics

Actual market contracts are identified, but counterparties' complete wallet
ledgers have not been reconstructed. A token-holder list or public portfolio
dashboard alone cannot identify beneficial ownership, external hedges or
realized after-cost return. Neither a governance-token whale nor a market
contract itself is evidence of a profitable fixed-yield trader.

No T1 return, frequency, capital efficiency or competitor count is claimed.
The nominal $15k cap on Pendle itself applies across all its markets together;
splitting among several PTs does not diversify that protocol exposure. Underlying
stablecoin and wrapper exposures must also be counted across lending/funding
positions. The observed higher implied APYs do not justify ignoring the tail
constraints or the $300 net-excess simulation gate.

## Next concrete test

Choose a mature eligible underlying, fetch actual PT/SY price history and pool
state, identify holders/settled trades, and reconstruct a hold-to-maturity
position with entry liquidity and costs. Compare against the **same capital's**
net lending alternative. Test early-exit yield repricing, underlying depeg and
redemption delay separately. No recommendation before T2 plus qualifying T3.
