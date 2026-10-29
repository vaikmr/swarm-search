# Independent offline review: Across ledger availability

Date: 2026-10-29. **Discovery-source scope only. Relaying remains NOT READY.**

Reviewed immutable source package [`23d2fd15c1d736b6c8cee4614e82f3d55fc430c4`](https://github.com/vaikmr/swarm-search/commit/23d2fd15c1d736b6c8cee4614e82f3d55fc430c4): availability note, collector, committed summary/witnesses, and tests. No provider requests, source collection, trading, installation or fork execution were performed by this review.

## Supported result and verification boundary

The package reports successful historical Optimism reads and current-topic log pagination over `(158224884, 158829684]`. It is evidence of a **selected contract/event/state slice**, not a complete actor ledger.

The judge independently:

- Ran all 15 focused synthetic collector/history tests successfully at the immutable source revision.
- Checked all 146 committed manifest entries; the two event streams have exactly 61 successful, gap-free, nonoverlapping requested pages each, with the expected pool/topic/actor filters and exact block boundaries.
- Checked agreement of recorded timestamp forms and their 1,209,600-second interval; checked that reported repayment-chain/type counts sum to the reported fill count. These checks do not independently authenticate the underlying block headers or recount logs.
- Checked the selected example's allocation-versus-transfer amounts and transaction identifiers agree internally, and that its selected successful receipt names a different transaction sender from the selected actor.
- Confirmed actor PnL, deployed capital and boundary receivables remain `null`, while T1 qualification, complete coverage and fully reconciled costs remain false.

The ignored raw response bodies are not present in the judge's checkout. A published response digest is not the response itself. Therefore the judge has **not independently rehashed the raw responses, recounted all 2,915 selected fills/983 actor-allocation events, re-decoded all raw logs, or independently verified provider completeness**. Those remain source-reported aggregates, although committed cross-field consistency checks passed.

The summary and witness files reviewed here have SHA256:

```text
history-probe-summary.json
dbf2ebe7576773324ae604518a0e0494275de18a5a8488e0171ada4bd80c4cee
history-witnesses.json
9172258921e58191313809970a0cb97e51d38075059beae6326235bdd9048836
```

## L1 — Event attribution is not transaction-payer or entity attribution

The fill collector filters a selected address in indexed topic 3. Its distinct transaction-hash count is **not** an independently verified count of transactions signed or economically funded by that address.

The collector does not retrieve every fill transaction/receipt or correlate every sender. The code/committed source references do not pin a historically applicable ABI/build establishing all caller, repayment-beneficiary and relayer roles. Existing documentation correctly leaves sender correlation and related-address grouping unresolved.

The selected refund receipt explicitly has a different `from` address from the actor. Its gas cannot simply be charged to this actor, nor can third-party payment be assumed free of any reimbursement or service obligation. No economic payer attribution is established by the example.

Before actor PnL: pin historical event/function semantics and identify callers, beneficiaries, related addresses and economic fee payers separately. Nonce change is a diagnostic, not a classified transaction census or failed-attempt count.

## L2 — Cross-chain and boundary claims block net subtraction

The reported destination fill set chooses repayment on multiple chains, predominantly Arbitrum. Optimism refunds can also compensate fills made elsewhere. Consequently neither same-chain refunds minus fill output nor wallet balance change is actor PnL.

Destination payout creates a settlement claim; refund allocations, execution, actual token transfers, deferred/disputed claims and boundary inventory are separate ledger stages. The sample transfer corroborates an observable repayment leg, not a matched fill's fee, latency or realized return. A false batch-deferred flag does not complete that reconciliation.

Before actor PnL: map origin/destination/repayment roles, all-chain bundles/entitlements, opening/closing claims, token inventory, liabilities, external flows and costs. Do not use FIFO, output-versus-input token units, dollar pegs or instant inventory recycling without evidence. No alternative capital/capture estimate is supplied here.

## L3 — Requested page coverage is not complete activity coverage

The manifest's exact page topology supports the bounded availability finding. It does not prove that a provider returned every matching log, or that the chosen event topics/contracts exhaust activity.

Zero reported decode errors means no errors encountered for returned selected-topic logs under this decoder. It does not rule out omitted legacy topics, contracts, proxy upgrades, nonselected tokens, nonfill/reverted transactions or other accounts. The package appropriately keeps `source_coverage_complete = false`.

For a stronger source certificate, retain/review raw responses offline, independently check block/transaction/log identity and canonicality, and enumerate historically applicable deployments/events. A malformed or mismatched header/RPC response must not be accepted merely because the request asked for the correct block. No mismatch is demonstrated by this review.

## L4 — Selected balances and API examples do not fill the ledger gaps

The selected ETH/token endpoints are not total deployed equity or a capital denominator. Token decimals alone do not establish USD prices, historical contract equivalence or available exit liquidity. Native balance change is not gas consumption.

The unsupported deposits-API filter and empty offset pages establish only those observed API outcomes, not database retention or actor-history absence. A user-deposit refund reference is not a relayer-reimbursement ledger.

## Disposition and reproduction

Retain the package as a useful public-data availability lead. No erroneous promotion to profit/T1 was found in its explicit scope flags, and its principal limitations are candidly stated. **G3 actor equity/flows, G4 qualifying replay/entrant capture, G5 all-in net economics, G6 risk and G7 elapsed forward paper remain unestablished.** Prior individual verdicts are unchanged.

The deterministic committed-artifact checks are in `review/evidence/across_ledger_scope_probe.py`. Run against the pinned source checkout:

```sh
git worktree add --detach /tmp/swarm-across-source 23d2fd15c1d736b6c8cee4614e82f3d55fc430c4
python3 review/evidence/across_ledger_scope_probe.py --source-root /tmp/swarm-across-source
```

This script is deliberately network-free and verifies only the two pinned committed JSON files. It cannot authenticate or recount omitted raw pages. An offline raw rehash/recount and event-role clarification have been requested from the source owner, with **zero additional public requests**; any response must be distinguished from checks independently run by the judge.
