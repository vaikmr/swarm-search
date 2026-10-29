"""Offline consistency checks of pinned Across summary/witnesses, NOT raw data or PnL."""

import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re


SOURCE_REVISION = "23d2fd15c1d736b6c8cee4614e82f3d55fc430c4"
DIGESTS = {
    "history-probe-summary.json":
        "dbf2ebe7576773324ae604518a0e0494275de18a5a8488e0171ada4bd80c4cee",
    "history-witnesses.json":
        "9172258921e58191313809970a0cb97e51d38075059beae6326235bdd9048836",
}
TOPICS = {
    "fills": "0x44b559f101f8fbcc8a0ea43fa91a05a729a5ea6e14a7c75aa750374690137208",
    "refunds": "0xf4ad92585b1bc117fbdd644990adf0827bc4c95baeae8a23322af807b6d0020e",
}
AUDIT_SOURCE_REVISION = "12a5426c528d691d7ecf5e51eff8ec2d63f32cc6"
AUDIT_DIGESTS = {
    "offline-audit-summary.json":
        "9294336a65d2c61bcdf5c710b072d17b2a26ba4024c57bea58d7fd3768033ec0",
    "offline-raw-witnesses.json":
        "5c8f2320382c44d08057411576b87d80c854884e2ab672ee8fe37e841c452f46",
}


def check(source_root):
    folder = source_root / "strategies/cross-chain-relaying/evidence"
    data = {}
    for name, expected in DIGESTS.items():
        blob = (folder / name).read_bytes()
        if hashlib.sha256(blob).hexdigest() != expected:
            raise ValueError("This historical check requires pinned source " + SOURCE_REVISION)
        data[name] = json.loads(blob)
    summary, witness = (data[name] for name in DIGESTS)
    manifest = summary["request_manifest"]
    assert len(manifest) == summary["request_count"] == 146
    assert len({row["name"] for row in manifest}) == 146
    actor = summary["actor_address"]
    actor_topic = "0x" + actor[2:].rjust(64, "0")
    first, last = summary["open_block_excluded"] + 1, summary["close_block_included"]
    counts = {}
    for kind, topic in TOPICS.items():
        pages = sorted(
            (row for row in manifest if row["name"].startswith(kind + "-")),
            key=lambda row: int(row["params"][0]["fromBlock"], 16),
        )
        assert len(pages) == 61
        next_block = first
        for row in pages:
            query = row["params"][0]
            lo, hi = (int(query[name], 16) for name in ("fromBlock", "toBlock"))
            assert row["method"] == "eth_getLogs"
            assert row["source_url"] == "https://mainnet.optimism.io"
            assert row["ok"] and row["http_status"] == 200
            assert query["address"].lower() == summary["spoke_pool"]
            assert lo == next_block and lo <= hi <= last and hi - lo + 1 <= 10000
            assert query["topics"] == (
                [topic, None, None, actor_topic] if kind == "fills" else [topic]
            )
            assert re.fullmatch("[0-9a-f]{64}", row["response_sha256"])
            assert 0 < row["response_bytes"] <= 2_000_000
            next_block = hi + 1
        assert next_block == last + 1
        counts[kind] = len(pages)
    assert summary["pagination"]["successful_pages"] == counts
    assert not summary["pagination"]["failed_pages"]
    assert not summary["pagination"]["decode_errors"]
    states = summary["selected_inventory_not_total_capital"]
    for state in states.values():
        assert int(datetime.fromisoformat(state["timestamp_utc"]).timestamp()) == state["timestamp_unix"]
    assert (
        states["closing"]["timestamp_unix"] - states["opening"]["timestamp_unix"]
        == summary["elapsed_window_seconds"] == 1_209_600
    )
    assert (
        sum(summary["fill_repayment_chain_counts"].values())
        == sum(summary["fill_type_counts"].values())
        == summary["observed_fill_event_count"] == 2915
    )
    assert summary["observed_unique_fill_transactions"] == 2915
    assert summary["refund_event_count_with_actor_allocation"] == 983
    for row in (
        witness["fill_boundaries"] + witness["refund_boundaries"]
        + witness["refund_example_allocation_rows"]
    ):
        assert first <= row["block_number"] <= last
    allocations, transfers = Counter(), Counter()
    for row in witness["refund_example_allocation_rows"]:
        allocations[row["token"]] += int(row["allocated_amount_raw"])
        assert not row["cash_receipt_independently_verified"]
    for row in witness["actual_pool_to_actor_transfers"]:
        transfers[row["token"]] += int(row["amount_raw"])
    assert allocations == transfers
    receipt = witness["refund_example_selected_receipt"]
    assert receipt["status"] == "0x1" and receipt["from"].lower() != actor
    for row in witness["refund_example_allocation_rows"] + witness["actual_pool_to_actor_transfers"]:
        assert row["transaction_hash"] == receipt["transactionHash"]
    for row in witness["refund_example_allocation_rows"]:
        assert row["block_number"] == int(receipt["blockNumber"], 16)
    assert not summary["qualifies_t1"] and not summary["all_costs_reconciled"]
    assert not summary["source_coverage_complete"]
    for key in (
        "realized_pnl_usd", "capital_deployed_usd",
        "opening_receivables_raw", "closing_receivables_raw",
    ):
        assert summary[key] is None
    return {
        "reviewed_source_revision": SOURCE_REVISION,
        "committed_json_integrity_and_internal_consistency": "PASS",
        "requested_manifest_page_counts": counts,
        "network_calls": 0,
        "raw_response_bodies_rehashed_or_recounted": False,
        "provider_completeness_verified": False,
        "actor_sender_or_economic_payer_attribution_verified": False,
        "strategy_performance_or_evidence_tier_certified": False,
    }


