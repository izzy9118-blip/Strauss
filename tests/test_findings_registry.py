from __future__ import annotations

import unittest

import findings_registry


class FindingsRegistryTests(unittest.TestCase):
    def test_registry_validates_for_current_findings_state(self) -> None:
        registry = findings_registry.load_registry()
        self.assertEqual(findings_registry.validate_registry(registry), [])
        self.assertEqual(registry["identity"]["version"], "1.10.0")
        self.assertEqual(
            registry["status"]["registry_scope"],
            "EXHAUSTIVE_FOR_CURRENT_COMMITTED_FINDINGS_RECORD_STATE",
        )
        self.assertEqual(
            registry["status"]["findings_completion"],
            "INCOMPLETE_OPEN_FINDINGS_STORE",
        )
        self.assertEqual(registry["status"]["certification"], "NOT_CERTIFIED")

    def test_finding_and_gap_identifiers_are_unique(self) -> None:
        registry = findings_registry.load_registry()
        finding_ids = [item["finding_set_id"] for item in registry["finding_sets"]]
        gap_ids = [item["gap_id"] for item in registry["findings_gaps"]]
        self.assertEqual(len(finding_ids), 57)
        self.assertEqual(len(finding_ids), len(set(finding_ids)))
        self.assertEqual(len(gap_ids), 6)
        self.assertEqual(len(gap_ids), len(set(gap_ids)))

    def test_problem_synthesis_tree_is_exhaustively_registered(self) -> None:
        registry = findings_registry.load_registry()
        registered = {
            item["path"]
            for item in registry["finding_sets"]
            if item["record_class"] == "PROBLEM_LOCAL_SYNTHESIS"
        }
        self.assertEqual(registered, findings_registry._actual_synthesis_paths())
        self.assertEqual(registered, findings_registry.EXPECTED_SYNTHESIS_PATHS)
        self.assertEqual(len(registered), 35)

    def test_migration_transaction_tree_is_exhaustively_registered(self) -> None:
        registry = findings_registry.load_registry()
        registered = {
            item["path"]
            for item in registry["finding_sets"]
            if item["record_class"] == "MIGRATION_TRANSACTION_LEDGER"
        }
        self.assertEqual(registered, findings_registry._actual_transaction_paths())
        self.assertEqual(registered, findings_registry.EXPECTED_TRANSACTION_PATHS)

    def test_all_corpus_studies_are_registered_as_findings_sets(self) -> None:
        registry = findings_registry.load_registry()
        registered = {
            item["path"]
            for item in registry["finding_sets"]
            if item["record_class"]
            in {"SOURCE_SPECIFIC_STUDY", "INTEGRATION_GOVERNANCE_RECORD"}
        }
        self.assertEqual(registered, findings_registry._corpus_study_paths())
        self.assertEqual(len(registered), 17)

    def _assert_source_derivation(
        self,
        *,
        study_id: str,
        source_id: str,
        local_syntheses: list[tuple[str, str]],
    ) -> dict:
        registry = findings_registry.load_registry()
        by_id = {item["finding_set_id"]: item for item in registry["finding_sets"]}
        study = by_id[study_id]
        self.assertEqual(study["source_bindings"], [source_id])
        self.assertEqual(
            study["derived_local_syntheses"],
            [finding_id for finding_id, _ in local_syntheses],
        )
        self.assertEqual(study["independent_corroboration"], "INCOMPLETE")
        self.assertEqual(study["certification"], "NOT_CERTIFIED")
        for finding_id, expected_problem in local_syntheses:
            synthesis = by_id[finding_id]
            self.assertEqual(synthesis["source_bindings"], [source_id])
            self.assertEqual(synthesis["derived_from"], [study_id])
            self.assertEqual(synthesis["problem_bindings"], [expected_problem])
            self.assertEqual(synthesis["successor_effect"], "NONE")
            self.assertEqual(synthesis["certification"], "NOT_CERTIFIED")
        return study

    def test_jerusalem_and_athens_study_and_local_syntheses_are_explicitly_derived(self) -> None:
        study = self._assert_source_derivation(
            study_id="FINDSET-008",
            source_id="CORPUS-SRC-109",
            local_syntheses=[
                ("FINDSET-111", "theologico-political"),
                ("FINDSET-112", "athens-vs-jerusalem"),
            ],
        )
        self.assertEqual(study["original_edition_comparison"], "PENDING")

    def test_cohen_study_and_three_local_syntheses_are_explicitly_derived(self) -> None:
        study = self._assert_source_derivation(
            study_id="FINDSET-009",
            source_id="CORPUS-SRC-105",
            local_syntheses=[
                ("FINDSET-113", "theologico-political"),
                ("FINDSET-114", "athens-vs-jerusalem"),
                ("FINDSET-115", "ancients-vs-moderns"),
            ],
        )
        self.assertEqual(study["original_edition_comparison"], "PENDING")

    def test_talmon_study_and_three_local_syntheses_are_explicitly_derived(self) -> None:
        study = self._assert_source_derivation(
            study_id="FINDSET-010",
            source_id="CORPUS-SRC-111",
            local_syntheses=[
                ("FINDSET-116", "theologico-political"),
                ("FINDSET-117", "athens-vs-jerusalem"),
                ("FINDSET-118", "ancients-vs-moderns"),
            ],
        )
        self.assertEqual(study["original_edition_comparison"], "PENDING")
        self.assertEqual(study["reviewed_work_reconstruction"], "INCOMPLETE")

    def test_spinoza_preface_study_and_three_local_syntheses_are_explicitly_derived(self) -> None:
        study = self._assert_source_derivation(
            study_id="FINDSET-011",
            source_id="CORPUS-SRC-102",
            local_syntheses=[
                ("FINDSET-119", "theologico-political"),
                ("FINDSET-120", "athens-vs-jerusalem"),
                ("FINDSET-121", "ancients-vs-moderns"),
            ],
        )
        self.assertEqual(study["witness_id"], "CORPUS-WIT-102")
        self.assertEqual(study["original_1965_edition_comparison"], "PENDING")
        self.assertEqual(study["authorial_1968_reprint_comparison"], "PENDING")
        self.assertEqual(study["byte_identity_state"], "UNAVAILABLE_WITH_REASON_PRESERVED")
        self.assertEqual(study["successor_effect"], "NONE")

    def test_spinoza_treatise_study_and_two_local_syntheses_are_explicitly_derived(self) -> None:
        study = self._assert_source_derivation(
            study_id="FINDSET-012",
            source_id="CORPUS-SRC-103",
            local_syntheses=[
                ("FINDSET-122", "theologico-political"),
                ("FINDSET-123", "wise-vs-vulgar"),
            ],
        )
        self.assertEqual(study["witness_id"], "CORPUS-WIT-103")
        self.assertEqual(study["original_1948_journal_comparison"], "PENDING")
        self.assertEqual(study["successor_effect"], "NONE")

    def test_genesis_study_and_three_local_syntheses_are_explicitly_derived(self) -> None:
        study = self._assert_source_derivation(
            study_id="FINDSET-013",
            source_id="CORPUS-SRC-108",
            local_syntheses=[
                ("FINDSET-124", "theologico-political"),
                ("FINDSET-125", "athens-vs-jerusalem"),
                ("FINDSET-126", "nomos-vs-physis"),
            ],
        )
        self.assertEqual(study["witness_id"], "CORPUS-WIT-108")
        self.assertEqual(study["earlier_published_text_comparison"], "PENDING")
        self.assertEqual(study["successor_effect"], "NONE")

    def test_persecution_intro_study_and_two_local_syntheses_are_explicitly_derived(self) -> None:
        study = self._assert_source_derivation(
            study_id="FINDSET-014",
            source_id="CORPUS-SRC-113",
            local_syntheses=[("FINDSET-127", "theologico-political"), ("FINDSET-128", "wise-vs-vulgar")],
        )
        self.assertEqual(study["witness_id"], "CORPUS-WIT-113")
        self.assertEqual(study["original_1952_printing_comparison"], "PENDING")
        self.assertEqual(study["successor_effect"], "NONE")

    def test_hobbes_preface_study_and_two_local_syntheses_preserve_documentary_limit(self) -> None:
        study = self._assert_source_derivation(study_id="FINDSET-015", source_id="CORPUS-SRC-116", local_syntheses=[("FINDSET-129", "theologico-political"), ("FINDSET-130", "ancients-vs-moderns")])
        self.assertEqual(study["witness_id"], "CORPUS-WIT-116")
        self.assertEqual(study["omitted_text_review"], "INCOMPLETE")
        self.assertEqual(study["successor_effect"], "NONE")

    def test_indexes_are_derived_from_finding_set_bindings(self) -> None:
        registry = findings_registry.load_registry()
        finding_sets = registry["finding_sets"]
        self.assertEqual(
            registry["indexes"]["by_problem"],
            findings_registry._derived_problem_index(finding_sets),
        )
        self.assertEqual(
            registry["indexes"]["by_source"],
            findings_registry._derived_source_index(finding_sets),
        )
        self.assertEqual(
            registry["indexes"]["by_record_class"],
            findings_registry._derived_record_class_index(finding_sets),
        )

    def test_theologico_political_predecessor_is_preserved(self) -> None:
        self.assertEqual(
            findings_registry.TP_ACTIVE_PATH.read_bytes(),
            findings_registry.TP_PRESERVED_PATH.read_bytes(),
        )
        registry = findings_registry.load_registry()
        predecessor = next(
            item
            for item in registry["finding_sets"]
            if item["finding_set_id"] == "FINDSET-301"
        )
        self.assertEqual(predecessor["successor_effect"], "NONE")
        self.assertEqual(predecessor["status"], "ACTIVE_PREDECESSOR_UNTOUCHED")

    def test_legacy_predecessor_source_filter_preserves_derivation(self) -> None:
        context = findings_registry.build_registry_context(source="CORPUS-SRC-101-119")
        ids = [item["declaration"]["finding_set_id"] for item in context["finding_sets"]]
        self.assertIn("FINDSET-008", ids)
        self.assertIn("FINDSET-111", ids)
        self.assertIn("FINDSET-112", ids)
        self.assertIn("FINDSET-301", ids)
        self.assertNotIn("FINDSET-009", ids)
        self.assertNotIn("FINDSET-011", ids)
        self.assertIn("no proposition promotion", context["non_effects"])
        self.assertIn("no doctrinal certification", context["non_effects"])

    def test_spinoza_source_filter_preserves_derivation_and_platform_limits(self) -> None:
        context = findings_registry.build_registry_context(source="CORPUS-SRC-102")
        ids = [item["declaration"]["finding_set_id"] for item in context["finding_sets"]]
        self.assertEqual(
            ids,
            [
                "FINDSET-011",
                "FINDSET-105",
                "FINDSET-119",
                "FINDSET-120",
                "FINDSET-121",
                "FINDSET-203",
                "FINDSET-301",
            ],
        )
        study = next(
            item["declaration"]
            for item in context["finding_sets"]
            if item["declaration"]["finding_set_id"] == "FINDSET-011"
        )
        self.assertEqual(study["independent_corroboration"], "INCOMPLETE")
        self.assertEqual(study["byte_identity_state"], "UNAVAILABLE_WITH_REASON_PRESERVED")
        self.assertIn("no doctrinal certification", context["non_effects"])
        self.assertIn("no predecessor displacement", context["non_effects"])

    def test_cohen_source_filter_preserves_derivation_without_corroboration(self) -> None:
        context = findings_registry.build_registry_context(source="CORPUS-SRC-105")
        ids = [item["declaration"]["finding_set_id"] for item in context["finding_sets"]]
        self.assertEqual(
            ids,
            ["FINDSET-009", "FINDSET-105", "FINDSET-113", "FINDSET-114", "FINDSET-115", "FINDSET-203", "FINDSET-301"],
        )
        study = next(
            item["declaration"]
            for item in context["finding_sets"]
            if item["declaration"]["finding_set_id"] == "FINDSET-009"
        )
        self.assertEqual(study["independent_corroboration"], "INCOMPLETE")

    def test_problem_filter_preserves_jurisdictional_separation(self) -> None:
        tp = findings_registry.build_registry_context(problem="theologico-political")
        avj = findings_registry.build_registry_context(problem="athens-vs-jerusalem")
        avm = findings_registry.build_registry_context(problem="ancients-vs-moderns")
        tp_ids = {item["declaration"]["finding_set_id"] for item in tp["finding_sets"]}
        avj_ids = {item["declaration"]["finding_set_id"] for item in avj["finding_sets"]}
        avm_ids = {item["declaration"]["finding_set_id"] for item in avm["finding_sets"]}

        self.assertIn("FINDSET-011", tp_ids & avj_ids & avm_ids)
        self.assertIn("FINDSET-119", tp_ids)
        self.assertNotIn("FINDSET-119", avj_ids | avm_ids)
        self.assertIn("FINDSET-120", avj_ids)
        self.assertNotIn("FINDSET-120", tp_ids | avm_ids)
        self.assertIn("FINDSET-121", avm_ids)
        self.assertNotIn("FINDSET-121", tp_ids | avj_ids)

    def test_unknown_filters_fail(self) -> None:
        with self.assertRaises(findings_registry.FindingsRegistryError):
            findings_registry.build_registry_context(problem="not-a-problem")
        with self.assertRaises(findings_registry.FindingsRegistryError):
            findings_registry.build_registry_context(source="not-a-source")
        with self.assertRaises(findings_registry.FindingsRegistryError):
            findings_registry.build_registry_context(record_class="not-a-class")


if __name__ == "__main__":
    unittest.main()
