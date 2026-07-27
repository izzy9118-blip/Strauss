#!/usr/bin/env python3
"""Validate and load the typed Strauss corpus registry.

The validator distinguishes source identity, reviewed witness, source-status record,
source-specific study, independent corroboration, findings, migration, and certification.
Passing validation never converts a bounded current-state registry into a complete corpus
or a doctrinal authority.
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
    "studies/theologico-political/jerusalem-and-athens/source-status.yaml",
    "studies/theologico-political/jerusalem-and-athens/sequential-reconstruction.yaml",
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


def _find_record(records: Any, field: str, value: str) -> dict[str, Any] | None:
    if not isinstance(records, list):
        return None
    return next(
        (item for item in records if isinstance(item, dict) and item.get(field) == value),
        None,
    )


def _unique_ids(records: Any, field: str, label: str, errors: list[str]) -> set[str]:
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
            if not _resolve(value).exists():
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
    return {
        str(path.relative_to(ROOT))
        for path in (ROOT / "studies").rglob("*.yaml")
        if path.is_file()
    }


def _tp_sequence_from_source_id(source_id: str) -> int | None:
    match = re.fullmatch(r"CORPUS-SRC-(1\d{2})", source_id)
    if not match:
        return None
    sequence = int(match.group(1)) - 100
    return sequence if 1 <= sequence <= 19 else None


def _validate_container_fingerprint(
    registry: dict[str, Any],
    *,
    witness_id: str,
    source_status_path: str,
    status_field: str,
    label: str,
    errors: list[str],
) -> None:
    witness = _find_record(registry.get("reviewed_witnesses", []), "witness_id", witness_id)
    status = load_yaml(_resolve(source_status_path))
    reviewed = status.get(status_field, {})
    if not isinstance(witness, dict):
        errors.append(f"{label} reviewed witness is missing")
        return
    if not isinstance(reviewed, dict):
        errors.append(f"{label} {status_field} must be a mapping")
        return
    for registry_field, status_key in (
        ("page_count", "page_count"),
        ("file_size_bytes", "file_size_bytes"),
        ("sha256", "sha256"),
    ):
        if registry_field in witness and witness.get(registry_field) != reviewed.get(status_key):
            errors.append(f"{label} reviewed witness {registry_field} mismatch")


def _validate_tp_sources_and_statuses(
    registry: dict[str, Any], predecessor_sources: list[dict[str, Any]], errors: list[str]
) -> None:
    source_entities = registry.get("source_entities", [])
    status_records = registry.get("source_status_records", [])
    witness_records = registry.get("reviewed_witnesses", [])
    study_records = registry.get("study_records", [])

    tp_statuses = [
        item
        for item in status_records
        if isinstance(item, dict)
        and isinstance(item.get("source_id"), str)
        and _tp_sequence_from_source_id(item["source_id"]) is not None
    ]
    if len(tp_statuses) != 19:
        errors.append(f"expected 19 Theologico-Political item statuses, found {len(tp_statuses)}")

    for sequence, original in enumerate(predecessor_sources, start=1):
        source_id = f"CORPUS-SRC-{100 + sequence:03d}"
        status_id = f"CORPUS-STATUS-{100 + sequence:03d}"
        source = _find_record(source_entities, "source_id", source_id)
        entry = _find_record(status_records, "status_id", status_id)
        if not isinstance(source, dict):
            errors.append(f"missing source entity {source_id}")
            continue
        if not isinstance(entry, dict):
            errors.append(f"missing source-status entry {status_id}")
            continue
        if entry.get("source_id") != source_id:
            errors.append(f"{status_id} source binding mismatch")
        path_value = entry.get("path")
        if not isinstance(path_value, str):
            errors.append(f"{status_id} path must be a string")
            continue
        status = load_yaml(_resolve(path_value))
        identity = status.get("identity", {})
        state = status.get("status", {})
        registration = status.get("registration_basis", {})
        termination = status.get("termination", {})

        expected_identity = {
            "status_id": status_id,
            "corpus_source_id": source_id,
            "canonical_title": original.get("title"),
            "author": "Leo Strauss",
            "date": original.get("date"),
        }
        for field, expected in expected_identity.items():
            if identity.get(field) != expected:
                errors.append(
                    f"{status_id} identity.{field} mismatch: expected {expected!r}, "
                    f"found {identity.get(field)!r}"
                )
        if source.get("canonical_title") != original.get("title"):
            errors.append(f"{source_id} title does not match predecessor sequence {sequence}")
        if source.get("date") != original.get("date"):
            errors.append(f"{source_id} date does not match predecessor sequence {sequence}")
        alias = original.get("canonical_alias")
        if alias:
            if alias not in source.get("canonical_aliases", []):
                errors.append(f"{source_id} omits canonical alias {alias!r}")
            if alias not in identity.get("canonical_aliases", []):
                errors.append(f"{status_id} omits canonical alias {alias!r}")
        scope = original.get("scope")
        if scope:
            if source.get("registered_scope") != scope:
                errors.append(f"{source_id} registered scope mismatch")
            if identity.get("registered_scope") != scope:
                errors.append(f"{status_id} registered scope mismatch")
        if registration.get("active_predecessor_source_sequence") != sequence:
            errors.append(f"{status_id} predecessor sequence mismatch")
        if registration.get("active_predecessor") != "problems/theologico-political.yaml":
            errors.append(f"{status_id} active predecessor reference mismatch")
        if registration.get("corpus_source_id") != source_id:
            errors.append(f"{status_id} corpus source binding mismatch")
        if entry.get("certification") != "NOT_CERTIFIED":
            errors.append(f"{status_id} registry entry must remain NOT_CERTIFIED")
        if state.get("certification") != "NOT_CERTIFIED":
            errors.append(f"{status_id} source status must remain NOT_CERTIFIED")
        if termination.get("certification") != "NOT_CERTIFIED":
            errors.append(f"{status_id} termination must remain NOT_CERTIFIED")
        if termination.get("successor_effect") != "NONE":
            errors.append(f"{status_id} may not affect successor activation")

        reviewed_witness_id = state.get("reviewed_witness")
        if source_id == "CORPUS-SRC-109":
            if reviewed_witness_id != "CORPUS-WIT-109":
                errors.append("CORPUS-STATUS-109 must retain CORPUS-WIT-109")
            witness = _find_record(witness_records, "witness_id", "CORPUS-WIT-109")
            reviewed = status.get("reviewed_witness", {})
            if not isinstance(witness, dict):
                errors.append("CORPUS-WIT-109 is missing")
            elif witness.get("source_id") != source_id:
                errors.append("CORPUS-WIT-109 source binding mismatch")
            if source.get("reviewed_witnesses") != ["CORPUS-WIT-109"]:
                errors.append("CORPUS-SRC-109 must list CORPUS-WIT-109")
            if source.get("study_records") != ["CORPUS-STUDY-008"]:
                errors.append("CORPUS-SRC-109 must list CORPUS-STUDY-008")
            if state.get("independent_sequential_study") != "JA-STUDY-001":
                errors.append("CORPUS-STATUS-109 must record JA-STUDY-001")
            study = _find_record(study_records, "study_id", "CORPUS-STUDY-008")
            if not isinstance(study, dict):
                errors.append("CORPUS-STUDY-008 is missing")
            elif study.get("path") != "studies/theologico-political/jerusalem-and-athens/sequential-reconstruction.yaml":
                errors.append("CORPUS-STUDY-008 path mismatch")
            if termination.get("study_state") != "COMPLETE_PROVISIONAL":
                errors.append("CORPUS-STATUS-109 study_state must be COMPLETE_PROVISIONAL")
            if termination.get("study_id") != "JA-STUDY-001":
                errors.append("CORPUS-STATUS-109 termination study id mismatch")
            if not isinstance(reviewed, dict) or reviewed.get("witness_id") != "CORPUS-WIT-109":
                errors.append("CORPUS-STATUS-109 reviewed_witness block mismatch")
            if isinstance(witness, dict):
                for field in ("container_sha256", "printed_page_range", "pdf_page_range_one_based"):
                    if witness.get(field) != reviewed.get(field):
                        errors.append(f"CORPUS-WIT-109 {field} mismatch")
            if termination.get("reviewed_witness_state") != "REGISTERED":
                errors.append("CORPUS-STATUS-109 must terminate with registered witness")
        else:
            if reviewed_witness_id != "NOT_YET_REGISTERED":
                errors.append(f"{status_id} must remain without a reviewed witness")
            if state.get("independent_sequential_study") != "NOT_YET_COMPLETED":
                errors.append(f"{status_id} independent study must remain incomplete")
            if termination.get("study_state") != "INCOMPLETE":
                errors.append(f"{status_id} study state must remain INCOMPLETE")
            publication = status.get("publication_and_witness_condition", {})
            if publication.get("fingerprint") != "NOT_AVAILABLE":
                errors.append(f"{status_id} may not claim a fingerprint before witness registration")
            if publication.get("locator_reproducibility") != "INCOMPLETE":
                errors.append(f"{status_id} missing-witness locator state mismatch")
            if termination.get("reviewed_witness_state") != "MISSING":
                errors.append(f"{status_id} must preserve missing witness state")


def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP_LEVEL - set(registry))
    if missing:
        errors.append("corpus registry missing sections: " + ", ".join(missing))

    identity = registry.get("identity", {})
    if identity.get("id") != "STRAUSS-CORPUS-INDEX-001":
        errors.append("corpus registry identity.id mismatch")
    if identity.get("version") != "1.6.0":
        errors.append("corpus registry identity.version must be 1.6.0")

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

    expected_counts = {
        "source entities": (len(source_ids), 22),
        "reviewed witnesses": (len(witness_ids), 4),
        "source-status records": (len(status_ids), 22),
        "study records": (len(study_ids), 8),
        "corpus gaps": (len(gap_ids), 7),
    }
    for label, (actual, expected) in expected_counts.items():
        if actual != expected:
            errors.append(f"expected {expected} {label}, found {actual}")

    for label, records in (
        ("reviewed_witnesses", witness_records),
        ("source_status_records", status_records),
        ("study_records", study_records),
    ):
        if isinstance(records, list):
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
    if not TP_PRESERVED_PATH.exists() or TP_PREDECESSOR_PATH.read_bytes() != TP_PRESERVED_PATH.read_bytes():
        errors.append("Theologico-Political active predecessor does not match preserved copy")
    predecessor_sources = predecessor.get("documentary_source_basis", {}).get("sources", [])
    if not isinstance(predecessor_sources, list) or len(predecessor_sources) != 19:
        errors.append("Theologico-Political predecessor must contain 19 source records")
        predecessor_sources = []
    if predecessor_sources:
        _validate_tp_sources_and_statuses(registry, predecessor_sources, errors)

    _validate_container_fingerprint(
        registry,
        witness_id="CORPUS-WIT-001",
        source_status_path="studies/studies-in-platonic-political-philosophy/source-status.yaml",
        status_field="reviewed_witness",
        label="SPPP",
        errors=errors,
    )
    _validate_container_fingerprint(
        registry,
        witness_id="CORPUS-WIT-003",
        source_status_path="studies/socrates-and-aristophanes/source-status.yaml",
        status_field="reviewed_witness",
        label="Socrates and Aristophanes",
        errors=errors,
    )

    tp_entities = [
        item
        for item in source_entities
        if isinstance(item, dict)
        and isinstance(item.get("source_id"), str)
        and _tp_sequence_from_source_id(item["source_id"]) is not None
    ]
    coverage = registry.get("coverage", {})
    expected_coverage = {
        "source_entities_registered": len(source_ids),
        "reviewed_witnesses_registered": len(witness_ids),
        "source_status_records_registered": len(status_ids),
        "study_records_registered": len(study_ids),
        "problem_witness_registries_registered": len(problem_registries) if isinstance(problem_registries, list) else 0,
        "theologico_political_predecessor_sources_registered": len(tp_entities),
        "theologico_political_item_level_statuses_registered": 19,
        "theologico_political_reviewed_item_witnesses_registered": 1,
        "theologico_political_independent_item_studies_registered": 1,
        "current_studies_tree_yaml_records_accounted_for": len(actual_studies),
        "exhaustive_within_declared_scope": True,
    }
    for field, expected in expected_coverage.items():
        if coverage.get(field) != expected:
            errors.append(f"coverage.{field} mismatch: expected {expected!r}, found {coverage.get(field)!r}")

    termination = registry.get("termination", {})
    if termination.get("registry_state") != "COMPLETE_FOR_CURRENT_COMMITTED_SOURCE_AND_STUDY_STATE":
        errors.append("registry termination state must preserve bounded current-state completion")
    if termination.get("theologico_political_identity_registration_state") != "COMPLETE_19_OF_19":
        errors.append("TP identity registration must remain COMPLETE_19_OF_19")
    if termination.get("theologico_political_reviewed_witness_state") != "INCOMPLETE_1_OF_19":
        errors.append("TP reviewed-witness state must be INCOMPLETE_1_OF_19")
    if termination.get("theologico_political_independent_study_state") != "INCOMPLETE_1_OF_19":
        errors.append("TP independent-study state must be INCOMPLETE_1_OF_19")
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
            "no witness ranking as truth",
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
            "Typed corpus registry validation passed for the current committed source and "
            "study state; corpus remains open, materially incomplete, and not certified."
        )
        return 0
    context = build_registry_context()
    print(json.dumps(context, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
