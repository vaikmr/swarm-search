"""Bounded public GET scout. No keys, signing, trading, or transaction submission.

Outputs are discovery samples, never actor PnL, a replay, or paper-trade results.
Run from repository root; default output is an ignored data directory.
"""

import argparse
import concurrent.futures
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ENDPOINTS = {
    "across_fills": "https://app.across.to/api/deposits?limit=50",
    "across_configs": (
        "https://raw.githubusercontent.com/across-protocol/"
        "exclusive-relayer-configs/master/build/exclusive-relayer-configs.json"
    ),
    "across_registrations": (
        "https://api.github.com/repos/across-protocol/"
        "relayer-registration-repository/contents/relayer_registration"
    ),
    "uniswapx_base": (
        "https://api.uniswap.org/v2/orders?"
        "orderStatus=filled&chainId=8453&orderType=Dutch_V3&limit=20"
    ),
}
ACROSS_FIELDS = (
    "id", "relayHash", "depositId", "originChainId", "destinationChainId",
    "inputToken", "inputAmount", "outputToken", "outputAmount", "exclusiveRelayer",
    "exclusivityDeadline", "quoteTimestamp", "depositTxHash", "depositBlockNumber",
    "depositBlockTimestamp", "status", "relayer", "fillBlockNumber",
    "fillBlockTimestamp", "fillTx", "bridgeFeeUsd", "fillGasFeeUsd",
)
ORDER_FIELDS = (
    "type", "orderStatus", "chainId", "txHash", "fillBlock", "fillTimestamp",
    "orderHash", "createdAt", "settledAmounts",
)


def select_payload(name, body):
    """Explicit field selection avoids persisting signatures or order calldata."""
    if name == "across_fills":
        if not isinstance(body, list):
            raise ValueError("Across deposits must be an array")
        return [{key: row.get(key) for key in ACROSS_FIELDS} for row in body]
    if name == "uniswapx_base":
        if not isinstance(body, dict) or not isinstance(body.get("orders"), list):
            raise ValueError("UniswapX response must contain orders")
        rows = []
        for order in body["orders"]:
            selected = {key: order.get(key) for key in ORDER_FIELDS}
            selected["exclusive_filler"] = (order.get("cosignerData") or {}).get(
                "exclusiveFiller"
            )
            rows.append(selected)
        return rows
    if name == "across_registrations":
        if not isinstance(body, list):
            raise ValueError("Registration directory must be an array")
        return [
            {"name": row.get("name"), "sha": row.get("sha"),
             "source_url": row.get("html_url"), "type": row.get("type")}
            for row in body
        ]
    if name == "across_configs":
        if not isinstance(body, (dict, list)):
            raise ValueError("Config payload must be an object or array")
        return body
    raise ValueError("Unknown fixed endpoint")


def summarize(name, selected):
    if name == "across_fills":
        actors = Counter(row["relayer"].lower() for row in selected if row["relayer"])
        times = [row["depositBlockTimestamp"] for row in selected
                 if row["depositBlockTimestamp"]]
        return {
            "sample_rows": len(selected),
            "filled_rows": sum(row["status"] == "filled" for row in selected),
            "filled_rows_missing_relayer": sum(
                row["status"] == "filled" and not row["relayer"] for row in selected
            ),
            "relayer_counts_in_sample_only": dict(actors),
            "deposit_timestamp_min": min(times) if times else None,
            "deposit_timestamp_max": max(times) if times else None,
            "warning": "Latest-deposit sample, not market share or profits.",
        }
    if name == "uniswapx_base":
        empty = {None, "", "0x0000000000000000000000000000000000000000"}
        actors = Counter(row["exclusive_filler"].lower() for row in selected
                         if row["exclusive_filler"] not in empty)
        return {
            "sample_rows": len(selected),
            "exclusive_filler_counts_in_sample_only": dict(actors),
            "orders_without_exclusive_filler": sum(
                row["exclusive_filler"] in empty for row in selected
            ),
            "warning": "Nominee is not proof of actual executor; no PnL.",
        }
    if name == "across_registrations":
        return {
            "file_count": sum(row["type"] == "file" for row in selected),
            "example_files": [row["name"] for row in selected
                              if "example" in (row["name"] or "").lower()],
            "warning": "Do not count example configurations as active actors.",
        }
    return {
        "top_level_type": type(selected).__name__,
        "top_level_count": len(selected),
        "warning": "Configuration entries are not active competitor counts.",
    }


def fetch(name):
    url = ENDPOINTS[name]
    stamp = datetime.now(timezone.utc).isoformat()
    result = {
        "source_url": url, "retrieved_at_utc": stamp, "method": "GET",
        "evidence_kind": "public_discovery_sample_not_T1_T2_or_T3",
        "realized_pnl_usd": None, "capital_deployed_usd": None,
        "qualifies_t1": False,
    }
    try:
        req = Request(url, headers={"User-Agent": "swarm-search-public-research/1.0"})
        with urlopen(req, timeout=30) as response:
            raw = response.read(2_000_001)
            if len(raw) > 2_000_000:
                raise ValueError("Response exceeded bounded discovery limit")
            result["http_status"] = response.status
            result["server_date"] = response.headers.get("Date")
        selected = select_payload(name, json.loads(raw))
        result["upstream_body_sha256"] = hashlib.sha256(raw).hexdigest()
        result["selected_records"] = selected
        result["summary"] = summarize(name, selected)
        result["ok"] = True
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError) as exc:
        result["ok"] = False
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("data/raw/scout-execution"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(fetch, ENDPOINTS))
    for name, result in zip(ENDPOINTS, results):
        path = args.output_dir / f"{name}.json"
        path.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({"name": name, "ok": result["ok"],
                          "summary": result.get("summary"), "error": result.get("error")}))


if __name__ == "__main__":
    main()
