#!/usr/bin/env python3
"""Validate the founding seven-problem architecture and migration references."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

YAML_ROOTS = (
    ROOT / "governance",
    ROOT / "problems",
    ROOT / "protocols",
    ROOT / "migrations" / "foundational-problems-v2",
    ROOT / "studies" / "studies-in-platonic-political-philosophy",
)

REQUIRED_PROTOCOLS = {
    "source-status",
    "evidence-classification",
    "inference-discipline",
    "uncertainty-preservation",
    "speech-and-deed",
    "irony",
    "comedy",
    "claimant-to-wisdom",
    "audience-and-rhetoric",
}


def load_yaml(path: Path, errors: list[str]) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except Exception as exc:  # pragma: no cover - diagnostic path
        errors.append(f"YAML parse failure: {path.relative_to(ROOT)}: {exc}")
        return None


def check_path(value: str, context: str, errors: list[str]) -> None:
    candidate = ROOT / value
    if not candidate.exists():
        errors.append(f"Missing path ({context}): {value}")


def iter_yaml_files() -> list[Path]:
    files: list[Path] = []
    for root in YAML_ROOTS:
        if root.exists():
            files.extend(path for path in root.rglob("*.yaml") if path.is_file())
    return sorted(set(files))


def validate_all_yaml(errors: list[str]) -> int:
    files = iter_yaml_files()
    for path in files:
        load_yaml(path, errors)
    return len(files)


def validate_registry(errors: list[str]) -> None:
    registry_path = ROOT / "problems" / "registry.yaml"
    registry = load_yaml(registry_path, errors)
    if not isinstance(registry, dict):
        return

    problems = registry.get("canonical_problems")
    if not isinstance(problems, list):
        errors.append("problems/registry.yaml: canonical_problems must be a list")
        return

    if len(problems) != 7:
        errors.append(f"Expected 7 canonical problems, found {len(problems)}")

    keys: list[str] = []
    orders: list[int] = []

    for entry in problems:
        if not isinstance(entry, dict):
            errors.append("Registry problem entry is not a mapping")
            continue

        key = entry.get("canonical_key")
        order = entry.get("canonical_order")
        successor_path = entry.get("successor_path")

        if not isinstance(key, str):
            errors.append("Registry problem missing canonical_key")
            continue
        if not isinstance(order, int):
            errors.append(f"Registry problem {key} missing integer canonical_order")
            continue
        if not isinstance(successor_path, str):
            errors.append(f"Registry problem {key} missing successor_path")
            continue

        keys.append(key)
        orders.append(order)
        check_path(successor_path, f"successor for {key}", errors)

        successor = load_yaml(ROOT / successor_path, errors)
        if not isinstance(successor, dict):
            continue
        identity = successor.get("identity", {})
        if identity.get("canonical_key") != key:
            errors.append(
                f"Canonical key mismatch: registry {key}, successor "
                f"{identity.get('canonical_key')} at {successor_path}"
            )
        if identity.get("canonical_order") != order:
            errors.append(
                f"Canonical order mismatch for {key}: registry {order}, successor "
                f"{identity.get('canonical_order')}"
            )

        status = successor.get("status", {})
        if status.get("certification") == "CERTIFIED":
            errors.append(f"Unauthorized certification found in {successor_path}")
        if status.get("activation") in {"ACTIVE", "ACTIVATED"}:
            errors.append(f"Unauthorized activation found in {successor_path}")

        subordinate = entry.get("subordinate_records", {})
        if isinstance(subordinate, dict):
            for field, value in subordinate.items():
                if field == "remaining_required":
                    continue
                if isinstance(value, str):
                    check_path(value, f"registry subordinate {key}.{field}", errors)

    if len(set(keys)) != len(keys):
        errors.append("Duplicate canonical_key in problems/registry.yaml")
    if len(set(orders)) != len(orders):
        errors.append("Duplicate canonical_order in problems/registry.yaml")
    if sorted(orders) != list(range(1, 8)):
        errors.append(f"Canonical orders must be 1 through 7; found {sorted(orders)}")


def validate_protocol_registry(errors: list[str]) -> None:
    path = ROOT / "protocols" / "registry.yaml"
    registry = load_yaml(path, errors)
    if not isinstance(registry, dict):
        return

    entries = registry.get("protocols") or registry.get("registered_protocols")
    if not isinstance(entries, list):
        errors.append("protocols/registry.yaml: protocol list not found")
        return

    keys: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        key = entry.get("canonical_key")
        if isinstance(key, str):
            keys.add(key)
        value = entry.get("path") or entry.get("protocol_path")
        if isinstance(value, str):
            check_path(value, f"protocol {key}", errors)

    missing = sorted(REQUIRED_PROTOCOLS - keys)
    if missing:
        errors.append(f"Required protocols absent from registry: {', '.join(missing)}")


def validate_sppp_integration(errors: list[str]) -> None:
    required_paths = (
        "studies/studies-in-platonic-political-philosophy/source-status.yaml",
        "studies/studies-in-platonic-political-philosophy/sequential-reading.yaml",
        "studies/studies-in-platonic-political-philosophy/foundational-problems-synthesis.yaml",
        "studies/studies-in-platonic-political-philosophy/theologico-political-reconstruction.yaml",
        "studies/studies-in-platonic-political-philosophy/repository-integration.yaml",
        "studies/studies-in-platonic-political-philosophy/integration-completion.yaml",
        "migrations/foundational-problems-v2/transactions/theologico-political-sppp-study-001.yaml",
        "migrations/foundational-problems-v2/validation/sppp-integration-001.yaml",
        "problems/philosophy-vs-poetry/witnesses.yaml",
        "problems/theologico-political/witnesses.yaml",
        "protocols/speech-and-deed.yaml",
    )
    for value in required_paths:
        check_path(value, "SPPP integration", errors)

    bridge_paths = (
        "problems/nomos-vs-physis/synthesis/studies-in-platonic-political-philosophy.yaml",
        "problems/theory-vs-practice/synthesis/studies-in-platonic-political-philosophy.yaml",
        "problems/athens-vs-jerusalem/synthesis/studies-in-platonic-political-philosophy.yaml",
        "problems/wise-vs-vulgar/synthesis/studies-in-platonic-political-philosophy.yaml",
        "problems/ancients-vs-moderns/synthesis/studies-in-platonic-political-philosophy.yaml",
    )
    for value in bridge_paths:
        check_path(value, "SPPP problem bridge", errors)

    active_predecessor = ROOT / "problems" / "theologico-political.yaml"
    preserved_predecessor = (
        ROOT
        / "history"
        / "foundational-problems"
        / "theologico-political"
        / "STR-PROBLEM-002-v1.1-active-predecessor.yaml"
    )
    if active_predecessor.exists() and preserved_predecessor.exists():
        if active_predecessor.read_bytes() != preserved_predecessor.read_bytes():
            errors.append("Theologico-Political active predecessor differs from preserved copy")
    else:
        errors.append("Theologico-Political predecessor or preserved copy is missing")


def main() -> int:
    errors: list[str] = []
    yaml_count = validate_all_yaml(errors)
    validate_registry(errors)
    validate_protocol_registry(errors)
    validate_sppp_integration(errors)

    if errors:
        print(f"Validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validation passed: parsed {yaml_count} YAML files.")
    print("Seven canonical problem identities and orders are unique and aligned.")
    print("SPPP integration paths and preserved predecessor equality are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
