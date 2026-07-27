#!/usr/bin/env python3
"""Validate and load the typed Strauss corpus registry.

The registry is exhaustive only for the repository's current committed source and
study state. This validator does not admit source texts, certify findings, complete
missing witnesses, or convert current-state indexing into a closed corpus.
"""

from __future__ import annotations

import argparse
import json
import re
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

BASE_REQUIRED_STUDY_PATHS = {
    "studies/socrates-and-aristophanes/source-status.yaml",
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


def _check_paths(
    records: Iterable[dict[str, Any]],
    fields: Iterable[str],
    errors: list[str],
) -> None:
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


def _find_record(records: Any, field: str, value: str) -> dict[str, Any] | None:
    if not isinstance(records, list):
        return None
    for item in records:
        if isinstance(item, dict) and item.get(field) == value:
            return item
    return None


def _validate_semver(version: Any, errors: list[str]) -> None:
    if not isinstance(version, str) or not re.fullmatch(r"1\.\d+\.0", version):
        errors.append("corpus registry identity.version must be a 1.x.0 semantic version")


def _validate_reviewed_witness_fingerprint(
    *,
    source_status_path: Path,
    witness_id: str,
    witness_records: Any,
    label: str,
    errors: list[str],
) -> None:
    status = load_yaml(source_status_path)
    witness = _find_record(witness_records, "witness_id", witness_id)
    reviewed = status.get("reviewed_witness", {})
    if not isinstance(witness, dict):
        errors.append(f"{label} reviewed witness is missing")
        return
    if not isinstance(reviewed, dict):
        errors.append(f"{label} source-status reviewed_witness must be a mapping")
        return
    for field in ("page_count", "file_size_bytes", "sha256"):
        if witness.get(field) != reviewed.get(field):
            errors.append(f"{label} reviewed witness {field} mismatch")


def _tp_sequence_from_source_id(source_id: str) -> int | None:
    match = re.fullmatch(r"CORPUS-SRC-(1\d{2})", source_id)
    if not match:
        return None
    sequence = int(match.group(1)) - 100
    return sequence if 1 <= sequence <= 19 else None


def _validate_tp_item_statuses(
    *,
    source_entities: Any,
    status_records: Any,
    predecessor_sources: Any,
    errors: list[str],
) -> None:
    if not isinstance(source_entities, list) or not isinstance(status_records, list):
        return
    if not isinstance(predecessor_sources, list):
        return

    for entry in status_records:
        if not isinstance(entry, dict):
            continue
        source_id = entry.get("source_id")
        sequence = _tp_sequence_from_source_id(source_id) if isinstance(source_id, str) else None
        if sequence is None:
            continue

        status_id = entry.get("status_id")
        path_value = entry.get("path")
        source = _find_record(source_entities, "source_id", source_id)
        if not isinstance(source, dict):
            errors.append(f"{status_id} references missing source entity {source_id}")
            continue
        if not isinstance(status_id, str) or not status_id.startswith("CORPUS-STATUS-"):
            errors.append(f"Theologico-Political status for {source_id} has invalid status_id")
            continue
        if source.get("source_status_record") != status_id:
            errors.append(f"{source_id} must reference {status_id} as source_status_record")
        if source.get("item_level_source_status") != "REGISTERED_SOURCE_IDENTITY_WITHOUT_REVIEWED_WITNESS":
            errors.append(f"{source_id} must preserve registered-identity-without-witness status")
        if entry.get("certification") != "NOT_CERTIFIED":
            errors.append(f"{status_id} must remain NOT_CERTIFIED")
        if not isinstance(path_value, str):
            errors.append(f"{status_id} path must be a string")
            continue

        status = load_yaml(_resolve(path_value))
        identity = status.get("identity", {})
        lifecycle = status.get("status", {})
        registration = status.get("registration_basis", {})
        publication = status.get("publication_and_witness_condition", {})
        termination = status.get("termination", {})
        original = predecessor_sources[sequence - 1]

        expected_identity = {
            "status_id": status_id,
            "corpus_source_id": source_id,
            "canonical_title": source.get("canonical_title"),
            "author": "Leo Strauss",
            "date": source.get("date"),
            "version": "1.0.0",
        }
        for field, expected in expected_identity.items():
            if identity.get(field) != expected:
                errors.append(
                    f"{status_id} identity.{field} mismatch: "
                    f"expected {expected!r}, found {identity.get(field)!r}"
                )

        source_aliases = source.get("canonical_aliases", [])
        if source_aliases:
            if identity.get("canonical_aliases") != source_aliases:
                errors.append(f"{status_id} canonical aliases do not match the source entity")
        if source.get("canonical_title") != original.get("title"):
            errors.append(f"{status_id} source title does not match predecessor sequence {sequence}")
        if source.get("date") != original.get("date"):
            errors.append(f"{status_id} source date does not match predecessor sequence {sequence}")
        original_alias = original.get("canonical_alias")
        if original_alias and original_alias not in source_aliases:
            errors.append(f"{status_id} omits predecessor canonical alias {original_alias!r}")

        if lifecycle.get("lifecycle") != "REGISTERED_SOURCE_IDENTITY":
            errors.append(f"{status_id} lifecycle must remain REGISTERED_SOURCE_IDENTITY")
        if lifecycle.get("reviewed_witness") != "NOT_YET_REGISTERED":
            errors.append(f"{status_id} must preserve the missing reviewed witness")
        if lifecycle.get("independent_sequential_study") != "NOT_YET_COMPLETED":
            errors.append(f"{status_id} must preserve the incomplete independent study")
        if lifecycle.get("certification") != "NOT_CERTIFIED":
            errors.append(f"{status_id} source status must remain NOT_CERTIFIED")
        if registration.get("active_predecessor_source_sequence") != sequence:
            errors.append(f"{status_id} predecessor sequence must remain {sequence}")
        if registration.get("active_predecessor") != "problems/theologico-political.yaml":
            errors.append(f"{status_id} active predecessor reference mismatch")
        if registration.get("corpus_source_id") != source_id:
            errors.append(f"{status_id} corpus source binding mismatch")
        if publication.get("fingerprint") != "NOT_AVAILABLE":
            errors.append(f"{status_id} may not claim a fingerprint before witness registration")
        if publication.get("locator_reproducibility") != "INCOMPLETE":
            errors.append(f"{status_id} locator reproducibility must remain INCOMPLETE")
        if termination.get("reviewed_witness_state") != "MISSING":
            errors.append(f"{status_id} termination must preserve missing witness state")
        if termination.get("study_state") != "INCOMPLETE":
            errors.append(f"{status_id} termination must preserve incomplete study state")
        if termination.get("certification") != "NOT_CERTIFIED":
            errors.append(f"{status_id} termination must remain NOT_CERTIFIED")
        if termination.get("successor_effect") != "NONE":
            errors.append(f"{status_id} may not affect successor activation")

    for source in source_entities:
        if not isinstance(source, dict):
            continue
        source_id = source.get("source_id")
        sequence = _tp_sequence_from_source_id(source_id) if isinstance(source_id, str) else None
        if sequence is None:
            continue
        status_id = source.get("source_status_record")
        if status_id is None:
            continue
        entry = _find_record(status_records, "status_id", status_id)
        if not isinstance(entry, dict):
            errors.append(f"{source_id} references unregistered source status {status_id!r}")


def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    missing = sorted(REQUIRED_TOP_LEVEL - set(registry))
    if missing:
        errors.append("corpus registry missing sections: " + ", ".join(missing))

    identity = registry.get("identity", {})
    if identity.get("id") != "STRAUSS-CORPUS-INDEX-001":
        errors.append("corpus registry identity.id mismatch")
    _validate_semver(identity.get("version"), errors)

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

    fixed_expected = {
        "source entities": (len(source_ids), 22),
        "reviewed witnesses": (len(witness_ids), 3),
        "study records": (len(study_ids), 7),
        "corpus gaps": (len(gap_ids), 7),
    }
    for label, (actual, expected) in fixed_expected.items():
        if actual != expected:
            errors.append(f"expected {expected} {label}, found {actual}")
    if len(status_ids) < 5:
        errors.append(f"expected at least 5 source-status records, found {len(status_ids)}")

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
    missing_baseline = sorted(BASE_REQUIRED_STUDY_PATHS - actual_studies)
    if missing_baseline:
        errors.append("required study records disappeared: " + ", ".join(missing_baseline))
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
        and _tp_sequence_from_source_id(item["source_id"]) is not None
    ]
    tp_entities.sort(key=lambda item: item["source_id"])
    if len(tp_entities) != 19:
        errors.append(f"expected 19 registered predecessor source entities, found {len(tp_entities)}")
    elif isinstance(predecessor_sources, list):
        for position, (registered, original) in enumerate(zip(tp_entities, predecessor_sources), start=1):
            if registered.get("source_id") != f"CORPUS-SRC-{100 + position:03d}":
                errors.append(f"predecessor source id sequence mismatch at {position}")
            if registered.get("canonical_title") != original.get("title"):
                errors.append(
                    f"predecessor source title mismatch at {position}: "
                    f"registry={registered.get('canonical_title')!r}, original={original.get('title')!r}"
                )
            if registered.get("date") != original.get("date"):
                errors.append(f"predecessor source date mismatch at {position}")

    _validate_reviewed_witness_fingerprint(
        source_status_path=ROOT / "studies" / "studies-in-platonic-political-philosophy" / "source-status.yaml",
        witness_id="CORPUS-WIT-001",
        witness_records=witness_records,
        label="SPPP",
        errors=errors,
    )
    _validate_reviewed_witness_fingerprint(
        source_status_path=ROOT / "studies" / "socrates-and-aristophanes" / "source-status.yaml",
        witness_id="CORPUS-WIT-003",
        witness_records=witness_records,
        label="Socrates and Aristophanes",
        errors=errors,
    )
    _validate_tp_item_statuses(
        source_entities=source_entities,
        status_records=status_records,
        predecessor_sources=predecessor_sources,
        errors=errors,
    )

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
