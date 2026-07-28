#!/usr/bin/env python3
"""Validate and load the typed Strauss findings registry.

The registry indexes committed findings-bearing records by reference. It preserves
record-local evidence classes, uncertainty, dissent, migration state, jurisdiction,
and provenance. It does not normalize every proposition, certify doctrine, or activate
successors.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent
REGISTRY_PATH = ROOT / "findings" / "index.yaml"
CORPUS_PATH = ROOT / "corpus" / "index.yaml"
PROBLEM_REGISTRY_PATH = ROOT / "problems" / "registry.yaml"
TP_ACTIVE_PATH = ROOT / "problems" / "theologico-political.yaml"
TP_PRESERVED_PATH = (
    ROOT
    / "history"
    / "foundational-problems"
    / "theologico-political"
    / "STR-PROBLEM-002-v1.1-active-predecessor.yaml"
)

EXPECTED_SYNTHESIS_PATHS = {
    "problems/nomos-vs-physis/synthesis/studies-in-platonic-political-philosophy.yaml",
    "problems/philosophy-vs-poetry/synthesis/socrates-and-aristophanes.yaml",
    "problems/philosophy-vs-poetry/synthesis/studies-in-platonic-political-philosophy.yaml",
    "problems/theory-vs-practice/synthesis/studies-in-platonic-political-philosophy.yaml",
    "problems/theologico-political/synthesis/predecessor-v1.1-reconstruction.yaml",
    "problems/theologico-political/synthesis/studies-in-platonic-political-philosophy.yaml",
    "problems/theologico-political/synthesis/jerusalem-and-athens.yaml",
    "problems/theologico-political/synthesis/hermann-cohen-religion-of-reason.yaml",
    "problems/theologico-political/synthesis/talmon-nature-of-jewish-history.yaml",
    "problems/theologico-political/synthesis/preface-to-spinozas-critique-of-religion.yaml",
    "problems/athens-vs-jerusalem/synthesis/studies-in-platonic-political-philosophy.yaml",
    "problems/athens-vs-jerusalem/synthesis/jerusalem-and-athens.yaml",
    "problems/athens-vs-jerusalem/synthesis/hermann-cohen-religion-of-reason.yaml",
    "problems/athens-vs-jerusalem/synthesis/talmon-nature-of-jewish-history.yaml",
    "problems/athens-vs-jerusalem/synthesis/preface-to-spinozas-critique-of-religion.yaml",
    "problems/theologico-political/synthesis/how-to-study-spinozas-theologico-political-treatise.yaml",
    "problems/wise-vs-vulgar/synthesis/how-to-study-spinozas-theologico-political-treatise.yaml",
    "problems/wise-vs-vulgar/synthesis/plato-apology.yaml",
    "problems/wise-vs-vulgar/synthesis/studies-in-platonic-political-philosophy.yaml",
    "problems/ancients-vs-moderns/synthesis/studies-in-platonic-political-philosophy.yaml",
    "problems/ancients-vs-moderns/synthesis/hermann-cohen-religion-of-reason.yaml",
    "problems/ancients-vs-moderns/synthesis/talmon-nature-of-jewish-history.yaml",
    "problems/ancients-vs-moderns/synthesis/preface-to-spinozas-critique-of-religion.yaml",
}

EXPECTED_TRANSACTION_PATHS = {
    "migrations/foundational-problems-v2/transactions/wise-vs-vulgar-v0.2.yaml",
    "migrations/foundational-problems-v2/transactions/theologico-political-sppp-study-001.yaml",
    "migrations/foundational-problems-v2/transactions/theologico-political-v1.1.yaml",
}

REQUIRED_TOP_LEVEL = {
    "identity",
    "status",
    "purpose",
    "scope_rule",
    "finding_unit_rule",
    "identifier_rules",
    "finding_sets",
    "indexes",
    "coverage",
    "proposition_kinds",
    "preservation_rules",
    "findings_gaps",
    "validation_rules",
    "termination",
}

REFERENCE_FIELDS = {
    "derived_from",
    "derived_local_syntheses",
    "derivation_targets",
    "migration_targets",
    "repository_artifact_bindings",
}

DIRECT_SOURCE_KEYS = [
    "CORPUS-SRC-001",
    "CORPUS-SRC-002",
    "CORPUS-SRC-003",
    "CORPUS-SRC-102",
    "CORPUS-SRC-103",
    "CORPUS-SRC-105",
    "CORPUS-SRC-111",
]

SOURCE_STUDY_CONTRACTS = {
    "FINDSET-008": {
        "source_id": "CORPUS-SRC-109",
        "local_syntheses": ["FINDSET-111", "FINDSET-112"],
        "problem_bindings": {
            "FINDSET-111": "theologico-political",
            "FINDSET-112": "athens-vs-jerusalem",
        },
        "required_limits": {
            "original_edition_comparison": "PENDING",
            "independent_corroboration": "INCOMPLETE",
        },
    },
    "FINDSET-009": {
        "source_id": "CORPUS-SRC-105",
        "local_syntheses": ["FINDSET-113", "FINDSET-114", "FINDSET-115"],
        "problem_bindings": {
            "FINDSET-113": "theologico-political",
            "FINDSET-114": "athens-vs-jerusalem",
            "FINDSET-115": "ancients-vs-moderns",
        },
        "required_limits": {
            "original_edition_comparison": "PENDING",
            "independent_corroboration": "INCOMPLETE",
        },
    },
    "FINDSET-010": {
        "source_id": "CORPUS-SRC-111",
        "local_syntheses": ["FINDSET-116", "FINDSET-117", "FINDSET-118"],
        "problem_bindings": {
            "FINDSET-116": "theologico-political",
            "FINDSET-117": "athens-vs-jerusalem",
            "FINDSET-118": "ancients-vs-moderns",
        },
        "required_limits": {
            "original_edition_comparison": "PENDING",
            "reviewed_work_reconstruction": "INCOMPLETE",
            "independent_corroboration": "INCOMPLETE",
        },
    },
    "FINDSET-011": {
        "source_id": "CORPUS-SRC-102",
        "local_syntheses": ["FINDSET-119", "FINDSET-120", "FINDSET-121"],
        "problem_bindings": {
            "FINDSET-119": "theologico-political",
            "FINDSET-120": "athens-vs-jerusalem",
            "FINDSET-121": "ancients-vs-moderns",
        },
        "required_limits": {
            "witness_id": "CORPUS-WIT-102",
            "original_1965_edition_comparison": "PENDING",
            "authorial_1968_reprint_comparison": "PENDING",
            "byte_identity_state": "UNAVAILABLE_WITH_REASON_PRESERVED",
            "independent_corroboration": "INCOMPLETE",
        },
    },
    "FINDSET-012": {
        "source_id": "CORPUS-SRC-103",
        "local_syntheses": ["FINDSET-122", "FINDSET-123"],
        "problem_bindings": {"FINDSET-122": "theologico-political", "FINDSET-123": "wise-vs-vulgar"},
        "required_limits": {"witness_id": "CORPUS-WIT-103", "original_1948_journal_comparison": "PENDING", "independent_corroboration": "INCOMPLETE"},
    },
}


class FindingsRegistryError(RuntimeError):
    """Raised when the findings registry cannot be loaded or validated safely."""


def _resolve(relative_path: str) -> Path:
    path = (ROOT / relative_path).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError as exc:
        raise FindingsRegistryError(f"Path escapes repository root: {relative_path}") from exc
    return path


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise FindingsRegistryError(f"Cannot read {path.relative_to(ROOT)}: {exc}") from exc
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise FindingsRegistryError(f"Invalid YAML in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(data, dict):
        raise FindingsRegistryError(f"Expected a YAML mapping in {path.relative_to(ROOT)}")
    return data


def load_registry() -> dict[str, Any]:
    return load_yaml(REGISTRY_PATH)


def _unique_ids(records: Any, field: str, label: str, errors: list[str]) -> set[str]:
    if not isinstance(records, list):
        errors.append(f"{label} must be a list")
        return set()
    values: list[str] = []
    for position, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            errors.append(f"{label} item {position} must be a mapping")
            continue
        value = record.get(field)
        if not isinstance(value, str) or not value:
            errors.append(f"{label} item {position} missing {field}")
            continue
        values.append(value)
    if len(values) != len(set(values)):
        errors.append(f"{label} contains duplicate {field} values")
    return set(values)


def _actual_synthesis_paths() -> set[str]:
    return {
        str(path.relative_to(ROOT))
        for path in (ROOT / "problems").glob("*/synthesis/*.yaml")
        if path.is_file()
    }


def _actual_transaction_paths() -> set[str]:
    root = ROOT / "migrations" / "foundational-problems-v2" / "transactions"
    return {str(path.relative_to(ROOT)) for path in root.glob("*.yaml") if path.is_file()}


def _corpus_source_ids() -> set[str]:
    corpus = load_yaml(CORPUS_PATH)
    return {
        item.get("source_id")
        for item in corpus.get("source_entities", [])
        if isinstance(item, dict) and isinstance(item.get("source_id"), str)
    }


def _corpus_study_paths() -> set[str]:
    corpus = load_yaml(CORPUS_PATH)
    return {
        item.get("path")
        for item in corpus.get("study_records", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }


def _canonical_problem_keys() -> list[str]:
    registry = load_yaml(PROBLEM_REGISTRY_PATH)
    return [
        item.get("canonical_key")
        for item in registry.get("canonical_problems", [])
        if isinstance(item, dict)
    ]


def _certification_is_prohibited(value: Any) -> bool:
    return isinstance(value, str) and value in {"CERTIFIED", "ACTIVE_CERTIFIED"}


def _record_claims_certification(record: dict[str, Any]) -> bool:
    if _certification_is_prohibited(record.get("certification")):
        return True
    status = record.get("status")
    return isinstance(status, dict) and _certification_is_prohibited(status.get("certification"))


def _derived_problem_index(finding_sets: list[dict[str, Any]]) -> dict[str, list[str]]:
    result = {key: [] for key in _canonical_problem_keys()}
    for item in finding_sets:
        for key in item.get("problem_bindings", []):
            if key in result:
                result[key].append(item["finding_set_id"])
    return result


def _derived_record_class_index(finding_sets: list[dict[str, Any]]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {
        "SOURCE_SPECIFIC_STUDY": [],
        "INTEGRATION_GOVERNANCE_RECORD": [],
        "PROBLEM_LOCAL_SYNTHESIS": [],
        "MIGRATION_TRANSACTION_LEDGER": [],
        "PRESERVED_FINDING_BASIS": [],
    }
    for item in finding_sets:
        record_class = item.get("record_class")
        if record_class in {
            "ACTIVE_PREDECESSOR_FINDING_BASIS",
            "ACCEPTED_MIGRATION_SOURCE_FINDING_BASIS",
        }:
            result["PRESERVED_FINDING_BASIS"].append(item["finding_set_id"])
        elif record_class in result:
            result[record_class].append(item["finding_set_id"])
    return result


def _derived_source_index(finding_sets: list[dict[str, Any]]) -> dict[str, list[str]]:
    result = {key: [] for key in DIRECT_SOURCE_KEYS}
    result["CORPUS-SRC-101-119"] = []
    predecessor_sources = {f"CORPUS-SRC-{number:03d}" for number in range(101, 120)}
    separately_indexed = {"CORPUS-SRC-102", "CORPUS-SRC-103", "CORPUS-SRC-105", "CORPUS-SRC-111"}
    for item in finding_sets:
        bindings = set(item.get("source_bindings", []))
        finding_id = item["finding_set_id"]
        for key in DIRECT_SOURCE_KEYS:
            if key in bindings:
                result[key].append(finding_id)
        if bindings & predecessor_sources and not (
            len(bindings) == 1 and next(iter(bindings)) in separately_indexed
        ):
            result["CORPUS-SRC-101-119"].append(finding_id)
    return result


def _validate_reference_fields(
    finding_sets: list[dict[str, Any]], finding_ids: set[str], errors: list[str]
) -> None:
    for item in finding_sets:
        finding_id = item.get("finding_set_id")
        for field in REFERENCE_FIELDS:
            value = item.get(field, [])
            if value is None:
                continue
            if not isinstance(value, list):
                errors.append(f"{finding_id}.{field} must be a list")
                continue
            unknown = sorted(set(value) - finding_ids)
            if unknown:
                errors.append(f"{finding_id}.{field} references unknown finding sets: {unknown!r}")
        classification_ledger = item.get("classification_ledger")
        if classification_ledger is not None and classification_ledger not in finding_ids:
            errors.append(
                f"{finding_id}.classification_ledger references unknown finding set "
                f"{classification_ledger!r}"
            )


def _validate_source_study_derivations(
    finding_sets: list[dict[str, Any]], errors: list[str]
) -> None:
    by_id = {item.get("finding_set_id"): item for item in finding_sets}
    for study_id, contract in SOURCE_STUDY_CONTRACTS.items():
        study = by_id.get(study_id)
        if not isinstance(study, dict):
            errors.append(f"{study_id} is missing")
            continue
        if study.get("source_bindings") != [contract["source_id"]]:
            errors.append(f"{study_id} source binding mismatch")
        if study.get("derived_local_syntheses") != contract["local_syntheses"]:
            errors.append(f"{study_id} local synthesis derivation mismatch")
        if study.get("certification") != "NOT_CERTIFIED":
            errors.append(f"{study_id} must remain NOT_CERTIFIED")
        if study.get("successor_effect") not in {None, "NONE"}:
            errors.append(f"{study_id} may not affect successor activation")
        for field, expected in contract["required_limits"].items():
            if study.get(field) != expected:
                errors.append(f"{study_id} must preserve {field}={expected!r}")

        for finding_id, expected_problem in contract["problem_bindings"].items():
            synthesis = by_id.get(finding_id)
            if not isinstance(synthesis, dict):
                errors.append(f"{finding_id} is missing")
                continue
            if synthesis.get("source_bindings") != [contract["source_id"]]:
                errors.append(f"{finding_id} source binding mismatch")
            if synthesis.get("problem_bindings") != [expected_problem]:
                errors.append(f"{finding_id} problem binding mismatch")
            if synthesis.get("derived_from") != [study_id]:
                errors.append(f"{finding_id} must derive only from {study_id}")
            if synthesis.get("successor_effect") != "NONE":
                errors.append(f"{finding_id} must preserve successor_effect NONE")
            if synthesis.get("certification") != "NOT_CERTIFIED":
                errors.append(f"{finding_id} must remain NOT_CERTIFIED")


def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP_LEVEL - set(registry))
    if missing:
        errors.append("findings registry missing sections: " + ", ".join(missing))

    identity = registry.get("identity", {})
    if identity.get("id") != "STRAUSS-FINDINGS-INDEX-001":
        errors.append("findings registry identity.id mismatch")
    if identity.get("version") != "1.5.0":
        errors.append("findings registry identity.version must be 1.5.0")

    status = registry.get("status", {})
    if status.get("registry_scope") != "EXHAUSTIVE_FOR_CURRENT_COMMITTED_FINDINGS_RECORD_STATE":
        errors.append("findings registry must state bounded current-state exhaustiveness")
    if status.get("findings_completion") != "INCOMPLETE_OPEN_FINDINGS_STORE":
        errors.append("findings registry must remain an incomplete open findings store")
    if status.get("certification") != "NOT_CERTIFIED":
        errors.append("findings registry must remain NOT_CERTIFIED")

    finding_sets_raw = registry.get("finding_sets", [])
    finding_ids = _unique_ids(finding_sets_raw, "finding_set_id", "finding_sets", errors)
    gap_ids = _unique_ids(registry.get("findings_gaps", []), "gap_id", "findings_gaps", errors)
    finding_sets = [item for item in finding_sets_raw if isinstance(item, dict)]

    if len(finding_ids) != 40:
        errors.append(f"expected 40 finding sets, found {len(finding_ids)}")
    if len(gap_ids) != 6:
        errors.append(f"expected 6 findings gaps, found {len(gap_ids)}")

    source_ids = _corpus_source_ids()
    problem_keys = _canonical_problem_keys()
    if len(problem_keys) != 7:
        errors.append(f"expected seven canonical problem keys, found {problem_keys!r}")

    registered_paths: set[str] = set()
    for item in finding_sets:
        finding_id = item["finding_set_id"]
        path_value = item.get("path")
        if not isinstance(path_value, str) or not path_value:
            errors.append(f"{finding_id} missing path")
            continue
        if path_value in registered_paths:
            errors.append(f"findings path registered more than once: {path_value}")
        registered_paths.add(path_value)
        path = _resolve(path_value)
        if not path.is_file():
            errors.append(f"registered findings path does not resolve: {path_value}")
            continue
        record = load_yaml(path)
        if _record_claims_certification(record):
            errors.append(f"registered record claims prohibited certification: {path_value}")

        for field in ("preserved_path", "active_predecessor_path"):
            target = item.get(field)
            if target is not None and (
                not isinstance(target, str) or not _resolve(target).is_file()
            ):
                errors.append(f"{finding_id}.{field} does not resolve")

        bindings = item.get("source_bindings", [])
        if not isinstance(bindings, list):
            errors.append(f"{finding_id}.source_bindings must be a list")
        else:
            unknown_sources = sorted(set(bindings) - source_ids)
            if unknown_sources:
                errors.append(f"{finding_id} references unknown corpus sources: {unknown_sources!r}")

        problems = item.get("problem_bindings", [])
        if not isinstance(problems, list) or not problems:
            errors.append(f"{finding_id} must bind at least one canonical problem")
        else:
            unknown_problems = sorted(set(problems) - set(problem_keys))
            if unknown_problems:
                errors.append(f"{finding_id} references unknown problems: {unknown_problems!r}")

        if _certification_is_prohibited(item.get("certification")):
            errors.append(f"{finding_id} may not be certified by the registry")
        if item.get("successor_effect") not in {None, "NONE"}:
            errors.append(f"{finding_id} may not produce successor effect")

    _validate_reference_fields(finding_sets, finding_ids, errors)
    _validate_source_study_derivations(finding_sets, errors)

    actual_syntheses = _actual_synthesis_paths()
    if actual_syntheses != EXPECTED_SYNTHESIS_PATHS:
        errors.append(
            "problem synthesis tree changed without findings registry revision: "
            f"missing_expected={sorted(EXPECTED_SYNTHESIS_PATHS - actual_syntheses)!r}, "
            f"new_unexpected={sorted(actual_syntheses - EXPECTED_SYNTHESIS_PATHS)!r}"
        )
    registered_syntheses = {
        item["path"]
        for item in finding_sets
        if item.get("record_class") == "PROBLEM_LOCAL_SYNTHESIS"
    }
    if registered_syntheses != actual_syntheses:
        errors.append(
            "problem synthesis records are not exhaustively registered: "
            f"unregistered={sorted(actual_syntheses - registered_syntheses)!r}, "
            f"stale={sorted(registered_syntheses - actual_syntheses)!r}"
        )

    actual_transactions = _actual_transaction_paths()
    if actual_transactions != EXPECTED_TRANSACTION_PATHS:
        errors.append(
            "transaction tree changed without findings registry revision: "
            f"missing_expected={sorted(EXPECTED_TRANSACTION_PATHS - actual_transactions)!r}, "
            f"new_unexpected={sorted(actual_transactions - EXPECTED_TRANSACTION_PATHS)!r}"
        )
    registered_transactions = {
        item["path"]
        for item in finding_sets
        if item.get("record_class") == "MIGRATION_TRANSACTION_LEDGER"
    }
    if registered_transactions != actual_transactions:
        errors.append(
            "migration transactions are not exhaustively registered: "
            f"unregistered={sorted(actual_transactions - registered_transactions)!r}, "
            f"stale={sorted(registered_transactions - actual_transactions)!r}"
        )

    corpus_studies = _corpus_study_paths()
    registered_studies = {
        item["path"]
        for item in finding_sets
        if item.get("record_class") in {"SOURCE_SPECIFIC_STUDY", "INTEGRATION_GOVERNANCE_RECORD"}
    }
    if registered_studies != corpus_studies:
        errors.append(
            "corpus study records are not exhaustively registered as findings sets: "
            f"unregistered={sorted(corpus_studies - registered_studies)!r}, "
            f"stale={sorted(registered_studies - corpus_studies)!r}"
        )

    if not TP_PRESERVED_PATH.is_file() or TP_ACTIVE_PATH.read_bytes() != TP_PRESERVED_PATH.read_bytes():
        errors.append("Theologico-Political active predecessor does not match preserved copy")

    indexes = registry.get("indexes", {})
    by_problem = indexes.get("by_problem", {}) if isinstance(indexes, dict) else {}
    by_source = indexes.get("by_source", {}) if isinstance(indexes, dict) else {}
    by_class = indexes.get("by_record_class", {}) if isinstance(indexes, dict) else {}
    if by_problem != _derived_problem_index(finding_sets):
        errors.append("indexes.by_problem does not match finding-set bindings")
    if by_source != _derived_source_index(finding_sets):
        errors.append("indexes.by_source does not match finding-set source bindings")
    if by_class != _derived_record_class_index(finding_sets):
        errors.append("indexes.by_record_class does not match finding-set record classes")

    coverage = registry.get("coverage", {})
    expected_coverage = {
        "finding_sets_registered": len(finding_ids),
        "source_specific_and_integration_records_registered": len(registered_studies),
        "problem_syntheses_registered": len(registered_syntheses),
        "migration_transaction_ledgers_registered": len(registered_transactions),
        "preserved_finding_bases_registered": sum(
            1
            for item in finding_sets
            if item.get("record_class")
            in {"ACTIVE_PREDECESSOR_FINDING_BASIS", "ACCEPTED_MIGRATION_SOURCE_FINDING_BASIS"}
        ),
        "current_problem_synthesis_tree_yaml_records_accounted_for": len(actual_syntheses),
        "current_foundational_transaction_tree_yaml_records_accounted_for": len(actual_transactions),
        "corpus_study_records_accounted_for": len(corpus_studies),
        "canonical_problem_indexes_registered": len(by_problem) if isinstance(by_problem, dict) else 0,
        "exhaustive_within_declared_scope": True,
    }
    for field, expected in expected_coverage.items():
        if coverage.get(field) != expected:
            errors.append(
                f"coverage.{field} mismatch: expected {expected!r}, found {coverage.get(field)!r}"
            )

    termination = registry.get("termination", {})
    if termination.get("registry_state") != "COMPLETE_FOR_CURRENT_COMMITTED_FINDINGS_RECORD_STATE":
        errors.append("termination.registry_state must preserve bounded current-state completion")
    if termination.get("findings_state") != "OPEN_MATERIALLY_INCOMPLETE_AND_NONCERTIFIED":
        errors.append("termination.findings_state must remain open, incomplete, and noncertified")
    if termination.get("certification") != "NOT_CERTIFIED":
        errors.append("termination may not certify findings")

    return errors


def build_registry_context(
    problem: str | None = None,
    source: str | None = None,
    record_class: str | None = None,
) -> dict[str, Any]:
    registry = load_registry()
    errors = validate_registry(registry)
    if errors:
        raise FindingsRegistryError("Findings registry validation failed:\n- " + "\n- ".join(errors))

    finding_sets = registry["finding_sets"]
    selected_ids: set[str] | None = None
    indexes = registry["indexes"]
    if problem is not None:
        by_problem = indexes["by_problem"]
        if problem not in by_problem:
            raise FindingsRegistryError(f"Unknown problem filter: {problem}")
        selected_ids = set(by_problem[problem])
    if source is not None:
        by_source = indexes["by_source"]
        if source not in by_source:
            raise FindingsRegistryError(f"Unknown source filter: {source}")
        source_ids = set(by_source[source])
        selected_ids = source_ids if selected_ids is None else selected_ids & source_ids
    if record_class is not None:
        by_class = indexes["by_record_class"]
        if record_class not in by_class:
            raise FindingsRegistryError(f"Unknown record-class filter: {record_class}")
        class_ids = set(by_class[record_class])
        selected_ids = class_ids if selected_ids is None else selected_ids & class_ids

    chosen = [
        item
        for item in finding_sets
        if selected_ids is None or item["finding_set_id"] in selected_ids
    ]
    materialized = [
        {
            "declaration": item,
            "record": load_yaml(_resolve(item["path"])),
        }
        for item in chosen
    ]
    return {
        "identity": registry["identity"],
        "status": registry["status"],
        "filters": {
            "problem": problem,
            "source": source,
            "record_class": record_class,
        },
        "finding_sets": materialized,
        "coverage": registry["coverage"],
        "authority": "READ_ONLY_DISCOVERY_PROVENANCE_AND_JURISDICTION_CONTEXT",
        "non_effects": [
            "no proposition promotion",
            "no independent corroboration through derived repetition",
            "no doctrinal certification",
            "no migration certification",
            "no successor activation",
            "no predecessor displacement",
            "no Assembly authority",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--problem")
    parser.add_argument("--source")
    parser.add_argument("--record-class")
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
            "Typed findings registry validation passed for the current committed findings "
            "state; findings remain open, materially incomplete, and not certified."
        )
        return 0
    context = build_registry_context(
        problem=args.problem,
        source=args.source,
        record_class=args.record_class,
    )
    print(json.dumps(context, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
