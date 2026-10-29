"""Public read-only data adapters and explicitly T4 carry calculations.

No wallets, credentials, signing, transaction payloads, or exchange endpoints.
Historical rate integration is NOT a fork replay and must never be labeled T2.
"""

import argparse
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import re
import time
import urllib.request

UTC = dt.timezone.utc
YEAR_SECONDS = 365 * 86400
HL_INFO = "https://api.hyperliquid.xyz/info"
LLAMA = "https://yields.llama.fi"
MAX_BYTES = 20_000_000


class DataError(ValueError):
    """Missing, invalid, incomplete, or stale public input."""


def iso_now():
    return dt.datetime.now(UTC).isoformat()


def timestamp(value):
    if not isinstance(value, str):
        raise DataError("ISO source timestamp required")
    result = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise DataError("timezone required")
    return result.timestamp()


def finite(value, name, minimum=None):
    if isinstance(value, bool) or value is None:
        raise DataError(f"{name} missing or invalid")
    try:
        result = float(value)
    except (ValueError, TypeError) as exc:
        raise DataError(f"{name} invalid") from exc
    if not math.isfinite(result) or (minimum is not None and result < minimum):
        raise DataError(f"{name} outside permitted range")
    return result


class PublicData:
    """Allowlisted HTTPS market-data requests; POST /info is a read operation."""

    def __init__(self, timeout=20, opener=urllib.request.urlopen):
        self.timeout = timeout
        self.opener = opener

    def _read(self, url, body=None):
        get_ok = url == LLAMA + "/pools" or re.fullmatch(
            re.escape(LLAMA) + r"/chart/[a-f0-9-]{36}", url
        )
        info_ok = url == HL_INFO and isinstance(body, dict) and body.get("type") in {
            "metaAndAssetCtxs", "l2Book", "fundingHistory"
        }
        coinbase_ok = url == (
            "https://api.exchange.coinbase.com/products/BTC-USD/book?level=2"
        ) and body is None
        if not ((get_ok and body is None) or info_ok or coinbase_ok):
            raise DataError("non-allowlisted public data request")
        request = urllib.request.Request(
            url,
            data=None if body is None else json.dumps(body).encode(),
            headers={"User-Agent": "swarm-search-research/0.1",
                     "Content-Type": "application/json"},
        )
        started = iso_now()
        before = time.monotonic()
        with self.opener(request, timeout=self.timeout) as response:
            # Reject redirects out of the allowlist, even for public reads.
            if response.geturl() != url:
                raise DataError("redirect rejected")
            raw = response.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise DataError("response too large")
            server_date = response.headers.get("Date")
            status = response.status
        payload = json.loads(raw)
        return {
            "url": url, "request_body": body, "http_status": status,
            "http_date": server_date, "requested_at": started,
            "received_at": iso_now(), "latency_ms": (time.monotonic() - before) * 1000,
            "sha256": hashlib.sha256(raw).hexdigest(), "payload": payload,
            "evidence_class": "public_source_input_not_strategy_evidence",
        }

    def pools(self):
        return self._read(LLAMA + "/pools")

    def chart(self, pool):
        if not re.fullmatch(r"[a-f0-9-]{36}", pool):
            raise DataError("invalid pool id")
        return self._read(LLAMA + "/chart/" + pool)

    def book(self, coin="BTC"):
        if coin not in {"BTC", "ETH"}:
            raise DataError("only BTC/ETH enabled")
        return self._read(HL_INFO, {"type": "l2Book", "coin": coin})

    def meta(self):
        return self._read(HL_INFO, {"type": "metaAndAssetCtxs"})

    def coinbase_btc_book(self):
        return self._read(
            "https://api.exchange.coinbase.com/products/BTC-USD/book?level=2"
        )

    def funding_history(self, coin, start_ms, end_ms, max_pages=20):
        if coin not in {"BTC", "ETH"} or not 0 <= start_ms < end_ms:
            raise DataError("invalid funding range")
        if not 1 <= max_pages <= 20:
            raise DataError("page bound invalid")
        cursor, envelopes, rows = start_ms, [], []
        for _ in range(max_pages):
            envelope = self._read(HL_INFO, {
                "type": "fundingHistory", "coin": coin,
                "startTime": cursor, "endTime": end_ms,
            })
            page = envelope["payload"]
            envelopes.append(envelope)
            if not isinstance(page, list):
                raise DataError("funding response must be a list")
            if not page:
                break
            previous = cursor - 1
            for row in page:
                stamp = int(row["time"])
                if row.get("coin") != coin or not cursor <= stamp <= end_ms:
                    raise DataError("funding coin/time mismatch")
                if stamp <= previous:
                    raise DataError("non-increasing funding page")
                finite(row.get("fundingRate"), "fundingRate")
                previous = stamp
                rows.append(row)
            cursor = previous + 1  # endpoint is inclusive
            if len(page) < 500 or cursor > end_ms:
                break
        else:
            raise DataError("funding pagination limit reached; incomplete")
        # Completeness is checked separately; no empty response means success.
        return {"coin": coin, "start_ms": start_ms, "end_ms": end_ms,
                "requests": envelopes, "rows": rows}


def lending_points(payload):
    if payload.get("status") != "success" or not isinstance(payload.get("data"), list):
        raise DataError("invalid chart response")
    points = []
    for row in payload["data"]:
        stamp = timestamp(row.get("timestamp"))
        apy = finite(row.get("apyBase"), "apyBase", minimum=0)
        points.append((stamp, apy))
    if not points or any(b[0] <= a[0] for a, b in zip(points, points[1:])):
        raise DataError("empty, duplicated, or non-increasing chart")
    return points


