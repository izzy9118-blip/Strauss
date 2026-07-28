from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(relative_path: str) -> dict:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


class TalmonIntegrationCompletionTests(unittest.TestCase):
    def test_operational_records_are_synchronized(self) -> None:
        manifest = load_yaml("manifest.yaml")
        audit = load_yaml("audits/operational-completeness.yaml")
        mapping = load_yaml("migrations/lean-operational-interface.yaml")
        process = load_yaml(
            "history/production-plans/2026-07-27-ten-step-completion-process.yaml"
        )
        schedule = load_yaml(
            "history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml"
        )
        corpus = load_yaml("corpus/index.yaml")
        findings = load_yaml("findings/index.yaml")

        self.assertEqual(manifest["identity"]["version"], "1.17.0")
        self.assertEqual(audit["identity"]["version"], "3.5.0")
        self.assertEqual(mapping["identity"]["version"], "1.17.0")
        self.assertEqual(process["identity"]["version"], "1.19.0")
        self.assertEqual(schedule["identity"]["version"], "1.17.0")
        self.assertEqual(corpus["identity"]["version"], "1.21.0")
        self.assertEqual(findings["identity"]["version"], "1.13.0")

        state = manifest["corpus"]["theologico_political_item_level_statuses"]
        self.assertEqual(state["registered_count"], 19)
        self.assertEqual(state["reviewed_witness_count"], 19)
        self.assertEqual(state["independent_sequential_study_count"], 13)
        self.assertEqual(state["remaining_without_reviewed_item_witness"], 0)
        self.assertEqual(state["remaining_without_independent_sequential_study"], 6)
        self.assertEqual(
            state["completed_study_ids"],
            ["COHEN-STUDY-001", "JA-STUDY-001", "TALMON-STUDY-001", "SPINOZA-PREFACE-STUDY-001", "SPINOZA-TREATISE-STUDY-001", "GENESIS-STUDY-001", "PERSECUTION-INTRO-STUDY-001", "HOBBES-PREFACE-STUDY-001", "PROGRESS-RETURN-STUDY-001", "HUSIK-PREFACE-STUDY-001", "FREUD-MOSES-STUDY-001", "WHY-REMAIN-JEWS-STUDY-001", "STATE-ISRAEL-LETTER-STUDY-001"],
        )
        self.assertEqual(schedule["termination"]["next_item_witness"], "NONE")
        self.assertEqual(schedule["termination"]["next_item_study"], "CORPUS-SRC-110")

    def test_talmon_records_remain_provisional_and_nonactivating(self) -> None:
        witness = load_yaml(
            "studies/theologico-political/review-talmon-nature-of-jewish-history/reviewed-witness.yaml"
        )
        study = load_yaml(
            "studies/theologico-political/review-talmon-nature-of-jewish-history/sequential-reconstruction.yaml"
        )
        source_status = load_yaml(
            "studies/theologico-political/review-talmon-nature-of-jewish-history/source-status.yaml"
        )

        self.assertEqual(witness["identity"]["witness_id"], "CORPUS-WIT-111")
        self.assertEqual(study["identity"]["id"], "TALMON-STUDY-001")
        self.assertEqual(study["status"]["certification"], "NOT_CERTIFIED")
        self.assertEqual(source_status["termination"]["certification"], "NOT_CERTIFIED")
        self.assertEqual(source_status["termination"]["successor_effect"], "NONE")
        self.assertEqual(source_status["termination"]["original_edition_comparison"], "PENDING")
        self.assertEqual(source_status["termination"]["reviewed_work_reconstruction"], "INCOMPLETE")

    def test_generated_python_cache_artifacts_are_excluded(self) -> None:
        exclusions = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertIn("__pycache__/", exclusions)
        self.assertIn("*.py[cod]", exclusions)


if __name__ == "__main__":
    unittest.main()
