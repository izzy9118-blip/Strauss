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
TP_PRESERVED_PATH = ROOT / "history" / "foundational-problems" / "theologico-political" / "STR-PROBLEM-002-v1.1-active-predecessor.yaml"

CANONICAL_PROBLEMS = [
    "nomos-vs-physis",
    "philosophy-vs-poetry",
    "theory-vs-practice",
    "theologico-political",
    "athens-vs-jerusalem",
    "wise-vs-vulgar",
    "ancients-vs-moderns",
]

COMPLETED_TP_ITEMS = {
    "CORPUS-SRC-105": {
        "status_id": "CORPUS-STATUS-105",
        "witness_id": "CORPUS-WIT-105",
        "study_id": "COHEN-STUDY-001",
        "corpus_study_id": "CORPUS-STUDY-009",
        "study_path": "studies/theologico-political/introductory-essay-hermann-cohen-religion-of-reason/sequential-reconstruction.yaml",
        "printed_page_range": {"start": 233, "end": 247},
        "pdf_page_range_one_based": {"start": 237, "end": 251},
    },
    "CORPUS-SRC-109": {
        "status_id": "CORPUS-STATUS-109",
        "witness_id": "CORPUS-WIT-109",
        "study_id": "JA-STUDY-001",
        "corpus_study_id": "CORPUS-STUDY-008",
        "study_path": "studies/theologico-political/jerusalem-and-athens/sequential-reconstruction.yaml",
        "printed_page_range": {"start": 147, "end": 173},
        "pdf_page_range_one_based": {"start": 151, "end": 177},
    },
}

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
    "studies/theologico-political/introductory-essay-hermann-cohen-religion-of-reason/source-status.yaml",
    "studies/theologico-political/introductory-essay-hermann-cohen-religion-of-reason/sequential-reconstruction.yaml",
}

REQUIRED_TOP_LEVEL = {
    "identity", "status", "purpose", "scope_rule", "identifier_rules",
    "source_entities", "reviewed_witnesses", "source_status_records", "study_records",
    "problem_witness_registries", "repository_documentary_artifacts", "coverage",
    "corpus_gaps", "validation_rules", "termination",
}

CONTAINER_SHA256 = "8479ed41fe951b8ebc5a2a5b6557a482a60de0d13032785a68f11d51ea8b4fb6"


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
    return next((item for item in records if isinstance(item, dict) and item.get(field) == value), None)


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
            elif not _resolve(value).exists():
                errors.append(f"registered path does not resolve: {value}")


