# Canonical cost and capital-opportunity-cost model

Status: Stage 0/1 accounting specification, **T4 model, not an attainable-return
claim**. Public fee documentation was retrieved on 2026-10-29. No live transaction
was signed or sent, paid service purchased, or seven-day paper run completed.
The module is pure arithmetic, dependency-free, and has no networking/signing.

## 1. What the target requires, not what a strategy can earn

User-specified total capital `C = $50,000`; desired net monthly profit `N`:

```
required simple monthly total-capital net return = N / C
required gross contribution = N + costs - signed separate idle contribution
```

| Requirement (T4 arithmetic from user inputs) | Lower target | Upper target |
| --- | ---: | ---: |
| Net monthly profit | $2,000 | $5,000 |
| Simple monthly net return on all $50,000 | 4% | 10% |
| Gross contribution if infrastructure consumes its full $500 ceiling, before other costs and with no idle income | $2,500 | $5,500 |
| Corresponding simple monthly gross contribution / $50,000 | 5% | 11% |

These are requirements, **not forecasts, historical results, or evidence that any
strategy earns them**. The $500 is a user-imposed ceiling, not an assumed invoice
and not authorization to spend. Actual variable costs raise the gross threshold.
Deploying less than total capital raises the necessary return on deployed capital;
it does not change the total-capital denominator.

Reproduce: `python3 -m research_tools.costs`.

## 2. One net-PnL boundary across every strategy

Use a fixed UTC observation window and USD marks contemporaneous with flows:

```
G = strategy earned fees + realized trading PnL + strategy/hedge mark-to-market
    + funding received + actually earned/redeemable rewards and rebates
N = G + I_idle - sum(costs not already included in G)
R_total = N / 50,000
E = N - B_net
```

`N` is **marked net economic PnL**, exposed as `net_economic_pnl_usd`. It is not
realized cash PnL. Cash received, withdrawable liquidity and settled profit cannot
be inferred from it: unrealized appreciation or unsettled earned income can
produce positive `N` while cash receipts are zero. There is deliberately no
old cash-named output alias. Evidence for realized actor profit still needs a
separate cashflow/accrual/mark reconciliation.

`I_idle`, supplied as `idle_contribution_usd`, is the **signed** economic
contribution from separate idle holdings, including negative yield, price
changes and principal write-downs. Its scope excludes anything already in `G`.
Only genuinely earned yield on eligible funds belongs here; never assume yield
on locked relayer receivables, gas reserves, hedge collateral, bonds, or all cash
irrespective of deployment. A counterfactual lending return belongs in `B_net`,
not in `I_idle`. Funding paid is a cost. If gross uses **net** funding, flag
funding paid as already included. Do likewise for rebates and trading fees.
An idle depeg/default loss is a signed contribution (or is already in whole-
portfolio equity), not something to omit because an APY helper rejects -100%.
The helper converts rates; it does not model a principal default or recovery.

`B_net` is a feasible, same-capital, same-period benchmark including its own
entry/exit/claim gas, token conversion fees, and any necessary monitoring costs.
Report `N` and `E` separately: foregone lending is not a second cash expense.
Do not subtract it from `N` and then subtract the benchmark again for ranking.
The study's Stage 2 threshold is `p50(N) >= B_net + $300`, not `$300` above an
already benchmark-subtracted number. The independent judge owns that gate.

Reconcile all wallets, CEX balances, protocol positions, and claims:

```
net equity PnL = closing marked equity - opening marked equity
                - external deposits + external withdrawals
```

Equity includes outstanding liabilities, conservatively recoverable receivables,
unclaimed earned income, and native gas-token inventory. Principal moved between
owned chains/wallets is not revenue. Pair transfers and the receivable they create.
If net equity already includes an expense, show it for audit but do not subtract
again. Record the USD price source, timestamp, decimals, and stablecoin mark;
do not force every stablecoin to $1 during a depeg.

### Mutually exclusive adapter boundaries

- **Strategy-only contribution:** `G` excludes separate idle holdings; supply
  their entire signed contribution in `idle_contribution_usd`, and deduct only
  costs not already reflected in `G`.
- **Whole-portfolio equity contribution:** if `G` instead contains the reconciled
  whole portfolio, including idle accrual and price/default losses, supply zero
  separate idle contribution. All paid/embedded costs are audit-only using
  `included_in_gross=True`; only expenses genuinely outside the equity boundary
  are additional. This is an explicitly declared alternative adapter, not a
  reason to relabel already-net equity as pre-cost gross.
