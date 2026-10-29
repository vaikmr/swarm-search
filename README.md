# Swarm Search

Evidence-first research into legitimate, risk-adjusted on-chain strategies for a hypothetical $50,000 portfolio.

**Research only. No live trading, transaction signing, mainnet deployments, or private keys. No strategy is currently certified or recommended.**

**Search closed at the user's request, 2026-10-29.** Read the [early closeout](FINAL_REPORT.md): all twelve entries remained unverified, and no further research or paper run is scheduled.

## Research question

Can a single operator realistically earn $2,000–$5,000 net per month while respecting the capital, loss, concentration, leverage, and infrastructure limits in [the charter](docs/CHARTER.md)? An honest negative result is valid. The target is a research question, not a promised return.

## Starting points

- [Final early-closeout findings and stop state](FINAL_REPORT.md)
- [Interim discovery findings and limits](STAGE01_REPORT.md)
- [Charter, constraints, and evidence gates](docs/CHARTER.md)
- [Strategy tracker](STRATEGY_BOARD.md)
- [Worker ownership and independent review](docs/WORKSTREAMS.md)
- [Independent evidence rubric](review/AUDIT_RUBRIC.md)
- [Independent risk specifications](risk/README.md)
- [Canonical cost accounting](analysis/costs.md)
- [Entrant capacity and admission constraints](analysis/capacity.md)
- [Replay-accounting and provenance tools](research_tools/replay_README.md)
- [Read-only yield inputs and paper observer](research_tools/paper_yield_README.md)

Strategy packages use `strategies/<slug>/hypothesis.md`, `evidence/`, `sim/`, `redteam.md`, and `verdict.md`. Missing files or evidence are not proof that a strategy fails economically.

## Evidence labels

| Tier | Required evidence |
| --- | --- |
| T1 | At least 14 days of real actors' realized PnL, reconciled to capital, inventory, transfers, and costs |
| T2 | At least 30 days of historical fork/state replay, including volatility, realistic costs, latency, and competition |
| T3 | At least 7 elapsed days of forward paper trading with the intended decision logic |
| T4 | Models, estimates, hypothetical scenarios, and unvalidated assumptions |

A recommendation requires T2 **and** T3, plus independent capacity, cost, risk, and evidence review. Data downloads, advertised APYs, synthetic fixtures, toy backtests, and historical observations do not become stronger evidence merely by being placed in an evidence folder.

## Status

Eight workstreams supplied discovery, partial actor evidence, independent reviews and paper-only tools. The user stopped the search before the required economic validation. No qualifying historical strategy replay or forward paper duration was established. Evidence-gathering scripts are preserved for reference, not scheduled to run.

## Running checks

The tools use Python's standard library. Run the accounting, provenance, public-snapshot, paper-observer, and risk-arithmetic checks from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s risk -p 'test_*.py' -v
python3 -m unittest discover -s analysis/capacity_sources -p 'test_*.py' -v
python3 -m unittest discover -s strategies/cross-chain-relaying/evidence -p 'test_*.py' -v
python3 -m unittest discover -s strategies/benchmark-lending/sim -p 'test_*.py' -v
python3 -m unittest discover -s strategies/funding-basis/sim -p 'test_*.py' -v
```

The delivered public snapshots reproduce gross modeled rate/funding components only. The default observer rejects all fills because a strategy and complete cost model have not been configured. Its single sample is not seven-day forward evidence.

Do not interpret passing tests, a source hash, historical APY integration, or precomputed accounting as profitable strategy evidence or a qualifying fork replay.
