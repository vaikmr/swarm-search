# Paper-only replay accounting and evidence manifests

**Status: scaffolding only. No T1 actor PnL, no T2 historical fork replay, and no T3 forward observation were produced by these tools.**

Python standard library only, Python 3.10+; tested in the development sandbox with Python 3.14.7. Run from repository root:

```sh
python3 -m unittest discover -s tests -p 'test_replay*.py' -v
python3 -m unittest discover -s tests -p 'test_evidence*.py' -v
python3 -m research_tools.evidence path/to/manifest.json --root .
python3 -m research_tools.replay path/to/accounting-input.json
```

The CLIs read local files and print JSON. They do not contact RPCs, store keys, sign, broadcast, place trades, or execute transaction/contract code. Do not add live executors here.

## What the evidence validator does

`evidence.py` provides frozen typed manifest/source/claim/window records, decimal-string quantities, and strict UTC timestamps. Version 1 manifests require:

| Field | Meaning |
| --- | --- |
| `schema_version`, `paper_only` | Integer `1` and boolean `true`; fail closed otherwise |
| `id`, `strategy_id` | Nonempty identifiers, not private coordination IDs |
| `tier` | Claimed `T1`, `T2`, `T3`, or `T4`; never automatically promoted |
| `data_kind` | `observed_onchain`, `historical_fork`, `forward_paper`, `model`, or `synthetic` |
| `start`, `end`, `created_at` | Explicit UTC ISO timestamps; no future/negative coverage |
| `sources` | Nonempty source records described below |
| `claims` | Numeric claim records described below |
| `checks` | Required check name to a nonempty list of source IDs |
| `actors` | Public actor identifiers, required for T1 |
| `volatile_windows` | Sourced start/end windows within coverage, required for T2 |

Each source is `{id, url, retrieved_at, artifact_path, sha256}`. Use credential-free public HTTPS URLs; the artifact is a downloaded raw public response, query output, or reproducible simulation output. Preserve the raw response before summarizing. Local paths must be relative to `--root`, with no parent traversal or external symlinks. SHA256 hashes are verified from file bytes. Missing/unreadable/hash-mismatched artifacts fail checks. Do not include credentials in URLs, query strings, paths or artifact contents.

Each claim is `{id, metric, value, unit, source_ids}`. `value` is a finite decimal **string**, including for counts. The source references should support the claim's exact value, scope, timestamp/window and units. A hash does not prove they do; an independent reviewer must open the evidence.

Minimum durations are charter inputs, not empirical findings: T1 actor observation at least 14 elapsed days; T2 replay at least 30 covered days and a sourced volatile period; T3 at least 7 elapsed days of actual live forward observation. Historical or fabricated timestamps cannot substitute for elapsed T3 collection.

Required evidence check names:

```text
T1: inventory_reconciliation, external_cashflows, actor_attribution,
    capital_deployed, prices, all_costs
T2: fork_state, execution_replay, latency, gas, failed_transactions,
    competition, capital_lockup, slippage, prices, all_costs,
    inventory_reconciliation, volatile_window
T3: forward_observation_log, decision_logic_identity, simulated_fills,
    latency, competition, prices, all_costs, inventory_reconciliation
```

**Passing checks establishes structural/metadata consistency and artifact integrity only, not the truth of contents or a verified tier.** Someone can relabel a synthetic artifact dishonestly; no metadata validator can infer otherwise. `recommendation_eligible` is always false. Review actual content and reject relabeling, incomplete inventories, missing fees, optimistic fills, lookahead or cherry-picked periods. There is no grade, promotion, probability estimate or investment recommendation here.

## Accounting input contract

`replay.py` consumes **precomputed** opportunities and mark paths, not raw chain state. Its output is always **T4**, including with historical data. It does not qualify as T2 just because the dates cover a month.

Top-level required fields:

```text
schema_version = 1
paper_only = true
data_kind = "synthetic" or "historical_precomputed"
start, end = UTC ISO timestamps
initial_capital_usd = positive decimal string
infrastructure_per_30d_usd = nonnegative decimal string
benchmark_period_net_usd = decimal string or null if unknown
inventory_marks_complete = explicit boolean
gross_excludes_all_costs_and_external_flows = true
gas_all_in_includes_base_priority_l1_operator = true
source_ids = nonempty identifier list
opportunities = list of opportunity records
```

An opportunity requires:

```text
id
decision_at, settlement_at, latest_fill_at = UTC timestamps
competitor_arrival_at = UTC timestamp or null for unknown
measured_latency_ms = nonnegative integer, no assumed unmeasured latency
capital_usd = principal reserved until settlement
gross_pnl_usd = economic PnL excluding external flows and ALL supplied costs
success_costs, failed_costs = complete cost objects
attempt_on_loss, race_proven = explicit booleans
marks = increasing [{at, cumulative_gross_pnl_usd}, ...]
source_ids = references included in top-level source_ids
```

Each cost object must explicitly contain every field:

