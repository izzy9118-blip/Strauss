from __future__ import annotations

import unittest

import corpus_registry


class CorpusRegistryTests(unittest.TestCase):
    def test_registry_validates_for_current_repository_state(self) -> None:
        registry = corpus_registry.load_registry()
        self.assertEqual(corpus_registry.validate_registry(registry), [])
        self.assertEqual(registry["identity"]["version"], "1.7.0")
        self.assertEqual(
            registry["status"]["registry_scope"],
            "EXHAUSTIVE_FOR_CURRENT_COMMITTED_SOURCE_AND_STUDY_STATE",
        )
        self.assertEqual(registry["status"]["corpus_completion"], "INCOMPLETE_OPEN_CORPUS")
        self.assertEqual(registry["status"]["certification"], "NOT_CERTIFIED")

    def test_identifiers_are_unique(self) -> None:
        registry = corpus_registry.load_registry()
        for section, field in (
            ("source_entities", "source_id"),
            ("reviewed_witnesses", "witness_id"),
            ("source_status_records", "status_id"),
            ("study_records", "study_id"),
            ("corpus_gaps", "gap_id"),
        ):
            values = [item[field] for item in registry[section]]
            self.assertEqual(len(values), len(set(values)), section)

    def test_current_studies_tree_is_exhaustively_accounted_for(self) -> None:
        registry = corpus_registry.load_registry()
        actual = corpus_registry._actual_study_tree_paths()
        registered = corpus_registry._registered_study_paths(registry)
        self.assertEqual(registered, actual)
        self.assertTrue(corpus_registry.BASE_REQUIRED_STUDY_PATHS.issubset(actual))
        self.assertEqual(registry["coverage"]["current_studies_tree_yaml_records_accounted_for"], 31)
        self.assertEqual(registry["coverage"]["study_records_registered"], 9)

    def test_nineteen_tp_sources_preserve_predecessor_identity(self) -> None:
        registry = corpus_registry.load_registry()
        predecessor = corpus_registry.load_yaml(corpus_registry.TP_PREDECESSOR_PATH)
        original = predecessor["documentary_source_basis"]["sources"]
        registered = [
            item for item in registry["source_entities"]
            if corpus_registry._tp_sequence_from_source_id(item["source_id"]) is not None
        ]
        registered.sort(key=lambda item: item["source_id"])
        self.assertEqual(len(registered), 19)
        self.assertEqual(
            [(item["canonical_title"], item["date"]) for item in registered],
            [(item["title"], item["date"]) for item in original],
        )

    def test_seventeen_tp_sources_remain_without_witness_or_study(self) -> None:
        registry = corpus_registry.load_registry()
        entries = {item["source_id"]: item for item in registry["source_status_records"]}
        sources = [
            item for item in registry["source_entities"]
            if corpus_registry._tp_sequence_from_source_id(item["source_id"]) is not None
            and item["source_id"] not in corpus_registry.COMPLETED_TP_ITEMS
        ]
        self.assertEqual(len(sources), 17)
        for source in sources:
            status = corpus_registry.load_yaml(corpus_registry._resolve(entries[source["source_id"]]["path"]))
            self.assertEqual(source["item_level_source_status"], "REGISTERED_SOURCE_IDENTITY_WITHOUT_REVIEWED_WITNESS")
            self.assertEqual(status["status"]["reviewed_witness"], "NOT_YET_REGISTERED")
            self.assertEqual(status["status"]["independent_sequential_study"], "NOT_YET_COMPLETED")
            self.assertEqual(status["termination"]["study_state"], "INCOMPLETE")
            self.assertEqual(status["termination"]["certification"], "NOT_CERTIFIED")
            self.assertEqual(status["termination"]["successor_effect"], "NONE")

    def _assert_completed_item(self, source_id: str) -> None:
        registry = corpus_registry.load_registry()
        expected = corpus_registry.COMPLETED_TP_ITEMS[source_id]
        source = next(item for item in registry["source_entities"] if item["source_id"] == source_id)
        entry = next(item for item in registry["source_status_records"] if item["status_id"] == expected["status_id"])
        witness = next(item for item in registry["reviewed_witnesses"] if item["witness_id"] == expected["witness_id"])
        study = next(item for item in registry["study_records"] if item["study_id"] == expected["corpus_study_id"])
        status = corpus_registry.load_yaml(corpus_registry._resolve(entry["path"]))
        study_record = corpus_registry.load_yaml(corpus_registry._resolve(study["path"]))

        self.assertEqual(source["reviewed_witnesses"], [expected["witness_id"]])
        self.assertEqual(source["study_records"], [expected["corpus_study_id"]])
        self.assertEqual(witness["printed_page_range"], expected["printed_page_range"])
        self.assertEqual(witness["pdf_page_range_one_based"], expected["pdf_page_range_one_based"])
        self.assertEqual(witness["container_sha256"], corpus_registry.CONTAINER_SHA256)
        self.assertEqual(status["status"]["reviewed_witness"], expected["witness_id"])
        self.assertEqual(status["status"]["independent_sequential_study"], expected["study_id"])
        self.assertEqual(status["termination"]["study_state"], "COMPLETE_PROVISIONAL")
        self.assertEqual(status["termination"]["study_id"], expected["study_id"])
        self.assertEqual(status["termination"]["independent_corroboration"], "INCOMPLETE")
        self.assertEqual(status["termination"]["certification"], "NOT_CERTIFIED")
        self.assertEqual(status["termination"]["successor_effect"], "NONE")
        self.assertEqual(study_record["identity"]["id"], expected["study_id"])
        self.assertEqual(study_record["termination"]["reading_state"], "COMPLETE_FOR_REVIEWED_1983_COLLECTED_WITNESS")
        self.assertEqual(study_record["termination"]["independent_corroboration"], "INCOMPLETE")
        self.assertTrue(study_record["termination"]["original_edition_comparison_required"])

    def test_jerusalem_and_athens_completed_provisional_state(self) -> None:
        self._assert_completed_item("CORPUS-SRC-109")

    def test_cohen_essay_completed_provisional_state(self) -> None:
        self._assert_completed_item("CORPUS-SRC-105")

    def test_context_is_read_only_and_noncertifying(self) -> None:
        context = corpus_registry.build_registry_context()
        self.assertEqual(context["authority"], "READ_ONLY_DISCOVERY_AND_PROVENANCE_CONTEXT")
        self.assertIn("no source-text admission", context["non_effects"])
        self.assertIn("no doctrinal certification", context["non_effects"])
        self.assertIn("no successor activation", context["non_effects"])
        self.assertIn("no Assembly authority", context["non_effects"])


if __name__ == "__main__":
    unittest.main()
