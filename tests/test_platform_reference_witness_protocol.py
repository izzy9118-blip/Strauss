from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(relative_path: str) -> dict:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


class PlatformReferenceWitnessProtocolTests(unittest.TestCase):
    def test_protocol_is_registered_with_matching_identity(self) -> None:
        registry = load_yaml("protocols/registry.yaml")
        protocol = load_yaml("protocols/platform-reference-witness.yaml")
        entry = next(
            item
            for item in registry["protocols"]
            if item["canonical_key"] == "platform-reference-witness"
        )
        self.assertEqual(entry["path"], "protocols/platform-reference-witness.yaml")
        self.assertEqual(entry["protocol_version"], "1.0.0")
        self.assertEqual(
            protocol["identity"]["canonical_key"],
            "platform-reference-witness",
        )
        self.assertEqual(protocol["identity"]["protocol_version"], "1.0.0")

    def test_platform_identifier_is_not_treated_as_a_digest(self) -> None:
        protocol = load_yaml("protocols/platform-reference-witness.yaml")
        witness_class = protocol["witness_classes"]["PLATFORM_REFERENCE_WITNESS"]
        self.assertEqual(witness_class["byte_custody"], "NOT_EXPOSED_TO_REPOSITORY")
        self.assertEqual(
            witness_class["cryptographic_identity"],
            "UNAVAILABLE_WITH_REASON_PRESERVED",
        )
        self.assertIn(
            "platform object identifier equals SHA256",
            protocol["prohibited_inferences"],
        )
        self.assertIn(
            "reviewable text equals repository custody",
            protocol["prohibited_inferences"],
        )

    def test_registration_remains_qualified_and_nonactivating(self) -> None:
        protocol = load_yaml("protocols/platform-reference-witness.yaml")
        self.assertEqual(protocol["status"]["certification"], "NOT_CERTIFIED")
        self.assertEqual(protocol["status"]["doctrinal_effect"], "NONE")
        self.assertEqual(protocol["status"]["migration_effect"], "NONE")
        self.assertEqual(protocol["status"]["successor_activation_effect"], "NONE")
        self.assertIn(
            "QUALIFIED_PLATFORM_REFERENCE_WITNESS_REGISTERED",
            protocol["controlled_states"],
        )

    def test_materialization_requires_forward_revision(self) -> None:
        protocol = load_yaml("protocols/platform-reference-witness.yaml")
        self.assertIn(
            "forward revision",
            protocol["materialization_rule"],
        )
        self.assertIn(
            "may not be rewritten",
            protocol["materialization_rule"],
        )


if __name__ == "__main__":
    unittest.main()
