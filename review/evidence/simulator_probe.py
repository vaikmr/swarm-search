"""Independent probes of original simulator boundaries; not return evidence.

This historical reproducer requires the original module blobs, even if invoked
from a later review checkout. Pass --reviewed-root for a pinned historical worktree.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys


def git_blob_id(content):
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviewed-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    root = args.reviewed_root.resolve()
    expected = {
        "research_tools/replay.py": "364980e92cefe85bc703382edb5e22462be8656d",
        "research_tools/yield_data.py": "9d240ba70f6651ce51187dd12b4ced2b0c09e925",
    }
    for name, digest in expected.items():
        if git_blob_id((root / name).read_bytes()) != digest:
            raise SystemExit(
                "Historical probe requires original e716c89 simulator blobs. "
                "Use --reviewed-root with a pinned historical worktree, "
                "not corrected HEAD."
            )
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(root / "tests"))
    from research_tools.evidence import EvidenceError
    from research_tools.replay import ReplayInput
    from research_tools.yield_data import funding_carry
    from test_replay import fixture

    rows = [{"time": 3600000, "fundingRate": ".0001"}]
    incomplete = funding_carry(rows, 1, 7200000, 10000, None)
    complete = funding_carry(
        rows + [{"time": 7200000, "fundingRate": "-.0002"}],
        1, 7200000, 10000, None,
    )
    assert incomplete["payments"] == 1
    assert incomplete["gross_short_funding_usd"] == 1
    assert complete["gross_short_funding_usd"] == -1
    assert incomplete["net_component_after_explicit_costs_only_usd"] is None

    row = fixture()
    item = row["opportunities"][0]
    item["settlement_at"] = "2026-10-02T00:00:00Z"
    item["marks"][-1]["at"] = item["settlement_at"]
    item["marks"].insert(0, {
        "at": "2026-09-30T12:00:00Z",
        "cumulative_gross_pnl_usd": "-6000",
    })
    try:
        ReplayInput.parse(row)
    except EvidenceError as exc:
        open_position_error = str(exc)
    else:
        raise AssertionError("Original closed-position-only rejection not reproduced")

    sample = json.loads(
        (root / "research_tools/yield_funding_sample_20261029.json").read_text()
    )
    coverage = {}
    for name, comparator in sample["comparators"].items():
        start, end = comparator["start_ms"], comparator["end_ms"]
        stamps = [
            item[0] for item in sample["compact_input_rows"]
            if start <= item[0] <= end
        ]
        expected_hours = set(range(math.ceil(start / 3600000), math.floor(end / 3600000) + 1))
        actual_hours = {stamp // 3600000 for stamp in stamps}
        assert actual_hours == expected_hours
        assert len(stamps) == len(actual_hours)
        coverage[name] = {
            "input_observation_count": len(stamps),
            "expected_hour_buckets": len(expected_hours),
            "missing_extra_or_duplicate_buckets": False,
            "not_strategy_performance_evidence": True,
        }

    print(json.dumps({
        "synthetic_probe_tier": "T4",
        "not_strategy_performance_evidence": True,
        "reviewed_integrated_revision": "e716c892b29cdf0074aa402e1a4c3e3a50e19204",
        "synthetic_funding_edge": {
            "omitted_boundary_event_accepted": True,
            "incomplete_component_usd": incomplete["gross_short_funding_usd"],
            "complete_component_usd": complete["gross_short_funding_usd"],
        },
        "synthetic_open_position_rejection": open_position_error,
        "committed_source_input_hour_coverage": coverage,
    }, indent=2))


if __name__ == "__main__":
    main()
