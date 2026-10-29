# Capacity source records

These records support Stage 0/1 feasibility analysis, not a trading recommendation.

- `sources.json`: public documentation retrieved on 2026-10-29 UTC. Facts are paraphrased; documentation can lag deployed contracts and admission policies.
- `api_probes.json`: one read-only UniswapX access probe per selected chain. An empty response is not evidence that no profitable orders exist.
- `calculate_bounds.py`: deterministic arithmetic and hypothetical capacity sensitivities. No network, transactions, keys, orders or mainnet execution.
- `test_bounds.py`: checks arithmetic, units and invalid-input behavior. Tests are not T2 replay or T3 paper-trading.
- `bounds.json`: generated output, explicitly labeled T4.
- `verify_funding_histories.py` and `funding_crosscheck.json`: independent
  arithmetic on the source-pinned public hourly histories, not position PnL.

Reproduce from the repository root:

```sh
python3 -m unittest discover -s analysis/capacity_sources -p 'test_*.py' -v
python3 analysis/capacity_sources/calculate_bounds.py > analysis/capacity_sources/bounds.json
git fetch origin scout/yield-evidence
python3 analysis/capacity_sources/verify_funding_histories.py > analysis/capacity_sources/funding_crosscheck.json
```

The margin, lock-duration and polling-workload examples are hypothetical inputs,
not measured market opportunities. The infrastructure ceiling is a sensitivity
input, not an invoice or spending authorization. Use the cost accountant's
period-aligned all-in cost ledger for actual performance.

## Across historical-slice consistency review

`verify_across_ledger.py` checks only committed request/aggregate metadata and
selected decoded witnesses at immutable scout commit `23d2fd1`. It makes no RPC
requests and does not independently recount or decode omitted raw event logs.
`across_crosscheck.json` records source hashes, units, chain-role counts and
explicitly unknown capacity/profit/lock values. See
[`../capacity-across-ledger.md`](../capacity-across-ledger.md) for the finite next
data requirements. `test_across_ledger.py` includes synthetic mutation tests.

From the repository root, with the source commit available (the fetch below
retrieves committed repository evidence, not new blockchain data):

```sh
git fetch origin 23d2fd15c1d736b6c8cee4614e82f3d55fc430c4
python3 analysis/capacity_sources/verify_across_ledger.py > analysis/capacity_sources/across_crosscheck.json
python3 -m unittest discover -s analysis/capacity_sources -p 'test_*.py' -v
```
