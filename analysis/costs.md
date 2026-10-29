# Canonical cost and capital-opportunity-cost model

Status: Stage 0/1 accounting specification, **T4 model, not an attainable-return
claim**. Public fee documentation was retrieved on 2026-10-29. No live transaction
was signed or sent, paid service purchased, or seven-day paper run completed.
The module is pure arithmetic, dependency-free, and has no networking/signing.

## 1. What the target requires, not what a strategy can earn

User-specified total capital `C = $50,000`; desired net monthly profit `N`:

```
required simple monthly total-capital net return = N / C
required gross contribution = N + actual cash costs - separate idle income
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
G = earned fees + realized trading PnL + inventory/hedge mark-to-market
    + funding received + actually earned/redeemable rewards and rebates
N = G + Y_idle - sum(cash costs not already included in G)
R_total = N / 50,000
E = N - B_net
```

`Y_idle` is income actually earned on separate, eligible idle funds, not yield
assumed on locked relayer receivables, gas reserves, hedge collateral, bonds, or
all cash irrespective of deployment. A counterfactual lending return belongs in
`B_net`, not in `Y_idle`. Funding paid is a cost. If gross uses **net** funding,
flag funding paid as already included. Do likewise for rebates and trading fees.

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

**Current benchmark dollars remain unknown in this cost package.** The yield scout
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
budget enforcement, net-vs-benchmark separation, lending conversions, and external
flow reconciliation. **They do not validate strategy profitability, fills, races,
tail probabilities, live rates, or any T1/T2/T3 claim.**

Each strategy package must supply observed/replayed/paper gross PnL and cost
records with source artifacts and explicit inclusions. Tier metadata in code is a
label, not a validator or an automatic promotion. The weakest material assumption
must remain visible; an isolated T2 gas estimate cannot upgrade T4 gross income.
The independent judge owns evidence sufficiency and recommendation.
