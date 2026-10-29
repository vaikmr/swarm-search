# CEX–DEX arbitrage — independent risk specification

Date: 2026-10-29. Status: **not risk-certified; slower-entrant fills, custody and legging evidence missing**. **CEX access required.**

Apply all eight scenarios and both loss gates in the [shared review](../../risk/README.md). No strategy verdict or performance evidence is supplied.

## Candidate-specific failure paths

- Order-book quotes and a contemporaneous DEX quote are not jointly executable fills. The entrant is explicitly slower than incumbents; ties and unproven races must be lost.
- One leg can fill while the other disappears, pauses, rejects, partially fills or requires fresh margin. CEX inventory and the DEX leg do not settle atomically.
- CEX fiat cash, stablecoins, spot, margin and outstanding transfers share custody risk. A historical regulator complaint documents why reported account balances can differ from accessible recoverable assets ([S06](https://www.cftc.gov/PressRoom/PressReleases/8638-22)).

## Required tests and mitigations

Replay order-book/AMM depth with synchronized observations, adverse queue assumptions, partial fills, taker/maker fees, failed gas, rebalancing and transfer delays. Deny withdrawals and independently deny trading; measure residual inventory. Stress depeg, oracle/reference failure, gas, bridge delay, DEX chain halt, changed limits/fees and a larger competitor.

Pre-position inventory inside all issuer/chain/protocol/CEX caps; do not assume immediate free transfer or rescue credit. Stop on stale data, excessive venue divergence, unreconciled balances or broken hedge access. L1 builder-dominated opportunities remain excluded unless data proves an entrant-contestable niche.

**Reassessment inputs:** actual venue eligibility, API/latency evidence, depth/queue reconstruction, admissible fills, fees and correlated margin/custody stresses. No future CEX default probability, actor net return or monthly 99% bound is established.
