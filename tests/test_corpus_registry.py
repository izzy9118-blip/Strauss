from __future__ import annotations

import unittest

import corpus_registry


class CorpusRegistryTests(unittest.TestCase):
    def test_registry_validates_for_current_repository_state(self) -> None:
        registry = corpus_registry.load_registry()
        self.assertEqual(corpus_registry.validate_registry(registry), [])
        self.assertEqual(registry["identity"]["version"], "1.3.0")
        self.assertEqual(
            registry["status"]["registry_scope"],
            "EXHAUSTIVE_FOR_CURRENT_COMMITTED_SOURCE_AND_STUDY_STATE",
        )
        self.assertEqual(
            registry["status"]["corpus_completion"],
            "INCOMPLETE_OPEN_CORPUS",
        )
        self.assertEqual(registry["status"]["certification"], "NOT_CERTIFIED")

    def test_source_witness_study_status_and_gap_identifiers_are_unique(self) -> None:
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
            12,
        )

    def test_nineteen_theologico_political_sources_are_preserved_verbatim_by_identity(self) -> None:
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

    def test_posthumous_collection_editorial_limits_are_preserved(self) -> None:
        registry = corpus_registry.load_registry()
        sppp = next(
            item
            for item in registry["source_entities"]
            if item["source_id"] == "CORPUS-SRC-002"
        )
        limits = "\n".join(sppp["limits"])
        self.assertIn("intended introduction", limits)
        self.assertIn("projected essay on Plato's Gorgias", limits)
        self.assertIn("Pangle", limits)
        self.assertIn("secondary", limits)

    def test_plato_apology_translation_limit_is_explicit(self) -> None:
        registry = corpus_registry.load_registry()
        apology = next(
            item
            for item in registry["source_entities"]
            if item["source_id"] == "CORPUS-SRC-003"
        )
        witness = next(
            item
            for item in registry["reviewed_witnesses"]
            if item["source_id"] == "CORPUS-SRC-003"
        )
        self.assertEqual(witness["translator"], "Benjamin Jowett")
        self.assertEqual(witness["greek_alignment"], "PENDING")
        self.assertTrue(any("English translation" in item for item in apology["limits"]))

    def test_socrates_and_aristophanes_witness_is_registered_without_filename_date_drift(self) -> None:
        registry = corpus_registry.load_registry()
        source = next(
            item
            for item in registry["source_entities"]
            if item["source_id"] == "CORPUS-SRC-001"
        )
        witness = next(
            item
            for item in registry["reviewed_witnesses"]
            if item["witness_id"] == "CORPUS-WIT-003"
        )
        self.assertEqual(source["date"], 1966)
        self.assertEqual(
            witness["reviewed_edition"],
            "University of Chicago Press paperback edition 1980",
        )
        self.assertIn("NONAUTHORITATIVE", witness["filename_year_status"])

    def _assert_unreviewed_tp_status(
        self,
        *,
        source_id: str,
        status_id: str,
        sequence: int,
        title: str,
        alias: str | None = None,
    ) -> None:
        registry = corpus_registry.load_registry()
        source = next(
            item
            for item in registry["source_entities"]
            if item["source_id"] == source_id
        )
        entry = next(
            item
            for item in registry["source_status_records"]
            if item["status_id"] == status_id
        )
        status = corpus_registry.load_yaml(corpus_registry._resolve(entry["path"]))

        self.assertEqual(source["source_status_record"], status_id)
        self.assertEqual(
            source["item_level_source_status"],
            "REGISTERED_SOURCE_IDENTITY_WITHOUT_REVIEWED_WITNESS",
        )
        self.assertEqual(entry["source_id"], source_id)
        self.assertEqual(entry["certification"], "NOT_CERTIFIED")
        self.assertEqual(status["identity"]["canonical_title"], title)
        self.assertEqual(
            status["registration_basis"]["active_predecessor_source_sequence"],
            sequence,
        )
        self.assertEqual(status["status"]["reviewed_witness"], "NOT_YET_REGISTERED")
        self.assertEqual(
            status["status"]["independent_sequential_study"],
            "NOT_YET_COMPLETED",
        )
        self.assertEqual(
            status["publication_and_witness_condition"]["fingerprint"],
            "NOT_AVAILABLE",
        )
        self.assertEqual(status["termination"]["successor_effect"], "NONE")
        if alias is not None:
            self.assertIn(alias, status["identity"]["canonical_aliases"])
            self.assertIn(alias, source["canonical_aliases"])

    def test_progress_or_return_has_identity_status_but_no_reviewed_witness(self) -> None:
        self._assert_unreviewed_tp_status(
            source_id="CORPUS-SRC-101",
            status_id="CORPUS-STATUS-101",
            sequence=1,
            title="Progress or Return?",
        )

    def test_spinoza_preface_has_identity_and_alias_but_no_reviewed_witness(self) -> None:
        self._assert_unreviewed_tp_status(
            source_id="CORPUS-SRC-102",
            status_id="CORPUS-STATUS-102",
            sequence=2,
            title="Preface to Spinoza's Critique of Religion",
            alias="Autobiographical Preface to Spinoza's Critique of Religion",
        )

    def test_all_seven_problem_witness_registries_are_registered_in_order(self) -> None:
        registry = corpus_registry.load_registry()
        self.assertEqual(
            [item["problem"] for item in registry["problem_witness_registries"]],
            corpus_registry.CANONICAL_PROBLEMS,
        )

    def test_context_is_read_only_and_noncertifying(self) -> None:
        context = corpus_registry.build_registry_context()
        self.assertEqual(
            context["authority"],
            "READ_ONLY_DISCOVERY_AND_PROVENANCE_CONTEXT",
        )
        self.assertIn("no source-text admission", context["non_effects"])
        self.assertIn("no doctrinal certification", context["non_effects"])
        self.assertIn("no successor activation", context["non_effects"])
        self.assertIn("no Assembly authority", context["non_effects"])


if __name__ == "__main__":
    unittest.main()