def lending_carry(points, start_s, end_s, capital_usd, costs_usd, max_gap_s=36*3600):
    """Left-continuous APY integration, base only, fixed $1 stablecoin model.

    Explicit costs are caller inputs, not verified observations. Rewards,
    depegs, fees, caps, protocol availability and liquidity-index path are not
    reconstructed: this calculation remains T4 even with historical inputs.
    """
    capital_usd = finite(capital_usd, "capital", minimum=0)
    costs_usd = None if costs_usd is None else finite(costs_usd, "costs", minimum=0)
    if not points or end_s <= start_s or max_gap_s <= 0:
        raise DataError("invalid carry interval")
    for stamp, apy in points:
        finite(stamp, "sample time", minimum=0)
        finite(apy, "APY", minimum=0)
    if any(b[0] <= a[0] for a, b in zip(points, points[1:])):
        raise DataError("non-increasing lending points")
    if points[0][0] > start_s or points[-1][0] < end_s:
        raise DataError("history does not bracket full window; no extrapolation")
    log_growth, used = 0.0, 0
    for (left, apy), (right, _) in zip(points, points[1:]):
        a, b = max(left, start_s), min(right, end_s)
        if a >= b:
            continue
        if right - left > max_gap_s:
            raise DataError("lending sample gap too large")
        log_growth += math.log1p(apy / 100) * (b - a) / YEAR_SECONDS
        used += 1
    gross = capital_usd * math.expm1(log_growth)
    return {
        "evidence_tier": "T4", "calculation": "historical_base_APY_integration",
        "capital_usd": capital_usd, "window_days": (end_s-start_s)/86400,
        "start_s": start_s, "end_s": end_s,
        "gross_carry_usd": gross, "explicit_costs_usd": costs_usd,
        "net_after_explicit_costs_only_usd": None if costs_usd is None else gross-costs_usd,
        "costs_status": "unknown" if costs_usd is None else "caller_supplied_only",
        "intervals_used": used,
        "not_T2_reason": "No fork, index-state, withdrawal, gas or competition replay",
        "excludes": ["depeg", "reward tokens", "default", "liquidity/cap constraints"],
    }


def funding_carry(rows, start_ms, end_ms, notional_usd, costs_usd,
                  period_ms=3600000, tolerance_ms=120000):
    """Gross short-side funding component only, not a delta-neutral backtest."""
    notional_usd = finite(notional_usd, "notional", minimum=0)
    costs_usd = None if costs_usd is None else finite(costs_usd, "costs", minimum=0)
    if end_ms <= start_ms or period_ms <= 0 or tolerance_ms < 0:
        raise DataError("invalid funding interval")
    stamps, rate_sum = [], 0.0
    for row in rows:
        stamp = int(row["time"])
        if not start_ms <= stamp <= end_ms:
            raise DataError("funding outside requested window")
        stamps.append(stamp)
        rate_sum += finite(row.get("fundingRate"), "fundingRate")
    if not stamps:
        raise DataError("no funding history")
    if stamps[0]-start_ms > period_ms+tolerance_ms or end_ms-stamps[-1] > period_ms+tolerance_ms:
        raise DataError("funding history truncated at window edge")
    if any(not period_ms-tolerance_ms <= b-a <= period_ms+tolerance_ms
           for a, b in zip(stamps, stamps[1:])):
        raise DataError("missing, duplicate or non-hourly funding data")
    gross = notional_usd * rate_sum
    return {
        "evidence_tier": "T4", "calculation": "funding_component_only",
        "constant_short_notional_usd": notional_usd,
        "start_ms": start_ms, "end_ms": end_ms,
        "window_days": (end_ms-start_ms)/86400000, "payments": len(rows),
        "funding_rate_sum": rate_sum, "gross_short_funding_usd": gross,
        "explicit_costs_usd": costs_usd,
        "net_component_after_explicit_costs_only_usd": (
            None if costs_usd is None else gross-costs_usd),
        "costs_status": "unknown" if costs_usd is None else "caller_supplied_only",
        "not_strategy_PnL": True,
        "excludes": ["spot/perp basis", "spot carry", "mark-to-market",
                     "liquidation", "fees not explicitly supplied", "fills"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    chart = sub.add_parser("chart")
    chart.add_argument("pool")
    chart.add_argument("--out", required=True)
    funding = sub.add_parser("funding")
    funding.add_argument("--coin", choices=["BTC", "ETH"], required=True)
    funding.add_argument("--days", type=int)
    funding.add_argument("--start-ms", type=int)
    funding.add_argument("--end-ms", type=int)
    funding.add_argument("--out", required=True)
    args = parser.parse_args()
    client = PublicData()
    if args.action == "chart":
        result = client.chart(args.pool)
        lending_points(result["payload"])
    else:
        if args.start_ms is not None or args.end_ms is not None:
            if args.start_ms is None or args.end_ms is None or args.days is not None:
                parser.error("pass both timestamp bounds, without --days")
            start, end = args.start_ms, args.end_ms
        else:
            days = args.days if args.days is not None else 30
            if not 1 <= days <= 180:
                parser.error("--days must be 1..180")
            end = int(time.time()*1000)
            start = end-days*86400000
        result = client.funding_history(args.coin, start, end)
    Path(args.out).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"saved": args.out, "evidence_tier": "input_only"}))


if __name__ == "__main__":
    main()
