from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(path: str) -> dict:
    with (ROOT / path).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)

class StateOfIsraelLetterCompletionTests(unittest.TestCase):
    def test_source_witness_study_and_status_remain_distinct(self) -> None:
        corpus = load_yaml("corpus/index.yaml")
        source = next(x for x in corpus["source_entities"] if x["source_id"] == "CORPUS-SRC-112")
        witness = next(x for x in corpus["reviewed_witnesses"] if x["witness_id"] == "CORPUS-WIT-112")
        status = load_yaml("studies/theologico-political/letter-to-editor-state-of-israel/source-status.yaml")
        witness_record = load_yaml("studies/theologico-political/letter-to-editor-state-of-israel/reviewed-witness.yaml")
        study = load_yaml("studies/theologico-political/letter-to-editor-state-of-israel/sequential-reconstruction.yaml")
        self.assertEqual(source["reviewed_witnesses"], ["CORPUS-WIT-112"])
        self.assertEqual(source["study_records"], ["CORPUS-STUDY-020"])
        self.assertEqual(witness["printed_page_range"], {"start": 413, "end": 414})
        self.assertEqual(witness["pdf_page_range_one_based"], {"start": 432, "end": 433})
        self.assertEqual(status["status"]["independent_sequential_study"], "STATE-ISRAEL-LETTER-STUDY-001")
        self.assertEqual(status["termination"]["study_state"], "COMPLETE_PROVISIONAL")
        self.assertEqual(status["termination"]["original_1957_national_review_comparison"], "PENDING")
        self.assertEqual(study["identity"]["id"], "STATE-ISRAEL-LETTER-STUDY-001")
        self.assertEqual(study["termination"]["successor_effect"], "NONE")
        self.assertEqual(witness_record["termination"]["study_state"], "INCOMPLETE")

    def test_predecessor_theological_language_is_materially_qualified(self) -> None:
        study = load_yaml("studies/theologico-political/letter-to-editor-state-of-israel/sequential-reconstruction.yaml")
        comparison = study["comparison_with_active_predecessor"]
        self.assertEqual(comparison["state"], "PROVISIONAL_RETEST_PARTIAL_CONFIRMATION_WITH_MATERIAL_QUALIFICATION_NO_PROMOTION")
        qualifications = " ".join(comparison["qualifications"])
        self.assertIn("does not explicitly use the language of redemption, messianic fulfillment, or providence", qualifications)
        self.assertIn("Political necessity is less explicit than political dignity and moral force", qualifications)
        self.assertEqual(comparison["predecessor_effect"], "NONE")

    def test_findings_preserve_tp_and_ancients_moderns_jurisdictions_only(self) -> None:
        findings = load_yaml("findings/index.yaml")
        by_id = {x["finding_set_id"]: x for x in findings["finding_sets"]}
        study = by_id["FINDSET-020"]
        self.assertEqual(study["source_bindings"], ["CORPUS-SRC-112"])
        self.assertEqual(study["problem_bindings"], ["theologico-political", "ancients-vs-moderns"])
        self.assertEqual(study["derived_local_syntheses"], ["FINDSET-140", "FINDSET-141"])
        self.assertNotIn("athens-vs-jerusalem", study["problem_bindings"])
        self.assertEqual(study["predecessor_retest_state"], "PARTIAL_CONFIRMATION_WITH_MATERIAL_QUALIFICATION")
        self.assertEqual(study["independent_corroboration"], "INCOMPLETE")
        self.assertEqual(study["successor_effect"], "NONE")

    def test_thirteen_of_nineteen_completion_language_is_synchronized(self) -> None:
        corpus = load_yaml("corpus/index.yaml")
        manifest = load_yaml("manifest.yaml")
        schedule = load_yaml("history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml")
        self.assertEqual(corpus["coverage"]["theologico_political_independent_item_studies_registered"], 13)
        self.assertEqual(corpus["termination"]["theologico_political_independent_study_state"], "INCOMPLETE_13_OF_19")
        self.assertEqual(manifest["corpus"]["theologico_political_item_level_statuses"]["independent_sequential_study_count"], 13)
        self.assertEqual(schedule["termination"]["independent_sequential_reconstruction"], "INCOMPLETE_13_OF_19")
        self.assertEqual(schedule["termination"]["next_item_study"], "CORPUS-SRC-110")

if __name__ == "__main__":
    unittest.main()