```json
{"gas_all_in":"0","protocol":"0","bridge":"0","slippage":"0",
 "cex":"0","hedge":"0","borrow":"0","other":"0"}
```

This zero-valued illustration is **not a fee assumption**. Every zero must mean verified not applicable, not unknown. Fees are positive expenses; token rewards/funding or rebates belong in evidenced gross economic change, not negative fee guesses.

Use execution/base + priority + chain-specific data/operator gas **exactly once** in `gas_all_in`. If an all-in receipt includes L1/poster/operator charges, do not add them again. Mark-to-market gross must exclude separately stated slippage/fees; normalize actual records carefully to avoid double subtraction. The accountant owns canonical conventions in `analysis/costs.md` and `research_tools/costs.py`; adapters must reconcile into that ledger before relying on research outputs.

The terminal cumulative gross mark must equal the opportunity's final gross PnL. Provide interim marks dense enough to reveal drawdown; settlement-only profitable snapshots cannot establish drawdown. `inventory_marks_complete=false` suppresses drawdown values. Setting it true is an adapter assertion, not independent proof. Real deployment risk may be larger between marks.

The accounting boundary requires opportunities to close within the chosen data window. Extend the data through final settlement, or use a genuine end-of-window fair-value/locked-capital adapter; **never silently drop unsettled positions or their liabilities** to satisfy this input format. This limitation prevents using the scaffold unmodified for live open positions.

## Conservative accounting and sensitivities

- Unknown races lose. Ties lose. Only a supplied evidence-backed competitor arrival strictly after our measured completion can yield a candidate fill. A stale deadline or unusable mark path also loses.
- Losses incur explicit failed-attempt costs only when the hypothetical strategy would attempt the fill. A lost race is not automatically a free skipped trade. Retry costs must be present in the input.
- Principal stays locked from decision to settlement; capital cannot be reused. Fees and prior marked losses reduce available budget. Principal plus the larger of success/failure costs must fit the budget. Profits do not compound.
- Same-time opportunities use identifier order, not an optimized ex-post selection. Supply the actual strategy decision ordering in adapters.
- Gross PnL minus variable costs minus time-prorated infrastructure is cash net. Benchmark excess subtracts the period-aligned counterfactual net **once**. Unknown benchmark means null excess, not zero benchmark. No unproven idle yield is credited.
- Infrastructure uses an explicit fixed 30-day convention. It is not a payment or spending authorization.
- Sensitivities: base; +50ms latency; +200ms latency; all-in gas 2x; incumbent capture +20% relative; combined. This is a scenario grid, not a return forecast.
- Capture stress raises the **proven incumbent win count** by 20% relative, rounds up, and removes closest-margin entrant wins. It is an ex-post adverse scenario, **not evidence of competitor capture probabilities**. Zero observed incumbent wins implies zero relative uplift: a separate absolute-takeover stress is still needed. Unknown competitor races remain losses.
- Added latency may alter price/slippage/adverse selection. This accounting grid does not re-execute state or reprice quotes; genuine strategy fork adapters must do that.
- Cash/marked equity and capital-time utilization are reported, along with profitable-fill share and capture share. These do not include liquidation/margin mechanics, leverage eligibility, chain/protocol/stablecoin/bridge exposure gates or CEX freeze risk.
- Rolling 30-day PnL samples use daily-spaced complete windows; shorter series produce null percentiles, not annualized estimates. Overlapping empirical p5/p50/p95 are descriptive, not independent samples or confidence intervals. One window is one observation even if all percentiles coincide.
- A p5 outcome or historical maximum drawdown cannot certify the charter's separate **99% monthly drawdown confidence** or annual tail-loss gate.

## Reproducible synthetic smoke tests

The tests construct conspicuously named `SYNTHETIC` data in memory/temporary files. They are code tests only. To exercise the CLIs end-to-end without treating fixture outputs as market data:

```sh
python3 - <<'PY'
import json, pathlib, runpy
for name in ("replay", "evidence"):
    fixture = runpy.run_path(f"tests/test_{name}.py")["fixture"]()
    pathlib.Path(f"/tmp/SYNTHETIC-{name}.json").write_text(json.dumps(fixture))
pathlib.Path("/tmp/SYNTHETIC.txt").write_bytes(b"SYNTHETIC NOT MARKET DATA\n")
PY
python3 -m research_tools.evidence /tmp/SYNTHETIC-evidence.json --root /tmp
python3 -m research_tools.replay /tmp/SYNTHETIC-replay.json > /tmp/SYNTHETIC-replay-output.json
```

Do not publish fixture accounting numbers as strategy returns.

## What is still required

Genuine strategy-specific historical fork/state adapters, reproducible source blocks/receipts/traces, all rejected opportunities, measured latency/competition data, latency-dependent state repricing, complete inventory and external flow reconciliation, tail/exposure analysis, actual elapsed seven-day forward observation with identical decision logic, independent judging and human approval. Missing evidence is **unverified**, not proof of unprofitability.
