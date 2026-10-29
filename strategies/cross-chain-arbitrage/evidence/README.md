# Source register

Retrieved 2026-10-29:

- https://arxiv.org/html/2501.17335v2
  Discovery of actors and example transaction URLs only. Published statistics and
  return numbers are not reproduced or promoted to T1/T2.
- https://basescan.org/tx/0xeb546c545453b6b1ecc6ebf8ad694d4b4dafcc208c330cc505f10b4954037f7c
- https://arbiscan.io/tx/0xffefbd860c0b9a3219c8961a5566b995ed29286683c146fcc13851856c3aa7aa
  The explorer links were supplied by the paper. Their successful receipts and
  canonical block timestamps were independently fetched via the official Base
  and Arbitrum public RPCs; selected responses are retained next to this file.
  Token flows and economic classification remain unverified.

Blockscout Base address-history GETs attempted in this session returned HTTP 403.
This is a concrete access blocker for that provider, not proof that other public
RPC/history sources are inaccessible.

Official RPC alternatives succeeded. Reproduce the fixed read-only receipt
probes using `python3 strategies/intent-solvers/evidence/verify_public_receipts.py`
from the repository root. A publicnode Base probe also returned HTTP 403; that
does not invalidate the successful official Base receipt reads.
