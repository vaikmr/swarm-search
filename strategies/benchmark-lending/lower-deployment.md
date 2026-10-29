# Lower-deployment baseline — conditional, not certified compliant

The prior three-chain allocation is a nominal-cap prototype, not a requirement
to invest 90% or a compliant benchmark. A conservative next study uses only
**Aave V3 Ethereum USDC**, counts its Ethereum/protocol/USDC failure domains
together, and leaves substantially more money off-chain.

## What was verified

- The official [executed activation proposal 147](https://governance-v2.aave.com/governance/proposal/147)
  dates Ethereum V3 activation to January 27, 2023 and explicitly lists USDC.
  This is stronger evidence of market age than an aggregator's first sample.
- The pinned official address registry identifies pool
  `0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2`, underlying
  `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` and aToken
  `0x98C23E9d8f34FEFb1B7BD6a91B7FF122F4e16F5c`.
- A public Ethereum read at block **26,296,884**, timestamp
  **2026-10-29 07:24:59 UTC**, returned the proxy implementation
  `0x728a138a4823392c2efa55e028d434f526fe03cf`, matching the pinned registry.
  The implementation's public explorer source is verified, named `PoolInstance`.
- USDC `balanceOf(aToken)` at that same block was **134,392,870.622605 USDC**.
  This is point-in-time token inventory, not a reserved withdrawal or proof of
  exit capacity under stress. The existing provider snapshot reports about
  $16.326B Aave V3 protocol TVL and $134.848M for this pool.
- [Public Aave audits exist](https://aave.com/security). Exact current
  implementation/aToken/admin/oracle-to-audited-build coverage is **not yet
  established**; verified source and a registry match do not prove audit coverage.

All requests, block hash, source hashes and limitations are in
[`aave-usdc-deployment-identity.json`](evidence/aave-usdc-deployment-identity.json).
No transaction or paid data source was used.

## Capital and cost budget, not a probability

Under a **hypothetical aggregate all-cost ceiling of $500 per month**:

```text
one-month full-principal-loss component = principal + $500
one-year full-principal-loss component = principal + 12 * $500
```

With **$4,000** principal and **$46,000** initially off-chain, these components
are $4,500 / 9% in one month and $10,000 / 20% over a year. This assumes one
non-replenished principal budget and every cost fits the scenario ceiling.
It is not a probability estimate, 99% drawdown claim, annual solvency guarantee,
actual expense quote or authority to spend $500.

The earlier $4,500-principal example fits a 10% monthly component budget with
$500 costs, but **fails** the corresponding 20% annual component budget at
$10,500. The $4,000 example avoids that arithmetic mistake. A $15,000 position
obeys the 30% concentration cap but full loss would already exceed the 10%
monthly component budget even before costs.

The exact source-rate calculations and capital ladder are in
[`lower-deployment-sensitivity.json`](evidence/lower-deployment-sensitivity.json).
At $4,000 principal they give **$12.581271 gross over 30 days** and
**$35.178977 gross over 90 days**. These are not cost-covering or net claims.
The preserved 30/90-day histories are rate inputs, not account PnL. Cash income
is explicitly zero in the scenario, while actual cash yield and risk are unknown.
Actual costs and net returns remain unknown.

The $500 scenario would have to cover gas, entry/exit, failed attempts,
monitoring, adverse unwinds and every other expense. The independent ledger's
infrastructure-budget flag covers infrastructure **only** and is not used here
as evidence that all-in costs fit this ceiling.

## Why full feasibility remains unresolved

The off-chain reserve is **not risk-free by assumption**. At a conservative
$15,000 per independent counterparty, $46,000 needs at least four custody slots.
These are arithmetic placeholders, not actual available accounts or a claim
that four independent, legally accessible, insured places were verified.
Insurance, beneficial owner, aggregation, jurisdiction, FX, withdrawal delay,
credential compromise and common custody/government dependencies must be mapped.
No CEX or bank was selected, opened, funded or added to the allowed venue set.

For example, [FDIC guidance](https://www.fdic.gov/resources/deposit-insurance/understanding-deposit-insurance)
distinguishes insured bank deposits from non-deposit products and crypto assets;
it does **not** establish this operator's eligibility or turn stablecoins into
insured cash. A Treasury product is not itself an FDIC-insured bank deposit.

The loss-budget example bounds only specified sleeve losses relative to initial
capital. It does not cover cash losses, all portfolio paths or a monthly maximum
peak-to-trough drawdown. No assumption is made that every shared-L1 incident
causes total loss: full loss is an explicit severe component stress, and there
is no second chain here to falsely treat as independent.

This is a better bounded research candidate, not the requested certified
compliant baseline. Finish current-deployment audit linkage and cash exposure,
price all actual costs, and require qualifying T2 plus T3 and independent risk
review. Reconciled T1 actor evidence is preferred, not mandatory. The conditional
annual component budget does not establish the separate annual tail-probability gate.

## Reproduction

From the repository root, with Python 3 and curl:

```sh
python3 strategies/benchmark-lending/sim/snapshot_market_identity.py
python3 strategies/benchmark-lending/sim/build_lower_deployment.py
python3 -m unittest discover -s strategies/benchmark-lending/sim -v
```

Identity collection pins the stated historical block and registry commit. A
future provider that does not serve that block should fail rather than silently
substitute current state. The stress tests are synthetic arithmetic checks,
not observed loss episodes or confidence estimates.
