"""All inputs are SYNTHETIC unit-test fixtures, not trading observations."""

from copy import deepcopy
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal as D
import unittest

from research_tools.evidence import EvidenceError
from research_tools.replay import (
    COST_KEYS, SCENARIOS, ReplayInput, Scenario, quantile, run_replay, sensitivity_matrix,
)


def costs(gas="0", protocol="0"):
    return {key: gas if key == "gas_all_in" else protocol if key == "protocol" else "0"
            for key in COST_KEYS}


def opportunity(identifier="SYNTHETIC-1"):
    return {
        "id": identifier, "decision_at": "2026-09-01T00:00:00Z",
        "settlement_at": "2026-09-02T00:00:00Z",
        "latest_fill_at": "2026-09-01T00:00:01Z",
        "competitor_arrival_at": "2026-09-01T00:00:00.200Z",
        "measured_latency_ms": 100, "capital_usd": "10000", "gross_pnl_usd": "100",
        "success_costs": costs("2", "3"), "failed_costs": costs("1"),
        "attempt_on_loss": True, "race_proven": True,
        "marks": [{"at": "2026-09-02T00:00:00Z", "cumulative_gross_pnl_usd": "100"}],
        "source_ids": ["SYNTHETIC-NOT-MARKET-DATA"],
    }


def fixture():
    return {
        "schema_version": 1, "paper_only": True, "data_kind": "synthetic",
        "start": "2026-09-01T00:00:00Z", "end": "2026-10-01T00:00:00Z",
        "initial_capital_usd": "50000", "infrastructure_per_30d_usd": "30",
        "benchmark_period_net_usd": "5", "inventory_marks_complete": True,
        "gross_excludes_all_costs_and_external_flows": True,
        "gas_all_in_includes_base_priority_l1_operator": True,
        "source_ids": ["SYNTHETIC-NOT-MARKET-DATA"], "opportunities": [opportunity()],
    }


