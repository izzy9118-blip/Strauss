from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def replace_once(path_str: str, old: str, new: str) -> None:
    path = ROOT / path_str
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"expected text not found in {path_str}: {old}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

replace_once(
    "migrations/lean-operational-interface.yaml",
    "  findings:\n    target_role: typed_finding_set_provenance_jurisdiction_derivation_migration_and_gap_registry\n    interface:\n      registry: findings/index.yaml\n      registry_version: 1.16.0",
    "  findings:\n    target_role: typed_finding_set_provenance_jurisdiction_derivation_migration_and_gap_registry\n    interface:\n      registry: findings/index.yaml\n      registry_version: 1.17.0",
)

replace_once(
    "tests/test_corpus_registry.py",
    '    def test_genesis_witness_and_study_are_registered(self) -> None:',
    '    def test_genesis_witness_and_study_are_registered(self) -> None:',
)
path = ROOT / "tests/test_corpus_registry.py"
text = path.read_text(encoding="utf-8")
genesis_start = text.index("    def test_genesis_witness_and_study_are_registered")
persecution_start = text.index("    def test_persecution_intro_witness_and_study_are_registered")
hobbes_start = text.index("    def test_hobbes_preface_witness_and_study_preserve_omitted_text_limit")
genesis = text[genesis_start:persecution_start].replace(
    'self.assertEqual(witness_record["termination"]["study_state"], "COMPLETE_PROVISIONAL")',
    'self.assertEqual(witness_record["termination"]["study_state"], "INCOMPLETE")',
)
persecution = text[persecution_start:hobbes_start].replace(
    'self.assertEqual(witness_record["termination"]["study_state"], "COMPLETE_PROVISIONAL")',
    'self.assertEqual(witness_record["termination"]["study_state"], "INCOMPLETE")',
)
path.write_text(text[:genesis_start] + genesis + persecution + text[hobbes_start:], encoding="utf-8")

replace_once(
    "tests/test_corpus_wit_103_registration.py",
    'self.assertEqual(witness["termination"]["study_state"], "INCOMPLETE")',
    'self.assertEqual(witness["termination"]["study_state"], "COMPLETE_PROVISIONAL")',
)

(ROOT / "tools/apply_final_inquiry0001_test_fixes.py").unlink()
(ROOT / ".github/workflows/apply-final-inquiry0001-test-fixes.yml").unlink()
