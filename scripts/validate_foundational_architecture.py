#!/usr/bin/env python3
"""Validate the founding seven-problem architecture and migration references."""

from __future__ import annotations

import hashlib
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

CANONICAL_KEYS = (
    "nomos-vs-physis",
    "philosophy-vs-poetry",
    "theory-vs-practice",
    "theologico-political",
    "athens-vs-jerusalem",
    "wise-vs-vulgar",
    "ancients-vs-moderns",
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

RECONCILED_PROTOCOL_VERSIONS = {
    "speech-and-deed": "1.1.0",
    "irony": "1.1.0",
    "comedy": "1.1.0",
    "audience-and-rhetoric": "1.1.0",
}

REQUIRED_SUBORDINATE_FIELDS = {
    "inquiry_profile",
    "witnesses",
    "relations",
    "synthesis_directory",
}

CONTROLLED_RELATION_TYPES = {
    "DEPENDS_ON",
    "INTERSECTS",
    "SUPPLIES_FINDING_TO",
}

CONTROLLED_DISPOSITIONS = {
    "RETAIN",
    "TRANSFER",
    "ELEVATE",
    "PRESERVE_HISTORICALLY",
    "REJECT_WITH_REASON",
}

CONTROLLED_TRANSFORMATIONS = {
    "VERBATIM",
    "REVISED",
    "DIVIDED",
    "CONSOLIDATED",
    "REFERENCE_ONLY",
}

TRANSACTION_REQUIRED_FIELDS = {
    "transaction_id",
    "source_canonical_key",
    "source_version",
    "source_item_or_section",
    "original_text_or_exact_source_reference",
    "disposition",
    "destination_canonical_key_or_protocol",
    "destination_item",
    "transformation_mode",
    "reason",
    "continuing_relevance",
    "unresolved_overlap",
    "review_status",
    "implementing_commit",
}

BROTHER_PAIR = frozenset({"philosophy-vs-poetry", "theologico-political"})


def load_yaml(path: Path, errors: list[str]) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except Exception as exc:  # pragma: no cover - diagnostic path
        errors.append(f"YAML parse failure: {path.relative_to(ROOT)}: {exc}")
        return None


def check_path(value: str, context: str, errors: list[str]) -> Path:
    candidate = ROOT / value
    if not candidate.exists():
        errors.append(f"Missing path ({context}): {value}")
    return candidate


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


def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("utf-8")
    return hashlib.sha1(header + payload).hexdigest()


def extract_neighbor_keys(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    keys: list[str] = []
    for item in value:
        if isinstance(item, str):
            keys.append(item)
        elif isinstance(item, dict):
            key = item.get("canonical_key")
            if isinstance(key, str):
                keys.append(key)
    return keys


def validate_problem_boundaries(
    key: str,
    successor: dict[str, Any],
    errors: list[str],
) -> None:
    jurisdiction = successor.get("jurisdiction")
    if not isinstance(jurisdiction, dict):
        errors.append(f"{key}: jurisdiction must be a mapping")
        return

    expected_neighbors = set(CANONICAL_KEYS) - {key}
    excluded = extract_neighbor_keys(jurisdiction.get("does_not_own"))
    if len(excluded) != len(set(excluded)):
        errors.append(f"{key}: duplicate canonical_key under jurisdiction.does_not_own")
    if set(excluded) != expected_neighbors:
        missing = sorted(expected_neighbors - set(excluded))
        extra = sorted(set(excluded) - expected_neighbors)
        errors.append(
            f"{key}: does_not_own mismatch; missing={missing or 'none'}, "
            f"extra={extra or 'none'}"
        )

    relations = successor.get("relations")
    if not isinstance(relations, list):
        errors.append(f"{key}: problem.yaml relations must be a list")
        return

    related: list[str] = []
    for index, relation in enumerate(relations, start=1):
        if not isinstance(relation, dict):
            errors.append(f"{key}: problem relation {index} is not a mapping")
            continue
        other = relation.get("related_problem")
        relation_type = relation.get("relation_type")
        if not isinstance(other, str):
            errors.append(f"{key}: problem relation {index} missing related_problem")
            continue
        related.append(other)
        if other == key:
            errors.append(f"{key}: self-relation is prohibited")
        if other not in CANONICAL_KEYS:
            errors.append(f"{key}: unknown related_problem {other}")
        if relation_type not in CONTROLLED_RELATION_TYPES:
            errors.append(
                f"{key}: uncontrolled relation_type {relation_type!r} for {other}"
            )

    if len(related) != len(set(related)):
        errors.append(f"{key}: duplicate related_problem in problem.yaml")
    if set(related) != expected_neighbors:
        missing = sorted(expected_neighbors - set(related))
        extra = sorted(set(related) - expected_neighbors)
        errors.append(
            f"{key}: problem relation coverage mismatch; missing={missing or 'none'}, "
            f"extra={extra or 'none'}"
        )


def validate_registry(errors: list[str]) -> dict[str, dict[str, Any]]:
    registry_path = ROOT / "problems" / "registry.yaml"
    registry = load_yaml(registry_path, errors)
    if not isinstance(registry, dict):
        return {}

    problems = registry.get("canonical_problems")
    if not isinstance(problems, list):
        errors.append("problems/registry.yaml: canonical_problems must be a list")
        return {}

    if len(problems) != 7:
        errors.append(f"Expected 7 canonical problems, found {len(problems)}")

    keys: list[str] = []
    orders: list[int] = []
    entries: dict[str, dict[str, Any]] = {}

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
        entries[key] = entry

        successor_file = check_path(successor_path, f"successor for {key}", errors)
        successor = load_yaml(successor_file, errors)
        if not isinstance(successor, dict):
            continue

        identity = successor.get("identity", {})
        if not isinstance(identity, dict):
            errors.append(f"{successor_path}: identity must be a mapping")
            continue
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
        if isinstance(status, dict):
            if status.get("certification") == "CERTIFIED":
                errors.append(f"Unauthorized certification found in {successor_path}")
            if status.get("activation") in {"ACTIVE", "ACTIVATED"}:
                errors.append(f"Unauthorized activation found in {successor_path}")

        subordinate = entry.get("subordinate_records")
        if not isinstance(subordinate, dict):
            errors.append(f"{key}: subordinate_records must be a mapping")
        else:
            missing_fields = sorted(REQUIRED_SUBORDINATE_FIELDS - set(subordinate))
            if missing_fields:
                errors.append(
                    f"{key}: missing subordinate fields: {', '.join(missing_fields)}"
                )
            for field, value in subordinate.items():
                if not isinstance(value, str):
                    continue
                candidate = check_path(
                    value,
                    f"registry subordinate {key}.{field}",
                    errors,
                )
                if field == "synthesis_directory" and candidate.exists():
                    if not candidate.is_dir():
                        errors.append(f"{key}: synthesis_directory is not a directory")
                    elif not any(candidate.glob("*.yaml")):
                        errors.append(
                            f"{key}: synthesis_directory contains no YAML records"
                        )

        validate_problem_boundaries(key, successor, errors)

    if set(keys) != set(CANONICAL_KEYS):
        missing = sorted(set(CANONICAL_KEYS) - set(keys))
        extra = sorted(set(keys) - set(CANONICAL_KEYS))
        errors.append(
            f"Canonical key set mismatch; missing={missing or 'none'}, "
            f"extra={extra or 'none'}"
        )
    if len(set(keys)) != len(keys):
        errors.append("Duplicate canonical_key in problems/registry.yaml")
    if len(set(orders)) != len(orders):
        errors.append("Duplicate canonical_order in problems/registry.yaml")
    if sorted(orders) != list(range(1, 8)):
        errors.append(f"Canonical orders must be 1 through 7; found {sorted(orders)}")

    return entries


def relation_has_boundary(relation: dict[str, Any]) -> bool:
    if isinstance(relation.get("boundary"), str):
        return True
    if isinstance(relation.get("neighboring_jurisdiction"), str):
        local_fields = [key for key in relation if key.endswith("_jurisdiction")]
        return bool(local_fields)
    jurisdiction_fields = [key for key in relation if key.endswith("_jurisdiction")]
    return len(jurisdiction_fields) >= 2


def validate_relations(
    registry_entries: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    relation_maps: dict[str, dict[str, dict[str, Any]]] = {}
    brother_records: list[tuple[str, str, dict[str, Any]]] = []

    for key in CANONICAL_KEYS:
        entry = registry_entries.get(key)
        if not isinstance(entry, dict):
            continue
        subordinate = entry.get("subordinate_records", {})
        path_value = subordinate.get("relations") if isinstance(subordinate, dict) else None
        if not isinstance(path_value, str):
            errors.append(f"{key}: relations path absent from registry")
            continue

        path = check_path(path_value, f"relations for {key}", errors)
        data = load_yaml(path, errors)
        if not isinstance(data, dict):
            continue

        identity = data.get("identity", {})
        if not isinstance(identity, dict) or identity.get("problem") != key:
            errors.append(f"{path_value}: identity.problem must equal {key}")

        relations = data.get("relations")
        if not isinstance(relations, list):
            errors.append(f"{path_value}: relations must be a list")
            continue

        per_problem: dict[str, dict[str, Any]] = {}
        for index, relation in enumerate(relations, start=1):
            if not isinstance(relation, dict):
                errors.append(f"{path_value}: relation {index} is not a mapping")
                continue
            other = relation.get("related_problem")
            relation_type = relation.get("relation_type")
            if not isinstance(other, str):
                errors.append(f"{path_value}: relation {index} missing related_problem")
                continue
            if other == key:
                errors.append(f"{path_value}: self-relation is prohibited")
            if other not in CANONICAL_KEYS:
                errors.append(f"{path_value}: unknown related_problem {other}")
            if relation_type not in CONTROLLED_RELATION_TYPES:
                errors.append(
                    f"{path_value}: uncontrolled relation_type {relation_type!r} "
                    f"for {other}"
                )
            if other in per_problem:
                errors.append(f"{path_value}: duplicate relation to {other}")
            per_problem[other] = relation
            if not relation_has_boundary(relation):
                errors.append(
                    f"{path_value}: relation to {other} lacks a jurisdictional boundary"
                )

            designation = relation.get("constitutional_designation")
            if designation is not None:
                if designation != "BROTHER_PROBLEM":
                    errors.append(
                        f"{path_value}: uncontrolled constitutional_designation "
                        f"{designation!r}"
                    )
                brother_records.append((key, other, relation))

        expected = set(CANONICAL_KEYS) - {key}
        if set(per_problem) != expected:
            missing = sorted(expected - set(per_problem))
            extra = sorted(set(per_problem) - expected)
            errors.append(
                f"{path_value}: relation coverage mismatch; missing={missing or 'none'}, "
                f"extra={extra or 'none'}"
            )
        relation_maps[key] = per_problem

    for key, relations in relation_maps.items():
        for other in relations:
            reciprocal = relation_maps.get(other, {}).get(key)
            if reciprocal is None:
                errors.append(
                    f"Missing reciprocal relation: {key} -> {other} exists, "
                    f"but {other} -> {key} does not"
                )

    if len(brother_records) != 2:
        errors.append(
            f"Expected exactly two reciprocal BROTHER_PROBLEM records, found "
            f"{len(brother_records)}"
        )
    for key, other, relation in brother_records:
        if frozenset({key, other}) != BROTHER_PAIR:
            errors.append(
                f"Unauthorized BROTHER_PROBLEM designation between {key} and {other}"
            )
        if relation.get("relation_type") != "INTERSECTS":
            errors.append(
                f"BROTHER_PROBLEM relation {key}->{other} must use INTERSECTS"
            )
        if relation.get("relation_strength") != "CO_FOUNDATIONAL":
            errors.append(
                f"BROTHER_PROBLEM relation {key}->{other} must be CO_FOUNDATIONAL"
            )


def protocol_file_version(data: dict[str, Any]) -> str | None:
    identity = data.get("identity")
    if isinstance(identity, dict):
        version = identity.get("protocol_version")
        if isinstance(version, str):
            return version
    version = data.get("protocol_version")
    return version if isinstance(version, str) else None


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
            errors.append("protocols/registry.yaml: protocol entry is not a mapping")
            continue
        key = entry.get("canonical_key")
        if not isinstance(key, str):
            errors.append("protocols/registry.yaml: protocol missing canonical_key")
            continue
        if key in keys:
            errors.append(f"protocols/registry.yaml: duplicate protocol {key}")
        keys.add(key)

        value = entry.get("path") or entry.get("protocol_path")
        if not isinstance(value, str):
            errors.append(f"protocols/registry.yaml: {key} missing path")
            continue
        protocol_path = check_path(value, f"protocol {key}", errors)
        protocol = load_yaml(protocol_path, errors)
        if not isinstance(protocol, dict):
            continue
        identity = protocol.get("identity", {})
        if isinstance(identity, dict) and identity.get("canonical_key") != key:
            errors.append(f"Protocol canonical key mismatch for {key} at {value}")

        actual_version = protocol_file_version(protocol)
        registry_version = entry.get("protocol_version")
        if registry_version != actual_version:
            errors.append(
                f"Protocol version mismatch for {key}: registry={registry_version}, "
                f"file={actual_version}"
            )
        expected_version = RECONCILED_PROTOCOL_VERSIONS.get(key)
        if expected_version and actual_version != expected_version:
            errors.append(
                f"Reconciled protocol {key} must be {expected_version}, "
                f"found {actual_version}"
            )

    missing = sorted(REQUIRED_PROTOCOLS - keys)
    if missing:
        errors.append(f"Required protocols absent from registry: {', '.join(missing)}")


def validate_wise_vs_vulgar_transactions(errors: list[str]) -> None:
    ledger_path = (
        ROOT
        / "migrations"
        / "foundational-problems-v2"
        / "transactions"
        / "wise-vs-vulgar-v0.2.yaml"
    )
    ledger = load_yaml(ledger_path, errors)
    if not isinstance(ledger, dict):
        return

    section_transactions = ledger.get("section_transactions")
    proposition_transactions = ledger.get("proposition_transactions")
    if not isinstance(section_transactions, list):
        errors.append("Wise vs. Vulgar ledger: section_transactions must be a list")
        section_transactions = []
    if not isinstance(proposition_transactions, list):
        errors.append("Wise vs. Vulgar ledger: proposition_transactions must be a list")
        proposition_transactions = []

    if len(section_transactions) != 18:
        errors.append(
            f"Wise vs. Vulgar: expected 18 section transactions, "
            f"found {len(section_transactions)}"
        )
    if len(proposition_transactions) != 49:
        errors.append(
            f"Wise vs. Vulgar: expected 49 proposition transactions, "
            f"found {len(proposition_transactions)}"
        )

    all_transactions = section_transactions + proposition_transactions
    identifiers: set[str] = set()
    disposition_counts = {value: 0 for value in CONTROLLED_DISPOSITIONS}

    for index, transaction in enumerate(all_transactions, start=1):
        if not isinstance(transaction, dict):
            errors.append(f"Wise vs. Vulgar transaction {index} is not a mapping")
            continue
        missing = sorted(TRANSACTION_REQUIRED_FIELDS - set(transaction))
        if missing:
            errors.append(
                f"Wise vs. Vulgar transaction {index} missing fields: "
                f"{', '.join(missing)}"
            )

        transaction_id = transaction.get("transaction_id")
        if not isinstance(transaction_id, str):
            errors.append(f"Wise vs. Vulgar transaction {index} missing transaction_id")
        elif transaction_id in identifiers:
            errors.append(f"Duplicate Wise vs. Vulgar transaction_id {transaction_id}")
        else:
            identifiers.add(transaction_id)

        disposition = transaction.get("disposition")
        if disposition not in CONTROLLED_DISPOSITIONS:
            errors.append(
                f"{transaction_id or index}: invalid disposition {disposition!r}"
            )
        else:
            disposition_counts[disposition] += 1

        transformation = transaction.get("transformation_mode")
        if transformation not in CONTROLLED_TRANSFORMATIONS:
            errors.append(
                f"{transaction_id or index}: invalid transformation_mode "
                f"{transformation!r}"
            )

        destination = transaction.get("destination_canonical_key_or_protocol")
        if not isinstance(destination, str) or not destination.strip():
            errors.append(f"{transaction_id or index}: primary destination is empty")

        if transaction.get("source_canonical_key") != "wise-vs-vulgar":
            errors.append(
                f"{transaction_id or index}: source_canonical_key must be wise-vs-vulgar"
            )

    if len(all_transactions) != 67:
        errors.append(
            f"Wise vs. Vulgar: expected 67 total transactions, "
            f"found {len(all_transactions)}"
        )

    source_identity = ledger.get("source_identity", {})
    if isinstance(source_identity, dict):
        accepted_path_value = source_identity.get("source_path")
        accepted_sha = source_identity.get("source_blob_sha")
        active_path_value = source_identity.get("active_predecessor_path")
        active_sha = source_identity.get("active_predecessor_blob_sha")

        if isinstance(accepted_path_value, str):
            accepted_path = check_path(
                accepted_path_value,
                "Wise vs. Vulgar accepted migration source",
                errors,
            )
            if accepted_path.exists() and isinstance(accepted_sha, str):
                actual = git_blob_sha(accepted_path)
                if actual != accepted_sha:
                    errors.append(
                        f"Wise vs. Vulgar accepted source blob mismatch: "
                        f"expected {accepted_sha}, found {actual}"
                    )
        if isinstance(active_path_value, str):
            active_path = check_path(
                active_path_value,
                "Wise vs. Vulgar active predecessor",
                errors,
            )
            if active_path.exists() and isinstance(active_sha, str):
                actual = git_blob_sha(active_path)
                if actual != active_sha:
                    errors.append(
                        f"Wise vs. Vulgar active predecessor blob mismatch: "
                        f"expected {active_sha}, found {actual}"
                    )

    wise_problem_path = ROOT / "problems" / "wise-vs-vulgar" / "problem.yaml"
    wise_problem = load_yaml(wise_problem_path, errors)
    if isinstance(wise_problem, dict):
        classification = wise_problem.get("migration_classification", {})
        if isinstance(classification, dict):
            coverage = classification.get("coverage", {})
            if isinstance(coverage, dict):
                expected_values = {
                    "accepted_top_level_units": 18,
                    "accepted_top_level_units_classified": 18,
                    "constitutive_propositions": 49,
                    "constitutive_propositions_classified": 49,
                    "rejected_with_reason": disposition_counts["REJECT_WITH_REASON"],
                }
                for field, expected in expected_values.items():
                    if coverage.get(field) != expected:
                        errors.append(
                            f"Wise vs. Vulgar problem coverage {field}: "
                            f"expected {expected}, found {coverage.get(field)}"
                        )
            recorded_blob = classification.get("transaction_blob_sha")
            actual_blob = git_blob_sha(ledger_path)
            if recorded_blob != actual_blob:
                errors.append(
                    f"Wise vs. Vulgar ledger blob mismatch in problem.yaml: "
                    f"expected {recorded_blob}, found {actual_blob}"
                )

    relations_path = ROOT / "problems" / "wise-vs-vulgar" / "relations.yaml"
    relations = load_yaml(relations_path, errors)
    if isinstance(relations, dict):
        status = relations.get("status", {})
        lifecycle = status.get("lifecycle") if isinstance(status, dict) else None
        if lifecycle == "CLASSIFICATION_AND_REDISTRIBUTION_PENDING":
            errors.append(
                "Wise vs. Vulgar relations still claims classification is pending"
            )
        termination = relations.get("termination", {})
        remaining = (
            termination.get("remaining_requirements", [])
            if isinstance(termination, dict)
            else []
        )
        if isinstance(remaining, list):
            for item in remaining:
                if isinstance(item, str) and "proposition-level redistribution" in item:
                    errors.append(
                        "Wise vs. Vulgar relations retains stale redistribution requirement"
                    )


def validate_predecessor_preservation(errors: list[str]) -> None:
    active_tp = ROOT / "problems" / "theologico-political.yaml"
    preserved_tp = (
        ROOT
        / "history"
        / "foundational-problems"
        / "theologico-political"
        / "STR-PROBLEM-002-v1.1-active-predecessor.yaml"
    )
    if active_tp.exists() and preserved_tp.exists():
        if active_tp.read_bytes() != preserved_tp.read_bytes():
            errors.append(
                "Theologico-Political active predecessor differs from preserved copy"
            )
    else:
        errors.append(
            "Theologico-Political active predecessor or preserved copy is missing"
        )

    required_wvg_paths = (
        "problems/wise-and-vulgar.yaml",
        "history/foundational-problems/wise-vs-vulgar/"
        "WVG-v0.2-reconstruction-accepted.yaml",
        "migrations/foundational-problems-v2/transactions/"
        "wise-vs-vulgar-v0.2.yaml",
    )
    for value in required_wvg_paths:
        check_path(value, "Wise vs. Vulgar preservation", errors)


def validate_sppp_integration(errors: list[str]) -> None:
    required_paths = (
        "studies/studies-in-platonic-political-philosophy/source-status.yaml",
        "studies/studies-in-platonic-political-philosophy/sequential-reading.yaml",
        "studies/studies-in-platonic-political-philosophy/"
        "foundational-problems-synthesis.yaml",
        "studies/studies-in-platonic-political-philosophy/"
        "theologico-political-reconstruction.yaml",
        "studies/studies-in-platonic-political-philosophy/repository-integration.yaml",
        "studies/studies-in-platonic-political-philosophy/integration-completion.yaml",
        "migrations/foundational-problems-v2/transactions/"
        "theologico-political-sppp-study-001.yaml",
        "migrations/foundational-problems-v2/validation/sppp-integration-001.yaml",
        "migrations/foundational-problems-v2/validation/"
        "cross-problem-jurisdiction-review-001.yaml",
        "problems/philosophy-vs-poetry/witnesses.yaml",
        "problems/theologico-political/witnesses.yaml",
        "protocols/speech-and-deed.yaml",
    )
    for value in required_paths:
        check_path(value, "SPPP and migration integration", errors)

    bridge_paths = (
        "problems/nomos-vs-physis/synthesis/"
        "studies-in-platonic-political-philosophy.yaml",
        "problems/philosophy-vs-poetry/synthesis/"
        "studies-in-platonic-political-philosophy.yaml",
        "problems/theory-vs-practice/synthesis/"
        "studies-in-platonic-political-philosophy.yaml",
        "problems/theologico-political/synthesis/"
        "studies-in-platonic-political-philosophy.yaml",
        "problems/athens-vs-jerusalem/synthesis/"
        "studies-in-platonic-political-philosophy.yaml",
        "problems/wise-vs-vulgar/synthesis/"
        "studies-in-platonic-political-philosophy.yaml",
        "problems/ancients-vs-moderns/synthesis/"
        "studies-in-platonic-political-philosophy.yaml",
    )
    for value in bridge_paths:
        check_path(value, "SPPP problem bridge", errors)


def validate_cross_problem_review(errors: list[str]) -> None:
    path = (
        ROOT
        / "migrations"
        / "foundational-problems-v2"
        / "validation"
        / "cross-problem-jurisdiction-review-001.yaml"
    )
    review = load_yaml(path, errors)
    if not isinstance(review, dict):
        return

    status = review.get("status", {})
    if isinstance(status, dict):
        if status.get("certification") == "CERTIFIED":
            errors.append("Cross-problem review may not certify the migration")
        if status.get("activation_authorized") is True:
            errors.append("Cross-problem review may not authorize activation")

    pairs = review.get("pairwise_review")
    if not isinstance(pairs, list):
        errors.append("Cross-problem review: pairwise_review must be a list")
        return

    seen: set[frozenset[str]] = set()
    for index, item in enumerate(pairs, start=1):
        if not isinstance(item, dict):
            errors.append(f"Cross-problem review pair {index} is not a mapping")
            continue
        problems = item.get("problems")
        if not isinstance(problems, list) or len(problems) != 2:
            errors.append(
                f"Cross-problem review pair {index} must identify exactly two problems"
            )
            continue
        pair = frozenset(problems)
        if len(pair) != 2 or not pair.issubset(CANONICAL_KEYS):
            errors.append(
                f"Cross-problem review pair {index} contains invalid problems {problems}"
            )
            continue
        if pair in seen:
            errors.append(
                f"Cross-problem review contains duplicate pair {sorted(pair)}"
            )
        seen.add(pair)

    if len(seen) != 21:
        errors.append(
            f"Cross-problem review must cover 21 unique pairs, found {len(seen)}"
        )


def main() -> int:
    errors: list[str] = []
    yaml_count = validate_all_yaml(errors)
    registry_entries = validate_registry(errors)
    validate_relations(registry_entries, errors)
    validate_protocol_registry(errors)
    validate_wise_vs_vulgar_transactions(errors)
    validate_predecessor_preservation(errors)
    validate_sppp_integration(errors)
    validate_cross_problem_review(errors)

    if errors:
        print(f"Validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validation passed: parsed {yaml_count} YAML files.")
    print("Seven canonical problem identities, orders, and subordinate contracts align.")
    print("All reciprocal relation records resolve and preserve jurisdictional boundaries.")
    print("Shared protocol registry versions match their governing files.")
    print("Wise vs. Vulgar contains 18 section and 49 proposition transactions.")
    print("Predecessor preservation and SPPP integration paths are valid.")
    print("Cross-problem review covers all 21 unique problem pairs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
