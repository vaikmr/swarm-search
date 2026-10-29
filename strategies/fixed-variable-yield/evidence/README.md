# Pendle source records

- [`pendle-selected-markets.json`](pendle-selected-markets.json):
  bounded top-ten matching quote snapshot, complete pagination counts/hashes,
  exact filter and retrieval time. The full API market set was inspected in
  temporary storage; it is not copied into Git as a large unbounded dump.
- [`pendle-susds-history.json`](pendle-susds-history.json):
  actual daily implied/underlying APY and TVL samples with exact source URL and
  response hash. These are quoted market inputs, not wallet performance.
- [Official API overview](https://docs.pendle.finance/pendle-v2-dev/Backend/ApiOverview):
  documents market pagination and `v3` historical data.

Reproduce the cross-chain market crawl with public HTTP GET requests:

```sh
curl --fail 'https://api-v2.pendle.finance/core/v2/markets/all?limit=100&skip=0'
```

Read `total`, then advance `skip` by `limit` until the reported total is covered.
Filter expiry against the study timestamp; do not treat the first page as active
markets. The observed data had 833 unique chain/address pairs.

Historical endpoint used:

```text
GET https://api-v2.pendle.finance/core/v3/1/markets/0x9c560ebaf78e596cbcc27411d633a74d628dd7dc/historical-data
?time_frame=day
&timestamp_start=2026-07-31T00%3A00%3A00Z
&timestamp_end=2026-10-29T06%3A00%3A00Z
```

Actual access issues preserved: Python's default urllib client received 403 on
the market listing; normal public curl requests worked. Supplying Unix-second
date parameters to the historical endpoint returned 400
(`timestamp_start/end must be a Date instance`); ISO dates worked. Neither
failure indicated a missing account credential. No key or paid service was used.

All rate/TVL figures are nonqualifying observations or T4 quote inputs.
No actor's >=14-day net PnL is provided.
