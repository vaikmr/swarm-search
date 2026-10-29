import copy
import json
from pathlib import Path
import unittest
from collect_actor_ledger import ACTOR, USDC, TRANSFER
from collect_actor_ledger import ATOKEN
from reconcile_actor_ledger import check_index, partition_interest, receipt_fee, reconcile, signed, verify_log


class ActorLedgerTests(unittest.TestCase):
    """Synthetic validation cases, not actor performance evidence."""
    def test_deployed_floor_rounding_is_not_legacy_half_up(self):
        endpoint = {"scaled": "1", "index": str(10**27 + 6 * 10**26), "aUSDC": "1"}
        check_index(endpoint)
        with self.assertRaises(ValueError):
            check_index({**endpoint, "aUSDC": "2"})

    def test_network_fee_includes_base_and_priority_effective_price(self):
        self.assertEqual(receipt_fee({"gasUsed": "0x10", "effectiveGasPrice": "0x20"}), 512)
        self.assertEqual(receipt_fee({"gasUsed": "0x10", "effectiveGasPrice": "0x20",
                                      "blobGasUsed": "0x2", "blobGasPrice": "0x3"}), 518)

    def test_missing_blob_component_is_unknown_not_zero(self):
        with self.assertRaises(ValueError):
            receipt_fee({"gasUsed": "0x10", "effectiveGasPrice": "0x20", "blobGasUsed": "0x2"})
        with self.assertRaises(ValueError):
            receipt_fee({"type": "0x3", "gasUsed": "0x10", "effectiveGasPrice": "0x20"})

    def test_self_transfer_is_not_new_capital(self):
        self.assertEqual(signed(10, ACTOR, ACTOR), 0)
        with self.assertRaises(ValueError):
            signed(10, "other", "other")

    def fixture(self):
        sender = "0x" + "1" * 40
        row = {"token": USDC, "from": sender, "to": ACTOR, "raw_value": "7",
               "block": 20, "log_index": 3}
        log = {"address": USDC, "topics": [TRANSFER, "0x" + sender[2:].rjust(64, "0"),
                                          "0x" + ACTOR[2:].rjust(64, "0")],
               "data": "0x7", "logIndex": "0x3"}
        return row, {"status": "0x1", "blockNumber": "0x14", "logs": [log]}

    def test_transfer_must_match_actual_receipt(self):
        row, receipt = self.fixture()
        verify_log(row, receipt)
        for field, value in (("data", "0x8"), ("address", "0x" + "f" * 40)):
            bad = copy.deepcopy(receipt)
            bad["logs"][0][field] = value
            with self.assertRaises(ValueError):
                verify_log(row, bad)

    def test_missing_duplicate_or_failed_receipt_is_rejected(self):
        row, receipt = self.fixture()
        for bad in ({**receipt, "logs": []}, {**receipt, "logs": receipt["logs"] * 2},
                    {**receipt, "status": "0x0"}):
            with self.assertRaises(ValueError):
                verify_log(row, bad)

    def test_partial_withdrawal_does_not_close_a_segment(self):
        flows = []
        for i, value in enumerate((60, -40, 95, -200), 1):
            flows.append({"block": i, "log_index": 0, "tx": str(i), "raw_value": str(abs(value)),
                          "from": ATOKEN if value > 0 else ACTOR, "to": ACTOR if value > 0 else ATOKEN})
        realized, unclosed, rows = partition_interest(100, 205, flows, {"1": "50", "3": "0"})
        self.assertEqual(realized, 15)
        self.assertEqual(unclosed, 5)
        self.assertIsNone(rows[0]["completed_segment_cash_interest_usdc"])
        self.assertIsNotNone(rows[1]["completed_segment_cash_interest_usdc"])

    def test_missing_post_withdraw_inventory_cannot_be_assumed_zero(self):
        flow = {"block": 1, "log_index": 0, "tx": "1", "raw_value": "100", "from": ATOKEN, "to": ACTOR}
        with self.assertRaises(ValueError):
            partition_interest(100, 0, [flow], {})


class ObservedActorRegressionTests(unittest.TestCase):
    """Actual captured public observations, not synthetic return evidence."""
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / "evidence" / "actor-observations.json"
        cls.data = json.loads(path.read_text())

    def test_captured_units_receipts_and_gas_reconcile_without_tier_upgrade(self):
        result = reconcile(self.data)
        self.assertEqual(result["reconciliation"]["USDC_raw_cash_residual"], 0)
        self.assertEqual(result["reconciliation"]["ETH_wei_residual"], 0)
        self.assertEqual(result["transfers"]["receipt_checked_logs"], 126)
        self.assertEqual(result["observed_network_fees"]["paid_wei"], "334130451297696")
        self.assertEqual(result["reconciliation"]["post_opening_USDC_interest_units"], "194463.135111")
        self.assertFalse(result["T1_qualified"])
        self.assertIsNone(result["full_actor_net_pnl_usd"])

    def test_one_raw_unit_transfer_mutation_is_detected(self):
        bad = copy.deepcopy(self.data)
        bad["transfers"][0]["raw_value"] = str(int(bad["transfers"][0]["raw_value"]) + 1)
        with self.assertRaises(ValueError):
            reconcile(bad)

    def test_native_balance_mutation_is_detected(self):
        bad = copy.deepcopy(self.data)
        endpoint = bad["endpoints"][str(bad["end"])]
        endpoint["ETH"] = str(int(endpoint["ETH"]) + 1)
        with self.assertRaises(ValueError):
            reconcile(bad)

    def test_missing_historical_price_cannot_be_zero(self):
        bad = copy.deepcopy(self.data)
        bad["reference_prices_8_decimals"] = {}
        with self.assertRaises(KeyError):
            reconcile(bad)

    def test_short_or_unverified_window_is_rejected(self):
        bad = copy.deepcopy(self.data)
        bad["elapsed_seconds"] = 1
        with self.assertRaises(ValueError):
            reconcile(bad)


if __name__ == "__main__":
    unittest.main()
