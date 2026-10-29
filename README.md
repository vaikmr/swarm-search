# Swarm Search

Evidence-first research into legitimate, risk-adjusted on-chain strategies for a hypothetical $50,000 portfolio.

**Research only. No live trading, transaction signing, mainnet deployments, or private keys. No strategy is currently certified or recommended.**

## Research question

Can a single operator realistically earn $2,000–$5,000 net per month while respecting the capital, loss, concentration, leverage, and infrastructure limits in [the charter](docs/CHARTER.md)? An honest negative result is valid. The target is a research question, not a promised return.

## Starting points

- [Charter, constraints, and evidence gates](docs/CHARTER.md)
- [Strategy tracker](STRATEGY_BOARD.md)
- [Worker ownership and independent review](docs/WORKSTREAMS.md)
- [Independent evidence rubric](review/AUDIT_RUBRIC.md)
- [Independent risk specifications](risk/README.md)
- [Canonical cost accounting](analysis/costs.md)
- [Replay-accounting and provenance tools](research_tools/replay_README.md)
- [Read-only yield inputs and paper observer](research_tools/paper_yield_README.md)

Each strategy package will use `strategies/<slug>/hypothesis.md`, `evidence/`, `sim/`, `redteam.md`, and `verdict.md`. Missing files or evidence are not proof that a strategy fails economically.

## Evidence labels

| Tier | Required evidence |
| --- | --- |
| T1 | At least 14 days of real actors' realized PnL, reconciled to capital, inventory, transfers, and costs |
| T2 | At least 30 days of historical fork/state replay, including volatility, realistic costs, latency, and competition |
| T3 | At least 7 elapsed days of forward paper trading with the intended decision logic |
| T4 | Models, estimates, hypothetical scenarios, and unvalidated assumptions |

A recommendation requires T2 **and** T3, plus independent capacity, cost, risk, and evidence review. Data downloads, advertised APYs, synthetic fixtures, toy backtests, and historical observations do not become stronger evidence merely by being placed in an evidence folder.

## Status

Eight workstreams have been assigned. The initial phase establishes the lending benchmark, screens candidates, identifies data gaps, and prepares paper-only tools. No historical replay or forward observation duration has yet been established in this repository.

## Running checks

The tools use Python's standard library. Run the accounting, provenance, public-snapshot, paper-observer, and risk-arithmetic checks from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s risk -p 'test_*.py' -v
```

The delivered public snapshots reproduce gross modeled rate/funding components only. The default observer rejects all fills because a strategy and complete cost model have not been configured. Its single sample is not seven-day forward evidence.

Do not interpret passing tests, a source hash, historical APY integration, or precomputed accounting as profitable strategy evidence or a qualifying fork replay.
