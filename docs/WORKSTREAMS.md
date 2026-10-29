# Eight-worker research swarm

## Authorized discovery restart

The user authorized a new, single discovery-first pass on 2026-10-29. For this pass the [discovery brief](../discovery/README.md) supersedes the old assignments below. Workers own only their corresponding `discovery/workstreams/<folder>/`; previous strategy/model/risk/verdict files are preserved, not resumed. The coordinator owns the shared source inventory and synthesis. The judge and red team remain independent of strategy return origination. See the brief for the 32-reference reading allocation and full extracted bibliography triage.

## Earlier study ownership (historical)

The coordinator integrates work, maintains the strategy board, resolves written disagreements, enforces gates, and assembles the final report. Eight workers handle the following disjoint responsibilities.

| Worker | Responsibility | Owned paths |
| --- | --- | --- |
| Scout A | Lending baseline, funding/basis, hedged LP, fixed/variable yield; public actor evidence | `strategies/benchmark-lending/`, `strategies/funding-basis/`, `strategies/hedged-lp/`, `strategies/fixed-variable-yield/`, except independent risk/verdict files |
| Scout B | Relaying, DEX arbitrage, backrunning, liquidations, solvers, keepers, CEX-DEX | Remaining strategy folders, except independent risk/verdict files |
| Simulator A | Replay scaffolding and provenance/evidence checks; explicitly distinguish fixtures from T2 | `research_tools/replay*`, `research_tools/evidence*`, `tests/test_replay*`, `tests/test_evidence*` |
| Simulator B | Read-only paper observation and yield adapters; real-time duration and data freshness | `research_tools/paper*`, `research_tools/yield*`, `tests/test_paper*`, `tests/test_yield*` |
| Capacity analyst | New entrant capture, incumbent advantage, capital locks, bonds and concentration feasibility | `analysis/capacity.md` and its source records |
| Cost accountant | Canonical all-in costs, opportunity cost and net-PnL conventions | `analysis/costs.md`, `research_tools/costs.py`, `tests/test_costs.py` |
| Red team | Independent tail scenarios, historical sources and mitigations | `risk/`, strategy `redteam.md` |
| Judge | Independent rubric and evidence package verdicts; no self-grading | `review/`, strategy `verdict.md` |

Scouts discover actors but do not independently certify their own evidence. Simulators report actual run results, not strategy approval. The cost accountant and capacity analyst challenge assumptions; the red team and judge remain separate from strategy construction.

Use written findings and linked artifacts. Record disagreements, the evidence behind each side, and the coordinator's resolution. Do not turn uncertainty into an unsupported numerical probability.

## Integration

The empty repository received a content-free initial commit to establish `main`. Research foundation and subsequent substantive changes are reviewed as branches/PRs. Workers use separate sandboxes and disjoint branches; the coordinator integrates tested commits, avoiding direct `main` pushes and competing pull requests.
