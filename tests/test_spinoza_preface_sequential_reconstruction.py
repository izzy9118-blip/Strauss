from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
STUDY_PATH = (
    ROOT
    / "studies"
    / "theologico-political"
    / "preface-to-spinozas-critique-of-religion"
    / "sequential-reconstruction.yaml"
)
STATUS_PATH = STUDY_PATH.with_name("source-status.yaml")
WITNESS_PATH = STUDY_PATH.with_name("reviewed-witness.yaml")
TP_SYNTHESIS_PATH = (
    ROOT
    / "problems"
    / "theologico-political"
    / "synthesis"
    / "preface-to-spinozas-critique-of-religion.yaml"
)
AVJ_SYNTHESIS_PATH = (
    ROOT
    / "problems"
    / "athens-vs-jerusalem"
    / "synthesis"
    / "preface-to-spinozas-critique-of-religion.yaml"
)
AVM_SYNTHESIS_PATH = (
    ROOT
    / "problems"
    / "ancients-vs-moderns"
    / "synthesis"
    / "preface-to-spinozas-critique-of-religion.yaml"
)


def load(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"{path} must contain a mapping")
    return data


class SpinozaPrefaceSequentialReconstructionTests(unittest.TestCase):
    def test_study_is_complete_provisional_and_ordered(self) -> None:
        study = load(STUDY_PATH)
        self.assertEqual(study["identity"]["id"], "SPINOZA-PREFACE-STUDY-001")
        self.assertEqual(
            study["status"]["source_reading"],
            "COMPLETE_FOR_QUALIFIED_1997_PLATFORM_REFERENCE_WITNESS",
        )
        self.assertEqual(len(study["sequential_reading"]), 10)
        self.assertEqual(
            [unit["unit"] for unit in study["sequential_reading"]],
            [f"SPINOZA-PREFACE-RU-{number:03d}" for number in range(1, 11)],
        )
        self.assertEqual(len(study["permanent_source_level_findings"]), 12)
        self.assertEqual(study["termination"]["certification"], "NOT_CERTIFIED")
        self.assertEqual(study["termination"]["successor_effect"], "NONE")
        self.assertEqual(study["termination"]["predecessor_displacement_effect"], "NONE")

    def test_platform_reference_and_editorial_composite_limits_remain_explicit(self) -> None:
        study = load(STUDY_PATH)
        source = study["source"]
        platform = source["platform_reference"]
        self.assertEqual(platform["platform_object_identifier"], "file_0000000073c081fd9fb65f9ea7552cde")
        self.assertEqual(platform["byte_custody_state"], "NOT_EXPOSED_TO_REPOSITORY")
        self.assertEqual(platform["sha256_state"], "UNAVAILABLE_WITH_REASON_PRESERVED")
        self.assertEqual(platform["file_size_state"], "NOT_AVAILABLE")
        self.assertEqual(source["locators"]["pdf_pages_one_based"], "PENDING_DIRECT_OFFSET_VERIFICATION")
        self.assertEqual(
            source["textual_state"],
            "1997_EDITORIAL_COMPOSITE_BASED_ESSENTIALLY_ON_1965_WITH_MOST_1968_CHANGES",
        )
        self.assertEqual(study["status"]["original_1965_edition_comparison"], "PENDING")
        self.assertEqual(study["status"]["authorial_1968_reprint_comparison"], "PENDING")
        witness = load(WITNESS_PATH)
        self.assertEqual(witness["termination"]["study_state"], "INCOMPLETE")
        self.assertEqual(witness["termination"]["certification"], "NOT_CERTIFIED")

    def test_reason_revelation_distinctions_are_not_collapsed(self) -> None:
        study = load(STUDY_PATH)
        findings = {
            item["id"]: item["proposition"]
            for item in study["permanent_source_level_findings"]
        }
        self.assertIn("historical and political defeat", findings["SPINOZA-PREFACE-PF-003"])
        self.assertIn("clear and exhaustive account", findings["SPINOZA-PREFACE-PF-007"])
        self.assertIn("does not refute revelation understood as a possibility", findings["SPINOZA-PREFACE-PF-008"])
        self.assertIn("not proof of revelation", findings["SPINOZA-PREFACE-PF-009"])
        self.assertIn("not evidence that a miracle occurred", findings["SPINOZA-PREFACE-PF-009"])
        self.assertIn("reopens rather than settles", findings["SPINOZA-PREFACE-PF-010"])

    def test_predecessor_is_retested_without_promotion_or_displacement(self) -> None:
        study = load(STUDY_PATH)
        comparison = study["comparison_with_active_predecessor"]
        self.assertEqual(
            comparison["statement_status"],
            "PREDECESSOR_SYNTHESIS_PARAPHRASE_NOT_SOURCE_QUOTATION",
        )
        self.assertEqual(comparison["state"], "PROVISIONAL_RETEST_COMPLETE_NO_PROMOTION")
        self.assertEqual(comparison["predecessor_effect"], "NONE")
        self.assertEqual(comparison["migration_effect"], "NONE")
        self.assertEqual(comparison["successor_activation_effect"], "NONE")
        status = load(STATUS_PATH)
        self.assertEqual(status["termination"]["study_id"], "SPINOZA-PREFACE-STUDY-001")
        self.assertEqual(status["termination"]["independent_corroboration"], "INCOMPLETE")
        self.assertEqual(status["termination"]["certification"], "NOT_CERTIFIED")
        self.assertEqual(status["termination"]["successor_effect"], "NONE")

    def test_problem_syntheses_preserve_primary_jurisdiction(self) -> None:
        tp = load(TP_SYNTHESIS_PATH)
        avj = load(AVJ_SYNTHESIS_PATH)
        avm = load(AVM_SYNTHESIS_PATH)
        self.assertEqual(tp["identity"]["problem"], "theologico-political")
        self.assertEqual(avj["identity"]["problem"], "athens-vs-jerusalem")
        self.assertEqual(avm["identity"]["problem"], "ancients-vs-moderns")
        self.assertEqual(tp["status"]["successor_effect"], "NONE_WITHOUT_CERTIFIED_MIGRATION")
        self.assertEqual(avj["termination"]["theologico_political_precedence"], "PRESERVED")
        self.assertEqual(avm["termination"]["theologico_political_precedence"], "PRESERVED")
        for record in (tp, avj, avm):
            self.assertEqual(record["status"]["certification"], "NOT_CERTIFIED")
            self.assertEqual(record["termination"]["certification"], "NOT_CERTIFIED")

    def test_prohibitions_preserve_documentary_safeguards(self) -> None:
        study = load(STUDY_PATH)
        joined = "\n".join(study["prohibitions"])
        self.assertIn("Do not infer the actuality of revelation", joined)
        self.assertIn("Do not infer that a miracle occurred", joined)
        self.assertIn("Do not treat political dignity", joined)
        self.assertIn("Do not treat a platform object identifier as a digest", joined)
        self.assertIn("Do not identify the 1997 editorial composite", joined)
        self.assertIn("mechanical reversal or unrestricted deception", joined)
        self.assertIn("Do not certify doctrine", joined)


if __name__ == "__main__":
    unittest.main()
