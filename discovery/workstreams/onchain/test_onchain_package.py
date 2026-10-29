"""Offline integrity checks only; no market collection or economic simulation."""

import hashlib
import json
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).parent


def load(name):
    return json.loads((ROOT / name).read_text())


class OnchainPackageIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = load("sources.json")
        cls.gate = load("counterfactual_input_gate.json")
        cls.mechanisms = load("mechanisms.json")["mechanisms"]
        cls.spots = load("public_spot_checks.json")
        cls.wire = [
            r for r in cls.spots["results"]
            if r.get("network_request_sent") is not False
        ]

    def test_reference_coverage_is_scoped(self):
        summary = self.sources["reading_summary"]
        records = {r["id"]: r for r in self.sources["sources"]}
        self.assertEqual(len(summary["assigned_ids"]), 9)
        self.assertEqual(len(set(summary["priority_ids"])), 4)
        for ref in summary["priority_ids"]:
            self.assertIn(
                records[ref]["reading_status"],
                {"full_current_page", "full_current_readme"},
            )
        self.assertEqual(records["R054"]["reading_status"], "abstract_only_context")
        self.assertEqual(records["R012"]["reading_status"], "triage_access_gap")

    def test_fetch_and_search_budgets(self):
        summary = self.sources["reading_summary"]
        log = self.sources["retrieval_log"]
        self.assertEqual([r["n"] for r in log], list(range(1, 22)))
        self.assertEqual(len(log), summary["document_fetch_attempts"])
        self.assertEqual(len({r["source_id"] for r in log}), 20)
        self.assertEqual(len(self.sources["search_log"]), 8)
        budget = summary["budget_allocation"]
        self.assertEqual(budget["original_document_fetches"], 20)
        self.assertLessEqual(
            budget["candidate_only_additional_document_fetches"], 6
        )
        self.assertEqual(budget["candidate_only_additional_searches"], 2)
        self.assertEqual(
            [r["source_id"] for r in log if r.get("budget")],
            ["O-S11"],
        )

    def test_method_budget_includes_local_failures(self):
        spots = self.spots
        self.assertEqual(len(spots["results"]), spots["request_count"])
        self.assertEqual(spots["request_count"], 9)
        self.assertLessEqual(spots["request_count"], 12)
        self.assertEqual(len(self.wire), 5)
        self.assertEqual(spots["local_preparation_failures"], 4)
        self.assertEqual(spots["network_requests_attempted"], len(self.wire))
        self.assertEqual(
            self.sources["reading_summary"]["conservatively_charged_method_attempts"],
            spots["request_count"],
        )

    def test_requests_are_market_or_issuer_state_reads_only(self):
        for result in self.spots["results"]:
            request = result["request"]
            if result["endpoint"] == "https://api.hyperliquid.xyz/info":
                self.assertIn(request["type"], {"meta", "l2Book"})
                self.assertNotIn("user", request)
            else:
                self.assertEqual(
                    result["endpoint"], "https://api.mainnet-beta.solana.com"
                )
                self.assertIn(
                    request["method"],
                    {"getGenesisHash", "getAccountInfo", "getBlockTime"},
                )

    def test_retained_wire_response_hashes(self):
        for result in self.wire:
            self.assertEqual(result["http_status"], 200)
            raw = result["response_text"]
            self.assertEqual(
                hashlib.sha256(raw.encode()).hexdigest(),
                result["response_text_sha256"],
            )
            json.loads(raw)

    def test_solana_identity_units_and_clock(self):
        results = {r["label"]: json.loads(r["response_text"]) for r in self.wire}
        genesis = results["solana-genesis"]["result"]
        self.assertEqual(
            genesis, "5eykt4UsFv8P8NJdTREpY1vzqKqZKvdpKuc147dw2N9d"
        )
        account = results["eurc-premint-account"]["result"]
        self.assertEqual(account["context"]["slot"], 462822009)
        value = account["value"]
        self.assertEqual(value["owner"], "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
        info = value["data"]["parsed"]["info"]
        self.assertEqual(
            info["mint"], "HzwqbKZw8HxMN6bF2yFZNrht3c2iXXzpKcFu7uBEDKtr"
        )
        amount = info["tokenAmount"]
        units = Decimal(amount["amount"]) / (10 ** amount["decimals"])
        self.assertEqual(units, Decimal("20000009.79"))
        stamp = results["solana-observed-slot-time"]["result"]
        self.assertEqual(
            datetime.fromtimestamp(stamp, timezone.utc).isoformat(),
            "2026-10-29T08:58:01+00:00",
        )

    def test_current_book_and_meta_are_not_historical_fills(self):
        results = {r["label"]: r["response"] for r in self.wire}
        meta = results["hypercore-first-dex-meta"]
        self.assertEqual(len(meta["universe"]), 235)
        by_name = {r["name"]: r for r in meta["universe"]}
        self.assertEqual(by_name["BTC"]["maxLeverage"], 40)
        self.assertEqual(by_name["ETH"]["maxLeverage"], 25)
        book = results["btc-current-book-capability"]
        self.assertEqual(book["coin"], "BTC")
        self.assertEqual(book["time"], 1793264281601)
        self.assertTrue(book["levels"][0])
        self.assertTrue(book["levels"][1])
        self.assertEqual(self.gate["counterfactual_rows_run"], 0)

    def test_missing_economics_are_unknown_not_zero(self):
        gate = self.gate
        self.assertEqual(gate["reported_sample_size"], 21)
        self.assertEqual(gate["identified_trade_rows"], 0)
        for key in (
            "historically_unhedgeable_trade_count",
            "historically_supported_hedge_count",
            "unhedged_sample_pnl_usd",
            "hedged_sample_pnl_usd",
            "improvement_usd",
            "fits_total_capital_usd_50000",
            "risk_certificate",
        ):
            self.assertIsNone(gate[key], key)
        self.assertFalse(gate["evidence_upgrade"])

    def test_mechanism_and_source_links(self):
        sources = self.sources["sources"]
        source_ids = {s["id"] for s in sources}
        mechanism_ids = {m["id"] for m in self.mechanisms}
        self.assertEqual(len(source_ids), len(sources))
        self.assertEqual(len(mechanism_ids), 2)
        for source in sources:
            self.assertTrue(set(source["linked_mechanism_ids"]) <= mechanism_ids)
        for mechanism in self.mechanisms:
            self.assertTrue(set(mechanism["source_ids"]) <= source_ids)
            self.assertIsNone(mechanism["profitability_usd"])
            self.assertFalse(mechanism["riskless"])


if __name__ == "__main__":
    unittest.main()
