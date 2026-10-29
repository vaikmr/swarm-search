# Lending evidence and reproduction

## Sources and scope

- [DefiLlama current pools](https://yields.llama.fi/pools): current APY/base/reward,
  chain, underlying assets, pool identifiers and pool-level net TVL.
- `https://yields.llama.fi/chart/{pool}`: daily historical APY samples.
  [`rate-summary.json`](rate-summary.json) links every source and time window.
- [Protocol API](https://api.llama.fi/protocol/aave-v3), with analogous
  `compound-v3`, `morpho-blue` and `pendle` slugs: protocol TVL, first TVL
  observation and audit links. First observation is not proof of deployment.
- [Aave security](https://aave.com/security),
  [Compound III audit](https://blog.openzeppelin.com/compound-iii-audit),
  [Morpho audits](https://docs.morpho.org/get-started/resources/audits/):
  public review records, not a guarantee of safety or exact deployment linkage.

T4 current base APYs from the 2026-10-29 snapshot:

| Market | Base APY | Trailing 30d time-weighted base APY | Trailing 90d time-weighted base APY |
| --- | ---: | ---: | ---: |
| Aave Ethereum DAI | 3.35682% | 3.33502% | 3.10902% |
| Compound Arbitrum USDT | 2.37203% | 2.39388% | 2.39514% |
| Morpho Base SparkUSDC | 5.56637% | 4.14942% | 3.97713% |
| Aave Ethereum USDC | 4.17536% | 3.89502% | 3.61541% |
| Compound Ethereum USDC | 4.34553% | 4.65497% | 4.45679% |

The last two rows are comparison markets, not additional allocated positions.
Numbers are computed from samples rather than copying the feed's `apyMean30d`,
which may use a different window or weighting. `apyReward` is not included.
USD-on-$50k columns retained inside the summaries are explicitly **invalid
single-pool concentration illustrations**, never a portfolio recommendation.

The Aave, Compound, Morpho and Pendle protocol snapshots respectively reported
approximately $16.326B, $1.334B, $11.203B and $1.071B TVL. Their exact values and
source timestamps are in the eligibility JSON. These are protocol totals, not
the amount safely withdrawable from the selected pool.

## Observed actors, no T1 PnL

[`actor-leads.json`](actor-leads.json) contains the first ten entries of the
first public Blockscout holder page for verified token address
`0x98C23E9d8f34FEFb1B7BD6a91B7FF122F4e16F5c`
([metadata](https://eth.blockscout.com/api/v2/tokens/0x98C23E9d8f34FEFb1B7BD6a91B7FF122F4e16F5c),
[holders](https://eth.blockscout.com/api/v2/tokens/0x98C23E9d8f34FEFb1B7BD6a91B7FF122F4e16F5c/holders)).
This query did return current on-chain accounts, including an account labelled
`AaveV3Lender` at `0x7D7F72d393F242DA6e22D3b970491C06742984Ff` and
`Yield Bearing AAVE USDC` at `0xD2011d314aCAA68E5401E7f5AeC3Be6d2C574DCf`.
These are explorer labels, not identified beneficial owners or verified strategies.
Large raw aToken balances are not net capital or realized profit; borrowers,
vault depositors and transfers must be reconciled. The holder list is partial.
These initial holder records alone contain no fourteen-day reconciled net-PnL
result. The later partial ledger linked below remains explicitly scope-limited.

## Run

```sh
python3 strategies/benchmark-lending/sim/fetch_public_rates.py
python3 strategies/benchmark-lending/sim/build_candidate_allocation.py
python3 -m unittest discover -s strategies/benchmark-lending/sim -v
```

Only public read endpoints are used. Snapshot metadata records full-response
hashes and retains bounded ninety-day excerpts plus one pre-window observation
for offline reproduction. `selected-pools.json` distinguishes a cached response's
original observed-time basis from the later calculation time.

Each interval uses:

```text
log_growth += ln(1 + base_apy_pct / 100) * interval_seconds / (365 * 86400)
gross_usd = position_capital * expm1(log_growth)
```

The unit tests are synthetic arithmetic tests, not performance evidence. Exact
cost accounting remains owned independently; absent fees are unknown, not zero.

## Actual holder follow-up

The later [fourteen-day public holder ledger](../actor-ledger.md) adds actual
historical state, token-index checks, transfers, receipts, observed network fees
and historical oracle marks. These are explicitly scoped account components,
not APY arithmetic, full-firm equity, certified T1, fork replay or paper trading.
Its actual-input regressions are distinguished from synthetic arithmetic tests.
