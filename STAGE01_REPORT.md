# Interim on-chain strategy discovery report

**Checkpoint: 2026-10-29 UTC. Paper-only; no deployment recommendation.**

The eight research roles delivered initial discovery, capacity, accounting, risk and validation packages. The study has **not** reached its required final evidence standard. No strategy has reconciled fourteen-day actor PnL (T1), qualifying thirty-day historical fork/state replay (T2), or seven elapsed days of strategy-specific forward paper trading (T3).

Current disposition: **all twelve entries remain unverified / NOT READY**. Missing evidence is not proof that a strategy is unprofitable. No positive risk-adjusted return ranking, achievable monthly income band, or 99% monthly drawdown certificate can be reported.

## What the initial data actually shows

| Component | Modeled window | Gross component | Evidence and limitation |
| --- | --- | ---: | --- |
| Nominal three-sleeve lending illustration | 30 days ending 2026-10-29 06:01:03.674 UTC | $119.90 | T4 base-APY integration; net unknown and full allocation compliance unresolved |
| Same nominal lending illustration | 90 days ending at the same timestamp | $346.38 | T4, not three independent monthly outcomes or a forecast |
| BTC short funding on constant $30,000 notional | Trailing 30-day source window | $211.93 | T4 funding component only, excluding spot/basis/hedge costs and margin dynamics |
| ETH short funding on constant $30,000 notional | Same trailing 30-day source window | $190.28 | T4 funding component only; not a second independent investable portfolio |

These are different incomplete models, **not amounts that can be added together** on the same capital. Historical rates and funding observations are real public inputs, but integrating them under simplified assumptions does not make the resulting profits T1 or T2.

The lending illustration allocates $15,000 each to Aave/Ethereum/DAI, Compound/Arbitrum/USDT and Morpho/Base/SparkUSDC, with $5,000 in an explicit zero-yield cash scenario. It was constructed to test nominal caps, **not proposed as a compliant portfolio**. Shared Ethereum settlement, DAI backing overlap, precise Morpho vault eligibility, reserve custody and actual costs remain unresolved.

The accountant independently fetched the three public histories and reproduced approximately $119.900112 gross over the common 30-day window. With purely assumed aggregate costs of $0, $25, $100 or $500, arithmetic net would be approximately $119.90, $94.90, $19.90 or -$380.10. **Those are cost sensitivities, not observed bills or an approved net benchmark.** Depeg/default and valuation effects are additional unknowns.

Sources and reproducible inputs:

- [Lending allocation, exact pool IDs and component math](strategies/benchmark-lending/evidence/candidate-allocation.json).
- [Lending source records and limitations](strategies/benchmark-lending/evidence/README.md).
- [Independent cost reconciliation and scenario assumptions](analysis/costs.md).
- [Funding observations, actor leads and omitted economics](strategies/funding-basis/hypothesis.md).
- [Independent nominal-allocation risk review](risk/baseline-nominal-review.md).

These selected BTC/ETH funding components are materially below the $2,000-$5,000 monthly target before costs. That is not a broad rejection of other markets or proof of a complete strategy's net result.

## Feasibility and market-access findings

The target requires 4%-10% simple monthly net return on total $50,000 capital. Spending the entire $500 infrastructure ceiling would raise required pre-infrastructure profit to $2,500-$5,500 before variable expenses. These are requirement calculations, not attainable returns or spending authorization.

The literal three-chain limit and 30% domain cap permit **at most $45,000 on-chain**. This is a ceiling, not a deployment objective. More idle reserve may be appropriate, but its custody, issuer and freeze dependencies still require analysis and it remains in the return denominator. A $15,000 domain loss exceeds the separate $5,000 monthly loss budget: complying with nominal concentration alone does not prove drawdown safety.

CoW's documented self-funded bonding routes exceed the available capital. The sponsored route is distinct and still requires access; it must not be incorrectly rejected using the standalone bond. Other intent venues also have nomination, exclusivity, compliance or delegated-power requirements. Public protocol volume is not flow that a new entrant can necessarily capture.