- **Execution-only transaction fee:** price execution alone in the fee helper
  and book additional L1/operator/auction components separately.
- **All-in transaction fee:** book the helper's complete total once, documenting
  which components it includes. Extra categories for embedded components are
  explicit zero with an inclusion explanation, not separate additional charges.

For example, $100 of idle accrual is either `G=0, I_idle=100` in a strategy-only
adapter or `G=100, I_idle=0` in a whole-equity adapter; not `100+100`. Likewise an
all-in fee of $0.54 is either one deduction or exclusive component deductions
summing to $0.54. These are synthetic **T4 accounting examples**, not observations.
The module cannot infer overlapping economic identities from numbers alone.
Category uniqueness is not provenance deduplication: adapters must preserve
transaction/cost IDs, component and scope metadata and their inclusion decisions.

### Mandatory ledger categories

Each is present as known amount, sourced explicit zero/inapplicable, or unknown.
Unknown never silently becomes zero. `net_pnl` suppresses net outputs when a
category is missing/unknown and suppresses benchmark excess when `B_net` is absent.
`included_in_gross` avoids subtracting a disclosed cost a second time.

| Category | Required treatment |
| --- | --- |
| execution_success | Receipt gas used times actual effective price for successful included transactions |
| execution_failed | Same for included reverts/replacements/cancellations; private bundles are not universally free when lost |
| data_operator_fees | Additional L1/blob data and operator fees only where not embedded in charged gas |
| auction_payments | Solver/OFA user refunds, builder/sequencer/auction payments not already in receipts |
| dex_cex_fees | Every filled DEX/CEX leg, pool fee, protocol fee, and applicable tier; separate rebates as revenue |
| bridge_rebalance | Actual bridge/LP fees, route conversions, replenishment and claim gas; no hot-path bridge does not mean free inventory replenishment |
| slippage | Only relative to the declared pre-cost reference; actual fills may already include price impact and spread |
| borrow_interest | Time-varying borrow indexes, margin opening/rollover charges, and liabilities |
| funding_paid | Paid perp funding over actual intervals; received funding is revenue |
| hedge_costs | Hedge spread, rehedge trades, unwind fees, and liquidation penalties not counted elsewhere |
| lp_lvr | LVR/IL attribution only if not already reflected in marked LP equity; never deduct IL and LVR as independent losses from the same marked path |
| custody_withdrawal | CEX withdrawal/deposit/settlement fees and minimums by asset, network, time, and jurisdiction |
| infrastructure | RPC CU usage and peak capacity, servers, storage/egress, archive/trace data, logs and monitoring |

Taxes are a flag, **not tax advice and not assumed to be zero**: headline results
are pre-tax; jurisdiction, legal treatment, reporting and tax calculation remain
unverified. Labor and one-time development are separately disclosed, unpriced
unless measured. Setup/data-backfill invoices are research costs and must not be
hidden in a free production run; disclose first-month and steady-state economics.

## 3. Public primary cost evidence and limitations

Published schedules are sourced inputs, not T1 actor profits, T2 historical
execution, or T3 live fills. Using them in projections remains **T4**. Mutable
webpages cannot establish fees applicable at a historical block.

### Ethereum / OP Stack: receipt totals, not max fee

