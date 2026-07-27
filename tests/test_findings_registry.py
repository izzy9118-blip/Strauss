from __future__ import annotations

import unittest

import findings_registry


class FindingsRegistryTests(unittest.TestCase):
    def test_registry_validates_for_current_findings_state(self) -> None:
        registry = findings_registry.load_registry()
        self.assertEqual(findings_registry.validate_registry(registry), [])
        self.assertEqual(registry["identity"]["version"], "1.2.0")
        self.assertEqual(
            registry["status"]["registry_scope"],
            "EXHAUSTIVE_FOR_CURRENT_COMMITTED_FINDINGS_RECORD_STATE",
        )
        self.assertEqual(registry["status"]["findings_completion"], "INCOMPLETE_OPEN_FINDINGS_STORE")
        self.assertEqual(registry["status"]["certification"], "NOT_CERTIFIED")

    def test_finding_and_gap_identifiers_are_unique(self) -> None:
        registry = findings_registry.load_registry()
        finding_ids = [item["finding_set_id"] for item in registry["finding_sets"]]
        gap_ids = [item["gap_id"] for item in registry["findings_gaps"]]
        self.assertEqual(len(finding_ids), 28)
        self.assertEqual(len(finding_ids), len(set(finding_ids)))
        self.assertEqual(len(gap_ids), 6)
        self.assertEqual(len(gap_ids), len(set(gap_ids)))

    def test_problem_synthesis_tree_is_exhaustively_registered(self) -> None:
        registry = findings_registry.load_registry()
        registered = {
            item["path"] for item in registry["finding_sets"]
            if item["record_class"] == "PROBLEM_LOCAL_SYNTHESIS"
        }
        self.assertEqual(registered, findings_registry._actual_synthesis_paths())
        self.assertEqual(registered, findings_registry.EXPECTED_SYNTHESIS_PATHS)
        self.assertEqual(len(registered), 14)

    def test_migration_transaction_tree_is_exhaustively_registered(self) -> None:
        registry = findings_registry.load_registry()
        registered = {
            item["path"] for item in registry["finding_sets"]
            if item["record_class"] == "MIGRATION_TRANSACTION_LEDGER"
        }
        self.assertEqual(registered, findings_registry._actual_transaction_paths())
        self.assertEqual(registered, findings_registry.EXPECTED_TRANSACTION_PATHS)

    def test_all_corpus_studies_are_registered_as_findings_sets(self) -> None:
        registry = findings_registry.load_registry()
        registered = {
            item["path"] for item in registry["finding_sets"]
            if item["record_class"] in {"SOURCE_SPECIFIC_STUDY", "INTEGRATION_GOVERNANCE_RECORD"}
        }
        self.assertEqual(registered, findings_registry._corpus_study_paths())
        self.assertEqual(len(registered), 9)

    def _assert_source_derivation(
        self,
        study_id: str,
        source_id: str,
        synthesis_ids: list[str],
        problem_bindings: list[list[str]],
    ) -> None:
        registry = findings_registry.load_registry()
        by_id = {item["finding_set_id"]: item for item in registry["finding_sets"]}
        study = by_id[study_id]
        self.assertEqual(study["source_bindings"], [source_id])
        self.assertEqual(study["derived_local_syntheses"], synthesis_ids)
        self.assertEqual(study["independent_corroboration"], "INCOMPLETE")
        self.assertEqual(study["certification"], "NOT_CERTIFIED")
        for synthesis_id, expected_problems in zip(synthesis_ids, problem_bindings):
            synthesis = by_id[synthesis_id]
            self.assertEqual(synthesis["derived_from"], [study_id])
            self.assertEqual(synthesis["problem_bindings"], expected_problems)
            self.assertEqual(synthesis["successor_effect"], "NONE")
            self.assertEqual(synthesis["certification"], "NOT_CERTIFIED")

    def test_jerusalem_and_athens_derivation_is_explicit(self) -> None:
        self._assert_source_derivation(
            "FINDSET-008",
            "CORPUS-SRC-109",
            ["FINDSET-111", "FINDSET-112"],
            [["theologico-political"], ["athens-vs-jerusalem"]],
        )

    def test_cohen_derivation_is_explicit(self) -> None:
        self._assert_source_derivation(
            "FINDSET-009",
            "CORPUS-SRC-105",
            ["FINDSET-113", "FINDSET-114"],
            [["theologico-political"], ["athens-vs-jerusalem"]],
        )

    def test_indexes_are_derived_from_finding_set_bindings(self) -> None:
        registry = findings_registry.load_registry()
        finding_sets = registry["finding_sets"]
        self.assertEqual(registry["indexes"]["by_problem"], findings_registry._derived_problem_index(finding_sets))
        self.assertEqual(registry["indexes"]["by_source"], findings_registry._derived_source_index(finding_sets))
        self.assertEqual(registry["indexes"]["by_record_class"], findings_registry._derived_record_class_index(finding_sets))

    def test_theologico_political_predecessor_is_preserved(self) -> None:
        self.assertEqual(findings_registry.TP_ACTIVE_PATH.read_bytes(), findings_registry.TP_PRESERVED_PATH.read_bytes())
        registry = findings_registry.load_registry()
        predecessor = next(item for item in registry["finding_sets"] if item["finding_set_id"] == "FINDSET-301")
        self.assertEqual(predecessor["successor_effect"], "NONE")
        self.assertEqual(predecessor["status"], "ACTIVE_PREDECESSOR_UNTOUCHED")

    def test_problem_filter_preserves_jurisdictional_separation(self) -> None:
        tp = findings_registry.build_registry_context(problem="theologico-political")
        avj = findings_registry.build_registry_context(problem="athens-vs-jerusalem")
        avm = findings_registry.build_registry_context(problem="ancients-vs-moderns")
        tp_ids = {item["declaration"]["finding_set_id"] for item in tp["finding_sets"]}
        avj_ids = {item["declaration"]["finding_set_id"] for item in avj["finding_sets"]}
        avm_ids = {item["declaration"]["finding_set_id"] for item in avm["finding_sets"]}
        self.assertIn("FINDSET-009", tp_ids & avj_ids & avm_ids)
        self.assertIn("FINDSET-113", tp_ids)
        self.assertNotIn("FINDSET-113", avj_ids)
        self.assertIn("FINDSET-114", avj_ids)
        self.assertNotIn("FINDSET-114", tp_ids)

    def test_context_is_noncertifying(self) -> None:
        context = findings_registry.build_registry_context(source="CORPUS-SRC-101-119")
        ids = {item["declaration"]["finding_set_id"] for item in context["finding_sets"]}
        self.assertIn("FINDSET-009", ids)
        self.assertIn("FINDSET-113", ids)
        self.assertIn("FINDSET-114", ids)
        self.assertIn("no proposition promotion", context["non_effects"])
        self.assertIn("no doctrinal certification", context["non_effects"])

    def test_unknown_filters_fail(self) -> None:
        with self.assertRaises(findings_registry.FindingsRegistryError):
            findings_registry.build_registry_context(problem="not-a-problem")
        with self.assertRaises(findings_registry.FindingsRegistryError):
            findings_registry.build_registry_context(source="not-a-source")
        with self.assertRaises(findings_registry.FindingsRegistryError):
            findings_registry.build_registry_context(record_class="not-a-class")


if __name__ == "__main__":
    unittest.main()
