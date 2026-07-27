from __future__ import annotations

import unittest

import adapter


HERMENEUTIC_PATHS = {
    "literary-concealment": "hermeneutics/literary-concealment.yaml",
    "whole-and-part": "hermeneutics/whole-and-part.yaml",
    "speaker-and-author": "hermeneutics/speaker-and-author.yaml",
    "audience": "hermeneutics/audience.yaml",
    "contradiction": "hermeneutics/contradiction.yaml",
    "historical-and-philosophical-understanding": (
        "hermeneutics/historical-and-philosophical-understanding.yaml"
    ),
}

COMMON_REQUIRED_SECTIONS = {
    "input_contract",
    "application_sequence",
    "valid_outputs",
    "required_output_fields",
    "prohibited_outputs",
    "speech_mechanism_integration",
    "termination_rule",
    "behavioral_tests",
    "self_limitation",
}


class HermeneuticContractTests(unittest.TestCase):
    def load_contract(self, key: str) -> dict:
        return adapter.load_yaml(adapter._resolve(HERMENEUTIC_PATHS[key]))

    def test_all_six_contracts_are_substantively_reconstructed(self) -> None:
        for key in HERMENEUTIC_PATHS:
            with self.subTest(key=key):
                record = self.load_contract(key)
                self.assertEqual(record["record_type"], "hermeneutic_contract")
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
                self.assertGreaterEqual(len(record["application_sequence"]), 10)
                self.assertGreaterEqual(len(record["behavioral_tests"]), 10)
                self.assertTrue(record["valid_outputs"])
                self.assertTrue(record["required_output_fields"])
                self.assertTrue(record["prohibited_outputs"])

    def test_each_contract_has_an_evidence_burden(self) -> None:
        evidence_sections = {
            "literary-concealment": "positive_evidence_threshold",
            "whole-and-part": "required_evidence",
            "speaker-and-author": "required_evidence",
            "audience": "responsibility_tests",
            "contradiction": "resolution_burdens",
            "historical-and-philosophical-understanding": "required_evidence",
        }
        for key, section in evidence_sections.items():
            with self.subTest(key=key):
                record = self.load_contract(key)
                self.assertIn(section, record)
                self.assertTrue(record[section])

    def test_behavioral_test_ids_are_unique(self) -> None:
        all_ids: list[str] = []
        for key in HERMENEUTIC_PATHS:
            record = self.load_contract(key)
            ids = [test["id"] for test in record["behavioral_tests"]]
            self.assertEqual(len(ids), len(set(ids)))
            all_ids.extend(ids)
        self.assertEqual(len(all_ids), len(set(all_ids)))

    def test_literary_concealment_requires_positive_evidence(self) -> None:
        record = self.load_contract("literary-concealment")
        threshold = record["positive_evidence_threshold"]
        self.assertTrue(threshold["required"])
        self.assertIn("obscurity", threshold["insufficient_by_itself"])
        self.assertIn("persecution", threshold["insufficient_by_itself"])
        self.assertIn("FUNCTION_SUPPORTED_CONTENT_OPAQUE", record["valid_outputs"])
        self.assertIn("OPACITY_PRESERVED", record["valid_outputs"])

    def test_whole_and_part_protects_sequence_and_independence(self) -> None:
        record = self.load_contract("whole-and-part")
        relations = set(record["whole_part_relations"])
        self.assertIn("PART_QUALIFIED_BY_SEQUENCE", relations)
        self.assertIn("PART_REFRAMED_BY_ENDING", relations)
        self.assertIn("CORPUS_PARALLEL_INCOMMENSURABLE", relations)
        rules = "\n".join(record["corpus_comparison_rules"])
        self.assertIn("independently", rules)

    def test_speaker_and_author_preserves_documentary_agents(self) -> None:
        record = self.load_contract("speaker-and-author")
        agents = set(record["input_contract"]["agent_classes"])
        for required in {
            "author",
            "narrator",
            "dramatic_character",
            "editor",
            "translator",
            "quoted_authority",
        }:
            self.assertIn(required, agents)
        self.assertIn(
            "AUTHORIAL_RELATION_UNRESOLVED", record["attribution_relations"]
        )

    def test_audience_contract_preserves_responsibility_and_capture(self) -> None:
        record = self.load_contract("audience")
        self.assertIn("PARTIAL_ENLIGHTENMENT", record["valid_outputs"])
        self.assertIn("ELITE_CAPTURE_RISK", record["valid_outputs"])
        self.assertIn(
            "audience classification remains corrigible and subject to capture review",
            record["behavioral_tests"][8]["behavior"],
        )

    def test_contradiction_can_end_unresolved(self) -> None:
        record = self.load_contract("contradiction")
        self.assertIn("GENUINE_CONTRADICTION_PRESERVED", record["valid_outputs"])
        self.assertIn("CONTRADICTION_UNRESOLVED", record["valid_outputs"])
        prohibited = "\n".join(record["prohibited_outputs"])
        self.assertIn("proof of irony", prohibited)
        self.assertIn("silently harmonized", prohibited)

    def test_historical_and_philosophical_contract_blocks_reduction(self) -> None:
        record = self.load_contract("historical-and-philosophical-understanding")
        controls = "\n".join(record["reduction_controls"])
        self.assertIn("not philosophical refutation", controls)
        self.assertIn("Transhistorical assertion does not establish demonstration", controls)
        self.assertIn(
            "HISTORICAL_AND_PHILOSOPHICAL_RELATION_UNRESOLVED",
            record["valid_outputs"],
        )

    def test_all_contracts_remain_subordinate_to_speech_mechanism(self) -> None:
        for key in HERMENEUTIC_PATHS:
            with self.subTest(key=key):
                record = self.load_contract(key)
                self.assertEqual(
                    record["speech_mechanism_integration"]["contract"],
                    "speech/speech-mechanism.yaml",
                )


if __name__ == "__main__":
    unittest.main()
