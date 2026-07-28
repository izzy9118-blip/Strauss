from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(relative_path: str) -> dict:
    data = yaml.safe_load((ROOT / relative_path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"{relative_path} must contain a YAML mapping")
    return data


class InterfaceConsistencyTests(unittest.TestCase):
    def test_manifest_audit_mapping_process_and_registry_versions_agree(self) -> None:
        manifest = load_yaml("manifest.yaml")
        audit = load_yaml("audits/operational-completeness.yaml")
        mapping = load_yaml("migrations/lean-operational-interface.yaml")
        process = load_yaml("history/production-plans/2026-07-27-ten-step-completion-process.yaml")
        corpus = load_yaml("corpus/index.yaml")
        findings = load_yaml("findings/index.yaml")

        self.assertEqual(manifest["audit"]["version"], audit["identity"]["version"])
        self.assertEqual(mapping["completion_audit"]["version"], audit["identity"]["version"])
        self.assertEqual(manifest["corpus"]["registry_version"], corpus["identity"]["version"])
        self.assertEqual(
            mapping["mappings"]["corpus"]["interface"]["registry_version"],
            corpus["identity"]["version"],
        )
        self.assertEqual(manifest["findings"]["registry_version"], findings["identity"]["version"])
        self.assertEqual(
            mapping["mappings"]["findings"]["interface"]["registry_version"],
            findings["identity"]["version"],
        )
        step_one = next(item for item in process["steps"] if item["sequence"] == 1)
        step_two = next(item for item in process["steps"] if item["sequence"] == 2)
        self.assertEqual(step_one["current_version"], audit["identity"]["version"])
        self.assertEqual(step_two["current_version"], manifest["identity"]["version"])

    def test_nineteen_identity_five_witness_four_study_language_matches(self) -> None:
        manifest = load_yaml("manifest.yaml")
        audit = load_yaml("audits/operational-completeness.yaml")
        mapping = load_yaml("migrations/lean-operational-interface.yaml")
        corpus = load_yaml("corpus/index.yaml")

        item_statuses = [
            item
            for item in corpus["source_status_records"]
            if item["source_id"].startswith("CORPUS-SRC-1")
        ]
        self.assertEqual(len(item_statuses), 19)
        manifest_state = manifest["corpus"]["theologico_political_item_level_statuses"]
        audit_state = audit["summary"]["theologico_political_item_level_status"]
        mapping_state = mapping["mappings"]["corpus"]["theologico_political_item_level_statuses"]

        self.assertEqual(manifest_state["registered_count"], 19)
        self.assertEqual(audit_state["registered_source_identity_count"], 19)
        self.assertEqual(mapping_state["registered_count"], 19)
        self.assertEqual(manifest_state["reviewed_witness_count"], 5)
        self.assertEqual(audit_state["reviewed_item_witness_count"], 5)
        self.assertEqual(mapping_state["reviewed_witness_count"], 5)
        self.assertEqual(manifest_state["independent_sequential_study_count"], 4)
        self.assertEqual(audit_state["independently_reconstructed_count_within_this_sequence"], 4)
        self.assertEqual(mapping_state["independent_sequential_study_count"], 4)
        self.assertEqual(manifest_state["remaining_without_reviewed_item_witness"], 14)
        self.assertEqual(mapping_state["remaining_without_reviewed_witness"], 14)
        self.assertEqual(manifest_state["remaining_without_independent_sequential_study"], 15)
        self.assertEqual(mapping_state["remaining_without_independent_sequential_study"], 15)
        self.assertEqual(
            corpus["termination"]["theologico_political_identity_registration_state"],
            "COMPLETE_19_OF_19",
        )
        self.assertEqual(
            corpus["termination"]["theologico_political_reviewed_witness_state"],
            "INCOMPLETE_5_OF_19",
        )
        self.assertEqual(
            corpus["termination"]["theologico_political_independent_study_state"],
            "INCOMPLETE_4_OF_19",
        )

    def test_priority_schedule_advances_witness_to_genesis_while_spinoza_treatise_study_is_next(self) -> None:
        schedule = load_yaml(
            "history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml"
        )
        self.assertEqual(
            schedule["selection"]["completed_source_ids"],
            ["CORPUS-SRC-109", "CORPUS-SRC-105", "CORPUS-SRC-111", "CORPUS-SRC-102", "CORPUS-SRC-103"],
        )
        self.assertEqual(
            schedule["selection"]["completed_witness_ids"],
            ["CORPUS-WIT-109", "CORPUS-WIT-105", "CORPUS-WIT-111", "CORPUS-WIT-102", "CORPUS-WIT-103"],
        )
        self.assertEqual(
            schedule["selection"]["completed_study_ids"],
            ["JA-STUDY-001", "COHEN-STUDY-001", "TALMON-STUDY-001", "SPINOZA-PREFACE-STUDY-001"],
        )
        self.assertEqual(
            schedule["termination"]["reviewed_item_witness_registration"],
            "COMPLETE_FOR_CORPUS_WIT_102_CORPUS_WIT_103_CORPUS_WIT_105_CORPUS_WIT_109_AND_CORPUS_WIT_111",
        )
        self.assertEqual(
            schedule["termination"]["independent_sequential_reconstruction"],
            "COMPLETE_PROVISIONAL_FOR_COHEN_STUDY_001_JA_STUDY_001_TALMON_STUDY_001_AND_SPINOZA_PREFACE_STUDY_001",
        )
        self.assertEqual(schedule["termination"]["next_item_witness"], "CORPUS-SRC-108")
        self.assertEqual(schedule["termination"]["next_item_study"], "CORPUS-SRC-103")
        self.assertEqual(schedule["status"]["certification"], "NOT_CERTIFIED")

    def test_source_derivations_preserve_problem_jurisdiction(self) -> None:
        findings = load_yaml("findings/index.yaml")
        by_id = {item["finding_set_id"]: item for item in findings["finding_sets"]}

        expected = {
            "FINDSET-008": [("FINDSET-111", "theologico-political"), ("FINDSET-112", "athens-vs-jerusalem")],
            "FINDSET-009": [("FINDSET-113", "theologico-political"), ("FINDSET-114", "athens-vs-jerusalem"), ("FINDSET-115", "ancients-vs-moderns")],
            "FINDSET-010": [("FINDSET-116", "theologico-political"), ("FINDSET-117", "athens-vs-jerusalem"), ("FINDSET-118", "ancients-vs-moderns")],
            "FINDSET-011": [("FINDSET-119", "theologico-political"), ("FINDSET-120", "athens-vs-jerusalem"), ("FINDSET-121", "ancients-vs-moderns")],
        }
        for study_id, syntheses in expected.items():
            self.assertEqual(
                by_id[study_id]["derived_local_syntheses"],
                [finding_id for finding_id, _ in syntheses],
            )
            for finding_id, problem in syntheses:
                self.assertEqual(by_id[finding_id]["problem_bindings"], [problem])
                self.assertEqual(by_id[finding_id]["derived_from"], [study_id])
                self.assertEqual(by_id[finding_id]["successor_effect"], "NONE")

    def test_completion_and_repin_limits_remain_explicit(self) -> None:
        manifest = load_yaml("manifest.yaml")
        audit = load_yaml("audits/operational-completeness.yaml")
        mapping = load_yaml("migrations/lean-operational-interface.yaml")
        process = load_yaml("history/production-plans/2026-07-27-ten-step-completion-process.yaml")

        self.assertEqual(manifest["status"]["semantic_completion"], "INCOMPLETE")
        self.assertEqual(manifest["status"]["doctrinal_certification"], "NOT_CERTIFIED")
        self.assertEqual(audit["status"]["repository_completion"], "INCOMPLETE")
        self.assertEqual(mapping["status"]["semantic_completion"], "INCOMPLETE")
        self.assertEqual(
            manifest["sanctum_contract"]["completed_interface_repin_status"],
            "BLOCKED_WHILE_SEMANTIC_COMPLETION_IS_INCOMPLETE",
        )
        step_ten = next(item for item in process["steps"] if item["sequence"] == 10)
        self.assertEqual(step_ten["state"], "BLOCKED_UNTIL_SUBSTANTIVE_COMPLETION")


if __name__ == "__main__":
    unittest.main()