[OP fee documentation](https://docs.optimism.io/app-developers/transactions/fees)
states that total OP fees after Isthmus are execution + L1 data + operator fee.
Execution uses `gasUsed * (baseFee + priorityFee)`; actual effective gas price
already contains the paid priority fee. Do not add the priority fee a second time
or charge `gasLimit * maxFeePerGas` as realized spend.

The documentation distinguishes Isthmus and Jovian operator-fee formulas.
Replay the formula and parameters active at the historical block, not a static
constant. Fees for reverted included transactions still consume resources.
Dropped unsigned/unincluded requests are not automatically charged on-chain gas,
but requests can incur data/API charges and must be logged.

### Arbitrum: avoid adding the poster fee twice

[Arbitrum gas and fees](https://docs.arbitrum.io/how-arbitrum-works/gas-fees)
describes the parent-chain poster charge converted to child-chain gas units.
If the receipt already embeds that charge, add **zero** extra L1 fee with the
inclusion explicitly documented. The fetched page also distinguishes FCFS and PGA
tip collection. Do not carry an old assumption that all Arbitrum tips are ignored
into a replay without checking the chain's then-active ordering policy.
Chain-specific receipt reconciliation must prove the total paid before a T2 label.

`transaction_fee_usd` supports both representations but cannot infer one from a
chain name. Include auction payments separately only if absent from the receipt.
If native-token decimals differ from the EVM convention, pass them explicitly.

### Across: user fees are not relayer net profit

[Across fees](https://docs.across.to/introduction/fees) defines
`totalFee = inputAmount - outputAmount` and splits it into LP and relayer fees.
Repayment chain/route affects LP fees; suggested gas/capital/risk fees are a quote,
not a guarantee of an entrant's realized profit. Attribute repayment net of LP
charges to the winning filler, subtract delivered principal, execution and
replenishment costs, and mark pending repayment receivables conservatively.

The page gives an approximate settlement delay, **not a measured latency
distribution**. We do not substitute that number for replay data. Record actual
deposit, fill, repay, inventory rebalance and availability timestamps. Capital
locked until repayment cannot fill a second order or earn idle lending at the
same time. Quote time, fill time, fee rate and repayment route must be recorded.

### CEX: product, pair, tier, jurisdiction and date matter

[Kraken published fee schedule](https://www.kraken.com/features/fee-schedule),
retrieved 2026-10-29, presents the following entry-tier spot crypto and futures
rates (sourced schedule, modeled use is T4):

| Product / entry row | Maker | Taker |
| --- | ---: | ---: |
| Spot Crypto, Tier 1, $0+ qualifying volume | 0.40% | 0.80% |
| Futures, Tier 1, futures volume below $5M / $0+ spot | 0.02% | 0.05% |

Do not reuse older remembered fee schedules. The page says tier can depend on
qualifying volume or assets on platform; pair-specific stablecoin/FX, rebate and
promotional schedules differ. New entry-level orders start at applicable rates:
replay a tier improvement only after qualifying volume/asset requirements have
actually been met, never use end-of-month tier retroactively. A CEX fee quote is
not confirmation of the operator's geographic eligibility, KYC or futures access.
Every strategy that uses it must be marked **CEX required**.

Example **T4 cost arithmetic only**: at an unchanged 0.80% taker spot fee,
two $15,000 filled legs cost `2 * 15,000 * 0.008 = $240`, before spread,
withdrawals or funding. At a 0.05% futures taker fee, analogous legs cost $15.
This is not an executable round trip or assumed tier path. Maker execution is
not free certainty: use queue/adverse-selection evidence and assume lost ties.

The same page says deposit/withdrawal fees may be static, dynamic, coin-denominated
or percentage-based and points to current account quotes. We do **not** invent a
single withdrawal price. Fetch the exact intended asset/network quote later and
record the applicable minimum and freeze/settlement risk.

### Infrastructure: a ceiling is not a measured bill

[Alchemy pricing](https://www.alchemy.com/pricing), retrieved 2026-10-29, lists:

- Free tier: 30 million CU/month and 15 requests/second.
- Pay-as-you-go: $0.52 per million CU for **all** usage.
- Included PAYG capacity: 10,000 CU/second (displayed as 300 requests/second).
- Extra capacity: $160/month per 5,000 CU/second block.

Published prices are sourced inputs, modeled usage is **T4**. Do not subtract the
free plan allowance from PAYG usage or equate requests with CU: methods differ.
Historical trace/archive access, chain coverage, retention and rate limits need
verification. A free plan is not evidence of competitive latency or uptime.

[Hetzner cloud](https://www.hetzner.com/cloud) displayed different starting prices
by server class and EUR prices excluding VAT; parts of its dynamic calculator
rendered as zero. We deliberately adopt no zero-dollar server quote and no USD
conversion without a selected region/spec, current FX, storage/traffic and taxes.

Production budget equation:
`rpc CU + peak capacity + compute + storage/egress + data + monitoring <= $500`.
Report usage measurement and source per component. No subscription/purchase has
been authorized or made. Research currently uses available local tools and public
sources; this does not prove production costs or archive sufficiency.

## 4. Capital time, benchmark feasibility and liquidity

For each non-overlapping interval, account for every dollar as active inventory,
separate lending-eligible idle funds, locked receivable/bond, gas reserve, or
off-chain cash. Sum to total marked equity and track liabilities separately.
Borrow proceeds are not extra equity. Return is always on total $50,000; leverage
and gross notional are disclosed separately. Do not annualize a brief idle period
and assume perpetual reinvestment.

For a quoted constant APR `r`, income is `principal * r * days/365`.
For quoted APY `a`, it is `principal * ((1+a)^(days/365) - 1)`.
Variable indexes or actual daily history take priority over either conversion.
APY is not APR divided by twelve. Historical 30/90-day rate summaries are not
evidence that today's quote persists or that a hypothetical account earned it.

**Current net benchmark dollars remain unknown in this cost package.** Section 6
records a conditional T4 gross allocation model, not an approved net benchmark.
The yield scout
must supply source/observation time, pool/chain/asset, protocol fee treatment,
current rate, 30/90-day histories, protocol age/TVL/audit evidence, allocation,
feasible liquidity, stablecoin marks, and entry/exit cost policy. A rate directory
or unverified protocol quote alone is not T1 actor profit.

Under the user's literal chain concentration cap, `3 * 30% = 90%` maximum capital
on three chains, so **at least $5,000 remains outside those three chains** if every
dollar there is fully chain-exposed. This is feasibility arithmetic, not a
recommendation to place it with any CEX. Native gas balances count toward chain
exposure; wrapper/bridge collateral can create additional overlapping exposure.
Protocol, bridge, stablecoin and chain caps are assessed separately, not offset
against each other. Keeping $50,000 on one lending protocol is an ineligible
benchmark portfolio even if useful as a clearly labeled unconstrained comparator.
Correlated L2/L1 dependencies require red-team assessment.

## 5. Handoff and verification limits

Run focused synthetic tests:
`python3 -m unittest discover -s tests -p 'test_costs.py' -v`.
Tests verify target arithmetic, paid/reverted gas, fee inclusion, explicit unknowns,
budget enforcement, net-vs-benchmark separation, lending conversions, external
flow reconciliation, unrealized-only reporting, negative idle rates and idle
principal losses, and mutually exclusive equity/fee adapter paths.
**They do not validate strategy profitability, fills, races,
tail probabilities, live rates, or any T1/T2/T3 claim.**

Each strategy package must supply observed/replayed/paper gross PnL and cost
records with source artifacts and explicit inclusions. Tier metadata in code is a
label, not a validator or an automatic promotion. The weakest material assumption
must remain visible; an isolated T2 gas estimate cannot upgrade T4 gross income.
The independent judge owns evidence sufficiency and recommendation.

## 6. Conditional lending-baseline cost reconciliation (T4)

An independent public-data calculation at **2026-10-29T07:21:20.899Z** reproduced
the candidate allocation's historical base-rate gross return. This does **not**
establish an eligible, safe, actually invested, or net-profitable portfolio.
The input allocation and its original source records are preserved in the
[public candidate-allocation artifact](https://github.com/vaikmr/swarm-search/blob/0767bcc1cb2b01d3dfc732fc7ed3c8b9f625652f/strategies/benchmark-lending/evidence/candidate-allocation.json).
The accountant separately fetched all three public histories and reproduced
the 30-day gross to the precision shown below.
The model fixes each stablecoin's USD value, assumes continued reinvestment of
the quoted base APY, excludes reward APY, and assumes zero yield on the separate
cash sleeve. It does not model depeg/default, actual shares, deposits or fills.

Common 30-day window: **2026-09-29T06:01:03.674Z through
2026-10-29T06:01:03.674Z**. The latest known base APY is carried forward until
the next observation; the rate active at the start is the last one at/before
the start. No observation after the end is used. Gross arithmetic is:

```
sleeve_gross = 15000 * (product((1 + apyBase_i/100)^(seconds_i/31536000)) - 1)
candidate_gross = sum(sleeve_gross); conditional_net = candidate_gross - C
```

| Nominal capital sleeve | Principal | Modeled 30-day gross (T4) | Public history source |
| --- | ---: | ---: | --- |
| Aave / Ethereum / DAI | $15,000 | $40.500009 | [3665ee7e](https://yields.llama.fi/chart/3665ee7e-6c5d-49d9-abb7-c47ab5d9d4ac) |
| Compound / Arbitrum / USDT | $15,000 | $29.193998 | [85247b13](https://yields.llama.fi/chart/85247b13-8180-44e7-b38c-4d324cc68a92) |
| Morpho / Base / SparkUSDC | $15,000 | $50.206106 | [a5fab52f](https://yields.llama.fi/chart/a5fab52f-73fa-4f44-9c09-9af1eb20996c) |
| Off-chain cash, explicit zero-yield model assumption | $5,000 | $0 | User capital constraint and stated scenario assumption |
| Aggregate, before costs and price/risk effects | $50,000 | **$119.900112** | Sum of the three public-history calculations |

The three histories each yield 31 piecewise intervals in that common window.
Largest interval lengths were approximately 24.999, 24.029 and 24.068 hours,
respectively: this is daily sampled-rate integration, not continuous realized
index/share accrual or a forked-state replay. Source responses had 1,362 / 844 /
652 rows respectively. Raw response SHA-256 digests at that retrieval were:

- Aave DAI: `cb9446cb24891686e8b2b86c44d6594b7c24b752dd6263cd59b4c6168340e6cc`
- Compound USDT: `2af4da73af98f4eae1131c23f9c827f4fb296e1852f8184999121653fa5cd7a4`
- Morpho SparkUSDC: `4b7e88af0c3abe91136b6886d12525966eaba2ecbc7ac234adcbf76d71b7d126`

These hashes identify the fetched payloads, not an immutable promise that the
public API will never revise historical rates. Sources were retrieved read-only,
without account credentials or paid data.

### Explicit aggregate-cost scenarios, not observed costs

`C` below is an **assumed all-in aggregate cash-cost input for that same 30-day
window**, combining any entry, exit, claim, token conversion, gas, bridge,
withdrawal, and infrastructure costs without double-counting. None of these
inputs is an observed or estimated transaction bill. The $0 row is a hypothetical
frictionless ceiling in this fixed-price model, **not a zero-cost assumption for
the actual baseline**. Price/risk losses and taxes remain outside these scenarios.

| Assumed aggregate 30-day cash cost `C` (T4 scenario) | Conditional modeled net | Conditional return on total $50,000 |
| --- | ---: | ---: |
| $0 | $119.900112 | 0.239800224% |
| $25 | $94.900112 | 0.189800224% |
| $100 | $19.900112 | 0.039800224% |
| $500 | -$380.099888 | -0.760199776% |

The model's all-in break-even cost allowance is **$119.900112 over that window**,
before any stablecoin price change, credit loss or other omitted economic effect.
Consuming the full infrastructure ceiling alone would make this particular
modeled baseline negative, even before transaction costs. That is cost
sensitivity, not evidence that the operator would actually spend $500.

**Actual `B_net` remains unknown and no risk/compliance gate has passed.**
The nominal allocation uses different chain/protocol/token labels but DAI's
collateral can overlap USDC exposure; L2s share Ethereum dependencies; the exact
Morpho vault market/version/audit/age and exit liquidity need verification.
Gas reserves also need room inside the nominal caps. Do not treat an exact
30%-per-sleeve headline as proof of look-through compliance. Unknown cost and
price effects must not be replaced by the scenario table to clear a strategy.

## 7. Lower-deployment follow-up: much less room for costs (T4)

The subsequent [lower-deployment study](https://github.com/vaikmr/swarm-search/blob/18370d81039303e86263dc998c87164d8d75226e/strategies/benchmark-lending/lower-deployment.md)
uses **$4,000 Aave Ethereum USDC plus $46,000 off-chain reserve before costs**.
It does not certify reserve custody, full exposure compliance, audited-build
coverage, exit access or a portfolio drawdown probability. Neither the old
nominal-cap prototype nor this lower-deployment variant is a recommendation.

The accountant independently integrated the [preserved USDC rate history](https://github.com/vaikmr/swarm-search/blob/18370d81039303e86263dc998c87164d8d75226e/strategies/benchmark-lending/evidence/aave-ethereum-usdc-history.json),
whose public source is [pool aa70268e](https://yields.llama.fi/chart/aa70268e-4b52-42bf-a116-608b370f9501).
With the same piecewise base-APY formula as section 6, $4,000 principal,
reinvestment, fixed $1 USDC marks, zero modeled reserve income and no expenses:

- **30-day modeled gross: $12.581271**, window
  2026-09-29T06:01:03.674Z to 2026-10-29T06:01:03.674Z, 31 rate intervals.
- **90-day modeled gross: $35.178977**, window
  2026-07-31T06:01:03.674Z to 2026-10-29T06:01:03.674Z, 91 rate intervals.

Both are **T4 archived-rate arithmetic**, not T1 realized profit, T2 execution,
or T3 paper fills. They match the [source sensitivity artifact](https://github.com/vaikmr/swarm-search/blob/18370d81039303e86263dc998c87164d8d75226e/strategies/benchmark-lending/evidence/lower-deployment-sensitivity.json).
Actual reserve income and economic risk remain unknown, not observed zero.

| Assumed aggregate 30-day cost (T4 sensitivity only) | Conditional modeled economic net, reserve income fixed at zero |
| --- | ---: |
| $0 | $12.581271 |
| $5 | $7.581271 |
| $10 | $2.581271 |
| $25 | -$12.418729 |
| $100 | -$87.418729 |
| $500 | -$487.418729 |

The cost allowance for a nonnegative result in this specific fixed-price model
is only **$12.581271 over 30 days**. This does not establish an achievable
operating budget: no entry/exit gas bill, failed-attempt cost, infrastructure
invoice or adverse-unwind ceiling has been observed or bounded here.
The hypothetical $500 all-in ceiling used in component stress examples is not
the user-specified infrastructure ceiling and is not evidence of an actual cap.
The API's `infrastructure_within_budget` flag tests the infrastructure line only.
It must not be reused to certify total costs, opening-capital loss envelopes,
pathwise maximum drawdown, annual tails or confidence levels.

**Actual net remains unknown.** Lower deployment reduces the amount exposed to
the on-chain sleeve in specified scenarios, but leaves reserve concentration,
custody/access/FX risks and missing cost evidence unresolved. Any off-chain
income must be independently evidenced and reconciled, not assumed or omitted.

## 8. Actual holder receipts: independently checked partial costs, not T1

The scout's [actual holder ledger](https://github.com/vaikmr/swarm-search/blob/cd38c61b47ee55e3a3f1b9f9aeb892a4a2171a77/strategies/benchmark-lending/actor-ledger.md)
preserves [observations](https://github.com/vaikmr/swarm-search/blob/cd38c61b47ee55e3a3f1b9f9aeb892a4a2171a77/strategies/benchmark-lending/evidence/actor-observations.json)
and a [reconciliation](https://github.com/vaikmr/swarm-search/blob/cd38c61b47ee55e3a3f1b9f9aeb892a4a2171a77/strategies/benchmark-lending/evidence/actor-reconciliation.json).
Its window is blocks 26,196,084–26,296,884, 2026-10-15T06:20:59Z to
2026-10-29T07:24:59Z, or 14.044444 days. This is one public address with roughly
$134 million in the selected lending position, not a $50,000 strategy.

The accountant performed a separate offline calculation directly from the
preserved observations, without importing the scout's reconciler:

- Identified all **39 actor-sent receipts** independently from receipt senders
  and matched their transaction IDs to the normal-transaction list. All 39
  were type-2, successful transactions; no failed-attempt fee was observed in
  this preserved sender sample. Other senders' expenses were not assigned to
  this address.
- Summed actual `gasUsed * effectiveGasPrice`, checked that observed receipts
  had no blob-fee component, and reproduced **334,130,451,297,696 wei =
  0.000334130451297696 ETH**. Using preserved transaction-block ETH oracle marks
  gives **$0.79976342890542135972220161**, not an executable USD conversion.
- Matched all **126 unique selected token logs** to preserved receipt token,
  transaction/block identity, topics, parties, values and log indices, and
  confirmed the logs were not marked removed.
- Independently recomputed external versus internal token flows, verified
  **zero raw USDC and native-ETH residuals**, and checked both endpoint indexed
  aToken balances using integer floor multiplication.
- Reproduced **194,463.135111 USDC units** of post-opening position accrual and
  **$173,641.32936046476502656973587238** of flow-adjusted, oracle-marked change
  in the selected USDC/aUSDC/native-ETH components.

These checks validate arithmetic and internal consistency of the **archived
sample**. They are not an independent live RPC re-fetch, proof that an indexer
omitted no transactions, full-actor accounting, owner/strategy attribution,
fork execution, forward-paper observation or T1 qualification.

**No double fee deduction:** the selected-component marked change already
includes paid gas through native-ETH balances. Add the unallocated stable
component ($173,669.99458170140272) to the native component
(-$28.66522123663769343026412762). Do not instead add a stable component with
gas deducted to that same fee-inclusive native component. The report's
alternative stable-only fee allocation is not a second wallet expense.

**Keep full net unknown.** Infrastructure, custody, other assets/liabilities,
off-address accounts and USD realization remain unresolved. Closed-position
cash-interest units are not full realized USD profit or a known lifetime/tax
basis. Neither the large holder's dollars nor its observed $0.80 network bill
can be linearly transferred to the proposed capital, fee environment or
deployment plan. This observation does not replace section 7's missing
strategy-specific all-in costs, reserve evidence or risk gates.
