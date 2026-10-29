# Cross-chain relaying / intent filling

Stage: discovery only. Status: **unverified**, not a strategy recommendation.
No qualifying T1, T2 or T3 net return has been produced. No actor PnL is inferred
from protocol volume, fees, balance snapshots or successful fills.

## Hypothesis

Small, adequately priced transfers on established low-cost routes might support a
new inventory-backed relayer. This requires proving access to order flow, residual
margin after auction competition and all costs, and capital turnover while
repayments remain outstanding. An API fee quote is not a realizable relayer profit.

## Verified discovery facts

- Across uses nominated exclusive relayers, with open fills available after the
  exclusivity deadline. The documented entry path includes step-in fills and a
  performance history. [Nomination documentation](https://docs.across.to/introduction/relayers/relayer-nomination).
- A newer public registration repository says assignment is at Risk Labs'
  discretion and is not guaranteed. Its directory returned only `example.json`
  when queried on 2026-10-29; that example is not an observed active competitor.
  [Registration repository](https://github.com/across-protocol/relayer-registration-repository).
- The older public compiled configuration contained **46 entries** in the bounded
  discovery snapshot. This is an observed configuration count, **not** the number
  of active independent competitors or their market shares.
  [Public configurations](https://raw.githubusercontent.com/across-protocol/exclusive-relayer-configs/master/build/exclusive-relayer-configs.json).
- The public deposits endpoint returned actual fill transaction hashes and relayer
  addresses. The latest **50 deposits** covered **2026-10-29 07:14:50–07:17:07 UTC**.
  These discovery counts are not performance evidence. See the snapshot summary.
- Across's docs describe a **1.5-hour minimum root-bundle publication cadence**.
  This is a documented mechanism parameter, not measured reimbursement latency,
  guaranteed refund finality, or a safe turnover assumption.
  [Relayer documentation](https://docs.across.to/introduction/relayers/running-relayer).

## Actor leads

Addresses directly attributed as relayers in this short API sample include
`0xfd03abcadaf3f930fa4e37eb2f6ea3a44a41b7f0`,
`0x394311a6aaa0d8e3411d8b62de4578d41322d1bd`,
and `0x07ae8551be970cb1cca11dd7a11f47ae82e70e67`.
They are not attributed to legal owners. Full sample identifiers, hashes,
timestamps, chain IDs and source URL are retained in
[`evidence/snapshot-across-fills.json`](evidence/snapshot-across-fills.json).
Some rows marked filled have no relayer; do not manufacture attribution for them.

## Next evidence gate

Reconcile each fill with origin deposits, actual destination receipts, all
refund-root allocations and realized repayment timestamps over a qualifying
history. Reconcile all related addresses, inventory, rebalancing transfers, LP fees,
gas, failed fills and capital locked. Measure eligible non-exclusive flow separately
from nominated flow. A newcomer gets no assumed allocation from incumbent fills.
The protocol/chain/stablecoin/bridge concentration limits still apply to repayment
claims, not only wallet balances. Eligibility TVL, protocol age and audits remain
unverified in this package.

A subsequent [historical-availability probe](evidence/HISTORICAL_LEDGER_AVAILABILITY.md)
retrieved a complete fixed 14-day page interval for two current event topics and
selected Optimism balances for the same actor. It did not reconcile all-chain
receivables, capital, funding or costs, so it did not upgrade the evidence tier.

## Reproduction

Run `python3 strategies/cross-chain-relaying/evidence/collect_public.py`.
Only fixed unauthenticated public GETs are supported; no keys, transaction signing
or transaction submission are implemented. Default output is ignored
`data/raw/scout-execution/`. Tests:
`python3 strategies/cross-chain-relaying/evidence/test_public_scout.py`.
