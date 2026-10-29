"""Recompute committed PUBLIC historical-input arithmetic, not source authenticity."""
import hashlib
import json
from pathlib import Path
import unittest
from research_tools.yield_data import funding_carry, lending_carry, lending_points

ROOT = Path(__file__).resolve().parents[1] / "research_tools"


class PublicSnapshotArithmetic(unittest.TestCase):
    def test_delivered_manifest_integrity(self):
        manifest = json.loads((ROOT/"paper_yield_manifest.json").read_text())
        for filename, digest in manifest["file_sha256"].items():
            content = (ROOT.parent/filename).read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), digest, filename)

    def test_lending_gross_reproduces_without_network(self):
        sample = json.loads((ROOT/"yield_sample_20261029.json").read_text())
        for result in sample["results"].values():
            points = lending_points({"status": "success", "data": result["data_excerpt"]})
            for expected in result["comparators"].values():
                actual = lending_carry(points, expected["start_s"], expected["end_s"],
                                       expected["capital_usd"], None)
                self.assertAlmostEqual(actual["gross_carry_usd"],
                                       expected["gross_carry_usd"], places=8)
                self.assertIsNone(actual["net_after_explicit_costs_only_usd"])

    def test_funding_gross_reproduces_without_network(self):
        sample = json.loads((ROOT/"yield_funding_sample_20261029.json").read_text())
        all_rows = [{"time": t, "fundingRate": r} for t, r in sample["compact_input_rows"]]
        self.assertEqual(len(all_rows), 2160)
        for expected in sample["comparators"].values():
            rows = [r for r in all_rows if expected["start_ms"] <= r["time"] <= expected["end_ms"]]
            actual = funding_carry(rows, expected["start_ms"], expected["end_ms"],
                                   expected["constant_short_notional_usd"], None)
            self.assertAlmostEqual(actual["gross_short_funding_usd"],
                                   expected["gross_short_funding_usd"], places=8)
            self.assertIsNone(actual["net_component_after_explicit_costs_only_usd"])


if __name__ == "__main__":
    unittest.main()
