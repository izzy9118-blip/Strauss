#!/usr/bin/env python3
"""Load and validate the lean Strauss operational interface.

The adapter is deliberately read-only. It resolves records declared in manifest.yaml,
validates the speech contract and typed speech requests, and emits candidate runtime
context or candidate ministerial-report structures. It does not interpret sources,
certify doctrine, activate problems, rewrite records, or confer Assembly authority.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "manifest.yaml"

CANONICAL_PROBLEM_KEYS = [
    "nomos-vs-physis",
    "philosophy-vs-poetry",
    "theory-vs-practice",
    "theologico-political",
    "athens-vs-jerusalem",
    "wise-vs-vulgar",
    "ancients-vs-moderns",
]

REQUIRED_PROPOSITION_KINDS = {
    "documented_finding",
    "supported_inference",
    "working_hypothesis",
    "comparative_question",
    "unresolved_uncertainty",
}

ALLOWED_CONFIDENCE_VALUES = {"HIGH", "MODERATE", "LOW", "NOT_APPLICABLE"}

REQUIRED_SPEECH_SECTIONS = {
    "input_contract",
    "problem_activation",
    "reasoning_to_expression_pipeline",
    "source_and_evidence_contract",
    "speech_and_deed_contract",
    "concealment_contract",
    "irony_contract",
    "comedy_contract",
    "voice_and_rhetoric_contract",
    "output_contract",
    "failure_and_stopping_conditions",
    "termination_contract",
    "behavioral_test_requirements",
    "sanctum_interoperability",
    "prohibited_outputs",
    "self_limitation",
}

REQUIRED_BEHAVIORAL_TEST_IDS = {
    f"SPEECH-TEST-{index:03d}" for index in range(1, 11)
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
        raise StraussAdapterError(
            f"Invalid YAML in {path.relative_to(ROOT)}: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise StraussAdapterError(
            f"Expected a YAML mapping in {path.relative_to(ROOT)}"
        )
    return data


def _resolve(relative_path: str) -> Path:
    path = (ROOT / relative_path).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError as exc:
        raise StraussAdapterError(
            f"Path escapes repository root: {relative_path}"
        ) from exc
    return path


def _missing_or_empty(mapping: dict[str, Any], fields: Iterable[str]) -> list[str]:
    return [
        field
        for field in fields
        if field not in mapping or mapping[field] in (None, "", [], {})
    ]


def load_manifest() -> dict[str, Any]:
    return load_yaml(MANIFEST_PATH)


def load_speech_mechanism(manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    manifest = manifest or load_manifest()
    return load_yaml(_resolve(manifest["speech"]["mechanism"]))


def iter_declared_paths(manifest: dict[str, Any]) -> Iterable[str]:
    for problem in manifest.get("problems", []):
        yield problem["source"]
        for optional_key in (
            "active_predecessor",
            "historical_copy",
            "accepted_migration_source",
        ):
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
    yield manifest["audit"]["path"]


def validate_speech_mechanism(mechanism: dict[str, Any]) -> list[str]:
    """Validate the semantic shape of the speech-mechanism contract."""
    errors: list[str] = []

    identity = mechanism.get("identity", {})
    if identity.get("contract_version") != "STRAUSS-SPEECH-CONTRACT-1":
        errors.append(
            "speech mechanism identity.contract_version must be STRAUSS-SPEECH-CONTRACT-1"
        )

    missing_sections = sorted(REQUIRED_SPEECH_SECTIONS - set(mechanism))
    if missing_sections:
        errors.append(
            "speech mechanism missing required sections: " + ", ".join(missing_sections)
        )

    status = mechanism.get("status", {})
    if status.get("doctrinal_certification") != "OWNER_CERTIFIED_FOR_OPERATIONAL_USE":
        errors.append("speech mechanism must carry owner operational certification")
    if status.get("voice") != "subordinate_to_reasoning":
        errors.append("speech mechanism voice must remain subordinate_to_reasoning")

    contract = mechanism.get("input_contract", {})
    common = set(contract.get("required_common_fields", []))
    expected_common = {
        "request_id",
        "inquiry_ref",
        "question",
        "activated_problems",
        "sources",
        "audience",
        "occasion",
        "requested_output",
    }
    if not expected_common.issubset(common):
        errors.append(
            "speech input contract missing common fields: "
            + ", ".join(sorted(expected_common - common))
        )

    finding_fields = set(contract.get("finding_required_fields", []))
    expected_finding_fields = {
        "kind",
        "statement",
        "supporting_evidence",
        "source_location",
        "confidence",
        "alternatives_considered",
    }
    if not expected_finding_fields.issubset(finding_fields):
        errors.append(
            "speech input contract missing finding fields: "
            + ", ".join(sorted(expected_finding_fields - finding_fields))
        )

    allowed = contract.get("allowed_problem_keys", [])
    if allowed != CANONICAL_PROBLEM_KEYS:
        errors.append(f"speech contract problem order mismatch: {allowed!r}")

    output = mechanism.get("output_contract", {})
    if output.get("record_type") != "ministerial_report":
        errors.append("speech output record_type must be ministerial_report")
    if output.get("authority") != "AUTHORIZED_STRAUSS_MINISTERIAL_REPORT":
        errors.append("speech output authority must be owner-authorized")

    test_ids = {
        item.get("id")
        for item in mechanism.get("behavioral_test_requirements", [])
        if isinstance(item, dict)
    }
    if test_ids != REQUIRED_BEHAVIORAL_TEST_IDS:
        errors.append(
            "speech behavioral test set mismatch: "
            f"missing={sorted(REQUIRED_BEHAVIORAL_TEST_IDS - test_ids)!r}, "
            f"extra={sorted(test_ids - REQUIRED_BEHAVIORAL_TEST_IDS)!r}"
        )

    if mechanism.get("concealment_contract", {}).get("threshold") != "POSITIVE_EVIDENCE_REQUIRED":
        errors.append("concealment threshold must require positive evidence")

    comedy_key = mechanism.get("comedy_contract", {}).get("permanent_interpretive_key")
    if comedy_key != "Strauss's comedy corrects solemn scholarship.":
        errors.append("permanent comedy interpretive key is missing or altered")

    return errors


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    identity = manifest.get("identity", {})
    if identity.get("repository") != "izzy9118-blip/Strauss":
        errors.append("manifest identity.repository must be izzy9118-blip/Strauss")
    if identity.get("minister_id") != "leo-strauss":
        errors.append("manifest identity.minister_id must be leo-strauss")

    status = manifest.get("status", {})
    if status.get("semantic_completion") != "INCOMPLETE":
        errors.append("manifest must state semantic_completion: INCOMPLETE")
    if status.get("doctrinal_certification") != "OWNER_CERTIFIED_FOR_OPERATIONAL_USE":
        errors.append("manifest must state owner operational certification")
    if status.get("runtime_readiness") != "FULL_OPERATIONAL_USE_WITH_EVIDENTIARY_QUALIFICATIONS":
        errors.append("manifest runtime_readiness must state full authorized operational use")

    problems = manifest.get("problems", [])
    keys = [item.get("canonical_key") for item in problems]
    orders = [item.get("canonical_order") for item in problems]
    if keys != CANONICAL_PROBLEM_KEYS:
        errors.append(f"problem order mismatch: {keys!r}")
    if orders != list(range(1, 8)):
        errors.append(f"canonical orders must be 1 through 7: {orders!r}")

    kinds = set(manifest.get("proposition_kinds", []))
    if kinds != REQUIRED_PROPOSITION_KINDS:
        errors.append(f"proposition kinds mismatch: {sorted(kinds)!r}")

    audit = manifest.get("audit", {})
    if audit.get("path") != "audits/operational-completeness.yaml":
        errors.append("manifest must reference the operational completeness audit")

    speech = manifest.get("speech", {})
    if speech.get("contract_version") != "STRAUSS-SPEECH-CONTRACT-1":
        errors.append("manifest speech contract version mismatch")
    if speech.get("completion") != "OPERATIONAL_AND_OWNER_AUTHORIZED":
        errors.append("manifest must state speech completion as operational and owner-authorized")

    safeguards = manifest.get("safeguards", {})
    for required in (
        "independent_reconstruction_before_comparison",
        "documentary_evidence_before_interpretation",
        "preserve_uncertainty",
        "silent_revision_prohibited",
        "predecessor_overwrite_prohibited",
        "cross_problem_absorption_prohibited",
        "poetry_is_not_revelation",
        "irony_is_not_mechanical_inversion",
        "laughter_does_not_certify_wisdom",
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
    if migration.get("mode") != "AUTHORIZED_ADDITIVE_NON_DESTRUCTIVE":
        errors.append("migration mode must be authorized additive non-destructive")

    try:
        mechanism = load_speech_mechanism(manifest)
    except StraussAdapterError as exc:
        errors.append(str(exc))
    else:
        errors.extend(validate_speech_mechanism(mechanism))

    return errors


def _select_problem(manifest: dict[str, Any], canonical_key: str) -> dict[str, Any]:
    for item in manifest["problems"]:
        if item["canonical_key"] == canonical_key:
            return item
    raise StraussAdapterError(f"Unknown problem key: {canonical_key}")


def _validate_required_mapping(
    value: Any,
    fields: Iterable[str],
    label: str,
    errors: list[str],
) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(f"{label} must be a mapping")
        return None
    missing = _missing_or_empty(value, fields)
    if missing:
        errors.append(f"{label} missing or empty fields: {', '.join(missing)}")
    return value


def validate_speech_request(request: dict[str, Any]) -> list[str]:
    """Validate a typed request before any ministerial expression is attempted."""
    errors: list[str] = []
    mechanism = load_speech_mechanism()
    contract = mechanism["input_contract"]

    if not isinstance(request, dict):
        return ["speech request must be a mapping"]

    missing_common = _missing_or_empty(request, contract["required_common_fields"])
    if missing_common:
        errors.append(
            "speech request missing or empty common fields: " + ", ".join(missing_common)
        )

    mode = request.get("mode", "reasoned")
    if mode not in contract["modes"]:
        errors.append(f"unsupported speech mode: {mode!r}")

    inquiry_ref = _validate_required_mapping(
        request.get("inquiry_ref"),
        contract["inquiry_ref_required_fields"],
        "inquiry_ref",
        errors,
    )
    if inquiry_ref and str(inquiry_ref.get("commit", "")).lower() in {"latest", "head", "main"}:
        errors.append("inquiry_ref.commit must be a pinned commit, not a moving ref")

    activated = request.get("activated_problems", [])
    if not isinstance(activated, list):
        errors.append("activated_problems must be a list")
    else:
        invalid = [key for key in activated if key not in CANONICAL_PROBLEM_KEYS]
        if invalid:
            errors.append(f"unregistered activated problems: {invalid!r}")
        if mode == "reasoned" and not activated:
            errors.append("reasoned mode requires at least one activated problem")

    sources = request.get("sources", [])
    if not isinstance(sources, list) or not sources:
        errors.append("sources must be a non-empty list")
    else:
        for index, source in enumerate(sources):
            _validate_required_mapping(
                source,
                contract["source_required_fields"],
                f"sources[{index}]",
                errors,
            )

    _validate_required_mapping(
        request.get("audience"),
        contract["audience_required_fields"],
        "audience",
        errors,
    )

    findings = request.get("findings", [])
    if mode == "reasoned":
        if not isinstance(findings, list) or not findings:
            errors.append("reasoned mode requires a non-empty findings list")
        else:
            for index, finding in enumerate(findings):
                label = f"findings[{index}]"
                mapping = _validate_required_mapping(
                    finding,
                    contract["finding_required_fields"],
                    label,
                    errors,
                )
                if not mapping:
                    continue
                kind = mapping.get("kind")
                if kind not in REQUIRED_PROPOSITION_KINDS:
                    errors.append(f"{label}.kind is not permitted: {kind!r}")
                confidence = mapping.get("confidence")
                if confidence not in ALLOWED_CONFIDENCE_VALUES:
                    errors.append(f"{label}.confidence is not permitted: {confidence!r}")
                evidence = mapping.get("supporting_evidence")
                if not isinstance(evidence, list) or not evidence:
                    errors.append(f"{label}.supporting_evidence must be a non-empty list")
                alternatives = mapping.get("alternatives_considered")
                if not isinstance(alternatives, list):
                    errors.append(f"{label}.alternatives_considered must be a list")
                if kind in {"supported_inference", "working_hypothesis"} and not alternatives:
                    errors.append(f"{label} requires at least one alternative considered")

    if mode == "outside_my_ground":
        missing = _missing_or_empty(
            request, contract["outside_my_ground_required_fields"]
        )
        if missing:
            errors.append(
                "outside_my_ground mode missing or empty fields: " + ", ".join(missing)
            )

    optional = contract["optional_interpretive_records"]

    if "speech_and_deed" in request:
        record = _validate_required_mapping(
            request["speech_and_deed"],
            optional["speech_and_deed"]["required_fields"],
            "speech_and_deed",
            errors,
        )
        if record:
            permitted = set(mechanism["speech_and_deed_contract"]["permitted_relations"])
            if record.get("relation") not in permitted:
                errors.append(
                    f"speech_and_deed.relation is not permitted: {record.get('relation')!r}"
                )

    if "concealment_claim" in request:
        claim = _validate_required_mapping(
            request["concealment_claim"],
            optional["concealment_claim"]["required_fields"],
            "concealment_claim",
            errors,
        )
        if claim:
            evidence = claim.get("positive_evidence")
            if not isinstance(evidence, list) or not evidence:
                errors.append("concealment_claim requires positive_evidence")
            if claim.get("literal_reading_preserved") is not True:
                errors.append(
                    "concealment_claim must preserve the literal reading unless separately eliminated"
                )

    if "irony_claim" in request:
        claim = _validate_required_mapping(
            request["irony_claim"],
            optional["irony_claim"]["required_fields"],
            "irony_claim",
            errors,
        )
        if claim:
            if claim.get("mechanical_reversal") is True:
                errors.append("irony_claim may not use mechanical reversal")
            evidence = claim.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                errors.append("irony_claim.evidence must be a non-empty list")
            if claim.get("literal_meaning_preserved") is not True:
                errors.append(
                    "irony_claim must preserve plausible literal meaning"
                )

    if "comedy_claim" in request:
        claim = _validate_required_mapping(
            request["comedy_claim"],
            optional["comedy_claim"]["required_fields"],
            "comedy_claim",
            errors,
        )
        if claim and claim.get("laughter_certifies_truth") is True:
            errors.append("comedy_claim may not treat laughter as certification")

    return errors


def _normalized_proposition(finding: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": finding["kind"],
        "claim": finding["statement"],
        "grounds": finding["supporting_evidence"],
        "source_location": finding["source_location"],
        "confidence": finding["confidence"],
        "alternatives_considered": finding["alternatives_considered"],
    }


def build_candidate_report(request: dict[str, Any]) -> dict[str, Any]:
    """Build a typed, non-authoritative report structure from a valid request.

    The function preserves classifications and evidence. It does not invent a direct
    answer or perform the interpretation that would supply one.
    """
    errors = validate_speech_request(request)
    if errors:
        raise StraussAdapterError(
            "Speech request validation failed:\n- " + "\n- ".join(errors)
        )

    mode = request.get("mode", "reasoned")
    findings = request.get("findings", [])
    propositions = [_normalized_proposition(item) for item in findings]
    unresolved = [
        item for item in propositions if item["kind"] == "unresolved_uncertainty"
    ]

    report: dict[str, Any] = {
        "record_type": "ministerial_report",
        "id": request.get("report_id", f"{request['request_id']}-strauss-report"),
        "authority": "CANDIDATE_ONLY_UNTIL_SANCTUM_VALIDATION",
        "inquiry_ref": request["inquiry_ref"],
        "minister": {
            "actor": "leo-strauss",
            "repository": "izzy9118-blip/Strauss",
            "manifest_ref": "manifest.yaml",
            "speech_contract": "STRAUSS-SPEECH-CONTRACT-1",
        },
        "mode": mode,
        "governing_question": request["question"],
        "activated_problems": request["activated_problems"],
        "sources": request["sources"],
        "direct_answer": request.get(
            "direct_answer",
            "NOT_GENERATED_BY_ADAPTER: substantive expression requires source-grounded reasoning.",
        ),
        "propositions": propositions,
        "rival_alternatives_and_burdens": request.get(
            "rival_alternatives_and_burdens", []
        ),
        "speech_and_deed": request.get("speech_and_deed"),
        "audience_and_rhetoric": {
            "audience": request["audience"],
            "occasion": request["occasion"],
            "requested_output": request["requested_output"],
        },
        "concealment_irony_and_comedy": {
            "concealment_claim": request.get("concealment_claim"),
            "irony_claim": request.get("irony_claim"),
            "comedy_claim": request.get("comedy_claim"),
        },
        "contradictions_and_dissent": request.get(
            "contradictions_and_dissent", []
        ),
        "unresolved_uncertainties": unresolved
        + request.get("additional_unresolved_uncertainties", []),
        "jurisdiction_and_cross_problem_refs": request.get(
            "jurisdiction_and_cross_problem_refs", []
        ),
        "termination_status": request.get(
            "termination_status",
            "OUTSIDE_MY_GROUND_COMPLETE"
            if mode == "outside_my_ground"
            else "CANDIDATE_REPORT_STRUCTURE_COMPLETE",
        ),
        "provenance": request.get(
            "provenance",
            {
                "produced_by": {
                    "actor": "leo-strauss-adapter",
                    "repo": "izzy9118-blip/Strauss",
                    "commit": "UNCOMMITTED_RUNTIME_CANDIDATE",
                },
                "consumed_records": [request["inquiry_ref"]]
                + [
                    {"ref": source["ref"], "commit": source.get("commit", "UNPINNED")}
                    for source in request["sources"]
                ],
            },
        ),
    }

    if mode == "outside_my_ground":
        report["outside_my_ground"] = {
            "reason": request["outside_my_ground_reason"],
            "limited_documentary_contribution": request[
                "limited_documentary_contribution"
            ],
            "jurisdictional_boundary": request.get(
                "jurisdictional_boundary", "Recorded by the responding minister."
            ),
        }

    return report


def build_context(problem_keys: list[str] | None = None) -> dict[str, Any]:
    manifest = load_manifest()
    errors = validate_manifest(manifest)
    if errors:
        raise StraussAdapterError(
            "Manifest validation failed:\n- " + "\n- ".join(errors)
        )

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
        "audit": load_yaml(_resolve(manifest["audit"]["path"])),
        "component_completion": manifest["component_completion"],
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
        "speech": load_speech_mechanism(manifest),
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
    parser.add_argument(
        "--speech-request",
        type=Path,
        help="Validate a YAML speech request and emit a candidate report structure.",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
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
        print(
            "Strauss operational manifest and speech-contract validation passed; "
            "semantic completion remains incomplete."
        )
        return 0

    if args.speech_request:
        try:
            request = load_yaml(args.speech_request.resolve())
            report = build_candidate_report(request)
        except (StraussAdapterError, OSError) as exc:
            print(f"ERROR: {exc}")
            return 1
        print(json.dumps(report, indent=2 if args.pretty else None, sort_keys=args.pretty))
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
