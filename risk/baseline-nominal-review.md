# Independent review of the nominal-cap lending prototype

Date: 2026-10-29. This follow-up reviews the scout's immutable [candidate allocation](https://github.com/vaikmr/swarm-search/blob/0767bcc1cb2b01d3dfc732fc7ed3c8b9f625652f/strategies/benchmark-lending/evidence/candidate-allocation.json), not a live account. It does not originate strategy return evidence or judge the scout's work. All new arithmetic below is **T4 conditional stress arithmetic**, not a calibrated loss distribution.

## Allocation actually reviewed

The prototype declares $15,000 Aave/Ethereum/DAI, $15,000 Compound/Arbitrum/USDT, $15,000 Morpho/Base/SparkUSDC and $5,000 unspecified off-chain cash. Its own status is `NOMINAL_CAPS_ONLY_NOT_A_COMPLIANT_OR_RECOMMENDED_ALLOCATION`; costs and net income remain unknown. This review preserves that status.

The 90% on-chain maximum is a **ceiling, not an objective**. No strategy needs to use all available chain, issuer or protocol headroom. Additional reserve can be appropriate, but unused capital must remain in the return denominator and its custody/dependency treatment must be explicit.

## Findings

| Item | What the supplied artifact establishes | What remains unresolved |
| --- | --- | --- |
| Named-chain caps | Ethereum, Arbitrum and Base each have a nominal $15,000 sleeve. | Common Ethereum settlement/liveness dependencies affect all three. Counting separate names does not prove independence. |
| Protocol caps | Aave, Compound and Morpho each have a nominal $15,000 sleeve. | Exact deployed contracts, vault allocations, curator/manager dependencies, collateral, oracle and upgrade control are not reconciled. |
| Stablecoin caps | DAI, USDT and USDC each have a nominal $15,000 sleeve. | DAI underlying reserve/collateral may overlap USDC or other common dependencies. The artifact does not provide a verified backing matrix. |
| Off-chain reserve | $5,000 is outside the three nominal chain buckets in the model. | The counterparty, account form, liquidity, recovery treatment, issuer look-through and genuine independence are unspecified. |
| Eligibility | Protocol-wide public metadata and a potential vault identity are leads. | Specific deployed-market/vault age, TVL, relevant audit linkage and aggregator-to-vault mapping are not established. |
| Return | The scout supplies a reproducible gross historical-rate illustration. | This review has not independently rederived that yield series; actual net return and risk-adjusted benchmark remain unverified. |

### Shared settlement: map the failure, do not invent the loss

The declared sleeves sum to $45,000 potentially affected by a common Ethereum settlement failure, **if that scenario actually impairs all three sleeves**. This is a dependency-screening sum, not proof that an Ethereum incident destroys $45,000. Temporary sequencing failure, L1 finality disruption, withdrawal delay, bridge failure and permanent loss are distinct scenarios. Each must specify access restrictions, affected claims, duration, legal/technical recovery and executable marks.

For a deliberately assumed **joint 15% recoverable-value impairment** of those $45,000 sleeves, direct unlevered loss is $6,750 (13.5% of total capital), before costs. For a separately assumed **joint 25% impairment**, it is $11,250 (22.5%). These arbitrary severities illustrate why the shared failure matters; neither is an observed outcome, probability, quantile or claim that the annual kill gate is met. A pure delay must instead report unavailable liquidity and justified funding/valuation costs without automatically writing off principal.

Reproduce those two calculations from the repository root:

```sh
PYTHONPATH=risk python3 -c 'from stress_checks import conditional_loss; print(conditional_loss("45000", ".15")); print(conditional_loss("45000", ".25"))'
```

A risk-based haircut is not free concentration headroom. Do not discount away a shared dependency using an unsupported probability or loss-given-default estimate, and do not declare independence merely because a stress happened to leave book value unchanged.

### Stablecoin look-through: no hidden spare capacity

If the direct USDC sleeve already occupies the full $15,000 cap, any **verified additional positive effective USDC exposure** through DAI or another position consumes headroom that is not present. As a bookkeeping illustration only, with an assumed effective overlap coefficient \(q>0\), declared USDC exposure becomes \(15,000 + 15,000q\). No value of \(q\) has been estimated here.

A reserve/collateral fraction is not automatically identical to a token holder's USD loss sensitivity: overcollateralization, liquidation, redemption rules, other collateral and governance matter. Obtain dated issuer/collateral evidence and define the scenario transmission before calculating effective exposure. Neither zero overlap nor full-face overlap is silently assumed.

### More reserve: name the account and common failures

Moving money out of lending can reduce protocol risk but does not make it riskless. A larger balance at one CEX shares its custody/freeze domain; a stablecoin at that CEX still has issuer risk. An unspecified bank/cash account cannot be credited with insured recovery, immediate access or unlimited diversification. A balance on a fourth chain is not an off-chain reserve and would introduce another chain.

Thus, replacing the prototype with a single smaller on-chain sleeve and an unspecified large cash reserve is **not yet** a demonstrably compliant baseline. Reserve custody must be included in the same no-single-point-of-failure analysis. This is a disclosure/research blocker, not permission to relax caps or open accounts.

## Requirements for the next candidate

- Select at most the allowed number of chains, with documented distinct or bounded shared failure domains. The scout owns market/rate selection; this review does not nominate unverified alternatives.
- Supply the exact market/vault and underlying token identities, deposited-asset mapping, current vault allocation and relevant age/TVL/audit evidence.
- Provide dated issuer/collateral/bridge/settlement and reserve-counterparty dependencies. Separate declared capital at risk, recoverable value, liveness lock-up and conditional loss.
- Rerun concentration across **all** sleeves and reserves, not separate strategy worksheets. Preserve whole-capital accounting when deploying less.
- Reconcile costs, then run genuine replay and forward paper evidence plus local stress tests. Apply both the monthly drawdown requirement and additional annual-scenario rule; do not treat the p5 screen as the 99% certificate.

**Outcome:** the nominal allocation is suitable as a clearly labeled research illustration only. No current compliant net benchmark, quantified shared-tail probability, or 99% monthly drawdown bound is established. The next review needs a specific revised allocation and dependency evidence, not a target percentage of capital deployment.
