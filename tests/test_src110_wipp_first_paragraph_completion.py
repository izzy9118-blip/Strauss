from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(path: str) -> dict:
    with (ROOT / path).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)

class WippFirstParagraphCompletionTests(unittest.TestCase):
    def test_registered_scope_witness_study_and_status_remain_distinct(self) -> None:
        corpus = load_yaml("corpus/index.yaml")
        source = next(x for x in corpus["source_entities"] if x["source_id"] == "CORPUS-SRC-110")
        witness = next(x for x in corpus["reviewed_witnesses"] if x["witness_id"] == "CORPUS-WIT-110")
        status = load_yaml("studies/theologico-political/what-is-political-philosophy/source-status.yaml")
        witness_record = load_yaml("studies/theologico-political/what-is-political-philosophy/reviewed-witness.yaml")
        study = load_yaml("studies/theologico-political/what-is-political-philosophy/sequential-reconstruction.yaml")
        self.assertEqual(source["reviewed_witnesses"], ["CORPUS-WIT-110"])
        self.assertEqual(source["study_records"], ["CORPUS-STUDY-021"])
        self.assertEqual(source["registered_scope"], "first paragraph")
        self.assertEqual(witness["printed_page_range"], {"start": 409, "end": 409})
        self.assertEqual(witness["pdf_page_range_one_based"], {"start": 428, "end": 428})
        self.assertEqual(status["termination"]["registered_scope"], "FIRST_PARAGRAPH_ONLY")
        self.assertEqual(status["termination"]["study_scope_state"], "COMPLETE_PROVISIONAL_FOR_REGISTERED_SCOPE")
        self.assertEqual(status["termination"]["study_state"], "COMPLETE_PROVISIONAL")
        self.assertEqual(study["termination"]["registered_scope"], "FIRST_PARAGRAPH_ONLY")
        self.assertEqual(witness_record["termination"]["study_state"], "INCOMPLETE")

    def test_predecessor_best_regime_language_is_materially_qualified(self) -> None:
        study = load_yaml("studies/theologico-political/what-is-political-philosophy/sequential-reconstruction.yaml")
        comparison = study["comparison_with_active_predecessor"]
        self.assertEqual(comparison["state"], "PROVISIONAL_RETEST_PARTIAL_CONFIRMATION_WITH_MATERIAL_QUALIFICATION_NO_PROMOTION")
        qualifications = " ".join(comparison["qualifications"])
        self.assertIn("does not itself use the phrase philosophic best regime", qualifications)
        self.assertIn("may not be silently imported", qualifications)
        self.assertEqual(comparison["predecessor_effect"], "NONE")

    def test_findings_preserve_tp_and_structural_avj_jurisdictions_only(self) -> None:
        findings = load_yaml("findings/index.yaml")
        by_id = {x["finding_set_id"]: x for x in findings["finding_sets"]}
        study = by_id["FINDSET-021"]
        self.assertEqual(study["source_bindings"], ["CORPUS-SRC-110"])
        self.assertEqual(study["problem_bindings"], ["theologico-political", "athens-vs-jerusalem"])
        self.assertEqual(study["registered_scope"], "FIRST_PARAGRAPH_ONLY")
        self.assertEqual(study["derived_local_syntheses"], ["FINDSET-142", "FINDSET-143"])
        self.assertEqual(study["predecessor_retest_state"], "PARTIAL_CONFIRMATION_WITH_MATERIAL_QUALIFICATION")
        self.assertEqual(study["successor_effect"], "NONE")

    def test_fourteen_of_nineteen_completion_language_is_synchronized(self) -> None:
        corpus = load_yaml("corpus/index.yaml")
        manifest = load_yaml("manifest.yaml")
        schedule = load_yaml("history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml")
        self.assertEqual(corpus["coverage"]["theologico_political_independent_item_studies_registered"], 14)
        self.assertEqual(corpus["termination"]["theologico_political_independent_study_state"], "INCOMPLETE_14_OF_19")
        self.assertEqual(manifest["corpus"]["theologico_political_item_level_statuses"]["independent_sequential_study_count"], 14)
        self.assertEqual(schedule["termination"]["independent_sequential_reconstruction"], "INCOMPLETE_14_OF_19")
        self.assertEqual(schedule["termination"]["next_item_study"], "CORPUS-SRC-114")

if __name__ == "__main__":
    unittest.main()
