"""Separately authorized eight-read dRPC archive prerequisite check; not a replay."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal
import json
from pathlib import Path
import re
from typing import Any

from .replay_rpc_probe import (
    ATOKEN, DRPC_URL, IMPL_SLOT, POOL, RECENT_BLOCK, RECENT_HASH, REGISTRY_URL,
    ProbeClient, tool_availability, utc_now,
)


START_BLOCK = 26_080_884
START_HASH = "0xc27eb6a8592b703fed5180626e29db037f217eff4f11f4a188687cece69ed244"
ACTOR = "0x56957E411Ea83a0B4A0689C1fB0D1e5eA0d20149"
BUDGET = 8


def hex_word(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"0x[0-9a-fA-F]{64}", value) is not None


def header_valid(value: Any, number: int, expected_hash: str | None = None) -> bool:
    if not isinstance(value, dict):
        return False
    try:
        valid = (value.get("number") == hex(number) and hex_word(value.get("hash"))
                 and int(value["timestamp"], 16) > 0)
        return valid and (expected_hash is None or value["hash"] == expected_hash)
    except (KeyError, ValueError, TypeError):
        return False


def probe() -> dict[str, Any]:
    client = ProbeClient(endpoint=DRPC_URL, max_reads=BUDGET)
    output: dict[str, Any] = {
        "started_at": utc_now(), "paper_only": True, "endpoint": DRPC_URL,
        "rpc_read_budget": BUDGET, "rpc_records": client.records,
        "evidence_class": "access_prerequisite_only", "is_t2_evidence": False,
        "fork_started": False, "completed_fork_replay": False,
        "continuous_30day_state_coverage_established": False,
        "tools": tool_availability(), "registry_reference": REGISTRY_URL,
        "identity_evidence_reference": "https://github.com/vaikmr/swarm-search/blob/"
        "18370d81039303e86263dc998c87164d8d75226e/"
        "strategies/benchmark-lending/evidence/aave-usdc-deployment-identity.json",
        "public_actor_candidate": ACTOR,
        "actor_reference": f"https://etherscan.io/address/{ACTOR}",
        "limits": [
            "Two dated state snapshots, not 30 days of replay or continuous state coverage.",
            "Actor token balances are not realized PnL or evidence that actor/strategy is profitable.",
            "Historical implementation slots are read independently, not copied from current registry.",
            "Historical implementation bytecode/ABI/audit equivalence and all fork dependencies unverified.",
            "No local EVM runtime installed or fork started; no signing, transactions or payments.",
            "No strategy cost, latency, execution or competition model was tested.",
        ],
    }
    try:
        chain = client.call("eth_chainId", [])
        start = client.call("eth_getBlockByNumber", [hex(START_BLOCK), False])
        end = client.call("eth_getBlockByNumber", [hex(RECENT_BLOCK), False])
        valid = (chain == "0x1" and header_valid(start, START_BLOCK, START_HASH)
                 and header_valid(end, RECENT_BLOCK, RECENT_HASH))
        output["block_identity_checks_passed"] = valid
        if not valid:
            output["blocker"] = "invalid chain/header or substituted pinned end-block identity"
            return output
        start_seconds, end_seconds = int(start["timestamp"], 16), int(end["timestamp"], 16)
        output["snapshot_interval"] = {
            "start_block": START_BLOCK, "start_hash": start["hash"],
            "start_utc": datetime.fromtimestamp(start_seconds, timezone.utc).isoformat(),
            "end_block": RECENT_BLOCK, "end_hash": end["hash"],
            "end_utc": datetime.fromtimestamp(end_seconds, timezone.utc).isoformat(),
            "elapsed_seconds": end_seconds - start_seconds,
            "elapsed_days": str(Decimal(end_seconds - start_seconds) / Decimal(86400)),
            "at_least_30_days": end_seconds - start_seconds >= 30 * 86400,
        }
        if not output["snapshot_interval"]["at_least_30_days"]:
            output["blocker"] = "actual snapshot interval shorter than 30 days"
            return output
        start_tag, end_tag = hex(START_BLOCK), hex(RECENT_BLOCK)
        balance_data = "0x70a08231" + ACTOR[2:].lower().rjust(64, "0")
        observed = {
            "pool_code_at_start": client.call("eth_getCode", [POOL, start_tag]),
            "implementation_slot_at_start": client.call("eth_getStorageAt", [POOL, IMPL_SLOT, start_tag]),
            "implementation_slot_at_end": client.call("eth_getStorageAt", [POOL, IMPL_SLOT, end_tag]),
            "atoken_balance_at_start": client.call("eth_call", [{"to": ATOKEN, "data": balance_data}, start_tag]),
            "atoken_balance_at_end": client.call("eth_call", [{"to": ATOKEN, "data": balance_data}, end_tag]),
        }
        output["observations"] = observed
        code = observed["pool_code_at_start"]
        checks = {
            "nonempty_historical_pool_code": isinstance(code, str)
            and re.fullmatch(r"0x(?:[0-9a-fA-F]{2})+", code) is not None,
            **{key: hex_word(observed[key]) for key in (
                "implementation_slot_at_start", "implementation_slot_at_end",
                "atoken_balance_at_start", "atoken_balance_at_end")},
            "nonzero_implementation_at_start": hex_word(observed["implementation_slot_at_start"])
            and int(observed["implementation_slot_at_start"], 16) != 0,
            "nonzero_implementation_at_end": hex_word(observed["implementation_slot_at_end"])
            and int(observed["implementation_slot_at_end"], 16) != 0,
        }
        output["state_shape_checks"] = checks
        output["tested_remote_state_prerequisites_passed"] = all(checks.values())
        output["local_fork_ready"] = False
        if not all(checks.values()):
            output["blocker"] = "empty, invalid or unavailable dated state result; no prerequisite success accepted"
        elif not output["tools"]["anvil"] and not output["tools"]["revm"]:
            output["local_fork_blocker"] = "remote sample passed, but no local EVM executable found on PATH"
    finally:
        output["rpc_reads_attempted"] = len(client.records)
        output["completed_at"] = utc_now()
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-eight-read-probe", action="store_true", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = probe()
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result.get(key) for key in (
        "rpc_reads_attempted", "snapshot_interval", "tested_remote_state_prerequisites_passed",
        "blocker", "local_fork_blocker", "fork_started", "is_t2_evidence")}, indent=2))
    return 1 if result.get("blocker") else 0


if __name__ == "__main__":
    raise SystemExit(main())
