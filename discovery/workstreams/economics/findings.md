# Fees, credit, rebalancing and stablecoin-variant discovery

**Cutoff: 2026-10-29.** One bounded public-source pass. The most useful result is a distinction between mechanisms with identifiable economic payers and apparent spreads caused by different claims or incomplete settlement. No current executable spread, filled cycle, repeatable net return or risk-qualified allocation was established.

All nine assigned citations were triaged; the four priority sources were substantively read. Three priority cited URLs worked. Across's cited FAQ was missing, but its substantive same-path FAQ was recovered on the official **legacy** host; that is a recovered legacy reading, not a successful reading of the original URL. The five nonpriority citations received metadata/context triage only. Exact statuses, publication/data dates and source links are in [sources.json](sources.json).

The initial pass used 20 document fetches and five search calls. The separately authorized stablecoin-candidate extension used six additional document fetches and two searches, solely for that candidate: **26 fetches, 23 distinct requested URLs, seven searches, zero RPC calls and zero independently read explorer pages**. Repeated paper chunks are not separate sources. No installs, collectors, simulators, servers, signatures or transactions were used.

## Added candidate: stablecoin variants do not automatically converge through CCTP

The smaller supported research subset is Ethereum/Arbitrum USDC; USDT/USDT0 and USDG were not independently researched. Current primary docs establish the following identities, not interchangeable ticker labels:

