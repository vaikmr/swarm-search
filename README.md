# Swarm Search

Evidence-first research into legitimate, risk-adjusted on-chain strategies for a hypothetical $50,000 portfolio.

**Research only. No live trading, transaction signing, mainnet deployments, or private keys. No strategy is currently certified or recommended.**

**The bounded eight-workstream discovery pass completed, 2026-10-29.** The [opportunity map](discovery/OPPORTUNITY_MAP.md) covers the seven supplied candidates, current instrument/rail leads and useful rejections. The [independent audit](discovery/workstreams/audit/findings.md) reconciled 73 relevance triages and 32 scoped priority topics, including one legacy recovery and three explicit replacements—not 32 exact original full texts. No repeatable net-profit result was established. The [earlier study's closeout](FINAL_REPORT.md) remains historical; no trading or forward paper run is authorized.

## Research question

Can a single operator realistically earn $2,000–$5,000 net per month while respecting the capital, loss, concentration, leverage, and infrastructure limits in [the charter](docs/CHARTER.md)? An honest negative result is valid. The target is a research question, not a promised return.

## Starting points

- [Current discovery brief and source coverage](discovery/README.md)
- [Seven-candidate opportunity map and next cheap tests](discovery/OPPORTUNITY_MAP.md)
- [Independent reading and claim audit](discovery/workstreams/audit/findings.md)
- [Current cBridge quote and exact-token probe](discovery/probes/cbridge-2026-10-29.md)
- [Extracted bibliography and 32 priority-reference owners](discovery/citation-inventory.json)
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

All eight workstreams delivered their single discovery package and paused. The source-backed opportunity map and independent coverage audit are integrated. The 21-trade hedge counterfactual was not run because the original sample and historical executable hedge inputs remain unidentified. A current quote probe found no imbalance surplus on the tested corridor and confirmed a bridged/native USDC identity mismatch. No qualifying historical strategy replay or forward paper duration was established; earlier evidence-gathering scripts remain preserved, not scheduled to run.

## Running checks

The tools use Python's standard library. Run the accounting, provenance, public-snapshot, paper-observer, and risk-arithmetic checks from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s risk -p 'test_*.py' -v
python3 -m unittest discover -s analysis/capacity_sources -p 'test_*.py' -v
python3 -m unittest discover -s strategies/cross-chain-relaying/evidence -p 'test_*.py' -v
python3 -m unittest discover -s strategies/benchmark-lending/sim -p 'test_*.py' -v
python3 -m unittest discover -s strategies/funding-basis/sim -p 'test_*.py' -v
python3 -m unittest discover -s discovery/workstreams/settlement -p 'test_*.py' -v
python3 -m unittest discover -s discovery/workstreams/onchain -p 'test_onchain_package.py' -v
```

The delivered public snapshots reproduce gross modeled rate/funding components only. The default observer rejects all fills because a strategy and complete cost model have not been configured. Its single sample is not seven-day forward evidence.

Do not interpret passing tests, a source hash, historical APY integration, or precomputed accounting as profitable strategy evidence or a qualifying fork replay.