Bounded public discovery worked for Across and UniswapX:

- Fifty sampled Across deposits included 46 filled rows; 10 filled rows lacked relayer attribution. The attributed sample is not an active-firm census or an estimate of win share.
- Twenty filled Base UniswapX orders were retrieved. An empty open-order snapshot at another time did not establish absence of activity.
- Selected recent receipts and an older published cross-chain transaction pair were checked against public RPC block data. Successful transactions do not reconcile refunds, inventory, costs, capital, ownership or actor profit.

These make Across and UniswapX useful **data-acquisition priorities**, not an investment ranking. See [execution discovery](strategies/cross-chain-relaying/evidence/SCOUT_SUMMARY.md), [capacity and admission analysis](analysis/capacity.md), and the [complete candidate board](STRATEGY_BOARD.md).

## What the tools validate—and what they do not

The combined six test suites passed **124 tests** at this checkpoint. They cover arithmetic, explicit unknowns, public-response filtering, provenance/path checks, hypothetical capital locks, loss accounting, timestamp coverage, and rejection of unsupported fills. Passing tests do not validate a trading strategy, a source's truth, a historical fork, an executable fill, or a return distribution.

Independent review found and owners corrected several contract problems before economic reporting:

- Marked/accrued economic PnL was labeled cash. Outputs now use economic-PnL terminology; realized cash cannot be inferred.
- Separately accounted idle contributions rejected negative values. Signed idle losses are now supported with regression coverage.
- The closed-position replay scaffold could be mistaken for whole-portfolio coverage. Outputs explicitly disclaim complete portfolio coverage; pending positions cannot be filtered away to establish monthly PnL.
- The funding helper could accept a missing scheduled boundary payment. It now requires the complete scheduled-event grid and count, with edge regressions.

The original independent cost review remains [source-pinned](review/COST_MODEL_REVIEW.md); its historical defect probes target the old revision, not the corrected API. The judge independently inspected and tested the owner corrections: see the [simulator review](review/SIMULATOR_REVIEW.md) and [correction dispositions](review/FOLLOWUP_DISPOSITIONS.md). These rechecks passed the scoped fixes; they did not certify source completeness or economic outcomes.

The replay tool still consumes precomputed records and is **T4 closed-position accounting, not a stateful EVM fork**. The default public observer rejects every fill because no strategy-specific decision/cost model is configured. A coordinator read-only smoke observation also rejected its fill and reported zero elapsed days. **No unattended seven-day strategy observation has started.**

No live trades, signatures, keys, deployments, paid data services or purchases were used. The infrastructure ceiling was not treated as spending permission.

## Next evidence gates

1. Establish a specific eligible baseline with exact market/audit mapping, dated issuer/settlement/reserve dependencies, period-aligned costs and whole-capital accounting. Lower deployment is allowed; unknown reserve risk is not waived.
2. Reconcile at least one fully public actor's opening/closing equity, transfers, liabilities, rewards, refunds and costs for fourteen days. Keep receipts separate from realized economic profit and distinguish firms from their contracts/addresses.
3. Only for a defensible surviving candidate, run genuine historical fork/state replay for at least thirty days including a volatile period, with executable information timing, competition, locks, failures, rebalancing and adverse joint scenarios.
4. Freeze strategy and costs, then collect genuinely elapsed forward paper evidence for at least seven days. Raw no-fill observation time is not a substitute for strategy evidence.
5. Independently evaluate costs, capacity, monthly drawdown and annual tail gates. Do not substitute a p5 screen or short zero-failure sample for the hard 99% monthly requirement.

No stage is declared complete merely because code or a checklist exists. The supplied final-report outline ends at item 2; that gap is preserved in the [charter](docs/CHARTER.md), not silently filled with invented requirements. This checkpoint is deliberately **not** `FINAL_REPORT.md`.
