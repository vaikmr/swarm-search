"""Offline consistency checks, NOT an independent chain/event recount or PnL."""

import hashlib
import json
import re
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path

SOURCE_COMMIT = "23d2fd15c1d736b6c8cee4614e82f3d55fc430c4"
SOURCE_DIR = "strategies/cross-chain-relaying/evidence/"
ROOT = Path(__file__).resolve().parents[2]
FILL_TOPIC = "0x44b559f101f8fbcc8a0ea43fa91a05a729a5ea6e14a7c75aa750374690137208"
REFUND_TOPIC = "0xf4ad92585b1bc117fbdd644990adf0827bc4c95baeae8a23322af807b6d0020e"
TOKENS = {
    "USDC": "0x0b2c639c533813f4aa9d7837caf62653d097ff85",
    "WETH": "0x4200000000000000000000000000000000000006",
    "bridged_USDT": "0x94b008aa00579c1307b0ef2c499ad98a8ce58e58",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def units(raw, decimals):
    require(isinstance(raw, str) and re.fullmatch(r"[0-9]+", raw), "Invalid raw amount")
    require(type(decimals) is int and 0 <= decimals <= 36, "Invalid decimals")
    digits = str(int(raw))
    if decimals == 0:
        return digits
    padded = digits.rjust(decimals + 1, "0")
    return padded[:-decimals] + "." + padded[-decimals:]


def validate_pages(summary, kind):
    """Check recorded request coverage, not provider response contents."""
    start = summary["open_block_excluded"] + 1
    end = summary["close_block_included"]
    size = summary["pagination"]["page_size_blocks"]
    require(type(size) is int and size > 0, "Invalid page size")
    expected = [(lo, min(lo + size - 1, end)) for lo in range(start, end + 1, size)]
    requests = [
        r for r in summary["request_manifest"] if r["name"].startswith(kind + "-")
    ]
    actual = []
    actor_topic = "0x" + summary["actor_address"][2:].rjust(64, "0")
    topics = [FILL_TOPIC, None, None, actor_topic] if kind == "fills" else [REFUND_TOPIC]
    for request in requests:
        require(request["method"] == "eth_getLogs", "Wrong method")
        require(request["ok"] and request["http_status"] == 200, "Failed page")
        require(re.fullmatch(r"[0-9a-f]{64}", request["response_sha256"]), "Missing digest")
        query = request["params"][0]
        require(query["address"].lower() == summary["spoke_pool"].lower(), "Wrong pool")
        require(query["topics"] == topics, "Wrong chain-role/actor filter")
        actual.append((int(query["fromBlock"], 16), int(query["toBlock"], 16)))
    require(sorted(actual) == expected, "Missing, overlapping or duplicate page")
    require(len(actual) == summary["pagination"]["successful_pages"][kind], "Count mismatch")
    return len(actual)


def check_summary(summary):
    require(summary["chain_id"] == 10, "This evidence is an Optimism destination slice")
    state = summary["selected_inventory_not_total_capital"]
    opening, closing = state["opening"], state["closing"]
    require(opening["block_number"] == summary["open_block_excluded"], "Opening mismatch")
    require(closing["block_number"] == summary["close_block_included"], "Closing mismatch")
    for point in (opening, closing):
        parsed = int(datetime.fromisoformat(point["timestamp_utc"]).timestamp())
        require(parsed == point["timestamp_unix"], "Timestamp mismatch")
    seconds = closing["timestamp_unix"] - opening["timestamp_unix"]
    require(seconds == summary["elapsed_window_seconds"] == 14 * 86400, "Not exact 14 days")
    require(len(summary["request_manifest"]) == summary["request_count"], "Manifest mismatch")
    require(not summary["pagination"]["failed_pages"], "Failed pages")
    require(not summary["pagination"]["decode_errors"], "Decode errors")
    pages = {kind: validate_pages(summary, kind) for kind in ("fills", "refunds")}
    require(all(v == summary["pagination"]["expected_pages_per_kind"] for v in pages.values()),
            "Expected-page mismatch")
    fills = summary["observed_fill_event_count"]
    chains = summary["fill_repayment_chain_counts"]
    require(all(type(v) is int and v >= 0 for v in chains.values()), "Invalid counts")
    require(sum(chains.values()) == fills, "Repayment counts do not sum to fills")
    require(sum(summary["fill_type_counts"].values()) == fills, "Fill types do not sum")
    require(0 <= summary["observed_unique_fill_transactions"] <= fills, "Invalid tx count")
    inventory = {}
    for label, point in state.items():
        inventory[label] = {"native_ETH": units(point["native_wei"], 18)}
        for symbol in TOKENS:
            inventory[label][symbol] = units(
                point[symbol + "_raw"], summary["token_decimals"][symbol]
            )
    return {
        "window_seconds": seconds,
        "window_is_historical_not_forward_paper": True,
        "recorded_contiguous_pages": pages,
        "reported_fill_count_not_independently_recounted": fills,
        "reported_actor_allocation_event_count_not_paid_refund_count":
            summary["refund_event_count_with_actor_allocation"],
        "reported_repayment_chain_counts": {
            "arbitrum_42161": chains.get("42161", 0),
            "optimism_10": chains.get("10", 0),
            "other_chain_ids": fills - chains.get("42161", 0) - chains.get("10", 0),
        },
        "repayment_chain_id_does_not_determine_origin_chain": True,
        "nonce_advance_not_transaction_census":
            int(closing["account_nonce"]) - int(opening["account_nonce"]),
        "selected_wallet_balances_token_units_not_USD_or_total_capital": inventory,
    }


def check_witnesses(summary, witnesses):
    lo, hi = summary["open_block_excluded"], summary["close_block_included"]
    for key in ("fill_boundaries", "refund_boundaries", "refund_example_allocation_rows"):
        for row in witnesses[key]:
            require(lo < row["block_number"] <= hi, "Witness outside interval")
    receipt = witnesses["refund_example_selected_receipt"]
    require(receipt["status"] == "0x1", "Example receipt failed")
    require(lo < int(receipt["blockNumber"], 16) <= hi, "Receipt outside interval")
    amounts = defaultdict(int)
    for row in witnesses["refund_example_allocation_rows"]:
        require(row["transaction_hash"] == receipt["transactionHash"], "Wrong example tx")
        amounts[row["token"]] += int(row["allocated_amount_raw"])
    transfers = defaultdict(int)
    for row in witnesses["actual_pool_to_actor_transfers"]:
        require(row["transaction_hash"] == receipt["transactionHash"], "Wrong transfer tx")
        transfers[row["token"]] += int(row["amount_raw"])
    require(dict(amounts) == dict(transfers), "Example allocation/transfer mismatch")
    decimals = {
        address: summary["token_decimals"][symbol] for symbol, address in TOKENS.items()
    }
    route_witnesses = []
    for row in witnesses["fill_boundaries"]:
        if row["origin_chain_id"] == row["repayment_chain_id"] == 42161:
            route_witnesses.append({
                "destination_chain_id": 10,
                "origin_chain_id": 42161,
                "repayment_chain_id": 42161,
                "output_token": row["output_token"],
                "output_token_units": units(
                    row["actual_output_amount_raw"], decimals[row["output_token"]]
                ),
                "block_number": row["block_number"],
                "matched_claim_or_payment": False,
            })
    return {
        "decoded_witnesses_only_no_raw_log_redecode": True,
        "example_allocation_transfer_amounts_consistent": True,
        "example_selected_transfers_token_units_not_profit": {
            token: units(str(amount), decimals[token]) for token, amount in transfers.items()
        },
        "example_refund_transaction_sender_is_selected_actor":
            receipt["from"].lower() == summary["actor_address"].lower(),
        "retained_arbitrum_origin_and_repayment_route_witnesses": route_witnesses,
    }


def build_output():
    sources, parsed = [], {}
    for name in ("history-probe-summary.json", "history-witnesses.json"):
        path = SOURCE_DIR + name
        raw = subprocess.check_output(["git", "show", SOURCE_COMMIT + ":" + path], cwd=ROOT)
        parsed[name] = json.loads(raw)
        sources.append({
            "url": "https://github.com/vaikmr/swarm-search/blob/" + SOURCE_COMMIT + "/" + path,
            "sha256": hashlib.sha256(raw).hexdigest(),
        })
    summary, witnesses = parsed["history-probe-summary.json"], parsed["history-witnesses.json"]
    return {
        "source_commit": SOURCE_COMMIT,
        "sources": sources,
        "verification_scope": "Offline consistency of committed summaries and selected decoded witnesses",
        "network_rpc_requests_performed_by_this_checker": 0,
        "summary": check_summary(summary),
        "witnesses": check_witnesses(summary, witnesses),
        "unverified": {
            "actor_pnl_usd": None,
            "entrant_capture_share": None,
            "qualified_lock_time_seconds": None,
            "peak_outstanding_receivables_usd": None,
            "entrant_deployable_capital_usd": None,
            "qualifies_t1": False,
            "qualifies_t2": False,
            "qualifies_t3": False,
        },
    }


if __name__ == "__main__":
    print(json.dumps(build_output(), indent=2) + "\n", end="")