def check_raw_witness_followup(source_root):
    """Decode exported objects; this does not prove membership in absent pages."""
    folder = source_root / "strategies/cross-chain-relaying/evidence"
    extra = {}
    for name, expected in AUDIT_DIGESTS.items():
        blob = (folder / name).read_bytes()
        if hashlib.sha256(blob).hexdigest() != expected:
            raise ValueError("Follow-up check requires pinned source " + AUDIT_SOURCE_REVISION)
        extra[name] = json.loads(blob)
    audit, exported = (extra[name] for name in AUDIT_DIGESTS)
    original = json.loads((folder / "history-probe-summary.json").read_text())
    previous = json.loads((folder / "history-witnesses.json").read_text())
    entries = {row["name"]: row for row in original["request_manifest"]}
    canonical = lambda value: hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    expected_checks = [{
        "name": row["name"], "observed_sha256": row["response_sha256"],
        "observed_bytes": row["response_bytes"], "sha256_matches": True,
        "bytes_match": True,
    } for row in sorted(entries.values(), key=lambda item: item["name"]) if row["ok"]]
    assert audit["audited_manifest_sha256"] == DIGESTS["history-probe-summary.json"]
    assert audit["successful_raw_entries_checked"] == len(expected_checks) == 144
    assert audit["raw_http_bytes_checked"] == sum(row["observed_bytes"] for row in expected_checks)
    assert audit["all_source_checks_canonical_fingerprint"] == canonical(expected_checks)
    assert audit["all_response_sha256_and_sizes_matched"]
    assert all(audit["recount_comparisons"].values()) and not audit["errors"]
    assert audit["audit_kind"] == "collection_author_offline_raw_rehash_recount_not_independent_review"
    assert audit["network_requests_performed"] == 0
    assert not audit["abi_source_pin_available_in_saved_data"]
    assert not audit["economic_or_attribution_semantics_certified"] and not audit["qualifies_t1"]
    for key in ("fill", "actor_refund_allocation", "receipt_pool_to_actor_transfer"):
        item = exported[key]
        entry = entries[item["source_response_name"]]
        assert item["source_response_sha256"] == entry["response_sha256"]
        assert item["source_response_bytes"] == entry["response_bytes"]
        assert item["object_fingerprint_kind"] == "sha256_canonical_json_not_http_bytes"
        raw = item["original_raw_object"]
        assert canonical(raw) == item["object_fingerprint"] and not raw["removed"]
        assert original["open_block_excluded"] < int(raw["blockNumber"], 16) <= original["close_block_included"]
    actor = original["actor_address"]
    actor_topic = "0x" + actor[2:].rjust(64, "0")
    fill = exported["fill"]["original_raw_object"]
    assert fill["address"] == original["spoke_pool"]
    assert fill["topics"][0] == TOPICS["fills"] and fill["topics"][3] == actor_topic
    data = bytes.fromhex(fill["data"][2:])
    assert len(data) == 480
    uint = lambda offset: int.from_bytes(data[offset:offset + 32], "big")
    decoded = previous["fill_boundaries"][0]
    assert fill["transactionHash"] == decoded["transaction_hash"]
    assert fill["logIndex"] == decoded["log_index"]
    assert uint(128) == decoded["repayment_chain_id"]
    assert uint(416) == int(decoded["actual_output_amount_raw"])
    assert uint(448) == decoded["fill_type"]
    assert int(fill["topics"][1], 16) == decoded["origin_chain_id"]
    assert int(fill["topics"][2], 16) == int(decoded["deposit_id"])

    refund = exported["actor_refund_allocation"]["original_raw_object"]
    assert refund["address"] == original["spoke_pool"] and refund["topics"][0] == TOPICS["refunds"]
    assert int(refund["topics"][1], 16) == 10
    data = bytes.fromhex(refund["data"][2:])
    assert len(data) % 32 == 0
    amount_offset, address_offset = uint(32), uint(96)
    assert min(amount_offset, address_offset) >= 192
    assert amount_offset % 32 == address_offset % 32 == 0
    count = uint(amount_offset)
    assert count == uint(address_offset) and count <= 1000
    assert max(amount_offset, address_offset) + 32 * (count + 1) <= len(data)
    amount = sum(
        uint(amount_offset + 32 * (i + 1)) for i in range(count)
        if uint(address_offset + 32 * (i + 1)) == int(actor, 16)
    )
    token = f"0x{uint(64):040x}"
    assert uint(128) == 0
    prior_refund = next(
        row for row in previous["refund_example_allocation_rows"]
        if row["token"] == token
    )
    assert str(amount) == prior_refund["allocated_amount_raw"]
    assert refund["transactionHash"] == prior_refund["transaction_hash"]
    assert refund["logIndex"] == prior_refund["log_index"]
    assert int(refund["topics"][2], 16) == prior_refund["root_bundle_id"]
    assert int(refund["topics"][3], 16) == prior_refund["leaf_id"]
    transfer = exported["receipt_pool_to_actor_transfer"]["original_raw_object"]
    assert transfer["address"] == token and len(bytes.fromhex(transfer["data"][2:])) == 32
    assert int(transfer["data"], 16) == amount
    assert transfer["topics"] == [
        "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
        "0x" + original["spoke_pool"][2:].rjust(64, "0"), actor_topic,
    ]
    for log in (refund, transfer):
        assert log["transactionHash"] == prior_refund["transaction_hash"]
        assert log["blockHash"] == exported["receipt_block_hash"]
        assert log["blockNumber"] == exported["receipt_block_number"]
    assert exported["receipt_from"] != actor
    return {
        "followup_revision": AUDIT_SOURCE_REVISION,
        "author_audit_metadata_internal_consistency": "PASS",
        "three_exported_raw_object_fingerprints_and_manifest_references": "PASS",
        "selected_declared_layout_and_USDC_transfer_consistency": "PASS",
        "independently_rehashed_or_recounted_bulk_bodies": False,
        "membership_in_absent_HTTP_pages_independently_verified": False,
        "historically_deployed_ABI_or_economic_payer_semantics_certified": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--include-raw-witness-followup", action="store_true")
    args = parser.parse_args()
    root = args.source_root.resolve()
    result = check(root)
    if args.include_raw_witness_followup:
        result["raw_witness_followup"] = check_raw_witness_followup(root)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
