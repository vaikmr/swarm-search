import unittest
from build_lower_deployment import stress


class LowerDeploymentTests(unittest.TestCase):
    def test_four_thousand_passes_only_component_cost_stresses(self):
        r = stress(4000, 500)
        self.assertEqual(r["monthly_pct_of_initial_total"], 9)
        self.assertEqual(r["annual_pct_of_initial_total"], 20)
        self.assertTrue(r["within_monthly_10pct_component_bound"])
        self.assertTrue(r["within_annual_20pct_component_bound"])
        self.assertIsNone(r["portfolio_tail_probability"])

    def test_monthly_budget_does_not_establish_annual_budget(self):
        r = stress(4500, 500)
        self.assertTrue(r["within_monthly_10pct_component_bound"])
        self.assertFalse(r["within_annual_20pct_component_bound"])

    def test_fifteen_thousand_is_not_a_ten_percent_full_loss_bound(self):
        self.assertFalse(stress(15000, 0)["within_monthly_10pct_component_bound"])

    def test_zero_cost_is_only_an_explicit_scenario(self):
        self.assertTrue(stress(5000, 0)["within_monthly_10pct_component_bound"])
        self.assertFalse(stress(5000, 500)["within_monthly_10pct_component_bound"])

    def test_invalid_budget_fails(self):
        for args in ((-1, 500), (50001, 500), (4000, -1)):
            with self.assertRaises(ValueError):
                stress(*args)


if __name__ == "__main__":
    unittest.main()
