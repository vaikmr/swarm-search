# Offline raw-response audit of the historical followup

**The saved responses reproduce the reported counts and token aggregates.**
This is a collection-author self-audit, not an independent review of every raw
page, a pinned-ABI semantics review, or qualifying actor PnL.
The audit process used **zero new network requests**, reading only the responses
already collected for the prior followup.

## Scope and reproducible result

Input manifest: `history-probe-summary.json` as published in research commit
`23d2fd15c1d736b6c8cee4614e82f3d55fc430c4`.
Its file SHA256 is
`dbf2ebe7576773324ae604518a0e0494275de18a5a8488e0171ada4bd80c4cee`.

The separate byte-offset decoder in
[`audit_saved_history.py`](audit_saved_history.py) does **not** import the
collector's decode functions. It checks the same recorded event layout; agreement
between two decoders does not independently establish that layout's protocol
semantics.

[`offline-audit-summary.json`](offline-audit-summary.json) records:

- **144** successful original HTTP response bodies rehashed and byte-counted,
  **7,389,954 bytes** total. Every observed SHA256 and byte length matched the
  previously committed manifest. The two failed requests remain failed entries
  in that manifest, not empty-success responses.
- Both saved boundary headers' returned `number`, `hash` and `timestamp` matched
  the requested window and summary; selected balances and account nonces matched
  their saved read responses.
- **61 fill pages and 61 refund pages** covered the exact nonoverlapping queried
  block interval. Recounting and duplicate-key checks reproduced **2,915 current
  fill events**, **2,915 distinct event transaction hashes**, and **983 refund
  events with an allocation to the indexed address**.
- All repayment-chain counts, fill-type counts, per-token raw fill-output totals
  and per-token raw refund-allocation totals matched the prior summary exactly.
  No batch containing a selected allocation had a deferred-payment flag.
- The complete saved example refund receipt was successful. Its transaction hash
  matched the request; its log block numbers/hashes matched the receipt; the
  matching refund events were exactly equal to the saved page objects. The
  receipt's block hash also agreed with the event-page block hash. Its two
  SpokePool-to-address token transfers matched the prior summary.

The receipt's sender was `0xf7bac63fc7ceacf0589f25454ecf5c2ce904997c`,
not the selected repayment recipient. A third party executing a refund does not
make that executor the economic recipient or establish who paid for all fills.

## Original raw witness export

[`offline-raw-witnesses.json`](offline-raw-witnesses.json) preserves one original
JSON log object for each of:

- A fill log from a saved fill response.
- The selected address's USDC refund-allocation event from a saved refund page.
- The corresponding actual USDC transfer log from the full saved receipt.

Each object has a JSON pointer, original source-response name, HTTP-response
SHA256 and byte size. Its separately labeled canonical-JSON fingerprint is **not**
the HTTP-response digest. Values are retained without rewriting the raw event
object; enclosing witness metadata is derived. Bulk response bodies remain in
ignored local storage and were not silently replaced by these witnesses.

The judge can inspect these exported objects directly. Without the bulk raw
files, a reviewer still cannot independently rehash/recount every page. This
self-audit therefore narrows the raw-versus-derived gap but does not remove that
review boundary.

## ABI/source pin and attribution blocker

**No exact ABI/source commit or deployed-implementation pin is available in the
saved data.** The earlier source references were mutable `master` URLs:

- https://raw.githubusercontent.com/across-protocol/contracts/master/contracts/interfaces/V3SpokePoolInterface.sol
- https://raw.githubusercontent.com/across-protocol/contracts/master/contracts/spoke-pools/SpokePool.sol

The source bodies, commit/blob IDs, and the proxy's implementation mapping over
the historical window were not retained. The existing explorer example and the
byte-layout agreement do not repair that omission. This audit deliberately did
not fetch new material to manufacture a retrospective pin.

Consequently, the `FilledRelay` indexed `relayer` value is treated here only as
the **logged indexed address**, not as a verified transaction sender, gas payer,
legal entity, or an independently pinned repayment-beneficiary role for every
fill. In particular, **2,915 distinct event transaction hashes does not establish
2,915 transactions signed or paid for by that address**.
The refund arrays and receipt transfers do establish the recipient of the
specific inspected refund example; they do not settle the fill-event semantic
question across versions.

Resolving the semantic gap requires a properly pinned deployed implementation
and ABI for the window, inspection of the fill function's caller versus repayment
address assignment, and transaction/receipt sender correlation. Those checks were
not performed under the zero-new-requests instruction.

## Limits left unchanged

Only two saved boundary headers were checked. Intermediate log/receipt hashes
were checked for consistency within the saved responses, not against independently
retrieved headers, recomputed header hashes or another canonical chain source.
Cross-chain receivables, all costs, funding/rebalancing, liabilities, complete
inventory and total deployed capital remain unreconciled. Profit and capital
remain null; no evidence tier, capture estimate or recommendation was upgraded.

## Reproduce offline

With the already collected local responses present, from the repository root:

```
python3 strategies/cross-chain-relaying/evidence/audit_saved_history.py
python3 -m unittest discover -s strategies/cross-chain-relaying/evidence -p 'test_*.py' -v
```

The audit script has no networking or process-execution imports. It writes
outputs under ignored `data/raw/across-offline-audit/` by default, including a
per-file rehash checklist. The full local suite passed **21 focused tests**,
including six new synthetic offline-audit tests. Passing integrity checks is not
economic or attribution-semantic certification.
