# Independent evidence audit rubric

Status: draft review policy; no strategy return or safety has been certified.

All numerical limits in this document are **user-specified research constraints**, not measured returns, costs, event probabilities, or claims of achievable performance. Evidence tiers attach to empirical claims, not to these policy thresholds. The repository's [research charter](../docs/CHARTER.md) records those constraints.

## Independence and decisions

The judge must not have produced the strategy's actor-profit study, replay, capacity estimate, or red-team analysis. Package owners cannot approve their own work. The judge records conflicts, reproduces material checks where possible, identifies unresolved disagreements, and gives the coordinator a written decision.

Allowed decisions:

- **NOT READY:** required evidence is absent, inaccessible, incomplete, or not independently checked. This is not a claim that the strategy is unprofitable.
- **RESEARCH CONTINUE:** a limited stage gate passed; identify the next permitted research stage. This is not a recommendation.
- **REJECTED:** inspected evidence shows a hard constraint or stage kill criterion fails. State the failed gate and artifact.
- **ELIGIBLE FOR HUMAN REVIEW:** all recommendation gates passed with adequate evidence and stated residual uncertainty. This never authorizes live trading.

No weighted score can compensate for a failed hard gate. Compare survivors only after every applicable gate passes. Record each gate as PASS, FAIL, MISSING, or UNCHECKED; missing and unchecked gates cannot produce an eligible decision.

## Gate G0: Safety, access, and scope

- Research/paper-only. No real-chain signatures, transactions, approvals, contract deployments, private keys, or production automation.
- Allowed economic strategies only; no sandwiching, user front-running, manipulation, exploit testing, or exploitation.
- If an incidental vulnerability is noticed, stop that path and privately report only minimal identifying details. Do not reproduce it or add exploit instructions to public artifacts.
- Public-source study only. No unrelated company/customer data, internal credentials, or private coordination metadata in repository artifacts.
- Free sources first. The infrastructure ceiling is not authorization to buy services.
- A later human decision is required before any live operation. A research verdict is not that decision.

## Gate G1: Provenance and claims

Every material number needs a claim-ledger entry: exact quantity/unit, evidence tier, observation interval, chain/market, source URL, immutable block/transaction or dataset reference where applicable, extraction time, raw artifact hash, calculation command, output reference, limitations, and owner.

User targets, risk limits, scenario inputs, and imposed stress factors must be labeled **constraint** or **assumption**, not observed evidence. An endpoint being reachable proves only access. A downloaded dataset is not a completed replay or PnL study.

Reproduce or independently reconcile the figures used for a gate. Unavailable or irreproducible source material remains unverified. References to papers, dashboards, announcements, or protocol documentation may identify leads or mechanics; they are not substitutes for measured strategy returns.

### Tier requirements

| Tier | Minimum package | Claims it does not establish by itself |
| --- | --- | --- |
| T1 observed | Identified real actor addresses/contracts; at least 14 elapsed days; auditable chain-level net PnL and funding reconciliation | New-entrant capture, safe future returns, or actors outside the searched universe |
| T2 replay | At least 30 elapsed historical days; forked state; volatile regime; realistic execution, latency, failed costs and competition | A genuine forward record or an empirically established monthly extreme-tail guarantee |
| T3 forward paper | At least 7 genuinely elapsed days; prospectively logged live inputs and decisions; frozen versioned strategy; realistic simulated execution | Live fills, cash realized by the study, or a month-long observed result |
| T4 model/estimate | Explicit assumptions, formulae, sensitivities and provenance | A recommendation, a completed fork replay, or an observed actor return |

Historical API data collected today cannot become forward paper observations. AMM quotes, endpoint APYs, gross transfer flows, aggregate market fees, and TVL are not T1 actor net PnL. A rate can be an observed input without being a measured strategy return. Keep input-data descriptions distinct from the return-evidence tiers.

