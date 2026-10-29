"""Bounded, public, read-only availability probe for one Across relayer.

This collects one chain's historical events and selected inventory, NOT actor PnL.
Run from repository root. Raw records stay in ignored data/raw/; summary.json is
small enough to review separately. No dependency outside Python's standard library.
"""

import argparse
import hashlib
import json
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

RPC = "https://mainnet.optimism.io"
ACTOR = "0x07ae8551be970cb1cca11dd7a11f47ae82e70e67"
POOL = "0x6f26bf09b1c792e3228e5467807a900a503c0281"
OPEN_BLOCK = 158224884
CLOSE_BLOCK = 158829684
PAGE_SIZE = 10000
FILL = "0x44b559f101f8fbcc8a0ea43fa91a05a729a5ea6e14a7c75aa750374690137208"
REFUND = "0xf4ad92585b1bc117fbdd644990adf0827bc4c95baeae8a23322af807b6d0020e"
TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
REFUND_EXAMPLE = "0x5bd36a12ca618cf6e3d406d9352207fd6c413f323ced70dfc4768523e9e953e6"
TOKENS = {
    "USDC": "0x0b2c639c533813f4aa9d7837caf62653d097ff85",
    "WETH": "0x4200000000000000000000000000000000000006",
    "bridged_USDT": "0x94b008aa00579c1307b0ef2c499ad98a8ce58e58",
}
ALLOWED = {
    "eth_getBlockByNumber", "eth_getBalance", "eth_getTransactionCount",
    "eth_getCode", "eth_call", "eth_getLogs", "eth_getTransactionReceipt",
}
SOURCE_URLS = [
    "https://docs.across.to/api-reference/deposits/get",
    "https://docs.across.to/concepts/intent-lifecycle-in-across",
    "https://docs.across.to/reference/contract-addresses",
    "https://raw.githubusercontent.com/across-protocol/contracts/master/contracts/interfaces/V3SpokePoolInterface.sol",
    "https://raw.githubusercontent.com/across-protocol/contracts/master/contracts/spoke-pools/SpokePool.sol",
    "https://optimistic.etherscan.io/tx/" + REFUND_EXAMPLE + "#eventlog",
]


def address_word(address):
    return "0x" + address.removeprefix("0x").lower().rjust(64, "0")


def ranges(start, end, size=PAGE_SIZE):
    if size <= 0 or start > end:
        raise ValueError("Invalid pagination range")
    return [(lo, min(lo + size - 1, end)) for lo in range(start, end + 1, size)]


def words(data):
    raw = bytes.fromhex(data.removeprefix("0x"))
    if len(raw) % 32:
        raise ValueError("Non-word-aligned event data")
    return [raw[i:i + 32].hex() for i in range(0, len(raw), 32)]


def evm_address(word):
    if len(word) != 64 or int(word[:24], 16) != 0:
        raise ValueError("Not an EVM address word")
    return "0x" + word[24:].lower()


def decode_fill(log):
    if log["address"].lower() != POOL or log["topics"][0].lower() != FILL:
        raise ValueError("Unexpected fill source/topic")
    if len(log["topics"]) != 4 or log["topics"][3].lower() != address_word(ACTOR):
        raise ValueError("Unexpected actor attribution")
    w = words(log["data"])
    if len(w) != 15:
        raise ValueError("Unsupported fill event layout")
    return {
        "transaction_hash": log["transactionHash"], "log_index": log["logIndex"],
        "block_number": int(log["blockNumber"], 16),
        "input_token": evm_address(w[0]), "output_token": evm_address(w[1]),
        "input_amount_raw": str(int(w[2], 16)),
        "original_output_amount_raw": str(int(w[3], 16)),
        "repayment_chain_id": int(w[4], 16),
        "origin_chain_id": int(log["topics"][1], 16),
        "deposit_id": str(int(log["topics"][2], 16)),
        "actual_output_amount_raw": str(int(w[13], 16)),
        "fill_type": int(w[14], 16),
    }


