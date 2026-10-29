# Independent discovery and claim audit

**Cutoff:** 2026-10-29. **Common research base:** `135d5388654ad6699868ecccd8821bd7bb01850b`.
**Scope:** one discovery pass; independent criticism, not strategy origination or a return forecast.

## Decision

Candidate 7 is a conditional redemption/basis hypothesis, **not an inherently USD-neutral or near-riskless trade**. The primary documents demonstrate actual conversion and withdrawal constraints; they do not demonstrate an executable discount, realized profit, current queue duration, sufficient capacity, or a hedge available to this entrant. No candidate receives a T1/T2/T3 upgrade or investment approval from this package.

The four assigned priority references were read at full extracted-main-text scope. All nine assigned bibliography entries were triaged. The canonical bibliography contains 73 references and matches the 73-entry local inventory one-to-one. **All eight manifests reconcile to 73 assigned-reference triages and 32 scoped priority-topic full reads: 28 cited-work/current-page resolutions, one official legacy recovery and three current replacements. This does not establish 32 exact original-source reads.** Other owners' reading is supported by inspected immutable manifests and reports, not primary sources independently re-read by this auditor.

## Candidate 7: LST/LRT discount versus real redemption

### What is the asset and what is the claim?

The [Lido integration guide](https://docs.lido.fi/guides/lido-tokens-integration-guide/) distinguishes rebasing stETH from non-rebasing wstETH. A fixed quantity of wstETH represents a changing quantity of stETH. Its documented native conversion is available through `stEthPerToken()` or `getStETHByWstETH(10 ** decimals)`, not an assumption that one wstETH is one ETH. The guide documents canonical wstETH on Ethereum and bridged representations on other networks. These are documented identities, **not runtime/bytecode verification by this auditor**.

The same guide expressly states that **on most networks bridged wstETH cannot be unwrapped locally**. Some OP Stack networks also have stETH with a specific token/rate architecture. Consequently, the entry token's exact chain, address, decimals, bridge endpoint, escrow, upgrade permissions and supported exit matter. Buying a ticker on a remote chain does not itself acquire an immediately exercisable Ethereum withdrawal.

The [cross-chain adoption guide](https://docs.lido.fi/token-guides/cross-chain-tokens-guide) is prominently marked **outdated due to the Chainlink partnership**, describing a pre-CCIP setup to be revised. It remains useful for identifying failure domains, not certifying today's route. Its bridge recommendations include dedicated endpoints, custody/lock-and-mint, governance, pausing, implementation/audit matching and rate propagation. This package neither verifies deployment of the replacement route nor dates the partnership from an undated mutable warning.

### A wrapper conversion is not the withdrawal payment

The [withdrawal contract documentation](https://docs.lido.fi/contracts/withdrawal-queue-erc721/) describes a FIFO request, finalization and claim process. A request locks stETH or unwraps native wstETH into stETH and creates a transferable unstETH NFT. Finalization depends on available ETH, elapsed time and the oracle-determined share rate. Claiming requires a finalized, unclaimed request and its owner's authorization. The guide says requests cannot be canceled; transferring a claim is not redemption and has no guaranteed secondary-market liquidity.

Two details invalidate a riskless par anchor:

- The queued amount does **not** earn queue-period rewards for the withdrawing holder.
- A sufficiently adverse protocol loss can reduce the finalization rate below the normal stETH/ETH relationship. The holder remains risk-exposed while waiting.

The contract documentation also distinguishes pausing new requests/finalization from claiming already finalized requests: claiming remains available during those documented pauses. It would be inaccurate to say every pause necessarily blocks every existing claim.

No current queue state, claim size, live conversion value, executable price or request-to-cash time was observed here. The documented risk is not an estimated probability of loss.

### Do not use an old weETH label to certify current restaking exposure

The current [ether.fi staking description](https://etherfi.gitbook.io/etherfi/resources/ether.fi-whitepaper/ether.fi-staking), [product page](https://etherfi.gitbook.io/etherfi/products/staking/eeth) and [restaking description](https://etherfi.gitbook.io/etherfi/resources/ether.fi-whitepaper/ether.fi-re-staking.md) distinguish:

- eETH, a rebasing Ethereum staking receipt;
- weETH, its non-rebasing wrapper;
- separate optional restaking products such as weETHs, with additional product-specific dependencies, liquidity conditions and potential slashing exposure.

These current pages say eETH/weETH do not bundle additional restaking rewards or EigenLayer AVS slashing exposure. In contrast, the official [Cash help article dated 2026-04-13](https://help.ether.fi/en/articles/595737-weeth) calls weETH a liquid restaking token. That is a real source/date conflict, not permission to merge the claims into a uniform LRT category.

The current product page reports that **as of August 2026**, less than 1% of protocol assets remained in the legacy EigenLayer position, with remaining removal planned by the end of Q3 and withdrawal-credential removal by Q4. These are a dated reported state and plans. **Completion by the 2026-10-29 cutoff was not independently verified.** No exact optional-LRT deployment, AVS allocation or redemption waterfall was established by this reading.

The current product pages describe the weETH/eETH conversion relationship, but this package did not verify its live numeric rate or a deployed implementation's exact getter semantics. A search-generated answer mentioning a getter is deliberately not promoted to contract evidence.

### “Instant” and queued exits have different conditions

The official [ether.fi contract interaction guide](https://etherfi.gitbook.io/etherfi/developers/contracts-and-integrations/how-to) documents a standard queued withdrawal with no stated withdrawal fee/rate limit, then a distinct instant redemption path. “No fee” there is **not** zero total cost: network transactions, bridge travel, price impact, hedge costs and capital time still exist.

Instant redemption has per-token exit fees, rate limits, a liquidity buffer and a low watermark. The documentation says fee/watermark parameters are hard-capped at 5% in code, but that ceiling is **not the current fee**, a 5% loss forecast, an observed redeemable quantity, or confirmation of the deployed code. The live parameter and eligibility checks were not performed.

The same guide permits an ETH or stETH output selection. A stETH output is another staking claim, not ETH cash; the remaining conversion/withdrawal cannot be omitted. The older Cash help article also says in-app withdrawal is unsupported and directs users to an Ethereum interface.

### ETH-relative spread versus USD result

Closing a discount to an ETH-denominated claim does not remove ETH/USD exposure. A long unhedged receipt can gain ETH-relative value while losing USD. A short ETH hedge would be a separate position requiring actual access, matched notional and timestamps, contract/multiplier/settlement definition, funding, fees, margin, liquidation and counterparty treatment.

The effective ETH exposure can change with the wrapper rate, rewards, adverse finalization, bridge delay or exit choice. A hedge must be reconciled through the entire holding/queue interval and closed when the relevant exposure is actually extinguished. It does not insure slashing, a bridge/issuer default, an unclaimable receipt or a liquidity stop. Hedging also changes winners' costs and cannot be assumed to improve losing cases without changing profitable cases.

A future comparison would need both the ETH-relative redemption result and the USD economic result under the same benchmark, capital, holding period and hedge policy. This audit generates neither result.

### Cheap falsifiers and currently missing inputs

Before treating this as a concrete trade, the proponent would need to provide:

1. One exact chain/address pair and a documented, current conversion/bridge/withdrawal path; reject a presumed local unwrap where the token cannot provide it.
2. A state-pinned share conversion and executable acquisition/exit quotes at the proposed size; reject ticker parity, oracle NAV or stale valuation as a fill.
3. Entry-eligible redemption terms, current caps/buffer/queue conditions, failure paths, slashing/default loss allocation and actual output asset; reject a collateral or claim NFT as received cash.
4. A specified benchmark and actual hedge access/costs across the uncertain exit interval; reject “naturally USD-neutral.”
5. Complete gross-to-net accounting including failed attempts, approvals, both bridge legs where required, opportunity cost, queue reward treatment, slippage, hedge funding/margin and emergency exits.

These are falsification criteria, **not authorization for another collection wave**. Current executable net spread, deployment-specific security qualification, capital capacity, annual tail probability and full-portfolio monthly drawdown remain unknown.

## Independent critique of the seven user hypotheses

These are the coordinator's canonical definitions, not claims that any variant was implemented. None can be described as academically undocumented or structurally durable on the present evidence.

| Candidate | Claim that must not be silently accepted | Required distinction / disconfirming evidence |
|---|---|---|
| 1. Buy A / short matched perp / bridge / sell B / close hedge | A generic fee/latency median or a hedge makes an arbitrary historical loser profitable while leaving winners unchanged | Match each leg's asset, timestamp, size, executable hedge, funding, margin and failure unwind. The reported 21 trades need exact actor/day/input provenance. The seed's collateralized bridge-pending loan is prior inventory substitution, not a simultaneous cross-chain flash loan. |
| 2. Tokenized equity claim versus perp basis | Same equity name means identical enforceable ownership, corporate actions and trading clock | Issuer rights, access restrictions, redemption/NAV timing, dividends/splits, venue index and weekend/market closure exposure can differ. A new wrapper/date is not proof of a new academic mechanism or sustainable basis. |
| 3. Discounted dollar variant / actual par rail | Every dollar ticker can be converted permissionlessly and immediately at par | Native issuer claims, escrow-backed bridge claims, wrapping rails and DEX conversions are different. Verify the particular connection, user eligibility, caps, pauses and costs. Circle's documented Noble support withdrawal is a concrete warning against immutable par/access assumptions. |
| 4. Public postdeployment price correction | A newly deployed OFT/ITS token proves novel, persistent accessible alpha | Separate lawful public secondary-market correction from front-running users. Identity, launch date, chain liquidity and actual public fills must be known. Publication or launch recency does not establish an unstudied mechanism; historical activity correlation is not causal proof. |
| 5. Ordinary lawful liquidation with hedged collateral | A public liquidation condition guarantees an entrant can win profitably | Eligibility, healthy/unhealthy state, available close size, competition, settlement, costs and hedge failure matter. No stale-oracle exploitation, update manipulation or harmful reproduction is authorized. A collateral hedge does not remove contract/auction/access risks. |
| 6. Inventory-aware intent filling | A rebate/rebalance benefit is free additional income | Compare the same initial/final inventory, opportunity cost, reserved capital and actual required rebalance. Attribute who pays a reward and who bears LP/settlement loss; avoid counting saved rebalance expense again as cash revenue. |
| 7. LST/LRT discount / real redemption | Receipt units are ETH units; an ETH claim is a USD peg; redemption is instant and unconditional | Apply the claim/conversion/queue/hedge distinctions above, including current product taxonomy, bridge custody and slashing/default waterfall. |

This table is an independent **claim-level audit** grounded in the cited material, seven definitions and all seven immutable upstream source/findings packages listed below. It is not independent replication of their primary-source retrievals or a complete profitability validation.

### Cross-package discoveries that change the tests

The instruments package documents Robinhood's **mainnet**, not merely testnet, but also documents issuer debt-security claims rather than share ownership, restricted primary access and a primary trading clock. Its xStocks review identifies a different issuer claim, corporate-action mechanics and redemption eligibility. Neither establishes an accessible exact matched equity/perp pair, index terms, funding or an exercisable closing right. Thus candidate2 is a potentially testable claim/clock basis, not proof of deliverable equity parity. The full prospectuses and current user eligibility remain unverified.

The economics package distinguishes native Arbitrum USDC from USDC.e and Circle's native burn/mint rail from the newer configured-token wrapping rail. It does **not** establish that the specific purchased USDC.e claim is connected to an accessible current par-conversion contract. Gateway's documented EURC/cirBTC expansion transfers the same asset; it is not an EURC-to-USDC or cirBTC-to-BTC converter. Candidate3 needs the exact claim connection and complete closing costs, not just correct token addresses.

For candidate4, literature identifies ordinary inventory/rebalancing prior art as early as 2021. The seed's OMNI/MEXC activity association is historical and not a causal experiment; an exact primary listing announcement was not recovered. Its USDT0/Stellar and EURC/Gateway-Solana notices are dated recent non-EVM research leads, not executable spreads. **LIT-D4-02, the economics rail-convergence hypothesis and ONCHAIN-GATEWAY overlap**. Two same-day Circle notices corroborate one expanded capability and must not be counted as separate independent alpha.

The durability review separates Compound III absorbing an unhealthy account into protocol reserves from a later conditional discounted collateral purchase. Absorber points are not a documented immediate cash bonus. Public eligibility, collateral hedging or private submission therefore does not establish candidate5's attainable margin; protocol rules, access, competition and full failure costs still bind.

The settlement review identifies a concrete negative for candidate6: current official Relay Vaults documentation says **no new deposits**, while existing-position exits remain available until 2026-12-31. Relay Settlement itself is not thereby shown closed. Its Hub credit is not yet wallet cash, and Across's documented app fee goes to the integrator beneficiary, not automatically the filler. Compare the same accessible fills and terminal inventories; do not add ordinary margin, a saved LP fee and an already embedded rebate as three distinct payments. Institutional credit documentation adds contract/entitlement/approval requirements, not free general entrant funding.

The onchain package demonstrates free **current** public metadata/book access, not original-time listing, hedge depth or execution for candidate1. Hourly/interpolated/forward-filled accounting marks are not contemporaneous size-aware bids and asks. Funding must follow actual discrete settlement events and signs, not a continuously prorated assumed short income. During the matched WBTC-inventory/WBTC-debt portion of the loan case, debt already supplies an opposing token delta: an additional short can overhedge. Current exact GNO/ZGAP/DOS names missing from one first-DEX universe do not prove historical absence, different ticker equivalence or absence on every HIP-3 venue.

These findings improve identification and falsifiability. None demonstrates academically new, structurally persistent or near-riskless income. Source recency, protocol launch, instrument launch, operator admission and real execution are separate observations. Reading across many ecosystems is not a proposed portfolio within the chain/concentration limits.

### Loan-example discrepancy is not a replacement profit result

The empirical package pins six selected public explorer witnesses for the seed's separate 2024-07-23 loan-backed case. Its input manifest records **50 WETH spent** and a sale-overview internal transfer of **50.054589166191564555 ETH** to the actor. The nominal selected-leg difference is **0.054589166191564555 ETH**, whereas Appendix G says “earning 0.5 ETH.” The settlement package repeats the latter explicitly as paper-reported, not validated. **The discrepancy remains unresolved; neither number is certified actor net profit.**

This auditor reviewed the frozen factual manifest, not independently re-fetched raw receipts or the explorer pages. The sale extraction is truncated after the relevant overview/transfer material. Starting collateral, post-state debt, other positions, full fees, bridge retry prefunding/refunds and economic payer attribution remain incomplete. A gateway-funded arrival must not be charged again without reconciling its funding. Nominal WETH/ETH equivalence is only an arithmetic convention here, not a claim that cross-chain cash is interchangeable risklessly.

The loan case is also **not the unidentified 0xEf6c 21-trade day**. That actor/day/transaction/contract manifest and original-time matching perp existence remain unknown. Do not substitute the loan witness or present-day instruments for those missing historical inputs, fabricate a hedge replay, average away the discrepancy, or declare the unlocated case nonexistent.

### Current onchain corroboration has a narrow meaning

The onchain package retains five successful public responses: Solana genesis, the issuer-designated EURC pre-mint account, the finalized context slot's block time, and Hyperliquid first-DEX metadata plus one BTC book. This auditor recomputed and matched **all five raw-response SHA-256 hashes**, parsed the authoritative raw strings and verified exact token units. Four local preparation failures happened before network requests; the owner conservatively charged nine method attempts against its cap of twelve. No new network request was made by this auditor.

The retained Solana response records **20,000,009.79 token units** at the Circle-designated pre-mint account, with six decimals and finalized context slot 462822009 at **2026-10-29 08:58:01 UTC**. This corroborates one provider's current account state, not minter permissions, backing, public availability or deployment-time state. Circle says those pre-mint units are not circulating before authorized release. **They are not entrant inventory, tradeable pool depth, revenue or free credit.** The account is not a user deposit destination.

The retained first-DEX metadata contains 235 entries and the BTC book has one current timestamp. These are capability snapshots, not historical hedge witnesses, an exhaustive HIP-3 search or hypothetical fills. Raw `response_text` remains authoritative: JavaScript-parsed uint64 fields can round, so the snapshot's parsed numeric copy is not a substitute for exact raw values. None of this creates a T1/T2/T3 result.

### What the literature does and does not establish

[R025, Drake's based-rollup proposal](https://ethresear.ch/t/based-rollups-superpowers-from-l1-sequencing/15016), was published 2023-03-10. It concerns L1 sequencing, liveness and incentives, and explicitly discusses MEV accruing to L1. It is not evidence of current entrant-accessible atomic cross-chain execution. “Based” is an architecture, not the chain name Base.

[R061, the Espresso Sequencer design](https://hackmd.io/@EspressoSystems/EspressoSequencer), explicitly warns that it describes an earlier product version. Its design discussion of shared ordering and interoperability does not certify a currently deployed atomic rollback interface. The mutable current [changelog](https://docs.espressosys.com/network/network/changelog) records proof-of-stake mainnet activation on **2026-03-04**, distinct from the April 2025 permissionless testnet and October 2024 Mainnet0. Current [network docs](https://docs.espressosys.com/network/network/networks) distinguish production Ethereum from Sepolia-backed Decaf. The [chain list](https://docs.espressosys.com/network/network/chains-reference) labels Celo **devnet, unstable**. Listed endpoints/addresses were not called or runtime-verified here.

[R036, Gupta/Pai/Resnick](https://drops.dagstuhl.de/storage/00lipics/lipics-vol282-aft2023/LIPIcs.AFT.2023.20/LIPIcs.AFT.2023.20.pdf), provides a theoretical and empirical account of private order flow's complementarity with top-of-block ability. Its empirical window is **2023-04-01 through 2023-05-01**, not 2026. This supports testing access/competition assumptions, not the assertion that every new participant necessarily loses. Attack examples remain context-only and are not strategy construction.

[R070, Yang/Nayak/Zhang v5](https://arxiv.org/html/2405.01329v5), is dated **2025-04-29**, but the overall builder observations run **2022-09-15 through 2024-10-31**. Full bids cover selected weeks, not a continuous April–December 2023 dataset. Its lower-bound new-entrant exercise includes winning equal bids and no incumbent response—assumptions that cannot be silently imported into this swarm's conservative race model. ETH-balance income estimates do not identify all owned addresses, refunds or off-chain transfers. Linked [code](https://github.com/hackingdecentralized/Decentralization-of-Ethereum-Builder-Market) and [original data](https://doi.org/10.7910/DVN/3X7X2U) were not downloaded or independently rerun.

Backward/forward tracing in this pass followed the explicit Drake-to-Espresso conceptual link and Gupta-to-Yang citation chain, rather than claiming to read every linked reference. The seed's [Appendix G](https://arxiv.org/html/2501.17335v2#A7) already describes buying/bridging inventory and temporarily borrowing against collateral while the bridge is pending. This is direct prior-art evidence against presenting inventory substitution as newly invented; it does **not** prove every specific variant has already been academically analyzed.

The bounded candidate-7 search additionally surfaced queue design, optimal liquid-staking exit and interconnected restaking-risk papers. They are **search-only leads, not full reads or accepted findings**; their URLs/status are preserved in `sources.json`. Neither their titles nor a short bounded search proves novelty or non-novelty of every implementation.

## Actual recent changes, not inferred profits

The official [Circle Noble notice, 2026-09-10](https://www.circle.com/blog/circle-is-discontinuing-support-for-usdc-and-cctp-v1-on-noble), supplies a real recent **non-EVM** change. New Circle Mint issuance to Noble was disabled on 2026-10-13; CCTP V1 burn-limit reductions begin on **2026-10-31**, after this cutoff. Later pauses and manual/snapshot/compliance-dependent redemption must not be represented as present unconditional permissionless cash rights. No Noble executable discount or transaction state was collected.

Espresso's documented March 2026 production change and ether.fi's reported August 2026 wind-down are other recent structural observations. New documentation, new infrastructure or revised rights can change costs and risk without creating a profitable spread. The old R057 Scroll whitepaper (2024-06-24) distinguishes confirmed, committed and finalized states; it does not establish current bridge timing. R072's old Bridges URL now renders an Ecosystem directory; this mutable document drift is explicitly recorded, not passed off as an archived 2025 route specification.

## Provenance, coverage and stop boundary

### Aggregate reading audit — complete manifest reconciliation, not 32 exact originals

| Workstream | Inspected immutable commit | Assigned triages | Priority-topic full reads | Resolution distinction |
|---|---|---:|---:|---|
| Audit | This package | 9 | 4 | Cited works/current cited main texts |
| Durability | [ac94821](https://github.com/vaikmr/swarm-search/tree/ac94821ae54ab1e979b2634ba242198c1f55372a/discovery/workstreams/durability) | 9 | 4 | Four cited works/current pages |
| Instruments | [d126e3e](https://github.com/vaikmr/swarm-search/tree/d126e3ea7e14a6c2839ef210a477f2565d2477c8/discovery/workstreams/instruments) | 9 | 4 | Three documentation root pages plus one rate-limit article, not full site corpuses |
| Economics | [f61f3d7](https://github.com/vaikmr/swarm-search/tree/f61f3d74631f60cd59cd7eabb6fe073b786f1bd0/discovery/workstreams/economics) | 9 | 4 | Three cited bodies plus R002 official same-path legacy recovery |
| Settlement | [0aee939](https://github.com/vaikmr/swarm-search/tree/0aee9391e6aad737348a455b6749ce9763637bd7/discovery/workstreams/settlement) | 9 | 4 | R008 exact current quickstart; R049/R058/R059 current replacements |
| Literature | [9066149](https://github.com/vaikmr/swarm-search/tree/90661493d0e78caeb3d9185a99a2f7d81847fa82/discovery/workstreams/literature) | 10 | 4 | Four distinct works; obsolete partial R035v1 and full v2 count once |
| Empirical | [58ad593](https://github.com/vaikmr/swarm-search/tree/58ad5931f96c905903a1b99787cd4e83d83bcd8c/discovery/workstreams/empirical) | 9 | 4 | Four cited works via available primary/author copies; figures not visually audited |
| Onchain | [410c52e](https://github.com/vaikmr/swarm-search/tree/410c52e39e502f4368b91c68971db5e251de8936/discovery/workstreams/onchain) | 9 | 4 | Allium homepage/Prices, Dune homepage and Mempool Dumpster README; not linked corpuses |
| **Inspected total** | **Eight workstreams** | **73/73** | **32/32 scoped topics** | **28 cited-work/current-page resolutions +1 official legacy recovery +3 substantive replacements** |

The 28 cited-work/current-page resolutions include primary author versions and present mutable pages. They are not a claim to exact original publisher bytes, historical archived bodies or 32 completed original-source reads. The legacy Across FAQ is official, but its old chain list and airdrop 2022 text cannot establish current economics. Scroll's replacement is narrower than the unrecovered original route; a replacement can still be relevant without being the cited historical document.

The other owners' counts are **audited manifest/report attestations**, not primary sources independently re-read by this auditor. All 32 priority IDs and all 73 assigned IDs were matched to their disjoint inventory assignments; immutable commits share the exact common parent and touch only owned workstream prefixes. Abstracts, snippets, metadata, continuation chunks, duplicate document bodies and revision aliases do not add priority reads. Root/homepage scope does not imply reading an entire documentation corpus. Nor are 32 distinct bibliography entries 32 independent academic studies, datasets or providers. See `coverage-audit.json` for per-package inspection scope.

- **26 public document fetch calls**, including continuation chunks and two direct seed fetches; **21 distinct fetched documents**.
- **8 search calls**. The six extra document fetches and two extra searches were solely for added candidate 7. No paid data, RPC, credentials, installations, servers, signing, transactions, unattended jobs or return simulations. Offline manifest checks used the existing local parser.
- **4/4 assigned priority full main-text reads**; **9/9 assigned entries triaged**. Across assigned entries: six full main-text/page reads, one partial contextual text read, one extractor/chrome-only attempt, one metadata-only safety/context triage.
- Across all fetched sources: **18 full extracted-main-text/page reads**, two partial attempts, and the seed's bibliography/Appendix-G-only inspection. PDF figures were not visually verified; code/data links were not treated as downloads or replications.
- Canonical IDs are `bib.bib2` through `bib.bib74`, not the local `R001`–`R073` identifiers. All 73 unique inventory rows map one-to-one; 64 exact URL matches, two trailing-slash-normalized matches, seven manually compared no-URL metadata matches. This is bibliography integrity, not reading coverage.
- An original unavailable/moved page and its replacement can both be useful, but remain different evidence. A homepage or current mutable directory is not a whole documentation corpus, archived paper, or verified deployment.
- `retrieval-log.json` records every document call and extraction hashes where retained. These identify returned text, not raw publisher bytes, authenticated deployment state or a recreated archive.

The original 12-strategy checkpoint remains closed and NOT_READY. This is the single authorized discovery audit. No automatic repair wave, additional collection or investment recommendation follows from this package.
