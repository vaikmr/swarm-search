#!/usr/bin/env python3
"""Read-only public-rate collector. Never signs, builds, or submits transactions.

Historical rate arithmetic is T4, NOT wallet PnL, fork replay, or paper trading.
Uses only Python's standard library. Run from the repository root.
"""
import argparse
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import urllib.request
from concurrent.futures import ThreadPoolExecutor

POOLS = {
    "aave-ethereum-usdc": "aa70268e-4b52-42bf-a116-608b370f9501",
    "aave-ethereum-usdt": "f981a304-bb6c-45b8-b0c5-fd2f515ad23a",
    "aave-ethereum-dai": "3665ee7e-6c5d-49d9-abb7-c47ab5d9d4ac",
    "aave-arbitrum-usdc": "d9fa8e14-0447-4207-9ae8-7810199dfa1f",
    "aave-base-usdc": "7e0661bf-8cf3-45e6-9424-31916d4c7b84",
    "compound-ethereum-usdc": "7da72d09-56ca-4ec5-a45f-59114353e487",
    "compound-ethereum-usdt": "f4d5b566-e815-4ca2-bb07-7bcd8bc797f1",
    "compound-base-usdc": "0c8567f8-ba5b-41ad-80de-00a71895eb19",
    "compound-arbitrum-usdt": "85247b13-8180-44e7-b38c-4d324cc68a92",
    "morpho-base-sparkusdc": "a5fab52f-73fa-4f44-9c09-9af1eb20996c",
    "morpho-base-steakusdc": "ba68527f-8ec2-4c55-827a-8f4673ae047c",
}


def fetch(url):
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "public-yield-research/1.0"}),
        timeout=90,
    ) as res:
        raw = res.read()
    return raw, json.loads(raw)


def stamp(value):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def integrate(rows, start, end, field):
    """Piecewise-constant APY; do not interpolate or substitute missing fields."""
    ordered = sorted(rows, key=lambda r: r["timestamp"])
    log_return = covered = 0.0
    intervals = []
    for i, row in enumerate(ordered):
        left = max(start, stamp(row["timestamp"]))
        right = min(end, stamp(ordered[i + 1]["timestamp"]) if i + 1 < len(ordered) else end)
        seconds = (right - left).total_seconds()
        if seconds <= 0:
            continue
        # Refuse to carry sparse observations over a large gap.
        if seconds > 36 * 3600 or row.get(field) is None:
            continue
        value = float(row[field])
        if value <= -100:
            raise ValueError("invalid APY")
        log_return += math.log1p(value / 100) * seconds / (365 * 86400)
        covered += seconds
        intervals.append((value, seconds))
    return {
        "coverage_fraction": covered / (end - start).total_seconds(),
        "time_weighted_mean_apy_pct": sum(v * s for v, s in intervals) / covered if covered else None,
        "implied_gross_return_pct": math.expm1(log_return) * 100,
        "gross_usd_on_50000": math.expm1(log_return) * 50000,
        "warning": "T4 piecewise APY arithmetic; missing coverage is not zero yield; no fees, depeg, default or fill model",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="strategies/benchmark-lending/evidence")
    parser.add_argument("--cached-pools", type=Path)
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    retrieved = dt.datetime.now(dt.timezone.utc).isoformat()
    pool_observed = dt.datetime.fromtimestamp(args.cached_pools.stat().st_mtime, dt.timezone.utc).isoformat() if args.cached_pools else retrieved
    raw, pools = (args.cached_pools.read_bytes(), json.loads(args.cached_pools.read_text())) if args.cached_pools else fetch("https://yields.llama.fi/pools")
    selected = {r["pool"]: r for r in pools["data"] if r["pool"] in POOLS.values()}
    (out / "selected-pools.json").write_text(json.dumps({"built_at": retrieved, "source_observed_at": pool_observed, "source_observed_at_basis": "cached response filesystem mtime" if args.cached_pools else "request start", "source_response_sha256": hashlib.sha256(raw).hexdigest(), "source": "https://yields.llama.fi/pools", "data": list(selected.values())}, indent=2) + "\n")
    manifest, summary = [], []

    def one(item):
        label, pool = item
        url = "https://yields.llama.fi/chart/" + pool
        body, data = fetch(url)
        return label, pool, url, body, data

    for label, pool, url, body, data in ThreadPoolExecutor(max_workers=3).map(one, POOLS.items()):
        rows = data["data"]
        end = stamp(rows[-1]["timestamp"])
        # Keep a compact public excerpt: 90 days plus the immediately preceding
        # observation needed to cover the left boundary. Full response hash is
        # retained for provenance; never commit unbounded source datasets.
        lower = end - dt.timedelta(days=90)
        before = [r for r in rows if stamp(r["timestamp"]) < lower]
        excerpt = before[-1:] + [r for r in rows if stamp(r["timestamp"]) >= lower]
        filename = label + "-history.json"
        (out / filename).write_text(json.dumps({"status": data["status"], "data": excerpt}, separators=(",", ":")) + "\n")
        entry = {"label": label, "pool": pool, "latest_data_timestamp": rows[-1]["timestamp"], "current": selected.get(pool), "source": url, "tier": "T4", "windows": {}}
        for days in (30, 90):
            start = end - dt.timedelta(days=days)
            entry["windows"][str(days)] = {
                "start": start.isoformat(), "end": end.isoformat(),
                "base": integrate(rows, start, end, "apyBase"),
                "total": integrate(rows, start, end, "apy"),
            }
        summary.append(entry)
        manifest.append({"file": filename, "source": url, "retrieved_at": dt.datetime.now(dt.timezone.utc).isoformat(), "full_response_sha256": hashlib.sha256(body).hexdigest(), "full_response_rows": len(rows), "retained_rows": len(excerpt), "retained_sha256": hashlib.sha256((out / filename).read_bytes()).hexdigest()})
    (out / "rate-summary.json").write_text(json.dumps({"retrieved_at": retrieved, "tier": "T4", "data": summary}, indent=2) + "\n")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for row in summary:
        print(row["label"], "current", row["current"]["apyBase"], "30d", row["windows"]["30"]["base"], "90d", row["windows"]["90"]["base"])


if __name__ == "__main__":
    main()
