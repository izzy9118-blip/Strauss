from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    with (ROOT / rel).open(encoding="utf-8") as f:
        return yaml.safe_load(f)

class OwnerAuthorizationTests(unittest.TestCase):
    def test_repository_is_owner_certified_and_active(self):
        auth = load("governance/repository-authorization.yaml")
        manifest = load("manifest.yaml")
        registry = load("problems/registry.yaml")
        self.assertEqual(auth["status"]["certification"], "OWNER_CERTIFIED")
        self.assertEqual(auth["status"]["operational_authorization"], "FULLY_AUTHORIZED")
        self.assertEqual(manifest["status"]["doctrinal_certification"], "OWNER_CERTIFIED_FOR_OPERATIONAL_USE")
        self.assertEqual(manifest["status"]["activation"], "ACTIVE_OWNER_AUTHORIZED")
        self.assertEqual(manifest["sanctum_contract"]["completed_interface_repin_status"], "AUTHORIZED_FOR_CERTIFIED_OPERATIONAL_REPIN")
        self.assertEqual(registry["status"]["activation"], "ACTIVE_OWNER_AUTHORIZED")
        self.assertTrue(all(p["migration_status"] == "CERTIFIED_ACTIVE_OWNER_AUTHORIZED" for p in registry["canonical_problems"]))

    def test_certification_does_not_erase_open_research(self):
        manifest = load("manifest.yaml")
        corpus = load("corpus/index.yaml")
        findings = load("findings/index.yaml")
        self.assertEqual(manifest["status"]["semantic_completion"], "INCOMPLETE")
        self.assertEqual(corpus["status"]["corpus_completion"], "INCOMPLETE_OPEN_CORPUS")
        self.assertEqual(findings["status"]["findings_completion"], "INCOMPLETE_OPEN_FINDINGS_STORE")
        self.assertGreater(len(corpus["corpus_gaps"]), 0)
        self.assertGreater(len(findings["findings_gaps"]), 0)

if __name__ == "__main__":
    unittest.main()
