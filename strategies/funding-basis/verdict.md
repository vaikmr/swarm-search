# Independent verdict — delta-neutral funding and basis

**NOT READY. Recommendation eligible: false.**

Reviewed Scout A `0767bcc1cb2b01d3dfc732fc7ed3c8b9f625652f` and capacity `7f8dfae10f8816a3686ec79e5d7aecc64915ed54`. Highest quantitative material is T4 signed constant-notional funding arithmetic, not strategy PnL.

The funding component excludes basis/spot marks, actual fills, trading and rebalancing costs, collateral liquidity and liquidation. A vault dashboard with mixed strategies is not reconciled pure funding-actor T1 evidence. A below-threshold actor/venue lead does not prove the strategy family unprofitable.

Next gate: one eligible venue/asset implementation's spot/perp inventory, actual funding, capital/collateral, fees, changing basis, forced-exit path and all shared dependencies. A DEX-only route need not use a CEX; any CEX leg requires actual CEX access and custody analysis.

Qualifying T2, elapsed T3, complete net economics and required risk evidence remain absent. [Common independent gates and evidence](../../review/STAGE01_VERDICTS.md). Delta neutrality is not loss immunity.