T1 is preferred but is not a substitute for T2 plus T3. Where T1 is unavailable, document the search limits and avoid claiming no profitable actor exists.

## Gate G2: Benchmark and feasible capital

The benchmark package must be available before candidates are economically ranked.

- Inspect current rates and 30-day/90-day history across eligible blue-chip lending venues. Record actual timestamps, missing intervals, supply caps, withdrawal liquidity, base yield and incentive components separately.
- Reconstruct accrued yield using the documented rate convention and time integration. Do not treat the arithmetic mean of APYs as realized compound income.
- Build a feasible whole-portfolio allocation under the same chain, protocol, bridge, stablecoin and custody concentration constraints as the candidates. Do not benchmark against an impossible single-venue allocation.
- Include entry, exit, rebalancing, claim/swap fees, infrastructure actually needed, idle reserves, and realistic cash realization of rewards.
- Use the same valuation currency, capital base, observation window, time convention and liquidation assumptions for benchmark and candidate comparisons.
- Define `B` as the net dollar benchmark for the relevant monthly period. A spot advertised APY extrapolation is explicitly a model, not a realized benchmark.

Do not double-subtract opportunity cost. If `S` is strategy net PnL after its actual expenses, the Stage 2 profitability comparison is `median(S) >= B + 300 USD`, equivalently incremental PnL `median(S) - B >= 300 USD`. Subtracting `B` inside `S` and then comparing that result with `B + 300 USD` is incorrect.

Both `S` and `B` must include the same total capital and feasible idle allocation. Clarify treatment of benchmark uncertainty instead of presenting a single stale rate as certain.

## Gate G3: Actor PnL integrity and selection bias

For every purported T1 actor:

- Explain address attribution and uncertainty; include supporting transaction URLs. Do not merge unrelated addresses because their transaction patterns look similar.
- Reconcile starting/ending balances, external deposits and withdrawals, debt, collateral, inventory, rewards, rebates, bridges and settlement receivables.
- Separate realized trading/interest PnL from unrealized inventory changes. Reconcile both to total USD equity; use independent historical prices for inventory and collateral.
- Exclude customer principal and borrowed principal from revenue. Exclude own-account transfers and bridging from economic profit.
- Include gas, priority fees, failed transactions, auctions/builders, protocol fees, rebalancing, hedges and financing. Disclose costs that chain data cannot observe.
- Report deployed and reserved capital, capital-time, transaction frequency, competitors and attribution coverage. Do not annualize returns on a selected profitable leg while ignoring idle inventory or bonds.
- Define the actor universe and selection rule before ranking profits; include losing, inactive, failed and disappearing actors where the search can observe them.

If off-chain costs, CEX legs, inventory attribution or actor capital cannot be reconciled, do not call gross flows net T1 profit. An actor earning money does not prove that an entrant can capture its opportunities.

## Gate G4: Replay validity and entrant capacity

Required T2 inputs and controls:

- Chain IDs, fork block hashes, timestamps, archive-state access, state transitions, protocol configuration and address versions.
- At least 30 historical elapsed days with an identified volatile interval. Explain why the sample was chosen without hindsight.
- Strategy decisions use only information available at their simulated decision time. No future block ordering, oracle prices, settlement state or token-survivor lists.
- An executable, versioned decision rule, with exact sizing, inventory, stop rules, collateral, bonds, protocol limits and capital locks.
- Chain-specific confirmation, sequencer, finality, RPC, submission and execution delays; gas and priority fees; revert/failed submission costs; bridge/rebalancing fees and settlement delays.
- Sizing-dependent slippage, market impact, pool state consumption, stale quotes, partial fills and inventory risk. Multiple simulated trades cannot each consume the same untouched liquidity.
- Competitive outcomes: lose every tie and every race whose win cannot be proved. A profitable opportunity already taken by an incumbent is not assumed available.
- Explicit new-entrant opportunity access, competition population, permissions, auction admission, bonding and fill ordering. Incumbent throughput cannot be assigned to the study portfolio.
- Net monthly PnL distribution with p5/p50/p95; positive maximum-drawdown distribution; worst path, win rate, capital utilization and net capital reconciliation.
- Sensitivities requested by the brief: additional 50 ms and 200 ms latency, double gas, and 20% increased incumbent capture. State whether the last is a relative increase or percentage-point change; show the choice and cap capture at the feasible maximum.

