"""Verify fixed discovery transaction pointers using public read-only JSON-RPC.

There is no CLI parameter for an RPC method or transaction data. Nothing signs,
submits, simulates a live fill, or reads an account's private exchange records.
"""

import concurrent.futures
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

JOBS = [
    {
        "name": "across-optimism",
        "rpc_url": "https://mainnet.optimism.io",
        "transaction_hash": "0xe1c03f2fef3f72891fa4623fd20ec10705f88d77c76e45f35e8babe6554e958e",
        "output": "strategies/cross-chain-relaying/evidence/receipt-optimism.json",
    },
    {
        "name": "uniswapx-base",
        "rpc_url": "https://mainnet.base.org",
        "transaction_hash": "0xaa537f7fb7a50603ccfcfda470b9a746782b9df5e46f43ce69b070ab7868191d",
        "output": "strategies/intent-solvers/evidence/receipt-base.json",
    },
    {
        "name": "historical-arbitrage-base",
        "rpc_url": "https://mainnet.base.org",
        "transaction_hash": "0xeb546c545453b6b1ecc6ebf8ad694d4b4dafcc208c330cc505f10b4954037f7c",
        "output": "strategies/cross-chain-arbitrage/evidence/receipt-base-example.json",
    },
    {
        "name": "historical-arbitrage-arbitrum",
        "rpc_url": "https://arb1.arbitrum.io/rpc",
        "transaction_hash": "0xffefbd860c0b9a3219c8961a5566b995ed29286683c146fcc13851856c3aa7aa",
        "output": "strategies/cross-chain-arbitrage/evidence/receipt-arbitrum-example.json",
    },
]
RECEIPT_FIELDS = (
    "transactionHash", "blockNumber", "blockHash", "from", "to", "status",
    "gasUsed", "effectiveGasPrice", "l1Fee", "l1GasUsed", "l1GasPrice",
    "l1FeeScalar", "gasUsedForL1",
)


def rpc_read(url, method, params):
    if method not in {"eth_getTransactionReceipt", "eth_getBlockByNumber"}:
        raise ValueError("Only fixed read-only RPC methods are supported")
    payload = json.dumps(
        {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    ).encode()
    req = Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "User-Agent": "swarm-search-public-research/1.0",
    })
    with urlopen(req, timeout=30) as response:
        raw = response.read(1_000_001)
        if len(raw) > 1_000_000:
            raise ValueError("Read response exceeded discovery limit")
        server_date = response.headers.get("Date")
    body = json.loads(raw)
    if "error" in body or body.get("result") is None:
        raise ValueError(f"RPC returned no usable result: {body}")
    return body["result"], hashlib.sha256(raw).hexdigest(), server_date


def verify(job):
    result = {
        "source_url": job["rpc_url"],
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "receipt_method": "eth_getTransactionReceipt",
        "transaction_hash": job["transaction_hash"],
        "evidence_kind": "public_receipt_discovery_not_actor_pnl",
        "qualifies_t1": False, "realized_pnl_usd": None,
    }
    try:
        receipt, digest, date = rpc_read(
            job["rpc_url"], "eth_getTransactionReceipt", [job["transaction_hash"]]
        )
        result["selected_receipt"] = {
            field: receipt.get(field) for field in RECEIPT_FIELDS
        }
        result["receipt_response_sha256"] = digest
        result["server_date"] = date
        block, block_digest, _ = rpc_read(
            job["rpc_url"], "eth_getBlockByNumber", [receipt["blockNumber"], False]
        )
        result["block_response_sha256"] = block_digest
        result["block_timestamp_unix"] = int(block["timestamp"], 16)
        result["block_timestamp_utc"] = datetime.fromtimestamp(
            result["block_timestamp_unix"], timezone.utc
        ).isoformat()
        result["block_hash_matches_receipt"] = block["hash"] == receipt["blockHash"]
        result["ok"] = True
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError) as exc:
        result["ok"] = False
        result["error"] = f"{type(exc).__name__}: {exc}"
    path = Path(job["output"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n")
    return {"name": job["name"], **result}


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for output in pool.map(verify, JOBS):
            print(json.dumps(output))
