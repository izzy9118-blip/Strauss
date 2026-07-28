from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(path: str) -> dict:
    with (ROOT / path).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)

class WhyWeRemainJewsCompletionTests(unittest.TestCase):
    def test_source_witness_study_and_status_remain_distinct(self) -> None:
        corpus = load_yaml("corpus/index.yaml")
        source = next(x for x in corpus["source_entities"] if x["source_id"] == "CORPUS-SRC-107")
        witness = next(x for x in corpus["reviewed_witnesses"] if x["witness_id"] == "CORPUS-WIT-107")
        status = load_yaml("studies/theologico-political/why-we-remain-jews/source-status.yaml")
        witness_record = load_yaml("studies/theologico-political/why-we-remain-jews/reviewed-witness.yaml")
        study = load_yaml("studies/theologico-political/why-we-remain-jews/sequential-reconstruction.yaml")
        self.assertEqual(source["reviewed_witnesses"], ["CORPUS-WIT-107"])
        self.assertEqual(source["study_records"], ["CORPUS-STUDY-019"])
        self.assertEqual(witness["printed_page_range"], {"start": 311, "end": 356})
        self.assertEqual(witness["pdf_page_range_one_based"], {"start": 330, "end": 375})
        self.assertEqual(status["status"]["independent_sequential_study"], "WHY-REMAIN-JEWS-STUDY-001")
        self.assertEqual(status["termination"]["study_state"], "COMPLETE_PROVISIONAL")
        self.assertEqual(status["termination"]["documentary_transmission_limit"], "ACTIVE")
        self.assertEqual(study["identity"]["id"], "WHY-REMAIN-JEWS-STUDY-001")
        self.assertEqual(study["termination"]["successor_effect"], "NONE")
        self.assertEqual(witness_record["termination"]["study_state"], "INCOMPLETE")

    def test_speaker_and_editorial_layers_are_preserved(self) -> None:
        study = load_yaml("studies/theologico-political/why-we-remain-jews/sequential-reconstruction.yaml")
        layers = study["speaker_and_documentary_layers"]
        for key in ["cropsey_opening", "strauss_lecture", "editorial_aleinu_translation", "cropsey_post_lecture_comment", "q_and_a_questioners", "strauss_q_and_a", "dannhauser_lane_transcription", "green_editorial_layer"]:
            self.assertIn(key, layers)
        self.assertIn("not read by Strauss", " ".join(study["source_limits"]))
        self.assertEqual(study["source"]["editorial_provenance"]["transcribers"], ["Werner Dannhauser", "James Lane"])
        self.assertEqual(str(study["source"]["editorial_provenance"]["delivery_date"]), "1962-02-04")

    def test_findings_preserve_tp_and_avj_jurisdictions_only(self) -> None:
        findings = load_yaml("findings/index.yaml")
        by_id = {x["finding_set_id"]: x for x in findings["finding_sets"]}
        study = by_id["FINDSET-019"]
        self.assertEqual(study["source_bindings"], ["CORPUS-SRC-107"])
        self.assertEqual(study["problem_bindings"], ["theologico-political", "athens-vs-jerusalem"])
        self.assertEqual(study["derived_local_syntheses"], ["FINDSET-138", "FINDSET-139"])
        self.assertNotIn("ancients-vs-moderns", study["problem_bindings"])
        self.assertEqual(by_id["FINDSET-138"]["derived_from"], ["FINDSET-019"])
        self.assertEqual(by_id["FINDSET-139"]["derived_from"], ["FINDSET-019"])
        self.assertEqual(study["documentary_transmission_limit"], "ACTIVE")
        self.assertEqual(study["independent_corroboration"], "INCOMPLETE")
        self.assertEqual(study["successor_effect"], "NONE")

    def test_forward_completion_language_remains_synchronized_after_src112(self) -> None:
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
