import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "public_scout", Path(__file__).with_name("collect_public.py")
)
scout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scout)


class PublicScoutTests(unittest.TestCase):
    def test_signed_order_material_is_not_saved(self):
        result = scout.select_payload("uniswapx_base", {"orders": [{
            "signature": "DO_NOT_PERSIST", "encodedOrder": "DO_NOT_PERSIST",
            "txHash": "public-hash", "cosignerData": {"exclusiveFiller": "actor"},
        }]})
        self.assertNotIn("signature", result[0])
        self.assertNotIn("encodedOrder", result[0])
        self.assertEqual(result[0]["exclusive_filler"], "actor")

    def test_registration_examples_are_visible(self):
        selected = scout.select_payload("across_registrations", [{
            "name": "example.json", "type": "file",
        }])
        summary = scout.summarize("across_registrations", selected)
        self.assertEqual(summary["example_files"], ["example.json"])

    def test_bad_shapes_are_rejected(self):
        for name, body in (("across_fills", {}), ("uniswapx_base", []),
                           ("across_registrations", {}), ("across_configs", None)):
            with self.subTest(name=name), self.assertRaises(ValueError):
                scout.select_payload(name, body)

    def test_actor_count_is_only_sample_count(self):
        selected = scout.select_payload("across_fills", [
            {"relayer": "0xAB", "status": "filled", "depositBlockTimestamp": "b"},
            {"relayer": "0xab", "status": "filled", "depositBlockTimestamp": "a"},
            {"relayer": None, "status": "unfilled"},
        ])
        summary = scout.summarize("across_fills", selected)
        self.assertEqual(summary["sample_rows"], 3)
        self.assertEqual(summary["relayer_counts_in_sample_only"], {"0xab": 2})
        self.assertEqual(summary["deposit_timestamp_min"], "a")
        self.assertNotIn("profit", summary)

    def test_zero_address_is_not_a_competitor(self):
        summary = scout.summarize("uniswapx_base", [
            {"exclusive_filler": "0x0000000000000000000000000000000000000000"},
            {"exclusive_filler": None},
            {"exclusive_filler": "0xAB"},
        ])
        self.assertEqual(summary["exclusive_filler_counts_in_sample_only"], {"0xab": 1})
        self.assertEqual(summary["orders_without_exclusive_filler"], 2)

    def test_fixed_public_get_endpoints_only(self):
        self.assertTrue(all(url.startswith("https://") for url in scout.ENDPOINTS.values()))
        self.assertEqual(len(scout.ENDPOINTS), 4)

    def test_receipt_helper_rejects_writes_before_network_access(self):
        receipt_spec = importlib.util.spec_from_file_location(
            "receipt_probe",
            Path(__file__).parents[2] / "intent-solvers/evidence/verify_public_receipts.py",
        )
        receipt = importlib.util.module_from_spec(receipt_spec)
        receipt_spec.loader.exec_module(receipt)
        with self.assertRaises(ValueError):
            receipt.rpc_read("https://example.invalid", "not-a-read-method", [])


if __name__ == "__main__":
    unittest.main()
