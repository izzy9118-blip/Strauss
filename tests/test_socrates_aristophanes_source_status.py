from __future__ import annotations

import unittest

import corpus_registry


class SocratesAndAristophanesSourceStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.path = (
            corpus_registry.ROOT
            / "studies"
            / "socrates-and-aristophanes"
            / "source-status.yaml"
        )
        self.record = corpus_registry.load_yaml(self.path)

    def test_bibliographic_layers_remain_distinct(self) -> None:
        identity = self.record["identity"]
        condition = self.record["publication_condition"]
        self.assertEqual(identity["original_publication_year"], 1966)
        self.assertEqual(identity["reviewed_edition_year"], 1980)
        self.assertIn("1970", condition["filename_caution"])
        self.assertIn("may not govern", condition["filename_caution"])
        self.assertEqual(
            condition["class"],
            "AUTHOR_PUBLISHED_PRIMARY_STRAUSS_BOOK_REVIEWED_IN_LATER_PAPERBACK_EDITION",
        )

    def test_reviewed_file_identity_is_reproducible(self) -> None:
        witness = self.record["reviewed_witness"]
        self.assertEqual(witness["page_count"], 321)
        self.assertEqual(witness["file_size_bytes"], 25818895)
        self.assertEqual(
            witness["sha256"],
            "1b74826f62bbc70d887e0f224b553c3bb521c55688ae9ba28c455ee080df9fa6",
        )
        self.assertFalse(witness["encrypted"])
        self.assertEqual(
            witness["source_condition"],
            "SEARCHABLE_OCR_WITH_AUTHORITATIVE_PAGE_IMAGES",
        )

    def test_ocr_is_not_authoritative_over_page_images(self) -> None:
        text_condition = self.record["reviewed_witness"]["text_condition"]
        self.assertIn("OCR errors", text_condition)
        self.assertIn("Page images", text_condition)
        self.assertIn("govern", text_condition)

    def test_source_does_not_absorb_independent_witnesses(self) -> None:
        rule = self.record["independent_witness_rule"]
        self.assertIn("does not replace", rule)
        self.assertIn("Aristophanes", rule)
        self.assertIn("Plato", rule)
        self.assertIn("Xenophon", rule)
        prohibited = "\n".join(
            self.record["source_classes"]["strauss_argument"]["prohibited_use"]
        )
        self.assertIn("historical evidence about Socrates", prohibited)

    def test_registration_remains_noncertifying(self) -> None:
        self.assertEqual(self.record["status"]["certification"], "NOT_CERTIFIED")
        self.assertEqual(self.record["termination"]["certification"], "NOT_CERTIFIED")
        requirements = "\n".join(self.record["termination"]["remaining_requirements"])
        self.assertIn("no successor activation", requirements)
        self.assertIn("doctrinal certification", requirements)


if __name__ == "__main__":
    unittest.main()