| Exact asset | Chain | Contract | Documented claim |
| --- | --- | --- | --- |
| Native USDC | Ethereum | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` | Circle-native USDC |
| Native USDC | Arbitrum One | `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` | Circle-native USDC |
| USDC.e | Arbitrum One | `0xff970a61a04b1ca14834a43f5de4533ebddb5cc8` | Canonical bridged representation of Ethereum USDC |

The first two are listed in [Circle's issuer registry](https://developers.circle.com/stablecoins/usdc-contract-addresses); the distinction and both Arbitrum contracts are explicit in [Arbitrum's USDC guide](https://docs.arbitrum.io/arbitrum-bridge/usdc-arbitrum-one). Explorer links in those documents were **not** independently opened. A publisher registry match is not an independent bytecode, current pause/denylist or state check.

### Contract-specific conversion matrix

| Input → output | Rail | What is supported by the sources | What remains unverified |
| --- | --- | --- | --- |
| Ethereum native USDC → Arbitrum native USDC | Native CCTP V2 burn/mint | Domains 0 → 3; exact asset and TokenMessengerV2 registry addresses documented | Current burn cap, Fast allowance, amount-specific fee, minimum, timing and applicable access terms |
| Arbitrum native USDC → Ethereum native USDC | Native CCTP V2 burn/mint | Domains 3 → 0; exact native contracts documented | Same operational and legal gaps; this does not accept every dollar-denominated token |
| Ethereum native USDC → Arbitrum USDC.e | Canonical lock/mint gateway | Arbitrum explicitly distinguishes this output from native CCTP output | Current USDC-specific gateway/router mapping, execution cost and operational state |
| Arbitrum USDC.e → Ethereum native USDC | Canonical burn/release claim | Paired-token architecture burns on child chain and releases parent escrow after dispute window and confirmed assertion | Exact current USDC gateway, backing, claim cost, present dispute duration and completed claim evidence |
| Arbitrum USDC.e → Arbitrum native USDC | Alleged direct CCTP converter | **Not established** | No exact accepted variant, configured connection or native output proof |
| Arbitrum native USDC ↔ USDC.e | Potential AMM swap | Distinct contracts may be market-exchanged; no pool was verified here | Actual pool, executable bid/ask, fee, depth, fill and repeated flow |

Primary native-rail sources: [supported tokens/domains](https://developers.circle.com/cctp/concepts/supported-chains-and-domains), [mainnet contract registry](https://developers.circle.com/cctp/references/contract-addresses), [Arbitrum USDC guide](https://docs.arbitrum.io/arbitrum-bridge/usdc-arbitrum-one) and [canonical bridge architecture](https://docs.arbitrum.io/how-arbitrum-works/deep-dives/token-bridging). For Ethereum and Arbitrum, the registry lists TokenMessengerV2 `0x28b5a0e9C621a5BadaA536219b3a228C8168cf5d` and MessageTransmitterV2 `0x81D40F21F12A8F0E3252Bccb954D722d4c464B64`; these are **rail contracts, not token addresses**.

The current [CCTP fee page](https://developers.circle.com/cctp/concepts/fees) lists Ethereum-source Fast at 1 bp, Arbitrum-source Fast at 1.4 bp and Standard at 0 bp for those chains. These are mutable protocol-fee documentation values at retrieval, **not route quotes or all-in costs**. Source and claim gas, destination submission, relay/integration fees, failed attempts and capital lock remain. The same page documents Standard fee-switch exceptions on some deployments and gives inconsistent maxFee-failure descriptions, so generic prose must not substitute for version-specific runtime verification.

**A material current-doc expansion must not be overlooked:** [CCTP for non-USDC assets](https://developers.circle.com/cctp/expanded-assets) describes configured third-party ERC-20 assets and EURC using **CrossChainTokenService**, a different entry contract and source-native-gas fee model from native-USDC TokenMessengerV2. It offers issuer-controlled, ownerless and native-crosschain token configuration paths. That is not proof that a configured USDC.e connection exists, or that transporting a third-party claim converts it into the different Circle-native USDC contract. The overview does not establish the exact connection/backing/output rights for this candidate.

Access is not solved by a par quote. The sources distinguish on-chain transfer and bridge redemption from fiat redemption, but this pass did not independently read user-specific issuer onboarding, KYC, jurisdiction, minimum or banking terms. Arbitrum's general “directly redeemable” benefit for native USDC cannot be converted into an assumption that this user has unrestricted bank-USD redemption access. No unsupported fiat exit is used.

### Nearest valid mechanism, not a profitable strategy

`ECO-VARIANT-06` is an **architecture-level hypothesis**: buy the exact USDC.e at a genuine executable discount using native Arbitrum USDC; redeem through its verified gateway to Ethereum native USDC; then use native CCTP to return native Arbitrum USDC. The payer would be a seller paying for immediacy while the converter bears delayed settlement, backing and operational risk.

This is not yet a fully supported current contract path: the exact USDC gateway mapping/backing and market pool/quote were not obtained. A canonical architectural description alone does not close those gaps. No repeatable net-basis claim is made.

The economic identity is returned native USDC minus starting native USDC, all gas/relay costs, actual financing, allocated operating costs and realized losses. Benchmark excess is a separate comparison; do not double-count funding or inventory costs. No numerical return example is supplied because no live executable quote was collected.

The cheapest useful falsifier is a current exact-contract pool quote and documented gateway mapping/claim cost: if the discount cannot cover **the full redemption interval's capital cost plus all cycle fees**, or a required token is unsupported/paused/unbacked, the candidate fails. A label, nominal peg or a par quote for a different wrapped output is insufficient. [conversion-matrix.json](conversion-matrix.json) preserves route-specific access, fee, delay, cap and redemption unknowns.

## Other economic mechanisms supported by the assigned readings

### 1. Loan-backed inventory is ordinary collateralized financing

Appendix G of the [seed paper, v2 dated 2025-06-18](https://arxiv.org/html/2501.17335v2#A7) reports a concrete historical lifecycle: buy WBTC on Ethereum, initiate its bridge, borrow the receiving-chain WBTC on Aave before arrival, sell it, receive the delayed bridge output and repay. This can reduce the wait before the sale leg, but it requires posted collateral, debt-asset compatibility, headroom and repayment funding. It is **not** a free cross-chain flash loan.

Exact references supplied by the paper, not independently verified receipts:

| Step | Public transaction reference |
| --- | --- |
| Ethereum purchase | [Ethereum transaction](https://etherscan.io/tx/0xf9dac896022ab70b8831e4a0139b97738180bf1605f216400f66bb0957f9208a) |
| Ethereum bridge initiation | [Ethereum transaction](https://etherscan.io/tx/0x452a9c05cc02fe146ce13a788456f02bf68c83ee3d6a57c0402ccfd8c5108903) |
| Arbitrum borrowing | [Arbitrum transaction](https://arbiscan.io/tx/0xf7e5f28d391c2dee5f982fd27f8caf6fc250acd54ebe3d06ace25ac2a85feeff) |
| Arbitrum sale | [Arbitrum transaction](https://arbiscan.io/tx/0xdd45995d12a9404a667c13ec0ab014b927abeea3cf9cd650a5e8e63845c7972f) |
| Bridge arrival | [Arbitrum transaction](https://arbiscan.io/tx/0x7015f3ceff63cc5e4c2e7abffe3ed6c1d21da6b3305724ed1c9177e50cf411bf) |
| Loan repayment | [Arbitrum transaction](https://arbiscan.io/tx/0x798b5371e00f8a0d5dd7471aa36488e490f853004e638b547f272013b19db935) |

The seed's empirical window is **September 2023–August 2024**, not current 2026 performance. Its idealized theory assumes away costs and its empirical profit definition does not price inventory risk. Reported historical transaction economics therefore cannot be reused as an all-in small-account return.

`ECO-CREDIT-01` is worth understanding because it identifies where inventory financing acts. Its cheap falsifier is exact reserve/borrow eligibility and deliverable debt asset, followed by executable spread versus all-in financing and settlement cost. No such current reserve or quote check was run here.

### 2. Across repayment location has value, but replenishing inventory is not free

The recovered [legacy FAQ](https://legacy-docs.across.to/user-docs/additional-info/faq) explains relayers fronting funds and receiving reimbursement. Its old chain list, airdrop material and timing estimates must not be projected onto 2026.

Current [fee documentation](https://docs.across.to/introduction/fees) says the **LP-fee component can be zero when repayment is on the origin chain**. This is not zero user fee or zero relayer cost. Destination fill gas, capital risk, reimbursement delay and eventually restoring depleted destination inventory remain. [Running-relayer docs](https://docs.across.to/introduction/relayers/running-relayer) already describe inventory targets and intelligent repayment selection, so this is an existing cost mechanism, not evidence of uncaptured alpha.

For `ECO-REPAY-02`, compare a whole inventory cycle: fill on the destination, receive repayment, then restore targets through genuine opposing flow or a separately costed route. The cheap falsifier is that replenishment/capital costs exceed the saved LP fee or attainable user fee. No fill access, competitive share or current quote was measured. The fee docs deprecate `/suggested-fees` for new integrations; no obsolete collector was built.

### 3. cBridge rebalancing rebates have an identifiable payer

The [Celer FAQ](https://cbridge-docs.celer.network/reference/faq) distinguishes fixed/canonical xAsset transfers from pooled xLiquidity routes. Some xLiquidity pairs use StableSwap and can deliver more destination tokens when a transfer restores balance. The LP bears the associated inventory-value change/impermanent loss. The FAQ also warns the deviation commonly remains below fees except under substantial imbalance; its numerical illustrations are **not current quotes**.

`ECO-IMBALANCE-03` asks whether a legitimate beneficial rebalancing flow can close through **an independently supported cheaper return rail**, rather than undoing itself through the same pool. Ordinary external flow must recreate the imbalance for repetition. CCTP can only be used where the actual output asset is eligible; it cannot be silently substituted for USDC.e redemption.

The [Celer contract registry](https://cbridge-docs.celer.network/reference/contract-addresses) was consulted, but extraction lost some table labels. No ambiguous address was asserted to be the correct xLiquidity pool. The first useful check is exact pair/contract identity and an executable full-cycle quote; absent that, the surplus remains unknown.

### 4. Fallback tokens and refunds are accounting guards, not yield

The [Synapse support FAQ](https://docs.synapseprotocol.com/docs/Support/Transaction-Support) states that destination slippage can cause delivery of an intermediate asset instead of the requested final token. This creates a different inventory/exit problem, not a successful final-asset fill at the quoted value. Failed initiation, manual recovery, refunds and gas airdrops must retain their own transaction/accounting treatment; none is independent arbitrage income.

## Actual recent non-EVM changes, with deployment evidence limits

**2026-06-03 — Axelar Solana mainnet integration.** The [official launch](https://www.axelar.network/blog/axelar-solana-mainnet) explicitly reports mainnet availability and names SHx from Stellar and SAUCE from Hedera as launch uses. The [Solana ITS guide](https://docs.axelar.dev/dev/send-tokens/solana/its/) requires exact token IDs/mints and describes mint/unlock and optional on-arrival execution. This is more concrete than a proposal, but still provider-reported deployment, not our independent state/receipt check. `ECO-REPRESENTATION-05` remains a watchlist: token claim equivalence, live programs/mints and both sides' depth are unverified. New routes can compress an old basis rather than create a persistent one.

**2026-10-23 — Gateway EURC/cirBTC unified balances.** Circle's [dated launch](https://www.circle.com/blog/circle-gateway-now-supports-cirbtc-and-eurc) says separate unified balances now support EURC and cirBTC; the EURC list includes Ethereum, Base and **Solana**, among others. Separate balances do not exchange EUR, USD and BTC claims. The [Solana EURC pre-mint announcement](https://www.circle.com/blog/circle-gateway-new-pre-mint-address-for-eurc-on-solana) reports a concrete operational account, but this is **not the tradable EURC mint or a user deposit address**; pre-mint inventory is not circulating liquidity. Never send funds to that account.

The [Gateway overview](https://developers.circle.com/gateway) describes finalized prefunding and a permissionless fallback withdrawal, not unsecured credit. The launch's sub-500ms access claim is **after deposit finalization**, not instant source finality or atomic market execution. Its launch fee claims and any holiday omit important cycle costs; the seven-day fallback and service/issuer concentration matter. Some blog footer language still describes older USDC-only coverage, so asset-specific technical and legal terms must be reconciled rather than silently harmonized.

`ECO-GATEWAY-04` is therefore an inventory-cost hypothesis: a same-EURC price difference might require less duplicated inventory, but exact mints/contracts, eligibility, executable depth and total cost remain missing. A mature issuer does not automatically establish the audit coverage or operating history of its newest instrument.

## Newer citing work: useful screening, not observed capture

[When AI Agents Meet MEV, dated 2026-09-15](https://arxiv.org/html/2609.17897), explicitly cites the seed paper in reference 15. The economics/methods and references were read; attack-oriented sections were context-only and excluded from strategy construction.

Its aggregate calibration uses September 2025–March 2026, with swap observations from February 22–25 and March 23, 2026. Limited overlapping price bins and cost-screened scenarios are not simultaneous executable cross-chain bids and asks. Simulated success probabilities are not actual fill rates; chain-wide aggregate fees are not transaction gas. The useful method is to compare an exact route's gap to its real execution/settlement/financing costs, not to promote modeled viability percentages into net returns.

Backward source work included the seed's complete Appendix G, the assigned bridge references, current Across economics/relayer docs, Celer's registry and native-asset/bridge distinctions. The five nonpriority assigned references were triaged honestly, not claimed as full readings.

## Conclusion and stopping point

The strongest economic leads are (a) financed inventory replacement, (b) an explicitly LP-funded rebalancing surplus with an independent closing route, and (c) newly documented issuer-native cross-chain inventory access. Across repayment choice is a supporting cost optimization. The added stablecoin test chiefly establishes a valuable negative: **nominal dollar pegs and general CCTP support do not prove an executable variant converter or equal redemption rights**.

Contract/quote/access gaps are concrete availability blockers, not evidence that no profitable strategy exists. All expected returns remain unknown. Nothing here qualifies T2/T3, an allocation under protocol/issuer/chain caps, monthly 99% drawdown confidence, the separate annual tail-probability gate or independent approval. The package is ready for source/integration review; this bounded pass stops here without new collectors or an automatic next wave.
