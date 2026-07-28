from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(relative_path: str) -> dict:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


class FreudMosesCompletionTests(unittest.TestCase):
    def test_source_witness_study_and_status_remain_distinct(self) -> None:
        corpus = load_yaml("corpus/index.yaml")
        source = next(x for x in corpus["source_entities"] if x["source_id"] == "CORPUS-SRC-106")
        witness = next(x for x in corpus["reviewed_witnesses"] if x["witness_id"] == "CORPUS-WIT-106")
        status = load_yaml("studies/theologico-political/freud-on-moses-and-monotheism/source-status.yaml")
        witness_record = load_yaml("studies/theologico-political/freud-on-moses-and-monotheism/reviewed-witness.yaml")
        study = load_yaml("studies/theologico-political/freud-on-moses-and-monotheism/sequential-reconstruction.yaml")

        self.assertEqual(source["reviewed_witnesses"], ["CORPUS-WIT-106"])
        self.assertEqual(source["study_records"], ["CORPUS-STUDY-018"])
        self.assertEqual(witness["printed_page_range"], {"start": 285, "end": 309})
        self.assertEqual(witness["pdf_page_range_one_based"], {"start": 304, "end": 328})
        self.assertEqual(status["status"]["independent_sequential_study"], "FREUD-MOSES-STUDY-001")
        self.assertEqual(status["termination"]["study_state"], "COMPLETE_PROVISIONAL")
        self.assertEqual(status["termination"]["documentary_transmission_limit"], "ACTIVE")
        self.assertEqual(status["termination"]["independent_corroboration"], "INCOMPLETE")
        self.assertEqual(study["identity"]["id"], "FREUD-MOSES-STUDY-001")
        self.assertEqual(study["termination"]["reading_state"], "COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS")
        self.assertEqual(study["termination"]["successor_effect"], "NONE")
        self.assertEqual(witness_record["termination"]["study_state"], "INCOMPLETE")

    def test_posthumous_transcription_and_editorial_limits_are_preserved(self) -> None:
        status = load_yaml("studies/theologico-political/freud-on-moses-and-monotheism/source-status.yaml")
        study = load_yaml("studies/theologico-political/freud-on-moses-and-monotheism/sequential-reconstruction.yaml")
        publication = status["publication_and_witness_condition"]

        self.assertEqual(publication["source_form"], "POSTHUMOUSLY_PUBLISHED_LECTURE_TRANSCRIPTION")
        self.assertEqual(publication["transcription_state"], "UNKNOWN_TRANSCRIBER_FROM_TAPE_RECORDING")
        self.assertEqual(
            publication["transcript_authorial_approval"],
            "NOT_REVIEWED_OR_FORMALLY_APPROVED_BY_STRAUSS_AS_FAR_AS_COLLECTION_EDITOR_CAN_DETERMINE",
        )
        self.assertEqual(publication["editor_notes_authorship"], "ENTIRELY_KENNETH_HART_GREEN")
        self.assertIn("LIMITED_ADDITIONS_AND_CORRECTIONS", publication["acknowledged_editorial_emendation"])
        self.assertIn("unknown_transcriber", study["speaker_and_documentary_layers"])
        self.assertIn("green_editorial_layer", study["speaker_and_documentary_layers"])

    def test_findings_derivation_preserves_only_registered_problem_jurisdictions(self) -> None:
        findings = load_yaml("findings/index.yaml")
        by_id = {x["finding_set_id"]: x for x in findings["finding_sets"]}
        study = by_id["FINDSET-018"]
        self.assertEqual(study["source_bindings"], ["CORPUS-SRC-106"])
        self.assertEqual(study["problem_bindings"], ["theologico-political", "ancients-vs-moderns"])
        self.assertEqual(study["derived_local_syntheses"], ["FINDSET-136", "FINDSET-137"])
        self.assertNotIn("wise-vs-vulgar", study["problem_bindings"])
        self.assertNotIn("athens-vs-jerusalem", study["problem_bindings"])
        self.assertEqual(by_id["FINDSET-136"]["derived_from"], ["FINDSET-018"])
        self.assertEqual(by_id["FINDSET-136"]["problem_bindings"], ["theologico-political"])
        self.assertEqual(by_id["FINDSET-137"]["derived_from"], ["FINDSET-018"])
        self.assertEqual(by_id["FINDSET-137"]["problem_bindings"], ["ancients-vs-moderns"])
        self.assertEqual(
            study["transcript_authorial_approval"],
            "NOT_REVIEWED_OR_FORMALLY_APPROVED_BY_STRAUSS_AS_FAR_AS_COLLECTION_EDITOR_CAN_DETERMINE",
        )
        self.assertEqual(study["documentary_transmission_limit"], "ACTIVE")
        self.assertEqual(study["independent_corroboration"], "INCOMPLETE")
        self.assertEqual(study["successor_effect"], "NONE")

    def test_eleven_of_nineteen_completion_language_is_synchronized(self) -> None:
        corpus = load_yaml("corpus/index.yaml")
        manifest = load_yaml("manifest.yaml")
        schedule = load_yaml("history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml")
        self.assertEqual(corpus["coverage"]["theologico_political_independent_item_studies_registered"], 11)
        self.assertEqual(corpus["termination"]["theologico_political_independent_study_state"], "INCOMPLETE_11_OF_19")
        self.assertEqual(manifest["corpus"]["theologico_political_item_level_statuses"]["independent_sequential_study_count"], 11)
        self.assertEqual(schedule["termination"]["independent_sequential_reconstruction"], "INCOMPLETE_11_OF_19")
        self.assertEqual(schedule["termination"]["next_item_study"], "CORPUS-SRC-107")


if __name__ == "__main__":
    unittest.main()