def _registered_study_paths(registry: dict[str, Any]) -> set[str]:
    paths = {
        item.get("path") for item in registry.get("study_records", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    paths.update(
        item.get("path") for item in registry.get("source_status_records", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    )
    return paths


def _actual_study_tree_paths() -> set[str]:
    return {str(path.relative_to(ROOT)) for path in (ROOT / "studies").rglob("*.yaml") if path.is_file()}


def _tp_sequence_from_source_id(source_id: str) -> int | None:
    match = re.fullmatch(r"CORPUS-SRC-(1\d{2})", source_id)
    if not match:
        return None
    sequence = int(match.group(1)) - 100
    return sequence if 1 <= sequence <= 19 else None


def _validate_collection_fingerprint(
    registry: dict[str, Any], witness_id: str, status_path: str, status_field: str,
    label: str, errors: list[str]
) -> None:
    witness = _find_record(registry.get("reviewed_witnesses", []), "witness_id", witness_id)
    status = load_yaml(_resolve(status_path))
    reviewed = status.get(status_field, {})
    if not isinstance(witness, dict):
        errors.append(f"{label} reviewed witness is missing")
        return
    if not isinstance(reviewed, dict):
        errors.append(f"{label} {status_field} must be a mapping")
        return
    for field in ("page_count", "file_size_bytes", "sha256"):
        if field in witness and witness.get(field) != reviewed.get(field):
            errors.append(f"{label} reviewed witness {field} mismatch")


def _validate_completed_item(
    registry: dict[str, Any], source: dict[str, Any], entry: dict[str, Any],
    status: dict[str, Any], expected: dict[str, Any], errors: list[str]
) -> None:
    source_id = source["source_id"]
    state = status.get("status", {})
    termination = status.get("termination", {})
    reviewed = status.get("reviewed_witness", {})
    witness_id = expected["witness_id"]
    corpus_study_id = expected["corpus_study_id"]
    witness = _find_record(registry.get("reviewed_witnesses", []), "witness_id", witness_id)
    study = _find_record(registry.get("study_records", []), "study_id", corpus_study_id)

    if source.get("reviewed_witnesses") != [witness_id]:
        errors.append(f"{source_id} reviewed witness binding mismatch")
    if source.get("study_records") != [corpus_study_id]:
        errors.append(f"{source_id} study binding mismatch")
    if state.get("reviewed_witness") != witness_id:
        errors.append(f"{source_id} source-status witness mismatch")
    if state.get("independent_sequential_study") != expected["study_id"]:
        errors.append(f"{source_id} source-status study mismatch")
    if termination.get("reviewed_witness_state") != "REGISTERED":
        errors.append(f"{source_id} must terminate with registered witness")
    if termination.get("study_state") != "COMPLETE_PROVISIONAL":
        errors.append(f"{source_id} must terminate with COMPLETE_PROVISIONAL study")
    if termination.get("study_id") != expected["study_id"]:
        errors.append(f"{source_id} termination study id mismatch")
    if termination.get("independent_corroboration") != "INCOMPLETE":
        errors.append(f"{source_id} must preserve incomplete independent corroboration")
    if not isinstance(witness, dict):
        errors.append(f"missing {witness_id}")
    else:
        if witness.get("source_id") != source_id:
            errors.append(f"{witness_id} source binding mismatch")
        if witness.get("container_sha256") != CONTAINER_SHA256:
            errors.append(f"{witness_id} container fingerprint mismatch")
        for field in ("printed_page_range", "pdf_page_range_one_based"):
            if witness.get(field) != expected[field]:
                errors.append(f"{witness_id} {field} mismatch")
            if not isinstance(reviewed, dict) or reviewed.get(field) != expected[field]:
                errors.append(f"{source_id} source-status {field} mismatch")
        if not isinstance(reviewed, dict) or reviewed.get("container_sha256") != CONTAINER_SHA256:
            errors.append(f"{source_id} source-status container fingerprint mismatch")
    if not isinstance(study, dict):
        errors.append(f"missing {corpus_study_id}")
    elif study.get("path") != expected["study_path"]:
        errors.append(f"{corpus_study_id} path mismatch")
    else:
        study_record = load_yaml(_resolve(study["path"]))
        if study_record.get("identity", {}).get("id") != expected["study_id"]:
            errors.append(f"{corpus_study_id} record identity mismatch")
        if study_record.get("termination", {}).get("reading_state") != "COMPLETE_FOR_REVIEWED_1983_COLLECTED_WITNESS":
            errors.append(f"{corpus_study_id} reading state mismatch")
        if study_record.get("termination", {}).get("independent_corroboration") != "INCOMPLETE":
            errors.append(f"{corpus_study_id} must preserve incomplete corroboration")


def _validate_tp_sources_and_statuses(
    registry: dict[str, Any], predecessor_sources: list[dict[str, Any]], errors: list[str]
) -> None:
    source_entities = registry.get("source_entities", [])
    status_records = registry.get("source_status_records", [])
    tp_statuses = [
        item for item in status_records if isinstance(item, dict)
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

        for field, expected_value in {
            "status_id": status_id,
            "corpus_source_id": source_id,
            "canonical_title": original.get("title"),
            "author": "Leo Strauss",
            "date": original.get("date"),
        }.items():
            if identity.get(field) != expected_value:
                errors.append(f"{status_id} identity.{field} mismatch")
        if source.get("canonical_title") != original.get("title") or source.get("date") != original.get("date"):
            errors.append(f"{source_id} predecessor identity mismatch")
        alias = original.get("canonical_alias")
        if alias and (alias not in source.get("canonical_aliases", []) or alias not in identity.get("canonical_aliases", [])):
            errors.append(f"{source_id} canonical alias mismatch")
        scope = original.get("scope")
        if scope and (source.get("registered_scope") != scope or identity.get("registered_scope") != scope):
            errors.append(f"{source_id} registered scope mismatch")
        if registration.get("active_predecessor_source_sequence") != sequence:
            errors.append(f"{status_id} predecessor sequence mismatch")
        if registration.get("active_predecessor") != "problems/theologico-political.yaml":
            errors.append(f"{status_id} active predecessor mismatch")
        if registration.get("corpus_source_id") != source_id:
            errors.append(f"{status_id} corpus source binding mismatch")
        if entry.get("certification") != "NOT_CERTIFIED" or state.get("certification") != "NOT_CERTIFIED" or termination.get("certification") != "NOT_CERTIFIED":
            errors.append(f"{status_id} must remain NOT_CERTIFIED")
        if termination.get("successor_effect") != "NONE":
            errors.append(f"{status_id} may not affect successor activation")

        completed = COMPLETED_TP_ITEMS.get(source_id)
        if completed:
            _validate_completed_item(registry, source, entry, status, completed, errors)
        else:
            if state.get("reviewed_witness") != "NOT_YET_REGISTERED":
                errors.append(f"{status_id} must remain without reviewed witness")
            if state.get("independent_sequential_study") != "NOT_YET_COMPLETED":
                errors.append(f"{status_id} study must remain incomplete")
            if termination.get("reviewed_witness_state") != "MISSING" or termination.get("study_state") != "INCOMPLETE":
                errors.append(f"{status_id} missing state mismatch")
            publication = status.get("publication_and_witness_condition", {})
            if publication.get("fingerprint") != "NOT_AVAILABLE" or publication.get("locator_reproducibility") != "INCOMPLETE":
                errors.append(f"{status_id} may not claim witness fingerprint or locators")


def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP_LEVEL - set(registry))
    if missing:
        errors.append("corpus registry missing sections: " + ", ".join(missing))

    identity = registry.get("identity", {})
    if identity.get("id") != "STRAUSS-CORPUS-INDEX-001":
        errors.append("corpus registry identity.id mismatch")
    if identity.get("version") != "1.7.0":
        errors.append("corpus registry identity.version must be 1.7.0")
    status = registry.get("status", {})
    if status.get("registry_scope") != "EXHAUSTIVE_FOR_CURRENT_COMMITTED_SOURCE_AND_STUDY_STATE":
        errors.append("corpus registry must state bounded current-state exhaustiveness")
    if status.get("corpus_completion") != "INCOMPLETE_OPEN_CORPUS" or status.get("certification") != "NOT_CERTIFIED":
        errors.append("corpus registry must remain incomplete and NOT_CERTIFIED")

    source_entities = registry.get("source_entities", [])
    witnesses = registry.get("reviewed_witnesses", [])
    statuses = registry.get("source_status_records", [])
    studies = registry.get("study_records", [])
    problem_registries = registry.get("problem_witness_registries", [])
    gaps = registry.get("corpus_gaps", [])

    source_ids = _unique_ids(source_entities, "source_id", "source_entities", errors)
    witness_ids = _unique_ids(witnesses, "witness_id", "reviewed_witnesses", errors)
    status_ids = _unique_ids(statuses, "status_id", "source_status_records", errors)
    study_ids = _unique_ids(studies, "study_id", "study_records", errors)
    gap_ids = _unique_ids(gaps, "gap_id", "corpus_gaps", errors)

    for label, actual, expected in (
        ("source entities", len(source_ids), 22),
        ("reviewed witnesses", len(witness_ids), 5),
        ("source-status records", len(status_ids), 22),
        ("study records", len(study_ids), 9),
        ("corpus gaps", len(gap_ids), 7),
    ):
        if actual != expected:
            errors.append(f"expected {expected} {label}, found {actual}")

    for label, records in (("reviewed_witnesses", witnesses), ("source_status_records", statuses), ("study_records", studies)):
        if isinstance(records, list):
            for item in records:
                if isinstance(item, dict) and item.get("source_id") not in source_ids:
                    errors.append(f"{label} references unknown source_id {item.get('source_id')!r}")

    _check_paths(statuses if isinstance(statuses, list) else [], ("path",), errors)
    _check_paths(studies if isinstance(studies, list) else [], ("path",), errors)
    _check_paths(problem_registries if isinstance(problem_registries, list) else [], ("path",), errors)

    actual_studies = _actual_study_tree_paths()
    registered_studies = _registered_study_paths(registry)
    if not BASE_REQUIRED_STUDY_PATHS.issubset(actual_studies):
        errors.append("required study records disappeared")
    if registered_studies != actual_studies:
        errors.append(f"study tree coverage mismatch: unregistered={sorted(actual_studies - registered_studies)!r}, stale={sorted(registered_studies - actual_studies)!r}")

    if not isinstance(problem_registries, list) or [item.get("problem") for item in problem_registries] != CANONICAL_PROBLEMS:
        errors.append("problem witness registry order mismatch")

    predecessor = load_yaml(TP_PREDECESSOR_PATH)
    if not TP_PRESERVED_PATH.exists() or TP_PREDECESSOR_PATH.read_bytes() != TP_PRESERVED_PATH.read_bytes():
        errors.append("Theologico-Political active predecessor does not match preserved copy")
    predecessor_sources = predecessor.get("documentary_source_basis", {}).get("sources", [])
    if not isinstance(predecessor_sources, list) or len(predecessor_sources) != 19:
        errors.append("Theologico-Political predecessor must contain 19 source records")
    else:
        _validate_tp_sources_and_statuses(registry, predecessor_sources, errors)

    _validate_collection_fingerprint(registry, "CORPUS-WIT-001", "studies/studies-in-platonic-political-philosophy/source-status.yaml", "reviewed_witness", "SPPP", errors)
    _validate_collection_fingerprint(registry, "CORPUS-WIT-003", "studies/socrates-and-aristophanes/source-status.yaml", "reviewed_witness", "Socrates and Aristophanes", errors)

    tp_entities = [item for item in source_entities if isinstance(item, dict) and _tp_sequence_from_source_id(str(item.get("source_id", ""))) is not None]
    coverage = registry.get("coverage", {})
    expected_coverage = {
        "source_entities_registered": len(source_ids),
        "reviewed_witnesses_registered": len(witness_ids),
        "source_status_records_registered": len(status_ids),
        "study_records_registered": len(study_ids),
        "problem_witness_registries_registered": len(problem_registries),
        "theologico_political_predecessor_sources_registered": len(tp_entities),
        "theologico_political_item_level_statuses_registered": 19,
        "theologico_political_reviewed_item_witnesses_registered": 2,
        "theologico_political_independent_item_studies_registered": 2,
        "current_studies_tree_yaml_records_accounted_for": len(actual_studies),
        "exhaustive_within_declared_scope": True,
    }
    for field, expected in expected_coverage.items():
        if coverage.get(field) != expected:
            errors.append(f"coverage.{field} mismatch: expected {expected!r}, found {coverage.get(field)!r}")

    termination = registry.get("termination", {})
    if termination.get("registry_state") != "COMPLETE_FOR_CURRENT_COMMITTED_SOURCE_AND_STUDY_STATE":
        errors.append("registry termination state mismatch")
    if termination.get("theologico_political_identity_registration_state") != "COMPLETE_19_OF_19":
        errors.append("TP identity state mismatch")
    if termination.get("theologico_political_reviewed_witness_state") != "INCOMPLETE_2_OF_19":
        errors.append("TP reviewed-witness state must be INCOMPLETE_2_OF_19")
    if termination.get("theologico_political_independent_study_state") != "INCOMPLETE_2_OF_19":
        errors.append("TP study state must be INCOMPLETE_2_OF_19")
    if termination.get("corpus_state") != "OPEN_AND_MATERIALLY_INCOMPLETE" or termination.get("certification") != "NOT_CERTIFIED":
        errors.append("registry termination must remain open, incomplete, and noncertified")
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
        "non_effects": ["no source-text admission", "no doctrinal certification", "no witness ranking as truth", "no migration certification", "no successor activation", "no Assembly authority"],
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
        print("Typed corpus registry validation passed for the current committed source and study state; corpus remains open, materially incomplete, and not certified.")
        return 0
    print(json.dumps(build_registry_context(), indent=2 if args.pretty else None, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
