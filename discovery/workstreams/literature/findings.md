# Literature discovery and candidate 4: post-deployment price correction

As of **2026-10-29**. Research hypotheses only. No trading, RPC calls, new simulator, installation, actor backfill or forward-paper run was performed. This package completes one bounded pass and then pauses.

**Result:** four distinct priority works were read in full extracted text; all ten assigned references were triaged. Historical evidence supports inventory-first cross-chain trading as an already-known mechanism, not a new discovery or a near-riskless return. Two current-window non-EVM instrument changes provide concrete places to look next, but **no current executable discrepancy, entrant capture or complete-cycle profit was established**.

The recent search window is **2025-10-29 through 2026-10-29**. Publication, empirical observation, protocol launch and individual instrument deployment dates are separate below. The source ledger records access and reading separately, including unsuccessful and partial fetches.

## 1. What the four priority readings actually establish

| Reference | Actual reading and time scope | Useful transfer | What it does not establish |
| --- | --- | --- | --- |
| R035, *Cross-Rollup MEV* | Full v2, 17 Oct 2024; data 31 Dec 2023–30 Apr 2024 | Price gaps must be sized against reserves and costs; repeated blocks in one episode are not independent opportunities | Actual complete-cycle execution, current 2026 spreads, attainable capture or free cross-chain flash liquidity |
| R039, *An Empirical Study of Cross-chain Arbitrage in DEXs* | Full eprint copy; 2023 reference/2024 conference metadata; data 12 Dec 2022–13 Jan 2023 | Token-path and shared-pool accounting matter; inventory/route availability can bind | Authors explicitly do not identify trades users actually performed; representation equivalence and the complete rebalance ledger remain assumptions |
| R042, *SoK: Cross-Domain MEV* | Full 9 Aug 2023 paper and appendices; taxonomy, not a return window | Separate actual implementations from ideal functionality, ordering access from ordinary trading, and time optionality from intrinsic value | A 2023 proposal is not a deployed 2026 instrument; shared ordering is not atomic bridging or permissionless credit |
| R047, *Unity is Strength* | Full 3 Dec 2021 paper and appendices; formal/illustrative | Section 3.1 already describes assets on both domains and later inventory management; conversion between claims must be explicit | Theoretical extractor maxima and simplified AMM examples are not ordinary-entrant net returns |

