from __future__ import annotations

import unittest

import corpus_registry


class CorpusRegistryTests(unittest.TestCase):
    def test_registry_validates_for_current_repository_state(self) -> None:
        registry = corpus_registry.load_registry()
        self.assertEqual(corpus_registry.validate_registry(registry), [])
        self.assertEqual(registry["identity"]["version"], "1.0.0")
        self.assertEqual(
            registry["status"]["registry_scope"],
            "EXHAUSTIVE_FOR_CURRENT_COMMITTED_SOURCE_AND_STUDY_STATE",
        )
        self.assertEqual(
            registry["status"]["corpus_completion"],
            "INCOMPLETE_OPEN_CORPUS",
        )
        self.assertEqual(registry["status"]["certification"], "NOT_CERTIFIED")

    def test_source_witness_study_and_gap_identifiers_are_unique(self) -> None:
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
        self.assertEqual(
            corpus_registry._registered_study_paths(registry),
            corpus_registry._actual_study_tree_paths(),
        )
        self.assertEqual(
            corpus_registry._actual_study_tree_paths(),
            corpus_registry.EXPECTED_STUDY_TREE_PATHS,
        )

    def test_nineteen_theologico_political_sources_are_preserved_verbatim_by_identity(self) -> None:
        registry = corpus_registry.load_registry()
        predecessor = corpus_registry.load_yaml(corpus_registry.TP_PREDECESSOR_PATH)
        original = predecessor["documentary_source_basis"]["sources"]
        registered = [
            item
            for item in registry["source_entities"]
            if item["source_id"].startswith("CORPUS-SRC-1")
            and item["source_id"] not in {
                "CORPUS-SRC-001",
                "CORPUS-SRC-002",
                "CORPUS-SRC-003",
            }
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