A path consisting only of arithmetic on historical prices is not a fork-state T2 replay. If that is all available, retain the model at T4.

Thirty days of replay is a minimum stage coverage requirement, not enough independent monthly observations to establish a monthly PnL distribution empirically. Report how scenarios, resampling or rolling windows were generated, their dependence and their model limitations; do not label synthetic months additional observed months.

## Gate G5: Cost and economic hurdle

The cost accountant must independently review:

- Execution, reverted attempts, auction/builder fees, bridges, replenishment, final exits, borrow/funding, CEX trading and withdrawal fees, RPC/data/server costs, reward conversion and settlement inventory.
- Full portfolio capital accounting: deployed funds plus idle reserve, collateral, bonds, pending withdrawals, receivables and liabilities reconcile to the starting budget.
- No reuse of the same dollars simultaneously across chains, bonds and hedge margin.
- Infrastructure stays within the user ceiling. Unsupported free-tier assumptions cannot certify availability, latency or a zero recurring cost.
- CEX dependence and account prerequisites are explicit. Taxes are flagged as a jurisdiction-dependent consideration, not calculated as personal advice.

Apply the Stage 2 `B + 300 USD` hurdle to the independently cost-reviewed median monthly net result. A single gross best-case result or aggregate market revenue does not pass.

## Gate G6: Risk, exposure, and uncertainty

### Portfolio eligibility

Audit aggregate exposure across all proposed strategies, including collateral and in-flight settlement:

- Total capital 50,000 USD; at most three chains and one major CEX account where required.
- No single failure domain exceeds 30% of total capital: protocol, bridge, stablecoin issuer/claim, or chain; review CEX/custodian and shared dependencies under the same single-point-of-failure principle.
- Look through wrappers, vaults, correlated stablecoins, shared bridges, common oracles and shared collateral. Nominally different protocol labels do not establish independent failure domains.
- Leverage no more than 2x and only delta-neutral. Report gross exposure, debt and margin, hedge mismatch and gap risk rather than calling a hedge risk-free.
- At least 12 months live, at least 50 million USD TVL, and a public audit for each protocol, or explicitly label the strategy higher risk and outside the ordinary eligibility set. That label does not waive other hard constraints. Verify deployed version and relevant audit scope. An audit is not safety certification.

**Allocation consequence, not a return estimate:** three chain buckets capped at 30% each can hold at most 90% of the portfolio on-chain. Any proposal allocating the full portfolio only to those buckets fails the literal chain cap. Explain the remaining reserve/custody allocation and its own correlated exposures; do not silently assume another chain or safe fourth stablecoin.

### Drawdown gate

The top-level requirement is a maximum monthly drawdown of 10% at a 99% confidence level, including tails. Separate the probabilistic performance target from the statistical confidence used to estimate it; report both, their assumptions, and any ambiguity.

Use nonnegative drawdown `D = maximum peak-to-trough portfolio equity decline / preceding peak equity` over a defined monthly path, including mark-to-market, liquidation, failed settlements and liabilities. Use signed returns separately.

The Stage 2 wording "p5 drawdown" is ambiguous: p5 of nonnegative drawdown is the mild tail, not the bad tail. Report it literally if needed, but also report severe drawdown quantiles and the monthly exceedance probability for the 10% limit. Do not silently substitute p5 return for p5 drawdown.

