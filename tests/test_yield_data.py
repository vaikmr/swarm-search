import math
import unittest
from research_tools.yield_data import (
    DataError, PublicData, YEAR_SECONDS, finite, funding_carry, lending_carry,
    lending_points, timestamp,
)


class LendingTests(unittest.TestCase):
    def test_one_year_apy(self):
        result = lending_carry([(0, 5), (YEAR_SECONDS, 5)], 0, YEAR_SECONDS,
                               10000, 15, max_gap_s=YEAR_SECONDS)
        self.assertAlmostEqual(result["gross_carry_usd"], 500)
        self.assertAlmostEqual(result["net_after_explicit_costs_only_usd"], 485)
        self.assertEqual(result["evidence_tier"], "T4")

    def test_left_point_no_lookahead(self):
        result = lending_carry([(0, 0), (86400, 100)], 0, 86400, 10000, 0)
        self.assertEqual(result["gross_carry_usd"], 0)

    def test_unknown_cost_suppresses_net(self):
        result = lending_carry([(0, 5), (86400, 5)], 0, 86400, 10000, None)
        self.assertIsNone(result["net_after_explicit_costs_only_usd"])
        self.assertEqual(result["costs_status"], "unknown")

    def test_missing_and_stale_chart_fail(self):
        for points, start, end in [([(1, 5), (10, 5)], 0, 10),
                                    ([(0, 5), (10, 5)], 0, 11),
                                    ([(0, 5), (200000, 5)], 0, 200000),
                                    ([(0, 5), (0, 6)], 0, 1)]:
            with self.assertRaises(DataError):
                lending_carry(points, start, end, 10000, 0)

    def test_chart_missing_base_not_total_fallback(self):
        with self.assertRaises(DataError):
            lending_points({"status": "success", "data": [
                {"timestamp": "2026-10-29T00:00:00Z", "apy": 20, "apyBase": None}]})

    def test_finite_strict(self):
        for value in [None, True, math.nan, math.inf, "nan"]:
            with self.assertRaises(DataError):
                finite(value, "test")
        with self.assertRaises(DataError):
            timestamp("2026-10-29")


class FundingTests(unittest.TestCase):
    def test_sign_and_explicit_costs(self):
        rows = [{"time": 3600000, "fundingRate": ".0001"},
                {"time": 7200000, "fundingRate": "-.0002"}]
        result = funding_carry(rows, 1, 7200000, 10000, 2)
        self.assertAlmostEqual(result["gross_short_funding_usd"], -1)
        self.assertAlmostEqual(result["net_component_after_explicit_costs_only_usd"], -3)

    def test_unknown_cost_suppresses_net(self):
        result = funding_carry([{"time": 3600000, "fundingRate": ".0001"}],
                               1, 3600000, 10000, None)
        self.assertIsNone(result["net_component_after_explicit_costs_only_usd"])

    def test_gaps_and_empty_fail(self):
        for rows in [[], [{"time": 1, "fundingRate": 0},
                          {"time": 7200001, "fundingRate": 0}]]:
            with self.assertRaises(DataError):
                funding_carry(rows, 1, 7200001, 10000, 0)

    def test_duplicate_fails(self):
        with self.assertRaises(DataError):
            funding_carry([{"time": 3600000, "fundingRate": 0}]*2,
                          1, 7200000, 10000, 0)

    def test_public_request_allowlist(self):
        for url, body in [
            ("https://api.hyperliquid.xyz/exchange", {"type": "order"}),
            ("https://api.hyperliquid.xyz/info", {"type": "order"}),
            ("http://yields.llama.fi/pools", None),
        ]:
            with self.assertRaises(DataError):
                PublicData()._read(url, body)

    def test_pagination_inclusive_boundary(self):
        class Stub(PublicData):
            def _read(self, url, body=None):
                cursor = body["startTime"]
                count = 500 if cursor == 1 else 2
                return {"payload": [{"time": cursor+i, "coin": "BTC",
                                     "fundingRate": ".1"} for i in range(count)]}
        result = Stub().funding_history("BTC", 1, 1000)
        self.assertEqual(len(result["rows"]), 502)
        self.assertEqual(result["rows"][500]["time"], 501)

    def test_pagination_no_progress_fails(self):
        class Stub(PublicData):
            def _read(self, url, body=None):
                return {"payload": [{"time": 0, "coin": "BTC", "fundingRate": 0}]}
        with self.assertRaises(DataError):
            Stub().funding_history("BTC", 1, 1000)


if __name__ == "__main__":
    unittest.main()
