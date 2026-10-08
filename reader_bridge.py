"""Load and execute Custos's Strauss Reader without copying its methodology."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import hashlib
import json
import os
import subprocess
import sys
import uuid

import yaml


ROOT = Path(__file__).resolve().parent
PROVIDER = "izzy9118-blip/custos"
CONTEXT_CONTRACT = "custos.reader-context.v1"


class ReaderBridgeError(RuntimeError):
    pass


def load_binding(path: Path | None = None) -> dict[str, Any]:
    path = path or ROOT / "integrations/custos-reader.yaml"
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ReaderBridgeError(f"Cannot load Custos reader binding: {exc}") from exc
    if not isinstance(value, dict):
        raise ReaderBridgeError("Custos reader binding must be a mapping")
    expected = {
        "version": 1,
        "repository": PROVIDER,
        "ref": "main",
        "context_contract": CONTEXT_CONTRACT,
        "request_contract": "custos.reader-request.v1",
        "response_contract": "custos.reader-response.v1",
        "default_mode": "close",
    }
    for key, required in expected.items():
        if value.get(key) != required:
            raise ReaderBridgeError(f"Custos reader binding {key} must be {required!r}")
    if value.get("modes") != ["close", "sweep"]:
        raise ReaderBridgeError("Custos reader binding must declare close and sweep modes")
    pin = value.get("tested_commit", "")
    if not isinstance(pin, str) or len(pin) != 40 or any(c not in "0123456789abcdef" for c in pin):
        raise ReaderBridgeError("Custos reader binding must record a full tested_commit SHA")
    return value


def _git(root: Path, *args: str) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True, timeout=60,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ReaderBridgeError(f"Cannot access Custos checkout: {exc}") from exc
    if proc.returncode != 0:
        raise ReaderBridgeError(f"Custos checkout command failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def resolve_reader_root(binding: dict[str, Any], custos_root: Path | None = None) -> Path:
    """Use an explicit checkout or refresh the managed checkout from Custos/main."""
    override = custos_root or os.environ.get("STRAUSS_CUSTOS_ROOT")
    if override:
        root = Path(override).expanduser().resolve()
    else:
        root = ROOT / ".runtime" / "custos"
        root.mkdir(parents=True, exist_ok=True)
        if not (root / ".git").exists():
            if any(root.iterdir()):
                raise ReaderBridgeError(f"Managed Custos directory is not an empty checkout: {root}")
            _git(root, "init")
            _git(root, "remote", "add", "origin", f"https://github.com/{binding['repository']}.git")
        if _git(root, "remote", "get-url", "origin") != f"https://github.com/{PROVIDER}.git":
            raise ReaderBridgeError("Managed Custos checkout has an unexpected remote")
        _git(root, "fetch", "--depth", "1", "origin", binding["ref"])
        _git(root, "checkout", "--detach", "FETCH_HEAD")

    if not (root / "custos.yaml").is_file() or not (root / "src/custos/cli.py").is_file():
        raise ReaderBridgeError(f"Custos reader checkout is incomplete: {root}")
    if Path(_git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise ReaderBridgeError(f"Custos root must be a repository checkout: {root}")
    dirty = _git(root, "status", "--porcelain", "--", "CUSTOS.md", "custos.yaml", "protocol", "src")
    if dirty:
        raise ReaderBridgeError("Custos reader instructions or code have uncommitted changes; commit them before activation")
    return root


def _custos_command(root: Path, *args: str) -> list[str]:
    return [sys.executable, "-P", "-m", "custos.cli", "--repo-root", str(root), *args]


def _custos_env(root: Path) -> dict[str, str]:
    # The selected checkout must precede installed copies of Custos.
    return {**os.environ, "PYTHONPATH": str(root / "src")}


def load_reader_context(
    *, custos_root: Path | None = None, binding: dict[str, Any] | None = None,
) -> dict[str, Any]:
    binding = binding or load_binding()
    root = resolve_reader_root(binding, custos_root)
    try:
        proc = subprocess.run(
            _custos_command(root, "context"), cwd=root, env=_custos_env(root),
            capture_output=True, text=True, timeout=60,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ReaderBridgeError(f"Cannot load Custos reader context: {exc}") from exc
    if proc.returncode:
        raise ReaderBridgeError(f"Custos reader activation failed: {proc.stderr.strip()}")
    try:
        context = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise ReaderBridgeError("Custos context did not return valid JSON") from exc
    if not isinstance(context, dict) or context.get("contract") != CONTEXT_CONTRACT:
        raise ReaderBridgeError("Custos reader context contract mismatch")
    if context.get("repository") != PROVIDER:
        raise ReaderBridgeError("Custos reader provider mismatch")
    if context.get("repository_commit") != _git(root, "rev-parse", "HEAD"):
        raise ReaderBridgeError("Custos context commit does not match the selected checkout")
    if not isinstance(context.get("instructions"), str) or not context["instructions"].strip():
        raise ReaderBridgeError("Custos did not supply governing Reader instructions")
    documents = context.get("authority_documents")
    if not isinstance(documents, list) or len(documents) != 4:
        raise ReaderBridgeError("Custos did not supply the four Reader authority documents")
    for item in documents:
        if not isinstance(item, dict) or not isinstance(item.get("text"), str):
            raise ReaderBridgeError("Malformed Custos authority document")
        if hashlib.sha256(item["text"].encode("utf-8")).hexdigest() != item.get("sha256"):
            raise ReaderBridgeError("Custos authority document hash mismatch")
    return {**context, "checkout_root": str(root), "default_mode": binding["default_mode"]}


def run_reader(
    *, source: Path | None = None, inquiry: str | None = None, mode: str = "close",
    reasoner_command: str | None = None, output: Path | None = None,
    prepare: bool = False, custos_root: Path | None = None,
) -> dict[str, Any]:
    if (source is None) == (inquiry is None):
        raise ReaderBridgeError("Supply exactly one Reader input: --source or --inquiry")
    if mode not in ("close", "sweep"):
        raise ReaderBridgeError(f"Unknown Reader mode: {mode}")
    if not prepare and not reasoner_command:
        raise ReaderBridgeError("READER_REASONER_REQUIRED: --reasoner-command is required for a completed reading")
    context = load_reader_context(custos_root=custos_root)
    root = Path(context["checkout_root"])
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = (output or ROOT / "runs" / f"{stamp}-{mode}-{uuid.uuid4().hex[:8]}").expanduser().resolve()
    command = ["prepare" if prepare else "read", "--mode", mode, "--output", str(output)]
    if source is not None:
        command.extend(["--source", str(source.expanduser().resolve())])
    else:
        command.extend(["--inquiry", str(inquiry)])
    if not prepare:
        command.extend(["--reasoner-command", str(reasoner_command)])
    try:
        proc = subprocess.run(
            _custos_command(root, *command), env=_custos_env(root),
            capture_output=True, text=True, timeout=1860 if mode == "sweep" else 660,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ReaderBridgeError(f"Custos Reader execution failed: {exc}") from exc
    if proc.returncode:
        raise ReaderBridgeError(f"Custos Reader failed: {proc.stderr.strip()}")
    try:
        run = json.loads((output / "run.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReaderBridgeError("Custos did not preserve a valid Reader run record") from exc
    expected = "PREPARED_FOR_REASONER" if prepare else (
        "CLOSE_READING_ACT_COMPLETE" if mode == "close" else "WHOLE_TEXT_SWEEP_COMPLETE"
    )
    if run.get("status") != expected or run.get("repository_commit") != context["repository_commit"]:
        raise ReaderBridgeError("Custos Reader status or commit does not match the activated Reader")
    return {
        "reader_repository": PROVIDER,
        "reader_commit": context["repository_commit"],
        "reader_mode": mode,
        "status": run["status"],
        "output": str(output),
    }
