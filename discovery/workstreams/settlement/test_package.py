"""Validate discovery metadata, not strategy profitability."""
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).parent


class SettlementPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = json.loads((ROOT / "sources.json").read_text())
        cls.log = json.loads((ROOT / "retrieval-log.json").read_text())
        cls.mechanisms = json.loads((ROOT / "mechanisms.json").read_text())

    def test_all_nine_assignments_have_explicit_triage(self):
        rows = self.sources["assigned_references"]
        self.assertEqual({r["id"] for r in rows}, {
            "R008", "R010", "R021", "R040", "R049",
            "R052", "R058", "R059", "R066",
        })
        for row in rows:
            for key in ("title", "reading_status", "relevance",
                        "source_type", "retrieval_date", "data_window",
                        "publication_date", "mechanism_ids"):
                self.assertIn(key, row)
            self.assertNotEqual(row["reading_status"], "not_reviewed")

    def test_priority_originals_and_replacements_are_not_conflated(self):
        rows = {r["id"]: r for r in self.sources["assigned_references"]}
        self.assertTrue(rows["R008"]["exact_original_fully_read"])
        for key in ("R049", "R058", "R059"):
            self.assertFalse(rows[key]["exact_original_fully_read"])
            self.assertTrue(rows[key]["replacement_main_text_fully_read"])
            self.assertNotEqual(rows[key]["original_url"], rows[key]["read_url"])

    def test_budget_and_phase_counts(self):
        fetches, searches = self.log["document_fetches"], self.log["searches"]
        self.assertEqual(len(fetches), 26)
        self.assertEqual(len(searches), 8)
        self.assertEqual(sum(x["phase"] == "candidate6_extension"
                             for x in fetches), 6)
        self.assertEqual(sum(x["phase"] == "candidate6_extension"
                             for x in searches), 2)
        self.assertEqual(self.sources["coverage"]["new_rpc_calls"], 0)

    def test_redirected_relay_pages_are_one_substantive_source(self):
        rows = {r["id"]: r for r in self.log["document_fetches"]}
        self.assertEqual(rows["C6-RELAY-SOLVERS"]["main_body_sha256"],
                         rows["C6-RELAY-HOW"]["main_body_sha256"])
        self.assertEqual(self.sources["coverage"]["distinct_full_main_texts"], 16)

    def test_mechanism_source_links_resolve(self):
        valid = {x["id"] for x in self.sources["assigned_references"]}
        valid |= {x["id"] for x in self.sources["supplementary_sources"]}
        mechanisms = self.mechanisms["mechanisms"]
        self.assertEqual(len({x["id"] for x in mechanisms}), len(mechanisms))
        for mechanism in mechanisms:
            self.assertTrue(set(mechanism["source_ids"]) <= valid)
        ids = {x["id"] for x in mechanisms}
        for source in (self.sources["assigned_references"]
                       + self.sources["supplementary_sources"]):
            self.assertTrue(set(source["mechanism_ids"]) <= ids)

    def test_unknown_returns_are_not_fabricated(self):
        for mechanism in self.mechanisms["mechanisms"]:
            self.assertFalse(mechanism["recommended"])
            self.assertTrue(all(v is None
                                for v in mechanism["unknown_metrics"].values()))

    def test_candidate6_preserves_capital_and_access_limitations(self):
        c6 = next(x for x in self.mechanisms["mechanisms"]
                  if x["id"] == "SET-C6")
        self.assertFalse(c6["accounting"]["pending_claims_spendable"])
        self.assertFalse(c6["accounting"]["hub_credit_is_wallet_cash"])
        self.assertTrue(c6["accounting"]["same_fills_and_terminal_inventory"])
        self.assertFalse(c6["access"]["relay_vault_new_deposits_supported"])
        self.assertIsNone(c6["access"]["relay_solver_admission_verified"])


if __name__ == "__main__":
    unittest.main()
