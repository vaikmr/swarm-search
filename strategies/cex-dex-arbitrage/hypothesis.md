# CEX-DEX arbitrage

Stage: discovery only. Status: **unverified**.
**Requires CEX access**; none was connected or used by this scout.
No qualifying T1/T2/T3.

## Hypothesis and exclusion

A demonstrably contestable non-builder-dominated niche would need executable
cross-venue spread after exchange fees, hedging, inventory, latency and actual
winning inclusion costs. Ethereum L1 builder-dominated opportunities remain
excluded absent contrary niche evidence. No such niche has been established.

## Public actor leads, not return evidence

[Measuring CEX-DEX Extracted Value and Searcher Profitability](https://arxiv.org/html/2507.13023v3#A1.SS1)
publishes label-to-contract mappings. These are paper leads only, not independent
verification of identity or this study's realized PnL:

- Wintermute label: `0x0000006daea1723962647b7e189d311d757fb793`.
- SCP label: `0xa69babef1ca67a37ffaf7a485dfff3382056e78c`.
- Kayle pseudonym: `0xbc2c6cd5013585ac720160efcb1feced30837177`.
- Taric pseudonym: `0x767c8bb1574bee5d4fe35e27e0003c89d43c5121`,
  example [transaction](https://etherscan.io/tx/0x0488cad7726ed6947be6af09d17b012fd7c986cb32a9d59cd7285b9a4e0926be).

The paper estimates CEX execution because it cannot directly observe the CEX leg.
Therefore its estimated PnL is not a reconciled realized-actor T1 result under the
user's rules. No paper return or concentration percentage is adopted here.
The paper also explicitly excludes solver/aggregator activity from its CEX-DEX
classification, a useful warning against double-counting actors across strategies.

## Next gate

Verify a legal, contestable market and actual access/cost schedules at the selected
CEX. Public DEX activity plus historical CEX mid-prices does not reveal actual
CEX fills, balances, fee tiers or withdrawals. A new entrant's replay must use
available depth, conservative latency, adversarial competition and executable
prices, not incumbent volume or assumed fills. Without those data, this candidate
cannot establish realized actor PnL or a capital-adjusted recommendation.
