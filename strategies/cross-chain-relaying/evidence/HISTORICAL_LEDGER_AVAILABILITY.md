# Across: historical ledger availability for one relayer

**Result: a 14-day Optimism event/state slice is publicly obtainable; a full
capital-adjusted actor PnL ledger is not established.** This is primary public
data-availability and partial-cashflow evidence, not qualifying T1, T2 or T3.
Realized net PnL, total deployed capital, opening/closing receivables, and costs
not actually reconciled remain **unknown**, never zero.

The subsequent [offline raw audit](OFFLINE_RAW_AUDIT.md) reproduced the counts
and aggregates but identified a missing exact ABI/deployed-source pin.
The indexed relayer address must not be equated with verified sender or gas
payer across all fill-event transaction hashes.

## Actor and exact window

Selected relayer address:
`0x07ae8551be970cb1cca11dd7a11f47ae82e70e67`.
It had already been independently observed as the successful sender of an Across
fill, rather than chosen solely from a configuration example.
No corporate identity or related-address grouping is inferred.

Chain: Optimism (`10`), SpokePool
`0x6f26bf09b1c792e3228e5467807a900a503c0281`, sourced from
[official deployed contracts](https://docs.across.to/reference/contract-addresses).

Opening state is after block **158224884**, canonical block time
**2026-10-15 07:15:45 UTC**. Closing state is after block **158829684**, time
**2026-10-29 07:15:45 UTC**. Event queries cover the exact nonoverlapping interval
`(158224884, 158829684]`. Returned block timestamps differ by **1,209,600 seconds
(14 days)**. These historical dates are not an elapsed forward-paper observation.
The fixed probe ran **2026-10-29 07:36–07:37 UTC**.

## What was actually retrieved

Source: unauthenticated `https://mainnet.optimism.io`, JSON-RPC reads.
Every page's method, parameters, response digest, size, status and retrieval time
are retained in [`history-probe-summary.json`](history-probe-summary.json).
Small boundary witnesses are in [`history-witnesses.json`](history-witnesses.json);
bulk raw data is deliberately excluded from Git.

- `eth_getBlockByNumber`, `eth_getBalance`, `eth_getTransactionCount`, and selected
  `eth_call` `balanceOf`/`decimals` reads worked at the historical endpoints.
- The one-shot full-range `eth_getLogs` request returned **HTTP 413**, JSON-RPC
  error `-32614`: `eth_getLogs is limited to a 10,000 range`.
- The fallback used **61** consecutive pages per event kind, maximum **10,000**
  blocks each. **All 122 page requests succeeded**; no duplicate, removed,
  out-of-window or undecodable logs were encountered by the collector.
- The current `FilledRelay` topic with actor indexed in topic 3 yielded **2,915
  events in 2,915 distinct transaction hashes**, all decoded `FastFill`.
- The current `ExecutedRelayerRefundRoot` topic yielded **983 events containing
  allocations to the selected actor**. No batch in that selected set reported
  `deferredRefunds=true`. An allocation log is not, by itself, independently
  reconciled spendable cash.

These are counts returned for the specified contract/topics by one provider,
not a claim of complete actor activity, independent competitor counts, protocol
market share, executable newcomer capacity, or reconciled profitable trades.
Legacy contracts/event versions and implementation upgrade history were not
exhaustively enumerated.

## Why destination fills and same-chain refunds cannot be subtracted

Of the **2,915** Optimism fills, their explicit `repaymentChainId` selected
Arbitrum for **2,076**, Optimism for **72**, and other chains for the remainder.
The complete per-chain count is retained in the summary. These fields designate
repayment choices; they do not prove settlement or inventories on those chains.

Conversely, refunds paid on Optimism can compensate fills made elsewhere.
Therefore `OP refunds minus OP fill outputs` is not actor revenue or profit.
No FIFO assumption was used to associate aggregated refund allocations with fills.

The protocol's
[settlement lifecycle](https://docs.across.to/concepts/intent-lifecycle-in-across)
requires matching fills to deposits, bundling refund allocations, finalizing roots
and executing payment. **A destination payout decreases token cash and creates
a settlement receivable. It does not immediately free reusable inventory.**
The complete receivable at both window boundaries remains unknown.

One independent successful receipt,
[`0x5bd36a12ca618cf6e3d406d9352207fd6c413f323ced70dfc4768523e9e953e6`](https://optimistic.etherscan.io/tx/0x5bd36a12ca618cf6e3d406d9352207fd6c413f323ced70dfc4768523e9e953e6#eventlog),
contains actual SpokePool-to-actor transfers of **300,000 raw USDC units** and
**30,398,523 raw bridged-USDT units**. Both token `decimals()` reads returned **6**.
These transfers corroborate that the relayer repayment path is observable; they
are not yield, profit, or a measured latency for any particular earlier fill.
The explorer's decoded refund event also corroborates the topic/layout used by
the collector and the official contract source.

## Selected balances are available, but not a capital denominator

The fixed-block reads returned:

| Asset | Opening token units | Closing token units |
| --- | ---: | ---: |
| Native ETH | 0.199886595759699386 | 0.199081521123773935 |
| USDC | 38,683.840618 | 35,878.824937 |
| WETH | 60.457741367599737641 | 35.124401441065366289 |
| Bridged USDT | 133,340.677594 | 12,057.016628 |

Source: fixed-block public RPC reads in the summary; units follow the queried
token decimals (**6/18/6**) and native wei scaling. These are selected wallet
assets only, with **no USD peg assumption, token price marks, debt offset, or
claim that the entire balance was deployed**. Other tokens appeared in the fill
and refund events and are not included in this small balance probe. This is not
an operator demonstrated to run on $50,000, nor a return normalized to $50,000.

The account nonce changed from **460293** to **464954**, an advance of **4,661**,
whereas the retrieved fill set has **2,915** distinct transaction hashes.
Nonce movement is a diagnostic, not a fully classified transaction census:
sender correlation, nonce-affecting authorizations and every nonfill/reverted
transaction still need checking. Thus unsuccessful gas, unrelated operations and
rebalancing costs cannot be assumed zero. Native-balance change is not gas cost
because funding, withdrawals, wraps and other native flows are unreconciled.

## Deposits API limitation actually observed

The [documented deposits API](https://docs.across.to/api-reference/deposits/get)
supports `limit`/`skip` and depositor/recipient filters, **not a relayer filter**.
The attempted `?limit=2&relayer=<actor>` returned **HTTP 400** with a validation
error. Offsets **0** and **1000** returned same-day deposits; offsets **5000**,
**10000** and **100000** returned HTTP 200 with empty arrays during this run.
No unsupported claim about database retention follows from those empty pages.
They did not establish a way to recover the requested 14-day deposits through
this endpoint, whereas historical log pagination demonstrably did work.
Because the API is newest-first and live, offset pages also need stability checks.

`depositRefundTxnRef` is documented as refunding an expired **user deposit**.
It is **not the relayer reimbursement ledger**. The authoritative relayer path
for this followup is the separate root-allocation/payment events and receipts.

## Remaining blocker to qualifying actor PnL

The concrete blocker is **ledger coverage and cross-chain entitlement
reconciliation**, not lack of historical Optimism reads. This bounded followup
did not retrieve all-chain fills/deposits, refund bundles and opening/closing
claims, all actor/treasury addresses, all liabilities/funding/rebalances, every
failed/nonfill receipt, token marks, or infrastructure costs. No public endpoint
was demonstrated that already supplies that reconciled actor ledger.

No winning-capture rate or positive margin is assumed. No profitable or
unprofitable actor conclusion follows from these data.

## Reproduction and checks

From the repository root:

```
python3 -m unittest discover -s strategies/cross-chain-relaying/evidence -p 'test_*.py' -v
python3 strategies/cross-chain-relaying/evidence/probe_actor_history.py
```

The fixed run makes **146 public requests** with a **160-request maximum**,
three workers and a global minimum **0.35-second request-start interval**.
It has no write RPC method, signing, wallet, key or live-order interface.
Raw records and selected per-event data go to ignored `data/raw/`.
All new tests are synthetic fixtures explicitly labeled as such.
The local suite passed **15 focused tests**, including the original collector
tests; these checks validate tooling, not strategy economics.
