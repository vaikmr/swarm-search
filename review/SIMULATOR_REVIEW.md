# Independent simulator and evidence-boundary review

Review date: 2026-10-29. Strategy returns, fills and safety remain unverified.

Immutable originals reviewed:

- Replay/evidence: [`c154e78cbb761c3f26000a4f4a899362da559119`](https://github.com/vaikmr/swarm-search/commit/c154e78cbb761c3f26000a4f4a899362da559119).
- Paper/yield: [`831c0a310eb75281cb349bdc5cbbdcadd1665ef2`](https://github.com/vaikmr/swarm-search/commit/831c0a310eb75281cb349bdc5cbbdcadd1665ef2).
- Independent risk specification: [`49d5c01f43cbd2e0a7416d5e7da74603adc76d6a`](https://github.com/vaikmr/swarm-search/commit/49d5c01f43cbd2e0a7416d5e7da74603adc76d6a).

The originals were inspected together at integrated revision [`e716c892b29cdf0074aa402e1a4c3e3a50e19204`](https://github.com/vaikmr/swarm-search/commit/e716c892b29cdf0074aa402e1a4c3e3a50e19204). Git blob identities of both simulator modules in each package matched the original commits. No owner code was modified by the judge.

## S1 — Medium: funding window-edge completeness is not fail-closed

Reference: [`yield_data.py` lines 210–230](https://github.com/vaikmr/swarm-search/blob/831c0a310eb75281cb349bdc5cbbdcadd1665ef2/research_tools/yield_data.py#L210-L230).

The first/last observation can be as far as one period plus tolerance from the requested boundaries. Pairwise gap checks do not catch an omitted first/last scheduled event.

**T4 synthetic reviewer example, not market evidence:** request the inclusive millisecond interval `[1, 7200000]`. Supplying only an event at `3600000` with rate `0.0001` passes. At a synthetic 10,000 USD notional, the component is positive 1 USD. Adding the omitted event at `7200000` with rate `-0.0002` changes the full-window component to negative 1 USD.

This demonstrates that the generic completeness check can accept a selected subset that omits a loss. It does **not** establish that a committed market sample omitted data.

Requested owner action: validate expected scheduled event buckets and window edges with explicit handling of actual source timestamp jitter, or mark ambiguous boundaries incomplete. Add regression cases for missing first/last events, exact and unaligned cutoffs, and legitimate source jitter. Do not silently replace missing payments with zero.

**Owner correction independently verified:** [`5163ebc63d0572e8c2802db3bbd2bbadcd522666`](https://github.com/vaikmr/swarm-search/commit/5163ebc63d0572e8c2802db3bbd2bbadcd522666) adds exact inclusive scheduled-event count, edge and consecutive-slot checks; tolerance applies only to source timestamp jitter. The judge inspected the change, ran all 28 paper/yield tests in a separate immutable worktree, and independently confirmed that missing first/last events are rejected. S1 is resolved in that correction under its documented epoch-hour grid assumption, without changing evidence tiers or certifying point-in-time publication.

### Independent check of the delivered BTC sample

For each comparator, the judge independently selected its published interval and compared unique hourly buckets with the expected bucket range. The delivered 30-day comparator had 720 observations for 720 expected buckets; the 90-day comparator had 2,160 for 2,160 expected buckets. Neither had missing, extra or duplicated buckets in that check.

Those counts describe the committed source input, not strategy evidence. The defect above does not invalidate these samples on the specific hourly-coverage check. Original publication times, possible API revisions, execution, complete costs, hedge marks and margin paths remain unverified. The committed net component is correctly `null` when costs are unknown.

## S2 — Coverage limitation: unsettled positions cannot be represented

Reference: [`replay.py` lines 166–173](https://github.com/vaikmr/swarm-search/blob/c154e78cbb761c3f26000a4f4a899362da559119/research_tools/replay.py#L166-L173); output limitation at [line 342](https://github.com/vaikmr/swarm-search/blob/c154e78cbb761c3f26000a4f4a899362da559119/research_tools/replay.py#L342).

Every opportunity must settle inside the observation window. A synthetic position with a loss mark before the cutoff but settlement after the cutoff is rejected. This is fail-closed rejection, **not a demonstrated silent loss omission inside the engine**.

Nevertheless, an adapter that filters unsettled positions to satisfy this requirement can censor losses, receivables, margin and locked capital. The output instruction to include end-of-window positions cannot be fully satisfied by the current closed-position-only schema.

Disposition: acceptable only as a documented T4 closed-position accounting restriction, not as a complete monthly portfolio replay. Future qualifying replay must carry opening/closing inventory, unsettled claims and liabilities at the cutoff without using later settlement outcomes as information available at the cutoff. Do not drop such positions or call the resulting subset complete.

**Owner disclosure correction independently verified:** [`d9a5befd2b69badd03fabdfa17867a0663397acc`](https://github.com/vaikmr/swarm-search/commit/d9a5befd2b69badd03fabdfa17867a0663397acc) explicitly emits `scope = closed_positions_only`, `portfolio_coverage_complete = false`, and `monthly_portfolio_pnl_validated = false`. Broad coverage/monthly aliases were replaced with closed-cohort labels. The judge ran all 32 replay/evidence tests and independently checked those output fields. The reporting ambiguity is resolved there; actual full-portfolio carryover is still not implemented and remains a qualifying-replay blocker.

## S3 — Original cash naming issue: independently verified owner correction

The original replay field `cash_net_pnl_usd` included marked/accrued economics, mirroring cost-review C1.

Owner correction [`90beba4bda7d31823e61b728116877378166fd0b`](https://github.com/vaikmr/swarm-search/commit/90beba4bda7d31823e61b728116877378166fd0b) removes that field, emits `net_economic_pnl_usd`, leaves `realized_cash_pnl_usd = null`, and adds a focused regression.

The judge inspected the exact diff, checked out that immutable correction and independently ran all 15 replay and 16 evidence tests successfully. **The replay naming issue is resolved in that correction**, without certifying realized cash, strategy performance or any higher evidence tier. Integration into another branch must preserve the same code and result.

## Evidence-boundary controls that passed inspection

- Replay outputs remain T4, `is_t2_evidence = false`, and `recommendation_eligible = false`. Price/mark accounting is not represented as a historical fork.
- Evidence-manifest validation checks integrity/metadata only and always leaves recommendation eligibility false. A metadata pass means content review is needed, not that source contents prove the claimed tier.
- Synthetic relabeling cannot become verified T1/T2/T3 merely by changing a manifest flag. The code expressly warns that even structurally consistent metadata does not establish truth.
- Unknown races and ties lose. Gross losses and interim negative marks are retained. Missing cost fields reject input; partial costs are not automatically treated as free.
- Locked principal and costs reduce available capital. Same-time identifier ordering, no margin-call model, and absent strategy-specific exposure checks are disclosed limitations, not completed execution/risk modeling.
- Paper observation defaults to no fills, no strategy version, no inventory and no T3. Missing source timestamps and source failures are recorded, not inferred successful.
- The paper coverage gate permits **independent review only**, not T3 certification. Local hash chains detect some edits, not a reconstructed complete log or independent real-world observation times.
- Funding signs are preserved, and left-point base-APY integration does not use the next APY. The documentation correctly discloses post-cutoff retrieval and unverified point-in-time publication/revision history.

The paper MTM primitive is not a complete perp/spot ledger. Any future adapter still needs explicit entry-price PnL, real cash, collateral, liabilities and realized/unrealized reconciliation; no generic helper or favorable bid/ask mark proves those exist.

## Independent risk-tool boundary review

The risk checker aggregates only **declared** exposure maps and exactly reconciles declared allocated equity. It does not prove wrapper look-through, custody independence or completeness. Its risk certificate remains false.

Conditional scenario severity is kept separate from annual event frequency; absent probabilities are `null`, and the annual kill gate is not declared established. IID statistical examples are labeled assumptions, not empirical probabilities or a demonstration of the monthly risk bound.

The judge ran all 12 risk tests and reproduced the committed deterministic output byte-for-byte. No arithmetic or false-certification defect was found in that scoped check. This was not an independent reconstruction of incident data, deployed exposures or future event frequency; historical incident bibliography is context, not T1 actor returns.

## Reproduction and limitations

At integrated `e716c89`, all 72 main tests passed. Separately, all 12 risk tests passed and generated output matched. At owner correction `90beba4`, all 31 replay/evidence tests passed; at `d9a5bef`, all 32 passed. At owner funding correction `5163ebc`, all 28 paper/yield tests passed. These are separate checked revisions, not a claim about an untested combined tree.

The additional historical probes are in `review/evidence/simulator_probe.py`. They intentionally check the original simulator blobs; do not expect old-version probes to validate a later corrected HEAD. To use an unchanged historical checkout:

```sh
git worktree add --detach /tmp/swarm-sim-original e716c892b29cdf0074aa402e1a4c3e3a50e19204
python3 review/evidence/simulator_probe.py --reviewed-root /tmp/swarm-sim-original
```

Test fixtures, counts and code checks are not profitable-actor observations, a fork replay, elapsed forward trading, or safety certification. No strategy verdict is upgraded. S1/S3 and S2's reporting ambiguity are resolved in their identified corrections. S2's full-portfolio carryover requirement remains a qualifying-replay coverage blocker.
