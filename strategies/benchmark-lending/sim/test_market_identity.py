import unittest
from snapshot_market_identity import BLOCK, validate_header


class HeaderValidationTests(unittest.TestCase):
    def setUp(self):
        self.header = {"number": BLOCK, "hash": "0x" + "ab" * 32,
                       "timestamp": "0x6ae2f6cb"}

    def test_preserves_actual_header_fields(self):
        result = validate_header(self.header, BLOCK)
        self.assertEqual(result["block"], int(self.header["number"], 16))
        self.assertEqual(result["returned_block_number"], self.header["number"])
        self.assertEqual(result["block_hash"], self.header["hash"])
        self.assertEqual(result["returned_block_timestamp"], self.header["timestamp"])

    def test_substituted_latest_header_is_rejected(self):
        self.header["number"] = hex(int(BLOCK, 16) + 1)
        with self.assertRaisesRegex(ValueError, "does not match"):
            validate_header(self.header, BLOCK)

    def test_null_or_malformed_headers_are_rejected(self):
        for header in (None, [], "header", {}, {**self.header, "number": None},
                       {**self.header, "number": "latest"}, {**self.header, "number": "0xzz"},
                       {**self.header, "hash": "0x12"}, {**self.header, "timestamp": None},
                       {**self.header, "timestamp": "0x" + "f" * 100}):
            with self.subTest(header=header), self.assertRaises(ValueError):
                validate_header(header, BLOCK)

    def test_invalid_requested_tag_is_rejected(self):
        for tag in (None, "latest", 26296884):
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                validate_header(self.header, tag)


if __name__ == "__main__":
    unittest.main()
