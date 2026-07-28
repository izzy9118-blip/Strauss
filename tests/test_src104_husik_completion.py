from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(relative_path: str) -> dict:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


class HusikPrefaceCompletionTests(unittest.TestCase):
    def test_source_witness_study_and_status_remain_distinct(self) -> None:
        corpus = load_yaml("corpus/index.yaml")
        source = next(x for x in corpus["source_entities"] if x["source_id"] == "CORPUS-SRC-104")
        witness = next(x for x in corpus["reviewed_witnesses"] if x["witness_id"] == "CORPUS-WIT-104")
        status = load_yaml("studies/theologico-political/preface-to-isaac-husik-philosophical-essays/source-status.yaml")
        witness_record = load_yaml("studies/theologico-political/preface-to-isaac-husik-philosophical-essays/reviewed-witness.yaml")
        study = load_yaml("studies/theologico-political/preface-to-isaac-husik-philosophical-essays/sequential-reconstruction.yaml")

        self.assertEqual(source["reviewed_witnesses"], ["CORPUS-WIT-104"])
        self.assertEqual(source["study_records"], ["CORPUS-STUDY-017"])
        self.assertEqual(witness["printed_page_range"], {"start": 235, "end": 266})
        self.assertEqual(witness["pdf_page_range_one_based"], {"start": 254, "end": 285})
        self.assertEqual(status["status"]["independent_sequential_study"], "HUSIK-PREFACE-STUDY-001")
        self.assertEqual(status["termination"]["study_state"], "COMPLETE_PROVISIONAL")
        self.assertEqual(status["termination"]["original_1952_printing_comparison"], "PENDING")
        self.assertEqual(status["termination"]["independent_corroboration"], "INCOMPLETE")
        self.assertEqual(study["identity"]["id"], "HUSIK-PREFACE-STUDY-001")
        self.assertEqual(study["termination"]["reading_state"], "COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS")
        self.assertEqual(study["termination"]["successor_effect"], "NONE")
        self.assertEqual(witness_record["termination"]["study_state"], "INCOMPLETE")

    def test_collective_editorial_layer_is_preserved(self) -> None:
        study = load_yaml("studies/theologico-political/preface-to-isaac-husik-philosophical-essays/sequential-reconstruction.yaml")
        layers = study["speaker_and_documentary_layers"]
        self.assertIn("original_1952_editors_statement", layers)
        self.assertIn("green_1997_editorial_layer", layers)
        self.assertIn("collective editorial layer", " ".join(study["source_limits"]))
        self.assertIn("1997 collected-edition editorial layer", " ".join(study["source_limits"]))

    def test_findings_derivation_preserves_two_problem_jurisdictions_only(self) -> None:
        findings = load_yaml("findings/index.yaml")
        by_id = {x["finding_set_id"]: x for x in findings["finding_sets"]}
        study = by_id["FINDSET-017"]
        self.assertEqual(study["source_bindings"], ["CORPUS-SRC-104"])
        self.assertEqual(study["problem_bindings"], ["theologico-political", "athens-vs-jerusalem"])
        self.assertEqual(study["derived_local_syntheses"], ["FINDSET-134", "FINDSET-135"])
        self.assertNotIn("ancients-vs-moderns", study["problem_bindings"])
        self.assertEqual(by_id["FINDSET-134"]["derived_from"], ["FINDSET-017"])
        self.assertEqual(by_id["FINDSET-134"]["problem_bindings"], ["theologico-political"])
        self.assertEqual(by_id["FINDSET-135"]["derived_from"], ["FINDSET-017"])
        self.assertEqual(by_id["FINDSET-135"]["problem_bindings"], ["athens-vs-jerusalem"])
        self.assertEqual(study["original_1952_printing_comparison"], "PENDING")
        self.assertEqual(study["independent_corroboration"], "INCOMPLETE")
        self.assertEqual(study["successor_effect"], "NONE")

    def test_forward_completion_language_remains_synchronized_after_src106(self) -> None:
        corpus = load_yaml("corpus/index.yaml")
        manifest = load_yaml("manifest.yaml")
        schedule = load_yaml("history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml")
        self.assertEqual(corpus["coverage"]["theologico_political_independent_item_studies_registered"], 19)
        self.assertEqual(corpus["termination"]["theologico_political_independent_study_state"], "COMPLETE_19_OF_19")
        self.assertEqual(manifest["corpus"]["theologico_political_item_level_statuses"]["independent_sequential_study_count"], 19)
        self.assertEqual(schedule["termination"]["independent_sequential_reconstruction"], "COMPLETE_19_OF_19")
        self.assertEqual(schedule["termination"]["next_item_study"], "NONE")


if __name__ == "__main__":
    unittest.main()
