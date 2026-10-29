# Public data reality and the perp-hedged bridge counterfactual

**As of 2026-10-29. No PnL replay was run and no profitable strategy was established.**

The useful result is an identification gate, not a backtest: the reported
21-trade day still lacks a recoverable full actor/date/transaction/token manifest.
Free **current** public market data works, but current metadata and books cannot
create historical hedge markets or executable prices. The separate Appendix G
loan case must not be substituted for that sample.

This package also found a genuinely recent non-EVM rail change: Circle announced
EURC Gateway support and a Solana pre-mint account on **2026-10-23**. A bounded
public RPC read corroborates that account's present state, not route profit.

## 1. What was actually read and checked

The four assigned priority references were read at their precise current-page
scope: R005 Allium homepage, R006 Allium Prices overview, R026 Dune homepage and
R031 the full Mempool Dumpster README. These are not claims to have read every
linked report, all product docs, all repository code, or a historical 2025 page
snapshot. All nine assigned references were triaged; Qin is **abstract-only**,
the Yellow Paper is **README/context-only**, and Binance's dynamic index yielded
an empty listing rather than data. See [sources.json](sources.json) for exact
titles, URLs, publication/retrieval dates, read scopes, failed access and windows.
R IDs are local inventory IDs, not original paper citation numbers.

There were **21 document fetches, eight searches, and five public read-only
network methods**. Four additional local preparation failures occurred before
any network request because `AbortSignal` was unavailable; they are retained
and conservatively charged, giving **nine of the twelve allowed method
attempts**. Removing that unsupported local option was the reason for the
single corrected attempt. No provider rejection was inferred from those local
failures. All five actual requests returned HTTP 200 JSON.

The original twenty-document/six-search budget plus one candidate-only extra
document and two candidate-only extra searches were used. No paid archive,
installation, account enrollment, signer, transaction, order, collector or
server was used. No further wave or backfill is scheduled.

## 2. Accounting marks are not executable spreads

