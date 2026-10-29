# Lending/funding inputs and read-only paper observation

Stage 0/1 tooling only. There is no live-trading code, key handling, contract
deployment, transaction construction, transaction signing, or broadcasting.
The only Hyperliquid POSTs go to the **read-only `/info` endpoint** with
allowlisted market-data types. No exchange/order endpoint is implemented.

## What actually ran

On 2026-10-29 UTC, the public DefiLlama pool/chart, Hyperliquid funding/book,
and Coinbase BTC-USD book endpoints were reachable without account credentials.
The attached snapshots retain source URLs, request parameters, retrieval times,
HTTP dates, response hashes, and compact public-data excerpts. A response hash
is not independent proof of source authenticity or receipt time.
`paper_yield_manifest.json` hashes the delivered files for independent integrity
checking; it does not replace upstream response hashes or certify evidence tiers.

- `yield_sample_20261029.json`: three lending pool histories and gross T4
  calculations over 30 and 90 days ending at each latest source timestamp.
- `yield_funding_sample_20261029.json`: five bounded requests, 2,160 contiguous
  hourly BTC funding rows over 90 days, and gross funding-component calculations.
- `paper_sample_20261029.json`: one live read-only observation. It rejected all
  paper fills. There was no configured strategy/cost model, and the Coinbase
  REST level-2 response did not supply a source event timestamp.

No unattended seven-day job was started. The observation duration is zero days,
with no position, fill, or strategy return. **None of these files establishes
T1, T2, or T3 performance, a recommendation, or a 99% monthly risk guarantee.**
Tests use synthetic fixtures and are not market-performance evidence.

## Lending calculation

`lending_carry` compounds the base APY known at the **left** sample of each
historical interval:

`gross = capital * expm1(sum(log1p(base_APY/100) * seconds / (365*86400)))`

Points must bracket the entire interval. Missing base APY, duplicate/reversed
timestamps, and sample gaps over 36 hours fail closed; there is no extrapolation,
fallback to incentivized total APY, or use of a future APY. Reward tokens are
excluded. Default/depeg/withdrawal liquidity, deposit caps, actual liquidity-index
state, and execution/gas are not replayed: this is **T4**, not T2.

The hypothetical $50,000 in one pool is an **inadmissible-concentration comparator**,
not a proposed allocation. Unknown costs suppress the net output (`null`).
If a caller explicitly supplies zero costs, that does not prove fees/operations
are free. The net-model fields deduct only supplied costs and must not be
presented as verified all-in net profit. Map complete capital/cost boundaries
to the separate canonical cost ledger before reporting cash-net or benchmark excess.

Every historical point was retrieved **after** the historical cutoff (exact
cutoffs and request times are recorded). Left-point integration avoids using
the next sampled APY, but historical API timestamps do not establish original
publication time or protect against later revisions. Point-in-time availability
and publication latency remain unverified. Full-response hashes refer to the
upstream bytes, not the compact excerpts.

## Funding calculation

Positive Hyperliquid funding rates are modeled as cash received by a constant
short notional; negative rates are paid. `gross = notional * sum(hourly_rates)`.
The sample's $15,000 short notional is a component comparator, not an allocation.
It omits hedge acquisition/financing, spot/perp basis and mark-to-market,
liquidations, fees and realistic fills. The result is **not delta-neutral
strategy PnL**. Unknown all-in costs suppress net-component outputs. Historical funding payments do not prove a new entrant could
hold the position safely or earn the cash flow.

Requests are inclusive at both ends. Pagination resumes at the last timestamp
plus one millisecond, rejects overlap/non-progress, and has a hard page bound.
Coverage checks require the exact epoch-aligned hourly grid and event count
inside each **inclusive** nominal window, including its first and last scheduled
events. The timestamp tolerance applies only to event jitter, not to missing
boundary payments; it cannot replace an omitted event with an edge allowance.
Actual source timestamps must also lie inside the queried bounds. A cutoff
close enough to an hourly boundary that the source event straddles it fails
closed instead of pretending its inclusion is unambiguous. Empty histories,
shifted phases, missing/duplicate/reversed events and incomplete edges are rejected.
Epoch-hour phase is an explicit adapter assumption checked against every input
row, not inferred from whichever first row happened to arrive.
Complete rate history still is not T2 replay.

