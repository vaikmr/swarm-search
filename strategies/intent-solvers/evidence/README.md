# Source register and access limitations

Retrieved 2026-10-29:

- https://docs.cow.fi/cow-protocol/reference/core/auctions/bonding-pools
- https://docs.cow.fi/cow-protocol/tutorials/solvers/onboard
- https://docs.cow.fi/cow-protocol/reference/core/auctions/accounting
- https://explorer.cow.fi/solvers?solver=tsolver
- https://developers.uniswap.org/docs/liquidity/uniswapx/filling/overview
- https://business.1inch.com/portal/assets/legal-docs/resolvers/terms-of_use_resolvers_20260814.pdf
- https://help.1inch.com/en/articles/6796085-what-is-1inch-fusion-and-how-does-it-work

[`snapshot-uniswapx-base.json`](snapshot-uniswapx-base.json) is selected public
order data from the exact URL recorded inside. Signatures/encoded orders are not
retained. It is a bounded discovery sample, not T1/T2/T3 or an unbiased measure
of market share.

Concrete failed probes:

- `https://api.cow.fi/mainnet/api/v1/solver_competition/latest`: HTTP 404.
- Equivalent Base route: HTTP 404. These guessed routes are not claimed to be
  documented supported endpoints; use documented transaction/auction routes next.
- Base Blockscout actor transaction-history API: HTTP 403 for both sampled actor
  addresses. This blocks that provider route, not all public history access.

No complete CoW rewards export, actual UniswapX executor attribution, 1inch
whitelist state, or realized actor PnL has been established.

Official Base RPC receipt/block reads succeeded. `receipt-base.json` independently
verifies a recent fill's actual sender and recipient. The source RPC, method,
transaction hash, retrieval time, response digests and block timestamp are
retained. Reproduce with
`python3 strategies/intent-solvers/evidence/verify_public_receipts.py`.
This script can only read receipts and blocks; it does not submit transactions.