[Allium's short Prices overview](https://docs.allium.so/historical-data/prices)
describes hourly token prices derived from DEX and centralized exchange data.
It does not supply a synchronous bid, ask, executable depth, transfer eligibility
or a matched pair of cross-chain claims. Public documentation access is not proof
of free access to its underlying SQL/data products.

[Dune's methodology](https://docs.dune.com/data-catalog/curated/prices/overview)
is more explicit: external observations can be interpolated; DEX prices are
hourly volume-weighted aggregates; inactive series may be filled forward.
Documented maximum fill horizons are 30 days for daily, seven days for hourly
and two days for minute series. Consequently, different-chain accounting marks
can show an apparent spread without two contemporaneously available fills.
Preserve chain, contract/mint, source and actual observation age; symbols and
bucket timestamps alone are inadequate. This is a measurement limitation,
not a claim that every observed spread is artificial.

[Mempool Dumpster's README](https://github.com/flashbots/mempool-dumpster)
documents public daily transaction/source observations, not universal global
order-flow visibility. Source-relative exclusivity is not global exclusivity.
Duplicate source observations and transactions observed after inclusion require
care. Its inclusion-delay calculation can be negative because block-slot
timestamps and receipt times differ; that is not evidence of negative physical
latency. No archive file was downloaded or continuity verified in this pass.
These data are for coverage/timing context only, not front-running workflows.

The [Binance index](https://data.binance.vision/) did not render its dynamic file
listing. The [MEXC About page](https://www.mexc.co/about) supplies venue marketing,
not historical token-specific withdrawal availability or an all-in fee ledger.
Neither was counted as recovered execution data.

## 3. Candidate 1: what a short can and cannot hedge

The mechanism is reasonable only conditionally. With the **same economic units**,
a linear short may offset common asset-price movement while spot inventory is
in transit. It does not lock the destination's local spread. A destination
premium can disappear while the common price stays unchanged, leaving no
offsetting gain on the short. Perp-index basis, wrapped-claim impairment, FX,
bridge failure, counterparty failure, asynchronous fills and venue-local
liquidation remain.

For fixed quantity `q`, short quantity `h`, and actual executable prices, the
analytical accounting identity is:

```
economic PnL =
  q × (destination spot exit − source spot entry)
  + h × (perp bid entry − perp ask exit)
  + signed funding
  − all other costs
```

This is **not a replay result**. Fees charged in transferred token units require
actual receipt quantities rather than blindly retaining `q`; do not deduct the
same fee twice. A BTC-ETH spot cycle also requires an explicit numeraire and
accounting for both asset exposures. A correlated index or major-token short is
not an exact hedge for an unrelated token or its bridge-specific claim.

Adding a hedge changes winners as well as losers. There is no basis for assuming
every loser becomes profitable while every winner remains unchanged. Margin
capital is additional committed capital unless proven shared under the actual
venue/account setup; total spot inventory, hedge collateral, loan collateral,
buffers, gas and in-flight assets must fit one capital budget.

### Historical execution and fee availability

[Hyperliquid's history documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/historical-data.md)
documents L2/context archives with approximate monthly publication, possible
missing data and **requester-paid transfer**. No S3 data was requested under the
no-paid-data rule. This does not prove another free historical source cannot
exist, or that all documented archive objects are complete.

The [info reference](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint.md)
describes a current L2 snapshot with at most twenty levels per side, recent
candle retention, and bounded recent fills. Its `allMids` can even fall back to
the last trade if the book is empty. Candles, mids and last trades do not supply
the bid/ask/size needed for an invented short entry and later close.

The [perpetuals reference](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals.md)
documents current universe/margin metadata, DEX namespaces and historical
funding queries. These do not by themselves prove that the exact hedge contract
was listed, unhalted and tradable for the sample's unknown historical dates.
No historical funding query was arbitrarily chosen without identified times.

The [current fee schedule](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees.md)
does show **0.045%** as a baseline validator-perp taker fee at retrieval.
It is not a universal all-in or round-trip cost, and is not established as the
historical rate for the alleged sample. Both fills and actual maker/taker tier,
referral/staking/collateral adjustments, builder fee and HIP-3 deployer/growth
settings matter. The fill schema says a reported total fee includes a builder
fee when present: adding that component twice would overstate costs.

[Funding documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/funding.md)
distinguishes its eight-hour formula from hourly payments. Reconstruct actual
settlement events, position signs and oracle notional; do not assume a short
earns funding or continuously prorate an advertised APR through a brief bridge
interval. HIP-3 also has contract-specific funding parameters.

[Margining](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/margining.md)
and [HIP-3](https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-3-builder-deployed-perpetuals.md)
document collateral/mode/account-abstraction differences, initial and maintenance
requirements, deployer-defined contracts/oracles, settlement and ADL risks.
A profitable combined terminal mark does not prevent a short from being
liquidated on its own venue before spot proceeds arrive.

### A real but non-substitutable public capability check

[public_spot_checks.json](public_spot_checks.json) retains requests, exact raw
JSON response strings, their SHA-256 hashes and acquisition times.

- Current first-DEX `meta` returned **235 entries**. BTC reported a maximum
  leverage of 40 and ETH 25 at this snapshot; documentation examples are not
  observed settings. No exact GNO/ZGAP/DOS names appeared in this one current
  universe. That is **not** proof of historical unavailability, different ticker
  mappings, or absence on all HIP-3/other venues.
- One BTC `l2Book` returned a book timestamp of
  **2026-10-29T08:58:01.601Z**, with bid and ask price/size levels. It proves a
  current public feed can be read, not that a historical hedge would have filled
  or that a top-of-book price can fill arbitrary size.
- No public account trade history, historical listing or historical book was
  claimed from these two market-data requests.

### Decision and nearest valid test

**Do not run the proposed 21-trade counterfactual yet.** The identified-row count
is zero; that is an identification failure, not twenty-one zero-return trades
and not evidence the reported events never occurred.

[counterfactual_input_gate.json](counterfactual_input_gate.json) lists the precise
inputs and a single finite test if they become available: freeze the complete
sample; identify historically matching contracts; use size-aware entry bids and
exit asks at predeclared times; reconstruct actual bridge outcomes, funding,
margin and costs; report paired results and unavailable/failed rows. No selecting
only losing trades, retroactive perfect exits, automatic monthly expansion or
T2 designation.

## 4. Appendix G is borrowed inventory, not a free atomic loan

The [versioned seed paper's Appendix G](https://arxiv.org/html/2501.17335v2#A7)
describes buying WBTC on Ethereum, initiating its bridge, borrowing WBTC on
Arbitrum shortly afterward, selling the borrowed WBTC, and repaying after the
bridge delivery. This is a **non-atomic debt lifecycle**, requiring credit or
collateral, interest and liquidation/repayment accounting; the instant sale
does not eliminate the capital constraint.

During the portion where same-unit WBTC inventory is matched by WBTC debt,
that debt already provides an opposing token-price exposure. Adding another
BTC short without reconstructing the balance sheet can overhedge. Residual
claim/basis/quantity and collateral risks still exist.

This example belongs to the paper's historical 2023-09–2024-08 sample, not a
2026 performance window and not the unrecovered 21-trade day. A narrative gain
is not itself a reconciliation of receipts, liabilities, collateral and costs.
The paper's profit sentence is therefore not used here as reconciled net PnL.
This package does not independently certify the linked receipt amounts.
The [companion empirical manifest](https://github.com/vaikmr/swarm-search/blob/58ad5931f96c905903a1b99787cd4e83d83bcd8c/discovery/workstreams/empirical/candidate-input-manifest.json)
is a separate published evidence package, not an additional document read or
receipt audit by this workstream.

## 5. Recent non-EVM lead: EURC Gateway inventory reuse

Circle's [2026-10-23 announcement](https://www.circle.com/blog/circle-gateway-new-pre-mint-address-for-eurc-on-solana)
names the Solana EURC Gateway pre-mint account
`A6sLLUWebvoUUnQoCiB45ktetd34iamfD8kwTsBSReAb`.
Its [current technical overview](https://developers.circle.com/gateway)
explicitly documents USDC, EURC and cirBTC as **separate per-asset balances**:
Gateway does not convert one to another. The announcement's legacy footer still
says USDC-only, so the main technical overview is used for current asset scope,
not an inference that every disclaimer or eligibility condition is resolved.

The public mainnet RPC returned an initialized SPL token account at that
issuer-designated address, with mint
`HzwqbKZw8HxMN6bF2yFZNrht3c2iXXzpKcFu7uBEDKtr`,
six decimals, and **20,000,009.79 token units**. The reported context was finalized
slot **462822009**, whose RPC block time was **2026-10-29T08:58:01Z**.
Genesis, account and slot-time responses are retained. This is one provider's
bounded current-state evidence, not a historical deployment-time proof or an
independent verification of minter permissions, backing or redemption.

Crucially, Circle states pre-mint holdings are excluded from circulating supply
until authorized release. These units are **not entrant inventory, executable
DEX liquidity, arbitrage revenue or evidence of freely available credit**.
Never send tokens to the pre-mint account; Circle warns this loses funds.

The plausible mechanism is cheaper inventory reuse: an already deposited,
established EURC balance could serve urgent destination demand without each
chain maintaining an independent full inventory. The documented fast mint
latency applies **after the balance is established**; it does not instantly
finance a newly acquired, unfinalized source purchase. Deposit/finality,
fees, withdrawal/service dependencies, legal access and replenishment still
need testing. EURC's euro denomination also requires an explicit FX numeraire,
not a presumed one-dollar peg.

No current spread, accessible fee quote, realized turnover or net return was
measured. [mechanisms.json](mechanisms.json) records this as a fresh documented
rail hypothesis with cheap falsifiers, not a winner.

## 6. Other source boundaries and conclusion

The Qin citation was resolved to an [arXiv abstract/version page](https://arxiv.org/abs/2101.05511).
Its historical measurement context is not a current performance claim; attack
algorithms were not read for implementation or used to originate a strategy.
The [Yellow Paper repository](https://github.com/ethereum/yellowpaper) explicitly
warns its specification stops at Shanghai and lacks Cancun, so it cannot serve
as a current 2026 gas/execution rulebook.

The cheapest next meaningful check is **sample identity and contemporaneous
executable data**, not another simulator. A historical replay, margin-constrained
capital assessment, durable spread, return target and tail-risk certificate all
remain unestablished. Unknown economics stay null.

## Offline validation

```
python3 -m unittest discover -s discovery/workstreams/onchain -p 'test_onchain_package.py' -v
```

Nine checks passed: scoped reference coverage, fetch/search/method accounting,
read-only request allowlist, all five raw response hashes, exact token units and
timestamps, current-versus-historical separation, null economic outputs and
source/mechanism links. The owned-path and staged whitespace checks also passed.
These checks establish artifact integrity, not market performance.
