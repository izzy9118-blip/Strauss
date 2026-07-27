from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = (
    ROOT
    / "history"
    / "reviewed-witness-acquisitions"
    / "2026-07-27-preface-spinoza-file-library-witness.yaml"
)


class PrefaceSpinozaAcquisitionCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with RECORD_PATH.open(encoding="utf-8") as handle:
            cls.record = yaml.safe_load(handle)

    def test_source_and_item_identity_are_bounded(self) -> None:
        self.assertEqual(
            self.record["source_identity"]["corpus_source_id"],
            "CORPUS-SRC-102",
        )
        self.assertEqual(
            self.record["source_identity"]["source_status_id"],
            "CORPUS-STATUS-102",
        )
        self.assertEqual(
            self.record["item_identity_and_locators"]["printed_page_range"],
            {"start": 137, "end": 180},
        )
        self.assertEqual(
            self.record["item_identity_and_locators"]["pdf_page_range_one_based"],
            "PENDING_DIRECT_PAGE_IMAGE_SPOT_CHECK",
        )

    def test_missing_byte_identity_is_not_silently_filled(self) -> None:
        fingerprint = self.record["review_condition"]["byte_level_fingerprint"]
        self.assertEqual(fingerprint["algorithm"], "SHA256")
        self.assertEqual(fingerprint["value"], "NOT_AVAILABLE")
        self.assertEqual(
            self.record["review_condition"]["file_size_bytes"],
            "NOT_AVAILABLE",
        )
        self.assertEqual(
            self.record["registration_decision"]["state"],
            "DEFERRED_PENDING_BYTE_LEVEL_IDENTITY_OR_CONTROLLED_PLATFORM_REFERENCE_POLICY",
        )

    def test_acquisition_does_not_claim_registration_or_certification(self) -> None:
        status = self.record["status"]
        termination = self.record["termination"]
        self.assertEqual(status["corpus_registration_effect"], "NONE")
        self.assertEqual(status["independent_sequential_study_effect"], "NONE")
        self.assertEqual(status["successor_activation_effect"], "NONE")
        self.assertEqual(termination["reviewed_witness_registration"], "DEFERRED")
        self.assertEqual(termination["certification"], "NOT_CERTIFIED")
        self.assertEqual(termination["successor_effect"], "NONE")

    def test_editorial_composite_limits_are_explicit(self) -> None:
        provenance = self.record["publication_provenance"]
        self.assertEqual(provenance["original_1965_edition_comparison"], "PENDING")
        self.assertEqual(provenance["final_1968_reprint_comparison"], "PENDING")
        self.assertIn(
            "1965 version",
            provenance["editorial_composite_condition"],
        )
        self.assertIn(
            "1968 Liberalism Ancient and Modern version",
            provenance["editorial_composite_condition"],
        )


if __name__ == "__main__":
    unittest.main()
