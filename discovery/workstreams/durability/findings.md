# Durability and access challenges — one discovery pass

Research cutoff: **2026-10-29**. Scope: independent review, not strategy return
origination, an allocation recommendation or a new judge verdict.
[Source records and exact reading limits](sources.json) accompany this report.
Only this directory changed; the earlier actor, APY and replay work was not
resumed.

**Coverage:** all nine assigned bibliography entries were triaged. The four
priority references were read at their actual scope: full Protect overview,
BuilderNet overview and Dencun FAQ pages, plus the complete extracted 17-page
R056 publisher paper. A documentation-page read does not mean the entire site.
R055 and R071 remain abstract-only; the current Polygon page was read only for
its substantive context. Additional newer and backward references do not inflate
the four-of-32 contribution. The initial reference phase used **20
document-fetch calls, four searches and zero new RPC calls**. The later
candidate-only extension is recorded below. Continuation chunks and landing
pages are not separate references.

## Most useful conclusions

Discovery should continue to distinguish **service payments** from **risk
premia** and **privileged access rents**, rather than declare every persistent
cross-chain basis an arbitrage. This pass provides no measured spread or return.
The strongest concrete evidence is about rights and market structure:

- Public visibility, permitted submission, priority-update access and actual
  inclusion are different. Current BuilderNet documentation exposes a quote
  stream without a key but issues propAMM priority-update keys on request.
  Ordinary searcher/solver participation has a separate documented path.
  [R014](https://buildernet.org/docs),
  [DUR-S06](https://buildernet.org/docs/how-to-participate).
- The economic claim can change even if the token symbol does not. Circle's
  September 2026 Noble notice gives distinct minting, redemption, burn-limit and
  manual-redemption phases. A destination asset cannot be treated as instantly
  interchangeable solely because both tokens are called native USDC.
  [DUR-S08](https://www.circle.com/blog/circle-is-discontinuing-support-for-usdc-and-cctp-v1-on-noble).
- A live ecosystem does not imply uninterrupted availability of each feature.
  BAM's October 2026 notices describe mainnet activity but plan maintenance
  during which MPP and DBI are unavailable while ordinary Block Engine bundles
  remain supported. Those plans do not confirm that activation or restoration
  actually occurred by this report's cutoff.
  [DUR-S03](https://bam.dev/blog/bam-changelog-sept-23-oct-9/),
  [DUR-S09](https://bam.dev/blog/update-on-bam-readiness-for-alpenglow-on-mainnet/).

These are constraints on hypotheses, not proof that the opportunity set is
empty. Restricted minting, private orderflow or operational differences might
explain a basis without making it attainable, safely hedgeable or repeatable.

## DUR-ACCESS — identify the right being bought or earned

Protect describes private submission, refunds and filtering of reverting
transactions. The refund documentation says users reclaim part of the value
their flow creates, with the remainder shared with searchers and validators.
It also explicitly connects shared information to privacy and refund tradeoffs.
This is evidence of a value-sharing service, not evidence that a new searcher
can retain the gross MEV attributed to the same transaction.
[R032](https://docs.flashbots.net/flashbots-protect/overview),
[DUR-S01](https://docs.flashbots.net/flashbots-protect/mev-refunds).

Consequences for a legitimate proposed loop:

- Do not infer the accessible opportunity set from public mempool observations
  alone; missing private orderflow is not a zero-opportunity observation.
- Do not treat an open quote stream as permission to perform gated priority
  updates, or assume submission implies inclusion.
- Do not count a user refund, a searcher payment and a proposer/builder payment
  as three independent profits from the same surplus.
- Local revert filtering is not cross-chain rollback, and says nothing about
  inventory carried on an already executed second venue.

**Cheapest later falsifier:** write down which current access class the proposed
loop requires and whether a genuinely new entrant can obtain it under published
terms. If the loop needs a privilege the entrant does not have, reject the
access assumption before building a collector. This pass requested no access.

## DUR-CLAIMS — asset equivalence includes exit and mint rights

The Noble issuer notice is a concrete, in-window, non-EVM policy change. It says
Noble will not receive CCTP V2 and schedules:

| Announced event | Date | Relation to the research cutoff |
| --- | --- | --- |
| Disable new Noble minting through Circle Mint | 2026-10-13 | Scheduled before cutoff; not independently transaction-tested |
| Begin reducing CCTP V1 burn limits | 2026-10-31 | Still future at cutoff |
| Fully pause the Noble USDC contract and routes | 2027-01-12 | Future, not an already closed exit |
| Begin manual redemption | 2027-01-13 | Future, with compliance and snapshot conditions |

The same notice retains a transition period for transfers and certain exits.
It does **not** justify saying all Noble exits were closed on October 29.
Manual redemption requires, among other things, a holder-controlled wallet,
inclusion in the pause-day snapshot and Circle's compliance/security checks.
An announced issuer policy is not this worker's observation of deployed
contract state, a tested redemption entitlement or proof of venue liquidity.
[DUR-S08](https://www.circle.com/blog/circle-is-discontinuing-support-for-usdc-and-cctp-v1-on-noble).

**Cheapest later falsifier:** for each proposed representation pair, compare
issuer claim, authorized minter/redeemer, source and destination route support,
cutoff date, amount limits, transferability and accessible exit venue. An
unresolved mismatch is basis/default/access risk, not an assumed free hedge.
No actual discount, contract balance or mint/redemption transaction was fetched
in this pass.

For a scout's collateralized, non-atomic loan-backed inventory-replacement
hypothesis, apply the same rights test separately to collateral, loan proceeds,
the replacement asset and the final repayment asset. A symbol match is
insufficient. Borrowing is not free flash liquidity: a complete lifecycle must
still close debt and accrued costs and explain liquidation/recall exposure.
This is an accounting/risk challenge, not newly reconstructed evidence for the
seed paper's example.

## DUR-UPGRADES — versioned capability is not uninterrupted deployment

BuilderNet's current overview explicitly says its builder nodes are **not**
running in TEEs during a security-model transition, while backrunning and
routing remain in TEEs. An older whole-system TEE description should not be
silently reused for every current component. The overview gives no transition
date, so this is not labeled a dated 2026 launch.
[R014](https://buildernet.org/docs).

A separate in-window release, BuilderNet v1.6, documents changed orderflow
ingestion, bidding/latency improvements and out-of-block refund support. Its
publisher links versioned artifacts. That supports a release-capability claim,
not confirmation that every current node runs that build or that a particular
entrant captures more profit. No artifacts were downloaded or installed.
[DUR-S05](https://buildernet.org/blog/2025/12/02/buildernet-v1.6).

BAM's October 9, 2026 changelog supplies first-party evidence of existing Solana
mainnet participation and current revenue-distribution features. In that same
source, registry mainnet enrollment is a late-October **target**, and early
third-party operators are on **testnet**. Its October 5 readiness notice plans
MPP/DBI maintenance, fallback and gradual restoration, with exact timing to be
announced elsewhere. Neither source establishes completed activation,
restoration or registry launch by October 29.
[DUR-S03](https://bam.dev/blog/bam-changelog-sept-23-oct-9/),
[DUR-S09](https://bam.dev/blog/update-on-bam-readiness-for-alpenglow-on-mainnet/).

**Cheapest later falsifier:** match the needed capability to a dated production
release, supported access mode and operational status at the proposed trading
time. Specify what happens to each already executed inventory/loan leg if that
capability is unavailable. No outage probability is invented here.

## DUR-COMPETITION — do not turn historical surplus into entrant revenue

R056 separates theory, actual relay bids and interpretation of observed signing
latency. Its main empirical data are from March 4–April 11, **2023**, with
separate April 11 and May 3–4 subsamples. Its historical inference is not that
all late signatures prove intentional strategic behavior. The paper's
theoretical incentive is also not a small trader's accessible revenue stream:
proposer rights, infrastructure, other participants and competition matter.
This review uses it for durability and consensus-risk context only; it does not
propose consensus deviations or reproduce attacks.
[R056, sections 3–5](https://doi.org/10.4230/LIPIcs.AFT.2023.30).

The backward reference to Monnot's October 2022 post was checked directly. It is
an exploratory model, not an independent profitable-actor ledger. A newer
related paper, *Timing Games in Responsive Consensus Protocols*, was submitted
October 29, 2025; only its author abstract was read in this bounded pass.
Its proposed incentive design and simulations cannot be treated as a deployed
2026 instrument or fresh empirical returns. It is not counted as a fifth
complete paper.
[DUR-S07](https://ethresear.ch/t/timing-games-in-proof-of-stake/13980),
[DUR-S04, abstract only](https://arxiv.org/abs/2510.25144).

**Cheapest later falsifier:** require the scout to identify who pays the
surplus, why they continue paying, which part competitors or users capture,
what inventory/credit is scarce, and which historical regime generated the
evidence. No universal fee, capture-share or fill-probability constant is
substituted for those missing observations.

## DUR-SETTLEMENT — cheaper execution is not faster economic completion

Dencun activated on March 13, **2024**, not in the requested recent-instrument
window. Its FAQ describes a separate blob-cost regime for rollup data
publication, not a universal reduction in L1 execution gas or a benefit
automatically inherited by independent EVM L1s. Blob-retention policy is not a
guarantee that an arbitrary free provider serves every historical state or that
a withdrawal can settle instantly.
[R028](https://ethereum.org/en/roadmap/dencun/).

Other bibliography triage guards against similar substitutions:

- **R013:** the BNB homepage is ecosystem context, not a measured finality or
  arbitrage study. [Source](https://docs.bnbchain.org/).
- **R024:** the current Polygon URL describes checkpointed data transfer and
  example contracts; it does not substantiate an asset-withdrawal duration.
  [Source](https://docs.polygon.technology/pos/how-to/bridging/ethereum-polygon/matic-to-ethereum).
- **R045:** EIP-7547 currently displays **Stagnant**. It is not a deployed
  forced-inclusion promise. This does not establish the status of another
  inclusion-list proposal. [Source](https://eips.ethereum.org/EIPS/eip-7547).
- **R055:** only the Snow/Avalanche paper abstract was read; its experimental
  latency is not a present asset/bridge settlement guarantee.
  [Abstract](https://arxiv.org/abs/1906.08936).
- **R071:** only the SoK author abstract and bibliographic context were read.
  The academic/practitioner adoption gap is context, not proof of a deployed
  countermeasure. [Abstract](https://doi.org/10.1145/3689931.3694911).

**Cheapest later falsifier:** require a complete timeline from the first capital
commitment until reusable inventory and cleared debt are restored. Separate
execution, finality, message arrival, proof/attestation, redemption and
repayment. If the alleged return omits a capital lock or a claim mismatch, it is
not yet a closed arbitrage loop.

## Added human candidates — within this same pass

After the initial package was drafted, the user added seven hypotheses. The
authorized candidate-only extension used **three additional document fetches
and two searches**, below its six-fetch/two-search allowance. Total: **23
fetches, six searches, zero RPC calls**. Nothing was resumed from the old study.
The structured [seven-candidate critique](candidate-critique.json) separates
source observations, logical risk challenges and missing evidence. No generic
fee assumption, alleged trade sample or near-riskless claim was accepted.

### DUR-LIQUIDATION — candidate 5, ordinary permitted liquidation only

**Cross-chain information does not itself authorize liquidation.** Aave's
documentation defines eligibility through the protocol's Health Factor, using
protocol-oracle values, collateral and accrued debt. An observation of a price
elsewhere can inform valuation or a hedge, but is not independently a
protocol eligibility condition. This review found no documented cross-chain
informational privilege that bypasses those rules. It does not rule out every
other protocol design.
[DUR-C01](https://aave.com/help/borrowing/liquidations),
[DUR-C02](https://aave.com/docs/aave-v3/overview).

There is a material protocol-specific economic distinction: **Compound III
absorption is not an automatic cash bonus for its caller.** The protocol's
reserves absorb debt and receive collateral; caller gas/points are recorded
with possible future governance compensation. Purchasing discounted collateral
is a separate action, subject to inventory and reserve-target conditions.
A model that treats both steps as a generic Aave-style liquidator incentive
would misidentify the payer and the asset received.
[DUR-C03](https://docs.compound.finance/liquidation).

A liquidation discount is not necessarily a profitable hedgeable discount.
The exact collateral receipt, withdrawal rights, executable sale depth,
repayment asset and hedge instrument must match. Aave documents that aToken
redemption depends on available unborrowed liquidity; an interest-bearing
receipt cannot simply be booked as immediately withdrawable underlying.
No receipt option or reserve parameter was verified for a specific deployment.
[DUR-C02](https://aave.com/docs/aave-v3/overview).

For a lawful candidate, the later economic test would be proceeds from the
actually realizable collateral, less debt repayment, liquidation-specific
charges, execution/failure costs, bridge/settlement costs, hedge spread,
funding, margin and final unwind. A short perp only addresses part of market
price risk; it does not redeem a restricted claim, provide usable remote margin
during disruption or make separate chains atomic. No costs or quantities were
measured here.

**Safety boundary:** reject any variant whose claimed advantage requires
stale-oracle exploitation, manipulating or front-running an update, vulnerable
borrowers/contracts, strategic user harm or an ordering attack. No target was
searched for, no account list was collected, and no liquidation bot, timing
recipe or attack reproduction was produced. Protocol permission is not a legal
opinion about a particular jurisdiction or user.

**Nearest valid result:** a source-backed mechanism and payoff-rights critique.
A targeted replay is neither provided nor claimed: no candidate market,
current configuration, eligible historical event set, executable collateral
sale/hedge quotes or complete cost ledger was established. These are concrete
economic inputs missing from this pass, not a claim that public data is
universally unavailable.

**Cheapest later falsifier:** check whether the stated profit belongs to a
rewarded liquidation action, an unrewarded absorption action or a distinct
collateral purchase; reject any model counting an unpromised bonus. Then require
lawful protocol eligibility and a complete collateral-to-repayment exit path
before considering any separately authorized observation.

## Stop point and handoff

The strongest supported directions for the shared map are **permission-aware
access analysis**, **dated claim/redemption equivalence**, and **inventory/credit
completion across operational transitions**. These are independent filters on
scout hypotheses, not originated return evidence or a request for a new wave.

No spread, opportunity frequency, actor identity, fee budget, accessible
priority-update privilege, contract implementation, net return, monthly
drawdown distribution or annual tail probability was measured. Original
concentration and independent T2/T3 gates still apply to an eventual
recommendation; unknown profitability is not a discovery-stage rejection.
No private data, signing, transactions, new packages, runtimes or servers were
used. **One package, then pause.**
