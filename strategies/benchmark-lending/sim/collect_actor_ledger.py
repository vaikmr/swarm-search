#!/usr/bin/env python3
"""Bounded public-only actor observations. Never signs or submits transactions.

Python standard library plus curl. Cache is optional public response data, not
credentials. State/receipt observations are not a fork replay or T1 certificate.
"""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import time
from urllib.parse import urlencode
from snapshot_market_identity import validate_header

ACTOR = "0x56957e411ea83a0b4a0689c1fb0d1e5ea0d20149"
USDC = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
ATOKEN = "0x98c23e9d8f34fefb1b7bd6a91b7ff122f4e16f5c"
POOL = "0x87870bca3f3fd6335c3f4ce8392d69350b4fa4e2"
ORACLE = "0x54586be62e3c3580375ae3723c145253060ca0c2"
WETH = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
PROVIDER = "0x2f39d218133afab8f2b819b1066c7e434ad94e9e"
START, END = 26196084, 26296884
RPC = "https://eth.drpc.org"
EXPLORER = "https://eth.blockscout.com/api/v2/addresses/" + ACTOR
TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
ALLOWED = {"eth_call", "eth_getBalance", "eth_getBlockByNumber", "eth_getTransactionReceipt", "eth_getStorageAt"}


def word(address):
    return address[2:].lower().rjust(64, "0")


def call(to, data, block):
    return "eth_call", [{"to": to, "data": data}, hex(block)]


class PublicReader:
    def __init__(self, cache):
        self.cache = cache
        cache.mkdir(parents=True, exist_ok=True)
        self.rpc_count = 0
        self.provenance = []

    def get(self, url, name):
        path = self.cache / name
        if not path.exists():
            raw = subprocess.check_output(["curl", "--fail", "-sS", "--max-time", "60", url])
            path.write_bytes(raw)
        raw = path.read_bytes()
        self.provenance.append({"source": url, "response_sha256": hashlib.sha256(raw).hexdigest(),
                                "observed_at": dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).isoformat(),
                                "observed_at_basis": "public response cache filesystem mtime"})
        return json.loads(raw)

    def rpc(self, jobs):
        values = {}
        for offset in range(0, len(jobs), 3):
            chunk = jobs[offset:offset + 3]
            requests = [{"jsonrpc": "2.0", "id": i + 1, "method": method, "params": params}
                        for i, (_, method, params) in enumerate(chunk)]
            if any(r["method"] not in ALLOWED for r in requests):
                raise ValueError("Non-allowlisted RPC method")
            key = hashlib.sha256(json.dumps(requests, sort_keys=True).encode()).hexdigest()
            path = self.cache / ("rpc-" + key + ".json")
            if not path.exists():
                self.rpc_count += len(requests)
                if self.rpc_count > 350:
                    raise ValueError("Bounded live RPC budget exceeded")
                raw = subprocess.check_output(["curl", "--fail", "-sS", "--max-time", "60", RPC,
                                               "-H", "Content-Type: application/json",
                                               "--data", json.dumps(requests)])
                path.write_bytes(raw)
                time.sleep(0.3)
            raw = path.read_bytes()
            response = json.loads(raw)
            by_id = {r["id"]: r for r in response}
            if len(by_id) != len(requests):
                raise ValueError("Missing or duplicate RPC result")
            for i, (label, _, _) in enumerate(chunk):
                r = by_id[i + 1]
                if "result" not in r or r["result"] is None:
                    raise ValueError("Missing RPC observation: " + label + " " + str(r.get("error")))
                values[label] = r["result"]
            self.provenance.append({"source": RPC, "request": requests,
                                    "response_sha256": hashlib.sha256(raw).hexdigest(),
                                    "observed_at": dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).isoformat(),
                                    "observed_at_basis": "public response cache filesystem mtime"})
        return values


