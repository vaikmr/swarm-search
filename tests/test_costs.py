"""Synthetic accounting fixtures. Passing tests are not return evidence."""

import math
import unittest
from decimal import Decimal

from research_tools.costs import (
    COST_CATEGORIES,
    CostLine,
    Evidence,
    decimal,
    equity_pnl_usd,
    lending_income_usd,
    net_pnl,
    notional_fee_usd,
    required_gross_usd,
    required_return,
    transaction_fee_usd,
)


FIXTURE = Evidence("T4", "tests/test_costs.py", "Synthetic unit-test value, not market evidence")


def lines(**overrides):
    """An explicit zero is justified only for this synthetic fixture."""
    return [
        CostLine(category, overrides.get(category, "0"), FIXTURE)
        for category in COST_CATEGORIES
    ]


def report(costs=None, **overrides):
    kwargs = dict(
        total_capital_usd="50000",
        gross_strategy_pnl_usd="1000",
        gross_evidence=FIXTURE,
        idle_contribution_usd="25",
        idle_evidence=FIXTURE,
        costs=lines() if costs is None else costs,
        benchmark_net_usd="150",
        benchmark_evidence=FIXTURE,
    )
    kwargs.update(overrides)
    return net_pnl(**kwargs)


class CostTests(unittest.TestCase):
    def test_target_requirements_not_forecasts(self):
        self.assertEqual(required_return("2000", "50000"), Decimal(".04"))
        self.assertEqual(required_return("5000", "50000"), Decimal(".1"))
        self.assertEqual(required_gross_usd("2000", "500", "0"), Decimal("2500"))
        self.assertEqual(required_gross_usd("5000", "500", "0"), Decimal("5500"))

    def test_total_capital_denominator_includes_idle_and_locked(self):
        value = report(lines(infrastructure="100"))
        self.assertEqual(value.net_economic_pnl_usd, Decimal("925"))
        self.assertEqual(value.total_capital_return, Decimal(".0185"))
        self.assertEqual(value.excess_over_benchmark_usd, Decimal("775"))
        self.assertEqual(value.evidence_tiers, ("T4",))

    def test_benchmark_is_not_subtracted_from_economic_profit(self):
        a = report()
        b = report(benchmark_net_usd="700")
        self.assertEqual(a.net_economic_pnl_usd, b.net_economic_pnl_usd)
        self.assertNotEqual(a.excess_over_benchmark_usd, b.excess_over_benchmark_usd)

    def test_unknown_benchmark_does_not_silently_become_zero(self):
        value = report(benchmark_net_usd=None, benchmark_evidence=None)
        self.assertEqual(value.net_economic_pnl_usd, Decimal("1025"))
        self.assertIsNone(value.excess_over_benchmark_usd)
        self.assertTrue(value.benchmark_missing)

    def test_unknown_cost_suppresses_pnl(self):
        value = report(lines(bridge_rebalance=None))
        self.assertIsNone(value.net_economic_pnl_usd)
        self.assertIsNone(value.total_capital_return)
        self.assertIsNone(value.excess_over_benchmark_usd)
        self.assertIn("bridge_rebalance", value.missing_costs)

    def test_missing_costs_are_not_zero(self):
        value = report([])
        self.assertEqual(set(value.missing_costs), set(COST_CATEGORIES))
        self.assertIsNone(value.net_economic_pnl_usd)

    def test_included_slippage_lvr_not_deducted_twice(self):
        costs = [
            CostLine(line.category, "80", FIXTURE, True)
            if line.category in {"slippage", "lp_lvr"} else line
            for line in lines(infrastructure="100")
        ]
        value = report(costs)
        self.assertEqual(value.already_included_costs_usd, Decimal("160"))
        self.assertEqual(value.additional_costs_usd, Decimal("100"))
        self.assertEqual(value.net_economic_pnl_usd, Decimal("925"))

    def test_duplicate_category_rejected(self):
        with self.assertRaises(ValueError):
            report(lines() + [CostLine("slippage", "5", FIXTURE)])

    def test_budget_ceiling_is_inclusive_and_not_authorization(self):
        self.assertTrue(report(lines(infrastructure="500")).infrastructure_within_budget)
        self.assertFalse(report(lines(infrastructure="500.01")).infrastructure_within_budget)
        self.assertIsNone(report(lines(infrastructure=None)).infrastructure_within_budget)

    def test_gas_priority_data_operator_and_direct_bid(self):
        value = transaction_fee_usd(
            gas_used="100000", effective_gas_price_wei="2000000000",
            native_usd="2500", extra_l1_fee_wei="10000000000000",
            extra_operator_fee_wei="1000000000000",
            extra_auction_payment_wei="5000000000000",
        )
        self.assertEqual(value, Decimal(".54"))

    def test_failed_included_transaction_still_pays(self):
        # No success flag can accidentally exempt gas charged to a reverted tx.
        fee = transaction_fee_usd(
            gas_used="21000", effective_gas_price_wei="1000000000",
            native_usd="2000", extra_l1_fee_wei="0",
            extra_operator_fee_wei="0", extra_auction_payment_wei="0",
        )
        self.assertEqual(fee, Decimal(".042"))
        self.assertEqual(
            report(lines(execution_failed=fee)).net_economic_pnl_usd, Decimal("1024.958")
        )

    def test_arbitrum_embedded_poster_not_added_again(self):
        value = transaction_fee_usd(
            gas_used="300000", effective_gas_price_wei="10000000",
            native_usd="2000", extra_l1_fee_wei="0",
            extra_operator_fee_wei="0", extra_auction_payment_wei="0",
        )
        self.assertEqual(value, Decimal(".006"))

    def test_cex_filled_legs_each_incur_fees(self):
        fee = notional_fee_usd("15000", "80")
        self.assertEqual(fee, Decimal("120"))
        self.assertEqual(fee * 2, Decimal("240"))
        self.assertEqual(notional_fee_usd("15000", "5") * 2, Decimal("15"))

    def test_lending_apy_is_not_apr_divided_by_twelve(self):
        apy_income = lending_income_usd("15000", ".04", "30", rate_kind="apy")
        apr_income = lending_income_usd("15000", ".04", "30", rate_kind="apr")
        self.assertLess(apy_income, apr_income)
        independent = 15000 * math.expm1(math.log1p(.04) * (30 / 365))
        self.assertAlmostEqual(float(apy_income), independent, places=8)

    def test_lending_one_year_matches_definition(self):
        self.assertEqual(lending_income_usd("50000", ".05", "365", rate_kind="apy"), 2500)
        self.assertEqual(lending_income_usd("50000", ".05", "365", rate_kind="apr"), 2500)
        self.assertEqual(lending_income_usd("0", ".05", "30", rate_kind="apy"), 0)

    def test_external_flows_removed_internal_transfers_not_revenue(self):
        self.assertEqual(equity_pnl_usd("50000", "61000", "12000", "2000"), 1000)
        self.assertEqual(equity_pnl_usd("50000", "50000", "0", "0"), 0)

    def test_losses_are_allowed(self):
        value = report(gross_strategy_pnl_usd="-100", idle_contribution_usd="0")
        self.assertEqual(value.net_economic_pnl_usd, -100)
        self.assertEqual(value.total_capital_return, Decimal("-.002"))

    def test_entirely_unrealized_gain_is_economic_not_cash(self):
        # Stipulated receipts are zero; all 123 is unrealized marked appreciation.
        value = report(gross_strategy_pnl_usd="123", idle_contribution_usd="0")
        self.assertEqual(value.net_economic_pnl_usd, Decimal("123"))
        self.assertFalse(hasattr(value, "net_cash_pnl_usd"))
        self.assertFalse(hasattr(value, "realized_cash_pnl_usd"))

    def test_negative_idle_rate_is_accepted_without_clamping(self):
        idle_loss = lending_income_usd("1000", "-.01", "30", rate_kind="apy")
        self.assertLess(idle_loss, 0)
        value = report(gross_strategy_pnl_usd="0", idle_contribution_usd=idle_loss)
        # The rate helper computes at 40 digits; ledger arithmetic uses the
        # caller's Decimal context. Unary plus applies that same rounding.
        self.assertEqual(value.net_economic_pnl_usd, +idle_loss)
        self.assertLess(value.total_capital_return, 0)
        self.assertEqual(required_gross_usd("2000", "100", "-25"), Decimal("2125"))

    def test_idle_depeg_and_complete_default_losses_are_not_omitted(self):
        for idle_loss in ("-200", "-1000"):
            with self.subTest(idle_loss=idle_loss):
                value = report(
                    gross_strategy_pnl_usd="10", idle_contribution_usd=idle_loss
                )
                self.assertEqual(value.net_economic_pnl_usd, Decimal("10") + Decimal(idle_loss))
                already_in_whole_equity = report(
                    gross_strategy_pnl_usd=Decimal("10") + Decimal(idle_loss),
                    idle_contribution_usd="0",
                )
                self.assertEqual(
                    value.net_economic_pnl_usd,
                    already_in_whole_equity.net_economic_pnl_usd,
                )
        # Entire idle principal lost is supplied as a signed contribution, NOT
        # an APY=-100% input: rates and principal write-downs are different.
        self.assertEqual(
            report(gross_strategy_pnl_usd="0", idle_contribution_usd="-1000").net_economic_pnl_usd,
            Decimal("-1000"),
        )

    def test_strategy_only_and_whole_equity_idle_adapters_are_exclusive(self):
        strategy_only = report(
            gross_strategy_pnl_usd="0", idle_contribution_usd="100"
        )
        whole_portfolio = report(
            gross_strategy_pnl_usd=equity_pnl_usd("50000", "50100", "0", "0"),
            idle_contribution_usd="0",  # Included in the whole-equity input.
        )
        self.assertEqual(strategy_only.net_economic_pnl_usd, Decimal("100"))
        self.assertEqual(whole_portfolio.net_economic_pnl_usd, Decimal("100"))
        # Callers MUST NOT pass the same idle contribution through both paths.
        # The arithmetic cannot detect misclassified economic provenance.

    def test_whole_equity_paid_costs_are_audit_only(self):
        before_fees = report(
            lines(execution_success="20"),
            gross_strategy_pnl_usd="100", idle_contribution_usd="0",
        )
        embedded = [
            CostLine(line.category, line.amount_usd, line.evidence, True)
            for line in lines(execution_success="20")
        ]
        after_fees_equity = report(
            embedded, gross_strategy_pnl_usd="80", idle_contribution_usd="0"
        )
        self.assertEqual(before_fees.net_economic_pnl_usd, Decimal("80"))
        self.assertEqual(after_fees_equity.net_economic_pnl_usd, Decimal("80"))
        self.assertEqual(after_fees_equity.additional_costs_usd, Decimal("0"))

    def test_execution_only_and_all_in_receipt_adapters_are_exclusive(self):
        kwargs = dict(
            gas_used="100000", effective_gas_price_wei="2000000000",
            native_usd="2500", extra_l1_fee_wei="10000000000000",
            extra_operator_fee_wei="1000000000000",
            extra_auction_payment_wei="5000000000000",
        )
        all_in_fee = transaction_fee_usd(**kwargs)
        execution_only = transaction_fee_usd(
            **dict(kwargs, extra_l1_fee_wei="0", extra_operator_fee_wei="0",
                   extra_auction_payment_wei="0")
        )
        split = report(lines(
            execution_success=execution_only,
            data_operator_fees=".0275",
            auction_payments=".0125",
        ))
        # Alternative: book the helper's all-in .54 once. Extra categories are
        # explicit zero because their components are already in execution,
        # not because the chain did not charge them.
        embedded_evidence = Evidence(
            "T4", "tests/test_costs.py",
            "Synthetic component booked in execution_success all-in total",
        )
        all_in_lines = [
            CostLine(line.category, "0", embedded_evidence)
            if line.category in {"data_operator_fees", "auction_payments"} else line
            for line in lines(execution_success=all_in_fee)
        ]
        combined = report(all_in_lines)
        self.assertEqual(split.additional_costs_usd, Decimal(".54"))
        self.assertEqual(combined.additional_costs_usd, Decimal(".54"))
        self.assertEqual(split.net_economic_pnl_usd, combined.net_economic_pnl_usd)

    def test_evidence_and_benchmark_pair_required(self):
        with self.assertRaises(ValueError):
            Evidence("T5", "source", "invalid tier")
        with self.assertRaises(ValueError):
            Evidence("T4", "", "no source")
        with self.assertRaises(ValueError):
            report(benchmark_evidence=None)
        with self.assertRaises(TypeError):
            report(gross_evidence=None)

    def test_invalid_numeric_inputs(self):
        for bad in ("NaN", "Infinity", "-Infinity"):
            with self.assertRaises(ValueError):
                decimal(bad)
        for bad in (0.1, True):
            with self.assertRaises(TypeError):
                decimal(bad)
        with self.assertRaises(ValueError):
            required_return("100", "0")
        with self.assertRaises(ValueError):
            CostLine("infrastructure", "-5", FIXTURE)
        with self.assertRaises(ValueError):
            lending_income_usd("100", "-1", "30", rate_kind="apy")
        with self.assertRaises(ValueError):
            lending_income_usd("100", ".05", "30", rate_kind="unknown")


if __name__ == "__main__":
    unittest.main()
