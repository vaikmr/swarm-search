"""Bounded public, credential-free historical RPC prerequisite probe. NOT T2.

Read-only methods only, hard limit 12 JSON-RPC requests, no retries, no signer,
no deployment, no state-changing RPC, no dependency installation.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any


RPC_URL = "https://ethereum-rpc.publicnode.com"
DRPC_URL = "https://eth.drpc.org"
REGISTRY_URL = (
    "https://raw.githubusercontent.com/aave-dao/aave-address-book/"
    "73676d409a24eb33d04687f28287f23a40f2afd9/src/AaveV3Ethereum.sol"
)
OLD_BLOCK = 21_000_000
OLD_TIMESTAMP = 1_729_345_547  # Explorer reference; verify from returned block header.
RECENT_BLOCK = 26_296_884
RECENT_HASH = "0x534506ea07ed9fef6d016fb370ea548ff8554e3f33241f481e0ec84de4c08f30"
POOL = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
ATOKEN = "0x98C23E9d8f34FEFb1B7BD6a91B7FF122F4e16F5c"
IMPL_SLOT = "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"
ALLOWED_METHODS = frozenset({
    "eth_chainId", "eth_getBlockByNumber", "eth_getTransactionReceipt",
    "eth_getCode", "eth_getStorageAt", "eth_call",
})
MAX_READS = 12


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def curl_json(url: str, payload: Any | None = None) -> dict[str, Any]:
    """Use ordinary curl: provider may reject Python urllib's default transport/UA."""
    command = ["curl", "--silent", "--show-error", "--connect-timeout", "10",
               "--max-time", "20", "--write-out", "\n%{http_code}"]
    if payload is not None:
        command += ["--header", "Content-Type: application/json", "--data", json.dumps(payload)]
    command.append(url)
    response = subprocess.run(command, capture_output=True, text=True, timeout=25, check=False)
    raw, _, status = response.stdout.rpartition("\n")
    result: dict[str, Any] = {
        "http_status": int(status) if status.isdigit() else None,
        "curl_exit_code": response.returncode,
        "response_sha256": hashlib.sha256(raw.encode()).hexdigest(),
        "response_body_text": raw,
    }
    try:
        result["body"] = json.loads(raw)
    except json.JSONDecodeError:
        # Public responses only. Do not echo environment configuration or credentials.
        result["body"] = None
        result["non_json_excerpt"] = raw[:300]
    return result


class ProbeClient:
    def __init__(self, *, endpoint: str = RPC_URL, max_reads: int = MAX_READS) -> None:
        if endpoint not in {RPC_URL, DRPC_URL}:
            raise ValueError("only fixed credential-free public endpoints allowed")
        if type(max_reads) is not int or not 1 <= max_reads <= MAX_READS:
            raise ValueError("read budget must be an integer between 1 and 12")
        self.endpoint = endpoint
        self.max_reads = max_reads
        self.records: list[dict[str, Any]] = []

    def call(self, method: str, params: list[Any]) -> Any:
        if method not in ALLOWED_METHODS:
            raise ValueError("non-allowlisted RPC method prohibited")
        if len(self.records) >= self.max_reads:
            raise ValueError("probe budget exhausted")
        request = {"jsonrpc": "2.0", "id": len(self.records) + 1,
                   "method": method, "params": params}
        record: dict[str, Any] = {"requested_at": utc_now(), "request": request}
        # Reserve budget before a transport attempt, including failures.
        self.records.append(record)
        try:
            record.update(curl_json(self.endpoint, request))
        except (OSError, subprocess.TimeoutExpired):
            record.update({"http_status": None, "transport_error": "curl unavailable or timed out"})
        record["completed_at"] = utc_now()
        body = record.get("body")
        if (record.get("http_status") == 200 and isinstance(body, dict)
                and body.get("id") == request["id"] and "error" not in body):
            return body.get("result")
        return None


def verify_registry() -> dict[str, Any]:
    command = ["curl", "--silent", "--show-error", "--fail",
               "--connect-timeout", "10", "--max-time", "20", REGISTRY_URL]
    response = subprocess.run(command, capture_output=True, timeout=25, check=False)
    raw = response.stdout
    source = raw.decode("utf-8", errors="replace")
    wanted = (POOL, USDC, ATOKEN)
    matches = {address: address.lower() in source.lower() for address in wanted}
    lines = [line.strip() for line in source.splitlines()
             if any(address.lower() in line.lower() for address in wanted)]
    return {
        "url": REGISTRY_URL, "retrieved_at": utc_now(),
        "curl_exit_code": response.returncode,
        "full_response_sha256": hashlib.sha256(raw).hexdigest(),
        "addresses_present": matches, "selected_source_lines": lines,
        "identity_scope": "Official registry as of pinned commit; not historical implementation proof.",
    }


def tool_availability() -> dict[str, bool]:
    return {tool: shutil.which(tool) is not None
            for tool in ("anvil", "cast", "forge", "revm", "geth", "reth",
                         "node", "python3", "curl", "docker")}


