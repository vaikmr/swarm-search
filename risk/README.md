# Independent risk review — Stage 0/1

Research date: 2026-10-29. Scope: the lending benchmark and all eleven candidate strategies. This is a risk specification and sourced historical review, not a strategy recommendation, audit, T1 actor-PnL study, qualifying T2 replay, or T3 observation.

## Immediate findings

1. **Full-capital on-chain deployment is infeasible under the literal concentration rules.** Three chains capped at 30% of total capital each can hold at most 90%, or $45,000 of the $50,000 budget. At least $5,000 must remain outside those chain buckets. A genuine off-chain USD reserve is conceptually possible; a stablecoin balance on another chain is not off-chain cash. CEX custody introduces its own failure domain and eligibility/access requirements. The reserve and its yield must appear in whole-portfolio accounting. These are charter-derived calculations, reproduced in `stress_output.json` (T4, not observed returns).
2. **Protocol and stablecoin caps aggregate across chains.** Putting the same lending protocol or stablecoin on three chains does not create three independent protocol/issuer exposures. Wrapped assets inherit issuer, bridge, custodian and collateral dependencies. Three L2s may share Ethereum settlement, infrastructure and software dependencies; their individual chain caps do not remove those common factors. Record the dependency graph and alternative interpretations explicitly rather than assuming independence.
3. **A 30% concentration cap is not a loss cap.** A total loss of a $15,000 bucket is 30% of the portfolio, exceeding both the $5,000 monthly loss limit and $10,000 annual-scenario severity threshold. The annual gate additionally requires a defensible probability at or above 1% per year; we have not established that probability for any particular deployed candidate. Unknown frequency is not zero frequency.
4. **The Stage-2 p5 screen is insufficient for the hard monthly rule.** Report monthly pathwise maximum drawdown, not only end-of-month PnL. A passing p5/95%-tail screen does not demonstrate that drawdown stays within 10% with 99% monthly coverage. A probability coverage target and statistical confidence in an estimate are different concepts.
5. **No candidate has been certified by this review.** Sources establish that mechanisms and incidents exist, not their future frequency or the entrant's return. Where conditional losses can be large but probabilities lack a defensible estimate, the correct status is `UNQUANTIFIED TAIL / NOT CERTIFIED`, not a numerical probability or an automatic claim that a particular annual kill threshold was met.

## Evidence labeling and reproducibility

- Input constraints: the study charter; not market observations.
- T4: explicit scenario assumptions, arithmetic, hypothetical allocations and statistical illustrations. `stress_checks.py` writes deterministic examples to `stress_output.json`. Unit tests validate the arithmetic and invalid-input rejection only.
- Source-context evidence: incident reports, official documentation and regulator statements in `sources.json`. These are **not T1** under the charter, which requires reconstructed actor PnL over the minimum observation period.
- T2/T3: **not performed by the red team**. No historical fill, return, gas cost distribution, event probability or future safety certificate is claimed.

Run from the repository root:

```sh
python3 -m unittest discover -s risk -p 'test_*.py' -v
python3 risk/stress_checks.py > /tmp/risk-stress-output.json
diff -u risk/stress_output.json /tmp/risk-stress-output.json
```

The checker deliberately always reports `risk_certificate: false`. It aggregates **declared** exposures; it cannot prove that a dependency is complete, independent, correctly valued or recoverable. Its hypothetical allocation is not an investable recommendation.

## Sourced historical context

