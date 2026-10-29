# Seven user-supplied candidates: pressure-test specification

Added 2026-10-29 during the same discovery pass. These are **hypotheses**, not established profits, academic novelty or recommendations. The user-reported abbreviated actors, 21-trade sample and loss estimates are not assumed to be our existing dataset.

| Candidate | Proposed economic mechanism | Decisive pressure test | Owner |
| --- | --- | --- | --- |
| 1. Perp-hedged bridge arbitrage | Capture a cross-chain spot basis while a matched short reduces common market-price movement during transit | Exact historical token/claim and perp availability, executable entry/exit prices/depth, funding, margin, basis, bridge risk and full capital/cost accounting | Empirical + onchain |
| 2. Tokenized-stock dislocation | Trade differences between issuer/chain representations and a matched equity derivative | Actual deployed markets, transfer/access rights, underlying/currency/dividends/corporate actions, redemption eligibility and whether convergence is enforceable | Instruments |
| 3. Stablecoin-variant convergence | Buy a discount and realize it through a specifically valid conversion/redemption rail | Exact accepted contracts and domains, native versus bridge-backed claims, permission/access, caps, waiting, costs and residual issuer/bridge risk | Economics |
| 4. New-deployment dislocations | Correct public post-deployment pool mispricing across equivalent token representations | Actual economic equivalence, liquid executable pools, transfer/sell restrictions and recurring net edge; no front-running users or launch-sniping tactics | Literature |
| 5. Lawful liquidation / information differences | Assess ordinary protocol-permitted liquidation with a collateral hedge | Eligibility, incentives, fees and hedge risk; exclude stale-oracle exploitation, oracle manipulation, front-running and vulnerable-target discovery | Durability |
| 6. Inventory-aware intent filling | Earn incremental value when filling legitimate demand also performs a needed inventory move | Compare the same fills and ending inventories with ordinary filling plus independent rebalancing; no double counting or reuse of locked principal | Settlement |
| 7. LST/LRT discount and redemption | Capture a discount against an economically realizable redemption path | Exact claims, wrapping/bridging, queues, slashing/default risk, costs and ETH-versus-USD exposure; an ETH claim is not automatically USD-hedged | Independent audit |

## Priority counterfactual: inputs before arithmetic

The reported losing day refers to abbreviated `0xEf6c`, 21 trades, GNO/ZGAP/DOS and roughly minus $13. Exact address, chains, UTC date, transactions, token contracts, executed quantities and historical hedge markets must be recovered before the proposed replay can be identified.

The seed paper has a **different** loan-backed `0xCA74` example. Its paper-linked six-transaction cycle is not a substitute for the losing-day dataset. Absence from our current files is a recovery gap, not proof the reported events never occurred.

A valid small counterfactual must account for prices executable at each original decision time and size, historical instrument existence, financing/margin, both spot and hedge legs, funding, gas/bridge costs and pathwise liquidation/basis exposure. It cannot simply subtract observed transit drift from losses or assume the winners stay unchanged. No 30-day expansion or live orders are authorized.

## Initial source leads from the user

- [Third-party perp venue comparison](https://renesis.fi/articles/best-perp-dex): not authoritative historical market-specific fees.
- [The Price of Interoperability](https://arxiv.org/abs/2604.03083): submitted April 3, 2026; abstract describes 2022–25 bridge data, not today's executable token route quotes.
- [SSRN 7161018](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7161018): identity/content and issuer-term relevance still require verification.

Generic bridge-fee/latency medians, a flat taker fee, a hard 1:1 conversion for every dollar variant, universal availability of stock-token redemption, and automatic USD neutrality of LST/LRTs are not accepted premises.

## New concrete hooks, not proved strategies

- [Across fee documentation](https://docs.across.to/introduction/fees) specifies zero LP fee for origin-chain repayment while separately describing relayer gas, capital lock and risk. This supports a testable inventory/repayment design, not free total execution or entrant profit.
- [Circle's October 23, 2026 Gateway announcement](https://www.circle.com/blog/circle-gateway-now-supports-cirbtc-and-eurc) describes new EURC/cirBTC balances, supported networks and conditional post-finalization access. It creates an inventory-rebalancing hypothesis; no spread has been observed here. Its generic USDC-only legal text conflicts with the expanded-asset body and requires asset-specific terms verification.
- [Circle Credit API documentation](https://developers.circle.com/circle-mint/concepts/credit-api) describes settlement/redemption advances, but requires a core agreement, separate credit contract and account entitlement. This is a real financing mechanism, not established access for a $50k entrant or proof of a profitable trade.

These are inputs to the opportunity map. Deployed infrastructure, a lower fee or a documented credit line alone does not establish an accessible profitable strategy.