Neither a p5 return screen nor a p95 drawdown screen certifies the stricter monthly 99% top-level requirement. Missing tail evidence means **fail to certify**, not proof that the strategy fails economically and not proof it is safe.

Report sample construction, independent-equivalent sample count, overlapping-window dependence, confidence intervals or bounds, regime coverage and model uncertainty. Zero observed failures, a short quiet sample, bootstrap output, assumed Gaussian returns or repeated simulations on one historical path do not establish a distribution-free tail guarantee. Show stress and structural risks outside the observed sample.

Until the ambiguity is resolved and an evidence-supported risk assessment meets the strict top-level requirement, the verdict cannot be eligible. No point estimate may hide a wide or unbounded uncertainty interval.

### Independent red team

Require a separate red-team author and written owner response covering stablecoin depeg, bridge loss/delay, oracle failure, gas spikes, a competitor with ten times the capital, parameter changes, chain halt and CEX withdrawal freeze where relevant.

Scenario losses need mark-to-market and exit liquidity, duration of capital lock, hedge liquidation/collateral effects and portfolio correlation. Every event probability needs a traceable source or explicit T4 assumption. Unknown probability is not zero.

Apply the separate Stage 3 rule: an unmitigated plausible event with at least 1% annual probability and more than 20% portfolio loss kills the candidate. Do not convert annual to monthly probabilities without an explicit justified hazard/dependence model. Passing this rule alone does not prove the stricter monthly drawdown requirement.

Mitigations must be executable in the impaired state: a stop loss on a halted chain or instantaneous bridge escape is not a verified mitigation.

## Gate G7: True forward paper evidence

- At least seven genuinely elapsed days of prospective observations, with first and last UTC timestamps, gaps, uptime and covered markets reported.
- Freeze strategy, configuration, opportunity filters, paper-fill rule and costs in an immutable version before collection. A material change starts a new evaluation version and a separately reported forward window.
- Store input arrival and decision times, data age, intended sizing, predicted execution, reasons for no fill, simulated fees/reverts, inventory and equity. Preserve losing and no-op records.
- Use realistic simulated inclusion and competition; a displayed price is not an executable fill. Do not report paper PnL as live cash earnings.
- Run the same logic as replay. Show differences due to data availability or execution assumptions rather than hiding them.
- Compare forward performance with replay predictions over matched elapsed horizons and capital, including costs and confidence intervals. Do not compare a raw seven-day dollar figure with an unadjusted monthly figure.
- A performance gap greater than 30% requires diagnosis and corrected validation before proceeding. Predeclare a comparison metric and handling of near-zero/negative replay predictions; do not use an unstable percentage denominator to claim agreement.
- If the replay is changed after seeing paper results, separate model fitting from subsequent out-of-sample validation. Do not call the fitted period new validation evidence.

Accelerated replay, historical polling, backfilled candles and collecting seven timestamped samples in one session do not satisfy elapsed forward duration.

## Gate G8: Final review

Before an eligible decision:

- Confirm immutable versions of benchmark, evidence ledger, T2, T3, capacity analysis, cost review, red-team assessment and mitigation re-review.
- Independently reproduce material calculations and check every cited number used in the recommendation.
- Record disagreements, their resolution and any unresolved uncertainty. Unknown hard-gate quantities remain blocking.
- Rank only genuinely eligible portfolios; show lower-risk, medium-risk and explicitly higher-risk possibilities without treating hypothetical projections as evidence.
- Answer whether the target is supported by measured evidence. "Nothing clears the bar" and "insufficient evidence" are valid and distinct outcomes.
- Provide a human decision plan with prerequisites and residual risks, not a trading authorization.

## Reviewer record

For each package record the strategy slug, reviewed commit/hash, reviewer independence statement, stage requested, date, gate table, reproduced commands/results, critical claim checks, blockers, conflicting findings, verdict and exact next research step.

No strategy-specific verdict should be authored before its package is inspected. Initial status records list missing evidence without pretending that inspection happened.
