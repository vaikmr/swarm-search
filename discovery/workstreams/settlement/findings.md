# Settlement discovery and candidate 6 pressure-test

**As of 2026-10-29. Research hypotheses, not an allocation or a return certificate.**

Inventory-aware intent filling has a coherent **cost-saving** mechanism, but the sources do not establish a separately payable arbitrage edge. Across already lets relayers choose repayment chains; Relay already lets solvers choose withdrawal strategies. The comparison must therefore be against ordinary filling **plus independent rebalancing**, for the same accessible fills and the same terminal token inventories. No entrant allocation, executable margin, complete lock-duration distribution, or qualifying T2/T3 result was obtained.

One concrete negative finding changes the available instrument set: **Relay Vaults is winding down and no longer supports new deposits.** Its historical description of instant solver rebalancing is not a presently open LP-entry opportunity. This does not mean Relay Settlement has stopped. [Official Vaults overview](https://docs.relay.link/references/protocol/vaults/overview).

## Candidate 6: inventory-aware Across / Relay filling

### Who receives which funds

Keep these roles separate: origin depositor; destination user/contract recipient; fill executor; repayment/withdrawal beneficiary; optional integrator fee recipient. A fill transaction sender does not automatically own every related refund address, and the depositor's principal is not relayer revenue.

**Across, documented V3-style path:** the user escrows input on the origin SpokePool. An eligible relayer spends its own destination tokens to deliver the specified output to `recipient`, choosing a repayment chain when filling. The dataworker matches deposits and fills, builds chain-specific payment lists, proposes a bonded HubPool bundle on Ethereum, waits through challenge, and sends roots through canonical bridges. Payment execution then reimburses the designated relayer. Permissionless execution of a refund is not ownership of that refund. [Lifecycle](https://docs.across.to/concepts/intent-lifecycle-in-across).

**Relay Settlement:** the user deposits into an origin Depository; the solver fronts destination inventory. An Oracle attests deposit and fill, and credits the solver on the Hub on Relay Chain. To obtain spendable wallet tokens, the solver still selects target chain, depository, currency, amount, recipient and nonce; moves Hub balance into the withdrawal address; obtains Oracle-authorized parameters and an Allocator MPC proof through Aurora/NEAR; and submits the proof to the target Depository. **A real-time Hub credit is not yet wallet cash.** Quoting and order distribution are outside this settlement protocol. [How It Works](https://docs.relay.link/references/protocol/how-it-works).

Relay's solver-driven **user refund** is another fronted payment, this time on the origin, followed by settlement. Do not confuse the user's refund with the solver's reimbursement. The read page specifically limits its protocol-code-backed refund discussion to that solver-driven path; it does not establish every product-layer recovery route. [Same source](https://docs.relay.link/references/protocol/how-it-works).

### Exact inventory loop and incremental economics

For an eligible order O -> D:

1. Reserve actual spendable output inventory on D and gas on each required chain. Do not treat the user's escrow or an expected reimbursement as available capital.
2. Pay `q` output tokens to the destination user. Record one pending receivable, its token representation, settlement domain, beneficiary and allowed repayment destinations.
3. Choose repayment to replenish the inventory that will be needed next, rather than automatically taking the cheapest quoted refund location.
4. Only after reimbursement/withdrawal is actually spendable may it fund another obligation. If it is on the wrong chain or in the wrong token form, complete and cost the conversion/rebalancing leg.
5. Close with the same terminal inventory, liabilities and unresolved claims as the ordinary-filling comparator. Opposite-direction user flow can reduce rebalancing, but its availability and accessible margin are unknown.

Across says the user's total fee is `inputAmount - outputAmount`, split into LP and relayer components. Origin-chain repayment has **zero LP fee**, but the relayer has spent on D and recovered on O: it has shifted inventory toward O. Restoring D costs something unless genuinely useful opposite flow absorbs that inventory. Destination repayment may instead pay an LP fee to avoid that independent relocation. An LP fee already deducted from the refund must not be deducted twice. [Fees](https://docs.across.to/introduction/fees).

For one completed order, let `A_r` be the **actual net reimbursement**, after any deductions already embedded in it, and value all assets consistently:

```text
profit = V(A_r) - V(q)
         - fill/claim gas - rebalancing - funding
         - failed-race costs - inventory losses - access/operating costs
         + independently proven external payments
```

For the **same fills and terminal inventories**, `q` cancels:

```text
incremental profit =
    V(net reimbursements_inventory-aware - net reimbursements_ordinary)
    - difference in all rebalancing/funding/gas/failure/inventory/access costs
    + difference in independent external payments
```

These are accounting identities, not measured returns. Ordinary relayer margin, the LP fee avoided by a refund choice, a quoted capital fee, and an alleged inventory spread are not four independent revenues. A transfer of existing principal is not profit. A rebate counts separately only if a distinct paid transfer and its conditions are established.

Across's optional `appFee` goes to **`appFeeRecipient` on the destination chain**, not automatically to the filler. Its documentation now accepts a Solana base58 recipient as well as EVM destinations. This is integrator compensation for serving users, not a free solver bonus; an operator receiving both must reconcile the actual payments and customer-acquisition costs. No release date or executed app-fee transfer was independently established here. [Fees](https://docs.across.to/introduction/fees).

### Capital conservation and lock duration

At each chain/token pair:

```text
spendable inventory =
    initial wallet inventory + settled inflows + actually disbursed borrowing
    - user fills - outward rebalances - debt repayments - relevant gas outflows
```

Pending Across refunds, Relay Hub credits awaiting withdrawal, in-flight bridges and undisbursed credit requests are **not** spendable inventory. A pool of principal cannot simultaneously finance overlapping orders. Borrowed funds create a liability and consume collateral/credit capacity; they do not create free additional equity.

Measure lock time from first irrevocable capital commitment until the returned tokens are spendable in the **required chain and representation**. Across's documented minimum ~1.5-hour proposal cadence is not a guaranteed fill-to-refund duration or p99 bound: validation, challenge, bridges, execution and subsequent rebalancing remain. Relay's per-order real-time Hub update likewise does not bound Oracle, MPC, withdrawal or target-liquidity delay. No empirical lock-time distribution was collected. [Across lifecycle](https://docs.across.to/concepts/intent-lifecycle-in-across); [Relay lifecycle](https://docs.relay.link/references/protocol/how-it-works).

Count pending protocol claims and all relevant issuer/bridge/chain dependencies under the original $15k common-failure-domain ceiling. Across may depend on Ethereum HubPool even when the two asset venues are rollups. Relay additionally names Relay Chain and an Allocator on Aurora/NEAR: counting only the two trading venues does not establish compliance with the three-chain limit. The exact deployment/chain mapping and whether any domains coincide remain unverified.

### Access, instrument changes and concrete blockers

- **Across access:** open filling after exclusivity expiry is documented; exclusive frontend flow requires nomination and a track record. A public relayer implementation is not a promised share of useful orders. The freshly fetched nomination page still discusses a Q1-Q2 2025 rollout, and all three Across pages warn that upgraded-protocol/API documentation is coming. Thus these are current published descriptions, not independent verification of every latest deployment or admission outcome. [Nomination](https://docs.across.to/introduction/relayers/relayer-nomination).
- **Relay access:** the requested solver-guide URL resolved to the same How It Works content, not an independent access guide. That page separates application quoting/order distribution from settlement and verifies authorized **Oracle signers**. It does not establish an open solver feed, a whitelist decision, the user's admission, fee schedule, withdrawal liquidity, or executable spread. Oracle authorization is not evidence that solvers themselves are whitelisted, nor evidence that order flow is permissionless. [Resolved page](https://docs.relay.link/references/protocol/how-it-works).
- **Relay Vaults:** current docs explicitly say no new deposits; existing-position UI exits remain available until **2026-12-31**. The page's older base-yield/boost-yield explanation is historical mechanism context, not an accessible new capital service. The effective wind-down date is not given; do not invent a launch/sunset date. [Vaults](https://docs.relay.link/references/protocol/vaults/overview).
- **New financing rails:** Circle's 2026 release records document Credit API, institutional digital-asset-backed borrowing, Circle Match and RWA Redemption Advance. The read Credit API requires a Core API Agreement, a separate offline credit contract and an account entitlement. An RWA advance needs an Arc burn receipt and Treasury approval; Credit Express onchain delivery has its own pending-to-complete/failed lifecycle. No direct Across/Relay integration, entrant entitlement, actual fees, credit limit or current disbursement latency was verified. These could change funding costs for an eligible institution, not make the above inventory loop atomic. [Release notes](https://developers.circle.com/release-notes/mint-2026); [Credit API](https://developers.circle.com/circle-mint/concepts/credit-api).
- **Cheaper rebalancing is not a new payment:** CCTP offers fast versus standard settlement choices, but fees/allowance and asset support matter. The detailed fee page lists current standard fees as zero while also describing a standard-fee switch on some deployments; its prose disagrees about whether too-low fast `maxFee` reverts or degrades. Do not promise a universal free path or precise failure behavior without contract/version-specific checking. Gas remains. CCTP cannot directly burn an arbitrary bridged USDC representation. [CCTP fees](https://developers.circle.com/cctp/concepts/fees); [Arbitrum USDC identities](https://docs.arbitrum.io/arbitrum-bridge/usdc-arbitrum-one).

**Nearest valid result:** a source-backed inventory/cash-flow specification and falsification checklist, not a replayed profit estimate. The bounded pass did not obtain entrant-available orders, matched all-leg costs, exact refund-beneficiary ownership, current contract deployment mappings, or spendable-repayment timing. No old bulk collector, additional RPC, transaction or simulator was run.

**Cheapest falsifiers, if separately authorized later:** first establish access to one concrete eligible route and its precise tokens/beneficiaries. Then compare the same small set of lawful fills under repayment choices, mark terminal inventory, account for all failed attempts and settlement/withdrawal costs, and require positive incremental net margin. Stop the new-depositor Vaults branch now. A separately paid inventory-service contract would be needed to establish a distinct payer beyond ordinary filling.

## Other settlement mechanisms and constraints

### Collateralized loan-backed inventory replacement

Seed v2 Appendix G describes purchasing WBTC on Ethereum, initiating its bridge, borrowing the matching WBTC on Arbitrum/Aave about eight seconds later, selling there, then repaying after the bridged tokens arrive roughly seven minutes after the trades. The source reports about 0.5 ETH profit for that historical example. Those are **paper-reported historical observations**, not independently reconciled net PnL or a scalable current opportunity. Collateral, borrow availability, health factor, interest, exact repayment token, bridge arrival and debt closure are required. It is **not a free cross-chain flash loan** or proof of no upfront economic capital. [Seed Appendix G](https://arxiv.org/html/2501.17335v2#A7).

The same technique could finance a settlement gap, but it must beat the all-in cost of pre-positioned inventory. Extra borrowing can increase liquidation and common-domain exposure even when the trade legs are delta-neutral. The paper's empirical window is **September 2023-August 2024**. Its later publication and 2026 extended abstract do not refresh those observations.

### Native/bridged USDC and canonical exits

Arbitrum's official page distinguishes native USDC `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` from USDC.e `0xff970a61a04b1ca14834a43f5de4533ebddb5cc8`. The canonical bridge and Circle burn/mint route deliver different forms. A hypothesized wrapper discount only closes if the purchased claim can actually be redeemed into the exact debt/sale asset, within priced time and risk. A ticker match or generic $1 redemption statement does not establish the user's issuer-redemption eligibility or a permissionless conversion. No pool quote, borrow rate, gateway escrow or present basis was measured. [Official identities](https://docs.arbitrum.io/arbitrum-bridge/usdc-arbitrum-one).

Arbitrum quickstart describes at least seven days for child-to-Ethereum withdrawals, followed by a separate claim; deposits are described as roughly 15-30 minutes depending on congestion. OP Standard Bridge describes 1-3 minute deposits and a seven-day withdrawal challenge period, independent bridged token representations, and excludes rebasing/fee-on-transfer tokens. These are **documentation estimates/mechanics, not current delay measurements**. [Arbitrum](https://docs.arbitrum.io/arbitrum-bridge/quickstart); [OP current page](https://docs.optimism.io/app-developers/guides/bridging/standard-bridge).

Scroll's replacement withdrawal-gateway page requires finalized L2 roots and a Merkle-proof-driven L1 execution; it does not give a numeric delay. Do not import an optimistic seven-day window or an old table's timing into this ZK withdrawal path. Nor does proof readiness establish that a withdrawal claim is assignable or marketable. [Scroll](https://docs.scroll.io/en/technology/bridge/withdraw-gateways).

Current Superbridge describes canonical bridges, third-party protocols and solver networks under one interface. The aggregator is not an extra independent settlement protocol or evidence of atomicity, current fees or a specific exit time. [Current overview](https://docs.superbridge.app/overview/bridging).

### Non-EVM settlement and recent contractual instruments

NEAR OmniBridge's current documentation identifies `omni.bridge.near` and direction-specific verification: light clients on some routes, Wormhole on others, and MPC verification on additional routes, followed by Chain Signatures. Its NEAR outbound flow locks/burns, obtains signatures and then mints/releases on the destination. A local NEP-141 callback/refund is not global cross-chain rollback. The docs contrast this with a 4-8-hour Rainbow Bridge NEAR-to-Ethereum path, but no current measured timing, token mapping, pool depth, deployment date or executable spread was established. A faster route can **remove** an old inventory premium, rather than create income. [Overview](https://docs.near.org/chain-abstraction/omnibridge/overview); [Flow](https://docs.near.org/chain-abstraction/omnibridge/how-it-works).

Circle's official 2026 Mint release notes report Credit API on April 1; cirBTC API support on May 12; institutional cirBTC-backed borrowing and Arc mainnet support on September 16; Circle Match on September 28; and RWA Redemption Advance on October 19. These are **provider release records**, not independently observed contracts, account access or activity. The RWA advance bridges burn/redemption timing into USD funding but charges draw/recurring fees, constrains account balance, and can require manual approval. A newly supported Arc instrument does not inherit a twelve-month history or verified TVL/audit merely because Circle is an established provider. [Release notes](https://developers.circle.com/release-notes/mint-2026); [Credit mechanics](https://developers.circle.com/circle-mint/concepts/credit-api).

## Citation triage and honest reading coverage

The nine local IDs below are extraction IDs, not original paper reference numbers.

| ID | Actual access/reading | Relevance |
| --- | --- | --- |
| R008 | Exact cited Arbitrum quickstart read in full | Asymmetric exit, separate claim and native-asset gas |
| R049 | Old URL returned Not Found; current Standard Bridge main text read in full | Token-pair-specific claims; distinct representations |
| R058 | Old URL served unrelated Community FAQ; current Withdraw Gateways main text read in full | Finality/proof/execution; narrower replacement, not recovered original |
| R059 | Old URL unavailable; current Bridging overview read in full; another stale withdrawal URL also failed | Aggregator versus actual underlying settlement |
| R010 | Primary conference PDF located by search; snippet/metadata only | PBS concentration/access context; no new credit instrument |
| R021 | Inventory/seed context only, no fresh page retrieval | DEX volume is not entrant flow or net profit |
| R040 | Primary arXiv abstract read, not full paper | Ordering-game context; attack examples excluded from construction |
| R052 | Primary arXiv abstract read, not full paper | Algorand FCFS differs from EVM ordering; no current performance inference |
| R066 | Citation metadata/seed context only | Atomic cyclic-arbitrage literature is not proof of asynchronous claim closure |

**Counts:** 20 original document-fetch attempts plus six candidate-specific attempts; six original searches plus two candidate searches; zero new RPC calls. There are **16 distinct fully read substantive document bodies**, comprising four priority topic documents (one exact original and three explicitly labeled current replacements), seven supplementary documents, and five distinct candidate-6 documents. This is **not** a claim of reading all four original cited texts, the full seed paper, or 26 independent sources. Two candidate Relay URLs resolved to the same body and count once. Seed sections including all Appendix G and the Appendix B examples were read, not the whole paper. Two abstracts and search snippets are excluded from full-read counts. Runtime site metadata was not treated as article content; transport truncation remains recorded even where the full substantive body ended before that metadata.

Backward-reference resolution located the R010 primary conference PDF and the R040/R052 primary abstracts. Newer related search identified *When AI Agents Meet MEV: Cross-Chain Arbitrage in the Agentic Economy* (arXiv:2609.17897) and *Bunny Hops and Blockchain Stops* (arXiv:2511.17527), but these are **search-result-only leads here**, not full reads or verified contemporary fills. A 2026 SIGMETRICS extended abstract repeats the seed's 242,535-trade historical study; its publication date is not a new data window. Attack-focused search results were excluded from strategy development.

`sources.json` records each assignment, URL, reading level, date/data-window distinction and linked mechanism. `retrieval-log.json` preserves bounded attempt/search metadata and content digests, not bulk copyrighted texts or site runtime configuration. `mechanisms.json` keeps returns, entrant share and lock-time performance unknown. Local tests check package integrity and accounting assumptions, **not** market feasibility.

The original $50k, concentration, leverage, drawdown/tail, protocol maturity and independent T2/T3 gates are unresolved. This package ends the bounded pass; it does not authorize live filling, borrowing, a replay/backfill, or another discovery wave.
