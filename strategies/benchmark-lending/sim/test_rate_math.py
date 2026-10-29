import datetime as dt
import math
import unittest
from fetch_public_rates import integrate


class RateMathTests(unittest.TestCase):
    def setUp(self):
        self.start = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)

    def test_annual_apy_is_not_divided_by_twelve(self):
        end = self.start + dt.timedelta(days=30)
        rows = [{"timestamp": (self.start + dt.timedelta(days=i)).isoformat(), "apy": 5} for i in range(31)]
        value = integrate(rows, self.start, end, "apy")
        self.assertAlmostEqual(value["gross_usd_on_50000"], 50000 * ((1.05) ** (30 / 365) - 1), places=8)
        self.assertAlmostEqual(value["coverage_fraction"], 1)

    def test_missing_field_does_not_become_zero(self):
        value = integrate([{"timestamp": self.start.isoformat()}], self.start, self.start + dt.timedelta(days=1), "apyBase")
        self.assertEqual(value["coverage_fraction"], 0)
        self.assertIsNone(value["time_weighted_mean_apy_pct"])

    def test_large_gap_is_not_silently_filled(self):
        value = integrate([{"timestamp": self.start.isoformat(), "apy": 5}], self.start, self.start + dt.timedelta(days=3), "apy")
        self.assertEqual(value["coverage_fraction"], 0)

    def test_future_sample_does_not_earn_past_yield(self):
        rows = [{"timestamp": (self.start + dt.timedelta(days=1)).isoformat(), "apy": 5}]
        value = integrate(rows, self.start, self.start + dt.timedelta(days=1), "apy")
        self.assertEqual(value["gross_usd_on_50000"], 0)


if __name__ == "__main__":
    unittest.main()
