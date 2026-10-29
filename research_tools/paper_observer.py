"""One-shot, read-only public-market observation with fail-closed paper rules.

Run manually or via an approved external scheduler; this command never starts
an unattended loop. Zero inventory is the default and no trade is placed.
"""

import argparse
import hashlib
import json
from pathlib import Path
import time

from research_tools.yield_data import DataError, PublicData, finite, iso_now, timestamp


def normalize_hl_book(payload, expected_coin="BTC"):
    if payload.get("coin") != expected_coin:
        raise DataError("book asset mismatch")
    stamp = finite(payload.get("time"), "source time", minimum=1) / 1000
    sides = payload.get("levels")
    if not isinstance(sides, list) or len(sides) != 2:
        raise DataError("two book sides required")
    bids = [(finite(x.get("px"), "bid", minimum=0.00000001),
             finite(x.get("sz"), "bid size", minimum=0)) for x in sides[0]]
    asks = [(finite(x.get("px"), "ask", minimum=0.00000001),
             finite(x.get("sz"), "ask size", minimum=0)) for x in sides[1]]
    if not bids or not asks or bids[0][0] >= asks[0][0]:
        raise DataError("empty, locked or crossed book")
    if any(b[0] > a[0] for a, b in zip(bids, bids[1:])):
        raise DataError("bids not descending")
    if any(b[0] < a[0] for a, b in zip(asks, asks[1:])):
        raise DataError("asks not ascending")
    return {"source_time_s": stamp, "bids": bids, "asks": asks,
            "asset": expected_coin, "venue": "hyperliquid"}


def executable_quote(book, side, quantity, now_s, max_age_s, fee_bps,
                     adverse_bps, latency_ms):
    """Pessimistic depth estimate, not an actual fill or T2/T3 evidence.

    A future implementation must inspect a second book after latency elapses;
    this model only applies an explicit adverse-price assumption.
    """
    if side not in {"buy", "sell"}:
        raise DataError("invalid side")
    quantity = finite(quantity, "quantity", minimum=0.000000001)
    fee_bps = finite(fee_bps, "fee_bps", minimum=0)
    adverse_bps = finite(adverse_bps, "adverse_bps", minimum=0)
    finite(latency_ms, "latency_ms", minimum=0)
    finite(max_age_s, "max_age_s", minimum=0)
    source = finite(book.get("source_time_s"), "source timestamp", minimum=1)
    age = now_s - source
    if age < -1 or age > max_age_s:
        raise DataError("stale or future source timestamp")
    remaining, worst = quantity, None
    for px, size in book["asks" if side == "buy" else "bids"]:
        take = min(remaining, size)
        if take > 0:
            worst = px
            remaining -= take
        if remaining < 1e-12:
            break
    if remaining > 1e-12 or worst is None:
        raise DataError("insufficient visible depth")
    adjusted = worst * (1 + adverse_bps/10000 if side == "buy" else 1-adverse_bps/10000)
    if adjusted <= 0:
        raise DataError("invalid adverse price")
    gross = adjusted * quantity
    return {"evidence_tier": "T4", "kind": "pessimistic_depth_estimate_not_fill",
            "side": side, "quantity": quantity, "estimated_price": adjusted,
            "gross_usd": gross, "fee_usd": gross*fee_bps/10000,
            "latency_ms_assumption": latency_ms, "source_age_s": age,
            "adverse_bps_assumption": adverse_bps}


def mark_to_market(spot_qty, short_qty, spot_bid, perp_ask, entry_cash_usd,
                   funding_usd, costs_usd):
    """Liquidation-side MTM; excludes liquidation/default and unquoted fees."""
    values = [finite(v, name, minimum=0) for name, v in (
        ("spot_qty", spot_qty), ("short_qty", short_qty),
        ("spot_bid", spot_bid), ("perp_ask", perp_ask), ("costs", costs_usd))]
    spot_qty, short_qty, spot_bid, perp_ask, costs_usd = values
    return (finite(entry_cash_usd, "entry_cash") + spot_qty*spot_bid
            - short_qty*perp_ask + finite(funding_usd, "funding") - costs_usd)


