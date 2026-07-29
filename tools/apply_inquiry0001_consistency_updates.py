from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def replace(path_str: str, old: str, new: str) -> None:
    path = ROOT / path_str
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"expected text not found in {path_str}: {old}")
    path.write_text(text.replace(old, new), encoding="utf-8")

replace("manifest.yaml", "registry_version: 1.16.0", "registry_version: 1.17.0")
replace("migrations/lean-operational-interface.yaml", "findings_registry_version: 1.16.0", "findings_registry_version: 1.17.0")

replace("tests/test_findings_registry.py", '"1.16.0"', '"1.17.0"')
replace("tests/test_findings_registry.py", "len(finding_ids), 88", "len(finding_ids), 89")
replace("tests/test_findings_registry.py", "len(registered), 57", "len(registered), 58")
replace("tests/test_pr21_talmon_completion.py", '"1.16.0"', '"1.17.0"')

replace("tests/test_corpus_registry.py", 'witness_record["termination"]["study_state"], "INCOMPLETE"', 'witness_record["termination"]["study_state"], "COMPLETE_PROVISIONAL"')
replace("tests/test_corpus_wit_103_registration.py", 'witness["status"]["independent_sequential_study"], "NOT_YET_COMPLETED"', 'witness["status"]["independent_sequential_study"], "COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS"')

(ROOT / "tools/apply_inquiry0001_consistency_updates.py").unlink()
(ROOT / ".github/workflows/apply-inquiry0001-consistency-updates.yml").unlink()
