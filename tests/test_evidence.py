"""Synthetic fixture tests only. No market observations or return evidence."""

from datetime import datetime, timezone
import hashlib
from pathlib import Path
import tempfile
import unittest

from research_tools.evidence import (
    EvidenceError, Manifest, REQUIRED_CHECKS, Tier, file_digest, load_json, validate,
)


NOW = datetime(2026, 10, 29, tzinfo=timezone.utc)


def fixture() -> dict:
    return {
        "schema_version": 1, "paper_only": True, "id": "SYNTHETIC-fixture",
        "strategy_id": "SYNTHETIC-no-strategy", "tier": "T4", "data_kind": "synthetic",
        "start": "2026-09-01T00:00:00Z", "end": "2026-10-02T00:00:00Z",
        "created_at": "2026-10-28T00:00:00Z",
        "sources": [{"id": "synthetic", "url": "https://example.com/SYNTHETIC",
                     "retrieved_at": "2026-10-03T00:00:00Z",
                     "artifact_path": "SYNTHETIC.txt",
                     "sha256": hashlib.sha256(b"SYNTHETIC NOT MARKET DATA\n").hexdigest()}],
        "claims": [{"id": "synthetic-number", "metric": "fixture_only", "value": "1",
                    "unit": "test-unit-not-usd-return", "source_ids": ["synthetic"]}],
        "checks": {}, "actors": [], "volatile_windows": [],
    }


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "SYNTHETIC.txt").write_bytes(b"SYNTHETIC NOT MARKET DATA\n")

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, row):
        return validate(Manifest.parse(row), self.root, now=NOW)

    def test_synthetic_can_be_valid_t4_but_never_recommended(self):
        result = self.check(fixture())
        self.assertTrue(result["structural_and_integrity_checks_passed"])
        self.assertFalse(result["ready_for_independent_content_review"])
        self.assertFalse(result["recommendation_eligible"])

    def test_synthetic_cannot_claim_higher_tier(self):
        for tier in ("T1", "T2", "T3"):
            row = fixture()
            row["tier"] = tier
            self.assertFalse(self.check(row)["structural_and_integrity_checks_passed"])

    def test_hash_mismatch(self):
        (self.root / "SYNTHETIC.txt").write_text("changed")
        self.assertIn("source artifact hash mismatch", self.check(fixture())["errors"])

    def test_missing_artifact(self):
        (self.root / "SYNTHETIC.txt").unlink()
        self.assertFalse(self.check(fixture())["structural_and_integrity_checks_passed"])

    def test_path_traversal_absolute_and_symlink(self):
        for name in ("../escape", "/etc/passwd"):
            with self.assertRaises(EvidenceError):
                file_digest(self.root, name)
        (self.root / "escape").symlink_to("/etc/passwd")
        with self.assertRaises(EvidenceError):
            file_digest(self.root, "escape")

    def test_unknown_claim_reference(self):
        row = fixture()
        row["claims"][0]["source_ids"] = ["missing"]
        self.assertIn("claim/check/window references an unknown source", self.check(row)["errors"])

    def test_duplicate_source_and_claim(self):
        row = fixture()
        row["sources"] *= 2
        row["claims"] *= 2
        result = self.check(row)
        self.assertIn("duplicate source identifiers", result["errors"])
        self.assertIn("duplicate claim identifiers", result["errors"])

    def test_amount_rejects_float_bool_nan_infinity(self):
        for value in (1.1, True, "NaN", "Infinity", "-Infinity"):
            row = fixture()
            row["claims"][0]["value"] = value
            with self.assertRaises(EvidenceError):
                Manifest.parse(row)

    def test_credential_urls_rejected_without_echoing_value(self):
        for url in ("http://example.com", "https://user:password@example.com",
                    "https://example.com?api_key=SHOULD_NOT_PRINT", "https://127.0.0.1",
                    "https://localhost", "https://service.internal"):
            row = fixture()
            row["sources"][0]["url"] = url
            with self.assertRaises(EvidenceError) as error:
                Manifest.parse(row)
            self.assertNotIn("SHOULD_NOT_PRINT", str(error.exception))

    def test_timestamps_need_explicit_utc(self):
        for value in ("2026-10-01", "2026-10-01T00:00:00", "2026-10-01T00:00:00+01:00"):
            row = fixture()
            row["start"] = value
            with self.assertRaises(EvidenceError):
                Manifest.parse(row)

    def test_future_observations_rejected(self):
        row = fixture()
        row["end"] = "2027-01-01T00:00:00Z"
        self.assertFalse(self.check(row)["structural_and_integrity_checks_passed"])

    def test_t2_duration_volatile_window_and_check_references(self):
        row = fixture()
        row["tier"], row["data_kind"] = "T2", "historical_fork"
        row["checks"] = {key: ["synthetic"] for key in REQUIRED_CHECKS[Tier.T2]}
        row["volatile_windows"] = [
            {"start": "2026-09-10T00:00:00Z", "end": "2026-09-11T00:00:00Z",
             "source_ids": ["synthetic"]}]
        # Metadata alone is intentionally not verification, even if someone relabels
        # a fixture. Passing here means CONTENT REVIEW REQUIRED, not genuine T2.
        result = self.check(row)
        self.assertTrue(result["ready_for_independent_content_review"])
        self.assertFalse(result["recommendation_eligible"])
        row["end"] = "2026-09-20T00:00:00Z"
        self.assertIn("T2 requires at least 30 days", self.check(row)["errors"])
        row["volatile_windows"] = []
        self.assertIn("T2 requires a sourced volatile window", self.check(row)["errors"])

    def test_t1_and_t3_minimum_durations(self):
        for tier, kind, days in (("T1", "observed_onchain", 14), ("T3", "forward_paper", 7)):
            row = fixture()
            row["tier"], row["data_kind"] = tier, kind
            row["end"] = "2026-09-02T00:00:00Z"
            self.assertIn(f"{tier} requires at least {days} days", self.check(row)["errors"])

    def test_duplicate_json_keys_nonfinite_and_wrong_schema(self):
        path = self.root / "bad.json"
        for content in ('{"same":1,"same":2}', '{"value":NaN}'):
            path.write_text(content)
            with self.assertRaises(EvidenceError):
                load_json(path)
        row = fixture()
        row["schema_version"] = True
        with self.assertRaises(EvidenceError):
            Manifest.parse(row)

    def test_no_paper_only_acknowledgment(self):
        row = fixture()
        row["paper_only"] = False
        with self.assertRaises(EvidenceError):
            Manifest.parse(row)

    def test_malformed_collection_types_fail_closed(self):
        for field, value in (("checks", []), ("sources", {}), ("claims", "bad")):
            row = fixture()
            row[field] = value
            with self.assertRaises(EvidenceError):
                Manifest.parse(row)


if __name__ == "__main__":
    unittest.main()
