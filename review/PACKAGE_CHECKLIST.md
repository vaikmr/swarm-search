# Evidence package submission checklist

This is a submission template, not a completed study. Replace placeholders with source-backed facts. Leave unavailable items explicitly MISSING; do not insert invented zeroes, durations, fees, probabilities or returns. Numerical minimums below are user policy in the [research charter](../docs/CHARTER.md), not empirical observations.

## Package identity

- Strategy name/slug:
- Author(s) and independent reviewers:
- Stage requested:
- Immutable code/config commit:
- Data manifest hash:
- Observation interval, UTC, and historical/forward designation:
- Chains, protocols, versions, contracts and markets:
- Initial capital, reserves, collateral, bonds, leverage and CEX dependence:
- Known permissions, source access, gaps and blockers:

## Required folder contents

```text
strategies/<slug>/
  hypothesis.md
  evidence/
    manifest.json
    claims.csv
    actor-selection.md
    actor-pnl-reconciliation.csv
    raw/                       # public, permissible data or retrieval instructions
    derived/                   # reproducible output; do not confuse with raw data
  sim/
    README.md
    <replay code/config>
    <run manifest and outputs>
    <prospective paper logs and outputs, only once genuinely collected>
  redteam.md                   # independent author
  cost-review.md               # independent author
  capacity.md
  verdict.md                   # independent judge only, after inspection
```

Large raw data may be stored elsewhere if it remains accessible to reviewers with immutable references, checksums and public-source retrieval instructions. Never store API credentials, keys, personal access tokens, private chat metadata, or unrelated internal data. Cite public source URLs without credential-bearing query parameters.

## Stage 0: Benchmark

- [ ] Current lending input rates have UTC timestamps and protocol/asset/chain identities.
- [ ] Actual 30-day and 90-day histories are available, with missing data explained.
- [ ] Protocol age, TVL and relevant public audit are sourced.
- [ ] Feasible diversification and idle reserves are included in the benchmark allocation.
- [ ] Base interest, incentives, time convention, accrual and exits are documented.
- [ ] Net-dollar benchmark calculation is reproducible; advertised APY is not called realized yield.
- [ ] Independent cost review covers the same horizon and allocation.

## Stage 1: Breadth scan

- [ ] Hypothesis identifies the economic fee payer, why opportunity persists and entrant advantage, if any.
- [ ] Sources identify actor contracts/wallets and transactions rather than only market totals.
- [ ] T1, if claimed, has at least 14 elapsed days with capital and net PnL reconciliation.
- [ ] Scope-limited negative findings say "not found in this search", not "none exist".
- [ ] A T4 entrant model is labeled as a model, including fees, capacity and idle capital.
- [ ] Hard risk/eligibility violations are recorded, not offset by a high projected return.
- [ ] Decision is continue research, reject with inspected grounds, or missing evidence.

## Stage 2: T2 replay

- [ ] At least 30 historical elapsed days and an identified volatile regime are covered.
- [ ] Chain IDs, fork block hashes and historical protocol parameters reproduce the state.
- [ ] Versioned executable logic does not use future information or survivors only.
- [ ] Gas, priority fees, slippage, failures, finality, bridge/rebalance cost and delay are modeled.
- [ ] Capital lock-up, collateral, hedge margin and bond balances cannot reuse capital.
- [ ] We lose all ties and any race not proved winnable.
- [ ] Capacity analyst documents obtainable order flow and entrant capture, not incumbent gross revenue.
- [ ] Net monthly p5/p50/p95 outputs and path distributions include their sample-generation limitations.
- [ ] Drawdown is defined as nonnegative peak-to-trough equity loss, separate from signed returns.
- [ ] Monthly 99% drawdown target and estimation confidence are distinguished and uncertainty reported.
- [ ] Additional 50/200 ms latency, double gas and increased incumbent capture sensitivities are included.
- [ ] Independent cost review verifies full-portfolio median net >= net benchmark + 300 USD without double-counting opportunity cost.
- [ ] Reviewer can rerun material claims from the provided commands and data.

## Stage 3: Independent risk review

- [ ] Red-team author did not produce the candidate's simulation or grade their own package.
- [ ] Aggregate chain, bridge, issuer/stablecoin, protocol and shared-dependency exposures are mapped.
- [ ] No single point of failure exceeds 30% of total capital.
- [ ] At most three chains and any permitted CEX custody/reserve allocation are explicit.
- [ ] Leverage is within policy and used only delta-neutrally, with gap/margin risk quantified.
- [ ] Stablecoin, bridge, oracle, gas, competition, parameters, halt and custody scenarios are covered.
- [ ] Scenario loss amounts have reproducible calculations; probabilities have sources or are marked T4/unknown.
- [ ] Unmitigated plausible annual event threshold and monthly drawdown threshold are checked separately.
- [ ] Mitigations can actually execute under scenario impairments.
- [ ] Independent red team has re-scored any changed mitigation.

## Stage 4: T3 forward paper

- [ ] Frozen code/config and predeclared rules predate the observation window.
- [ ] At least seven full elapsed forward days exist; UTC start/end, gaps and coverage are stated.
- [ ] Inputs were recorded prospectively, including arrival time, staleness, rejection and no-op logs.
- [ ] Fills respect liquidity, latency, capital, slippage, fees and competition.
- [ ] No transaction was signed/sent and no paper fill is described as real execution.
- [ ] Replay and paper use the same logic; version differences and later tuning are disclosed.
- [ ] Replay/paper comparison matches horizons/capital and addresses unstable near-zero denominators.
- [ ] Any gap above 30% is explained and corrected validation is available.
- [ ] Reported observed PnL covers only the actual elapsed period; monthly extrapolations stay modeled.

## Final submission

- [ ] Claim ledger distinguishes measured results from constraints, stress assumptions and derived arithmetic.
- [ ] Each return/cost/probability claim has evidence tier, URL, artifact and reproduction path.
- [ ] Benchmark, cost and risk packages are independently reviewed.
- [ ] Immutable data/code versions support the actual claims used in the requested verdict.
- [ ] All missing evidence and unresolved disputes are listed.
- [ ] Package asks for a research verdict or human-review eligibility, not live execution.

## Minimal claim-ledger columns

```text
claim_id,strategy,claim_text,quantity,unit,claim_kind,evidence_tier,
period_start_utc,period_end_utc,chain_id,market_or_actor,
source_url,block_or_tx_ref,extracted_at_utc,raw_artifact,raw_sha256,
code_commit,reproduce_command,output_artifact,assumptions,limitations,owner
```

`claim_kind` distinguishes measured, derived, constraint and assumption. Use evidence tiers only when applicable; a policy constraint is not T1. A computed result inherits the limitations of its inputs and execution method, not the confidence of its formatting. Claims with undisclosed external costs or unknown quantities remain incomplete.

## Judge handoff record

```text
Strategy:
Stage requested:
Reviewed commit / data hashes:
Reviewer independence:
Gate table (PASS / FAIL / MISSING / UNCHECKED):
Critical claim IDs checked:
Commands independently run and observed results:
Disagreements and resolution:
Remaining uncertainty:
Verdict:
Reason and exact next permissible research action:
```

Do not prefill a strategy `verdict.md` with an approval. The judge owns it after inspecting submitted evidence.