| Reference | Verified statement used here | Limitation |
| --- | --- | --- |
| S01 Circle, March 2023 | Circle reported $3.3 billion of reserves at SVB, approximately 8% of its reserve, with availability restored after government intervention. | Historical reserve exposure; not a forecast of issuer loss or bailout availability. |
| S02 Federal Reserve, May 2023 | USDC traded temporarily as low as $0.87 before stabilizing near $1 following intervention. | The quoted low is not an executable venue/order-size fill or a T1 portfolio return. |
| S03 Arbitrum status, December 2023 | Sequencer/feed stoppage was followed by congestion and elevated gas before normal operations returned. | The headline incident window includes degraded operation; do not call all of it total chain downtime. |
| S04 Chainlink documentation | Sequencer unavailability can impede ordinary L2 interaction; uptime checks and a recovery grace period mitigate uneven access. | A guard is not insurance, nor proof that any named market implements it correctly. |
| S05 Across documentation | Relayers front their own capital and face reimbursement lock-up, software, finality and gas risks. | Approximate documented timing is not an empirical settlement distribution or a deadline guarantee. |
| S06 CFTC, December 2022 | The complaint alleged commingling/misappropriation of FTX customer deposits; recovery may be constrained by available assets. | Contemporaneous allegations, not a recovery forecast for a current CEX or a frequency estimate. |
| S07 Aave governance, November 2023 | Protective pauses/freezes limited actions; the risk analysis discussed pause duration, volatility and liquidation/repayment restrictions. | Protocol/asset/version specific. Third-party modeled insolvencies are not our evidence and are not imported. |
| S08 dYdX loss-mechanism documentation | Automatic deleveraging can close an offsetting profitable position and reduce its expected profits. | Current documentation must be pinned to the precise venue/version used in a later replay. |
| S09 dYdX October 2025 incident review | A volatility-period halt paused trading, liquidations and oracle updates; the restart briefly had stale oracle prices. | No exploit detail is used or reproduced; no trader loss is inferred from the outage alone. |
| S10 Reuters, February 2022 | Wormhole reported restoration after a bridge theft; restoration required an intervention. | Recovery in this incident is not a guarantee for any other bridge or claim. |

## Stress suite required for every survivor

All parameter values below are **T4 test scenarios, not estimated frequencies or calibrated quantiles**. Later T2 work must add observed episodes and actual execution costs, not silently relabel this suite as replay evidence.

| Scenario | Required replay/stress behavior | Loss and mitigation to measure |
| --- | --- | --- |
| Stablecoin depeg | Reprice inventory, debt, margin and collateral jointly; include the source-context $0.87 mark and a separately labeled total-loss severity. Include two supposedly distinct coins with shared collateral/reserves. | At the charter's $15,000 cap, a $1→$0.87 mark gives $1,950 direct unlevered loss (3.9% of total capital). Debt, liquidations and liquidity exits may add loss. Recovery later does not erase pathwise drawdown. |
| Bridge delay/default | Stop settlement/refunds for an explicitly assumed horizon; separately zero recoverable value of claims and bridge-backed assets. | Delay is capital unavailability, not automatically a principal loss. Reprice claims and funding/opportunity cost. Sum in-flight claims, bonds and bridge-wrapped inventory by failure domain, not only bridge calls. |
| Oracle failure | Feed stale/deviating prices and a sequencer-restart gap to a local decision model; no live testing or exploit reproduction. | Disable actions if freshness/uptime checks fail. Measure existing exposure while paused and liquidation/restart risk; a local stop cannot make an externally managed position safe. |
| Gas spike | Apply the charter's 2x cost shock to successful and failed attempts, plus observed congestion episodes when available. | Stop new entries below all-in profitability; still pay for prudent exits and already-submitted failures. Avoid fixed positive-PnL assumptions. |
| Larger competitor | Use a rival with the charter-requested 10x capital; lose ties and any race not provably won. Also apply the separate required incumbent-capture increase. | Remove captured revenue; retain fixed costs and inventory unwind losses. Do not assume 10x capital implies any fixed percentage of captured trades without data. |
| Parameter/governance change | Snapshot caps, fees, borrow rates, haircuts, rewards, allowed assets, pauses, bonds and auction access; rerun with adverse documented/configured changes. | Stop new entries, recognize borrow accrual and forced exits. A fixed-yield maturity promise is not immediate redemption liquidity. |
| Chain halt | Freeze the affected leg and mark accessible legs at contemporaneous market prices; model restart, congestion and oracle recovery. | Neutral net delta before the halt is not a cross-venue margin guarantee. Escape routes are not assumed timely or free. Distinguish locked funds from written-off funds. |
| CEX freeze | Deny withdrawals and transfers, then independently stress trading closure/margin access and eventual recovery haircuts. | CEX cash, spot, margin and unsettled claims share the CEX failure domain. Do not fund a rescue from the frozen account. Expose a CEX dependency even if marketing calls the strategy on-chain. |

