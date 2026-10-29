# Independent review of observed holder components

Review date: 2026-10-29. Immutable input: scout commit
[`cd38c61b47ee55e3a3f1b9f9aeb892a4a2171a77`](https://github.com/vaikmr/swarm-search/tree/cd38c61b47ee55e3a3f1b9f9aeb892a4a2171a77/strategies/benchmark-lending).
This review independently recomputed selected accounting quantities from the
archived, normalized observations. It did not make new public RPC requests,
authenticate a fresh chain response, identify a beneficial owner, or conduct a
fork, audit or complete actor-PnL reconstruction. The independent judge owns
qualification decisions.

## Checks actually performed

- Ran the supplied benchmark simulation-directory tests on an isolated export
  of the immutable input: **26 tests passed** in this review.
- Reran its offline reconciler; generated JSON matched the committed
  `actor-reconciliation.json` exactly.
- Separately recomputed unit interest, external-flow-adjusted endpoint component
  marks, and sender gas from the archived observations using Decimal/integer
  arithmetic, without calling the scout's reconciliation functions.
- Checked transaction-hash identity on the retained receipts and compared the
  selected transfer identities with scoped logs from **all 102 retained
  receipts** in both directions: the same **126** identities appeared.
- Confirmed 41 unique normal transaction hashes and one address-sent withdrawal
  transaction per withdrawal block in this capture. The latter matters because
  the segment inventory observations are end-of-block, not transaction-local.

The separately computed component result was
**$173,641.32936046476502656973587238**, after observed network fees.
Post-opening position interest was **194,463.135111 USDC**; the 39 sender
transactions paid **334,130,451,297,696 wei**. These are corroborated
calculations on the captured dataset, not independently collected market
observations or full net profit. No extra gas subtraction was applied to the
native-balance-inclusive component result.

## What this improves

This is actual historical address-component evidence, not merely an APY
scenario. The declared 14.044444-day interval, actual transfer/receipt matching,
historical reference marks, exact cash residuals and source-backed index
rounding make the partial result more auditable. The report correctly keeps
full actor net PnL null and does not claim T1/T2/T3.

The capture documents successful historical withdrawals, but distinguishes
13 withdrawals from four observed zero-inventory segment endings. Those
observations do not demonstrate future or stressed withdrawal availability.

## Risk and accounting boundaries that remain

1. **Visited receipts are not the whole chain.** The reverse log comparison
   closes a consistency gap within the retained receipts only. It cannot
   recover transactions never returned by the indexer, omitted internal calls,
   or offsetting missing flows. Zero endpoint cash residuals are not a proof
   of exhaustive event coverage.
2. **Endpoint debt is not a continuous leverage history.** Zero Aave debt at
   both endpoints does not rule out borrowing and repayment between them,
   other protocols, other addresses, or external liabilities. It does not
   certify the actor's complete equity or capital at risk.
3. **Protocol marks are not independent exit prices.** Aave oracle marks
   support the explicitly declared accounting basis, not actual USD conversion
   proceeds, executable prices, or independent confirmation during an
   oracle/depeg incident. Endpoint configuration equality does not establish
   unchanged configuration throughout the interval.
4. **The sampled account is not the proposed portfolio.** An approximately
   $134 million observed position and its paid fees cannot establish attainable
   dollars, costs, custody structure or concentration compliance for $50,000.
   Recurring counterparties are external capital flows, not presumed
   independently owned accounts or assumed common ownership.
5. **No tail certificate follows from this interval.** Endpoint component
   accounting does not measure whole-portfolio running-peak drawdown, monthly
   99% coverage, an annual scenario frequency, stressed liquidity, or the
   unspecified reserve's losses. No event probability has been inferred.

**Outcome:** the selected historical accounting result is reproducible from the
archive, with useful two-way receipt consistency. Full actor net income,
complete strategy scope and the proposed portfolio's risk qualification remain
unestablished. This does not change the prior reserve, common-dependency,
all-in-cost or audit-linkage blockers.
