# Inventory-based cross-chain DEX arbitrage

Stage: discovery only. Status: **unverified**. No qualifying T1/T2/T3.

## Hypothesis

Pre-positioned inventory can avoid hot-path bridging, but both legs are non-atomic.
The relevant edge is an executable residual spread after latency, all rebalancing
costs and inventory mark-to-market, not a difference between quoted spot prices.

## Public actor leads

[Cross-Chain Arbitrage: The Next Frontier of MEV](https://arxiv.org/html/2501.17335v2#A2)
provides concrete transaction leads and a full actor-address table. These are
**paper leads only**; its published return numbers are not adopted as evidence.
The paper itself states that inventory risk is not priced into its arbitrage profits.

- Actor `0x4cb6f0ef0eeb503f8065af1a6e6d5dd46197d3d9`.
  Example Base transaction:
  [0xeb546c545453b6b1ecc6ebf8ad694d4b4dafcc208c330cc505f10b4954037f7c](https://basescan.org/tx/0xeb546c545453b6b1ecc6ebf8ad694d4b4dafcc208c330cc505f10b4954037f7c).
  Related Arbitrum example:
  [0xffefbd860c0b9a3219c8961a5566b995ed29286683c146fcc13851856c3aa7aa](https://arbiscan.io/tx/0xffefbd860c0b9a3219c8961a5566b995ed29286683c146fcc13851856c3aa7aa).
- `0xca74f404e0c7bfa35b13b511097df966d5a65597` is another publicly
  enumerated actor. A paper case study uses borrowing plus bridge rebalancing;
  do not automatically classify all its activity as unleveraged inventory arb.
- `0xa311f7ca3eb2fb98123a807f9b8e4bbbdbdcb2ee` is a contract lead,
  not an identified operator or demonstrated newcomer edge.

## Missing evidence

Two example transaction receipts and their block timestamps were independently
retrieved from the official Base and Arbitrum RPCs. Both succeeded and have the
same sender, `0x4cb6f0ef0eeb503f8065af1a6e6d5dd46197d3d9`.
Their canonical timestamps are **2023-12-24 00:25:51 UTC** on Base and
**00:26:18 UTC** on Arbitrum, a historical example, not current operation.
See [`receipt-base-example.json`](evidence/receipt-base-example.json) and
[`receipt-arbitrum-example.json`](evidence/receipt-arbitrum-example.json).
This validates the transaction pointers, not arbitrage classification or PnL.

No complete token-flow reconciliation, actor capital ledger, complete
rebalancing costs, losing legs, competitor race history or legal-owner attribution
has been established. No claim of profitable actors, active competitor count or
attainable monthly return is made from the paper.

## Next gate

Replay a narrowly defined non-BSC L2 route with historical transaction receipts and
token inventories. Include hedging/borrow costs where applicable; do not smuggle
directional inventory exposure into a delta-neutral label. Test actual competing
execution deadlines and lose every unknown race. Chain, bridge, protocol and
stablecoin exposures must independently respect the capital limits. Protocol
eligibility still needs evidence. No fork or historical simulation is included here.
