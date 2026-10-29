# Across: independent entrant-capacity review of the historical slice

**Result: the committed record supports a finite next reconciliation step, not a
positive entrant capacity, realized profit or measured inventory-lock bound.**
This review uses only offline evidence pinned to
[`23d2fd1`](https://github.com/vaikmr/swarm-search/tree/23d2fd15c1d736b6c8cee4614e82f3d55fc430c4/strategies/cross-chain-relaying/evidence).
No new RPC or market-data request was made. The existing $50,000 portfolio,
maximum-three-chain scope and $15,000 shared-protocol exposure cap are unchanged.

Sources: [historical availability report][REPORT],
[request/aggregate summary][SUMMARY], [selected decoded witnesses][WITNESSES],
and [collector implementation][COLLECTOR]. The independent
[offline checker](capacity_sources/verify_across_ledger.py) produces
[across_crosscheck.json](capacity_sources/across_crosscheck.json), including
SHA-256 digests of the two source JSON files.

## 1. What was independently checked

The recorded interval is **(OP block 158224884, 158829684]**, with endpoint
timestamps **2026-10-15 07:15:45 UTC** and **2026-10-29 07:15:45 UTC**:
**1,209,600 seconds / 14 historical days**. The manifest contains 61 contiguous,
nonoverlapping requests per event kind, covering the complete selected block
range with at most 10,000 blocks per page. All 122 page records report success;
the actor-indexed fill filter and pool/topic roles are consistent with the
collector. This is request-manifest consistency, not an independent provider
completeness guarantee or exhaustive historical contract/version coverage.

The summary reports **2,915 OP destination fill events** and **983 OP refund
events containing actor allocations**. Its repayment-chain counts sum to 2,915:
**2,076 select Arbitrum, 72 select OP, and 767 select other chain IDs**.
The independently checked sum does **not** independently recount 2,915 raw
logs: bulk log responses/per-event rows were deliberately omitted from Git.
Response hashes provide provenance for retrieval but cannot replace those
bytes for a fresh decode. The retained first/last decoded witnesses lie within
the declared interval.

Token scaling is exact, with no USD marks or assumed pegs. In the selected
successful refund receipt, **300,000 raw OP USDC units = 0.300000 USDC** and
**30,398,523 raw bridged-USDT units = 30.398523 bridged USDT**, using the recorded
six decimals. The selected allocation and transfer amounts agree. These are
consistency checks of curated decoded rows, not a fresh raw-receipt validation.
They do not turn the full set of 983 allocation events into verified spendable cash.
The example transaction sender is **not** the selected relayer, so its gas bill
must not automatically be assigned to that relayer.

The account nonce advances by **4,661**, but neither that difference nor its gap
from 2,915 fill transactions is a classified transaction census. No failed-gas,
rebalancing or unrelated-transaction total can be inferred from it.

## 2. The chain roles prevent a one-chain profit or lock calculation

OP is the **destination cash-outflow chain** in the queried fill set.
`repaymentChainId=42161` is an explicit **Arbitrum repayment choice**, not proof
of an Arbitrum payment, an Arbitrum-origin deposit or available reusable funds.
An OP refund allocation can instead reimburse fills made on another chain.
Therefore none of these are valid:

- Subtracting OP fill outputs from OP allocation totals to obtain profit.
- Treating the 2,076 Arbitrum-repayment fills as a closed two-chain strategy.
- Dividing observed actor volume by $50,000 to obtain entrant capital turnover.
- Treating any allocation, nondeferred flag or nonce change as a settled receipt.
- Treating a returned Arbitrum token as immediately refillable OP inventory.

One retained boundary witness has both **origin and repayment chain 42161**,
destination OP, and **100,000 raw OP USDC output units = 0.100000 USDC**. It is
in the closing OP block. This is a concrete route to investigate, not a matched
claim/payment, scalable profitable trade or demonstration of a $50,000 operator.
There is no aggregate origin-by-repayment matrix in the committed summary.

A fill consumes destination cash and creates a receivable. A matched actual
payment extinguishes that receivable and creates cash on its payment chain;
the cash must not be counted again as an outstanding claim. Where payment is
on Arbitrum, **OP inventory reuse additionally needs an evidenced rebalance or
independently funded OP inventory**. The data do not measure either interval.
No finite maximum lock time, peak outstanding principal, or available entrant
share follows from this slice. Unmatched claims remain unknown/censored, not
zero; neither boundary's complete receivable is known.

## 3. Smallest finite next evidence package

This is a data specification, **not authorization for new network collection**.
First obtain a source-hashed export of the already-collected selected OP rows,
if available; do not repeat the 146-request probe merely to inspect them.

Start with **one predeclared route family**: canonical USDC from Arbitrum to OP,
with repayment on Arbitrum, one selected relayer address and the same fixed
14-day interval. It uses two execution chains; Ethereum hub/root provenance may
require a third chain. Shared Ethereum settlement remains one correlated
failure domain rather than independent L2 diversification. Verify exact token,
pool and implementation mappings at the relevant blocks; do not infer them
from symbols. Other-chain events stay outside this restricted study, not inside
its profit denominator. The original actor's full profitability still requires
its wider ledger.

The smallest matching proof is **one deterministic, non-profit-selected fill**
(for example, the earliest eligible fill by block/transaction/log order in
the exported interval), not every transaction the actor ever made. Require:

1. **Fill and deposit identity.** Raw receipt/log, actual output amount, origin
   chain and deposit ID/relay identity; its actual Arbitrum deposit, applied
   quote/update terms, token mapping, decimals and block timestamps. Do not
   subtract input/output amounts across chains without the exact entitlement
   and valuation rules.
2. **Entitlement-to-bundle membership.** The actual bundle/version/block ranges
   and proof or reproducible accepted bundle computation linking that fill to
   an actor/token refund leaf. Pin the OP-local root identifier to its canonical
   hub/root context and Arbitrum leaf execution. A refund leaf aggregates fills;
   raw OP refund events alone do not provide a per-fill foreign-chain match.
   **No FIFO or amount-only matching** substitutes for that membership.
3. **Actual Arbitrum cash receipt.** Successful receipt and token transfers (or
   the correct deferred-payment/claim path), actor/recipient, exact raw units
   and chain timestamp. Keep allocation, payable entitlement and paid cash as
   separate statuses; identify the gas payer rather than assuming it.
4. **Boundary and reuse records.** Opening and closing token inventories,
   independently determined unpaid entitlements, liabilities and funding for
   the restricted route; any actual Arbitrum-to-OP repositioning, its receipts,
   costs and final OP spendability. Include claims from before the opening
   cutoff and claims unpaid at the closing cutoff. If no complete opening
   claims state is available, disclose that the slice cannot close.
5. **Cost and capital attribution.** Failed and nonfill attempts within the
   declared scope, paid execution/data fees, bridge/rebalance charges, external
   funding/withdrawals, asset price marks, relevant outstanding liabilities and
   dated infrastructure costs. Unrelated actor assets do not supply a free
   capital denominator; reserves and other strategies need their own custody
   and shared-failure-domain attribution.

Use fixed endpoints and explicitly cap this first test to one selected claim.
If it cannot be matched within the declared evidence range, publish the
unmatched/censored result and missing record, rather than extending the search
until a favorable refund appears. A single closed cycle would establish only
that cycle's observed timing and flows, not T1 profitability, attainable share,
a statistical latency distribution, guaranteed lock time, or T2/T3.

Only after that identity/matching proof succeeds should a separate bounded
stage cover **all eligible route-family fills in the same interval**, with
boundary receivables and full funding/rebalancing records. That is the minimum
needed to reconstruct this restricted inventory path and its *sample*
peak exposure. It still cannot establish the whole actor's capital-adjusted
return or a newcomer's winning probability.

## 4. What the $15,000 constraint permits us to say now

The shared Across exposure cap is **$15,000 in aggregate**, not $15,000 on OP
plus another $15,000 on Arbitrum. The same claim cannot be counted twice simply
because it appears in both fill and refund records. Protocol, chain/settlement,
issuer and bridge look-through remain overlapping constraints, each checked
against the specified limit; these cannot be diversified by account labels.

A conservative **proposed operating budget**, not measured available capital,
can also earmark at most $15,000 in total for this service's destination
inventory, unpaid principal and funds awaiting repositioning, using consistent
USD marks and excluding double counting as claims become cash. An earmarked
budget is deliberately stricter than a claim about which wallet assets would
actually be lost in an Across failure. Direct wallet cash, settled claims and
bridge-pending funds require their own causal failure-domain classification.

Admission of a next fill would require its worst-case outstanding exposure and
all existing claims/committed inventory to remain within every applicable
limit, **before** assuming any refund or rebalance will complete. Receipts,
rebalance timing, cash funding and valuations are not available here, so no
numeric operational capacity, reusable-turnover forecast or feasible entrant
allocation is certified. Off-chain residual cash also remains subject to the
existing custody/access constraints; it is not silently risk-free.

This update does not change the performance tiers: the offline arithmetic is
T4; the primary event/state availability remains unqualified T1, and there is
no T2 replay, no T3 elapsed forward observation and no recommendation.

[REPORT]: https://github.com/vaikmr/swarm-search/blob/23d2fd15c1d736b6c8cee4614e82f3d55fc430c4/strategies/cross-chain-relaying/evidence/HISTORICAL_LEDGER_AVAILABILITY.md
[SUMMARY]: https://github.com/vaikmr/swarm-search/blob/23d2fd15c1d736b6c8cee4614e82f3d55fc430c4/strategies/cross-chain-relaying/evidence/history-probe-summary.json
[WITNESSES]: https://github.com/vaikmr/swarm-search/blob/23d2fd15c1d736b6c8cee4614e82f3d55fc430c4/strategies/cross-chain-relaying/evidence/history-witnesses.json
[COLLECTOR]: https://github.com/vaikmr/swarm-search/blob/23d2fd15c1d736b6c8cee4614e82f3d55fc430c4/strategies/cross-chain-relaying/evidence/probe_actor_history.py
