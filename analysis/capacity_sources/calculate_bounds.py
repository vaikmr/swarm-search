"""Deterministic T4 feasibility bounds, not market simulation.

Run from any directory; output is JSON to stdout. No network or transaction code.
"""

from __future__ import annotations

import json
import math


CAPITAL_USD = 50_000.0
DOMAIN_CAP = 0.30
MAX_CHAINS = 3
DAYS = 30
HOURS = DAYS * 24
INFRA_CEILING_USD = 500.0


def nonnegative(value: float, name: str) -> float:
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


def deployment_bound(capital: float, fraction: float, chains: int) -> dict:
    nonnegative(capital, "capital")
    nonnegative(fraction, "fraction")
    if fraction > 1 or type(chains) is not int or chains < 0:
        raise ValueError("fraction must be <=1; chains must be a nonnegative integer")
    deployed = min(capital, capital * fraction * chains)
    return {
        "capital_usd": capital,
        "per_domain_cap_usd": capital * fraction,
        "onchain_upper_bound_usd": deployed,
        "offchain_or_unallocated_lower_bound_usd": capital - deployed,
    }


def required_turnover(target_net: float, fixed_cost: float, net_margin_bps: float) -> float:
    """Margin is AFTER all variable costs, BEFORE separately passed fixed cost."""
    nonnegative(target_net, "target_net")
    nonnegative(fixed_cost, "fixed_cost")
    nonnegative(net_margin_bps, "net_margin_bps")
    if net_margin_bps == 0:
        raise ValueError("positive net variable margin required")
    return (target_net + fixed_cost) / (net_margin_bps / 10_000)


def ideal_lock_turnover(capital: float, lock_hours: float, hours: float = HOURS) -> float:
    """Fluid ideal, 100% utilization, unlimited flow, no competition. Not a forecast."""
    nonnegative(capital, "capital")
    nonnegative(lock_hours, "lock_hours")
    nonnegative(hours, "hours")
    if lock_hours == 0:
        raise ValueError("positive lock_hours required")
    return capital * hours / lock_hours


def workload_cost(chains: int, calls_per_second_per_chain: float, cu_per_call: float) -> dict:
    """Hypothetical workload, published Alchemy PAYG compute price only."""
    if type(chains) is not int or chains < 0:
        raise ValueError("chains must be a nonnegative integer")
    nonnegative(calls_per_second_per_chain, "calls_per_second_per_chain")
    nonnegative(cu_per_call, "cu_per_call")
    calls = chains * calls_per_second_per_chain * DAYS * 24 * 3600
    cu = calls * cu_per_call
    return {
        "chains": chains,
        "calls_per_second_per_chain": calls_per_second_per_chain,
        "hypothetical_cu_per_call": cu_per_call,
        "calls_per_month": calls,
        "cu_per_month": cu,
        "payg_compute_only_usd": cu / 1_000_000 * 0.52,
    }


def paired_notional_bound(equity: float, leverage: float, perp_collateral_cap: float) -> float:
    """Fully paid spot N plus perp margin N/L. Ignores further risk constraints."""
    nonnegative(equity, "equity")
    nonnegative(leverage, "leverage")
    nonnegative(perp_collateral_cap, "perp_collateral_cap")
    if leverage == 0 or leverage > 2:
        raise ValueError("leverage must be positive and <=2")
    return min(equity / (1 + 1 / leverage), perp_collateral_cap * leverage)


def build_output() -> dict:
    deployment = deployment_bound(CAPITAL_USD, DOMAIN_CAP, MAX_CHAINS)
    notional = paired_notional_bound(
        deployment["onchain_upper_bound_usd"], 2, deployment["per_domain_cap_usd"]
    )
    return {
        "evidence_tier": "T4 deterministic requirement arithmetic and hypothetical sensitivities",
        "not_performance": True,
        "as_of_date_utc": "2026-10-29",
        "month_days": DAYS,
        "deployment": deployment,
        "target_requirements": [
            {
                "net_target_usd": target,
                "net_target_fraction_total_capital": target / CAPITAL_USD,
                "required_before_variable_costs_at_full_infra_budget_usd": target + INFRA_CEILING_USD,
                "required_fraction_of_max_onchain_capital_before_variable_costs":
                    (target + INFRA_CEILING_USD) / deployment["onchain_upper_bound_usd"],
            }
            for target in (2000, 5000)
        ],
        "turnover_requirements": [
            {
                "net_target_usd": target,
                "fixed_cost_usd": INFRA_CEILING_USD,
                "hypothetical_after_variable_cost_margin_bps": margin,
                "required_notional_turnover_usd": required_turnover(
                    target, INFRA_CEILING_USD, margin
                ),
            }
            for margin in (1, 2, 5, 10)
            for target in (2000, 5000)
        ],
        "single_domain_lock_upper_bounds": [
            {
                "hypothetical_lock_hours": lock,
                "at_risk_capital_usd": 15000,
                "ideal_fluid_turnover_usd": ideal_lock_turnover(15000, lock),
                "limitations": "No guarantee of opportunity, eligibility, timing, utilization or profit",
            }
            for lock in (1, 6, 24)
        ],
        "funding_requirement": {
            "leverage": 2,
            "max_perp_collateral_usd": 15000,
            "paired_notional_upper_bound_usd": notional,
            "limitations": "Conditional algebraic bound, not a proven feasible allocation or actual funding rate",
            "required_monthly_funding_fraction_before_trade_hedge_costs": [
                {
                    "net_target_usd": target,
                    "fixed_infrastructure_cost_usd": INFRA_CEILING_USD,
                    "required_fraction": (target + INFRA_CEILING_USD) / notional,
                }
                for target in (2000, 5000)
            ],
        },
        "rpc_sensitivities": [
            workload_cost(3, 1, weight) for weight in (10, 100)
        ],
        "source_ids": {
            "constraints": "docs/CHARTER.md; user-specified constraints",
            "rpc_price": "ALCHEMY_PRICE in sources.json",
            "other_inputs": "Explicit hypothetical sensitivity choices, not observed measurements",
        },
    }


if __name__ == "__main__":
    print(json.dumps(build_output(), indent=2, allow_nan=False))
