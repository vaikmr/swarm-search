# Discovery snapshot provenance

The small JSON snapshots are selected public API/configuration records retrieved
on 2026-10-29. Each records its exact source URL, retrieval timestamp, HTTP server
date, upstream response SHA256 and explicit evidence-kind declaration.
The raw response digest is provenance of the original HTTP body; since only
selected fields are retained, it is not a checksum of the selected JSON file.
Dynamic endpoints will return a different sample on a later run.

`collect_public.py` has no wallet, signing, RPC-broadcast or paid-data dependency.
It removes signed order blobs, signatures, arbitrary calldata and unrelated user
identity fields before saving. Configuration parameters are operator requests,
not measured realized margins or capital balances.

- `snapshot-across-fills.json`: latest deposits, some unfilled and some lacking
  relayer attribution. Not an unbiased market sample.
- `snapshot-across-configs.json`: public nomination parameters, not active actors.
- `snapshot-across-registrations.json`: new directory listing, with the example
  explicitly marked. Not an active participant registry.
- The UniswapX sample is stored under the separate intent-solvers strategy.

No observation here meets T1's reconciled actor PnL requirement. No T2 replay or
T3 paper trading was run by this scout. No claim that absent evidence implies
unprofitability is made.

`receipt-optimism.json` independently verifies one API-attributed relayer using
the official Optimism public RPC. It includes selected receipt fields, L1 fee
fields where returned, the canonical block timestamp and block-hash match.
Reproduce the fixed receipt reads from the repository root with
`python3 strategies/intent-solvers/evidence/verify_public_receipts.py`.
Successful execution of a single receipt is not a profit or competition result.

## Historical followup

[`HISTORICAL_LEDGER_AVAILABILITY.md`](HISTORICAL_LEDGER_AVAILABILITY.md) documents
a bounded 14-day Optimism log/state retrieval for one actor, the observed
pagination limits, actual repayment-path witness and remaining cross-chain
receivable/cost gaps. It does not establish actor PnL. Its small provenance
summary is published; bulk per-event records remain in ignored `data/raw/`.

[`OFFLINE_RAW_AUDIT.md`](OFFLINE_RAW_AUDIT.md) adds a network-free rehash/recount
against those saved responses, original raw witnesses, and the explicit missing
ABI/deployed-source pin. It distinguishes collection-author integrity checks from
the independent reviewer's narrower witness review and from actor economics.
