#!/usr/bin/env python3
"""Fixed-block, public, read-only identity evidence; no transaction methods."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess

RPC = "https://ethereum-rpc.publicnode.com"
BLOCK = "0x1914234"
BOOK_COMMIT = "73676d409a24eb33d04687f28287f23a40f2afd9"
BOOK_URL = f"https://raw.githubusercontent.com/aave-dao/aave-address-book/{BOOK_COMMIT}/src/AaveV3Ethereum.sol"
POOL = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
ATOKEN = "0x98C23E9d8f34FEFb1B7BD6a91B7FF122F4e16F5c"
SLOT = "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"


def request(url, body=None):
    args = ["curl", "--fail", "-sS", "--max-time", "60", url]
    if body is not None:
        args += ["-H", "Content-Type: application/json", "--data", json.dumps(body)]
    return subprocess.check_output(args)


def main():
    observed = dt.datetime.now(dt.timezone.utc).isoformat()
    book = request(BOOK_URL)
    text = book.decode()
    for address in (POOL, USDC, ATOKEN):
        if address.lower() not in text.lower():
            raise ValueError("Expected address missing from pinned official registry")
    expected = re.search(r"POOL_IMPL\s*=\s*(0x[0-9A-Fa-f]{40})", text).group(1)
    calls = [
        {"jsonrpc": "2.0", "id": 1, "method": "eth_chainId", "params": []},
        {"jsonrpc": "2.0", "id": 2, "method": "eth_getBlockByNumber", "params": [BLOCK, False]},
        {"jsonrpc": "2.0", "id": 3, "method": "eth_getStorageAt", "params": [POOL, SLOT, BLOCK]},
        {"jsonrpc": "2.0", "id": 4, "method": "eth_call", "params": [
            {"to": USDC, "data": "0x70a08231" + ATOKEN[2:].lower().rjust(64, "0")}, BLOCK
        ]},
    ]
    raw = request(RPC, calls)
    response = {r["id"]: r for r in json.loads(raw)}
    if any("result" not in response.get(i, {}) for i in range(1, 5)):
        raise ValueError("Incomplete read-only RPC evidence")
    if int(response[1]["result"], 16) != 1:
        raise ValueError("Unexpected chain")
    block = response[2]["result"]
    actual = "0x" + response[3]["result"][-40:]
    if actual.lower() != expected.lower():
        raise ValueError("Official registry and fixed-block implementation differ")
    explorer_url = "https://eth.blockscout.com/api/v2/smart-contracts/" + actual
    source_raw = request(explorer_url)
    source = json.loads(source_raw)
    result = {
        "observed_at": observed, "tier": "deployment identity observation, not performance",
        "registry": {"source": BOOK_URL, "commit": BOOK_COMMIT, "sha256": hashlib.sha256(book).hexdigest()},
        "rpc": {"source": RPC, "request": calls, "response_sha256": hashlib.sha256(raw).hexdigest(),
                "chain_id": 1, "block": int(BLOCK, 16), "block_hash": block["hash"],
                "block_time": dt.datetime.fromtimestamp(int(block["timestamp"], 16), dt.timezone.utc).isoformat()},
        "pool": POOL, "underlying": USDC, "a_token": ATOKEN,
        "implementation": actual, "registry_implementation_match": True,
        "usdc_balance_at_a_token": int(response[4]["result"], 16) / 10**6,
        "liquidity_warning": "Point-in-time token inventory, not reserved exit capacity or a withdrawal guarantee",
        "explorer": {"source": explorer_url, "response_sha256": hashlib.sha256(source_raw).hexdigest(),
                     "name": source.get("name"), "is_verified": source.get("is_verified"),
                     "verified_at": source.get("verified_at"),
                     "source_sha256": hashlib.sha256(source.get("source_code", "").encode()).hexdigest()},
        "activation": {"source": "https://governance-v2.aave.com/governance/proposal/147",
                       "executed_date": "2023-01-27", "usdc_explicitly_in_initial_listing": True,
                       "basis": "Manually read official executed proposal; not a fresh contract creation proof"},
        "audit": {"source": "https://aave.com/security",
                  "public_protocol_audits_exist": True,
                  "exact_deployed_implementation_to_audited_build_equivalence": None},
        "warnings": ["No protocol safety or portfolio compliance certification",
                     "No transaction, signer, private credential, or paid service",
                     "urllib RPC returned403; ordinary public curl succeeded"],
    }
    path = Path("strategies/benchmark-lending/evidence/aave-usdc-deployment-identity.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print("Matched mainnet block", result["rpc"]["block"], "implementation", actual,
          "USDC token inventory", result["usdc_balance_at_a_token"])


if __name__ == "__main__":
    main()
