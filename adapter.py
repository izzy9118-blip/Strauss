#!/usr/bin/env python3
"""Load and validate the lean Strauss operational interface.

The adapter is deliberately read-only. It resolves records declared in manifest.yaml
and emits candidate runtime context. It does not certify, activate, rewrite, or delete
repository records.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "manifest.yaml"
REQUIRED_PROPOSITION_KINDS = {
    "documented_finding",
    "supported_inference",
    "working_hypothesis",
    "comparative_question",
    "unresolved_uncertainty",
}


class StraussAdapterError(RuntimeError):
    """Raised when the operational interface cannot be loaded safely."""


def load_yaml(path: Path) -> dict[str, Any]:
    """Load one YAML mapping and fail with a path-specific diagnostic."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise StraussAdapterError(f"Cannot read {path.relative_to(ROOT)}: {exc}") from exc

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise StraussAdapterError(f"Invalid YAML in {path.relative_to(ROOT)}: {exc}") from exc

    if not isinstance(data, dict):
        raise StraussAdapterError(f"Expected a YAML mapping in {path.relative_to(ROOT)}")
    return data


def _resolve(relative_path: str) -> Path:
    path = (ROOT / relative_path).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError as exc:
        raise StraussAdapterError(f"Path escapes repository root: {relative_path}") from exc
    return path


def load_manifest() -> dict[str, Any]:
    return load_yaml(MANIFEST_PATH)


def iter_declared_paths(manifest: dict[str, Any]) -> Iterable[str]:
    for problem in manifest.get("problems", []):
        yield problem["source"]
        for optional_key in ("active_predecessor", "historical_copy", "accepted_migration_source"):
            value = problem.get(optional_key)
            if value:
                yield value

    for section in ("hermeneutics", "method"):
        for record in manifest.get(section, []):
            yield record["path"]

    yield manifest["speech"]["mechanism"]
    yield manifest["corpus"]["index"]
    yield manifest["findings"]["index"]
    yield manifest["migration"]["mapping_record"]


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    identity = manifest.get("identity", {})
    if identity.get("repository") != "izzy9118-blip/Strauss":
        errors.append("manifest identity.repository must be izzy9118-blip/Strauss")
    if identity.get("minister_id") != "leo-strauss":
        errors.append("manifest identity.minister_id must be leo-strauss")

    problems = manifest.get("problems", [])
    keys = [item.get("canonical_key") for item in problems]
    orders = [item.get("canonical_order") for item in problems]
    expected_keys = [
        "nomos-vs-physis",
        "philosophy-vs-poetry",
        "theory-vs-practice",
        "theologico-political",
        "athens-vs-jerusalem",
        "wise-vs-vulgar",
        "ancients-vs-moderns",
    ]
    if keys != expected_keys:
        errors.append(f"problem order mismatch: {keys!r}")
    if orders != list(range(1, 8)):
        errors.append(f"canonical orders must be 1 through 7: {orders!r}")

    kinds = set(manifest.get("proposition_kinds", []))
    if kinds != REQUIRED_PROPOSITION_KINDS:
        errors.append(f"proposition kinds mismatch: {sorted(kinds)!r}")

    safeguards = manifest.get("safeguards", {})
    for required in (
        "independent_reconstruction_before_comparison",
        "preserve_uncertainty",
        "silent_revision_prohibited",
        "predecessor_overwrite_prohibited",
        "cross_problem_absorption_prohibited",
        "repository_self_certification_prohibited",
        "artificial_intelligence_self_certification_prohibited",
    ):
        if safeguards.get(required) is not True:
            errors.append(f"required safeguard is not true: {required}")

    seen: set[str] = set()
    for relative_path in iter_declared_paths(manifest):
        if relative_path in seen:
            continue
        seen.add(relative_path)
        path = _resolve(relative_path)
        if not path.is_file():
            errors.append(f"declared path does not resolve: {relative_path}")
            continue
        if path.suffix in {".yaml", ".yml"}:
            try:
                load_yaml(path)
            except StraussAdapterError as exc:
                errors.append(str(exc))

    migration = manifest.get("migration", {})
    if migration.get("mode") != "ADDITIVE_NON_DESTRUCTIVE":
        errors.append("migration mode must remain ADDITIVE_NON_DESTRUCTIVE")

    return errors


def _select_problem(manifest: dict[str, Any], canonical_key: str) -> dict[str, Any]:
    for item in manifest["problems"]:
        if item["canonical_key"] == canonical_key:
            return item
    raise StraussAdapterError(f"Unknown problem key: {canonical_key}")


def build_context(problem_keys: list[str] | None = None) -> dict[str, Any]:
    manifest = load_manifest()
    errors = validate_manifest(manifest)
    if errors:
        raise StraussAdapterError("Manifest validation failed:\n- " + "\n- ".join(errors))

    selected = problem_keys or [item["canonical_key"] for item in manifest["problems"]]
    problem_records = []
    for key in selected:
        declaration = _select_problem(manifest, key)
        problem_records.append(
            {
                "declaration": declaration,
                "record": load_yaml(_resolve(declaration["source"])),
            }
        )

    return {
        "manifest_identity": manifest["identity"],
        "status": manifest["status"],
        "source_hierarchy": manifest["source_hierarchy"],
        "proposition_kinds": manifest["proposition_kinds"],
        "method": [
            {"key": item["key"], "record": load_yaml(_resolve(item["path"]))}
            for item in manifest["method"]
        ],
        "hermeneutics": [
            {"key": item["key"], "record": load_yaml(_resolve(item["path"]))}
            for item in manifest["hermeneutics"]
        ],
        "problems": problem_records,
        "speech": load_yaml(_resolve(manifest["speech"]["mechanism"])),
        "corpus": load_yaml(_resolve(manifest["corpus"]["index"])),
        "findings": load_yaml(_resolve(manifest["findings"]["index"])),
        "sanctum_contract": manifest["sanctum_contract"],
        "safeguards": manifest["safeguards"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--problem",
        action="append",
        dest="problems",
        help="Canonical problem key to load; repeat for more than one.",
    )
    parser.add_argument("--validate", action="store_true", help="Validate and exit.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON context.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = load_manifest()
    errors = validate_manifest(manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if args.validate:
        print("Strauss operational manifest validation passed.")
        return 0

    try:
        context = build_context(args.problems)
    except StraussAdapterError as exc:
        print(f"ERROR: {exc}")
        return 1

    print(json.dumps(context, indent=2 if args.pretty else None, sort_keys=args.pretty))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
