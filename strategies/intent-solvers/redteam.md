# Intent-auction solving — independent risk specification

Date: 2026-10-29. Status: **not risk-certified; bond/admission and settlement-obligation evidence missing**.

Apply all eight scenarios and both loss gates in the [shared review](../../risk/README.md). No final strategy verdict or return evidence is supplied.

## Candidate-specific failure paths

- Permissionless publication of intents does not establish permissionless solver admission. Bonds, whitelists, auctions, exclusivity, slashing, deadlines and settlement penalties must be taken from current official rules for the chosen venue.
- Escrowed bonds, execution balances, unsettled fills and derivative hedges can all depend on the same protocol. A bond exceeding the charter's failure-domain cap cannot be dismissed as idle capital.
- Non-atomic or cross-chain obligations expose the entrant to delayed settlement, finality and inventory risk. Across's distinct relayer model documents why fronting capital is a real exposure; it does not establish another solver venue's exact rules ([S05](https://docs.across.to/introduction/actors)).

## Required tests and mitigations

Prove admission and funds requirements before modeling captured flow. Include losing bids, deadline misses, ordinary settlement failures and configured penalty cases. Test larger competitors, fee/reward changes, depeg, stale oracle/quotes, gas shocks, chain halt and bridge delays. Stress any CEX hedge/credit path as frozen.

Constrain outstanding obligations and collateral by shared failure domain; stop new commitments if settlement reconciliation is stale. Prove lawful atomic settlement where relied upon, rather than assuming it from a successful historical transaction by an incumbent.

**Reassessment inputs:** venue/version rules, eligibility, bonds/penalties, accessible order history, local decision/fill admissibility and exposure ledger. No bonding number, slashing probability or risk-adjusted return is invented.
