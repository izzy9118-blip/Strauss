from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest

import adapter
import reader_bridge
import sanctum_adapter


class CustosReaderIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.custos_root = reader_bridge.resolve_reader_root(reader_bridge.load_binding())

    def test_operational_activation_loads_the_actual_custos_reader(self) -> None:
        context = adapter.build_context(["philosophy-vs-poetry"], custos_root=self.custos_root)
        reader = context["reader"]
        self.assertEqual(reader["repository"], "izzy9118-blip/custos")
        self.assertEqual(reader["instructions"], (self.custos_root / "CUSTOS.md").read_text())
        self.assertEqual(len(reader["gates"]["outer"]["protocol"]["stages"]), 5)
        self.assertEqual(len(reader["gates"]["inner"]["taxonomy"]["techniques"]), 22)
        self.assertEqual(reader["activation_status"], "READER_CONTEXT_LOADED_NOT_ANALYSIS")
        self.assertNotIn("input", reader)
        self.assertEqual(len(context["problems"]), 1)

    def test_sanctum_preparation_gets_the_same_reader(self) -> None:
        prepared = sanctum_adapter.prepare_request({
            "record_type": "sanctum_adapter_request",
            "protocol": sanctum_adapter.PROTOCOL,
            "minister_id": sanctum_adapter.MINISTER_ID,
            "repository_pin": {"repository": sanctum_adapter.REPOSITORY, "commit": sanctum_adapter._head()},
            "question": "What does the supplied evidence establish?",
            "common_briefing": {"sha256": "a" * 64},
            "problem_keys": ["philosophy-vs-poetry"],
        })
        self.assertEqual(prepared["context"]["reader"]["contract"], "custos.reader-context.v1")

    def test_missing_provider_fails_activation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(reader_bridge.ReaderBridgeError):
                adapter.build_context(custos_root=Path(directory))

    def test_missing_binding_is_not_a_silent_fallback(self) -> None:
        manifest = copy.deepcopy(adapter.load_manifest())
        del manifest["reader"]
        self.assertIn("manifest must bind the Custos Strauss Reader", adapter.validate_manifest(manifest))

    def test_read_without_reasoner_cannot_create_a_completed_run(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "absent"
            with self.assertRaisesRegex(reader_bridge.ReaderBridgeError, "READER_REASONER_REQUIRED"):
                reader_bridge.run_reader(source=Path(directory) / "witness.txt", output=output)
            self.assertFalse(output.exists())

    def test_preparation_resumes_the_explicit_custos_inquiry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "prepared"
            result = reader_bridge.run_reader(
                inquiry="inquiries/thoughts-on-machiavelli/chapter-01-note-01",
                output=output, prepare=True, custos_root=self.custos_root,
            )
            self.assertEqual(result["status"], "PREPARED_FOR_REASONER")
            request = json.loads((output / "reader-request.json").read_text())
            self.assertEqual(request["input"]["kind"], "inquiry")
            self.assertEqual(request["input"]["status"]["inquiry_id"], "TM-CH01-N01")
            self.assertEqual(request["instructions"], (self.custos_root / "CUSTOS.md").read_text())
            self.assertFalse((output / "examination.md").exists())

    def test_cli_delegates_close_and_sweep_to_custos_execution(self) -> None:
        for mode, expected in (
            ("close", "CLOSE_READING_ACT_COMPLETE"),
            ("sweep", "WHOLE_TEXT_SWEEP_COMPLETE"),
        ):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                temp = Path(directory)
                source = temp / "explicit witness.txt"
                source.write_text("A fixed witness for the integration test.\n")
                output = temp / "run"
                reasoner = temp / "fixture reasoner.py"
                # Test transport, contract, and execution; this fixture claims no
                # actual philosophical examination of the supplied sentence.
                reasoner.write_text('''import json, sys
request = json.load(sys.stdin)
assert request["repository"] == "izzy9118-blip/custos"
assert request["contract"] == "custos.reader-request.v1"
assert "ACTIVE STRAUSS READER INSTRUCTIONS" in request["instructions"]
assert len(request["authority_documents"]) == 4
assert request["input"]["kind"] == "source"
assert len(request["gates"]["inner"]["taxonomy"]["techniques"]) == 22
mode = request["reader_mode"]
response = {
    "contract": "custos.reader-response.v1", "mode": mode,
    "examination_markdown": "# Integration fixture\\n\\nReader transport was exercised.",
    "documented_findings": [], "supported_inferences": [], "working_hypotheses": [],
    "uncertainties": [], "inner_gate_evaluations": [],
    "next_textual_act": "Proceed with actual textual examination outside this fixture.",
    "status": "INTEGRATION_FIXTURE",
}
if mode == "close":
    response.update(bounded_inquiry={"question": "Was the source transported?"}, strongest_alternative=None)
else:
    response.update(whole_text_map={"scope": "fixture"}, outer_gate_passes=[], candidate_inquiries=[])
print(json.dumps(response))
''')
                command = f"{shlex.quote(sys.executable)} {shlex.quote(reasoner.name)}"
                result = subprocess.run([
                    sys.executable, str(adapter.ROOT / "adapter.py"),
                    "--custos-root", str(self.custos_root), "--source", str(source),
                    "--mode", mode, "--reasoner-command", command, "--output", str(output),
                ], cwd=temp, env=os.environ.copy(), capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                summary = json.loads(result.stdout)
                self.assertEqual(summary["status"], expected)
                self.assertEqual(summary["reader_commit"], reader_bridge._git(self.custos_root, "rev-parse", "HEAD"))
                self.assertIn("Reader transport was exercised", (output / "examination.md").read_text())
                self.assertEqual(json.loads((output / "run.json").read_text())["status"], expected)

    def test_reasoner_failure_does_not_report_completion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            source = temp / "witness.txt"
            source.write_text("A fixed witness.")
            failing = temp / "fail.py"
            failing.write_text("raise SystemExit(7)\n")
            output = temp / "failed"
            with self.assertRaisesRegex(reader_bridge.ReaderBridgeError, "Reasoner failed"):
                reader_bridge.run_reader(
                    source=source, output=output, custos_root=self.custos_root,
                    reasoner_command=f"{shlex.quote(sys.executable)} {shlex.quote(str(failing))}",
                )
            self.assertFalse((output / "run.json").exists())
            self.assertFalse((output / "examination.md").exists())


if __name__ == "__main__":
    unittest.main()
