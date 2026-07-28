#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'tests/test_corpus_registry.py'
text = p.read_text(encoding='utf-8')
start = text.index('    def test_fourteen_tp_sources_have_witnesses_but_still_require_study')
end = text.index('    def test_spinoza_treatise_witness_and_study_are_registered', start)
section = text[start:end].replace(
    'self.assertEqual(status["status"]["independent_sequential_study"], "SPINOZA-TREATISE-STUDY-001")',
    'self.assertEqual(status["status"]["independent_sequential_study"], "NOT_YET_COMPLETED")',
)
p.write_text(text[:start] + section + text[end:], encoding='utf-8')
print('Fixed witness-only study expectation.')
