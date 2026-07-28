"""Regression coverage for complete 19-of-19 Theologico-Political reviewed-witness registration."""

from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SHA = "43e98521c28a9ef8ede1eb7a6507d8ee78d605d0a531624d5dd20075220bda66"


def load_yaml(path):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


class CompleteTPWitnessCoverageTests(unittest.TestCase):
    def test_all_nineteen_predecessor_sources_have_reviewed_witnesses(self):
        corpus = load_yaml("corpus/index.yaml")
        sources = {x["source_id"]: x for x in corpus["source_entities"]}
        witnesses = {
            x["source_id"]: x
            for x in corpus["reviewed_witnesses"]
            if x["source_id"].startswith("CORPUS-SRC-1")
        }
        expected = {f"CORPUS-SRC-{i:03d}" for i in range(101, 120)}
        self.assertEqual(set(witnesses), expected)
        for sid in expected:
            self.assertEqual(sources[sid]["reviewed_witnesses"], [witnesses[sid]["witness_id"]])
        self.assertEqual(corpus["coverage"]["theologico_political_reviewed_item_witnesses_registered"], 19)
        self.assertEqual(corpus["coverage"]["theologico_political_independent_item_studies_registered"], 10)
        self.assertEqual(corpus["termination"]["theologico_political_reviewed_witness_state"], "COMPLETE_19_OF_19")
        self.assertEqual(corpus["termination"]["theologico_political_independent_study_state"], "INCOMPLETE_10_OF_19")

    def test_nine_witness_only_items_remain_noncertified_and_unstudied(self):
        corpus = load_yaml("corpus/index.yaml")
        complete = {"CORPUS-SRC-102", "CORPUS-SRC-103", "CORPUS-SRC-105", "CORPUS-SRC-108", "CORPUS-SRC-109", "CORPUS-SRC-111", "CORPUS-SRC-113", "CORPUS-SRC-116", "CORPUS-SRC-101", "CORPUS-SRC-104"}
        witness_only = [
            x
            for x in corpus["source_entities"]
            if x["source_id"].startswith("CORPUS-SRC-1") and x["source_id"] not in complete
        ]
        self.assertEqual(len(witness_only), 9)
        for source in witness_only:
            self.assertEqual(
                source["item_level_source_status"],
                "REVIEWED_ITEM_WITNESS_REGISTERED_SEQUENTIAL_RECONSTRUCTION_REQUIRED",
            )
            status_entry = next(
                x for x in corpus["source_status_records"] if x["source_id"] == source["source_id"]
            )
            status = load_yaml(status_entry["path"])
            self.assertEqual(status["termination"]["study_state"], "INCOMPLETE")
            self.assertEqual(status["termination"]["certification"], "NOT_CERTIFIED")
            self.assertEqual(status["termination"]["successor_effect"], "NONE")

    def test_new_fingerprint_batch_uses_one_verified_container_without_collapsing_scopes(self):
        corpus = load_yaml("corpus/index.yaml")
        by_id = {x["witness_id"]: x for x in corpus["reviewed_witnesses"]}
        new_ids = {
            f"CORPUS-WIT-{i:03d}"
            for i in [101, 104, 106, 107, 108, 110, 112, 113, 114, 115, 116, 117, 118, 119]
        }
        for wid in new_ids:
            self.assertEqual(by_id[wid]["container_sha256"], SHA)
            self.assertEqual(by_id[wid]["container_file_size_bytes"], 39287307)
            self.assertEqual(by_id[wid]["container_page_count"], 526)
        self.assertEqual(by_id["CORPUS-WIT-110"]["registered_scope"], "first paragraph")
        self.assertEqual(by_id["CORPUS-WIT-119"]["registered_scope"], "last paragraph")
        self.assertEqual(by_id["CORPUS-WIT-101"]["printed_page_range"], {"start": 87, "end": 136})
        self.assertEqual(by_id["CORPUS-WIT-118"]["pdf_page_range_one_based"], {"start": 486, "end": 489})


if __name__ == "__main__":
    unittest.main()