def pages(reader, kind, token=None):
    query = {"type": "ERC-20", "token": token} if token else {}
    prefix = "aUSDC-transfers" if token == ATOKEN else "USDC-transfers" if token else kind
    rows, metadata, complete = {}, [], False
    for page in range(1, 6):
        url = EXPLORER + "/" + kind + ("?" + urlencode(query) if query else "")
        data = reader.get(url, prefix + f"-page{page}.json")
        items = data.get("items")
        if not isinstance(items, list):
            raise ValueError("Unexpected explorer page")
        blocks = [r["block_number"] for r in items]
        if blocks != sorted(blocks, reverse=True):
            raise ValueError("Unexpected explorer ordering; cannot infer boundary coverage")
        metadata.append({"source": url, "rows": len(items), "oldest_block": min(blocks) if blocks else None,
                         "next_page_params": data.get("next_page_params")})
        for row in items:
            if not START < row["block_number"] <= END:
                continue
            if token:
                if row["token"]["address_hash"].lower() != token:
                    raise ValueError("Provider ignored exact-contract filter")
                key = (row["transaction_hash"], row["log_index"])
            elif kind == "transactions":
                key = row["hash"]
            else:
                key = (row["transaction_hash"], row.get("index"))
            if key in rows and rows[key] != row:
                raise ValueError("Conflicting duplicate explorer observation")
            rows[key] = row
        if not items or any(b <= START for b in blocks) or not data.get("next_page_params"):
            complete = True
            break
        query = data["next_page_params"]
        if token:
            query = {"type": "ERC-20", **query}
    if not complete:
        raise ValueError("Bounded pagination did not cover requested start")
    return sorted(rows.values(), key=lambda r: (r["block_number"], r.get("log_index", 0))), metadata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path, default=Path("/tmp/public-aave-actor"))
    parser.add_argument("--out", type=Path, default=Path("strategies/benchmark-lending/evidence/actor-observations.json"))
    args = parser.parse_args()
    reader = PublicReader(args.cache)
    transfers, page_meta = [], {}
    for token in (USDC, ATOKEN):
        rows, meta = pages(reader, "token-transfers", token)
        transfers += rows
        page_meta[token] = meta
    normal, page_meta["normal"] = pages(reader, "transactions")
    internal, page_meta["internal"] = pages(reader, "internal-transactions")
    state_jobs = []
    for block in (START, END):
        prefix = str(block) + ":"
        state_jobs += [(prefix + "block", "eth_getBlockByNumber", [hex(block), False]),
                       (prefix + "USDC", *call(USDC, "0x70a08231" + word(ACTOR), block)),
                       (prefix + "aUSDC", *call(ATOKEN, "0x70a08231" + word(ACTOR), block)),
                       (prefix + "scaled", *call(ATOKEN, "0x1da24f3e" + word(ACTOR), block)),
                       (prefix + "index", *call(POOL, "0xd15e0053" + word(USDC), block)),
                       (prefix + "account", *call(POOL, "0xbf92857c" + word(ACTOR), block)),
                       (prefix + "ETH", "eth_getBalance", [ACTOR, hex(block)]),
                       (prefix + "USDC_price", *call(ORACLE, "0xb3596f07" + word(USDC), block)),
                       (prefix + "ETH_price", *call(ORACLE, "0xb3596f07" + word(WETH), block)),
                       (prefix + "oracle", *call(PROVIDER, "0xfca513a8", block)),
                       (prefix + "price_unit", *call(ORACLE, "0x8c89b64f", block))]
    values = reader.rpc(state_jobs)
    endpoints = {}
    for block in (START, END):
        prefix = str(block) + ":"
        header = validate_header(values[prefix + "block"], hex(block))
        endpoints[str(block)] = {"header": header}
        for field in ("USDC", "aUSDC", "scaled", "index", "ETH", "USDC_price", "ETH_price", "price_unit"):
            endpoints[str(block)][field] = str(int(values[prefix + field], 16))
        account = values[prefix + "account"][2:]
        endpoints[str(block)]["aave_account_base_8_decimals"] = [str(int(account[i:i + 64], 16)) for i in range(0, len(account), 64)]
        endpoints[str(block)]["oracle"] = "0x" + values[prefix + "oracle"][-40:]
        if endpoints[str(block)]["oracle"].lower() != ORACLE or endpoints[str(block)]["price_unit"] != "100000000":
            raise ValueError("Unexpected oracle identity or price unit")
    elapsed = (dt.datetime.fromisoformat(endpoints[str(END)]["header"]["block_time"]) -
               dt.datetime.fromisoformat(endpoints[str(START)]["header"]["block_time"])).total_seconds()
    if elapsed < 14 * 86400:
        raise ValueError("Window shorter than fourteen days")
    hashes = sorted({r["transaction_hash"] for r in transfers} | {r["hash"] for r in normal})
    if len(hashes) > 180:
        raise ValueError("Receipt scope exceeds bounded actor probe")
    receipts_raw = reader.rpc([(h, "eth_getTransactionReceipt", [h]) for h in hashes])
    receipts = {}
    for h, receipt in receipts_raw.items():
        if receipt["transactionHash"].lower() != h.lower() or not START < int(receipt["blockNumber"], 16) <= END:
            raise ValueError("Receipt identity/window mismatch")
        receipts[h] = {k: receipt.get(k) for k in ("transactionHash", "blockNumber", "blockHash", "from", "to",
                                                  "gasUsed", "effectiveGasPrice", "blobGasUsed", "blobGasPrice", "type", "status")}
        receipts[h]["logs"] = [r for r in receipt["logs"]
                               if r["address"].lower() in (USDC, ATOKEN)
                               and len(r["topics"]) == 3 and r["topics"][0].lower() == TRANSFER
                               and ACTOR[2:] in (r["topics"][1][-40:].lower(), r["topics"][2][-40:].lower())]
    price_keys = set()
    for r in transfers:
        f, t, value = r["from"]["hash"].lower(), r["to"]["hash"].lower(), int(r["total"]["value"])
        if value and "0x" + "0" * 40 not in (f, t) and ATOKEN not in (f, t):
            price_keys.add((r["block_number"], "USDC"))
    for r in normal:
        if r["from"]["hash"].lower() == ACTOR or int(r["value"]):
            price_keys.add((r["block_number"], "ETH"))
    for r in internal:
        if int(r["value"]):
            price_keys.add((r["block_number"], "ETH"))
    prices_raw = reader.rpc([(str(b) + ":" + asset, *call(ORACLE, "0xb3596f07" + word(USDC if asset == "USDC" else WETH), b))
                             for b, asset in sorted(price_keys)])
    prices = {k: str(int(v, 16)) for k, v in prices_raw.items()}
    for k, price in prices.items():
        if int(price) <= 0:
            raise ValueError("Invalid reference USD mark")
    withdraw_blocks = sorted({r["block_number"] for r in normal
                              if r["from"]["hash"].lower() == ACTOR and r.get("method") == "withdraw"})
    after_withdraw = reader.rpc([(str(b), *call(ATOKEN, "0x70a08231" + word(ACTOR), b))
                                for b in withdraw_blocks])
    base_currency = reader.rpc([(str(b), *call(ORACLE, "0xe19f4700", b)) for b in (START, END)])
    if any(int(v, 16) != 0 for v in base_currency.values()):
        raise ValueError("Oracle base currency is not the documented USD zero-address convention")
    implementation = reader.rpc([(str(b), "eth_getStorageAt", [
        ATOKEN, "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc", hex(b)])
        for b in (START, END)])
    impl = "0xadc45df3cf1584624c97338bef33363bf5b97ada"
    if any(("0x" + v[-40:]).lower() != impl for v in implementation.values()):
        raise ValueError("Different aToken implementation; rounding source must be rechecked")
    impl_url = "https://eth.blockscout.com/api/v2/smart-contracts/" + impl
    source = reader.get(impl_url, "atoken-implementation-source.json")
    snippets = []
    for f in source.get("additional_sources", []):
        lines = f.get("source_code", "").splitlines()
        for i, line in enumerate(lines):
            if "function getATokenBalance(" in line:
                snippets.append({"path": f["file_path"], "excerpt": "\n".join(lines[i:i + 6])})
    if not source.get("is_verified") or not any("rayMulFloor" in s["excerpt"] for s in snippets):
        raise ValueError("Missing verified rounding-function source")
    slim_transfers = [{"block": r["block_number"], "timestamp": r["timestamp"], "tx": r["transaction_hash"],
                       "log_index": r["log_index"], "token": r["token"]["address_hash"].lower(),
                       "from": r["from"]["hash"].lower(), "to": r["to"]["hash"].lower(),
                       "raw_value": r["total"]["value"]} for r in transfers]
    slim_normal = [{"block": r["block_number"], "timestamp": r["timestamp"], "tx": r["hash"],
                    "from": r["from"]["hash"].lower(), "to": r["to"]["hash"].lower() if r.get("to") else None,
                    "wei_value": r["value"], "explorer_fee_wei": r["fee"]["value"],
                    "method": r.get("method"), "status": r.get("status")} for r in normal]
    slim_internal = [{"block": r["block_number"], "tx": r["transaction_hash"],
                      "wei_value": r["value"], "from": r["from"]["hash"].lower(),
                      "to": r["to"]["hash"].lower(), "success": r.get("success")} for r in internal]
    output = {"built_at": dt.datetime.now(dt.timezone.utc).isoformat(),
              "scope": "one public address, only verified USDC/aUSDC/native ETH and Aave V3 debt endpoints",
              "actor": ACTOR, "selection": "First non-contract holder of archived first-ten holder sample; chosen before return calculation",
              "start": START, "end": END, "elapsed_seconds": elapsed,
              "endpoints": endpoints, "transfers": slim_transfers, "normal_transactions": slim_normal,
              "internal_transactions": slim_internal, "receipts": receipts, "reference_prices_8_decimals": prices,
              "a_token_balance_after_withdraw_block": {k: str(int(v, 16)) for k, v in after_withdraw.items()},
              "oracle_base_currency_at_endpoints": base_currency,
              "oracle_usd_convention_source": "https://github.com/aave/aave-v3-core/blob/master/contracts/misc/AaveOracle.sol",
              "a_token_rounding_source": {"source": impl_url, "is_verified": True,
                                          "implementations_at_endpoints": {k: "0x" + v[-40:] for k, v in implementation.items()},
                                          "function_excerpts": snippets,
                                          "source_response_sha256": hashlib.sha256((args.cache / "atoken-implementation-source.json").read_bytes()).hexdigest()},
              "page_coverage": page_meta, "provenance": reader.provenance,
              "rpc_reads_executed_this_invocation": reader.rpc_count,
              "price_basis": "Aave oracle getAssetPrice: reference USD accounting marks at each flow/expense block; not executable spot or realized USD",
              "limits": ["Other tokens, NFTs, protocols, chains, custody and off-address assets/liabilities not reconciled",
                         "Current holder does not identify beneficial owner or prove strategy/firm equity",
                         "No paid endpoint, private credential, signer, transaction broadcast or fork replay",
                         "Indexer pagination plus receipt checks is not an independent all-chain getLogs completeness proof",
                         "Token-index accrual includes unrealized closing value; not all income is realized",
                         "Only network fees borne by this address observed; infrastructure/overhead/tax/custody costs unknown"]}
    # Preserve actual failed/successful prerequisite observations from this
    # collection session when supplied. A fresh cache does not invent them.
    output["initial_access_probes"] = []
    for name, source in [
        ("state-probe.json", "https://ethereum-rpc.publicnode.com"),
        ("llama-archive-probe.json", "https://eth.llamarpc.com"),
        ("drpc-archive-probe.json", RPC),
        ("log-receipt-probe.json", RPC),
        ("short-logs-probe.json", RPC),
    ]:
        path = args.cache / name
        if path.exists():
            raw = path.read_bytes()
            output["initial_access_probes"].append({
                "source": source, "probe": name, "response_record_sha256": hashlib.sha256(raw).hexdigest(),
                "observed_at": dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).isoformat(),
                "observed_at_basis": "cache record filesystem mtime", "record": json.loads(raw)})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, separators=(",", ":")) + "\n")
    print("Observed", len(transfers), "verified-token transfers,", len(normal), "normal transactions,",
          len(internal), "internal transfers,", len(receipts), "receipts,", len(prices), "flow/expense prices;",
          reader.rpc_count, "new RPC reads")


if __name__ == "__main__":
    main()