Primary texts: [R035](https://arxiv.org/pdf/2406.02172), [R039](https://eprint.iacr.org/2023/1898.pdf), [R042](https://arxiv.org/pdf/2308.04159v1), [R047](https://arxiv.org/pdf/2112.01472v1).

R035's initially fetched v1 is titled *Layer-2 Arbitrage: An Empirical Analysis of Swap Dynamics and Price Disparities on Rollups*. The later text identifies itself as **arXiv:2406.02172v2, 17 Oct 2024** and matches the inventory title. These are one work, not two independent supporting studies. Its episode-peak de-duplication avoids one overcount but still chooses an ex-post maximum; that maximum is not a causal online decision rule.

The backward pass reviewed relevant parts of the [March 2020 Uniswap v2 whitepaper](https://app.uniswap.org/whitepaper.pdf), including arbitrary pairs and local atomic flash swaps. The latter must be repaid within the same transaction; it cannot fund an asynchronous cross-chain bridge by assumption. Attack examples were not operationalized.

The newer related full read, [*Atomic Execution is Not Enough*, v3, 2 Mar 2025](https://arxiv.org/html/2410.11552v3), explicitly distinguishes **atomic execution** from the much harder **atomic bridging**. Its model values residual inventory against an external price, assumes independent swap failures, and omits transaction costs. It is a useful challenge to an automatic “atomicity raises profit” claim—not empirical evidence that failed trades are desirable, that partial fills are riskless, or that a current flash-loan route exists.

PDF extraction damaged some equations/tables. Figures were not digitized and numerical formulas were not visually re-derived. “Full read” means the complete extracted text was reviewed, not that every extracted symbol was independently verified.

## 2. Full assigned-reference triage

| ID | Status | Relevance decision |
| --- | --- | --- |
| R003 | Full text fetched; selected sections read | Backward mechanism/cost reference; local repayment scope matters |
| R018 | Inventory metadata only, not fetched | CoinGecko venue directory; no ranking, deployment, depth or return claim adopted |
| R029 | Primary USENIX URL resolved in search; not fetched/read | Attack-focused context, excluded from strategy construction |
| R035 | Full extracted-text read | Historical opportunity/cost accounting and de-duplication |
| R039 | Full extracted-text read | Hypothetical cycles, representation and inventory constraints |
| R042 | Full extracted-text read | Protocol classes, access and proposal/deployment distinctions |
| R047 | Full extracted-text read | Prior art for inventory and cross-domain valuation |
| R048 | Full extracted homepage read | Project-linked OmniCat identities; undated metrics are not depth evidence |
| R062 | Full thread fetched; original byline, TLDR/introduction/overview read | FOCIL inclusion-list proposal, not a price-correction revenue source; current activation not checked |
| R073 | Inventory metadata only, not fetched | General ZKsync portal; no specific atomic bridge/deployment inference |

This is **10/10 relevance triage, not 10 full reads**. Only R035/R039/R042/R047 contribute four distinct completed priority readings to the swarm's 32-reference target. Exact URLs, reading status and source dates are in [sources.json](sources.json).

## 3. Pressure-test of the seed's OMNI example

### Historical observation versus causal explanation

The seed's [section 4.4.1](https://arxiv.org/html/2501.17335v2#S4.SS4.SSS1) reports OmniCat launching on **22 Dec 2023**, and its measured cross-chain activity falling following a **28 Dec 2023 MEXC listing**. These remain **paper-reported dates/associations**. Two bounded listing-focused searches did not locate the exact historical official listing announcement. Failure to locate it does not mean it never existed; current pages or a different OMNI ticker do not resolve the historical event.

The seed does not supply a counterfactual establishing that the listing caused the decline. Token volatility, DEX depth, transfer availability, competition, changing demand, actor inventory exhaustion and a change in where arbitrage is observed are alternative explanations. A CEX might improve price discovery and reduce a discrepancy, shift activity outside the paper's chain-pair detector, or introduce access constraints. These possibilities are untested—not causal findings.

Its second deployment-related example, tBTC/Aerodrome on Base in mid-May 2024, is also historical context, not a second fresh 2026 opportunity. A newer publication/indexing date does not refresh the seed's **Sep 2023–Aug 2024** empirical window. [Seed paper, v2, 18 Jun 2025](https://arxiv.org/html/2501.17335v2).

### Identity and representation checks

The [project homepage](https://omnicat.wtf/) currently links:

- Ethereum/Arbitrum/BNB/Canto/Polygon/Blast: `0x9e20461bc2c4c980f62f1B279D71734207a6A356`.
- Base: `0xC48E605c7b722a57277e087a6170B9E227e5AC0A`.
- Solana: `7mmXL6Et4SbpDs2iXoZQ3oPEeXeAiyETxh1QjDNi5qnV`.

These are **project-linked identities**, not a verification of every chain's token program, permissions or historic configuration. OmniCat OMNI is not Omni Network OMNI. The site's eight-chain marketing statement, incomplete charts and undated aggregate liquidity statistic cannot establish charter TVL, route depth or a current entry.

The [Base explorer](https://basescan.org/address/0xC48E605c7b722a57277e087a6170B9E227e5AC0A#code) corroborates the project-linked address, labels it OmniCat, and reports exact-match verified source named **OFTV2**, compiler **0.8.19**. The fetched response was truncated: only identity/source headers were reviewed, not a complete code audit. “OFTV2” in a contract name is not proof of the later LayerZero messaging protocol v2. No claim of zero transfer tax, unrestricted exits, current peers or historical 2023 configuration follows.

### What the example earns—and what is still missing

[Appendix B.1](https://arxiv.org/html/2501.17335v2#A2.SS1) describes buying about **1,034,616.49 OMNI for 0.9 WETH on Base**, selling inventory already held on Arbitrum for approximately **1 WETH**, with **27 seconds** between the swaps. The paper reports approximately **$198.95 after its included transaction fees**. These are source-reported trade amounts, not independently fetched/reconciled receipts in this pass. LayerZero inventory rebalancing is a later operation.

That is a concrete historical **inventory-first ordinary price-correction loop**, not launch sniping and not a closed capital-free cycle. The eventual rebalance, reverse cash inventory, residual balances, bridge/transfer fees, taxes, borrowing if any, failed attempts, infrastructure and capital opportunity cost belong in net returns. No such complete current operator ledger was produced.

For contrast, Appendix B.2's VOW bridge-first example has transfer delay and representation/eligibility uncertainty; its large reported amount is not adopted as repeatable or safe. It was not investigated as an incident or reproduced.

The [Appendix G](https://arxiv.org/html/2501.17335v2#A7) loan-backed example buys WBTC with **50 WETH** on Ethereum, starts a bridge, borrows replacement WBTC on Aave/Arbitrum before the bridge arrives, sells, then repays when bridged collateral inventory arrives. The selected transaction sequence does not establish the full prior collateral funding. This is **collateralized, asynchronous inventory replacement**, not a free cross-chain flash loan: source working capital, destination collateral, interest, health factor, bridge delays and repayment all matter. It is a financing comparator here, not a third new strategy proposal.

## 4. Recent instrument changes, including non-EVM

### A. USDT0 on Stellar: 2 September 2026

The [Stellar Development Foundation release](https://stellar.org/press/usdt0-goes-live-on-stellar-connecting-unified-dollar-liquidity-to-the-world-s-most-accessible-network), dated **2 Sep 2026**, announces USDT0 live on Stellar. This is a current-window, non-EVM destination deployment—not merely an old EVM token with a new article date. The release says USDT0 initially launched in January 2025; the network age and the much younger Stellar deployment are distinct.

The [USDT0 technical documentation](https://docs.usdt0.to/) describes underlying assets locked in Ethereum adapters and destination tokens minted/burned, with return to the underlying through burn/unlock. Its IOTA section is a useful counterexample to assuming all OFTs have every direct route: **Move-based IOTA L1 uses a dedicated Ethereum lockbox and cannot directly transfer USDT0 to all other USDT0 chains**. That current documentation has no verified deployment date for IOTA here, so IOTA is route context, not a second dated launch.

The release's “no wrappers/fragmentation” description does not eliminate backing, issuer, adapter, messaging, chain or redemption dependencies. Its disclaimer expressly does not guarantee the asset or independently verify aggregate figures. **Stellar issuer/contract ID, active pool IDs, sellability, transfer settings, quotes and all-in exit costs remain unverified.** A partner list or aggregate transferred volume is not entrant profit. Native legacy USDT, USDT0 and any similarly named Stellar asset must not be merged by ticker.

### B. EURC through Circle Gateway on Solana: 23 October 2026

[Circle's 23 Oct 2026 announcement](https://www.circle.com/blog/circle-gateway-now-supports-cirbtc-and-eurc) adds EURC and cirBTC to Gateway; a [same-day Solana pre-mint notice](https://www.circle.com/blog/circle-gateway-new-pre-mint-address-for-eurc-on-solana) documents EURC operational support. These two notices corroborate **one expanded capability**, not two independent profitable deployment events.

Current [asset-specific documentation](https://developers.circle.com/gateway/concepts/non-usdc-assets) and the [supported-chain table](https://developers.circle.com/gateway/references/supported-blockchains) narrow the claim:

- Each asset has its own balance; transfer burns/mints **the same asset**. Gateway never converts EURC to USDC or cirBTC to native BTC. cirBTC itself is a BTC-backed token.
- EURC supports Arc/Ethereum/Avalanche/Base/Solana/World Chain through Gateway; cirBTC supports Arc/Ethereum, **not Solana**. EURC issuance on Stellar/Cronos does not imply Gateway there. Solana is not supported by the nanopayments SDK.
- EURC uses **6 decimals**, cirBTC **8**. Fees are in the transferred asset's units; the transfer-specific estimate, not a generic blog fee, is authoritative.
- “Under 500ms” access is **after deposit finalization**. Current ordinary Ethereum/Base deposit documentation gives approximately **13–19 minutes** to attestation. These are provider descriptions, not measured timings in this pass.
- The blog's advertised outside-Arc **1bp EURC/cirBTC fee** is only a component, not an executed all-in quote or free transfer. Gas, swaps, slippage, retries, return inventory and eligibility still matter. Arc's advertised launch waiver is not assumed permanent.
- Permissionless withdrawal has a **seven-day delay** in the announcement; asset-specific documentation confirms delayed withdrawal applies. A transfer route can exist while an emergency exit is slow.
- The pre-mint staging address is **not a token mint, trading pool or user deposit address**. Pre-minted balances are not available liquidity. Do not send funds to it or directly transfer ERC-20s to the Gateway Wallet.

The new-asset blog body and generic USDC-only footer are in tension. Current asset-specific docs confirm expanded technical support, but operator eligibility and applicable legal terms still require verification; neither boilerplate nor marketing is silently treated as definitive.

These documents establish an issuer-described route change. They do **not** establish a price discrepancy, pool eligibility, operator redemption access or a repeatable return. Faster inventory mobility could reduce arbitrage spreads rather than create them.

## 5. Native/OFT/ITS is an identity question before a price question

| Representation | Necessary matching evidence | Important non-equivalences |
| --- | --- | --- |
| Issuer-native asset | Exact per-chain mint/contract, issuer claim and permissions; same asset on supported source/destination | Native does not remove freeze, issuer, reserve, FX, eligibility or withdrawal-delay risk |
| OFT/direct or adapter | Correct peers, underlying lock/mint/burn model, local/shared units, actual debit/credit behavior and live route | Unified supply is not immediate cash redemption, unrestricted transfer, identical protocol version or zero taxes/fees |
| ITS/custom token | Same `interchainTokenId`, per-chain token/manager identities, scaling metadata, manager type and appropriate mint/burn or lock/unlock authority | Matching ticker or even address is insufficient; independently linked tokens do not prove common economic redemption |

Primary references: [LayerZero OFT technical reference](https://docs.layerzero.network/v2/concepts/technical-reference/oft-reference), [USDT0 architecture](https://docs.usdt0.to/), [Axelar custom-token integration](https://docs.axelar.dev/dev/send-tokens/interchain-tokens/integrate-custom-token/), [Circle asset-specific rules](https://developers.circle.com/gateway/concepts/non-usdc-assets).

The OFT reference expressly permits custom fee/rate/access behavior and notes fee-on-transfer/rebasing assets are not supported by the vanilla accounting. Its generic decimal examples are not evidence of an actual token's decimals. ITS documentation ties identity to linked managers and metadata, not the symbol. No particular ITS deployed token pair was independently verified here.

## 6. Two falsifiable adaptations, not two winners

Full lifecycle, dependencies, unknowns and cheap falsifiers are in [mechanisms.json](mechanisms.json).

**LIT-D4-01 — Established-claim destination onboarding.** Use a new, publicly finalized destination deployment to define the research event; only investigate ordinary spot price correction **after** token identity, permissions and pools are public and working. Prefunded inventory permits ordinary independent buys/sells, with later complete inventory and cash restoration. USDT0/Stellar is a dated lead; OMNI is the historical comparator, not the proposed 2026 trade.

Cheapest falsifier, **if a later phase is authorized**: establish the exact Stellar issuer/contract and one eligible pool plus a lawful working return path. Then obtain synchronized, size-specific two-way quotes and complete costs for a small prespecified size. Reject that route if it is untradeable, identity is wrong, or executable proceeds cannot cover actual cycle costs. No current quotes were collected; no profitability or contestable capture is assumed.

**LIT-D4-02 — Existing-asset route expansion and inventory restoration.** Instead of speculating on a newly issued token, ask whether a newly available canonical rail makes an existing cross-chain inventory imbalance cheaper to restore after ordinary spot correction. EURC Gateway/Solana is a dated technical lead. Its same-asset units, source finality, fees, capital lock and withdrawal delay must be respected; this overlaps the economics worker's rail-convergence topic and must not be counted as an independent alpha strategy in synthesis.

Cheapest falsifier, **if separately authorized**: identify correct EURC mints/pools and the actual same-asset route estimate at a stated size, then compare the full closing inventory ledger against the old route and passive inventory. A smaller transfer component is not enough if total costs or exit delay dominate. It is also falsified as an income claim if the new rail simply closes discrepancies before an ordinary entrant can act.

Neither adaptation is academically novel: inventory/rebalancing is explicit in 2021 literature, and the seed already studies new deployment episodes. The potentially new research inputs are the **specific recent deployments and route constraints**, not the basic arbitrage mechanism. A proposed causal CEX event study remains blocked on the exact historical event and a prespecified comparison; the paper's correlation alone is not such a study.

## 7. Capital, concentration and recommendation gates remain open

The [$50k charter](../../../docs/CHARTER.md) applies to a proposed portfolio, not the number of ecosystems read. A chosen implementation must use at most three chains plus one major CEX account; this package does not propose an allocation.

Prefunding ties capital up on both sides. Lending collateral is additional committed capital, not free buying power. Stablecoin, bridge, issuer, adapter, chain and protocol dependencies overlap. In particular, USDT/USDT0 balances can share the same issuer/backing and Ethereum lockbox failure point even across distinct destination chains. A bridge route is not diversified simply because two token symbols or chains differ. Keeping an unexplained reserve does not make that reserve risk-free.

Protocol age of at least 12 months, $50m TVL and a public audit are not established by token market capitalization, homepage liquidity, an old underlying token, a recent press release or explorer source verification. New instruments on mature protocols still need instrument-specific risk assessment. Explicit higher-risk labeling is not permission to waive other charter limits.

There is no measured entrant advantage over incumbents, no complete cash-net or benchmark-excess return, no observed fill share, no p5/p50/p95 distribution and no substantiated monthly 99% drawdown or annual tail-probability gate. Unknown costs remain unknown rather than zero. The $2–5k monthly target is neither validated nor used to terminate discovery.

**No evidence-tier upgrade or deployment recommendation:** no qualifying T2 replay, elapsed T3 paper period or independent approval of these hypotheses was produced. Independent reading/source corroboration is not strategy validation.

## 8. Reproducibility and stopping point

Actual work used **26 document-fetch calls** (20 base plus the six candidate-specific additions), **eight search calls** (six base plus two additions), and **zero RPC calls**. There were 22 distinct attempted document URLs, including one 404 and navigation-only pages; continuation chunks and the obsolete R035 revision are not independent studies. Search snippets were not treated as issuer terms, quotes or completed reading.

The 404 ITS overview was recovered by following the official documentation home/developer links to the custom-token page, within the same bound. The exact MEXC historical listing record and current pool/contract execution checks remain unresolved rather than endlessly retried.

Authored outputs are limited to this folder: source/access ledger, findings and two hypothesis records. Offline validation is structural/provenance checking, not economic simulation. **Publish one disjoint commit, report the manifest and actual counts, then pause. No automatically scheduled follow-up or second wave.**
