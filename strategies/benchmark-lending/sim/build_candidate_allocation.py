#!/usr/bin/env python3
"""Nominal-cap candidate, not a certified feasible or risk-approved portfolio."""
import datetime as dt
import json
from pathlib import Path
from fetch_public_rates import integrate, stamp


SLOTS = [
    ("aave-ethereum-dai", "Aave", "Ethereum", "DAI", 15000),
    ("compound-arbitrum-usdt", "Compound", "Arbitrum", "USDT", 15000),
    ("morpho-base-sparkusdc", "Morpho", "Base", "USDC", 15000),
]


def main():
    out = Path("strategies/benchmark-lending/evidence")
    summary = json.loads((out / "rate-summary.json").read_text())
    lookup = {r["label"]: r for r in summary["data"]}
    end = min(stamp(lookup[s[0]]["latest_data_timestamp"]) for s in SLOTS)
    windows = {}
    for days in (30, 90):
        positions = []
        for label, protocol, chain, asset, capital in SLOTS:
            rows = json.loads((out / (label + "-history.json")).read_text())["data"]
            result = integrate(rows, end - dt.timedelta(days=days), end, "apyBase")
            if result["coverage_fraction"] < 0.999999:
                raise ValueError("Incomplete rate coverage")
            result["position_gross_usd"] = result["gross_usd_on_50000"] * capital / 50000
            positions.append({"label": label, "protocol": protocol, "chain": chain, "asset": asset, "capital_usd": capital, "source": lookup[label]["source"], "math": result})
        gross = sum(p["math"]["position_gross_usd"] for p in positions)
        windows[str(days)] = {"start": (end - dt.timedelta(days=days)).isoformat(), "end": end.isoformat(), "positions": positions, "cash_usd": 5000, "cash_income_scenario_usd": 0, "cash_income_basis": "explicit zero-yield cash scenario, not observed yield", "gross_usd": gross, "gross_return_pct_on_total_capital": gross / 50000 * 100, "net_usd": None, "benchmark_excess_usd": None}
    current_30d = sum(capital * ((1 + lookup[label]["current"]["apyBase"] / 100) ** (30 / 365) - 1) for label, _, _, _, capital in SLOTS)
    result = {
        "built_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "tier": "T4 historical APY arithmetic",
        "status": "NOMINAL_CAPS_ONLY_NOT_A_COMPLIANT_OR_RECOMMENDED_ALLOCATION",
        "total_capital_usd": 50000,
        "positions": [{"pool": lookup[label]["pool"], "label": label, "protocol": protocol, "chain": chain, "asset": asset, "capital_usd": capital} for label, protocol, chain, asset, capital in SLOTS],
        "nominal_caps": {"protocol_pct": 30, "chain_pct": 30, "stablecoin_pct": 30, "offchain_cash_pct": 10},
        "lookthrough_unknowns": [
            "DAI issuer/reserve exposures may overlap USDC and other backing; no verified backing matrix in this package",
            "Ethereum common settlement and bridge dependencies of Arbitrum/Base are not independent tail domains",
            "Morpho SparkUSDC exact deployed version, vault creation date, oracle/collateral/curator allocations and audit linkage unverified",
            "Initial/final gas, bridging, reward-realization and infrastructure costs unknown, not zero",
            "Protocol-wide TVL/audits do not establish specific market eligibility or cash availability",
        ],
        "current_rate_30d_gross_usd_scenario": current_30d,
        "current_rate_scenario_warning": "Assumes current base APYs persist for 30d, cash earns zero, and costs excluded; not forecast",
        "windows": windows,
        "cost_status": {"entry_exit_gas_usd": None, "bridge_usd": None, "execution_slippage_usd": None, "infra_usd": None, "stablecoin_mtm_usd": None, "default_loss_usd": None},
    }
    (out / "candidate-allocation.json").write_text(json.dumps(result, indent=2) + "\n")
    print("Current rate 30d gross scenario", current_30d)
    print("History", {days: window["gross_usd"] for days, window in windows.items()})


if __name__ == "__main__":
    main()
