"""Synthetic mutation tests of the offline evidence consistency checks."""

import copy
import json
import subprocess
import unittest

from verify_across_ledger import (
    ROOT, SOURCE_COMMIT, SOURCE_DIR, build_output, check_summary, check_witnesses, units,
)


def source(name):
    return json.loads(subprocess.check_output(
        ["git", "show", SOURCE_COMMIT + ":" + SOURCE_DIR + name], cwd=ROOT
    ))


class AcrossLedgerChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary = source("history-probe-summary.json")
        cls.witnesses = source("history-witnesses.json")

    def test_raw_units_are_not_usd(self):
        self.assertEqual(units("300000", 6), "0.300000")
        self.assertEqual(units("30398523", 6), "30.398523")
        self.assertEqual(units("123456789012345678901234567890123", 6),
                         "123456789012345678901234567.890123")
        for raw, decimals in [("-1", 6), ("1.5", 6), ("1", -1)]:
            with self.assertRaises(ValueError):
                units(raw, decimals)

    def test_committed_summary_is_consistent(self):
        result = check_summary(self.summary)
        self.assertEqual(result["window_seconds"], 1209600)
        self.assertEqual(result["recorded_contiguous_pages"], {"fills": 61, "refunds": 61})
        self.assertEqual(result["reported_repayment_chain_counts"]["other_chain_ids"], 767)

    def test_rejects_counter_mismatch(self):
        changed = copy.deepcopy(self.summary)
        changed["fill_repayment_chain_counts"]["42161"] += 1
        with self.assertRaisesRegex(ValueError, "do not sum"):
            check_summary(changed)

    def test_rejects_page_gap(self):
        changed = copy.deepcopy(self.summary)
        page = next(r for r in changed["request_manifest"] if r["name"].startswith("fills-"))
        page["params"][0]["fromBlock"] = hex(int(page["params"][0]["fromBlock"], 16) + 1)
        with self.assertRaisesRegex(ValueError, "Missing, overlapping"):
            check_summary(changed)

    def test_rejects_wrong_actor_filter(self):
        changed = copy.deepcopy(self.summary)
        page = next(r for r in changed["request_manifest"] if r["name"].startswith("fills-"))
        page["params"][0]["topics"][3] = "0x" + "0" * 64
        with self.assertRaisesRegex(ValueError, "actor filter"):
            check_summary(changed)

    def test_rejects_witness_outside_interval(self):
        changed = copy.deepcopy(self.witnesses)
        changed["fill_boundaries"][0]["block_number"] = self.summary["open_block_excluded"]
        with self.assertRaisesRegex(ValueError, "outside interval"):
            check_witnesses(self.summary, changed)

    def test_rejects_allocation_payment_mismatch(self):
        changed = copy.deepcopy(self.witnesses)
        changed["actual_pool_to_actor_transfers"][0]["amount_raw"] = "300001"
        with self.assertRaisesRegex(ValueError, "allocation/transfer mismatch"):
            check_witnesses(self.summary, changed)

    def test_does_not_promote_evidence(self):
        result = build_output()
        self.assertEqual(result["network_rpc_requests_performed_by_this_checker"], 0)
        for field, value in result["unverified"].items():
            self.assertIs(value, False if field.startswith("qualifies_") else None)
        self.assertFalse(result["witnesses"]["example_refund_transaction_sender_is_selected_actor"])


if __name__ == "__main__":
    unittest.main()
