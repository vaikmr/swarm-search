# Research charter

## Objective and limits

Find, test, and rank legitimate strategies a single operator could run with $50,000 total capital. Investigate the $2,000–$5,000 net monthly stretch target without fitting evidence to it. Papers and blog posts are leads, not evidence for achieved returns.

These numbers are user-supplied constraints, not empirical findings:

- Maximum acceptable monthly drawdown: 10% ($5,000), at 99% confidence, including tails.
- No single protocol, bridge, stablecoin, or chain may be a failure point for more than 30% of total capital.
- At most three chains plus one major CEX account; explicitly flag CEX dependence.
- Leverage at most 2x, only for delta-neutral positions.
- Protocols must be at least 12 months live, have at least $50 million TVL and one public audit, unless explicitly marked higher risk. Higher-risk labeling does not waive other limits.
- Infrastructure ceiling: $500/month. No spending is authorized by this ceiling.

At most three chains with 30% exposure each allow at most 90% of capital deployed on-chain under a literal chain-failure definition. The balance must remain outside those chain exposures; changing that interpretation requires an explicit decision. Protocol, bridge, stablecoin, chain, and CEX dependencies overlap and must all be tracked.

## Permitted universe

The starting candidates appear in [the strategy board](../STRATEGY_BOARD.md). Legitimate arbitrage, liquidation, non-manipulative intent filling, lawful backrunning, relaying, market making, LP, basis/funding and yield research are permitted.

No live trading, signing, private keys, mainnet contracts, sandwiching, front-running users, exploitation, manipulation, wash trading, phishing/bait tokens, or governance attacks. Incidentally discovered vulnerabilities end that line of inquiry; do not pursue or publish reproduction details.

Treat claims that BSC builders or Ethereum L1 searchers dominate their markets as leads requiring verification, not established facts. Reject builder-dominated arbitrage unless measured data establishes a contestable niche.

## Stages

1. **Baseline first:** current blue-chip stablecoin lending rates and 30/90-day history; eligibility, allocation feasibility, and net costs. Other strategy profitability rankings depend on this baseline.
2. **Breadth scan:** actor evidence and explicit T4 estimates for every candidate. Kill when documented risk violations apply, estimated attainable capture falls below the benchmark, or a sufficiently scoped search finds no profitable actors and there is no plausible entrant advantage. Incomplete evidence alone is unverified, not proof of loss.
3. **Deep simulation:** replay top three to five survivors over at least 30 days including volatility. Report p5/p50/p95 monthly net PnL, max drawdown, win rate, utilization, latency sensitivity (+50 ms, +200 ms), doubled gas, and incumbent capture +20%. Clarify absolute versus relative capture increments explicitly.
4. **Red team:** independent scenario review, mitigations, and re-scoring.
5. **Forward paper trading:** top one to three survivors for at least seven real elapsed days, using intended decision logic; reconcile a greater-than-30% replay/paper discrepancy before proceeding. When predicted profit is near zero, report absolute differences as well rather than divide by zero.
6. **Independent judgment and final report:** only evidence-qualified recommendations, or a clear finding that none qualifies.

Parallel scouting and tooling may begin while the baseline is retrieved, but no candidate may claim to beat a baseline that has not been computed.

## Evidence and decision gates

- **T1:** observed realized PnL of identified actors over at least 14 days, from chain data; account for external transfers, inventory and all relevant costs.
- **T2:** historical replay on forked state with realistic latency, gas, failures, capital lock-up and competition; lose all ties and unproven races. Simple price-history arithmetic is not automatically T2.
- **T3:** live-data paper trading over at least seven real elapsed days, with timestamped decisions, simulated fills and cost accounting.
- **T4:** estimates, models and assumptions; never sufficient for recommendation.

Keep every return/cost/probability traceable to a simulation artifact, chain query, or cited source with a URL. Record evidence tier, retrieval date, measurement window, source identifier/block range, method, units, assumptions, and limitations.

Kill a Stage 2 candidate when p50 monthly net PnL is below the net lending benchmark plus $300, or p5 drawdown exceeds 10%. These screening rules do not replace the stricter requirement to substantiate a 99% monthly drawdown bound.

Kill a candidate if a plausible scenario with at least 1% annual probability loses more than 20% of total capital and cannot be mitigated. Do not invent scenario probabilities. Insufficient tail evidence prevents certification.

Recommendation requires qualifying T2 **and** T3, ideally T1, and independent review. No seven-day observation can be completed instantly. An initial screening or unqualified report must not be presented as the final validated recommendation.

## Deliverable and source completeness

The supplied outline names `FINAL_REPORT.md` and specifies an executive summary of realistic low-, medium-, and higher-risk outcomes with evidence labels and an honest verdict on the stretch target. The uploaded source ends at the second outline item; its missing continuation was not provided.

Working report structure, pending any additional requirements: executive summary; baseline and allocation feasibility; full candidate kill/keep board; surviving evidence packages and limitations; capacity and full net costs; independent stress/risk review; evidence judge verdicts; and a human-gated deployment plan. This proposed structure does not imply additional user-supplied requirements.
