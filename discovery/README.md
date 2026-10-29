# Discovery pass 2: mechanisms before infrastructure

**Authorized restart, 2026-10-29. One bounded eight-worker discovery pass.**

The user subsequently supplied [seven specific candidate mechanisms](USER_CANDIDATES.md) for pressure testing inside this same pass. The reported 21-trade perp-hedge counterfactual is first priority, conditional on recovering genuine inputs; no returns are assumed.

The user clarified that the goal is to discover new cross-chain arbitrage strategies by following papers, citations, recent instruments and actual on-chain activity. This is not a restart of the old passive-yield/validation loop. The prior [early closeout](../FINAL_REPORT.md) and twelve NOT READY verdicts remain historical facts, not proof that the opportunity space is exhausted.

## Source coverage

Seed: [Cross-Chain Arbitrage: The Next Frontier of MEV in Decentralized Finance, v2](https://arxiv.org/html/2501.17335v2#A7), including Appendix G's collateralized, non-atomic loan-backed inventory replacement.

The [citation inventory](citation-inventory.json) contains **73 extracted bibliography entries**, all assigned for relevance triage. **32 distinct entries** have explicit reading owners, four each. These are local `R001` identifiers, not the paper's original bibliography numbers. Both Flashbots/mempool and Protect references are included; the original paper is canonical if extraction omitted anything.

An inventory row, search snippet, citation count or abstract is not a completed source review. Report actual access and reading separately. Resolve missing URLs by title/author from primary or author-hosted sources; do not invent URLs or bypass paywalls. Duplicate URLs, paper revisions and repeated citations do not count as independent evidence. If fewer than 32 sources can be meaningfully read within this pass, report the shortfall rather than silently claiming coverage or extending the pass indefinitely.

Follow backward references **and** newer citing/related work. Investigate actual deployed instrument changes during **2025-10-29 through 2026-10-29**, with earlier work as context. Publication date, data window, protocol age and instrument launch date are separate fields. A newer paper reusing 2023–24 data is not current-market evidence.

## Eight responsibilities

| Folder / owner | Discovery responsibility | Four priority local IDs |
| --- | --- | --- |
| `literature/` / Scout A | Citation archaeology; transferable inventory, bridge and credit mechanisms | R035, R039, R042, R047 |
| `empirical/` / Scout B | Executed-strategy studies, actors, evidence and economic loops | R037, R041, R017, R034 |
| `instruments/` / Simulator B | Recent instruments, borrowing, wrappers and cross-chain claims | R001, R038, R069, R063 |
| `settlement/` / Capacity | Settlement/redemption constraints and inventory reuse as opportunity sources | R008, R049, R059, R058 |
| `economics/` / Costs | Fees, credit, rebalancing and persistent basis mechanisms | R002, R009, R015, R060 |
| `onchain/` / Simulator A | Public evidence access and small actual mechanism spot-checks | R005, R006, R026, R031 |
| `durability/` / Red team | Independent persistence, access and risk-premium challenges | R032, R056, R014, R028 |
| `audit/` / Judge | Independent source/coverage/novelty audit, never return origination | R061, R025, R070, R036 |

Each owner may edit only `discovery/workstreams/<folder>/`. The coordinator owns this brief, inventory, coverage consolidation and opportunity map. Old strategy, model and verdict files are not new work targets.

## Required package per owner

- `sources.json`: assigned local ID, exact source URL/title, access/reading status, publication date, underlying data window, retrieval date, source type, relevance and linked mechanism IDs. Separate full reading, abstract-only, unavailable, metadata/context-only and triage.
- `findings.md`: source-backed mechanisms and limitations, recent deployment evidence, useful positive or negative findings, and the next cheapest falsification check. No forced quota of profitable ideas.
- `mechanisms.json`, where the role originates hypotheses: economic cause of the spread, who pays/earns it, why it might recur, exact asset/claim equivalence, candidate chain/protocol/contract evidence, financing and inventory lifecycle, access/capital assumptions, costs/risks and falsifiers. Unknown returns remain unknown.

The independent judge and red team challenge evidence without originating the strategy's return proof. Cite primary sources adjacent to material claims. Paraphrase; do not copy bulk copyrighted papers.

## What changes in the research method

Explore loan-backed inventory replacement, borrowing/collateral basis, chain-specific representations, yield-bearing claims and derivatives, redemption/settlement windows, and fee/rebalancing markets as **hypotheses**, not assumed profitable products. Do not confine discovery to Ethereum rollups; check relevant non-EVM developments without forcing unsupported ideas into the map.

Distinguish a deployed instrument from a proposal, and true economic arbitrage from compensation for issuer, bridge, liquidity, directional or default risk. A new instrument on a mature protocol is not automatically a newly launched protocol, nor automatically safe.

The $2–5k monthly target remains a stretch objective, not a reason to stop mechanism discovery. The $50k capital and charter constraints still matter for eventual feasibility. The three-chain limit applies to a proposed allocation, not the number of ecosystems that may be researched.

Do **not** start new generic simulators, replay engines, exhaustive whole-actor ledgers, package/runtime installs or unattended paper runs. First find a plausible economic mechanism and a cheap real-world signal. Detailed validation follows only if separately authorized after this pass.

## Bounds and safety

One package per worker, then pause. No automatic next research waves, routines, repeated review/fix loops or new peer assignments. Ask focused factual questions on the shared discovery thread; do not start another worker's project.

Use at most **20 public document fetches and 6 searches per worker** for this pass, including priority and newer sources. Report unavailable sources without endless retries. Only the `onchain` owner may make up to **12 new read-only public RPC calls total**; all others use public documents/explorers and existing records. No paid sources, credential requests, private employer data, private keys, signers, transaction submission or live funds. Do not install or start servers.

For the seven additional human-supplied candidates, each owner may use **up to six additional public document fetches and two searches**, solely for its assigned candidate. This resolves the internal quota blocker after several owners had already exhausted the original allowance. It does not authorize a second wave, 30/60-day backfills or extra RPC calls. One small 21-trade paper-only counterfactual is allowed only if actual inputs and historical executable hedge evidence are available; it is not a new replay engine or T2 qualification.

No front-running users, sandwiching, exploitation, oracle manipulation or attack reproduction. Attack-focused references may be marked context-only and excluded from strategy construction. If a vulnerability is noticed incidentally, stop that path and flag minimal safe details privately.

No recommendation without the original T2+T3 and independent review gates. A mechanism map, a paper example, one profitable trade or a code test is not that evidence. Never invent fees, fill shares, probabilities or a 99% drawdown certificate.

Publish a disjoint branch commit with `Assisted-by: Replit`, send its exact SHA/file manifest and report actual source coverage. No worker PR, main push, merge, purchase or deployment.
