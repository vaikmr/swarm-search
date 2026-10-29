#!/usr/bin/env python3
"""Public Hyperliquid info only. No exchange endpoint, keys or trading.

Funding-history sum on constant notional is a T4 sensitivity, not account PnL.
"""
import datetime as dt
import hashlib
import json
from pathlib import Path
import time
import urllib.request


def collect(coin, start, end):
    cursor, rows, pages = start, {}, []
    while cursor <= end:
        body = {"type": "fundingHistory", "coin": coin, "startTime": cursor, "endTime": end}
        req = urllib.request.Request("https://api.hyperliquid.xyz/info", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as res:
            raw = res.read()
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError("Unexpected funding response")
        pages.append({"request": body, "response_rows": len(data), "sha256": hashlib.sha256(raw).hexdigest()})
        if not data:
            break
        for row in data:
            if row["coin"] != coin or not start <= row["time"] <= end:
                raise ValueError("Unexpected funding row")
            rows[row["time"]] = row
        nxt = max(r["time"] for r in data) + 1
        if nxt <= cursor:
            raise ValueError("Non advancing page")
        cursor = nxt
        time.sleep(0.25)
    return sorted(rows.values(), key=lambda r: r["time"]), pages


def main():
    now = dt.datetime.now(dt.timezone.utc)
    end = int(now.timestamp() // 3600 * 3600000) - 1
    start = end - 90 * 86400000
    out = Path("strategies/funding-basis/evidence")
    out.mkdir(parents=True, exist_ok=True)
    summaries = []
    for coin in ("ETH", "BTC"):
        rows, pages = collect(coin, start, end)
        windows = {}
        for days in (30, 90):
            vals = [r for r in rows if end - days * 86400000 < r["time"] <= end]
            rates = [float(r["fundingRate"]) for r in vals]
            windows[str(days)] = {
                "rows": len(vals), "expected_hourly_rows": days * 24,
                "first_time": vals[0]["time"] if vals else None,
                "last_time": vals[-1]["time"] if vals else None,
                "hour_gaps": sum(b["time"] - a["time"] > 3700000 for a, b in zip(vals, vals[1:])),
                "sum_funding_fraction": sum(rates),
                "negative_hours": sum(v < 0 for v in rates),
                "gross_short_receipts_usd_constant_30000_notional": 30000 * sum(rates),
                "warning": "T4 constant USD notional funding-only arithmetic; excludes spot returns, basis, mark-to-market, fees, margin/liquidation, failures and infrastructure",
            }
        # Bounded compact observations make the arithmetic independently
        # reproducible offline; full API responses are represented by hashes.
        record = {"source": "https://api.hyperliquid.xyz/info", "retrieved_at": now.isoformat(), "start_ms": start, "end_ms": end, "coin": coin, "pages": pages, "windows": windows, "boundary_observations": rows[:2] + rows[-2:], "hourly_observation_columns": ["timestamp_ms", "funding_rate_fraction"], "hourly_observations": [[r["time"], r["fundingRate"]] for r in rows]}
        (out / (coin.lower() + "-funding-summary.json")).write_text(json.dumps(record, indent=2) + "\n")
        summaries.append(record)
        print(coin, json.dumps(windows))
    return summaries


if __name__ == "__main__":
    main()
