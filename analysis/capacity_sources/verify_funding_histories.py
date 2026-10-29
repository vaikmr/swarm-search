"""Independently sum public hourly rows at an immutable research commit.

Offline, read-only git-object access. No account, network, orders or private keys.
If the source object is absent: git fetch origin scout/yield-evidence
This verifies arithmetic, not market fills or a strategy's net return.
"""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import math
from pathlib import Path
import subprocess


SOURCE_COMMIT = "0767bcc1cb2b01d3dfc732fc7ed3c8b9f625652f"
ROOT = Path(__file__).resolve().parents[2]
DAY_MS = 86_400_000


def validated_records(rows):
    records = []
    previous = None
    for timestamp, rate_text in rows:
        if type(timestamp) is not int or (previous is not None and timestamp <= previous):
            raise ValueError("timestamps must be integer milliseconds, unique and increasing")
        rate = Decimal(str(rate_text))
        if not rate.is_finite():
            raise ValueError("funding rate must be finite")
        records.append((timestamp, rate))
        previous = timestamp
    return records


def iso(timestamp):
    return datetime.fromtimestamp(timestamp / 1000, timezone.utc).isoformat()


def source_bytes(path):
    return subprocess.check_output(
        ["git", "show", f"{SOURCE_COMMIT}:{path}"], cwd=ROOT
    )


def verify_asset(asset):
    path = f"strategies/funding-basis/evidence/{asset.lower()}-funding-summary.json"
    raw = source_bytes(path)
    data = json.loads(raw)
    rows = validated_records(data["hourly_observations"])
    if data["coin"] != asset:
        raise ValueError("source asset mismatch")
    if len(rows) != 2160:
        raise ValueError("expected source's complete 90-day hourly series")
    windows = {}
    for days in (30, 90):
        end = data["end_ms"]
        start = end - days * DAY_MS
        selected = [(t, r) for t, r in rows if start < t <= end]
        count = len(selected)
        if count != days * 24:
            raise ValueError(f"{days}-day window has missing or extra hourly rows")
        if max(b[0] - a[0] for a, b in zip(selected, selected[1:])) > 3_700_000:
            raise ValueError("hourly gap exceeded source completeness threshold")
        total = sum((r for _, r in selected), Decimal(0))
        reported = data["windows"][str(days)]
        if not math.isclose(
            float(total), reported["sum_funding_fraction"], rel_tol=0, abs_tol=1e-15
        ):
            raise ValueError("reported funding sum does not reproduce")
        receipts = total * Decimal(30000)
        if not math.isclose(
            float(receipts),
            reported["gross_short_receipts_usd_constant_30000_notional"],
            rel_tol=0,
            abs_tol=1e-9,
        ):
            raise ValueError("reported constant-notional receipts do not reproduce")
        negatives = sum(rate < 0 for _, rate in selected)
        if negatives != reported["negative_hours"]:
            raise ValueError("negative-funding count does not reproduce")
        windows[str(days)] = {
            "start_exclusive_utc": iso(start),
            "end_inclusive_utc": iso(end),
            "hourly_rows": count,
            "negative_hours": negatives,
            "sum_funding_fraction": str(total),
            "gross_funding_usd_on_constant_30000_notional": str(receipts),
        }
        if days == 30:
            windows["30"]["required_notional_at_same_historical_sum"] = [
                {
                    "net_target_usd": target,
                    "fixed_cost_ceiling_scenario_usd": 500,
                    "notional_usd_before_other_costs":
                        str(Decimal(target + 500) / total) if total > 0 else None,
                }
                for target in (2000, 5000)
            ]
    return {
        "asset": asset,
        "source_path": path,
        "source_blob_sha256": hashlib.sha256(raw).hexdigest(),
        "source_url":
            f"https://github.com/vaikmr/swarm-search/blob/{SOURCE_COMMIT}/{path}",
        "underlying_public_endpoint": data["source"],
        "source_retrieved_at": data["retrieved_at"],
        "windows": windows,
    }


def build_output():
    return {
        "tier": "T4 independent arithmetic on sourced hourly funding rates",
        "source_commit": SOURCE_COMMIT,
        "not_strategy_pnl": True,
        "limitations": [
            "Constant USD notional would require a separate execution and rebalancing model.",
            "No spot/basis PnL, fee, margin path, funding liquidity or live account is verified.",
            "Required notionals are counterfactual capacity requirements, not executable allocations.",
            "The $500 fixed-cost input is the budget-ceiling scenario, not an actual expense.",
            "This is not T1, T2, T3, a current-rate forecast or a global funding-strategy bound."
        ],
        "assets": [verify_asset(asset) for asset in ("BTC", "ETH")],
    }


if __name__ == "__main__":
    print(json.dumps(build_output(), indent=2, allow_nan=False))
