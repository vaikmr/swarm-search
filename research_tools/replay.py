"""PAPER-ONLY CLOSED-POSITION accounting; NOT full-portfolio coverage or T2 evidence.

Consumes locally supplied precomputed opportunity/mark records. Never fetches RPC
state, signs, sends, deploys, or executes transactions. Every output is T4, including
when input is historical. Real execution, costs and race evidence need adapters and
independent verification. Synthetic fixtures prove code behavior, not returns.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_CEILING
import json
from pathlib import Path
from typing import Any

from .evidence import EvidenceError, amount, load_json, references, text, timestamp


D = Decimal
ZERO = D("0")
DAY = timedelta(days=1)
MONTH = timedelta(days=30)
SECONDS_30D = D("2592000")
COST_KEYS = {"gas_all_in", "protocol", "bridge", "slippage", "cex", "hedge", "borrow", "other"}


@dataclass(frozen=True)
class Costs:
    """USD expenses, excluded from supplied gross PnL; explicit zeroes, no unknown defaults."""
    values: dict[str, Decimal]

    @classmethod
    def parse(cls, row: dict[str, Any]) -> Costs:
        if not isinstance(row, dict) or set(row) != COST_KEYS:
            raise EvidenceError("all eight cost fields are required; unknown is not zero")
        return cls({key: amount(value, nonnegative=True) for key, value in row.items()})

    def total(self, gas_multiplier: Decimal) -> Decimal:
        return sum((value * gas_multiplier if key == "gas_all_in" else value
                    for key, value in self.values.items()), ZERO)


@dataclass(frozen=True)
class Mark:
    at: datetime
    cumulative_gross_pnl_usd: Decimal


@dataclass(frozen=True)
class Opportunity:
    id: str
    decision_at: datetime
    settlement_at: datetime
    latest_fill_at: datetime
    competitor_arrival_at: datetime | None
    measured_latency_ms: int
    capital_usd: Decimal
    gross_pnl_usd: Decimal
    success_costs: Costs
    failed_costs: Costs
    attempt_on_loss: bool
    race_proven: bool
    marks: tuple[Mark, ...]
    source_ids: tuple[str, ...]

    @classmethod
    def parse(cls, row: dict[str, Any]) -> Opportunity:
        if any(type(row[key]) is not bool for key in ("attempt_on_loss", "race_proven")):
            raise EvidenceError("attempt_on_loss and race_proven must be explicit booleans")
        latency = row["measured_latency_ms"]
        if type(latency) is not int or latency < 0:
            raise EvidenceError("latency must be measured nonnegative integer milliseconds")
        marks = tuple(Mark(timestamp(m["at"]), amount(m["cumulative_gross_pnl_usd"]))
                      for m in row["marks"])
        item = cls(
            text(row["id"], "opportunity id"), timestamp(row["decision_at"]),
            timestamp(row["settlement_at"]), timestamp(row["latest_fill_at"]),
            timestamp(row["competitor_arrival_at"]) if row["competitor_arrival_at"] else None,
            latency, amount(row["capital_usd"], nonnegative=True), amount(row["gross_pnl_usd"]),
            Costs.parse(row["success_costs"]), Costs.parse(row["failed_costs"]),
            row["attempt_on_loss"], row["race_proven"], marks, references(row["source_ids"]),
        )
        if item.capital_usd <= 0:
            raise EvidenceError("capital_usd must be positive")
        if not item.decision_at < item.settlement_at or item.latest_fill_at > item.settlement_at:
            raise EvidenceError("invalid opportunity lifetime")
        if item.latest_fill_at < item.decision_at:
            raise EvidenceError("deadline precedes decision")
        if not marks or marks[-1].at != item.settlement_at:
            raise EvidenceError("marks must include a terminal settlement mark")
        if marks[-1].cumulative_gross_pnl_usd != item.gross_pnl_usd:
            raise EvidenceError("terminal mark must reconcile to gross PnL")
        previous = item.decision_at
        for mark in marks:
            if not previous < mark.at <= item.settlement_at:
                raise EvidenceError("marks must be strictly increasing inside opportunity lifetime")
            previous = mark.at
        return item


@dataclass(frozen=True)
class Scenario:
    name: str
    added_latency_ms: int = 0
    gas_multiplier: Decimal = D("1")
    incumbent_capture_multiplier: Decimal = D("1")


SCENARIOS = (
    Scenario("base"),
    Scenario("latency_plus_50ms", added_latency_ms=50),
    Scenario("latency_plus_200ms", added_latency_ms=200),
    Scenario("gas_2x", gas_multiplier=D("2")),
    Scenario("incumbent_capture_plus_20pct_relative", incumbent_capture_multiplier=D("1.2")),
    Scenario("combined", added_latency_ms=200, gas_multiplier=D("2"),
             incumbent_capture_multiplier=D("1.2")),
)


@dataclass(frozen=True)
class ReplayInput:
    start: datetime
    end: datetime
    initial_capital_usd: Decimal
    infrastructure_per_30d_usd: Decimal
    benchmark_period_net_usd: Decimal | None
    data_kind: str
    opportunities: tuple[Opportunity, ...]
    source_ids: tuple[str, ...]
    inventory_marks_complete: bool

    @classmethod
    def parse(cls, row: dict[str, Any]) -> ReplayInput:
        try:
            if row["paper_only"] is not True or type(row["schema_version"]) is not int or row["schema_version"] != 1:
                raise EvidenceError("paper_only=true and schema_version=1 required")
            if row["data_kind"] not in {"synthetic", "historical_precomputed"}:
                raise EvidenceError("data_kind must explicitly identify synthetic/precomputed data")
            if row["gross_excludes_all_costs_and_external_flows"] is not True:
                raise EvidenceError("gross/cost convention must be explicitly acknowledged")
            if row["gas_all_in_includes_base_priority_l1_operator"] is not True:
                raise EvidenceError("gas must be all-in, with no double-counted fee components")
            if type(row["inventory_marks_complete"]) is not bool:
                raise EvidenceError("inventory_marks_complete must be boolean")
            value = cls(timestamp(row["start"]), timestamp(row["end"]),
                        amount(row["initial_capital_usd"], nonnegative=True),
                        amount(row["infrastructure_per_30d_usd"], nonnegative=True),
                        amount(row["benchmark_period_net_usd"])
                        if row["benchmark_period_net_usd"] is not None else None,
                        row["data_kind"],
                        tuple(Opportunity.parse(item) for item in row["opportunities"]),
                        references(row["source_ids"]), row["inventory_marks_complete"])
            if value.initial_capital_usd <= 0 or value.end <= value.start:
                raise EvidenceError("positive capital and period duration required")
            ids = [item.id for item in value.opportunities]
            if len(ids) != len(set(ids)):
                raise EvidenceError("duplicate opportunity identifier")
            for item in value.opportunities:
                if not value.start <= item.decision_at < item.settlement_at <= value.end:
                    raise EvidenceError("closed_positions_only: all opportunities must settle inside the supplied period")
                if not set(item.source_ids) <= set(value.source_ids):
                    raise EvidenceError("opportunity references an unknown source")
            return value
        except (KeyError, TypeError, ValueError) as exc:
            if isinstance(exc, EvidenceError):
                raise
            raise EvidenceError("replay input has a missing or invalid field") from exc


def race(item: Opportunity, scenario: Scenario) -> tuple[bool, str, Decimal]:
    arrival = item.decision_at + timedelta(
        milliseconds=item.measured_latency_ms + scenario.added_latency_ms)
    if not item.race_proven or item.competitor_arrival_at is None:
        return False, "unproven_race", ZERO
    if arrival > item.latest_fill_at:
        return False, "stale", ZERO
    if item.marks[0].at < arrival:
        return False, "unusable_mark_path", ZERO
    margin_ms = D(str((item.competitor_arrival_at - arrival).total_seconds())) * D(1000)
    if arrival >= item.competitor_arrival_at:
        return False, "lost_or_tied_race", margin_ms
    return True, "proven_race_win", margin_ms


def quantile(values: list[Decimal], fraction: Decimal) -> Decimal | None:
    """Descriptive linear empirical quantile, NOT a population confidence bound."""
    if not values:
        return None
    ordered = sorted(values)
    point = (len(values) - 1) * fraction
    index = int(point)
    remainder = point - index
    if index + 1 == len(ordered):
        return ordered[index]
    return ordered[index] + remainder * (ordered[index + 1] - ordered[index])


def run_replay(data: ReplayInput, scenario: Scenario) -> dict[str, Any]:
    if (type(scenario.added_latency_ms) is not int or scenario.added_latency_ms < 0
            or not scenario.gas_multiplier.is_finite() or scenario.gas_multiplier < 1):
        raise EvidenceError("stress scenarios cannot improve latency or gas")
    if not scenario.incumbent_capture_multiplier.is_finite() or scenario.incumbent_capture_multiplier < 1:
        raise EvidenceError("incumbent stress must be finite and >=1")
    opportunities = sorted(data.opportunities, key=lambda item: (item.decision_at, item.id))
    race_results = {item.id: race(item, scenario) for item in opportunities}
    proven_competitor_wins = sum(
        result[1] == "lost_or_tied_race" for result in race_results.values())
    possible_wins = sorted((item for item in opportunities if race_results[item.id][0]),
                           key=lambda item: (race_results[item.id][2], item.id))
    # Scenario convention, not a capture prediction: increase observed incumbent win
    # COUNT by 20% relative, round conservatively up, take closest-margin entrant wins.
    target = int((D(proven_competitor_wins) * scenario.incumbent_capture_multiplier)
                 .to_integral_value(rounding=ROUND_CEILING))
    stress_takeovers = {item.id for item in possible_wins[:max(0, target - proven_competitor_wins)]}
    active: list[tuple[datetime, Decimal]] = []
    pnl_deltas: dict[datetime, Decimal] = defaultdict(lambda: ZERO)
    locked_seconds_usd = ZERO
    gross = ZERO
    costs = ZERO
    failed_costs = ZERO
    decisions: list[dict[str, Any]] = []
    counters: Counter[str] = Counter()
    for item in opportunities:
        active = [(until, capital) for until, capital in active if until > item.decision_at]
        locked = sum((capital for _, capital in active), ZERO)
        equity_now = data.initial_capital_usd + sum(
            (delta for at, delta in pnl_deltas.items() if at <= item.decision_at), ZERO)
        equity_now -= data.infrastructure_per_30d_usd * D(str(
            (item.decision_at - data.start).total_seconds())) / SECONDS_30D
        available = max(ZERO, min(data.initial_capital_usd, equity_now)) - locked
        required = item.capital_usd + max(item.success_costs.total(scenario.gas_multiplier),
                                        item.failed_costs.total(scenario.gas_multiplier))
        if required > available:
            counters["insufficient_capital"] += 1
            decisions.append({"id": item.id, "outcome": "insufficient_capital"})
            continue
        wins, reason, _ = race_results[item.id]
        if item.id in stress_takeovers:
            wins, reason = False, "incumbent_capture_stress"
        if not wins:
            counters[reason] += 1
            cost = item.failed_costs.total(scenario.gas_multiplier) if item.attempt_on_loss else ZERO
            costs += cost
            failed_costs += cost
            pnl_deltas[item.decision_at] -= cost
            decisions.append({"id": item.id, "outcome": reason, "net_pnl_usd": str(-cost)})
            continue
        cost = item.success_costs.total(scenario.gas_multiplier)
        pnl_deltas[item.decision_at] -= cost
        costs += cost
        gross += item.gross_pnl_usd
        active.append((item.settlement_at, item.capital_usd))
        locked_seconds_usd += item.capital_usd * D(str(
            (item.settlement_at - item.decision_at).total_seconds()))
        previous_mark = ZERO
        for mark in item.marks:
            pnl_deltas[mark.at] += mark.cumulative_gross_pnl_usd - previous_mark
            previous_mark = mark.cumulative_gross_pnl_usd
        counters["filled"] += 1
        if item.gross_pnl_usd - cost > 0:
            counters["profitable_fill"] += 1
        decisions.append({"id": item.id, "outcome": "filled",
                          "net_pnl_usd": str(item.gross_pnl_usd - cost)})
    duration_s = D(str((data.end - data.start).total_seconds()))
    infrastructure = data.infrastructure_per_30d_usd * duration_s / SECONDS_30D
    net = gross - costs - infrastructure
    # Include daily boundaries, all position marks, and observation end. Infrastructure
    # accrues continuously; marking/decisions at a boundary are included as of that time.
    points = {data.start, data.end, *pnl_deltas}
    at = data.start + DAY
    while at < data.end:
        points.add(at)
        at += DAY
    cumulative = ZERO
    curve: list[tuple[datetime, Decimal]] = []
    for at in sorted(points):
        cumulative += pnl_deltas.get(at, ZERO)
        accrued = data.infrastructure_per_30d_usd * D(str(
            (at - data.start).total_seconds())) / SECONDS_30D
        curve.append((at, data.initial_capital_usd + cumulative - accrued))
    peak = data.initial_capital_usd
    drawdown = ZERO
    drawdown_fraction = ZERO
    for _, equity in curve:
        peak = max(peak, equity)
        drawdown = max(drawdown, peak - equity)
        drawdown_fraction = max(drawdown_fraction, (peak - equity) / peak)
    rolling_30d: list[Decimal] = []
    endpoint = data.start + MONTH
    while endpoint <= data.end:
        # Pre-start boundary excludes costs incurred exactly at observation start.
        def equity_at(moment: datetime, *, before_initial: bool = False) -> Decimal:
            if before_initial and moment == data.start:
                return data.initial_capital_usd
            equity = data.initial_capital_usd
            for time, value in curve:
                if time > moment:
                    break
                equity = value
            return equity
        rolling_30d.append(equity_at(endpoint) - equity_at(endpoint - MONTH, before_initial=True))
        endpoint += DAY
    filled = counters["filled"]
    mark_quality = data.inventory_marks_complete
    return {
        "scenario": scenario.name, "paper_only": True, "evidence_tier": "T4",
        "data_kind": data.data_kind, "is_t2_evidence": False,
        "scope": "closed_positions_only",
        "portfolio_coverage_complete": False,
        "monthly_portfolio_pnl_validated": False,
        "recommendation_eligible": False,
        "gross_pnl_usd": str(gross), "variable_cost_usd": str(costs),
        "failed_attempt_cost_usd": str(failed_costs),
        "infrastructure_cost_usd": str(infrastructure), "net_economic_pnl_usd": str(net),
        "realized_cash_pnl_usd": None,
        "benchmark_excess_usd": str(net - data.benchmark_period_net_usd)
        if data.benchmark_period_net_usd is not None else None,
        "terminal_equity_usd": str(data.initial_capital_usd + net),
        "marked_max_drawdown_usd": str(drawdown) if mark_quality else None,
        "marked_max_drawdown_fraction": str(drawdown_fraction) if mark_quality else None,
        "drawdown_is_lower_bound_unless_marks_complete": not mark_quality,
        "capital_utilization_fraction": str(locked_seconds_usd / (data.initial_capital_usd * duration_s)),
        "profitable_fill_fraction": str(D(counters["profitable_fill"]) / filled) if filled else None,
        "capture_fraction": str(D(filled) / len(opportunities)) if opportunities else None,
        "outcome_counts": dict(counters),
        "closed_position_rolling_30d_economic_pnl_usd": {
            "window_count": len(rolling_30d), "overlapping_windows": True,
            **{name: str(quantile(rolling_30d, D(fraction))) if rolling_30d else None
               for name, fraction in (("p5", ".05"), ("p50", ".5"), ("p95", ".95"))},
        },
        "input_window_days": str(duration_s / D(86400)),
        "decisions": decisions,
        "equity_curve": [{"at": at.isoformat(), "equity_usd": str(value)} for at, value in curve],
        "limits": [
            "Accounting scaffolding is T4, not a stateful EVM fork, a fill simulator, or T2.",
            "No latency-adjusted repricing/slippage model; stale quoted economics may not fill.",
            "Race proof and complete marks are adapter assertions, not independently verified.",
            "Marked/accrued economics are not proof of received cash; realized cash PnL is unknown.",
            "Unknown races and ties lose; hypothetical failed attempts incur supplied failed costs.",
            "Profits do not compound; prior marked losses/fees reduce available capital. No margin-call model.",
            "Capital locks reserve principal from decision to settlement, conservatively.",
            "Same-time events use identifier order; strategy-specific opportunity selection is absent.",
            "Closed-position-only accounting rejects pending positions; full portfolio coverage is unestablished.",
            "Filtering pending positions can censor losses/locks; these outputs cannot validate monthly portfolio PnL or risk.",
            "Future carryover adapters must mark receivables/collateral at cutoff without later settlement lookahead.",
            "Monthly samples overlap and empirical percentiles do not certify a 99% tail limit.",
            "Capture stress is relative incumbent win-count uplift, rounding up, not probability.",
            "Zero incumbent wins gives zero relative uplift; use absolute takeover stress separately.",
            "No chain/protocol/stablecoin/bridge exposure or protocol-eligibility gate implemented.",
            "Tax treatment excluded; obtain jurisdiction-specific advice before deployment.",
        ],
    }


def sensitivity_matrix(data: ReplayInput) -> list[dict[str, Any]]:
    return [run_replay(data, scenario) for scenario in SCENARIOS]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        result = sensitivity_matrix(ReplayInput.parse(load_json(args.input)))
    except (EvidenceError, OSError, json.JSONDecodeError):
        print(json.dumps({"paper_only": True, "is_t2_evidence": False,
                          "error": "malformed or unreadable replay input; no output accepted"}))
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
