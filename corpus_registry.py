#!/usr/bin/env python3
"""Validate and load the typed Strauss corpus registry.

The registry is exhaustive only for the repository's current committed source and
study state. This validator does not admit source texts, certify findings, complete
missing witnesses, or convert current-state indexing into a closed corpus.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).resolve().parent
REGISTRY_PATH = ROOT / "corpus" / "index.yaml"
TP_PREDECESSOR_PATH = ROOT / "problems" / "theologico-political.yaml"
TP_PRESERVED_PATH = (
    ROOT
    / "history"
    / "foundational-problems"
    / "theologico-political"
    / "STR-PROBLEM-002-v1.1-active-predecessor.yaml"
)

CANONICAL_PROBLEMS = [
    "nomos-vs-physis",
    "philosophy-vs-poetry",
    "theory-vs-practice",
    "theologico-political",
    "athens-vs-jerusalem",
    "wise-vs-vulgar",
    "ancients-vs-moderns",
]

EXPECTED_STUDY_TREE_PATHS = {
    "studies/socrates-and-aristophanes/philosophy-poetry-theologico-political-reconstruction.yaml",
    "studies/studies-in-platonic-political-philosophy/source-status.yaml",
    "studies/studies-in-platonic-political-philosophy/sequential-reading.yaml",
    "studies/studies-in-platonic-political-philosophy/foundational-problems-synthesis.yaml",
    "studies/studies-in-platonic-political-philosophy/theologico-political-reconstruction.yaml",
    "studies/studies-in-platonic-political-philosophy/repository-integration.yaml",
    "studies/studies-in-platonic-political-philosophy/integration-completion.yaml",
    "studies/plato/apology/source-status.yaml",
    "studies/plato/apology/philosophy-poetry-divine-authority-reconstruction.yaml",
}

REQUIRED_TOP_LEVEL = {
    "identity",
    "status",
    "purpose",
    "scope_rule",
    "identifier_rules",
    "source_entities",
    "reviewed_witnesses",
    "source_status_records",
    "study_records",
    "problem_witness_registries",
    "repository_documentary_artifacts",
    "coverage",
    "corpus_gaps",
    "validation_rules",
    "termination",
}


class CorpusRegistryError(RuntimeError):
    """Raised when the corpus registry cannot be loaded or validated safely."""


def _resolve(relative_path: str) -> Path:
    path = (ROOT / relative_path).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError as exc:
        raise CorpusRegistryError(f"Path escapes repository root: {relative_path}") from exc
    return path


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CorpusRegistryError(f"Cannot read {path.relative_to(ROOT)}: {exc}") from exc
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise CorpusRegistryError(f"Invalid YAML in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(data, dict):
        raise CorpusRegistryError(f"Expected a YAML mapping in {path.relative_to(ROOT)}")
    return data


def load_registry() -> dict[str, Any]:
    return load_yaml(REGISTRY_PATH)


def _unique_ids(
    records: Any,
    field: str,
    label: str,
    errors: list[str],
) -> set[str]:
    if not isinstance(records, list):
        errors.append(f"{label} must be a list")
        return set()
    values: list[str] = []
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            errors.append(f"{label} item {index} must be a mapping")
            continue
        value = record.get(field)
        if not isinstance(value, str) or not value:
            errors.append(f"{label} item {index} missing {field}")
            continue
        values.append(value)
    if len(values) != len(set(values)):
        errors.append(f"{label} contains duplicate {field} values")
    return set(values)


def _check_paths(records: Iterable[dict[str, Any]], fields: Iterable[str], errors: list[str]) -> None:
    for record in records:
        for field in fields:
            value = record.get(field)
            if value is None or value == "NOT_SEPARATELY_REGISTERED":
                continue
            if not isinstance(value, str):
                errors.append(f"path field {field} must be a string when present")
                continue
            path = _resolve(value)
            if not path.exists():
                errors.append(f"registered path does not resolve: {value}")


def _registered_study_paths(registry: dict[str, Any]) -> set[str]:
    paths = {
        item.get("path")
        for item in registry.get("study_records", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    paths.update(
        item.get("path")
        for item in registry.get("source_status_records", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    )
    return paths


def _actual_study_tree_paths() -> set[str]:
    root = ROOT / "studies"
    return {
        str(path.relative_to(ROOT))
        for path in root.rglob("*.yaml")
        if path.is_file()
    }


def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    missing = sorted(REQUIRED_TOP_LEVEL - set(registry))
    if missing:
        errors.append("corpus registry missing sections: " + ", ".join(missing))

    identity = registry.get("identity", {})
    if identity.get("id") != "STRAUSS-CORPUS-INDEX-001":
        errors.append("corpus registry identity.id mismatch")
    if identity.get("version") != "1.0.0":
        errors.append("corpus registry identity.version must be 1.0.0")

    status = registry.get("status", {})
    if status.get("registry_scope") != "EXHAUSTIVE_FOR_CURRENT_COMMITTED_SOURCE_AND_STUDY_STATE":
        errors.append("corpus registry must state bounded current-state exhaustiveness")
    if status.get("corpus_completion") != "INCOMPLETE_OPEN_CORPUS":
        errors.append("corpus registry must remain an incomplete open corpus")
    if status.get("certification") != "NOT_CERTIFIED":
        errors.append("corpus registry must remain NOT_CERTIFIED")

    source_entities = registry.get("source_entities", [])
    witness_records = registry.get("reviewed_witnesses", [])
    status_records = registry.get("source_status_records", [])
    study_records = registry.get("study_records", [])
    problem_registries = registry.get("problem_witness_registries", [])
    gaps = registry.get("corpus_gaps", [])

    source_ids = _unique_ids(source_entities, "source_id", "source_entities", errors)
    witness_ids = _unique_ids(witness_records, "witness_id", "reviewed_witnesses", errors)
    status_ids = _unique_ids(status_records, "status_id", "source_status_records", errors)
    study_ids = _unique_ids(study_records, "study_id", "study_records", errors)
    gap_ids = _unique_ids(gaps, "gap_id", "corpus_gaps", errors)

    if len(source_ids) != 22:
        errors.append(f"expected 22 source entities, found {len(source_ids)}")
    if len(witness_ids) != 2:
        errors.append(f"expected 2 reviewed witnesses, found {len(witness_ids)}")
    if len(status_ids) != 2:
        errors.append(f"expected 2 source-status records, found {len(status_ids)}")
    if len(study_ids) != 7:
        errors.append(f"expected 7 study records, found {len(study_ids)}")
    if len(gap_ids) != 7:
        errors.append(f"expected 7 corpus gaps, found {len(gap_ids)}")

    for label, records in (
        ("reviewed_witnesses", witness_records),
        ("source_status_records", status_records),
        ("study_records", study_records),
    ):
        if not isinstance(records, list):
            continue
        for item in records:
            if isinstance(item, dict) and item.get("source_id") not in source_ids:
                errors.append(f"{label} references unknown source_id {item.get('source_id')!r}")

    _check_paths(status_records if isinstance(status_records, list) else [], ("path",), errors)
    _check_paths(study_records if isinstance(study_records, list) else [], ("path",), errors)
    _check_paths(problem_registries if isinstance(problem_registries, list) else [], ("path",), errors)

    actual_studies = _actual_study_tree_paths()
    registered_studies = _registered_study_paths(registry)
    if actual_studies != EXPECTED_STUDY_TREE_PATHS:
        errors.append(
            "studies tree changed without registry revision: "
            f"missing_expected={sorted(EXPECTED_STUDY_TREE_PATHS - actual_studies)!r}, "
            f"new_unexpected={sorted(actual_studies - EXPECTED_STUDY_TREE_PATHS)!r}"
        )
    if registered_studies != actual_studies:
        errors.append(
            "registered study and source-status paths do not exhaust the studies tree: "
            f"unregistered={sorted(actual_studies - registered_studies)!r}, "
            f"stale={sorted(registered_studies - actual_studies)!r}"
        )

    if not isinstance(problem_registries, list) or len(problem_registries) != 7:
        errors.append("exactly seven problem witness registries must be registered")
    else:
        problems = [item.get("problem") for item in problem_registries if isinstance(item, dict)]
        if problems != CANONICAL_PROBLEMS:
            errors.append(f"problem witness registry order mismatch: {problems!r}")

    predecessor = load_yaml(TP_PREDECESSOR_PATH)
    preserved = TP_PRESERVED_PATH.read_bytes() if TP_PRESERVED_PATH.exists() else b""
    active = TP_PREDECESSOR_PATH.read_bytes()
    if not preserved or active != preserved:
        errors.append("Theologico-Political active predecessor does not match preserved copy")

    predecessor_sources = predecessor.get("documentary_source_basis", {}).get("sources", [])
    if not isinstance(predecessor_sources, list) or len(predecessor_sources) != 19:
        errors.append("Theologico-Political predecessor must contain 19 source records")
    tp_entities = [
        item
        for item in source_entities
        if isinstance(item, dict)
        and isinstance(item.get("source_id"), str)
        and item["source_id"].startswith("CORPUS-SRC-1")
        and item["source_id"] not in {"CORPUS-SRC-001", "CORPUS-SRC-002", "CORPUS-SRC-003"}
    ]
    tp_entities.sort(key=lambda item: item["source_id"])
    if len(tp_entities) != 19:
        errors.append(f"expected 19 registered predecessor source entities, found {len(tp_entities)}")
    else:
        for position, (registered, original) in enumerate(
            zip(tp_entities, predecessor_sources),
            start=1,
        ):
            if registered.get("source_id") != f"CORPUS-SRC-{100 + position:03d}":
                errors.append(f"predecessor source id sequence mismatch at {position}")
            if registered.get("canonical_title") != original.get("title"):
                errors.append(
                    f"predecessor source title mismatch at {position}: "
                    f"registry={registered.get('canonical_title')!r}, original={original.get('title')!r}"
                )
            if registered.get("date") != original.get("date"):
                errors.append(f"predecessor source date mismatch at {position}")

    sppp_status = load_yaml(
        ROOT / "studies" / "studies-in-platonic-political-philosophy" / "source-status.yaml"
    )
    sppp_witness = next(
        (item for item in witness_records if item.get("witness_id") == "CORPUS-WIT-001"),
        None,
    )
    reviewed = sppp_status.get("reviewed_witness", {})
    if not isinstance(sppp_witness, dict):
        errors.append("SPPP reviewed witness is missing")
    else:
        for field in ("page_count", "file_size_bytes", "sha256"):
            if sppp_witness.get(field) != reviewed.get(field):
                errors.append(f"SPPP reviewed witness {field} mismatch")

    coverage = registry.get("coverage", {})
    expected_coverage = {
        "source_entities_registered": len(source_ids),
        "reviewed_witnesses_registered": len(witness_ids),
        "source_status_records_registered": len(status_ids),
        "study_records_registered": len(study_ids),
        "problem_witness_registries_registered": len(problem_registries) if isinstance(problem_registries, list) else 0,
        "theologico_political_predecessor_sources_registered": len(tp_entities),
        "current_studies_tree_yaml_records_accounted_for": len(actual_studies),
        "exhaustive_within_declared_scope": True,
    }
    for field, expected in expected_coverage.items():
        if coverage.get(field) != expected:
            errors.append(
                f"coverage.{field} mismatch: expected {expected!r}, found {coverage.get(field)!r}"
            )

    termination = registry.get("termination", {})
    if termination.get("registry_state") != "COMPLETE_FOR_CURRENT_COMMITTED_SOURCE_AND_STUDY_STATE":
        errors.append("registry termination state must preserve bounded current-state completion")
    if termination.get("corpus_state") != "OPEN_AND_MATERIALLY_INCOMPLETE":
        errors.append("registry termination must preserve an open, incomplete corpus")
    if termination.get("certification") != "NOT_CERTIFIED":
        errors.append("registry termination may not certify the corpus")

    return errors


def build_registry_context() -> dict[str, Any]:
    registry = load_registry()
    errors = validate_registry(registry)
    if errors:
        raise CorpusRegistryError("Corpus registry validation failed:\n- " + "\n- ".join(errors))
    return {
        "identity": registry["identity"],
        "status": registry["status"],
        "source_entities": registry["source_entities"],
        "reviewed_witnesses": registry["reviewed_witnesses"],
        "source_status_records": registry["source_status_records"],
        "study_records": registry["study_records"],
        "problem_witness_registries": registry["problem_witness_registries"],
        "corpus_gaps": registry["corpus_gaps"],
        "coverage": registry["coverage"],
        "authority": "READ_ONLY_DISCOVERY_AND_PROVENANCE_CONTEXT",
        "non_effects": [
            "no source-text admission",
            "no doctrinal certification",
            "no witness ranking",
            "no migration certification",
            "no successor activation",
            "no Assembly authority",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    registry = load_registry()
    errors = validate_registry(registry)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.validate:
        print(
            "Typed corpus registry validation passed for the current committed source "
            "and study state; the corpus remains open, incomplete, and not certified."
        )
        return 0
    context = build_registry_context()
    print(json.dumps(context, indent=2 if args.pretty else None, sort_keys=args.pretty))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
