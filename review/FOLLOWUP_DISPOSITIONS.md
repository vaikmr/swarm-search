# Independent review dispositions after owner corrections

Date: 2026-10-29. These are accounting/data/reporting checks, not economic outcome or strategy certification.

## Cost review C1 and C2: resolved in the checked owner correction

Original review: [`77f4e3fe36fa149975ba2b561942b17a7a9e7b12`](https://github.com/vaikmr/swarm-search/blob/77f4e3fe36fa149975ba2b561942b17a7a9e7b12/review/COST_MODEL_REVIEW.md), targeting immutable original costs revision [`43cda27e6e4a9d8fe828e75edcb1c244b7f78739`](https://github.com/vaikmr/swarm-search/commit/43cda27e6e4a9d8fe828e75edcb1c244b7f78739).

Checked owner correction: [`3b01b26affabb6728b0cd696c670764d3766ec21`](https://github.com/vaikmr/swarm-search/commit/3b01b26affabb6728b0cd696c670764d3766ec21).

The judge inspected the exact correction, ran all 25 focused cost tests in a separate worktree at that immutable revision, and independently exercised the **new** API:

- C1: `net_economic_pnl_usd` replaces the misleading cash field; there is no old cash alias. The model explicitly cannot infer received cash or withdrawable liquidity.
- C2: signed `idle_contribution_usd` preserves negative accrual and idle principal-loss contributions. A separate synthetic negative-idle check passed without clipping or rejection. The gross-requirement helper also handles signed idle contributions.
- C3: strategy-only and whole-equity conventions are now documented/tested separately, as are all-in receipt versus decomposed fee inputs. Component overlap still requires caller provenance; it is not automatically detected. No actual strategy double counting was established by the original review.

All reviewer examples are T4 synthetic fixtures, not observed losses or returns. No strategy/capital-risk gate passed as a result of these changes.

## Historical cost probe must stay pinned to old code

`review/evidence/cost_model_probe.py` in the original review commit is a **historical reproducer of the old contract**. Its old-field assertions are not expected to run against corrected HEAD. Retain it as historical evidence rather than changing those assertions to conceal the original behavior.

Once the historical reviewer file is present in the integrated checkout, pin its invocation to the original module using a detached historical worktree:

```sh
git worktree add --detach /tmp/swarm-cost-original 43cda27e6e4a9d8fe828e75edcb1c244b7f78739
python3 - /tmp/swarm-cost-original review/evidence/cost_model_probe.py <<'PY'
import pathlib
import runpy
import sys
root, probe = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2]
sys.path.insert(0, str(root))
import research_tools.costs as reviewed_costs
assert pathlib.Path(reviewed_costs.__file__).resolve().is_relative_to(root)
runpy.run_path(probe, run_name="__main__")
PY
```

The explicit pre-import pins the module used by the preserved script even though that script remains in a later review checkout. Current-contract regression checks instead use the corrected owner's `test_costs.py` and the new signed-input/economic-output API; they do not reuse old field names.

## Simulator owner corrections

See [the simulator review](SIMULATOR_REVIEW.md) for full immutable references and limits:

- Funding edge defect resolved at `5163ebc63d0572e8c2802db3bbd2bbadcd522666`; all 28 paper/yield tests and independent omitted-boundary checks passed.
- Replay cash/economic label corrected at `90beba4bda7d31823e61b728116877378166fd0b`; all 31 replay/evidence tests passed.
- Closed-cohort reporting made explicit at `d9a5befd2b69badd03fabdfa17867a0663397acc`; all 32 replay/evidence tests and independent scope-field checks passed.

Tests were run at the specified separate revisions. A later integrated tree needs its own compatibility checks; these results are not a claim that every API consumer has been updated.

## What remains unqualified

Full portfolio replay across opening/closing and unsettled positions, real historical fork execution, point-in-time data availability, true elapsed forward observations, attainable entrant capture, complete sourced costs and independent portfolio tail-risk substantiation remain required. Correcting arithmetic/reporting scaffolding supplies none of those by itself.

**No candidate is recommended; no realized strategy return or monthly risk bound is certified.**
