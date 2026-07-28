#!/usr/bin/env python3
"""Load and validate complete foundational-problem bundles.

A bundle consists of the problem constitution, inquiry profile, witness registry,
relation record, and registered synthesis records. The loader is read-only and
non-certifying. It does not interpret sources, activate successors, displace
predecessors, or convert provisional findings into doctrine.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "manifest.yaml"

CANONICAL_KEYS = [
    "nomos-vs-physis",
    "philosophy-vs-poetry",
    "theory-vs-practice",
    "theologico-political",
    "athens-vs-jerusalem",
    "wise-vs-vulgar",
    "ancients-vs-moderns",
]

REQUIRED_BUNDLE_PATH_FIELDS = {
    "source",
    "inquiry_profile",
    "witnesses",
    "relations",
    "synthesis_directory",
}

REQUIRED_PROFILE_SECTIONS = {
    "purpose",
    "shared_protocol_references",
    "problem_specific_operations",
    "activation_signals",
    "governing_distinctions",
    "investigative_questions",
    "false_resolutions",
}

REQUIRED_WITNESS_SECTIONS = {
    "source_status_rules",
    "witness_relation_rules",
}

WITNESS_LIST_KEYS = (
    "witnesses",
    "principal_witnesses",
)

CONTROLLED_RELATION_TYPES = {
    "DEPENDS_ON",
    "INTERSECTS",
    "SUPPLIES_FINDING_TO",
}


class ProblemBundleError(RuntimeError):
    """Raised when a foundational-problem bundle cannot be loaded safely."""


def _resolve(relative_path: str) -> Path:
    path = (ROOT / relative_path).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError as exc:
        raise ProblemBundleError(f"Path escapes repository root: {relative_path}") from exc
    return path


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ProblemBundleError(f"Cannot read {path.relative_to(ROOT)}: {exc}") from exc

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ProblemBundleError(f"Invalid YAML in {path.relative_to(ROOT)}: {exc}") from exc

    if not isinstance(data, dict):
        raise ProblemBundleError(f"Expected a YAML mapping in {path.relative_to(ROOT)}")
    return data


def load_manifest() -> dict[str, Any]:
    return load_yaml(MANIFEST_PATH)


def _select_declaration(manifest: dict[str, Any], canonical_key: str) -> dict[str, Any]:
    for declaration in manifest.get("problems", []):
        if declaration.get("canonical_key") == canonical_key:
            return declaration
    raise ProblemBundleError(f"Unknown problem key: {canonical_key}")


def iter_bundle_paths(declaration: dict[str, Any]) -> Iterable[str]:
    for field in REQUIRED_BUNDLE_PATH_FIELDS:
        value = declaration.get(field)
        if isinstance(value, str):
            yield value


def _status_is_noncertifying(record: dict[str, Any]) -> bool:
    status = record.get("status", {})
    if not isinstance(status, dict):
        return False
    if status.get("certification") == "CERTIFIED":
        return False
    if status.get("activation") in {"ACTIVE", "ACTIVATED"}:
        return False
    return True


def _principal_witnesses(record: dict[str, Any]) -> list[Any] | None:
    """Return the declared principal witness list without rewriting its source key."""
    for key in WITNESS_LIST_KEYS:
        value = record.get(key)
        if isinstance(value, list):
            return value
    return None


def _witness_registry_purpose(record: dict[str, Any]) -> str | None:
    """Resolve an explicit registry purpose without imposing one historical layout."""
    purpose = record.get("registry_purpose")
    if isinstance(purpose, str) and purpose.strip():
        return purpose
    authority = record.get("authority")
    if isinstance(authority, dict):
        governing_rule = authority.get("governing_rule")
        if isinstance(governing_rule, str) and governing_rule.strip():
            return governing_rule
    return None


def validate_problem_declaration(
    declaration: dict[str, Any],
    expected_key: str,
    expected_order: int,
) -> list[str]:
    errors: list[str] = []
    if declaration.get("canonical_key") != expected_key:
        errors.append(f"declaration canonical_key mismatch for {expected_key}")
    if declaration.get("canonical_order") != expected_order:
        errors.append(f"declaration canonical_order mismatch for {expected_key}")

    missing = sorted(REQUIRED_BUNDLE_PATH_FIELDS - set(declaration))
    if missing:
        errors.append(f"{expected_key} declaration missing bundle paths: {', '.join(missing)}")

    for field in REQUIRED_BUNDLE_PATH_FIELDS:
        value = declaration.get(field)
        if not isinstance(value, str) or not value:
            errors.append(f"{expected_key}.{field} must be a non-empty path")
            continue
        path = _resolve(value)
        if field == "synthesis_directory":
            if not path.is_dir():
                errors.append(f"{expected_key}.{field} does not resolve to a directory: {value}")
            elif not any(path.glob("*.yaml")):
                errors.append(f"{expected_key}.{field} contains no YAML synthesis records")
        elif not path.is_file():
            errors.append(f"{expected_key}.{field} does not resolve to a file: {value}")
    return errors


def validate_problem_bundle(bundle: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    declaration = bundle.get("declaration", {})
    key = declaration.get("canonical_key")
    if key not in CANONICAL_KEYS:
        return [f"bundle has unknown canonical key: {key!r}"]

    constitution = bundle.get("constitution", {})
    identity = constitution.get("identity", {}) if isinstance(constitution, dict) else {}
    if identity.get("canonical_key") != key:
        errors.append(f"{key}: constitution identity mismatch")
    # Local record status is evidentiary metadata; STRAUSS-AUTH-001 governs operational authority.

    profile = bundle.get("inquiry_profile", {})
    profile_identity = profile.get("identity", {}) if isinstance(profile, dict) else {}
    if profile_identity.get("problem") != key:
        errors.append(f"{key}: inquiry-profile identity mismatch")
    missing_profile = (
        sorted(REQUIRED_PROFILE_SECTIONS - set(profile))
        if isinstance(profile, dict)
        else sorted(REQUIRED_PROFILE_SECTIONS)
    )
    if missing_profile:
        errors.append(f"{key}: inquiry profile missing sections: {', '.join(missing_profile)}")
    # Owner authorization permits active use while preserving local record metadata.

    witnesses = bundle.get("witnesses", {})
    witness_identity = witnesses.get("identity", {}) if isinstance(witnesses, dict) else {}
    if witness_identity.get("problem") != key:
        errors.append(f"{key}: witness-registry identity mismatch")
    missing_witness = (
        sorted(REQUIRED_WITNESS_SECTIONS - set(witnesses))
        if isinstance(witnesses, dict)
        else sorted(REQUIRED_WITNESS_SECTIONS)
    )
    if missing_witness:
        errors.append(f"{key}: witness registry missing sections: {', '.join(missing_witness)}")
    if not isinstance(witnesses, dict) or not _witness_registry_purpose(witnesses):
        errors.append(
            f"{key}: witness registry must state its purpose either as registry_purpose "
            "or authority.governing_rule"
        )
    principal_witnesses = _principal_witnesses(witnesses) if isinstance(witnesses, dict) else None
    if not principal_witnesses:
        accepted = " or ".join(WITNESS_LIST_KEYS)
        errors.append(
            f"{key}: witness registry must contain at least one witness under {accepted}"
        )
    # Witness evidence classes remain local; operational use is owner-authorized.

    relation_record = bundle.get("relations", {})
    relation_identity = relation_record.get("identity", {}) if isinstance(relation_record, dict) else {}
    if relation_identity.get("problem") != key:
        errors.append(f"{key}: relation-record identity mismatch")
    relations = relation_record.get("relations") if isinstance(relation_record, dict) else None
    if not isinstance(relations, list):
        errors.append(f"{key}: relations must be a list")
        relations = []
    expected_neighbors = set(CANONICAL_KEYS) - {key}
    seen: set[str] = set()
    for index, relation in enumerate(relations, start=1):
        if not isinstance(relation, dict):
            errors.append(f"{key}: relation {index} is not a mapping")
            continue
        other = relation.get("related_problem")
        relation_type = relation.get("relation_type")
        if other not in expected_neighbors:
            errors.append(f"{key}: invalid related problem {other!r}")
        else:
            seen.add(other)
        if relation_type not in CONTROLLED_RELATION_TYPES:
            errors.append(f"{key}: uncontrolled relation type {relation_type!r}")
        boundary_fields = [
            name
            for name in relation
            if name == "boundary" or name.endswith("_jurisdiction")
        ]
        if not boundary_fields:
            errors.append(f"{key}: relation to {other!r} lacks a jurisdictional boundary")
    if seen != expected_neighbors:
        errors.append(
            f"{key}: relation coverage mismatch; missing={sorted(expected_neighbors - seen)!r}, "
            f"extra={sorted(seen - expected_neighbors)!r}"
        )
    # Relation records are operational under the repository authorization.

    syntheses = bundle.get("syntheses")
    if not isinstance(syntheses, list) or not syntheses:
        errors.append(f"{key}: bundle must expose at least one registered synthesis")
    else:
        for item in syntheses:
            if not isinstance(item, dict) or "path" not in item or "record" not in item:
                errors.append(f"{key}: malformed synthesis entry")

    return errors


def build_problem_bundle(
    canonical_key: str,
    manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    manifest = manifest or load_manifest()
    declaration = _select_declaration(manifest, canonical_key)
    expected_order = CANONICAL_KEYS.index(canonical_key) + 1
    declaration_errors = validate_problem_declaration(
        declaration,
        canonical_key,
        expected_order,
    )
    if declaration_errors:
        raise ProblemBundleError(
            "Problem declaration validation failed:\n- "
            + "\n- ".join(declaration_errors)
        )

    synthesis_dir = _resolve(declaration["synthesis_directory"])
    syntheses = [
        {"path": str(path.relative_to(ROOT)), "record": load_yaml(path)}
        for path in sorted(synthesis_dir.glob("*.yaml"))
    ]

    bundle = {
        "declaration": declaration,
        "constitution": load_yaml(_resolve(declaration["source"])),
        "inquiry_profile": load_yaml(_resolve(declaration["inquiry_profile"])),
        "witnesses": load_yaml(_resolve(declaration["witnesses"])),
        "relations": load_yaml(_resolve(declaration["relations"])),
        "syntheses": syntheses,
        "authority": "AUTHORIZED_OPERATIONAL_PROBLEM_CONTEXT",
    }
    errors = validate_problem_bundle(bundle)
    if errors:
        raise ProblemBundleError(
            "Problem bundle validation failed:\n- " + "\n- ".join(errors)
        )
    return bundle


def build_problem_bundle_context(problem_keys: list[str] | None = None) -> dict[str, Any]:
    manifest = load_manifest()
    selected = problem_keys or CANONICAL_KEYS
    bundles = [build_problem_bundle(key, manifest) for key in selected]
    return {
        "manifest_identity": manifest.get("identity"),
        "status": manifest.get("status"),
        "problem_bundle_completion": manifest.get("problem_bundle_completion"),
        "problems": bundles,
        "authority": "AUTHORIZED_STRAUSS_RUNTIME_CONTEXT",
        "authorization": "governance/repository-authorization.yaml",
        "preserved_limits": [
            "evidence classifications remain binding",
            "uncertainty remains visible",
            "no silent source-specific finding promotion",
            "predecessor history remains recoverable",
        ],
    }


def validate_manifest_problem_bundles(
    manifest: dict[str, Any] | None = None,
) -> list[str]:
    manifest = manifest or load_manifest()
    errors: list[str] = []
    problems = manifest.get("problems", [])
    keys = [item.get("canonical_key") for item in problems if isinstance(item, dict)]
    if keys != CANONICAL_KEYS:
        errors.append(f"problem declaration order mismatch: {keys!r}")
        return errors

    for order, key in enumerate(CANONICAL_KEYS, start=1):
        declaration = _select_declaration(manifest, key)
        declaration_errors = validate_problem_declaration(declaration, key, order)
        errors.extend(declaration_errors)
        if declaration_errors:
            continue
        try:
            build_problem_bundle(key, manifest)
        except ProblemBundleError as exc:
            errors.append(str(exc))
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--problem", action="append", dest="problems")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_manifest_problem_bundles()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.validate:
        print(
            "Seven foundational problem bundles validated for owner-authorized operational loading; "
            "research gaps remain evidentiary rather than activation blockers."
        )
        return 0
    try:
        context = build_problem_bundle_context(args.problems)
    except ProblemBundleError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(context, indent=2 if args.pretty else None, sort_keys=args.pretty))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
