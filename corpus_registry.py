#!/usr/bin/env python3
"""Validate and load the typed Strauss corpus registry.

Passing validation establishes only bounded current-state integrity. It does not admit
source text, certify doctrine, complete the corpus, execute migration, activate successor
problems, displace predecessors, or confer Assembly authority.
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
    "studies/theologico-political/introductory-essay-hermann-cohen-religion-of-reason/source-status.yaml",
    "studies/theologico-political/introductory-essay-hermann-cohen-religion-of-reason/reviewed-witness.yaml",
    "studies/theologico-political/introductory-essay-hermann-cohen-religion-of-reason/sequential-reconstruction.yaml",
    "studies/theologico-political/review-talmon-nature-of-jewish-history/source-status.yaml",
    "studies/theologico-political/review-talmon-nature-of-jewish-history/reviewed-witness.yaml",
    "studies/theologico-political/review-talmon-nature-of-jewish-history/sequential-reconstruction.yaml",
    "studies/theologico-political/preface-to-spinozas-critique-of-religion/reviewed-witness.yaml",
    "studies/theologico-political/preface-to-spinozas-critique-of-religion/sequential-reconstruction.yaml",
    "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/source-status.yaml",
    "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/reviewed-witness.yaml",
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

COMPLETE_TP_ITEMS: dict[str, dict[str, Any]] = {
    "CORPUS-SRC-102": {
        "status_id": "CORPUS-STATUS-102",
        "witness_id": "CORPUS-WIT-102",
        "study_id": "CORPUS-STUDY-011",
        "internal_study_id": "SPINOZA-PREFACE-STUDY-001",
        "study_path": (
            "studies/theologico-political/preface-to-spinozas-critique-of-religion/"
            "sequential-reconstruction.yaml"
        ),
        "witness_record_path": (
            "studies/theologico-political/preface-to-spinozas-critique-of-religion/"
            "reviewed-witness.yaml"
        ),
        "printed_page_range": {"start": 137, "end": 180},
        "pdf_page_range_one_based": "PENDING_DIRECT_OFFSET_VERIFICATION",
        "reading_state": "COMPLETE_FOR_QUALIFIED_1997_PLATFORM_REFERENCE_WITNESS",
        "platform_reference": True,
        "platform_object_identifier": "file_0000000073c081fd9fb65f9ea7552cde",
    },
    "CORPUS-SRC-105": {
        "status_id": "CORPUS-STATUS-105",
        "witness_id": "CORPUS-WIT-105",
        "study_id": "CORPUS-STUDY-009",
        "internal_study_id": "COHEN-STUDY-001",
        "study_path": (
            "studies/theologico-political/"
            "introductory-essay-hermann-cohen-religion-of-reason/"
            "sequential-reconstruction.yaml"
        ),
        "witness_record_path": (
            "studies/theologico-political/"
            "introductory-essay-hermann-cohen-religion-of-reason/"
            "reviewed-witness.yaml"
        ),
        "printed_page_range": {"start": 233, "end": 247},
        "pdf_page_range_one_based": {"start": 237, "end": 251},
        "reading_state": "COMPLETE_FOR_REVIEWED_1983_COLLECTED_WITNESS",
        "platform_reference": False,
    },
    "CORPUS-SRC-109": {
        "status_id": "CORPUS-STATUS-109",
        "witness_id": "CORPUS-WIT-109",
        "study_id": "CORPUS-STUDY-008",
        "internal_study_id": "JA-STUDY-001",
        "study_path": "studies/theologico-political/jerusalem-and-athens/sequential-reconstruction.yaml",
        "witness_record_path": None,
        "printed_page_range": {"start": 147, "end": 173},
        "pdf_page_range_one_based": {"start": 151, "end": 177},
        "reading_state": "COMPLETE_FOR_REVIEWED_1983_COLLECTED_WITNESS",
        "platform_reference": False,
    },
    "CORPUS-SRC-111": {
        "status_id": "CORPUS-STATUS-111",
        "witness_id": "CORPUS-WIT-111",
        "study_id": "CORPUS-STUDY-010",
        "internal_study_id": "TALMON-STUDY-001",
        "study_path": (
            "studies/theologico-political/review-talmon-nature-of-jewish-history/"
            "sequential-reconstruction.yaml"
        ),
        "witness_record_path": (
            "studies/theologico-political/review-talmon-nature-of-jewish-history/"
            "reviewed-witness.yaml"
        ),
        "printed_page_range": {"start": 232, "end": 232},
        "pdf_page_range_one_based": {"start": 236, "end": 236},
        "reading_state": "COMPLETE_FOR_REVIEWED_1983_COLLECTED_WITNESS",
        "platform_reference": False,
    },
}

WITNESS_ONLY_TP_ITEMS: dict[str, dict[str, Any]] = {
    "CORPUS-SRC-103": {
        "status_id": "CORPUS-STATUS-103",
        "witness_id": "CORPUS-WIT-103",
        "witness_record_path": (
            "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/"
            "reviewed-witness.yaml"
        ),
        "printed_page_range": {"start": 181, "end": 233},
        "pdf_page_range_one_based": {"start": 200, "end": 252},
        "container_sha256": "43e98521c28a9ef8ede1eb7a6507d8ee78d605d0a531624d5dd20075220bda66",
        "container_file_size_bytes": 39287307,
        "container_page_count": 526,
    },
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
        (record for record in records if isinstance(record, dict) and record.get(field) == value),
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
            if not _resolve(value).is_file():
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
    paths.update(
        item.get("witness_record_path")
        for item in registry.get("reviewed_witnesses", [])
        if isinstance(item, dict) and isinstance(item.get("witness_record_path"), str)
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


def _validate_completed_tp_item(
    registry: dict[str, Any],
    source: dict[str, Any],
    status_record: dict[str, Any],
    source_id: str,
    errors: list[str],
) -> None:
    spec = COMPLETE_TP_ITEMS[source_id]
    witness_id = spec["witness_id"]
    study_id = spec["study_id"]
    internal_study_id = spec["internal_study_id"]
    state = status_record.get("status", {})
    termination = status_record.get("termination", {})

    if state.get("reviewed_witness") != witness_id:
        errors.append(f"{spec['status_id']} must retain {witness_id}")
    if state.get("independent_sequential_study") != internal_study_id:
        errors.append(f"{spec['status_id']} must record {internal_study_id}")
    if source.get("reviewed_witnesses") != [witness_id]:
        errors.append(f"{source_id} must list {witness_id}")
    if source.get("study_records") != [study_id]:
        errors.append(f"{source_id} must list {study_id}")

    witness = _find_record(registry.get("reviewed_witnesses", []), "witness_id", witness_id)
    if not isinstance(witness, dict):
        errors.append(f"{witness_id} is missing")
    else:
        if witness.get("source_id") != source_id:
            errors.append(f"{witness_id} source binding mismatch")
        for field in ("printed_page_range", "pdf_page_range_one_based"):
            if witness.get(field) != spec[field]:
                errors.append(f"{witness_id} {field} mismatch")
        if spec["platform_reference"]:
            if witness.get("witness_class") != "PLATFORM_REFERENCE_WITNESS":
                errors.append(f"{witness_id} must retain platform-reference witness class")
            if witness.get("platform_object_identifier") != spec["platform_object_identifier"]:
                errors.append(f"{witness_id} platform object identifier mismatch")
            if witness.get("byte_custody_state") != "NOT_EXPOSED_TO_REPOSITORY":
                errors.append(f"{witness_id} must preserve absent repository byte custody")
            if witness.get("sha256_state") != "UNAVAILABLE_WITH_REASON_PRESERVED":
                errors.append(f"{witness_id} may not fabricate cryptographic identity")

    study = _find_record(registry.get("study_records", []), "study_id", study_id)
    if not isinstance(study, dict):
        errors.append(f"{study_id} is missing")
    elif study.get("path") != spec["study_path"]:
        errors.append(f"{study_id} path mismatch")

    reviewed = status_record.get("reviewed_witness", {})
    if not isinstance(reviewed, dict) or reviewed.get("witness_id") != witness_id:
        errors.append(f"{spec['status_id']} reviewed_witness block mismatch")
    elif isinstance(witness, dict):
        fields = ("printed_page_range", "pdf_page_range_one_based")
        if spec["platform_reference"]:
            fields += ("platform_object_identifier",)
        else:
            fields += ("container_sha256",)
        for field in fields:
            if witness.get(field) != reviewed.get(field):
                errors.append(f"{witness_id} {field} mismatch between registry and status")

    expected_witness_state = (
        "REGISTERED_QUALIFIED_PLATFORM_REFERENCE" if spec["platform_reference"] else "REGISTERED"
    )
    if termination.get("reviewed_witness_state") != expected_witness_state:
        errors.append(f"{spec['status_id']} reviewed witness termination mismatch")
    if termination.get("study_state") != "COMPLETE_PROVISIONAL":
        errors.append(f"{spec['status_id']} study_state must be COMPLETE_PROVISIONAL")
    if termination.get("study_id") != internal_study_id:
        errors.append(f"{spec['status_id']} termination study id mismatch")
    if termination.get("independent_corroboration") != "INCOMPLETE":
        errors.append(f"{spec['status_id']} must preserve incomplete independent corroboration")
    if termination.get("certification") != "NOT_CERTIFIED":
        errors.append(f"{spec['status_id']} must remain NOT_CERTIFIED")
    if termination.get("successor_effect") != "NONE":
        errors.append(f"{spec['status_id']} may not affect successor activation")

    study_record = load_yaml(_resolve(spec["study_path"]))
    if study_record.get("identity", {}).get("id") != internal_study_id:
        errors.append(f"{study_id} internal study identity mismatch")
    if study_record.get("termination", {}).get("reading_state") != spec["reading_state"]:
        errors.append(f"{study_id} reading state mismatch")
    if study_record.get("status", {}).get("certification") != "NOT_CERTIFIED":
        errors.append(f"{study_id} must remain NOT_CERTIFIED")
    if study_record.get("termination", {}).get("successor_effect") not in (None, "NONE"):
        errors.append(f"{study_id} may not affect successor activation")

    witness_record_path = spec.get("witness_record_path")
    if witness_record_path:
        if not isinstance(witness, dict):
            errors.append(f"{witness_id} witness record cannot be validated without registry entry")
            return
        if witness.get("witness_record_path") != witness_record_path:
            errors.append(f"{witness_id} witness record path mismatch")
        witness_record = load_yaml(_resolve(witness_record_path))
        if witness_record.get("identity", {}).get("witness_id") != witness_id:
            errors.append(f"{witness_id} record identity mismatch")
        if witness_record.get("status", {}).get("certification") != "NOT_CERTIFIED":
            errors.append(f"{witness_id} record must remain NOT_CERTIFIED")
        if witness_record.get("status", {}).get("successor_effect") != "NONE":
            errors.append(f"{witness_id} record must preserve successor_effect NONE")
        if spec["platform_reference"]:
            if (
                witness_record.get("byte_identity", {}).get("sha256_state")
                != "UNAVAILABLE_WITH_REASON_PRESERVED"
            ):
                errors.append(f"{witness_id} record must preserve missing digest")
            if witness_record.get("termination", {}).get("study_state") != "INCOMPLETE":
                errors.append(
                    f"{witness_id} registration record must remain witness-only and may not claim study completion"
                )


def _validate_witness_only_tp_item(
    registry: dict[str, Any],
    source: dict[str, Any],
    status_record: dict[str, Any],
    source_id: str,
    errors: list[str],
) -> None:
    spec = WITNESS_ONLY_TP_ITEMS[source_id]
    witness_id = spec["witness_id"]
    status_id = spec["status_id"]
    state = status_record.get("status", {})
    termination = status_record.get("termination", {})

    if state.get("reviewed_witness") != witness_id:
        errors.append(f"{status_id} must record {witness_id}")
    if state.get("independent_sequential_study") != "NOT_YET_COMPLETED":
        errors.append(f"{status_id} independent study must remain incomplete")
    if source.get("reviewed_witnesses") != [witness_id]:
        errors.append(f"{source_id} must list {witness_id}")
    if source.get("study_records") not in (None, []):
        errors.append(f"{source_id} may not list a completed study before reconstruction")

    witness = _find_record(registry.get("reviewed_witnesses", []), "witness_id", witness_id)
    if not isinstance(witness, dict):
        errors.append(f"{witness_id} is missing")
        return
    if witness.get("source_id") != source_id:
        errors.append(f"{witness_id} source binding mismatch")
    for field in (
        "printed_page_range",
        "pdf_page_range_one_based",
        "container_sha256",
        "container_file_size_bytes",
        "container_page_count",
    ):
        if witness.get(field) != spec[field]:
            errors.append(f"{witness_id} {field} mismatch")
    if witness.get("witness_record_path") != spec["witness_record_path"]:
        errors.append(f"{witness_id} witness record path mismatch")

    reviewed = status_record.get("reviewed_witness", {})
    if not isinstance(reviewed, dict) or reviewed.get("witness_id") != witness_id:
        errors.append(f"{status_id} reviewed_witness block mismatch")
    else:
        for field in (
            "printed_page_range",
            "pdf_page_range_one_based",
            "container_sha256",
            "container_file_size_bytes",
        ):
            if reviewed.get(field) != witness.get(field):
                errors.append(f"{witness_id} {field} mismatch between registry and status")

    publication = status_record.get("publication_and_witness_condition", {})
    fingerprint = publication.get("fingerprint", {})
    if not isinstance(fingerprint, dict) or fingerprint.get("value") != spec["container_sha256"]:
        errors.append(f"{status_id} fingerprint mismatch")
    if publication.get("file_size_bytes") != spec["container_file_size_bytes"]:
        errors.append(f"{status_id} file-size mismatch")
    if publication.get("container_page_count") != spec["container_page_count"]:
        errors.append(f"{status_id} page-count mismatch")
    if publication.get("original_1948_journal_copy_comparison") != "PENDING":
        errors.append(f"{status_id} must preserve pending original-1948 comparison")

    if termination.get("reviewed_witness_state") != "REGISTERED":
        errors.append(f"{status_id} reviewed witness state must be REGISTERED")
    if termination.get("study_state") != "INCOMPLETE":
        errors.append(f"{status_id} study state must remain INCOMPLETE")
    if termination.get("independent_corroboration") != "INCOMPLETE":
        errors.append(f"{status_id} independent corroboration must remain INCOMPLETE")
    if termination.get("original_edition_comparison") != "PENDING":
        errors.append(f"{status_id} original edition comparison must remain PENDING")
    if termination.get("certification") != "NOT_CERTIFIED":
        errors.append(f"{status_id} must remain NOT_CERTIFIED")
    if termination.get("successor_effect") != "NONE":
        errors.append(f"{status_id} may not affect successor activation")

    witness_record = load_yaml(_resolve(spec["witness_record_path"]))
    if witness_record.get("identity", {}).get("witness_id") != witness_id:
        errors.append(f"{witness_id} record identity mismatch")
    if witness_record.get("status", {}).get("certification") != "NOT_CERTIFIED":
        errors.append(f"{witness_id} record must remain NOT_CERTIFIED")
    if witness_record.get("termination", {}).get("study_state") != "INCOMPLETE":
        errors.append(f"{witness_id} witness record may not claim study completion")
    if witness_record.get("termination", {}).get("successor_effect") != "NONE":
        errors.append(f"{witness_id} record must preserve successor_effect NONE")


def _validate_tp_sources_and_statuses(
    registry: dict[str, Any], predecessor_sources: list[dict[str, Any]], errors: list[str]
) -> None:
    source_entities = registry.get("source_entities", [])
    status_entries = registry.get("source_status_records", [])
    tp_entries = [
        entry
        for entry in status_entries
        if isinstance(entry, dict)
        and isinstance(entry.get("source_id"), str)
        and _tp_sequence_from_source_id(entry["source_id"]) is not None
    ]
    if len(tp_entries) != 19:
        errors.append(f"expected 19 Theologico-Political item statuses, found {len(tp_entries)}")

    for sequence, original in enumerate(predecessor_sources, start=1):
        source_id = f"CORPUS-SRC-{100 + sequence:03d}"
        status_id = f"CORPUS-STATUS-{100 + sequence:03d}"
        source = _find_record(source_entities, "source_id", source_id)
        entry = _find_record(status_entries, "status_id", status_id)
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
        status_record = load_yaml(_resolve(path_value))
        identity = status_record.get("identity", {})
        state = status_record.get("status", {})
        registration = status_record.get("registration_basis", {})
        termination = status_record.get("termination", {})

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

        if source_id in COMPLETE_TP_ITEMS:
            _validate_completed_tp_item(registry, source, status_record, source_id, errors)
        elif source_id in WITNESS_ONLY_TP_ITEMS:
            _validate_witness_only_tp_item(registry, source, status_record, source_id, errors)
        else:
            if state.get("reviewed_witness") != "NOT_YET_REGISTERED":
                errors.append(f"{status_id} must remain without a reviewed witness")
            if state.get("independent_sequential_study") != "NOT_YET_COMPLETED":
                errors.append(f"{status_id} independent study must remain incomplete")
            if termination.get("study_state") != "INCOMPLETE":
                errors.append(f"{status_id} study state must remain INCOMPLETE")
            publication = status_record.get("publication_and_witness_condition", {})
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
    if identity.get("version") != "1.11.0":
        errors.append("corpus registry identity.version must be 1.11.0")

    status = registry.get("status", {})
    if status.get("registry_scope") != "EXHAUSTIVE_FOR_CURRENT_COMMITTED_SOURCE_AND_STUDY_STATE":
        errors.append("corpus registry must state bounded current-state exhaustiveness")
    if status.get("corpus_completion") != "INCOMPLETE_OPEN_CORPUS":
        errors.append("corpus registry must remain an incomplete open corpus")
    if status.get("certification") != "NOT_CERTIFIED":
        errors.append("corpus registry must remain NOT_CERTIFIED")

    source_entities = registry.get("source_entities", [])
    witnesses = registry.get("reviewed_witnesses", [])
    status_records = registry.get("source_status_records", [])
    studies = registry.get("study_records", [])
    problem_registries = registry.get("problem_witness_registries", [])
    gaps = registry.get("corpus_gaps", [])

    source_ids = _unique_ids(source_entities, "source_id", "source_entities", errors)
    witness_ids = _unique_ids(witnesses, "witness_id", "reviewed_witnesses", errors)
    status_ids = _unique_ids(status_records, "status_id", "source_status_records", errors)
    study_ids = _unique_ids(studies, "study_id", "study_records", errors)
    gap_ids = _unique_ids(gaps, "gap_id", "corpus_gaps", errors)

    expected_counts = {
        "source entities": (len(source_ids), 22),
        "reviewed witnesses": (len(witness_ids), 8),
        "source-status records": (len(status_ids), 22),
        "study records": (len(study_ids), 11),
        "corpus gaps": (len(gap_ids), 7),
    }
    for label, (actual, expected) in expected_counts.items():
        if actual != expected:
            errors.append(f"expected {expected} {label}, found {actual}")

    for label, records in (
        ("reviewed_witnesses", witnesses),
        ("source_status_records", status_records),
        ("study_records", studies),
    ):
        if isinstance(records, list):
            for item in records:
                if isinstance(item, dict) and item.get("source_id") not in source_ids:
                    errors.append(f"{label} references unknown source_id {item.get('source_id')!r}")

    _check_paths(status_records if isinstance(status_records, list) else [], ("path",), errors)
    _check_paths(studies if isinstance(studies, list) else [], ("path",), errors)
    _check_paths(witnesses if isinstance(witnesses, list) else [], ("witness_record_path",), errors)
    _check_paths(problem_registries if isinstance(problem_registries, list) else [], ("path",), errors)

    actual_studies = _actual_study_tree_paths()
    registered_studies = _registered_study_paths(registry)
    missing_baseline = sorted(BASE_REQUIRED_STUDY_PATHS - actual_studies)
    if missing_baseline:
        errors.append("required study records disappeared: " + ", ".join(missing_baseline))
    if registered_studies != actual_studies:
        errors.append(
            "registered study, witness-record, and source-status paths do not exhaust the studies tree: "
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
    if not TP_PRESERVED_PATH.is_file() or TP_PREDECESSOR_PATH.read_bytes() != TP_PRESERVED_PATH.read_bytes():
        errors.append("Theologico-Political active predecessor does not match preserved copy")
    predecessor_sources = predecessor.get("documentary_source_basis", {}).get("sources", [])
    if not isinstance(predecessor_sources, list) or len(predecessor_sources) != 19:
        errors.append("Theologico-Political predecessor must contain 19 source records")
    else:
        _validate_tp_sources_and_statuses(registry, predecessor_sources, errors)

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
        "theologico_political_reviewed_item_witnesses_registered": 5,
        "theologico_political_independent_item_studies_registered": 4,
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
    if termination.get("theologico_political_identity_registration_state") != "COMPLETE_19_OF_19":
        errors.append("TP identity registration must remain COMPLETE_19_OF_19")
    if termination.get("theologico_political_reviewed_witness_state") != "INCOMPLETE_5_OF_19":
        errors.append("TP reviewed-witness state must be INCOMPLETE_5_OF_19")
    if termination.get("theologico_political_independent_study_state") != "INCOMPLETE_4_OF_19":
        errors.append("TP independent-study state must be INCOMPLETE_4_OF_19")
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
    print(json.dumps(build_registry_context(), indent=2 if args.pretty else None, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
