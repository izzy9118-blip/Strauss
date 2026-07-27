from __future__ import annotations

import unittest

import corpus_registry


class CorpusRegistryTests(unittest.TestCase):
    def test_registry_validates_for_current_repository_state(self) -> None:
        registry = corpus_registry.load_registry()
        self.assertEqual(corpus_registry.validate_registry(registry), [])
        self.assertEqual(registry["identity"]["version"], "1.10.0")
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
        self.assertEqual(
            registry["coverage"]["current_studies_tree_yaml_records_accounted_for"],
            36,
        )
        self.assertEqual(registry["coverage"]["study_records_registered"], 11)
        self.assertEqual(registry["coverage"]["reviewed_witnesses_registered"], 7)

    def test_nineteen_tp_sources_preserve_predecessor_identity(self) -> None:
        registry = corpus_registry.load_registry()
        predecessor = corpus_registry.load_yaml(corpus_registry.TP_PREDECESSOR_PATH)
        original = predecessor["documentary_source_basis"]["sources"]
        registered = [
            item
            for item in registry["source_entities"]
            if corpus_registry._tp_sequence_from_source_id(item["source_id"]) is not None
        ]
        registered.sort(key=lambda item: item["source_id"])
        self.assertEqual(len(registered), 19)
        self.assertEqual(
            [(item["canonical_title"], item["date"]) for item in registered],
            [(item["title"], item["date"]) for item in original],
        )
        self.assertEqual(
            registry["coverage"]["theologico_political_item_level_statuses_registered"],
            19,
        )

    def test_fifteen_tp_sources_remain_without_witness_or_study(self) -> None:
        registry = corpus_registry.load_registry()
        entries = {
            item["source_id"]: item
            for item in registry["source_status_records"]
            if corpus_registry._tp_sequence_from_source_id(item["source_id"]) is not None
        }
        sources = [
            item
            for item in registry["source_entities"]
            if corpus_registry._tp_sequence_from_source_id(item["source_id"]) is not None
            and item["source_id"] not in corpus_registry.COMPLETE_TP_ITEMS
        ]
        self.assertEqual(len(sources), 15)
        for source in sources:
            status = corpus_registry.load_yaml(
                corpus_registry._resolve(entries[source["source_id"]]["path"])
            )
            self.assertEqual(
                source["item_level_source_status"],
                "REGISTERED_SOURCE_IDENTITY_WITHOUT_REVIEWED_WITNESS",
            )
            self.assertEqual(status["status"]["reviewed_witness"], "NOT_YET_REGISTERED")
            self.assertEqual(
                status["status"]["independent_sequential_study"],
                "NOT_YET_COMPLETED",
            )
            self.assertEqual(status["termination"]["study_state"], "INCOMPLETE")
            self.assertEqual(status["termination"]["certification"], "NOT_CERTIFIED")
            self.assertEqual(status["termination"]["successor_effect"], "NONE")

    def test_spinoza_preface_platform_witness_and_study_are_registered(self) -> None:
        registry = corpus_registry.load_registry()
        source = next(item for item in registry["source_entities"] if item["source_id"] == "CORPUS-SRC-102")
        entry = next(item for item in registry["source_status_records"] if item["source_id"] == "CORPUS-SRC-102")
        witness = next(item for item in registry["reviewed_witnesses"] if item["witness_id"] == "CORPUS-WIT-102")
        study = next(item for item in registry["study_records"] if item["study_id"] == "CORPUS-STUDY-011")
        status = corpus_registry.load_yaml(corpus_registry._resolve(entry["path"]))
        witness_record = corpus_registry.load_yaml(corpus_registry._resolve(witness["witness_record_path"]))
        study_record = corpus_registry.load_yaml(corpus_registry._resolve(study["path"]))

        self.assertEqual(source["reviewed_witnesses"], ["CORPUS-WIT-102"])
        self.assertEqual(source["study_records"], ["CORPUS-STUDY-011"])
        self.assertEqual(
            source["item_level_source_status"],
            "REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION",
        )
        self.assertEqual(witness["witness_class"], "PLATFORM_REFERENCE_WITNESS")
        self.assertEqual(witness["printed_page_range"], {"start": 137, "end": 180})
        self.assertEqual(witness["pdf_page_range_one_based"], "PENDING_DIRECT_OFFSET_VERIFICATION")
        self.assertEqual(witness["platform_object_identifier"], "file_0000000073c081fd9fb65f9ea7552cde")
        self.assertEqual(witness["sha256_state"], "UNAVAILABLE_WITH_REASON_PRESERVED")
        self.assertEqual(status["status"]["reviewed_witness"], "CORPUS-WIT-102")
        self.assertEqual(
            status["status"]["independent_sequential_study"],
            "SPINOZA-PREFACE-STUDY-001",
        )
        self.assertEqual(status["termination"]["study_state"], "COMPLETE_PROVISIONAL")
        self.assertEqual(status["termination"]["successor_effect"], "NONE")
        self.assertEqual(study_record["identity"]["id"], "SPINOZA-PREFACE-STUDY-001")
        self.assertEqual(
            study_record["termination"]["reading_state"],
            "COMPLETE_FOR_QUALIFIED_1997_PLATFORM_REFERENCE_WITNESS",
        )
        self.assertEqual(study_record["termination"]["successor_effect"], "NONE")
        self.assertEqual(witness_record["status"]["witness_class"], "PLATFORM_REFERENCE_WITNESS")
        self.assertEqual(witness_record["byte_identity"]["sha256_state"], "UNAVAILABLE_WITH_REASON_PRESERVED")
        self.assertEqual(
            witness_record["termination"]["study_state"],
            "INCOMPLETE",
            "witness registration record must not be silently rewritten as the later study record",
        )

    def _assert_complete_container_item(
        self,
        *,
        source_id: str,
        witness_id: str,
        corpus_study_id: str,
        internal_study_id: str,
        printed_range: dict[str, int],
        pdf_range: dict[str, int],
    ) -> None:
        registry = corpus_registry.load_registry()
        source = next(item for item in registry["source_entities"] if item["source_id"] == source_id)
        entry = next(
            item for item in registry["source_status_records"] if item["source_id"] == source_id
        )
        witness = next(
            item for item in registry["reviewed_witnesses"] if item["witness_id"] == witness_id
        )
        study = next(
            item for item in registry["study_records"] if item["study_id"] == corpus_study_id
        )
        status = corpus_registry.load_yaml(corpus_registry._resolve(entry["path"]))
        study_record = corpus_registry.load_yaml(corpus_registry._resolve(study["path"]))

        self.assertEqual(source["reviewed_witnesses"], [witness_id])
        self.assertEqual(source["study_records"], [corpus_study_id])
        self.assertEqual(witness["printed_page_range"], printed_range)
        self.assertEqual(witness["pdf_page_range_one_based"], pdf_range)
        self.assertEqual(
            witness["container_sha256"],
            "8479ed41fe951b8ebc5a2a5b6557a482a60de0d13032785a68f11d51ea8b4fb6",
        )
        self.assertEqual(status["status"]["reviewed_witness"], witness_id)
        self.assertEqual(status["status"]["independent_sequential_study"], internal_study_id)
        self.assertEqual(status["termination"]["study_state"], "COMPLETE_PROVISIONAL")
        self.assertEqual(status["termination"]["study_id"], internal_study_id)
        self.assertEqual(status["termination"]["independent_corroboration"], "INCOMPLETE")
        self.assertEqual(status["termination"]["certification"], "NOT_CERTIFIED")
        self.assertEqual(status["termination"]["successor_effect"], "NONE")
        self.assertEqual(study_record["identity"]["id"], internal_study_id)
        self.assertEqual(
            study_record["termination"]["reading_state"],
            "COMPLETE_FOR_REVIEWED_1983_COLLECTED_WITNESS",
        )
        self.assertEqual(study_record["status"]["certification"], "NOT_CERTIFIED")

    def test_jerusalem_and_athens_witness_and_study_are_registered(self) -> None:
        self._assert_complete_container_item(
            source_id="CORPUS-SRC-109",
            witness_id="CORPUS-WIT-109",
            corpus_study_id="CORPUS-STUDY-008",
            internal_study_id="JA-STUDY-001",
            printed_range={"start": 147, "end": 173},
            pdf_range={"start": 151, "end": 177},
        )

    def test_cohen_witness_and_study_are_registered(self) -> None:
        self._assert_complete_container_item(
            source_id="CORPUS-SRC-105",
            witness_id="CORPUS-WIT-105",
            corpus_study_id="CORPUS-STUDY-009",
            internal_study_id="COHEN-STUDY-001",
            printed_range={"start": 233, "end": 247},
            pdf_range={"start": 237, "end": 251},
        )

    def test_talmon_witness_and_study_are_registered(self) -> None:
        self._assert_complete_container_item(
            source_id="CORPUS-SRC-111",
            witness_id="CORPUS-WIT-111",
            corpus_study_id="CORPUS-STUDY-010",
            internal_study_id="TALMON-STUDY-001",
            printed_range={"start": 232, "end": 232},
            pdf_range={"start": 236, "end": 236},
        )
        registry = corpus_registry.load_registry()
        source = next(
            item for item in registry["source_entities"] if item["source_id"] == "CORPUS-SRC-111"
        )
        witness = next(
            item
            for item in registry["reviewed_witnesses"]
            if item["witness_id"] == "CORPUS-WIT-111"
        )
        witness_record = corpus_registry.load_yaml(
            corpus_registry._resolve(witness["witness_record_path"])
        )
        self.assertEqual(
            source["problem_bindings"],
            ["theologico-political", "athens-vs-jerusalem", "ancients-vs-moderns"],
        )
        self.assertEqual(witness_record["identity"]["witness_id"], "CORPUS-WIT-111")
        self.assertEqual(witness_record["status"]["certification"], "NOT_CERTIFIED")
        self.assertEqual(witness_record["status"]["successor_effect"], "NONE")
        self.assertEqual(witness_record["reviewed_work_identity"]["reviewed_work_witness_state"], "NOT_REGISTERED")

    def test_tp_aliases_and_registered_scopes_remain_attached(self) -> None:
        registry = corpus_registry.load_registry()
        predecessor = corpus_registry.load_yaml(corpus_registry.TP_PREDECESSOR_PATH)
        entries = {
            item["source_id"]: item
            for item in registry["source_status_records"]
            if corpus_registry._tp_sequence_from_source_id(item["source_id"]) is not None
        }
        for sequence, original in enumerate(predecessor["documentary_source_basis"]["sources"], start=1):
            source_id = f"CORPUS-SRC-{100 + sequence:03d}"
            source = next(item for item in registry["source_entities"] if item["source_id"] == source_id)
            status = corpus_registry.load_yaml(corpus_registry._resolve(entries[source_id]["path"]))
            if original.get("canonical_alias"):
                self.assertIn(original["canonical_alias"], source["canonical_aliases"])
                self.assertIn(original["canonical_alias"], status["identity"]["canonical_aliases"])
            if original.get("scope"):
                self.assertEqual(source["registered_scope"], original["scope"])
                self.assertEqual(status["identity"]["registered_scope"], original["scope"])

    def test_context_is_read_only_and_noncertifying(self) -> None:
        context = corpus_registry.build_registry_context()
        self.assertEqual(context["authority"], "READ_ONLY_DISCOVERY_AND_PROVENANCE_CONTEXT")
        self.assertIn("no source-text admission", context["non_effects"])
        self.assertIn("no doctrinal certification", context["non_effects"])
        self.assertIn("no successor activation", context["non_effects"])
        self.assertIn("no Assembly authority", context["non_effects"])


if __name__ == "__main__":
    unittest.main()
