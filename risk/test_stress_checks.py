import copy
from decimal import Decimal
import unittest

from stress_checks import (
    amount, concentration, conditional_loss, example_output,
    example_position, zero_breach_upper_bound,
)


class StressArithmeticTests(unittest.TestCase):
    def test_depeg_loss_not_return_evidence(self):
        result = conditional_loss("15000", "0.13")
        self.assertEqual(Decimal(result["conditional_loss_usd"]), Decimal("1950"))
        self.assertEqual(Decimal(result["portfolio_loss_fraction"]), Decimal("0.039"))
        self.assertFalse(result["exceeds_monthly_severity_limit"])
        self.assertIsNone(result["annual_probability"])
        self.assertFalse(result["risk_certificate"])

    def test_total_loss_breaches_severity_but_does_not_invent_frequency(self):
        result = conditional_loss("15000", 1)
        self.assertTrue(result["exceeds_monthly_severity_limit"])
        self.assertTrue(result["exceeds_annual_scenario_severity_limit"])
        self.assertFalse(result["annual_kill_gate_established"])

    def test_exact_thresholds_are_not_strict_breaches(self):
        self.assertFalse(conditional_loss("5000", 1)["exceeds_monthly_severity_limit"])
        self.assertFalse(conditional_loss("10000", 1)["exceeds_annual_scenario_severity_limit"])
        self.assertTrue(conditional_loss("10000.01", 1)["exceeds_annual_scenario_severity_limit"])

    def test_invalid_money_and_severity_fail(self):
        for value in [True, False, "NaN", "Infinity", "-1", "bad", None]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                amount(value)
        with self.assertRaises(ValueError):
            conditional_loss(100, "1.01")
        with self.assertRaises(ValueError):
            conditional_loss(100, 1, capital=0)

    def test_same_protocol_and_coin_aggregate_across_chains(self):
        positions = [
            example_position("one", 15000, chain={"A": "15000"}, protocol={"Shared": "15000"}, stablecoin={"Coin": "15000"}),
            example_position("two", 15000, chain={"B": "15000"}, protocol={"Shared": "15000"}, stablecoin={"Coin": "15000"}),
            example_position("reserve", 20000),
        ]
        result = concentration(positions)
        self.assertEqual({x["category"] for x in result["domain_breaches"]}, {"protocol", "stablecoin"})
        self.assertEqual(Decimal(result["exposures_usd"]["protocol"]["Shared"]), Decimal("30000"))
        self.assertFalse(result["risk_certificate"])

    def test_declared_gross_exposure_not_only_equity(self):
        positions = [example_position("one", 50000, protocol={"P": "100000"})]
        self.assertEqual(concentration(positions)["domain_breaches"][0]["exposure_usd"], "100000")

    def test_four_chain_allocation_violates_chain_count_even_if_each_below_cap(self):
        positions = [
            example_position(str(i), 12500, chain={str(i): "12500"})
            for i in range(4)
        ]
        result = concentration(positions)
        self.assertTrue(result["chain_count_breach"])
        self.assertEqual(result["domain_breaches"], [])

    def test_equity_reconciliation_and_missing_domains(self):
        with self.assertRaises(ValueError):
            concentration([example_position("one", 49999)])
        bad = example_position("one", 50000)
        del bad["exposures_usd"]["bridge"]
        with self.assertRaises(ValueError):
            concentration([bad])

    def test_duplicate_position_ids_and_unknown_domain_fail(self):
        one = example_position("one", 25000)
        with self.assertRaises(ValueError):
            concentration([one, copy.deepcopy(one)])
        bad = example_position("bad", 50000)
        bad["exposures_usd"]["unrecognized"] = {}
        with self.assertRaises(ValueError):
            concentration([bad])

    def test_chain_and_cap_input_validation(self):
        for limit in [0, -1, True, 1.5]:
            with self.assertRaises(ValueError):
                concentration([], max_chains=limit)
        with self.assertRaises(ValueError):
            concentration([], cap_fraction="1.01")
        with self.assertRaises(ValueError):
            concentration([], capital=0)

    def test_statistical_example_does_not_claim_observed_coverage(self):
        self.assertGreater(zero_breach_upper_bound(298), 0.01)
        self.assertLess(zero_breach_upper_bound(299), 0.01)
        self.assertAlmostEqual(zero_breach_upper_bound(1), 0.95)
        for months in [0, -1, 1.5, True]:
            with self.assertRaises(ValueError):
                zero_breach_upper_bound(months)
        for alpha in [0, 1, float("nan"), True]:
            with self.assertRaises(ValueError):
                zero_breach_upper_bound(1, alpha)

    def test_allocation_arithmetic_and_fixture_are_not_certified(self):
        result = example_output()
        self.assertEqual(Decimal(result["allocation_arithmetic"]["min_offchain_usd"]), Decimal("5000"))
        fixture = result["hypothetical_declared_allocation"]
        self.assertEqual(fixture["domain_breaches"], [])
        self.assertFalse(fixture["chain_count_breach"])
        self.assertFalse(fixture["risk_certificate"])
        self.assertFalse(result["risk_certificate"])


if __name__ == "__main__":
    unittest.main()
