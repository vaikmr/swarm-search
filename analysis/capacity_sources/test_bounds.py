"""Arithmetic checks only. No market data, fork, execution or paper fills."""

import math
import unittest

from calculate_bounds import (
    build_output,
    deployment_bound,
    ideal_lock_turnover,
    paired_notional_bound,
    required_turnover,
    workload_cost,
)


class CapacityBoundsTest(unittest.TestCase):
    def test_literal_chain_limits_leave_reserve(self):
        result = deployment_bound(50000, 0.30, 3)
        self.assertEqual(result["per_domain_cap_usd"], 15000)
        self.assertEqual(result["onchain_upper_bound_usd"], 45000)
        self.assertEqual(result["offchain_or_unallocated_lower_bound_usd"], 5000)

    def test_deployment_never_exceeds_capital(self):
        self.assertEqual(deployment_bound(50000, 0.3, 4)["onchain_upper_bound_usd"], 50000)
        self.assertEqual(deployment_bound(50000, 0.3, 0)["onchain_upper_bound_usd"], 0)

    def test_bps_are_not_percent(self):
        self.assertEqual(required_turnover(2000, 500, 1), 25000000)
        self.assertEqual(required_turnover(5000, 500, 10), 5500000)

    def test_fixed_cost_is_added_once(self):
        self.assertEqual(required_turnover(2000, 0, 10), 2000000)
        self.assertEqual(required_turnover(2000, 500, 10), 2500000)

    def test_capital_reuse_in_ideal_fluid_bound(self):
        self.assertEqual(ideal_lock_turnover(15000, 24), 450000)
        self.assertEqual(ideal_lock_turnover(15000, 6), 1800000)

    def test_paired_notional_uses_both_legs(self):
        self.assertEqual(paired_notional_bound(45000, 2, 15000), 30000)
        self.assertEqual(paired_notional_bound(15000, 2, 15000), 10000)
        self.assertEqual(paired_notional_bound(45000, 1, 15000), 15000)

    def test_hypothetical_rpc_cost_units(self):
        result = workload_cost(3, 1, 100)
        self.assertEqual(result["calls_per_month"], 7776000)
        self.assertEqual(result["cu_per_month"], 777600000)
        self.assertAlmostEqual(result["payg_compute_only_usd"], 404.352)

    def test_invalid_inputs_fail_closed(self):
        calls = [
            lambda: deployment_bound(50000, 1.01, 3),
            lambda: deployment_bound(50000, 0.3, -1),
            lambda: deployment_bound(50000, 0.3, 1.5),
            lambda: required_turnover(2000, 500, 0),
            lambda: required_turnover(2000, -1, 1),
            lambda: required_turnover(2000, 500, math.nan),
            lambda: ideal_lock_turnover(15000, 0),
            lambda: paired_notional_bound(45000, 3, 15000),
            lambda: workload_cost(3, math.inf, 10),
        ]
        for call in calls:
            with self.subTest(call=call):
                with self.assertRaises(ValueError):
                    call()

    def test_output_never_claims_performance(self):
        result = build_output()
        self.assertTrue(result["not_performance"])
        self.assertTrue(result["evidence_tier"].startswith("T4"))
        self.assertEqual(result["funding_requirement"]["paired_notional_upper_bound_usd"], 30000)


if __name__ == "__main__":
    unittest.main()
