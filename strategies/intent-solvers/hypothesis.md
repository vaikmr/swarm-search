# Intent auction solvers / fillers

Stage: discovery only. Status: **unverified**. No qualifying T1/T2/T3.
The entry-route constraints below are documentary facts, not returns.

## CoW Protocol

[Self-bonding documentation](https://docs.cow.fi/cow-protocol/reference/core/auctions/bonding-pools)
requires **$500,000** in eligible assets plus **1,500,000 COW** for a standalone
pool. A reduced arrangement starts at **$50,000** plus **500,000 COW**, subject to
approval, then grows. Both exceed this study's **$50,000** total budget and
single-protocol concentration limit. These particular self-funded entry routes
fail capital feasibility; that does **not** prove all CoW entry routes infeasible.

[DAO-sponsored onboarding](https://docs.cow.fi/cow-protocol/tutorials/solvers/onboard)
has company/shareholder KYC, onboarding approval, rewards restrictions and fees.
The current page starts sponsored entrants on BNB before other networks. This
is an admission and route-selection caveat, not permission to bypass the user's
BSC builder-dominated-arbitrage exclusion. The shadow environment is the appropriate
paper-only lead; staging is on-chain and must not be run under this study.

The [official solver directory](https://explorer.cow.fi/solvers) displayed
**46 entries** on retrieval. This directory count includes different environments,
statuses and chains; it is not **46 active competitors in one auction**.
The [Tsolver detail](https://explorer.cow.fi/solvers?solver=tsolver) maps the public
production submission address
`0x3980daa7eaad0b7e0c53cfc5c2760037270da54d` across Ethereum/Base/Arbitrum.
Rewards-address mapping and net economics still need reconciliation.
The onboarding page links https://dune.com/queries/5270914 for per-auction rewards.

## UniswapX

[Official filler overview](https://developers.uniswap.org/docs/liquidity/uniswapx/filling/overview)
distinguishes permissioned RFQ quoters from permissionless non-exclusive fillers.
The latter may fill after exclusivity or via the applicable soft-exclusivity
override. Open entry does not imply equal access to profitable flow.
The same docs now describe exclusive Dutch auctions on supported chains; do not
assume the previous priority-auction design is still current.

The public filled-orders endpoint worked for Base. The discovery sample contains
**20 filled orders**, with exclusive-filler nominees including
`0x225a38bc71102999dd13478bfabd7c4d53f2dc17` and
`0xbeef02961503351625926ea9a11ae13b29f5c555`.
**A nominee is not proof of actual executor.** The sample includes order hashes,
transaction hashes and settled token amounts, but no realized actor PnL.

An independent Base RPC receipt for
[`0xaa537f7fb7a50603ccfcfda470b9a746782b9df5e46f43ce69b070ab7868191d`](https://basescan.org/tx/0xaa537f7fb7a50603ccfcfda470b9a746782b9df5e46f43ce69b070ab7868191d)
confirms successful execution at **2026-10-29 07:13:33 UTC** with sender
`0x9caa8ba93c518d88bdd1383c4c258300e3ce78b9` calling
`0x225a38bc71102999dd13478bfabd7c4d53f2dc17`. This verifies one
transaction's sender/recipient roles, not legal ownership or independent firms.
Do not count the caller and filler contract as two competitors.

## 1inch Fusion / Fusion+

[August 2026 resolver terms](https://business.1inch.com/portal/assets/legal-docs/resolvers/terms-of_use_resolvers_20260814.pdf)
describe compliance and a whitelist eligibility threshold of **5%** of total
network Unicorn Power with a maximum **10** whitelisted resolvers. Delegations
can supply power; do not invent a fixed USD bond or infer impossibility solely
from total supply. Access and ongoing eligibility remain unverified.
[Official help](https://help.1inch.com/en/articles/6796085-what-is-1inch-fusion-and-how-does-it-work)
corroborates the staking/delegation requirements.
No off-chain API credential or Access NFT was acquired.

## Next gate

Reconcile actual winners, reward address distributions, gas reimbursement,
slippage accounting, reward locks, governance-token marks, and any co-funded
bond before computing PnL. Account for non-winners without assuming new-entrant
fills at incumbent prices. Confirm every chain/protocol's eligibility. Current
public UniswapX filler documentation does not itself establish cross-chain
execution support; keep same-chain solver evidence separate from bridge relaying.