def decode_refund(log):
    if log["address"].lower() != POOL or log["topics"][0].lower() != REFUND:
        raise ValueError("Unexpected refund source/topic")
    if len(log["topics"]) != 4 or int(log["topics"][1], 16) != 10:
        raise ValueError("Unexpected refund chain")
    w = words(log["data"])
    if len(w) < 8:
        raise ValueError("Truncated refund event")

    def array(offset_word):
        offset = int(offset_word, 16)
        if offset % 32 or offset < 192 or offset // 32 >= len(w):
            raise ValueError("Invalid refund array offset")
        base = offset // 32
        count = int(w[base], 16)
        if count > 1000 or base + 1 + count > len(w):
            raise ValueError("Invalid refund array length")
        return w[base + 1:base + 1 + count]

    amounts, addresses = array(w[1]), array(w[3])
    if len(amounts) != len(addresses) or int(w[4], 16) not in (0, 1):
        raise ValueError("Invalid refund array/flag")
    actor_amount = sum(
        int(amount, 16) for amount, address in zip(amounts, addresses)
        if evm_address(address) == ACTOR
    )
    if not actor_amount:
        return None
    return {
        "transaction_hash": log["transactionHash"], "log_index": log["logIndex"],
        "block_number": int(log["blockNumber"], 16),
        "root_bundle_id": int(log["topics"][2], 16),
        "leaf_id": int(log["topics"][3], 16),
        "token": evm_address(w[2]), "allocated_amount_raw": str(actor_amount),
        # True means at least one refund in the entire batch was deferred.
        # Neither this flag nor an allocation alone certifies actor cash receipt.
        "any_batch_refunds_deferred": bool(int(w[4], 16)),
        "cash_receipt_independently_verified": False,
    }


def confirmed_transfers(receipt):
    """Only actual successful receipt transfers from this pool to this actor."""
    if receipt.get("status") != "0x1":
        return []
    result = []
    for log in receipt.get("logs", []):
        t = [topic.lower() for topic in log.get("topics", [])]
        if len(t) == 3 and t == [TRANSFER, address_word(POOL), address_word(ACTOR)]:
            w = words(log["data"])
            if len(w) != 1:
                raise ValueError("Invalid ERC20 transfer amount")
            result.append({
                "transaction_hash": receipt["transactionHash"],
                "log_index": log["logIndex"], "token": log["address"].lower(),
                "amount_raw": str(int(w[0], 16)),
            })
    return result


class PublicProbe:
    def __init__(self, output_dir):
        self.output = Path(output_dir)
        self.output.mkdir(parents=True, exist_ok=True)
        self.manifest = []
        self.lock = threading.Lock()
        self.last_call = 0.0
        self.calls = 0

    def request(self, name, method, params=None, url=RPC):
        if method != "GET" and method not in ALLOWED:
            raise ValueError("Method not permitted by read-only probe")
        if method == "eth_call":
            for call in params[:1]:
                if call.get("data", "")[:10] not in {"0x70a08231", "0x313ce567"}:
                    raise ValueError("Only balanceOf/decimals calls are permitted")
        with self.lock:
            if self.calls >= 160:
                raise ValueError("Bounded probe request budget exhausted")
            delay = max(0, 0.35 - (time.monotonic() - self.last_call))
            time.sleep(delay)
            self.last_call = time.monotonic()
            self.calls += 1
        meta = {
            "name": name, "source_url": url, "method": method, "params": params,
            "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        }
        data = None if method == "GET" else json.dumps({
            "jsonrpc": "2.0", "id": 1, "method": method, "params": params,
        }).encode()
        req = Request(url, data=data, headers={
            "Content-Type": "application/json", "User-Agent": "public-history-research/1.0",
        })
        try:
            with urlopen(req, timeout=35) as response:
                raw = response.read(2_000_001)
                meta["http_status"] = response.status
                meta["server_date"] = response.headers.get("Date")
            if len(raw) > 2_000_000:
                raise ValueError("Bounded response size exceeded")
            body = json.loads(raw)
            if method != "GET" and ("error" in body or body.get("result") is None):
                raise ValueError("RPC returned no usable result: " + str(body))
            meta["response_sha256"] = hashlib.sha256(raw).hexdigest()
            meta["response_bytes"] = len(raw)
            (self.output / (name + ".json")).write_bytes(raw)
            meta["ok"] = True
            value = body if method == "GET" else body["result"]
        except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError) as exc:
            meta["ok"] = False
            meta["error"] = f"{type(exc).__name__}: {exc}"
            if isinstance(exc, HTTPError):
                meta["http_status"] = exc.code
                meta["error_body"] = exc.read(1200).decode(errors="replace")
            value = None
        with self.lock:
            self.manifest.append(meta)
        return value


