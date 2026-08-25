#!/usr/bin/env python3
"""Sanctum universal adapter boundary for the owner-certified Strauss pin.

This overlay adds only the generic Sanctum transport to the previously certified
minister state. It does not alter the minister corpus, findings, doctrine, or owner
certification. Context assembly and local validation remain sovereign to adapter.py.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any

import adapter

PROTOCOL = "sanctum.adapter.v1"
REPOSITORY = "izzy9118-blip/Strauss"
MINISTER_ID = "leo-strauss"


class SanctumAdapterError(RuntimeError):
    pass


def _head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=adapter.ROOT, capture_output=True, text=True, check=False)
    value = proc.stdout.strip()
    if proc.returncode != 0 or len(value) != 40:
        raise SanctumAdapterError("cannot resolve exact Strauss repository commit")
    return value


def _read_stdin_object() -> dict[str, Any]:
    try:
        value = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise SanctumAdapterError(f"stdin must contain one JSON object: {exc}") from exc
    if not isinstance(value, dict):
        raise SanctumAdapterError("stdin must contain one JSON object")
    return value


def describe() -> dict[str, Any]:
    manifest = adapter.load_manifest()
    return {
        "record_type": "sanctum_adapter_descriptor",
        "protocol": PROTOCOL,
        "minister_id": MINISTER_ID,
        "repository": REPOSITORY,
        "repository_commit": _head(),
        "manifest_path": "manifest.yaml",
        "manifest_version": str(manifest.get("version", manifest.get("identity", {}).get("version", "UNRECORDED"))),
        "commands": ["describe", "validate-interface", "prepare-request", "validate-report"],
        "capabilities": ["reasoned", "outside_my_ground", "minister_local_context", "minister_local_report_validation"],
        "authority": "OWNER_AUTHORIZED_ADAPTER_OVERLAY_NO_DOCTRINAL_CHANGE",
    }


def validate_interface() -> dict[str, Any]:
    manifest = adapter.load_manifest()
    errors = adapter.validate_manifest(manifest)
    if errors:
        raise SanctumAdapterError("; ".join(errors))
    return {
        "record_type": "sanctum_adapter_validation",
        "protocol": PROTOCOL,
        "minister_id": MINISTER_ID,
        "repository_commit": _head(),
        "status": "VALIDATED_INTERFACE_NOT_TRUTH_CERTIFIED",
    }


def prepare_request(request: dict[str, Any]) -> dict[str, Any]:
    if request.get("record_type") != "sanctum_adapter_request":
        raise SanctumAdapterError("record_type must be sanctum_adapter_request")
    if request.get("protocol") != PROTOCOL:
        raise SanctumAdapterError(f"protocol must be {PROTOCOL}")
    if request.get("minister_id") != MINISTER_ID:
        raise SanctumAdapterError("minister_id mismatch")
    pin = request.get("repository_pin")
    if not isinstance(pin, dict) or pin.get("repository") != REPOSITORY:
        raise SanctumAdapterError("repository_pin.repository mismatch")
    head = _head()
    if pin.get("commit") != head:
        raise SanctumAdapterError("repository_pin.commit does not match this exact checkout")
    question = request.get("question")
    if not isinstance(question, str) or not question.strip():
        raise SanctumAdapterError("question must be a non-empty string")
    briefing = request.get("common_briefing")
    if not isinstance(briefing, dict) or not briefing.get("sha256"):
        raise SanctumAdapterError("common_briefing with sha256 is required")
    requested = request.get("problem_keys")
    if requested is not None and not isinstance(requested, list):
        raise SanctumAdapterError("problem_keys must be a list when supplied")
    context = adapter.build_context(requested)
    return {
        "record_type": "sanctum_adapter_prepared_request",
        "protocol": PROTOCOL,
        "minister_id": MINISTER_ID,
        "repository": REPOSITORY,
        "repository_commit": head,
        "inquiry_id": request.get("inquiry_id"),
        "question": question,
        "common_briefing": briefing,
        "context": context,
        "output_rule": "SUBSTANTIVE_JUDGMENT_MUST_RETURN_THROUGH_MINISTER_LOCAL_VALIDATION",
        "certification": "NONE_SELF_CERTIFICATION_PROHIBITED",
    }


def validate_report(report: dict[str, Any]) -> dict[str, Any]:
    if report.get("record_type") != "ministerial_report":
        raise SanctumAdapterError("report record_type must be ministerial_report")
    minister = report.get("minister")
    if not isinstance(minister, dict) or minister.get("actor") != MINISTER_ID:
        raise SanctumAdapterError("report minister.actor mismatch")
    if report.get("certification_status") == "OWNER_CERTIFIED" and report.get("owner_certification") is None:
        raise SanctumAdapterError("owner-certified report requires owner_certification record")
    return {
        "record_type": "sanctum_adapter_report_validation",
        "protocol": PROTOCOL,
        "minister_id": MINISTER_ID,
        "repository_commit": _head(),
        "status": "MINISTER_LOCAL_STRUCTURE_VALIDATED_NOT_OWNER_CERTIFIED",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["describe", "validate-interface", "prepare-request", "validate-report"])
    args = parser.parse_args(argv)
    try:
        if args.command == "describe":
            result = describe()
        elif args.command == "validate-interface":
            result = validate_interface()
        elif args.command == "prepare-request":
            result = prepare_request(_read_stdin_object())
        else:
            result = validate_report(_read_stdin_object())
    except (SanctumAdapterError, adapter.StraussAdapterError, OSError, KeyError, TypeError, ValueError) as exc:
        print(f"SANCTUM ADAPTER ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
