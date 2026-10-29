# Inventory-based cross-chain arbitrage — independent risk specification

Date: 2026-10-29. Status: **not risk-certified; asynchronous-leg and replenishment evidence missing**.

Apply all eight scenarios and both loss gates in the [shared review](../../risk/README.md); historical sources are in [the registry](../../risk/sources.json). No verdict or return evidence is supplied.

## Candidate-specific failure paths

- Pre-positioning removes bridging from the trade's hot path, not the need to replenish inventory, settle claims, or value bridge-backed assets. Mark wrapper dependencies even if no bridge transaction occurs during a profitable trade.
- Separate chains cannot be assumed to execute both legs atomically. One fill followed by a losing race, halt, gas spike or stale feed creates directional inventory. Arbitrum's halt/congestion incident is a concrete operational lead, not a future probability ([S03](https://status.arbitrum.io/clq6te1l142387b8n5bmllk9es)).
- Apparently independent L2s may share L1 settlement and stablecoin issuer dependencies. Aggregated protocol/issuer failure can exceed the per-chain view.

## Required tests and mitigations

Execute the first leg only under the specified local decision logic, then deliberately deny the second. Mark the resulting inventory at adverse executable prices, include real exit depth, and charge failed-transaction costs. Test depeg, prolonged rebalancing failure, protocol parameter changes and a competitor taking any race the entrant cannot prove it wins. Do not call simultaneous quotes achievable fills.

Require inventory and asymmetric-execution limits, stale-data stops, a documented lawful access path and rescue liquidity outside the affected domain. Any CEX rescue creates a CEX dependency and must fail under a withdrawal/trading freeze stress.

**Reassessment inputs:** state/quote timestamp alignment, per-leg fill admissibility, failed legs, inventory paths, rebalancing delays/costs, exact dependencies and mitigated joint stress output. No calibrated tail frequency or 99% monthly bound is available.