def main(output_dir):
    probe = PublicProbe(output_dir)
    summary = {
        "actor_address": ACTOR, "chain_id": 10, "spoke_pool": POOL,
        "scope": "one_chain_availability_and_partial_cashflow_not_full_actor_ledger",
        "source_urls": SOURCE_URLS,
        "qualifies_t1": False, "realized_pnl_usd": None, "capital_deployed_usd": None,
        "opening_receivables_raw": None, "closing_receivables_raw": None,
        "all_costs_reconciled": False, "source_coverage_complete": False,
        "open_block_excluded": OPEN_BLOCK, "close_block_included": CLOSE_BLOCK,
    }
    states = {}
    for label, block in [("opening", OPEN_BLOCK), ("closing", CLOSE_BLOCK)]:
        tag = hex(block)
        b = probe.request(label + "-block", "eth_getBlockByNumber", [tag, False])
        states[label] = {
            "block_number": block, "block_hash": b.get("hash") if b else None,
            "timestamp_unix": int(b["timestamp"], 16) if b else None,
        }
        if b:
            states[label]["timestamp_utc"] = datetime.fromtimestamp(
                int(b["timestamp"], 16), timezone.utc
            ).isoformat()
        for suffix, method in [("native_wei", "eth_getBalance"),
                               ("account_nonce", "eth_getTransactionCount")]:
            value = probe.request(label + "-" + suffix, method, [ACTOR, tag])
            states[label][suffix] = str(int(value, 16)) if value is not None else None
        for symbol, token in TOKENS.items():
            call = {"to": token, "data": "0x70a08231" + address_word(ACTOR)[2:]}
            value = probe.request(label + "-" + symbol, "eth_call", [call, tag])
            states[label][symbol + "_raw"] = str(int(value, 16)) if value else None
    summary["selected_inventory_not_total_capital"] = states
    if all(states[x]["timestamp_unix"] is not None for x in states):
        summary["elapsed_window_seconds"] = (
            states["closing"]["timestamp_unix"] - states["opening"]["timestamp_unix"]
        )
    summary["token_decimals"] = {}
    for symbol, token in TOKENS.items():
        value = probe.request(
            "decimals-" + symbol, "eth_call",
            [{"to": token, "data": "0x313ce567"}, hex(CLOSE_BLOCK)],
        )
        summary["token_decimals"][symbol] = int(value, 16) if value else None
    summary["closing_code"] = probe.request(
        "closing-code", "eth_getCode", [ACTOR, hex(CLOSE_BLOCK)]
    )
    full_filter = {
        "address": POOL, "fromBlock": hex(OPEN_BLOCK + 1),
        "toBlock": hex(CLOSE_BLOCK), "topics": [FILL, None, None, address_word(ACTOR)],
    }
    # Preserve the documented range-limit failure before the bounded page fallback.
    probe.request("full-window-fill-probe", "eth_getLogs", [full_filter])
    jobs = [
        (kind, lo, hi) for lo, hi in ranges(OPEN_BLOCK + 1, CLOSE_BLOCK)
        for kind in ("fills", "refunds")
    ]

    def page(job):
        kind, lo, hi = job
        topics = [FILL, None, None, address_word(ACTOR)] if kind == "fills" else [REFUND]
        logs = probe.request(
            f"{kind}-{lo}-{hi}", "eth_getLogs", [{
                "address": POOL, "fromBlock": hex(lo), "toBlock": hex(hi),
                "topics": topics,
            }],
        )
        return kind, lo, hi, logs

    fills, refunds, page_counts, failed, errors = [], [], Counter(), [], []
    seen = set()
    with ThreadPoolExecutor(max_workers=3) as pool:
        for kind, lo, hi, logs in pool.map(page, jobs):
            if logs is None:
                failed.append({"kind": kind, "from_block": lo, "to_block": hi})
                continue
            page_counts[kind] += 1
            for log in logs:
                key = (kind, log["transactionHash"], log["logIndex"])
                if key in seen:
                    errors.append({"kind": kind, "error": "Duplicate event key"})
                    continue
                seen.add(key)
                try:
                    if log.get("removed") or not lo <= int(log["blockNumber"], 16) <= hi:
                        raise ValueError("Removed/out-of-range log")
                    value = decode_fill(log) if kind == "fills" else decode_refund(log)
                    if value is not None:
                        (fills if kind == "fills" else refunds).append(value)
                except (ValueError, KeyError, TypeError, IndexError) as exc:
                    errors.append({"kind": kind, "transaction_hash": log["transactionHash"],
                                   "error": str(exc)})
    summary["pagination"] = {
        "page_size_blocks": PAGE_SIZE, "expected_pages_per_kind": len(jobs) // 2,
        "successful_pages": dict(page_counts), "failed_pages": failed,
        "decode_errors": errors,
    }
    summary["observed_fill_event_count"] = len(fills)
    summary["observed_unique_fill_transactions"] = len({r["transaction_hash"] for r in fills})
    summary["fill_repayment_chain_counts"] = dict(Counter(r["repayment_chain_id"] for r in fills))
    summary["fill_type_counts"] = dict(Counter(r["fill_type"] for r in fills))
    totals = defaultdict(int)
    for row in fills:
        totals[row["output_token"]] += int(row["actual_output_amount_raw"])
    summary["fill_output_totals_by_token_raw_not_profit"] = {
        k: str(v) for k, v in totals.items()
    }
    totals = defaultdict(int)
    for row in refunds:
        totals[row["token"]] += int(row["allocated_amount_raw"])
    summary["refund_event_count_with_actor_allocation"] = len(refunds)
    summary["refund_allocations_by_token_raw_not_cash_or_profit"] = {
        k: str(v) for k, v in totals.items()
    }
    summary["refund_batches_with_any_deferred_payment"] = sum(
        r["any_batch_refunds_deferred"] for r in refunds
    )
    receipt = probe.request(
        "refund-receipt-example", "eth_getTransactionReceipt", [REFUND_EXAMPLE]
    )
    summary["one_receipt_confirmed_refund_transfers_not_profit"] = (
        confirmed_transfers(receipt) if receipt else None
    )
    # Small API checks test documented pagination and reject unsupported actor filters.
    checks = []
    for skip in (0, 1000, 5000, 10000, 100000):
        url = f"https://app.across.to/api/deposits?limit=2&skip={skip}"
        rows = probe.request("deposits-skip-" + str(skip), "GET", url=url)
        checks.append({
            "source_url": url, "skip": skip, "returned_count": len(rows) if isinstance(rows, list) else None,
            "timestamps": [r.get("depositBlockTimestamp") for r in rows] if isinstance(rows, list) else None,
        })
    url = "https://app.across.to/api/deposits?limit=2&relayer=" + ACTOR
    probe.request("unsupported-relayer-filter", "GET", url=url)
    summary["deposit_api_pagination_probes"] = checks
    summary["missing_for_actor_pnl"] = [
        "All other chains, all other token inventories and related entity addresses",
        "Opening/closing unexecuted refund entitlements and disputed/deferred receivables",
        "Fill-to-refund-root/bundle allocations and exact repayment latency",
        "All nonfill/reverted transactions, gas and explicit payments",
        "Funding/withdrawals, liabilities and bridge/rebalance transfers",
        "Token marks, protocol fees, infrastructure costs and operator capital denominator",
        "Other event versions, proxy implementation history, claims and legacy SpokePools",
    ]
    summary["request_count"] = probe.calls
    summary["request_manifest"] = sorted(probe.manifest, key=lambda r: r["name"])
    path = Path(output_dir)
    (path / "selected-fills.json").write_text(json.dumps(fills, indent=2) + "\n")
    (path / "selected-refund-allocations.json").write_text(json.dumps(refunds, indent=2) + "\n")
    (path / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({
        k: summary[k] for k in (
            "elapsed_window_seconds", "observed_fill_event_count",
            "refund_event_count_with_actor_allocation", "pagination", "request_count",
            "qualifies_t1", "realized_pnl_usd",
        ) if k in summary
    }))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="data/raw/across-actor-history")
    args = parser.parse_args()
    main(args.output_dir)