def collect_once(client, coin="BTC"):
    """Persist success AND failures; an unavailable source never implies a fill."""
    started = iso_now()
    sources, failures = {}, []
    for name, call in (("perp_book", lambda: client.book(coin)),
                       ("spot_book", client.coinbase_btc_book)):
        try:
            sources[name] = call()
        except Exception as exc:
            # Do not emit upstream response bodies, configuration or secrets.
            failures.append({"source": name, "error_type": type(exc).__name__,
                             "observed_at": iso_now()})
    rejection = ["observation_only_no_strategy_or_cost_model_configured"]
    if coin != "BTC":
        rejection.append("spot_perp_asset_mismatch")
    book_summary = None
    if "perp_book" in sources:
        try:
            book = normalize_hl_book(sources["perp_book"]["payload"], coin)
            age = time.time()-book["source_time_s"]
            if not -1 <= age <= 5:
                raise DataError("stale perp book")
            book_summary = {"best_bid": book["bids"][0][0],
                            "best_ask": book["asks"][0][0], "source_age_s": age}
        except (DataError, KeyError, TypeError, IndexError) as exc:
            failures.append({"source": "perp_book", "error_type": type(exc).__name__,
                             "observed_at": iso_now()})
            rejection.append("invalid_or_stale_perp_book")
    if "spot_book" in sources:
        # Coinbase REST L2 response has sequence, but no exchange event time.
        # HTTP Date/receipt time cannot certify source-book freshness.
        rejection.append("spot_book_missing_source_timestamp")
    if failures:
        rejection.append("source_failure")
    return {
        "schema_version": 1, "mode": "read_only_observation",
        "strategy_version": None, "started_at": started, "finished_at": iso_now(),
        "sources": sources, "failures": failures, "book_summary": book_summary,
        "decision": "REJECT_NO_PAPER_FILL", "rejection_reasons": rejection,
        "simulated_fills": [], "positions": [], "mark_to_market_usd": 0.0,
        "costs_usd": {"incurred_trading": 0.0, "infrastructure": None},
        "evidence_tier": "input_only_not_T3",
        "notes": ["zero-inventory observer; no return is computed",
                  "infrastructure cost unknown, not assumed free"],
    }


def append_record(path, record):
    """Append-only JSONL with a previous-record hash for corruption detection.

    Single-writer contract. Hash chaining is not independent timestamp proof.
    """
    path = Path(path)
    previous_hash = None
    if path.exists():
        lines = path.read_text().splitlines()
        if lines:
            previous = json.loads(lines[-1])
            previous_hash = previous["record_sha256"]
    row = dict(record, previous_record_sha256=previous_hash)
    if "record_sha256" in row:
        raise DataError("new record must not contain a stored hash")
    canonical = json.dumps(row, sort_keys=True, separators=(",", ":"), allow_nan=False)
    row["record_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    with path.open("a") as file:
        file.write(json.dumps(row, sort_keys=True, allow_nan=False) + "\n")
    return row


def load_records(path):
    """Verify hash chain before reporting coverage; no independent time proof."""
    records, previous_hash = [], None
    for line in Path(path).read_text().splitlines():
        record = json.loads(line)
        stored = record.pop("record_sha256", None)
        canonical = json.dumps(record, sort_keys=True, separators=(",", ":"), allow_nan=False)
        expected = hashlib.sha256(canonical.encode()).hexdigest()
        if stored != expected or record.get("previous_record_sha256") != previous_hash:
            raise DataError("observation log hash/chain mismatch")
        record["record_sha256"] = stored
        records.append(record)
        previous_hash = stored
    return records


def observation_gate(records, max_gap_s=300):
    """Minimum wall-time/coverage checks only: passing is NOT a T3 award."""
    if not records:
        return {"eligible_for_T3_review": False, "reasons": ["no_records"]}
    now = time.time()
    stamps = [timestamp(row["finished_at"]) for row in records]
    reasons = []
    if any(stamp > now+1 for stamp in stamps):
        reasons.append("future_observation_time")
    if any(b <= a or b-a > max_gap_s for a, b in zip(stamps, stamps[1:])):
        reasons.append("nonmonotonic_or_gap")
    span = stamps[-1]-stamps[0]
    if span < 7*86400:
        reasons.append("less_than_seven_elapsed_days")
    versions = {row.get("strategy_version") for row in records}
    if None in versions or len(versions) != 1:
        reasons.append("missing_or_changed_decision_logic")
    if any(row.get("failures") for row in records):
        reasons.append("source_failures_require_review")
    if not any(row.get("simulated_fills") for row in records):
        reasons.append("no_simulated_fills")
    return {"elapsed_days": span/86400, "records": len(records),
            "eligible_for_T3_review": not reasons, "reasons": reasons,
            "independent_evidence_review_required": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--out", help="append-only single-writer JSONL")
    group.add_argument("--audit", help="verify log and report minimum coverage checks")
    args = parser.parse_args()
    if args.audit:
        print(json.dumps(observation_gate(load_records(args.audit)), indent=2))
        return
    row = append_record(args.out, collect_once(PublicData()))
    print(json.dumps({key: row[key] for key in
                      ("finished_at", "decision", "rejection_reasons", "record_sha256")}))


if __name__ == "__main__":
    main()
