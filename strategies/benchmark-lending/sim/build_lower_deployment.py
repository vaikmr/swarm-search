#!/usr/bin/env python3
"""Conditional capital/cost stress arithmetic, not a probability or recommendation."""
import datetime as dt
import json
from pathlib import Path

TOTAL = 50000


def stress(principal, monthly_cost_ceiling):
    if not 0 <= principal <= TOTAL or monthly_cost_ceiling < 0:
        raise ValueError("Invalid capital or scenario cost ceiling")
    month = principal + monthly_cost_ceiling
    year = principal + 12 * monthly_cost_ceiling
    return {
        "monthly_full_sleeve_loss_plus_cost_usd": month,
        "annual_one_time_full_sleeve_loss_plus_12_costs_usd": year,
        "monthly_pct_of_initial_total": month / TOTAL * 100,
        "annual_pct_of_initial_total": year / TOTAL * 100,
        "within_monthly_10pct_component_bound": month <= TOTAL * 0.1,
        "within_annual_20pct_component_bound": year <= TOTAL * 0.2,
        "portfolio_tail_probability": None,
    }


def main():
    out = Path("strategies/benchmark-lending/evidence")
    summary = json.loads((out / "rate-summary.json").read_text())
    market = next(r for r in summary["data"] if r["label"] == "aave-ethereum-usdc")
    cases = []
    for principal in (0, 4000, 4500, 5000, 10000, 15000):
        gross = {}
        for days in (30, 90):
            window = market["windows"][str(days)]
            if window["base"]["coverage_fraction"] < 0.999999:
                raise ValueError("Incomplete historical rate coverage")
            gross[str(days)] = window["base"]["gross_usd_on_50000"] * principal / TOTAL
        cases.append({
            "principal_usd": principal, "offchain_cash_before_costs_usd": TOTAL - principal,
            "protocol_chain_coin_exposure_pct": principal / TOTAL * 100,
            "gross_history_usd": gross, "actual_net_usd": None,
            "scenario_monthly_aggregate_cost_ceiling_usd": 500,
            "component_stress": stress(principal, 500),
            "cash_counterparty_slots_needed_at_15000_maximum": (TOTAL - principal + 14999) // 15000,
        })
    result = {
        "built_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": "CONDITIONAL_SINGLE_CHAIN_STRESS_NOT_A_CERTIFIED_COMPLIANT_BASELINE",
        "tier": "T4 rate arithmetic and hypothetical component loss budgets",
        "market": {"label": market["label"], "pool": market["pool"], "source": market["source"],
                   "current": market["current"], "windows": {
                       k: {"start": v["start"], "end": v["end"]} for k, v in market["windows"].items()}},
        "cases": cases,
        "conditions": [
            "All costs combined, not only infrastructure, stay within assumed $500/month; no actual costs observed",
            "Principal is never replenished after a loss; no borrowing, leverage or unlimited external liability",
            "Cash income is explicitly zero in these scenarios; cash custody/FX/access losses are not included",
            "Cash counterparties are hypothetical independent slots, not existing or verified user accounts",
            "All Ethereum-dependent positions would share one aggregate budget; this model uses only Ethereum L1",
            "Capital loss and costs bound only the modeled sleeve, not path-dependent portfolio drawdown",
            "No 99% drawdown probability, annual tail probability, T1/T2/T3 or exact audit-build coverage established",
            "No spending, transfer, account-opening or deployment authorization",
        ],
        "unknowns": {"cash_risk": None, "cash_access": None, "actual_costs": None,
                     "exact_audit_build_linkage": None, "portfolio_99pct_drawdown": None},
    }
    (out / "lower-deployment-sensitivity.json").write_text(json.dumps(result, indent=2) + "\n")
    for c in cases:
        print(c["principal_usd"], "gross30d", c["gross_history_usd"]["30"],
              "gross90d", c["gross_history_usd"]["90"], "stress", c["component_stress"])


if __name__ == "__main__":
    main()
