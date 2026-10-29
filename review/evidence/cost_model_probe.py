"""Independent synthetic reviewer probes, not market or strategy-return evidence.

Run from the repository root:
    python3 review/evidence/cost_model_probe.py

The assertions capture behavior at reviewed revision 43cda27. The fixture probes
are not strategy construction, and reproducing a reporting issue is not an
economic result. They may intentionally need revision after owner fixes.
"""

import json
import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from research_tools.costs import (  # noqa: E402
    COST_CATEGORIES,
    CostLine,
    Evidence,
    equity_pnl_usd,
    lending_income_usd,
    net_pnl,
)


FIXTURE = Evidence(
    "T4",
    "review/evidence/cost_model_probe.py",
    "Synthetic independent reviewer fixture; not a market observation",
)


def probe(gross="0", idle="0", benchmark="0", overrides=None):
    costs = [
        CostLine(category, (overrides or {}).get(category, "0"), FIXTURE)
        for category in COST_CATEGORIES
    ]
    return net_pnl(
        total_capital_usd="50000",
        gross_strategy_pnl_usd=gross,
        gross_evidence=FIXTURE,
        idle_yield_usd=idle,
        idle_evidence=FIXTURE,
        costs=costs,
        benchmark_net_usd=benchmark,
        benchmark_evidence=FIXTURE if benchmark is not None else None,
    )


def main():
    marked_only = probe(gross="123")
    assert marked_only.net_cash_pnl_usd == Decimal("123")

    signed_idle = lending_income_usd("1000", "-.01", "30", rate_kind="apr")
    try:
        probe(idle=signed_idle)
    except ValueError as exc:
        signed_idle_error = str(exc)
    else:
        raise AssertionError("Reviewed signed-idle rejection no longer reproduced")

    whole_equity = equity_pnl_usd("50000", "50100", "0", "0")
    duplicate_idle = probe(gross=whole_equity, idle="100")
    separate_idle = probe(gross="0", idle="100")
    assert duplicate_idle.net_cash_pnl_usd == 200
    assert separate_idle.net_cash_pnl_usd == 100

    missing = probe(overrides={"bridge_rebalance": None})
    assert missing.net_cash_pnl_usd is None
    assert probe(gross="-100").net_cash_pnl_usd == -100
    b1, b2 = probe(gross="100", benchmark="10"), probe(gross="100", benchmark="20")
    assert b1.net_cash_pnl_usd == b2.net_cash_pnl_usd
    assert b1.excess_over_benchmark_usd != b2.excess_over_benchmark_usd
    no_benchmark = probe(gross="100", benchmark=None)
    assert no_benchmark.net_cash_pnl_usd == 100
    assert no_benchmark.excess_over_benchmark_usd is None

    print(json.dumps({
        "evidence_tier": "T4",
        "synthetic": True,
        "not_strategy_return_evidence": True,
        "reviewed_revision": "43cda27e6e4a9d8fe828e75edcb1c244b7f78739",
        "marked_only": {
            "unrealized_gain_usd": "123",
            "stipulated_cash_receipts_usd": "0",
            "reported_net_cash_pnl_usd": str(marked_only.net_cash_pnl_usd),
        },
        "negative_idle": {
            "lending_helper_output_usd": str(signed_idle),
            "net_pnl_rejection": signed_idle_error,
        },
        "caller_boundary_misuse_not_current_adapter_evidence": {
            "whole_equity_pnl_usd": str(whole_equity),
            "same_idle_added_twice_report_usd": str(duplicate_idle.net_cash_pnl_usd),
            "correct_separate_boundary_report_usd": str(separate_idle.net_cash_pnl_usd),
        },
        "known_checks": {
            "unknown_cost_suppresses_net": True,
            "gross_loss_preserved": True,
            "benchmark_separate_from_net": True,
            "missing_benchmark_does_not_hide_known_net": True,
        },
    }, indent=2))


if __name__ == "__main__":
    main()
