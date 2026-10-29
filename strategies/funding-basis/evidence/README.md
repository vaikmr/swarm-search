# Funding evidence

- [Official public info API documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals):
  `POST https://api.hyperliquid.xyz/info` with `type=fundingHistory`,
  `coin`, `startTime` and `endTime` in milliseconds.
- [`eth-funding-summary.json`](eth-funding-summary.json) and
  [`btc-funding-summary.json`](btc-funding-summary.json) preserve actual bounded
  hourly observations, exact request/page hashes and computation windows.

The HTTP POST is a read-only information query, not a trade. The collector has
no exchange endpoint, keys, signing, orders or transaction implementation.

```sh
python3 strategies/funding-basis/sim/fetch_funding_history.py
python3 -m unittest discover -s strategies/funding-basis/sim -v
```

Pagination advances to the largest received timestamp plus one and terminates
only on end coverage or an empty page. A repeated page fails rather than looping.
Rates can be negative and are never clipped to zero. The collector does not
identify actors, construct spot hedges or call its output net PnL.

## Missing T1 reconciliation

Named public leads in the hypothesis are documentation/dashboard observations
only. No complete public >=14-day inventory/equity/fee ledger has been
reconciled. Trading frequency, deployed capital, number of competitors and
strategy-attributed realized profit remain unknown. Vault TVL is not operator
equity and advertised APR is not a substitute.