Independent review found that the initial adapter accepted a synthetic omitted
window-edge event. The correction replaced its edge-distance allowance with
exact scheduled-event checks and added boundary/unaligned-cutoff regressions.
The committed BTC sample is separately revalidated against the stricter grid.

## Run focused tests

From the repository root, using Python 3.10+ and only its standard library:

```sh
python3 -m unittest discover -s tests -p 'test_yield*.py' -v
python3 -m unittest discover -s tests -p 'test_paper*.py' -v
git diff --check
```

## Re-fetch public inputs or take one observation

Output files below are local generated evidence, not an instruction to publish
large datasets. These commands do not place any order or move any funds.

```sh
python3 -m research_tools.yield_data chart \
  aa70268e-4b52-42bf-a116-608b370f9501 --out /tmp/aave-usdc-chart.json

python3 -m research_tools.yield_data funding --coin BTC \
  --start-ms 1785482194383 --end-ms 1793258194383 \
  --out /tmp/btc-funding-90d.json

python3 -m research_tools.paper_observer --out /tmp/paper-observations.jsonl
python3 -m research_tools.paper_observer --audit /tmp/paper-observations.jsonl
```

The observer stores full raw public responses locally, including failures.
The committed observation is a clearly labeled compact excerpt, not a complete
order-book archive. Hash-chain audit detects accidental edits/removals inside
the supplied log; rewriting a complete log or deleting its final records is
not detectable without an independent external anchor. Use a single writer.

`executable_quote` is a pessimistic visible-depth **T4 estimate**, not a fill
engine. It consumes explicit fee/latency/adverse-price assumptions, rejects
stale/future books and insufficient depth, and charges the worst consumed price.
Latency is not actually replayed: a real strategy must observe another book
after the modeled delay and reconcile both legs, size rounding, margin and costs.
`mark_to_market` supplies bid-for-long/ask-for-short accounting only; it is
not a risk engine.

## Still needed before T2/T3

1. A selected, independently screened strategy and an admissible allocation,
   including shared-chain/protocol/stablecoin/bridge dependencies.
2. At least 30 days of protocol state and executable bid/ask history, including
   volatile periods, exact fee schedules, failed-fill/margin/liquidation state,
   and conservative latency/competition behavior. Rate integration alone cannot
   supply this.
3. A timestamped spot feed synchronized to the perp feed. Coinbase REST receipt
   time or HTTP `Date` does not certify the age of the order-book state.
4. Frozen/versioned decisions, explicit all-in costs, a two-leg paper ledger,
   fills after delay with inventory/cash reconciliation, liquidation-side MTM,
   missing-data halts, and externally anchored observation logs.
5. At least seven **elapsed wall-clock days**, reviewed sampling coverage, and
   independent evaluation against replay predictions. The included gate checks
   minimum elapsed time, sequence/gaps, logic version, failures and fill presence;
   passing it only permits review, never automatically awards T3.

No scheduler, paid service, mainnet deployment, or trading activation is included.
Funding-with-Coinbase would require a CEX account if it were ever separately
approved for live use; the current public market-data reads do not.

## Sources

- [DefiLlama public pools](https://yields.llama.fi/pools)
- [Aave Ethereum USDC history](https://yields.llama.fi/chart/aa70268e-4b52-42bf-a116-608b370f9501)
- [Compound Ethereum USDC history](https://yields.llama.fi/chart/7da72d09-56ca-4ec5-a45f-59114353e487)
- [Aave Arbitrum USDC history](https://yields.llama.fi/chart/d9fa8e14-0447-4207-9ae8-7810199dfa1f)
- [Hyperliquid info API and pagination](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)
- [Hyperliquid historical funding API](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals)
- [Hyperliquid hourly funding rules](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/funding)
- [Coinbase BTC-USD public REST book](https://api.exchange.coinbase.com/products/BTC-USD/book?level=2)
