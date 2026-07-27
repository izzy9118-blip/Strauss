from __future__ import annotations

import unittest

import adapter


METHOD_PATHS = {
    "recover-question": "method/recover-question.yaml",
    "reconstruct-alternatives": "method/reconstruct-alternatives.yaml",
    "textual-order": "method/textual-order.yaml",
    "preserve-problem": "method/preserve-problem.yaml",
}

COMMON_REQUIRED_SECTIONS = {
    "input_contract",
    "application_sequence",
    "valid_outputs",
    "required_output_fields",
    "failure_recovery",
    "termination_rule",
    "behavioral_tests",
    "speech_mechanism_integration",
    "self_limitation",
}


class MethodContractTests(unittest.TestCase):
    def load_contract(self, key: str) -> dict:
        return adapter.load_yaml(adapter._resolve(METHOD_PATHS[key]))

    def test_all_four_methods_are_substantively_reconstructed(self) -> None:
        for key in METHOD_PATHS:
            with self.subTest(key=key):
                record = self.load_contract(key)
                self.assertEqual(record["record_type"], "inquiry_method_contract")
                self.assertEqual(record["identity"]["key"], key)
                self.assertEqual(record["identity"]["version"], "1.1.0")
                self.assertEqual(
                    record["status"]["semantic_completion"],
                    "SUBSTANTIVELY_RECONSTRUCTED",
                )
                self.assertEqual(record["status"]["certification"], "NOT_CERTIFIED")
                self.assertEqual(
                    record["status"]["source_specific_application"],
                    "INCOMPLETE",
                )
                self.assertTrue(COMMON_REQUIRED_SECTIONS.issubset(record))
                self.assertTrue(
                    "failure_conditions" in record or "prohibitions" in record,
                    f"{key} must declare failure conditions or explicit prohibitions",
                )
                self.assertGreaterEqual(len(record["application_sequence"]), 12)
                self.assertGreaterEqual(len(record["behavioral_tests"]), 10)

    def test_method_behavior_ids_are_unique(self) -> None:
        all_ids: list[str] = []
        for key in METHOD_PATHS:
            record = self.load_contract(key)
            ids = [item["id"] for item in record["behavioral_tests"]]
            self.assertEqual(len(ids), len(set(ids)))
            all_ids.extend(ids)
        self.assertEqual(len(all_ids), len(set(all_ids)))

    def test_recover_question_keeps_question_distinctions(self) -> None:
        record = self.load_contract("recover-question")
        distinctions = record["question_distinctions"]
        for required in {
            "user_question",
            "source_explicit_question",
            "governing_question",
            "topical_label",
            "doctrinal_proposition",
            "repository_problem_route",
        }:
            self.assertIn(required, distinctions)
        self.assertIn("DOCTRINAL_SUBSTITUTION_REJECTED", record["valid_outputs"])
        self.assertIn("MULTIPLE_GOVERNING_QUESTIONS_PRESERVED", record["valid_outputs"])

    def test_reconstruct_alternatives_requires_independence(self) -> None:
        record = self.load_contract("reconstruct-alternatives")
        blocked = "\n".join(record["independence_gate"]["blocked_if"])
        self.assertIn("reconstructed primarily through its rival", blocked)
        self.assertIn("COMPARISON_GATE_BLOCKED", record["valid_outputs"])
        self.assertIn("VICTOR_NOT_ESTABLISHED", record["valid_outputs"])
        self.assertIn("RECIPROCAL_BURDEN_REMAINS", record["burden_contract"]["burden_statuses"])

    def test_textual_order_requires_reproducibility(self) -> None:
        record = self.load_contract("textual-order")
        required = set(record["reproducibility_requirements"])
        self.assertTrue(any("edition or translation" in item for item in required))
        self.assertTrue(any("ordered unit identifiers" in item for item in required))
        self.assertIn("THEMATIC_FINDING_NOT_SEQUENCE_GROUNDED", record["valid_outputs"])
        self.assertIn("ENDING_PRESERVES_PROBLEM", record["valid_outputs"])

    def test_preserve_problem_accepts_affirmative_nonresolution(self) -> None:
        record = self.load_contract("preserve-problem")
        self.assertIn("AFFIRMATIVE_NON_RESOLUTION", record["resolution_states"])
        self.assertIn("AFFIRMATIVE_NON_RESOLUTION", record["valid_outputs"])
        self.assertIn("PRACTICAL_SETTLEMENT_ONLY", record["resolution_states"])
        self.assertIn("TRANSFER", record["migration_preservation"]["dispositions"])
        self.assertIn("ELEVATE", record["migration_preservation"]["dispositions"])
        self.assertIn("silent closure", record["prohibitions"])

    def test_all_methods_feed_speech_without_certifying(self) -> None:
        for key in METHOD_PATHS:
            with self.subTest(key=key):
                record = self.load_contract(key)
                self.assertEqual(
                    record["speech_mechanism_integration"]["contract"],
                    "speech/speech-mechanism.yaml",
                )
                self.assertIn("does not", record["self_limitation"].lower())


if __name__ == "__main__":
    unittest.main()
