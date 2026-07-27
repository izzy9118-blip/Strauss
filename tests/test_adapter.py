from __future__ import annotations

import unittest

import adapter


class StraussAdapterTests(unittest.TestCase):
    def test_manifest_validates(self) -> None:
        manifest = adapter.load_manifest()
        self.assertEqual(adapter.validate_manifest(manifest), [])

    def test_seven_problems_load_in_canonical_order(self) -> None:
        context = adapter.build_context()
        keys = [item["declaration"]["canonical_key"] for item in context["problems"]]
        self.assertEqual(
            keys,
            [
                "nomos-vs-physis",
                "philosophy-vs-poetry",
                "theory-vs-practice",
                "theologico-political",
                "athens-vs-jerusalem",
                "wise-vs-vulgar",
                "ancients-vs-moderns",
            ],
        )

    def test_single_problem_selection(self) -> None:
        context = adapter.build_context(["philosophy-vs-poetry"])
        self.assertEqual(len(context["problems"]), 1)
        self.assertEqual(
            context["problems"][0]["declaration"]["canonical_key"],
            "philosophy-vs-poetry",
        )

    def test_brother_problem_is_preserved(self) -> None:
        context = adapter.build_context(["philosophy-vs-poetry", "theologico-political"])
        records = {item["declaration"]["canonical_key"]: item["record"] for item in context["problems"]}
        pvp = records["philosophy-vs-poetry"]
        tp = records["theologico-political"]
        self.assertIn("brother_problem_designation", pvp)
        self.assertIn("brother_problem_designation", tp)
        self.assertEqual(
            pvp["brother_problem_designation"]["related_problem"],
            "theologico-political",
        )
        self.assertEqual(
            tp["brother_problem_designation"]["related_problem"],
            "philosophy-vs-poetry",
        )

    def test_non_destructive_and_non_certifying_safeguards(self) -> None:
        manifest = adapter.load_manifest()
        self.assertEqual(manifest["migration"]["mode"], "ADDITIVE_NON_DESTRUCTIVE")
        self.assertTrue(manifest["safeguards"]["predecessor_overwrite_prohibited"])
        self.assertTrue(manifest["safeguards"]["repository_self_certification_prohibited"])
        self.assertTrue(
            manifest["safeguards"]["artificial_intelligence_self_certification_prohibited"]
        )

    def test_unknown_problem_fails(self) -> None:
        with self.assertRaises(adapter.StraussAdapterError):
            adapter.build_context(["not-a-problem"])


if __name__ == "__main__":
    unittest.main()
