from __future__ import annotations

import copy
import unittest

import adapter


class StraussAdapterTests(unittest.TestCase):
    def valid_request(self) -> dict:
        return {
            "request_id": "req-001",
            "inquiry_ref": {"ref": "inq-001", "commit": "abc123def456"},
            "question": "What does the source establish about philosophy and poetry?",
            "activated_problems": [
                "philosophy-vs-poetry",
                "theologico-political",
            ],
            "sources": [
                {
                    "ref": "studies/example/source.yaml",
                    "commit": "source123",
                    "documentary_status": "AUTHOR_PUBLISHED_PRIMARY_SOURCE",
                    "limits": "Registered translation and documentary limits remain explicit.",
                }
            ],
            "audience": {
                "immediate": "Assembly inquiry",
                "wider": "human operator and later documentary reviewers",
                "purpose": "source-grounded ministerial analysis",
                "capacities": ["can inspect evidence and classifications"],
                "attachments": ["may expect a decisive conclusion"],
                "risks": ["premature closure", "false certainty"],
            },
            "occasion": "bounded documentary inquiry",
            "requested_output": "typed ministerial report",
            "mode": "reasoned",
            "findings": [
                {
                    "kind": "documented_finding",
                    "statement": "The source explicitly presents rival claims.",
                    "supporting_evidence": [
                        {"ref": "studies/example/source.yaml", "location": "lines 10-20"}
                    ],
                    "source_location": "lines 10-20",
                    "confidence": "HIGH",
                    "alternatives_considered": [
                        "no serious alternative identified at this source location"
                    ],
                },
                {
                    "kind": "unresolved_uncertainty",
                    "statement": "The source does not settle the final rank of the rivals.",
                    "supporting_evidence": [
                        {"ref": "studies/example/source.yaml", "location": "ending"}
                    ],
                    "source_location": "ending",
                    "confidence": "MODERATE",
                    "alternatives_considered": [
                        "the ending may deliberately preserve the rivalry"
                    ],
                },
            ],
            "speech_and_deed": {
                "explicit_statement": "The speaker claims superiority.",
                "speaker_or_agent": "represented speaker",
                "immediate_audience": "represented audience",
                "wider_audience": "reader",
                "occasion": "public contest",
                "action_performed": "the work subjects the claim to testing",
                "outcome": "the claim is qualified but not mechanically reversed",
                "documentary_layer": "dramatic representation",
                "relation": "DEED_QUALIFIES_SPEECH",
                "remaining_uncertainty": "final rank remains unresolved",
            },
        }

    def test_manifest_validates(self) -> None:
        manifest = adapter.load_manifest()
        self.assertEqual(adapter.validate_manifest(manifest), [])

    def test_manifest_admits_incomplete_semantic_state(self) -> None:
        manifest = adapter.load_manifest()
        self.assertEqual(manifest["status"]["semantic_completion"], "INCOMPLETE")
        self.assertEqual(manifest["status"]["runtime_readiness"], "FULL_OPERATIONAL_USE_WITH_EVIDENTIARY_QUALIFICATIONS")
        self.assertEqual(
            manifest["audit"]["path"], "audits/operational-completeness.yaml"
        )

    def test_seven_problems_load_in_canonical_order(self) -> None:
        context = adapter.build_context()
        keys = [item["declaration"]["canonical_key"] for item in context["problems"]]
        self.assertEqual(keys, adapter.CANONICAL_PROBLEM_KEYS)

    def test_single_problem_selection(self) -> None:
        context = adapter.build_context(["philosophy-vs-poetry"])
        self.assertEqual(len(context["problems"]), 1)
        self.assertEqual(
            context["problems"][0]["declaration"]["canonical_key"],
            "philosophy-vs-poetry",
        )

    def test_brother_problem_is_preserved(self) -> None:
        context = adapter.build_context(
            ["philosophy-vs-poetry", "theologico-political"]
        )
        records = {
            item["declaration"]["canonical_key"]: item["record"]
            for item in context["problems"]
        }
        pvp = records["philosophy-vs-poetry"]
        tp = records["theologico-political"]
        self.assertIn("brother_problem_designation", pvp)
        self.assertIn("brother_problem_designation", tp)
        self.assertEqual(
            pvp["brother_problem_designation"]["related_problem"],
            "theologico-political",
        )
        self.assertEqual(
            tp["brother_problem_designation"]["related_problem"],
            "philosophy-vs-poetry",
        )

    def test_non_destructive_and_non_certifying_safeguards(self) -> None:
        manifest = adapter.load_manifest()
        self.assertEqual(manifest["migration"]["mode"], "AUTHORIZED_ADDITIVE_NON_DESTRUCTIVE")
        self.assertTrue(manifest["safeguards"]["predecessor_overwrite_prohibited"])
        self.assertTrue(
            manifest["safeguards"]["repository_self_certification_prohibited"]
        )
        self.assertTrue(
            manifest["safeguards"][
                "artificial_intelligence_self_certification_prohibited"
            ]
        )

    def test_unknown_problem_fails(self) -> None:
        with self.assertRaises(adapter.StraussAdapterError):
            adapter.build_context(["not-a-problem"])

    def test_speech_contract_is_semantically_valid(self) -> None:
        mechanism = adapter.load_speech_mechanism()
        self.assertEqual(adapter.validate_speech_mechanism(mechanism), [])
        self.assertEqual(
            mechanism["identity"]["contract_version"],
            "STRAUSS-SPEECH-CONTRACT-1",
        )
        self.assertEqual(
            mechanism["concealment_contract"]["threshold"],
            "POSITIVE_EVIDENCE_REQUIRED",
        )

    def test_valid_speech_request_builds_candidate_report(self) -> None:
        request = self.valid_request()
        self.assertEqual(adapter.validate_speech_request(request), [])
        report = adapter.build_candidate_report(request)
        self.assertEqual(report["record_type"], "ministerial_report")
        self.assertEqual(
            report["authority"], "CANDIDATE_ONLY_UNTIL_SANCTUM_VALIDATION"
        )
        self.assertEqual(len(report["propositions"]), 2)
        self.assertEqual(len(report["unresolved_uncertainties"]), 1)
        self.assertIn("NOT_GENERATED_BY_ADAPTER", report["direct_answer"])

    def test_documented_finding_without_evidence_is_rejected(self) -> None:
        request = self.valid_request()
        request["findings"][0]["supporting_evidence"] = []
        errors = adapter.validate_speech_request(request)
        self.assertTrue(any("supporting_evidence" in error for error in errors))

    def test_mechanical_irony_is_rejected(self) -> None:
        request = self.valid_request()
        request["irony_claim"] = {
            "explicit_statement": "I know nothing.",
            "disparity": "the speaker performs an examination",
            "function": "qualification",
            "evidence": [{"ref": "source", "location": "passage"}],
            "audience": "public audience",
            "consequence": "claim is narrowed",
            "literal_meaning_preserved": True,
            "remaining_uncertainty": "scope of knowledge remains disputed",
            "mechanical_reversal": True,
        }
        errors = adapter.validate_speech_request(request)
        self.assertIn("irony_claim may not use mechanical reversal", errors)

    def test_concealment_without_positive_evidence_is_rejected(self) -> None:
        request = self.valid_request()
        request["concealment_claim"] = {
            "affected_claim": "public statement",
            "positive_evidence": [],
            "proposed_function": "protection",
            "literal_reading_preserved": True,
            "alternatives_considered": ["ordinary ambiguity"],
        }
        errors = adapter.validate_speech_request(request)
        self.assertIn("concealment_claim requires positive_evidence", errors)

    def test_laughter_cannot_certify_truth(self) -> None:
        request = self.valid_request()
        request["comedy_claim"] = {
            "comic_signal": "ridicule",
            "who_laughs": "represented audience",
            "target": "solemn claimant",
            "action": "title is exposed by conduct",
            "consequence": "rank is qualified",
            "disclosed_disproportion": "claim exceeds capacity",
            "serious_issue_preserved": "the underlying problem remains",
            "self_implication": "the laugher remains subject to examination",
            "remaining_uncertainty": "complete rank is unresolved",
            "laughter_certifies_truth": True,
        }
        errors = adapter.validate_speech_request(request)
        self.assertIn("comedy_claim may not treat laughter as certification", errors)

    def test_outside_my_ground_is_a_complete_typed_response(self) -> None:
        request = self.valid_request()
        request["mode"] = "outside_my_ground"
        request["activated_problems"] = ["theory-vs-practice"]
        request.pop("findings")
        request["outside_my_ground_reason"] = (
            "The inquiry asks for a technical determination not governed by political philosophy."
        )
        request["limited_documentary_contribution"] = (
            "The source status and framing limits can still be recorded."
        )
        self.assertEqual(adapter.validate_speech_request(request), [])
        report = adapter.build_candidate_report(request)
        self.assertEqual(report["termination_status"], "OUTSIDE_MY_GROUND_COMPLETE")
        self.assertIn("outside_my_ground", report)

    def test_source_commit_cannot_be_a_moving_ref(self) -> None:
        request = self.valid_request()
        request["inquiry_ref"]["commit"] = "main"
        errors = adapter.validate_speech_request(request)
        self.assertTrue(any("pinned commit" in error for error in errors))

    def test_speech_request_validation_does_not_mutate_input(self) -> None:
        request = self.valid_request()
        original = copy.deepcopy(request)
        adapter.validate_speech_request(request)
        self.assertEqual(request, original)


if __name__ == "__main__":
    unittest.main()
