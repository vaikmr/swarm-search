# Independent risk review of the smaller lending sleeve

Date: 2026-10-29. Input: scout commit [18370d81039303e86263dc998c87164d8d75226e](https://github.com/vaikmr/swarm-search/blob/18370d81039303e86263dc998c87164d8d75226e/strategies/benchmark-lending/lower-deployment.md), including its deployment-identity and sensitivity JSON. This review reads the recorded evidence; it does not claim an independent fresh RPC observation, audit, fork replay or return reconstruction.

## Supported improvements and remaining limits

| Item | What the package now supports | What it does not establish |
| --- | --- | --- |
| One chain/one sleeve | The model no longer stacks nominally independent L2/protocol/coin slots. Shared on-chain dependencies use one aggregate principal budget. | Safety of the off-chain reserve, complete joint failure modeling or diversification of every dependency. |
| Deployment identity | The recorded fixed-block implementation matches the pinned registry; the package identifies the pool, underlying and aToken. | Equivalence to an audited build, full current oracle/admin/aToken coverage, or uninterrupted withdrawal access. |
| Inventory | The artifact records underlying token inventory at the aToken at the pinned block. | Reserved liquidity, ordinary withdrawal execution for this operator or stress-period exit capacity. |
| Cost treatment | The hypothetical all-in ceiling is explicitly separate from the accountant's infrastructure-budget flag. | An observed or enforceable maximum for all future transaction, failed-attempt, unwind, custody and operating costs. |
| Reserve | The model explicitly labels reserve-counterparty slots hypothetical and leaves actual custody risk unresolved. | Availability, independence, insurance, jurisdictional access, authority to add accounts or compliance with the allowed venue scope. |

The scout's activation-proposal and registry/explorer references are useful identity/eligibility inputs, not proof of safety. Public audit existence is not current-build audit linkage. Nothing in this review reproduces vulnerabilities or tests live protocol behavior.

## Conditional arithmetic, not tail certification

The proposed **$4,000 principal + $500 assumed all-in monthly costs = $4,500**, or **9% of initial $50,000**. This leaves only **$500** before the opening-capital monthly severity threshold, so reserve losses and any omitted expense remain material. The expression bounds only the specified non-replenished sleeve and assumed costs; it is not a pathwise portfolio maximum-drawdown or 99% coverage proof.

The package's **$4,000 + 12 × $500 = $10,000 (20%)** annual comparison is a separately chosen conservative component-budget stress. It must **not** be relabeled as the charter's annual tail gate. That gate concerns an unmitigated scenario causing loss **greater than 20%** with a defensible occurrence probability **at least 1% annually**. An expected annual operating-cost total, a hypothetical ceiling, and a scenario occurrence probability are different quantities. Conversely, the earlier $4,500 sleeve's $10,500 annual component calculation does not by itself establish the charter's annual kill condition.

The **$46,000 reserve / $15,000 per hypothetical independent custody slot** arithmetic requires at least **four slots**. This is a lower-bound count under the stated assumptions, not a feasible account plan. A single exposed counterparty holding that reserve would represent **92%** of opening capital; neither zero risk nor insured recovery may be assumed. Multiple account labels do not establish independent failure domains.

The annual comparison assumes no replenishment after principal loss, no leverage/contingent liabilities and all expenses fitting the assumed ceilings. A later strategy that reinvests, tops up or accrues new obligations must be recomputed rather than inherit these bounds.

## Result and next evidence

**Risk certification remains blocked, not numerically disproven by a fabricated probability.** The smaller sleeve is a better specified research case, but not a completed compliant net benchmark. Actual costs/net income, a lawful accessible reserve custody structure, exact relevant audit linkage, complete portfolio valuation paths and qualifying T2/T3 evidence remain unavailable.

The next independent risk review should use the actual proposed reserve structure and dated dependency ledger. Continue to distinguish opening-capital component losses, running-peak portfolio drawdown, source-context incidents and statistically estimated tail probabilities. The judge, not this red team, owns the final strategy verdict.
