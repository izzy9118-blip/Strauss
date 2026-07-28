from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/source-status.yaml"
WITNESS_PATH = "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/reviewed-witness.yaml"
ACQUISITION_PATH = "history/reviewed-witness-acquisitions/2026-07-28-how-to-study-spinoza-uploaded-witness.yaml"
SHA256 = "43e98521c28a9ef8ede1eb7a6507d8ee78d605d0a531624d5dd20075220bda66"


def load_yaml(relative_path: str) -> dict:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{relative_path} must be a YAML mapping")
    return value


class CorpusWit103RegistrationTests(unittest.TestCase):
    def test_witness_identity_and_reproducible_locators(self) -> None:
        witness = load_yaml(WITNESS_PATH)
        self.assertEqual(witness["identity"]["witness_id"], "CORPUS-WIT-103")
        self.assertEqual(witness["identity"]["source_id"], "CORPUS-SRC-103")
        self.assertEqual(witness["container_witness"]["container_sha256"], SHA256)
        self.assertEqual(witness["container_witness"]["container_file_size_bytes"], 39287307)
        self.assertEqual(witness["container_witness"]["container_page_count"], 526)
        self.assertEqual(witness["item_locators"]["printed_page_range"], {"start": 181, "end": 233})
        self.assertEqual(witness["item_locators"]["pdf_page_range_one_based"], {"start": 200, "end": 252})
        self.assertEqual(witness["item_locators"]["argumentative_body_printed_page_range"], {"start": 181, "end": 224})
        self.assertEqual(witness["item_locators"]["notes_printed_page_range"], {"start": 224, "end": 233})

    def test_original_1948_publication_is_provenance_not_reviewed_copy(self) -> None:
        witness = load_yaml(WITNESS_PATH)
        publication = witness["publication_provenance"]
        self.assertEqual(publication["original_publication"]["journal"], "Proceedings of the American Academy for Jewish Research")
        self.assertEqual(publication["original_publication"]["volume"], 17)
        self.assertEqual(publication["original_publication"]["year"], 1948)
        self.assertEqual(publication["original_publication"]["printed_page_range"], {"start": 69, "end": 131})
        self.assertFalse(publication["original_1948_journal_copy_reviewed"])
        self.assertEqual(witness["termination"]["original_edition_comparison"], "PENDING")

    def test_witness_registration_does_not_claim_sequential_study_or_certification(self) -> None:
        witness = load_yaml(WITNESS_PATH)
        status = load_yaml(STATUS_PATH)
        self.assertEqual(witness["status"]["independent_sequential_study"], "NOT_YET_COMPLETED")
        self.assertEqual(witness["termination"]["study_state"], "INCOMPLETE")
        self.assertEqual(status["status"]["independent_sequential_study"], "NOT_YET_COMPLETED")
        self.assertEqual(status["termination"]["study_state"], "INCOMPLETE")
        self.assertEqual(status["termination"]["independent_corroboration"], "INCOMPLETE")
        self.assertEqual(status["termination"]["certification"], "NOT_CERTIFIED")
        self.assertEqual(status["termination"]["successor_effect"], "NONE")

    def test_acquisition_record_matches_registered_witness(self) -> None:
        acquisition = load_yaml(ACQUISITION_PATH)
        self.assertEqual(acquisition["status"]["corpus_registration_effect"], "CORPUS-WIT-103")
        self.assertEqual(acquisition["container_witness"]["sha256"], SHA256)
        self.assertEqual(acquisition["container_witness"]["file_size_bytes"], 39287307)
        self.assertEqual(acquisition["item_identity_and_locators"]["printed_page_range"], {"start": 181, "end": 233})
        self.assertEqual(acquisition["item_identity_and_locators"]["pdf_page_range_one_based"], {"start": 200, "end": 252})
        self.assertEqual(acquisition["publication_provenance"]["original_1948_journal_copy_comparison"], "PENDING")
        self.assertEqual(acquisition["termination"]["sequential_study_state"], "NOT_STARTED_BY_THIS_RECORD")
        self.assertEqual(acquisition["termination"]["successor_effect"], "NONE")


if __name__ == "__main__":
    unittest.main()