class ReplayTests(unittest.TestCase):
    def run_fixture(self, row=None, scenario=None):
        return run_replay(ReplayInput.parse(row or fixture()), scenario or SCENARIOS[0])

    def test_costs_net_benchmark_and_30day_sample_reconcile(self):
        result = self.run_fixture()
        self.assertEqual(D(result["net_economic_pnl_usd"]), D("65"))
        self.assertEqual(D(result["benchmark_excess_usd"]), D("60"))
        self.assertEqual(D(result["terminal_equity_usd"]), D("50065"))
        self.assertEqual(D(result["equity_curve"][-1]["equity_usd"]), D("50065"))
        self.assertEqual(D(result["rolling_30d_pnl_usd"]["p50"]), D("65"))
        self.assertEqual(result["rolling_30d_pnl_usd"]["window_count"], 1)
        self.assertFalse(result["is_t2_evidence"])
        self.assertEqual(result["evidence_tier"], "T4")
        self.assertFalse(result["recommendation_eligible"])

    def test_marked_economics_are_not_labeled_received_cash(self):
        # A final MTM/accrual mark does not establish asset sales, token receipts,
        # external transfers, or the realized-cash component of economic PnL.
        row = fixture()
        result = self.run_fixture(row)
        self.assertEqual(D(result["gross_pnl_usd"]), D("100"))
        self.assertEqual(D(result["net_economic_pnl_usd"]), D("65"))
        self.assertIsNone(result["realized_cash_pnl_usd"])
        self.assertNotIn("cash_net_pnl_usd", result)
        self.assertEqual(result["evidence_tier"], "T4")

    def test_latency_stress_loses_tie_and_charges_failed_gas(self):
        result = self.run_fixture(scenario=Scenario("tie", added_latency_ms=100))
        self.assertEqual(result["outcome_counts"]["lost_or_tied_race"], 1)
        self.assertEqual(D(result["net_economic_pnl_usd"]), D("-31"))
        self.assertEqual(D(result["failed_attempt_cost_usd"]), D("1"))

    def test_unproven_and_unknown_races_lose(self):
        for field, value in (("race_proven", False), ("competitor_arrival_at", None)):
            row = fixture()
            row["opportunities"][0][field] = value
            self.assertEqual(self.run_fixture(row)["outcome_counts"]["unproven_race"], 1)

    def test_no_attempt_means_no_failure_fee(self):
        row = fixture()
        row["opportunities"][0]["race_proven"] = False
        row["opportunities"][0]["attempt_on_loss"] = False
        self.assertEqual(D(self.run_fixture(row)["net_economic_pnl_usd"]), D("-30"))

    def test_gas_stress_doubles_only_gas(self):
        result = self.run_fixture(scenario=Scenario("gas", gas_multiplier=D("2")))
        self.assertEqual(D(result["variable_cost_usd"]), D("7"))
        self.assertEqual(D(result["net_economic_pnl_usd"]), D("63"))

    def test_capital_cannot_be_reused_during_lock(self):
        row = fixture()
        a = row["opportunities"][0]
        a["capital_usd"] = "30000"
        b = deepcopy(a)
        b["id"] = "SYNTHETIC-2"
        b["decision_at"] = "2026-09-01T00:00:00.001Z"
        row["opportunities"].append(b)
        result = self.run_fixture(row)
        self.assertEqual(result["outcome_counts"]["filled"], 1)
        self.assertEqual(result["outcome_counts"]["insufficient_capital"], 1)
        self.assertEqual(D(result["capital_utilization_fraction"]), D("0.02"))

    def test_losses_and_fee_budget_reduce_available_capital(self):
        row = fixture()
        row["opportunities"][0]["capital_usd"] = "50000"
        self.assertEqual(self.run_fixture(row)["outcome_counts"]["insufficient_capital"], 1)
        row["opportunities"][0]["capital_usd"] = "10000"
        row["opportunities"][0]["gross_pnl_usd"] = "-40000"
        row["opportunities"][0]["marks"][-1]["cumulative_gross_pnl_usd"] = "-40000"
        b = opportunity("SYNTHETIC-2")
        b.update(decision_at="2026-09-03T00:00:00Z",
                 latest_fill_at="2026-09-03T00:00:01Z",
                 competitor_arrival_at="2026-09-03T00:00:00.200Z",
                 settlement_at="2026-09-04T00:00:00Z",
                 marks=[{"at": "2026-09-04T00:00:00Z", "cumulative_gross_pnl_usd": "100"}])
        row["opportunities"].append(b)
        self.assertEqual(self.run_fixture(row)["outcome_counts"]["insufficient_capital"], 1)

    def test_interim_loss_not_hidden_by_profitable_settlement(self):
        row = fixture()
        row["opportunities"][0]["marks"].insert(
            0, {"at": "2026-09-01T12:00:00Z", "cumulative_gross_pnl_usd": "-6000"})
        result = self.run_fixture(row)
        self.assertGreater(D(result["marked_max_drawdown_usd"]), D("6000"))
        self.assertGreater(D(result["marked_max_drawdown_fraction"]), D(".10"))

    def test_incomplete_marks_do_not_produce_drawdown_claim(self):
        row = fixture()
        row["inventory_marks_complete"] = False
        result = self.run_fixture(row)
        self.assertIsNone(result["marked_max_drawdown_usd"])
        self.assertTrue(result["drawdown_is_lower_bound_unless_marks_complete"])

    def test_capture_stress_takes_closest_margin_entrant_win(self):
        row = fixture()
        loser = opportunity("SYNTHETIC-incumbent")
        loser["competitor_arrival_at"] = "2026-09-01T00:00:00.050Z"
        row["opportunities"].append(loser)
        base = self.run_fixture(row)
        stressed = self.run_fixture(row, Scenario("capture", incumbent_capture_multiplier=D("1.2")))
        self.assertEqual(base["outcome_counts"]["filled"], 1)
        self.assertEqual(stressed["outcome_counts"]["incumbent_capture_stress"], 1)
        self.assertNotIn("filled", stressed["outcome_counts"])

    def test_short_window_never_annualizes_to_monthly(self):
        row = fixture()
        row["end"] = "2026-09-03T00:00:00Z"
        result = self.run_fixture(row)
        self.assertEqual(result["rolling_30d_pnl_usd"]["window_count"], 0)
        self.assertIsNone(result["rolling_30d_pnl_usd"]["p50"])

    def test_invalid_costs_marks_sources_duplicates_and_schema(self):
        variants = []
        row = fixture()
        del row["opportunities"][0]["success_costs"]["bridge"]
        variants.append(row)
        row = fixture()
        row["opportunities"][0]["marks"][-1]["cumulative_gross_pnl_usd"] = "99"
        variants.append(row)
        row = fixture()
        row["opportunities"][0]["source_ids"] = ["unknown"]
        variants.append(row)
        row = fixture()
        row["opportunities"] *= 2
        variants.append(row)
        row = fixture()
        row["schema_version"] = True
        variants.append(row)
        for row in variants:
            with self.assertRaises(EvidenceError):
                ReplayInput.parse(row)

    def test_sensitivity_matrix_has_all_requested_stresses(self):
        matrix = sensitivity_matrix(ReplayInput.parse(fixture()))
        self.assertEqual(len(matrix), 6)
        self.assertIn("latency_plus_50ms", [entry["scenario"] for entry in matrix])
        self.assertIn("latency_plus_200ms", [entry["scenario"] for entry in matrix])
        self.assertTrue(all(entry["is_t2_evidence"] is False for entry in matrix))

    def test_quantiles_are_descriptive_and_decimal(self):
        self.assertEqual(quantile([D("0"), D("100")], D(".05")), D("5"))
        self.assertIsNone(quantile([], D(".5")))


if __name__ == "__main__":
    unittest.main()
