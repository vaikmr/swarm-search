# Lending benchmark — independent risk specification

Date: 2026-10-29. Status: **not risk-certified; allocation and tail-frequency evidence missing**. No strategy verdict or return evidence is supplied here.

Apply all eight scenarios and both loss gates in the [shared review](../../risk/README.md). Historical/design references are in [the source registry](../../risk/sources.json); none is T1 return evidence.

## Candidate-specific failure paths

- Depositing the same stablecoin in several markets does not diversify issuer risk. Depositing through the same protocol on several chains does not diversify its common code/governance failure domain. A vault inherits its lending markets, collateral and curator dependencies.
- Borrower collateral shocks can leave bad debt; utilization or a protective pause can prevent immediate withdrawal even when an account appears solvent. Aave's historical protective pause is context, not a claim that every current deployment is paused ([S07](https://governance.aave.com/t/aave-v2-v3-security-incident-04-11-2023/15335/37)).
- The USDC depeg is a direct challenge to any stablecoin-at-par benchmark ([S01](https://www.circle.com/pressroom/3-3-billion-of-usdc-reserve-risk-removed-dollar-de-peg-closes), [S02](https://www.federalreserve.gov/publications/2023-may-financial-stability-report-funding-risks.htm)). Recovery later does not eliminate intramonth drawdown.

## Required tests and mitigations

Use unlevered deposits for this benchmark. Reprice underlying assets, measure withdrawable versus book value, delay withdrawals, disable incentives, and change rate/utilization parameters. Include congestion, stale oracles, chain halt and bridge-backed collateral failure. A competitor/capital inflow may dilute rates; no fixed dilution percentage is assumed.

Bound exposure by actual issuer/protocol/chain dependencies. Include the required off-chain reserve in whole-capital return. If the reserve sits on a CEX, apply the CEX freeze stress even though lending itself does not require one. Verify specific market age, TVL, audit scope and available exit depth rather than assuming the protocol's brand suffices.

**Reassessment inputs:** proposed allocation, current market/deployment identities, withdrawal evidence, oracle/parameter snapshots, actual benchmark output, and a defensible tail model. All probabilities and statistically estimated monthly bounds remain unavailable.
