"""Regression tests for the bounded CORPUS-WIT-102 platform-reference state."""

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(relative_path: str) -> dict:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


class CorpusWitness102PlatformRegistrationTests(unittest.TestCase):
    def test_witness_meets_platform_reference_minimums(self) -> None:
        protocol = load_yaml("protocols/platform-reference-witness.yaml")
        witness = load_yaml(
            "studies/theologico-political/preface-to-spinozas-critique-of-religion/reviewed-witness.yaml"
        )
        status = load_yaml(
            "studies/theologico-political/preface-to-spinozas-critique-of-religion/source-status.yaml"
        )

        self.assertEqual(protocol["identity"]["protocol_version"], "1.0.0")
        self.assertEqual(witness["identity"]["witness_id"], "CORPUS-WIT-102")
        self.assertEqual(
            witness["status"]["lifecycle"],
            "QUALIFIED_PLATFORM_REFERENCE_WITNESS_REGISTERED",
        )
        self.assertEqual(
            witness["platform_reference"]["platform_object_identifier"],
            "file_0000000073c081fd9fb65f9ea7552cde",
        )
        self.assertEqual(
            witness["item_identity_and_locators"]["printed_page_range"],
            {"start": 137, "end": 180},
        )
        self.assertEqual(
            witness["byte_identity"]["byte_custody_state"],
            "NOT_EXPOSED_TO_REPOSITORY",
        )
        self.assertEqual(
            witness["byte_identity"]["sha256_state"],
            "UNAVAILABLE_WITH_REASON_PRESERVED",
        )
        self.assertEqual(
            status["termination"]["reviewed_witness_state"],
            "REGISTERED_QUALIFIED_PLATFORM_REFERENCE",
        )

    def test_historical_registration_remains_noncertifying_after_forward_study(self) -> None:
        witness = load_yaml(
            "studies/theologico-political/preface-to-spinozas-critique-of-religion/reviewed-witness.yaml"
        )
        status = load_yaml(
            "studies/theologico-political/preface-to-spinozas-critique-of-religion/source-status.yaml"
        )
        corpus = load_yaml("corpus/index.yaml")

        self.assertEqual(witness["termination"]["study_state"], "INCOMPLETE")
        self.assertEqual(witness["termination"]["certification"], "NOT_CERTIFIED")
        self.assertEqual(witness["termination"]["successor_effect"], "NONE")
        self.assertEqual(
            status["status"]["independent_sequential_study"],
            "SPINOZA-PREFACE-STUDY-001",
        )
        self.assertEqual(
            corpus["termination"]["theologico_political_reviewed_witness_state"],
            "INCOMPLETE_4_OF_19",
        )
        self.assertEqual(
            corpus["termination"]["theologico_political_independent_study_state"],
            "INCOMPLETE_4_OF_19",
        )

    def test_acquisition_record_remains_historically_distinct(self) -> None:
        acquisition = load_yaml(
            "history/reviewed-witness-acquisitions/2026-07-27-preface-spinoza-file-library-witness.yaml"
        )
        self.assertEqual(acquisition["status"]["corpus_registration_effect"], "NONE")
        self.assertEqual(
            acquisition["termination"]["reviewed_witness_registration"],
            "DEFERRED",
        )
        self.assertEqual(
            acquisition["registration_decision"]["state"],
            "DEFERRED_PENDING_BYTE_LEVEL_IDENTITY_OR_CONTROLLED_PLATFORM_REFERENCE_POLICY",
        )


if __name__ == "__main__":
    unittest.main()
