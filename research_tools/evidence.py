"""Offline evidence manifest checks. Integrity/metadata checks are NOT verification of truth.

No network calls, wallet access, signing, broadcasting, or code execution.
Run from the repository root: python3 -m research_tools.evidence manifest.json --root .
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from enum import Enum
import hashlib
import ipaddress
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import parse_qsl, urlsplit


class EvidenceError(ValueError):
    """Malformed evidence or unavailable provenance; fail closed."""


class Tier(str, Enum):
    T1 = "T1"
    T2 = "T2"
    T3 = "T3"
    T4 = "T4"


class DataKind(str, Enum):
    OBSERVED = "observed_onchain"
    FORK = "historical_fork"
    FORWARD = "forward_paper"
    MODEL = "model"
    SYNTHETIC = "synthetic"


def timestamp(value: Any) -> datetime:
    if not isinstance(value, str):
        raise EvidenceError("timestamp must be an ISO-8601 UTC string")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EvidenceError("invalid timestamp") from exc
    if result.tzinfo is None or result.utcoffset() != timedelta(0):
        raise EvidenceError("timestamps must explicitly use UTC")
    return result


def amount(value: Any, *, nonnegative: bool = False) -> Decimal:
    """Require decimal strings, avoiding binary float and bool coercion."""
    if not isinstance(value, str):
        raise EvidenceError("amounts must be decimal strings, not JSON numbers")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise EvidenceError("invalid decimal amount") from exc
    if not result.is_finite() or (nonnegative and result < 0):
        raise EvidenceError("amount must be finite and satisfy its sign constraint")
    return result


def text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvidenceError(f"{label} must be nonempty text")
    return value


def references(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list) or not value or any(
        not isinstance(item, str) or not item for item in value
    ):
        raise EvidenceError("source_ids must be a nonempty list of identifiers")
    return tuple(value)


def public_url(value: Any) -> str:
    value = text(value, "source URL")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise EvidenceError("source URL must be HTTPS without credentials")
    if parsed.hostname == "localhost" or parsed.hostname.endswith((".local", ".internal")):
        raise EvidenceError("source URL must not name a private service")
    try:
        address = ipaddress.ip_address(parsed.hostname)
    except ValueError:
        address = None
    if address is not None and not address.is_global:
        raise EvidenceError("source URL must not use a private IP address")
    if any(re.search(r"token|secret|password|api.?key|authorization", key, re.I)
           for key, _ in parse_qsl(parsed.query)):
        raise EvidenceError("source URL contains a credential-like query parameter")
    return value


@dataclass(frozen=True)
class Source:
    id: str
    url: str
    retrieved_at: datetime
    artifact_path: str
    sha256: str

    @classmethod
    def parse(cls, row: dict[str, Any]) -> Source:
        source = cls(
            text(row["id"], "source id"), public_url(row["url"]),
            timestamp(row["retrieved_at"]), text(row["artifact_path"], "artifact path"),
            text(row["sha256"], "sha256"),
        )
        if not re.fullmatch(r"[0-9a-f]{64}", source.sha256):
            raise EvidenceError("sha256 must be a lowercase 64-character digest")
        return source


@dataclass(frozen=True)
class Claim:
    id: str
    metric: str
    value: Decimal
    unit: str
    source_ids: tuple[str, ...]

    @classmethod
    def parse(cls, row: dict[str, Any]) -> Claim:
        return cls(text(row["id"], "claim id"), text(row["metric"], "metric"),
                   amount(row["value"]), text(row["unit"], "unit"),
                   references(row["source_ids"]))


@dataclass(frozen=True)
class VolatileWindow:
    start: datetime
    end: datetime
    source_ids: tuple[str, ...]


@dataclass(frozen=True)
class Manifest:
    id: str
    strategy_id: str
    tier: Tier
    data_kind: DataKind
    start: datetime
    end: datetime
    created_at: datetime
    sources: tuple[Source, ...]
    claims: tuple[Claim, ...]
    checks: dict[str, tuple[str, ...]]
    actors: tuple[str, ...]
    volatile_windows: tuple[VolatileWindow, ...]

    @classmethod
    def parse(cls, row: dict[str, Any]) -> Manifest:
        try:
            if not isinstance(row, dict) or not isinstance(row.get("checks", {}), dict):
                raise EvidenceError("manifest and checks must be objects")
            for key in ("sources", "claims", "actors", "volatile_windows"):
                if key in row and not isinstance(row[key], list):
                    raise EvidenceError("manifest collection fields must be lists")
            if type(row["schema_version"]) is not int or row["schema_version"] != 1:
                raise EvidenceError("unsupported schema_version")
            if row.get("paper_only") is not True:
                raise EvidenceError("paper_only must be explicitly true")
            sources = tuple(Source.parse(item) for item in row["sources"])
            claims = tuple(Claim.parse(item) for item in row["claims"])
            checks = {text(k, "check name"): references(v)
                      for k, v in row.get("checks", {}).items()}
            actors = tuple(text(a, "actor") for a in row.get("actors", []))
            windows = tuple(VolatileWindow(timestamp(w["start"]), timestamp(w["end"]),
                                           references(w["source_ids"]))
                            for w in row.get("volatile_windows", []))
            return cls(text(row["id"], "manifest id"), text(row["strategy_id"], "strategy id"),
                       Tier(row["tier"]), DataKind(row["data_kind"]),
                       timestamp(row["start"]), timestamp(row["end"]),
                       timestamp(row["created_at"]), sources, claims, checks, actors, windows)
        except (KeyError, TypeError, ValueError) as exc:
            if isinstance(exc, EvidenceError):
                raise
            # Do not echo untrusted manifest values, which may contain credentials.
            raise EvidenceError("manifest has a missing, invalid, or incorrectly typed field") from exc


REQUIRED_CHECKS: dict[Tier, set[str]] = {
    Tier.T1: {"inventory_reconciliation", "external_cashflows", "actor_attribution",
              "capital_deployed", "prices", "all_costs"},
    Tier.T2: {"fork_state", "execution_replay", "latency", "gas", "failed_transactions",
              "competition", "capital_lockup", "slippage", "prices", "all_costs",
              "inventory_reconciliation", "volatile_window"},
    Tier.T3: {"forward_observation_log", "decision_logic_identity", "simulated_fills",
              "latency", "competition", "prices", "all_costs", "inventory_reconciliation"},
    Tier.T4: set(),
}
MINIMUM_DAYS = {Tier.T1: 14, Tier.T2: 30, Tier.T3: 7, Tier.T4: 0}
EXPECTED_KIND = {Tier.T1: DataKind.OBSERVED, Tier.T2: DataKind.FORK, Tier.T3: DataKind.FORWARD}


def file_digest(root: Path, relative: str) -> str:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise EvidenceError("artifact paths must stay within the evidence root")
    base = root.resolve()
    resolved = (base / path).resolve()
    if not resolved.is_relative_to(base) or not resolved.is_file():
        raise EvidenceError("artifact is missing or escapes evidence root")
    digest = hashlib.sha256()
    with resolved.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate(manifest: Manifest, root: Path, *, now: datetime | None = None) -> dict[str, Any]:
    """Check artifacts and structural gates, never promote tier or issue a recommendation."""
    now = now or datetime.now(timezone.utc)
    errors: list[str] = []
    ids = {source.id for source in manifest.sources}
    if not manifest.sources:
        errors.append("no provenance sources supplied")
    if len(ids) != len(manifest.sources):
        errors.append("duplicate source identifiers")
    if not manifest.claims:
        errors.append("no numeric claims supplied")
    if len({claim.id for claim in manifest.claims}) != len(manifest.claims):
        errors.append("duplicate claim identifiers")
    if manifest.end <= manifest.start:
        errors.append("observation window must have positive duration")
    if manifest.end > now or manifest.created_at > now or manifest.created_at < manifest.end:
        errors.append("future or inconsistent observation/creation timestamps")
    days = Decimal(str((manifest.end - manifest.start).total_seconds())) / Decimal(86400)
    if days < MINIMUM_DAYS[manifest.tier]:
        errors.append(f"{manifest.tier.value} requires at least {MINIMUM_DAYS[manifest.tier]} days")
    if manifest.tier in EXPECTED_KIND and manifest.data_kind != EXPECTED_KIND[manifest.tier]:
        errors.append("data_kind cannot support claimed tier; synthetic/model is never T1/T2/T3")
    missing_checks = REQUIRED_CHECKS[manifest.tier] - manifest.checks.keys()
    if missing_checks:
        errors.append("missing evidence checks: " + ", ".join(sorted(missing_checks)))
    if manifest.tier == Tier.T1 and not manifest.actors:
        errors.append("T1 requires identified public actors")
    if manifest.tier == Tier.T2 and not manifest.volatile_windows:
        errors.append("T2 requires a sourced volatile window")
    all_refs = [claim.source_ids for claim in manifest.claims]
    all_refs += list(manifest.checks.values())
    all_refs += [window.source_ids for window in manifest.volatile_windows]
    if any(ref not in ids for refs in all_refs for ref in refs):
        errors.append("claim/check/window references an unknown source")
    for window in manifest.volatile_windows:
        if not manifest.start <= window.start < window.end <= manifest.end:
            errors.append("volatile window is empty or outside observation coverage")
    for source in manifest.sources:
        if source.retrieved_at > now or source.retrieved_at > manifest.created_at:
            errors.append("source retrieval time is in the future or after manifest creation")
        try:
            if file_digest(root, source.artifact_path) != source.sha256:
                errors.append("source artifact hash mismatch")
        except (EvidenceError, OSError):
            errors.append("source artifact missing, unreadable, or unsafe")
    return {
        "manifest_id": manifest.id, "claimed_tier": manifest.tier.value,
        "data_kind": manifest.data_kind.value, "observed_days": str(days),
        "structural_and_integrity_checks_passed": not errors,
        "ready_for_independent_content_review": not errors and manifest.tier != Tier.T4,
        "recommendation_eligible": False,
        "errors": errors,
        "limits": [
            "Hashes and timestamps establish integrity/metadata consistency, not factual truth.",
            "No independent content review, attribution review, or strategy grading was performed.",
            "T2 requires genuine historical fork executions, not an accounting replay or rate model.",
            "T3 duration must be elapsed live observation, not historical or synthetic timestamps.",
            "A recommendation additionally requires T2+T3, independent judging, and risk gates.",
        ],
    }


def load_json(path: Path) -> Any:
    """Reject duplicate keys and nonstandard NaN/Infinity rather than accepting ambiguous JSON."""
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise EvidenceError("duplicate JSON key")
            result[key] = value
        return result

    def invalid_constant(_: str) -> None:
        raise EvidenceError("non-finite JSON constant")

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique,
                      parse_constant=invalid_constant)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    try:
        result = validate(Manifest.parse(load_json(args.manifest)), args.root)
    except (EvidenceError, OSError, json.JSONDecodeError):
        print(json.dumps({"structural_and_integrity_checks_passed": False,
                          "recommendation_eligible": False,
                          "errors": ["malformed or unreadable manifest; no evidence accepted"]}))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["structural_and_integrity_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
