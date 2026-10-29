"""Synthetic parser checks only; fixtures are not market observations."""

from decimal import Decimal
import unittest

from verify_funding_histories import validated_records


class FundingHistoryInputTest(unittest.TestCase):
    def test_preserves_negative_funding(self):
        result = validated_records([[1000, "0.01"], [2000, "-0.02"]])
        self.assertEqual(sum(r for _, r in result), Decimal("-0.01"))

    def test_rejects_duplicate_or_unsorted_timestamps(self):
        for rows in (
            [[1000, "0.01"], [1000, "0.01"]],
            [[2000, "0.01"], [1000, "0.01"]],
        ):
            with self.subTest(rows=rows):
                with self.assertRaises(ValueError):
                    validated_records(rows)

    def test_rejects_nonfinite_rates(self):
        for value in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validated_records([[1000, value]])

    def test_rejects_noninteger_timestamp(self):
        with self.assertRaises(ValueError):
            validated_records([[1000.0, "0.01"]])


if __name__ == "__main__":
    unittest.main()
