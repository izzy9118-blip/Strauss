import unittest

import corpus_registry


class VerifyMergedTP19State(unittest.TestCase):
    def test_merged_registry_validates_with_complete_witness_coverage(self):
        registry = corpus_registry.load_registry()
        self.assertEqual(corpus_registry.validate_registry(registry), [])
        self.assertEqual(
            registry["termination"]["theologico_political_reviewed_witness_state"],
            "COMPLETE_19_OF_19",
        )
        self.assertEqual(
            registry["termination"]["theologico_political_independent_study_state"],
            "INCOMPLETE_4_OF_19",
        )


if __name__ == "__main__":
    unittest.main()
