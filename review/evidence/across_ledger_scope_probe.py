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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(check(args.source_root.resolve()), indent=2))


if __name__ == "__main__":
    main()
