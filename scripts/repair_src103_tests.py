#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def edit(path, fn):
    p = ROOT / path
    p.write_text(fn(p.read_text(encoding='utf-8')), encoding='utf-8')

# Correct overly broad first-pass replacements in corpus tests.
def corpus(text):
    text = text.replace('{"start": 237, "end": 252}', '{"start": 237, "end": 251}')
    text = text.replace('{"start": 152, "end": 177}', '{"start": 151, "end": 177}')
    text = text.replace('8479ed41fe952b8ebc5a2a5b6557a482a60de0d13032785a68f11d52ea8b4fb6', '8479ed41fe951b8ebc5a2a5b6557a482a60de0d13032785a68f11d51ea8b4fb6')
    # Only the witness-only loop must retain the pending-study status.
    marker = '    def test_fourteen_tp_sources_have_witnesses_but_still_require_study'
    start = text.index(marker)
    end = text.index('    def test_spinoza_treatise_witness_and_study_are_registered', start)
    section = text[start:end].replace(
        '"REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION"',
        '"REVIEWED_ITEM_WITNESS_REGISTERED_SEQUENTIAL_RECONSTRUCTION_REQUIRED"',
    )
    return text[:start] + section + text[end:]
edit('tests/test_corpus_registry.py', corpus)

# Witness registration record remains historical; the later source-status record now carries study completion.
def wit103(text):
    text = text.replace(
        'def test_witness_registration_does_not_claim_sequential_study_or_certification(self) -> None:',
        'def test_witness_registration_record_remains_historical_while_source_status_advances(self) -> None:',
    )
    text = text.replace(
        '        self.assertEqual(status["status"]["independent_sequential_study"], "NOT_YET_COMPLETED")\n',
        '        self.assertEqual(status["status"]["independent_sequential_study"], "SPINOZA-TREATISE-STUDY-001")\n',
    )
    text = text.replace(
        '        self.assertEqual(status["termination"]["study_state"], "INCOMPLETE")\n',
        '        self.assertEqual(status["termination"]["study_state"], "COMPLETE_PROVISIONAL")\n',
    )
    return text
edit('tests/test_corpus_wit_103_registration.py', wit103)

# Findings counts and direct SRC103 derivation coverage.
def findings(text):
    text = text.replace('"1.4.0"', '"1.5.0"', 1)
    text = text.replace('self.assertEqual(len(finding_ids), 37)', 'self.assertEqual(len(finding_ids), 40)')
    text = text.replace('self.assertEqual(len(registered), 21)', 'self.assertEqual(len(registered), 23)')
    text = text.replace('self.assertEqual(len(registered), 11)', 'self.assertEqual(len(registered), 12)')
    anchor = '    def test_indexes_are_derived_from_finding_set_bindings(self) -> None:\n'
    if 'def test_spinoza_treatise_study_and_two_local_syntheses_are_explicitly_derived' not in text:
        block = '''    def test_spinoza_treatise_study_and_two_local_syntheses_are_explicitly_derived(self) -> None:\n        study = self._assert_source_derivation(\n            study_id="FINDSET-012",\n            source_id="CORPUS-SRC-103",\n            local_syntheses=[\n                ("FINDSET-122", "theologico-political"),\n                ("FINDSET-123", "wise-vs-vulgar"),\n            ],\n        )\n        self.assertEqual(study["witness_id"], "CORPUS-WIT-103")\n        self.assertEqual(study["original_1948_journal_comparison"], "PENDING")\n        self.assertEqual(study["successor_effect"], "NONE")\n\n'''
        text = text.replace(anchor, block + anchor)
    return text
edit('tests/test_findings_registry.py', findings)

# 19/19 witnesses, 5/19 studies, 14 witness-only items.
def coverage(text):
    text = text.replace('theologico_political_independent_item_studies_registered"], 4', 'theologico_political_independent_item_studies_registered"], 5')
    text = text.replace('def test_fifteen_witness_only_items_remain_noncertified_and_unstudied', 'def test_fourteen_witness_only_items_remain_noncertified_and_unstudied')
    text = text.replace('{"CORPUS-SRC-102", "CORPUS-SRC-105", "CORPUS-SRC-109", "CORPUS-SRC-111"}', '{"CORPUS-SRC-102", "CORPUS-SRC-103", "CORPUS-SRC-105", "CORPUS-SRC-109", "CORPUS-SRC-111"}')
    text = text.replace('self.assertEqual(len(witness_only), 15)', 'self.assertEqual(len(witness_only), 14)')
    return text
edit('tests/test_tp_witness_coverage_complete.py', coverage)

# Collapse repeated FINDSET-012 lines caused by repeated materialization.
def consistency(text):
    line = '            "FINDSET-012": [("FINDSET-122", "theologico-political"), ("FINDSET-123", "wise-vs-vulgar")],\n'
    first = text.find(line)
    if first != -1:
        before = text[:first + len(line)]
        after = text[first + len(line):].replace(line, '')
        text = before + after
    return text
edit('tests/test_interface_consistency.py', consistency)

print('Repaired SRC103 integration regression tests.')
