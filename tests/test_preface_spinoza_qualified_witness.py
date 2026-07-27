from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(relative_path: str) -> dict:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


class PrefaceSpinozaQualifiedWitnessTests(unittest.TestCase):
    def test_witness_registration_is_qualified_and_relocatable(self) -> None:
        witness = load_yaml(
            "studies/theologico-political/preface-to-spinozas-critique-of-religion/"
            "reviewed-witness.yaml"
        )
        self.assertEqual(witness["identity"]["witness_id"], "CORPUS-WIT-102")
        self.assertEqual(
            witness["status"]["lifecycle"],
            "QUALIFIED_PLATFORM_REFERENCE_WITNESS_REGISTERED",
        )
        self.assertEqual(
            witness["item_locators"]["printed_page_range"],
            {"start": 137, "end": 180},
        )
        self.assertEqual(
            witness["platform_reference"]["platform_object_identifier"],
            "file_0000000073c081fd9fb65f9ea7552cde",
        )

    def test_missing_byte_identity_is_preserved(self) -> None:
        witness = load_yaml(
            "studies/theologico-political/preface-to-spinozas-critique-of-religion/"
            "reviewed-witness.yaml"
        )
        self.assertEqual(
            witness["platform_reference"]["byte_custody_state"],
            "NOT_EXPOSED_TO_REPOSITORY",
        )
        self.assertEqual(witness["byte_identity"]["sha256"], "NOT_AVAILABLE")
        self.assertEqual(
            witness["byte_identity"]["file_size_bytes"],
            "NOT_AVAILABLE",
        )
        self.assertIn(
            "may not be represented as a cryptographic fingerprint",
            witness["byte_identity"]["equivalence_prohibition"],
        )

    def test_witness_registration_does_not_complete_the_study(self) -> None:
        status = load_yaml(
            "studies/theologico-political/preface-to-spinozas-critique-of-religion/"
            "source-status.yaml"
        )
        self.assertEqual(status["status"]["reviewed_witness"], "CORPUS-WIT-102")
        self.assertEqual(
            status["status"]["independent_sequential_study"],
            "NOT_YET_COMPLETED",
        )
        self.assertEqual(status["termination"]["study_state"], "INCOMPLETE")
        self.assertEqual(status["termination"]["certification"], "NOT_CERTIFIED")
        self.assertEqual(status["termination"]["successor_effect"], "NONE")

    def test_corpus_distinguishes_four_witnesses_from_three_studies(self) -> None:
        corpus = load_yaml("corpus/index.yaml")
        self.assertEqual(corpus["identity"]["version"], "1.9.0")
        self.assertEqual(
            corpus["coverage"]["theologico_political_reviewed_item_witnesses_registered"],
            4,
        )
        self.assertEqual(
            corpus["coverage"]["theologico_political_independent_item_studies_registered"],
            3,
        )
        self.assertEqual(
            corpus["termination"]["theologico_political_reviewed_witness_state"],
            "INCOMPLETE_4_OF_19",
        )
        self.assertEqual(
            corpus["termination"]["theologico_political_independent_study_state"],
            "INCOMPLETE_3_OF_19",
        )


if __name__ == "__main__":
    unittest.main()
