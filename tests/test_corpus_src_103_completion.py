from __future__ import annotations

from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]

class CorpusSrc103CompletionTests(unittest.TestCase):
    def load(self, path: str) -> dict:
        return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))

    def test_witness_and_study_are_complete_but_not_certified(self) -> None:
        status = self.load("studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/source-status.yaml")
        study = self.load("studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/sequential-reconstruction.yaml")
        self.assertEqual(status["status"]["reviewed_witness"], "CORPUS-WIT-103")
        self.assertEqual(status["status"]["independent_sequential_study"], "SPINOZA-TREATISE-STUDY-001")
        self.assertEqual(len(study["sequential_reading"]), 10)
        self.assertEqual(len(study["permanent_source_level_findings"]), 12)
        self.assertEqual(study["status"]["certification"], "NOT_CERTIFIED")
        self.assertEqual(study["status"]["original_1948_journal_comparison"], "PENDING")

    def test_exact_reviewed_witness_identity_is_preserved(self) -> None:
        witness = self.load("studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/reviewed-witness.yaml")
        self.assertEqual(witness["byte_identity"]["sha256"], "43e98521c28a9ef8ede1eb7a6507d8ee78d605d0a531624d5dd20075220bda66")
        self.assertEqual(witness["item_identity_and_locators"]["printed_page_range"], {"start": 181, "end": 233})
        self.assertEqual(witness["item_identity_and_locators"]["pdf_page_range_one_based"], {"start": 200, "end": 252})

    def test_findings_and_problem_syntheses_are_registered(self) -> None:
        findings = self.load("findings/index.yaml")
        ids = {x["finding_set_id"] for x in findings["finding_sets"]}
        self.assertTrue({"FINDSET-012", "FINDSET-122", "FINDSET-123", "FINDSET-124"}.issubset(ids))

if __name__ == "__main__":
    unittest.main()
