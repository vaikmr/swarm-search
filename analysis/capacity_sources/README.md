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