## Whole-portfolio tail gates

For capital \(K=50,000\), declared exposure \(E\), and conditional unrecoverable fraction \(s\), the simple unlevered scenario loss is \(L=Es\). It is not a universal loss bound. Leverage, debt repayment, margin gaps, derivatives, correlated domains, adverse unwind and costs can add losses. Escrowed/bonded assets and receivables remain exposed until actually recoverable. Loss must be calculated without adding the same position's mutually overlapping losses twice; joint events require a state-based portfolio calculation.

If one insists on surviving a total loss of **any single** independent bucket within $5,000, each such bucket must be at most $5,000 before costs. This is a stronger deterministic policy than the charter's 30% cap and may be infeasible with the three-chain limit. It is not claimed to be a necessary condition when a valid probabilistic bound exists. Do not silently replace the user rule with it.

The annual condition is additional: a conditional loss strictly greater than $10,000 must be killed if its scenario has a defensible annual probability at or above 1% and cannot be mitigated. Separate the severity calculation, frequency evidence and mitigation evidence. Without frequency evidence, flag the certification blocker rather than inventing a pass or failing it on an unsupported probability.

Do not annualize frequencies by multiplying anecdotal incident counts. For illustration only, independent identical monthly breach probability of 1% compounds to \(1-0.99^{12}\), not 1% annually. Conversely, an independent 1% annual occurrence probability corresponds to \(1-0.99^{1/12}\) monthly. The independence/stationarity assumptions are not established for crypto failures.

With zero observed breaches in \(n\) independent, identically distributed month-long observations, the exact one-sided upper probability bound at confidence \(1-\alpha\) is \(1-\alpha^{1/n}\). For a **chosen illustrative 95% statistical confidence**, 299 zero-breach independent months would be needed to put this bound below 1%. Overlapping rolling windows are not independent months; repeated bootstraps do not create new history. This is a sample-size illustration (T4), not a claim that historical stationarity or such evidence exists. The charter has not specified a statistical confidence level for its estimated 99% coverage requirement.

## Mitigations and evidence required before live approval

- Build a look-through failure-domain ledger across strategies, not just per-strategy allocation. Include issuers/reserves, bridge representations, collateral baskets, lending protocol families, shared L1 settlement, custody, upgrade/governance authority and RPC/price-data dependencies.
- Verify protocol age, TVL and a public audit for the **specific deployed version and relevant dependencies**. A protocol-wide TVL headline does not establish each market's depth or safety; an audit is not an insurance guarantee.
- Reserve liquid cash for fees and margin where it remains accessible during the tested failure. Count that reserve against the relevant chain/issuer/protocol/CEX caps.
- Bound outstanding receivables, inventory, bonds and venue margin; use conservative recoverable values. Monitor stale data, health factor, depeg, halt, governance changes and settlement age. Stop new entries fail-closed.
- Require real stress/replay outputs, an exposure allocation, parameter versions, strategy-owner mitigations, then independent red-team reassessment. T3 paper execution cannot itself reveal rare insolvency/operational tails.
- Human approval remains mandatory. A merged research report, passing unit tests or a simulated positive median is not authorization to deploy capital.

## Unresolved items

No live positions, strategy allocation, venue eligibility, current deployment verification, insurance recovery contract, matched T2/T3 run, or calibrated failure-frequency dataset was supplied to this review. The individual `redteam.md` files therefore define candidate-specific tests and blockers rather than fabricate a passing verdict. The independent judge owns verdicts.