def probe() -> dict[str, Any]:
    output: dict[str, Any] = {
        "started_at": utc_now(), "paper_only": True, "evidence_class": "access_prerequisite_only",
        "is_t2_evidence": False, "completed_fork_replay": False, "fork_started": False,
        "endpoint": RPC_URL, "rpc_read_budget": MAX_READS, "tools": tool_availability(),
        "references": {
            "historical_block": "https://etherscan.io/block/21000000",
            "provider_endpoint": "https://ethereum.publicnode.com",
            "implementation_slot": "https://eips.ethereum.org/EIPS/eip-1967",
            "erc20_view_semantics": "https://eips.ethereum.org/EIPS/eip-20",
            "recent_identity": "https://github.com/vaikmr/swarm-search/blob/"
            "18370d81039303e86263dc998c87164d8d75226e/"
            "strategies/benchmark-lending/evidence/aave-usdc-deployment-identity.json",
        },
        "limits": [
            "Access check only: no strategy return/cost/competition or T1/T2/T3 performance evidence.",
            "Registry identity is current to its pinned commit, not historical build or configuration equivalence.",
            "A successful historical receipt/header alone does not establish historical account state.",
            "Historical code/storage/call access is not proof all lazy fork dependencies are available.",
            "No local fork, local EVM execution, historical strategy execution or transaction was attempted.",
            "Recent state is a fixed dated block, not a claim about continuously current balances.",
            "Token supply/balance is not PnL, protocol withdrawal capacity, or risk qualification.",
        ],
    }
    client = ProbeClient()
    output["rpc_records"] = client.records
    try:
        output["registry"] = verify_registry()
        if (output["registry"]["curl_exit_code"] != 0
                or not all(output["registry"]["addresses_present"].values())):
            output["blocker"] = "official pinned registry identity could not be verified"
            return output
        chain = client.call("eth_chainId", [])
        old = client.call("eth_getBlockByNumber", [hex(OLD_BLOCK), False])
        recent = client.call("eth_getBlockByNumber", [hex(RECENT_BLOCK), False])
        output["block_identity"] = {
            "chain_id_is_ethereum": chain == "0x1",
            "old_number_timestamp_match_reference": isinstance(old, dict)
            and old.get("number") == hex(OLD_BLOCK) and old.get("timestamp") == hex(OLD_TIMESTAMP),
            "recent_number_hash_match_scout": isinstance(recent, dict)
            and recent.get("number") == hex(RECENT_BLOCK) and recent.get("hash") == RECENT_HASH,
        }
        if not all(output["block_identity"].values()):
            output["blocker"] = "chain or dated block identity failed; no state claims accepted"
            return output
        old_tag, recent_tag = hex(OLD_BLOCK), hex(RECENT_BLOCK)
        balance_data = "0x70a08231" + ATOKEN[2:].lower().rjust(64, "0")
        observations = {
            "old_pool_code": client.call("eth_getCode", [POOL, old_tag]),
            "old_pool_implementation_slot": client.call("eth_getStorageAt", [POOL, IMPL_SLOT, old_tag]),
            "old_atoken_total_supply": client.call("eth_call", [{"to": ATOKEN, "data": "0x18160ddd"}, old_tag]),
            "old_usdc_balance_at_atoken": client.call("eth_call", [{"to": USDC, "data": balance_data}, old_tag]),
            "recent_usdc_balance_at_atoken": client.call("eth_call", [{"to": USDC, "data": balance_data}, recent_tag]),
            "old_atoken_decimals": client.call("eth_call", [{"to": ATOKEN, "data": "0x313ce567"}, old_tag]),
        }
        transactions = old.get("transactions", [])
        observations["old_receipt"] = client.call(
            "eth_getTransactionReceipt", [transactions[0]]) if transactions else None
        observations["old_atoken_code"] = client.call("eth_getCode", [ATOKEN, old_tag])
        observations["recent_pool_implementation_slot"] = client.call(
            "eth_getStorageAt", [POOL, IMPL_SLOT, recent_tag])
        output["observations"] = observations
        output["capabilities_observed"] = {
            "historical_block_header": True,
            "historical_receipt": isinstance(observations["old_receipt"], dict)
            and observations["old_receipt"].get("blockNumber") == old_tag,
            "historical_pool_code_nonempty": bool(observations["old_pool_code"])
            and observations["old_pool_code"] != "0x",
            "historical_pool_storage_word": isinstance(observations["old_pool_implementation_slot"], str)
            and len(observations["old_pool_implementation_slot"]) == 66,
            "historical_erc20_total_supply_call": isinstance(observations["old_atoken_total_supply"], str)
            and len(observations["old_atoken_total_supply"]) == 66,
            "historical_erc20_balance_call": isinstance(observations["old_usdc_balance_at_atoken"], str)
            and len(observations["old_usdc_balance_at_atoken"]) == 66,
        }
        if not all(output["capabilities_observed"].values()):
            output["blocker"] = "one or more archive capabilities failed; inspect raw RPC records"
        if not output["tools"]["anvil"] and not output["tools"]["revm"]:
            output["local_fork_blocker"] = "no Anvil/revm executable found on PATH; none installed by probe"
    except (OSError, subprocess.TimeoutExpired):
        output["blocker"] = "source/transport tool unavailable or timed out; no retry performed"
    finally:
        output["rpc_reads_attempted"] = len(client.records)
        output["completed_at"] = utc_now()
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-read-only-probe", action="store_true", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = probe()
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output_written": True, "rpc_reads_attempted": result["rpc_reads_attempted"],
                      "capabilities_observed": result.get("capabilities_observed"),
                      "blocker": result.get("blocker"),
                      "local_fork_blocker": result.get("local_fork_blocker"),
                      "is_t2_evidence": False}, indent=2))
    return 0 if not result.get("blocker") else 1


if __name__ == "__main__":
    raise SystemExit(main())
