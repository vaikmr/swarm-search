"""Offline self-audit of saved Across responses; deliberately no network imports.

The collection author runs this over ignored raw files. This does not give an
independent reviewer possession of every raw page or establish ABI semantics/PnL.
"""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

FILL = "0x44b559f101f8fbcc8a0ea43fa91a05a729a5ea6e14a7c75aa750374690137208"
REFUND = "0xf4ad92585b1bc117fbdd644990adf0827bc4c95baeae8a23322af807b6d0020e"
TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
TOKENS = {
    "USDC": "0x0b2c639c533813f4aa9d7837caf62653d097ff85",
    "WETH": "0x4200000000000000000000000000000000000006",
    "bridged_USDT": "0x94b008aa00579c1307b0ef2c499ad98a8ce58e58",
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def fingerprint(value):
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def address_word(address):
    return "0x" + address[2:].lower().rjust(64, "0")


def uint_at(data, offset):
    if offset < 0 or offset % 32 or offset + 32 > len(data):
        raise ValueError("Invalid ABI uint offset")
    return int.from_bytes(data[offset:offset + 32], "big")


def address_at(data, offset):
    value = uint_at(data, offset)
    if value >= 2 ** 160:
        raise ValueError("Non-EVM address word")
    return f"0x{value:040x}"


def refund_allocation(log, actor):
    """Second decoder: byte offsets, not an import of the collection decoder."""
    data = bytes.fromhex(log["data"][2:])
    if len(data) % 32 or len(data) < 256:
        raise ValueError("Bad refund data length")
    amount_offset = uint_at(data, 32)
    address_offset = uint_at(data, 96)
    if min(amount_offset, address_offset) < 192:
        raise ValueError("Refund array overlaps static head")
    count = uint_at(data, amount_offset)
    if count > 1000 or count != uint_at(data, address_offset):
        raise ValueError("Bad refund array lengths")
    flag = uint_at(data, 128)
    if flag not in (0, 1):
        raise ValueError("Non-boolean deferred flag")
    total = sum(
        uint_at(data, amount_offset + 32 * (i + 1))
        for i in range(count)
        if address_at(data, address_offset + 32 * (i + 1)) == actor
    )
    return address_at(data, 64), total, bool(flag)


def fill_fields(log, actor):
    data = bytes.fromhex(log["data"][2:])
    if len(data) != 480 or len(log["topics"]) != 4:
        raise ValueError("Bad current fill layout")
    if log["topics"][3].lower() != address_word(actor):
        raise ValueError("Wrong indexed relayer")
    return {
        "output_token": address_at(data, 32),
        "repayment_chain": str(uint_at(data, 128)),
        "updated_output_raw": uint_at(data, 416),
        "fill_type": str(uint_at(data, 448)),
    }


def check_file(raw_path, entry):
    raw = raw_path.read_bytes()
    digest = sha(raw)
    return {
        "name": entry["name"], "observed_sha256": digest,
        "observed_bytes": len(raw),
        "sha256_matches": digest == entry["response_sha256"],
        "bytes_match": len(raw) == entry["response_bytes"],
    }, json.loads(raw)


def check_coverage(pages, first, last):
    ordered = sorted(pages)
    if not ordered or ordered[0][0] != first or ordered[-1][1] != last:
        return False
    return all(
        hi >= lo and hi - lo + 1 <= 10000 and
        (i == 0 or ordered[i - 1][1] + 1 == lo)
        for i, (lo, hi) in enumerate(ordered)
    )


def audit(raw_dir, manifest_path):
    directory = Path(raw_dir)
    source_bytes = Path(manifest_path).read_bytes()
    source = json.loads(source_bytes)
    actor, pool = source["actor_address"], source["spoke_pool"]
    first, last = source["open_block_excluded"] + 1, source["close_block_included"]
    errors, checks, bodies = [], [], {}
    entries = {e["name"]: e for e in source["request_manifest"]}
    if len(entries) != len(source["request_manifest"]):
        errors.append("Duplicate manifest names")
    for name, entry in sorted(entries.items()):
        if not entry["ok"]:
            continue
        try:
            check, body = check_file(directory / (name + ".json"), entry)
            checks.append(check)
            if not check["sha256_matches"] or not check["bytes_match"]:
                errors.append("Raw hash/size mismatch: " + name)
            if entry["method"] != "GET" and ("error" in body or "result" not in body):
                errors.append("RPC error/missing result: " + name)
            bodies[name] = body
        except (OSError, ValueError, KeyError) as exc:
            errors.append(f"Unreadable response {name}: {exc}")

    pages = {"fills": [], "refunds": []}
    seen, block_hashes = set(), {}
    fill_count, refund_count = 0, 0
    fill_tx, repayment, fill_types = set(), Counter(), Counter()
    payout_totals, refund_totals = defaultdict(int), defaultdict(int)
    deferred = 0
    fill_witness, refund_witness = None, None
    matching_refund_logs = {}
    example = entries["refund-receipt-example"]["params"][0]

    def witness(name, index, value):
        return {
            "source_response_name": name,
            "source_response_sha256": entries[name]["response_sha256"],
            "source_response_bytes": entries[name]["response_bytes"],
            "json_pointer": "/result/" + str(index),
            "object_fingerprint_kind": "sha256_canonical_json_not_http_bytes",
            "object_fingerprint": fingerprint(value), "original_raw_object": value,
        }

    for name, entry in sorted(entries.items()):
        if entry["method"] != "eth_getLogs" or not entry["ok"]:
            continue
        query = entry["params"][0]
        topic = query["topics"][0]
        if topic not in (FILL, REFUND):
            errors.append("Unexpected queried event topic: " + name)
            continue
        kind = "fills" if topic == FILL else "refunds"
        lo, hi = int(query["fromBlock"], 16), int(query["toBlock"], 16)
        pages[kind].append((lo, hi))
        body = bodies.get(name, {})
        for index, log in enumerate(body.get("result", [])):
            try:
                block = int(log["blockNumber"], 16)
                if log["address"].lower() != pool or log["topics"][0].lower() != topic:
                    raise ValueError("Wrong emitting contract/topic")
                if log.get("removed") or not lo <= block <= hi:
                    raise ValueError("Removed/out-of-range log")
                key = (log["transactionHash"], log["logIndex"])
                if key in seen:
                    raise ValueError("Duplicate transaction/log-index key")
                seen.add(key)
                if block in block_hashes and block_hashes[block] != log["blockHash"]:
                    raise ValueError("Conflicting block hashes across saved logs")
                block_hashes[block] = log["blockHash"]
                if topic == FILL:
                    decoded = fill_fields(log, actor)
                    fill_count += 1
                    fill_tx.add(log["transactionHash"])
                    repayment[decoded["repayment_chain"]] += 1
                    fill_types[decoded["fill_type"]] += 1
                    payout_totals[decoded["output_token"]] += decoded["updated_output_raw"]
                    if fill_witness is None:
                        fill_witness = witness(name, index, log)
                else:
                    if len(log["topics"]) != 4 or int(log["topics"][1], 16) != 10:
                        raise ValueError("Wrong refund chain/topics")
                    token, amount, batch_deferred = refund_allocation(log, actor)
                    if amount:
                        refund_count += 1
                        refund_totals[token] += amount
                        deferred += batch_deferred
                        if log["transactionHash"] == example:
                            matching_refund_logs[key] = log
                            if token == TOKENS["USDC"]:
                                refund_witness = witness(name, index, log)
            except (ValueError, KeyError, TypeError, IndexError) as exc:
                errors.append(f"Log {name}[{index}]: {exc}")

    headers = {}
    states = source["selected_inventory_not_total_capital"]
    for label in ("opening", "closing"):
        header = bodies[label + "-block"]["result"]
        expected = states[label]
        headers[label] = {
            "number_matches_requested": int(header["number"], 16) == expected["block_number"],
            "hash_matches_summary": header["hash"] == expected["block_hash"],
            "timestamp_matches_summary": int(header["timestamp"], 16) == expected["timestamp_unix"],
        }
        if not all(headers[label].values()):
            errors.append("Boundary header mismatch: " + label)
        if expected["block_number"] in block_hashes and (
            block_hashes[expected["block_number"]] != header["hash"]
        ):
            errors.append("Boundary log/header hash mismatch: " + label)
        for suffix, field in [("native_wei", "native_wei"),
                              ("outgoing_nonce", "account_nonce"),
                              ("USDC", "USDC_raw"), ("WETH", "WETH_raw"),
                              ("bridged_USDT", "bridged_USDT_raw")]:
            actual = int(bodies[label + "-" + suffix]["result"], 16)
            if actual != int(expected[field]):
                errors.append("Historical state mismatch: " + label + "-" + suffix)

    receipt = bodies["refund-receipt-example"]["result"]
    receipt_checks = {
        "hash_matches_request": receipt["transactionHash"] == example,
        "successful": receipt["status"] == "0x1",
        "recipient_is_spoke_pool": receipt["to"].lower() == pool,
        "sender_is_different_from_indexed_relayer": receipt["from"].lower() != actor,
        "all_logs_match_receipt_header": all(
            log["transactionHash"] == example and log["blockNumber"] == receipt["blockNumber"]
            and log["blockHash"] == receipt["blockHash"]
            for log in receipt["logs"]
        ),
        "refund_page_logs_equal_receipt_logs": all(
            any(log == raw_log for raw_log in receipt["logs"])
            for log in matching_refund_logs.values()
        ) and len(matching_refund_logs) > 0,
        "block_hash_agrees_with_page": block_hashes.get(
            int(receipt["blockNumber"], 16)
        ) == receipt["blockHash"],
    }
    receipt_transfers, transfer_witness = [], None
    for i, log in enumerate(receipt["logs"]):
        if [t.lower() for t in log["topics"]] == [
            TRANSFER, address_word(pool), address_word(actor)
        ]:
            amount = uint_at(bytes.fromhex(log["data"][2:]), 0)
            receipt_transfers.append({
                "transaction_hash": example, "log_index": log["logIndex"],
                "token": log["address"].lower(), "amount_raw": str(amount),
            })
            if log["address"].lower() == TOKENS["USDC"]:
                transfer_witness = witness("refund-receipt-example", i, log)
                transfer_witness["json_pointer"] = "/result/logs/" + str(i)
    receipt_checks["transfers_equal_summary"] = (
        receipt_transfers == source["one_receipt_confirmed_refund_transfers_not_profit"]
    )
    if not all(receipt_checks.values()):
        errors.append("Receipt-to-page/header/summary check failed")

    comparisons = {
        "fill_event_count": fill_count == source["observed_fill_event_count"],
        "unique_fill_event_transaction_hashes": len(fill_tx) == source["observed_unique_fill_transactions"],
        "repayment_chain_counts": dict(repayment) == source["fill_repayment_chain_counts"],
        "fill_type_counts": dict(fill_types) == source["fill_type_counts"],
        "fill_token_totals": {k: str(v) for k, v in payout_totals.items()} ==
                             source["fill_output_totals_by_token_raw_not_profit"],
        "refund_actor_event_count": refund_count == source["refund_event_count_with_actor_allocation"],
        "refund_token_totals": {k: str(v) for k, v in refund_totals.items()} ==
                               source["refund_allocations_by_token_raw_not_cash_or_profit"],
        "deferred_batch_count": deferred == source["refund_batches_with_any_deferred_payment"],
        "fill_page_interval": check_coverage(pages["fills"], first, last),
        "refund_page_interval": check_coverage(pages["refunds"], first, last),
    }
    if not all(comparisons.values()):
        errors.append("Recount/coverage mismatch")
    result = {
        "audit_kind": "collection_author_offline_raw_rehash_recount_not_independent_review",
        "network_requests_performed": 0, "qualifies_t1": False,
        "realized_pnl_usd": None, "capital_deployed_usd": None,
        "audited_manifest_sha256": sha(source_bytes),
        "source_window_utc": {label: states[label]["timestamp_utc"] for label in states},
        "successful_raw_entries_checked": len(checks),
        "all_response_sha256_and_sizes_matched": all(
            c["sha256_matches"] and c["bytes_match"] for c in checks
        ) and len(checks) == sum(e["ok"] for e in source["request_manifest"]),
        "all_source_checks_canonical_fingerprint": fingerprint(checks),
        "raw_http_bytes_checked": sum(c["observed_bytes"] for c in checks),
        "boundary_header_checks": headers, "receipt_checks": receipt_checks,
        "recount_comparisons": comparisons,
        "fill_event_count": fill_count, "distinct_fill_event_transaction_hashes": len(fill_tx),
        "actor_refund_allocation_event_count": refund_count,
        "repayment_chain_counts": dict(repayment),
        "fill_output_totals_by_token_raw_not_profit": {k: str(v) for k, v in payout_totals.items()},
        "refund_allocations_by_token_raw_not_cash_or_profit": {k: str(v) for k, v in refund_totals.items()},
        "page_counts": {k: len(v) for k, v in pages.items()},
        "abi_source_pin_available_in_saved_data": False,
        "abi_semantics_limit": (
            "Only mutable master source URLs were retained, not the source bodies, "
            "commit/blob IDs, or deployed implementation mapping. Layout parity and "
            "an explorer example do not pin ABI semantics. Indexed relayer address "
            "must not be promoted to verified transaction sender, payer or firm."
        ),
        "canonicality_limit": (
            "Two saved boundary headers and within-response/page/receipt hash "
            "consistency checked; no independent headers for every intermediate "
            "block, block-header hash recomputation, or external canonicality recheck."
        ),
        "independent_review_limit": (
            "Raw 144 HTTP bodies remain local/ignored. Reviewer can inspect exported "
            "raw witnesses, but this collection-author audit is not an independent "
            "reviewer's recount of all 122 raw log pages."
        ),
        "errors": errors, "raw_integrity_recount_passed": not errors,
        "economic_or_attribution_semantics_certified": False,
    }
    witnesses = {
        "kind": "original_raw_objects_with_HTTP_response_references_not_PnL",
        "fill": fill_witness, "actor_refund_allocation": refund_witness,
        "receipt_pool_to_actor_transfer": transfer_witness,
        "receipt_from": receipt["from"], "receipt_to": receipt["to"],
        "receipt_block_hash": receipt["blockHash"], "receipt_block_number": receipt["blockNumber"],
    }
    return result, witnesses, checks


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", default="data/raw/across-actor-history")
    parser.add_argument("--manifest", default=(
        "strategies/cross-chain-relaying/evidence/history-probe-summary.json"
    ))
    parser.add_argument("--output-dir", default="data/raw/across-offline-audit")
    args = parser.parse_args()
    summary, witnesses, checks = audit(args.raw_dir, args.manifest)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for name, value in [("summary", summary), ("raw-witnesses", witnesses),
                        ("rehash-checks", checks)]:
        (out / (name + ".json")).write_text(json.dumps(value, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    raise SystemExit(0 if summary["raw_integrity_recount_passed"] else 1)
