from __future__ import annotations

import unittest

import problem_bundles


class ProblemBundleTests(unittest.TestCase):
    def test_manifest_declares_all_seven_complete_bundle_paths(self) -> None:
        manifest = problem_bundles.load_manifest()
        self.assertEqual(problem_bundles.validate_manifest_problem_bundles(manifest), [])
        self.assertEqual(
            [item["canonical_key"] for item in manifest["problems"]],
            problem_bundles.CANONICAL_KEYS,
        )
        for declaration in manifest["problems"]:
            with self.subTest(problem=declaration["canonical_key"]):
                self.assertTrue(
                    problem_bundles.REQUIRED_BUNDLE_PATH_FIELDS.issubset(declaration)
                )

    def test_all_problem_bundles_load_read_only_and_noncertifying(self) -> None:
        context = problem_bundles.build_problem_bundle_context()
        self.assertEqual(len(context["problems"]), 7)
        self.assertEqual(context["authority"], "CANDIDATE_RUNTIME_CONTEXT_ONLY")
        self.assertIn("no doctrinal certification", context["non_effects"])
        self.assertIn("no predecessor displacement", context["non_effects"])

        for bundle in context["problems"]:
            key = bundle["declaration"]["canonical_key"]
            with self.subTest(problem=key):
                self.assertEqual(
                    bundle["authority"],
                    "READ_ONLY_NONCERTIFYING_OPERATIONAL_CONTEXT",
                )
                self.assertEqual(bundle["constitution"]["identity"]["canonical_key"], key)
                self.assertEqual(bundle["inquiry_profile"]["identity"]["problem"], key)
                self.assertEqual(bundle["witnesses"]["identity"]["problem"], key)
                self.assertEqual(bundle["relations"]["identity"]["problem"], key)
                self.assertTrue(bundle["syntheses"])
                self.assertEqual(problem_bundles.validate_problem_bundle(bundle), [])

    def test_relation_coverage_is_complete_and_controlled(self) -> None:
        context = problem_bundles.build_problem_bundle_context()
        for bundle in context["problems"]:
            key = bundle["declaration"]["canonical_key"]
            relations = bundle["relations"]["relations"]
            with self.subTest(problem=key):
                self.assertEqual(len(relations), 6)
                self.assertEqual(
                    {item["related_problem"] for item in relations},
                    set(problem_bundles.CANONICAL_KEYS) - {key},
                )
                self.assertTrue(
                    all(
                        item["relation_type"]
                        in problem_bundles.CONTROLLED_RELATION_TYPES
                        for item in relations
                    )
                )

    def test_brother_problem_designation_is_reciprocal_and_bounded(self) -> None:
        context = problem_bundles.build_problem_bundle_context(
            ["philosophy-vs-poetry", "theologico-political"]
        )
        by_key = {
            item["declaration"]["canonical_key"]: item for item in context["problems"]
        }
        for key, other in (
            ("philosophy-vs-poetry", "theologico-political"),
            ("theologico-political", "philosophy-vs-poetry"),
        ):
            relation = next(
                item
                for item in by_key[key]["relations"]["relations"]
                if item["related_problem"] == other
            )
            self.assertEqual(relation["relation_type"], "INTERSECTS")
            self.assertEqual(relation["constitutional_designation"], "BROTHER_PROBLEM")
            self.assertEqual(relation["relation_strength"], "CO_FOUNDATIONAL")
            self.assertIn("non_absorption_rule", relation)

    def test_theologico_political_predecessor_is_preserved_in_declaration(self) -> None:
        bundle = problem_bundles.build_problem_bundle("theologico-political")
        declaration = bundle["declaration"]
        self.assertEqual(declaration["active_predecessor"], "problems/theologico-political.yaml")
        self.assertEqual(
            declaration["historical_copy"],
            "history/foundational-problems/theologico-political/"
            "STR-PROBLEM-002-v1.1-active-predecessor.yaml",
        )

    def test_wise_vulgar_accepted_migration_source_is_preserved(self) -> None:
        bundle = problem_bundles.build_problem_bundle("wise-vs-vulgar")
        self.assertEqual(
            bundle["declaration"]["accepted_migration_source"],
            "history/foundational-problems/wise-vs-vulgar/"
            "WVG-v0.2-reconstruction-accepted.yaml",
        )

    def test_single_problem_context_does_not_load_unselected_bundles(self) -> None:
        context = problem_bundles.build_problem_bundle_context(["philosophy-vs-poetry"])
        self.assertEqual(len(context["problems"]), 1)
        self.assertEqual(
            context["problems"][0]["declaration"]["canonical_key"],
            "philosophy-vs-poetry",
        )

    def test_unknown_problem_fails(self) -> None:
        with self.assertRaises(problem_bundles.ProblemBundleError):
            problem_bundles.build_problem_bundle("not-a-problem")


if __name__ == "__main__":
    unittest.main()
