# Empirical discovery: economic loops and the limits of trade evidence

As of **2026-10-29**. Four assigned priority works were read in their full available extracted text; all nine assigned bibliography entries were triaged. The other five entries are **metadata-only**, not completed paper reads. PDF tables/equations have extraction damage; figures were not visually audited. Source versions, dates, reading depth and extraction commitments are in [sources.json](sources.json).

**Result:** a real historical loan-backed inventory-replacement sequence is identifiable, but the paper's summarized gain conflicts with its linked sale transaction. The reported **0xEf6c / 21-trade day / GNO, ZGAP, DOS losses remain unidentified**. No historical matching-perp eligibility or hedge improvement is established. These are useful discovery findings, not T2/T3, repeatability or a return recommendation.

## What the four priority works actually establish

- **R037 — Non-Atomic Arbitrage in Decentralized Finance (2024).** Ethereum sample: 2022-09-15 through 2023-10-31. The authors observe the Ethereum leg, not identified CEX hedges, and explicitly allow both false positives and missed non-atomic trades. Private-transaction visibility, simple-swap, fee, first-in-pool and established-token filters shape detection. The model's off-chain price assumes sufficient outside liquidity; measured fees paid to builders are not full searcher profit. Builder/searcher integration and possible subsidies make a selected wallet's on-chain balance especially incomplete. Its related-work discussion connects inventory/hedge risk to earlier LVR and private-order-flow research, not a new current-market edge. [Author-hosted paper, §§3–7 and Appendix A](https://liobaheimba.ch/assets/pdf/Papers/Non-Atomic%20Arbitrage_in_Decentralized_Finance.pdf).

- **R041 — A Large Scale Study of the Ethereum Arbitrage Ecosystem (2023).** Sample: 2020-02-28 through 2022-07-10. Historical executed-transaction identification is separate from modeled opportunities and private-fork executions. ERC-20 flow cycles can confuse aggregated user trades with arbitrage; raw ETH, internal vault accounting and transfer-tax tokens complicate identification. In the authors' **over-one-ETH-revenue candidate subset**, only **106,139 of 20,622,390** candidates executed successfully on historical forks (**0.51%, author-reported**, not a live fill rate). They group persistent opportunities and exclude conflicting campaigns rather than summing repeated block observations. Reported weekly potential profit is a historical counterfactual with modeled fees, not capital-constrained entrant earnings. Attack/oracle sections are context only and excluded from mechanism construction. [Paper, §§3, 4.2–4.3 and appendices](https://www.usenix.org/system/files/usenixsecurity23-mclaughlin.pdf).

- **R017 — A Tale of Two Arbitrages (2023-06-21).** Q1 2023 analysis excludes the USDC depeg period. It separates a revenue leg from a hedging leg: liquidity, inventory risk and uncertain fills can matter more than atomicity. The CEX–DEX measurement uses attributed searchers and CEX midpoint valuation, not observed actual off-chain hedge fills. It supports investigating risk-bearing inventory mechanisms, not treating its revenue estimates as full actor profit. Its “risk-free” atomic/private-protection framing is conditional: it is not a universal guarantee of zero costs, reliable inclusion or no venue risk. [Full article and methodology](https://frontier.tech/a-tale-of-two-arbitrages).

- **R034 — MEV Capture Through Time-Advantaged Arbitrage (2024-10-14, v1).** This is theory and simulation, not empirical Timeboost actor PnL. Simulations use March 2024 Binance perpetual top-of-book price observations and a synthetic CPMM with **$100m active liquidity reset each minute** (author model input, not observed available strategy capital). Deep external liquidity, modelled price processes and the absence of noise-trader activity constrain transferability. Fee and mean-reversion assumptions change conclusions. The timing right has an auction price; gross modeled arbitrage cannot be assigned entirely to its purchaser. Timeboost and the LP value-sharing adaptation were proposals in this source, not deployed yield products. [Version-pinned paper, model, experiments and appendices](https://arxiv.org/html/2410.10797v1).

The backward-reference work here consists of reading the references/related-work sections and the overlapping assigned predecessor R037, including its citations in R034 and newer N-Hops. It does **not** turn every cited predecessor into a completed review. R019, R030 and R064 remain explicitly metadata/context-only.

## Newer work and actual recent deployment changes

**Timeboost: proposal versus observed deployment.** The 2026-10-09 v3 empirical study covers 2025-01-01 through 2026-04-13; it reports launch on 2025-04-17, outside this pass's recent-development window. Its observed February 2026 secondary-market changes are inside that window. Concentration and access economics matter, but its non-atomic “profit” estimate is not an execution ledger: Appendix 0.A restricts assets to WETH/WBTC/USDC/USDT single swaps, imposes other attribution filters and drops addresses below **100,000 detected trades**. It values with a **10-second Binance markout window selected for highest resulting profit**. That is a hindsight-sensitive estimate, not proof that a trader could choose and fill that hedge causally. Some secondary-market payments are off-chain; the study itself cannot directly establish those providers' post-integration profitability. [Version-pinned study, §§3–5 and Appendix 0.A](https://arxiv.org/html/2509.22143v3).

**Solana BAM Direct Bundle Ingest: live, but gated.** Official documentation dated 2026-10-13 says DBI had been live on mainnet for an early cohort during the preceding month. The same page explicitly requires requesting access and being whitelisted. Its September/October before-and-after inclusion and validator-reward metrics are provider reports, not an entrant's net arbitrage profit or unrestricted access. This is a relevant deployed non-EVM execution-path change, not a standalone cross-chain strategy. No access request, credential creation or transaction submission was made. [Official announcement, “Request Access” and “Early Results”](https://bam.dev/blog/introducing-bams-direct-bundle-ingest/).

**N-Hops: newer publication, older sample and restricted detection.** The 2026-01-07 v2 revision of a 2025 conference paper studies 2023-09-01 through 2024-08-31, including non-EVM ecosystems. Its matching imposes a five-minute window **between adjacent steps**, two-percent value continuity and excludes multi-asset/aggregator paths. It reports ten detected multihop cases, not the total universe of viable multihop actors. The endpoint USD difference is explicitly **gross**, and future work includes incorporating bridge latency/fee structures. Those reported “profits” are not a fee/funding-complete realized ledger. The small detected sample and mixed signed endpoint differences are not proof that other strategies cannot work today. [Methods, results and limitations](https://arxiv.org/html/2511.17527v2).

## Added candidate: exact identification precedes hedge replay

The [candidate input manifest](candidate-input-manifest.json) is the frozen factual handoff. Searching complete seed v1/v2 extracted text and hyperlinks did not resolve **0xEf6c**, the claimed UTC day, the 21 executed transactions, or the GNO/ZGAP/DOS token contracts. Figures were not OCRed. Negative search is not evidence that the events do not exist; abbreviations and tickers are not unique identities. [Seed v2](https://arxiv.org/html/2501.17335v2) and [v1](https://arxiv.org/html/2501.17335v1).

The supplied 2026 interoperability lead's data section describes **chain-day and bridge–corridor-day panels**, with underlying sample **2022-01-01 through 2025-10-31**. It is not a recovered 21-trade actor ledger. No relevant exact actor or token identity was recovered from its searchable text. [The Price of Interoperability, §4.1](https://arxiv.org/html/2604.03083v1#S4.SS1). The separate [SSRN lead](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7161018) failed one fetch with HTTP 500; its title, authors and contents remain unknown.

Without the original day and exact underlying, it is impossible to establish whether a genuinely matching perp existed **at the original trade time**, much less its executable size, fees, funding events and margin terms. No present-day listing, generic fee, perfect hedge or winner-unchanged assumption was substituted. No hedge replay or counterfactual PnL was generated.

## Separate loan-backed case: public witnesses, not full actor PnL

Appendix G identifies **0xca74f404e0c7bfa35b13b511097df966d5a65597**, Ethereum and Arbitrum, **2024-07-23 UTC**. Six public explorer pages were checked; the sale extract is incomplete after the overview/internal-transfer material. The sequence is:

| UTC | Chain | Observed selected flow | Witness |
| --- | --- | --- | --- |
| 08:52:23 | Ethereum | Spent 50 WETH; received 2.62922794 WBTC | [Buy](https://etherscan.io/tx/0xf9dac896022ab70b8831e4a0139b97738180bf1605f216400f66bb0957f9208a) |
| 08:52:35 | Ethereum | Sent 2.62922794 WBTC into bridge gateway | [Bridge](https://etherscan.io/tx/0x452a9c05cc02fe146ce13a788456f02bf68c83ee3d6a57c0402ccfd8c5108903) |
| 08:52:43 | Arbitrum | Borrowed 2.6292 WBTC; debt token minted | [Borrow](https://arbiscan.io/tx/0xf7e5f28d391c2dee5f982fd27f8caf6fc250acd54ebe3d06ace25ac2a85feeff) |
| 08:52:50 | Arbitrum | Sold 2.6292 WBTC; internal transfer to actor of 50.054589166191564555 ETH | [Sale](https://arbiscan.io/tx/0xdd45995d12a9404a667c13ec0ab014b927abeea3cf9cd650a5e8e63845c7972f) |
| 08:59:23 | Arbitrum | Gateway minted 2.62922794 WBTC to actor | [Arrival](https://arbiscan.io/tx/0x7015f3ceff63cc5e4c2e7abffe3ed6c1d21da6b3305724ed1c9177e50cf411bf) |
| 08:59:48 | Arbitrum | Actor transferred 2.62920022 WBTC to Aave reserve token | [Repay](https://arbiscan.io/tx/0x798b5371e00f8a0d5dd7471aa36488e490f853004e638b547f272013b19db935) |

**Material discrepancy:** [Appendix G](https://arxiv.org/html/2501.17335v2#A7) says “earning 0.5 ETH.” The linked sale overview instead shows **50.054589166191564555 ETH received**. Subtracting the **50 WETH** input gives **0.054589166191564555 nominal ETH before fees/unobserved positions**, not 0.5 ETH. This is selected-leg arithmetic under nominal WETH/ETH equivalence, not certified net profit. The discrepancy remains open pending independent receipt/accounting verification; it must not be silently adopted or replaced with a fabricated actor result.

Additional exact arithmetic from these selected witnesses: bridge-to-arrival **408 seconds**, borrow-to-repay **425 seconds**, and first-buy-to-repay **445 seconds**. The WBTC repayment exceeds borrowed principal by **0.00000022 WBTC**; bridged amount minus repayment leaves **0.00002772 WBTC**. These differences are not proof of a complete debt close or booked profit. All input timestamps/amounts and native transaction fees are preserved in the manifest.

This is **not a flash loan**: borrowing and repayment occur in separate transactions with persistent debt. Collateral, health factor and liquidation buffer remain unknown. “Replacing destination token inventory” does not mean “requiring no destination capital.” The 50-WETH purchase plus unmeasured collateral is not a demonstrated $50k allocation, and linear scaling is unproven.

The bridge transaction also sends native ETH as retry prefunding; the arrival sender is the aliased gateway, not the actor. Economic fee/refund attribution must be reconciled before adding settlement gas, rather than double-counting prefunding and execution fees. Current explorer USD displays and branding were not treated as historical prices or historical venue identities.

## Mechanisms and cheapest next falsifiers

The [mechanism map](mechanisms.json) distinguishes **EMP-01**, collateralized inventory replacement with a selected historical witness; **EMP-02**, an unidentified historical hedge hypothesis; and **EMP-03**, paid/gated execution access as a constraint, not a return strategy.

- **Loan loop:** independently reconcile the six receipts, the amount discrepancy, pre-borrow collateral and final debt/bridge fees before considering repeatability or scaled capital feasibility.
- **Reported loss-day hedge:** recover exact actor, day, all transactions and token identities first; then test original-time instrument existence and executable depth before computing any hedge result.
- **Recent execution paths:** establish actual entrant eligibility and all-in access charges before assuming a venue's improved inclusion rate benefits the portfolio.

All candidates remain subject to the charter's capital, concentration, leverage, protocol eligibility, original T2/T3 and independent-review gates. No qualifying new return evidence was produced.

## Pass boundary

Used **22 document fetch attempts and 8 searches**, including one failed SSRN attempt and candidate-only additional allowance; **zero RPCs**. Four candidate-only document slots were left unused rather than extending generic research. No new simulator, replay engine, runtime/package, server, paid data, signer, transaction or unattended observation was started. This package ends the bounded pass; it does not authorize another wave.
