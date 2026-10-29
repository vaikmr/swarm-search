# Legitimate smaller-market liquidations

Stage: discovery only. Status: **unverified**. No qualifying T1/T2/T3.

## Hypothesis

Established smaller lending markets might have legitimate liquidation work that
incumbents do not serve economically. The liquidation bonus is a gross spread,
not net profit. No oracle manipulation, vulnerability research or borrower
front-running is permitted.

## Actor leads

[Bitquery's public liquidation investigation](https://bitquery.io/investigations/defi-liquidation-bots)
lists contract-level liquidation actors. Treat its volume and concentration
statistics only as leads until independently queried. Public contract leads:

- `0xf0570ec48d03171a80ff796dceadf0d385a00004`
- `0x00000000009e50a7ddb7a7b0e2ee6604fd120e49`
- `0x36331e299247e5d0d3261e1d9852f6e0cffee95c`

No legal owner is inferred. No independent capital or PnL attribution has been
completed. These Ethereum leads do not establish a contestable L2/smaller-market
niche.

The same source identifies
[`ClinicStewardV2`, `0x6a14ebe9a934c8efe15c3811a999149472876b56`](https://etherscan.io/address/0x6a14ebe9a934c8efe15c3811a999149472876b56#code)
as Aave's cleanup infrastructure. **Do not count protocol-directed debt cleanup
as a profitable independent liquidation competitor.**

## Competition and costs

[Chainlink SVR](https://docs.chain.link/data-feeds/svr-feeds/searcher-onboarding-ethereum.md)
describes auctioned liquidation backruns and value recapture. The existence of an
oracle update does not grant a new bot priority or establish its winning bid.
Flash liquidity, when used, still requires accounting for fees, slippage, execution
gas and any builder payment; it does not prove the risk constraints.

## Next gate

Start from actual `LiquidationCall`/market-equivalent events, enumerate recipients
and callers separately, reconcile all collateral sale and debt acquisition flows
with receipts and reverts, and retain loss-making/unwon opportunities. Verify market
TVL, age and audit eligibility and current auction/admission conditions. No
qualifying actor history or complete liquidation-cost ledger has been retrieved.
