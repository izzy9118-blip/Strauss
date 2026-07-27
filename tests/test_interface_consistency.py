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
    def test_manifest_audit_mapping_and_registry_versions_agree(self) -> None:
        manifest = load_yaml("manifest.yaml")
        audit = load_yaml("audits/operational-completeness.yaml")
        mapping = load_yaml("migrations/lean-operational-interface.yaml")
        corpus = load_yaml("corpus/index.yaml")

        self.assertEqual(manifest["audit"]["version"], audit["identity"]["version"])
        self.assertEqual(mapping["completion_audit"]["version"], audit["identity"]["version"])
        self.assertEqual(manifest["corpus"]["registry_version"], corpus["identity"]["version"])
        self.assertEqual(
            mapping["mappings"]["corpus"]["interface"]["registry_version"],
            corpus["identity"]["version"],
        )

    def test_nineteen_of_nineteen_status_language_matches_registry(self) -> None:
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
        self.assertEqual(
            manifest["corpus"]["theologico_political_item_level_statuses"]["registered_count"],
            len(item_statuses),
        )
        self.assertEqual(
            audit["summary"]["theologico_political_item_level_status"]["registered_source_identity_count"],
            len(item_statuses),
        )
        self.assertEqual(
            mapping["mappings"]["corpus"]["theologico_political_item_level_statuses"]["registered_count"],
            len(item_statuses),
        )
        self.assertEqual(
            manifest["corpus"]["theologico_political_item_level_statuses"]["remaining_without_item_level_status"],
            0,
        )
        self.assertEqual(
            corpus["termination"]["theologico_political_identity_registration_state"],
            "COMPLETE_19_OF_19",
        )

    def test_identity_completion_does_not_claim_witness_or_study_completion(self) -> None:
        manifest = load_yaml("manifest.yaml")
        audit = load_yaml("audits/operational-completeness.yaml")
        mapping = load_yaml("migrations/lean-operational-interface.yaml")
        corpus = load_yaml("corpus/index.yaml")

        self.assertEqual(
            corpus["termination"]["theologico_political_reviewed_witness_state"],
            "INCOMPLETE",
        )
        self.assertEqual(
            corpus["termination"]["theologico_political_independent_study_state"],
            "INCOMPLETE",
        )
        self.assertEqual(
            manifest["corpus"]["theologico_political_item_level_statuses"]["reviewed_witness_count"],
            0,
        )
        self.assertEqual(
            audit["summary"]["theologico_political_item_level_status"]["independently_reconstructed_count_within_this_sequence"],
            0,
        )
        self.assertEqual(
            mapping["mappings"]["corpus"]["theologico_political_item_level_statuses"]["independent_sequential_study_count"],
            0,
        )

    def test_completion_and_repin_limits_remain_explicit(self) -> None:
        manifest = load_yaml("manifest.yaml")
        audit = load_yaml("audits/operational-completeness.yaml")
        mapping = load_yaml("migrations/lean-operational-interface.yaml")
        process = load_yaml(
            "history/production-plans/2026-07-27-ten-step-completion-process.yaml"
        )

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
