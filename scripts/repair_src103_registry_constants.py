#!/usr/bin/env python3
from pathlib import Path
from pprint import pformat
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    with (ROOT / path).open(encoding='utf-8') as f:
        return yaml.safe_load(f)

registry = load('corpus/index.yaml')
witnesses = {x['source_id']: x for x in registry['reviewed_witnesses']}

complete = {
    'CORPUS-SRC-102': {
        'status_id': 'CORPUS-STATUS-102',
        'witness_id': 'CORPUS-WIT-102',
        'study_id': 'CORPUS-STUDY-011',
        'internal_study_id': 'SPINOZA-PREFACE-STUDY-001',
        'study_path': 'studies/theologico-political/preface-to-spinozas-critique-of-religion/sequential-reconstruction.yaml',
        'witness_record_path': 'studies/theologico-political/preface-to-spinozas-critique-of-religion/reviewed-witness.yaml',
        'printed_page_range': {'start': 137, 'end': 180},
        'pdf_page_range_one_based': 'PENDING_DIRECT_OFFSET_VERIFICATION',
        'reading_state': 'COMPLETE_FOR_QUALIFIED_1997_PLATFORM_REFERENCE_WITNESS',
        'platform_reference': True,
        'platform_object_identifier': 'file_0000000073c081fd9fb65f9ea7552cde',
    },
    'CORPUS-SRC-103': {
        'status_id': 'CORPUS-STATUS-103',
        'witness_id': 'CORPUS-WIT-103',
        'study_id': 'CORPUS-STUDY-012',
        'internal_study_id': 'SPINOZA-TREATISE-STUDY-001',
        'study_path': 'studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/sequential-reconstruction.yaml',
        'witness_record_path': 'studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/reviewed-witness.yaml',
        'printed_page_range': {'start': 181, 'end': 233},
        'pdf_page_range_one_based': {'start': 200, 'end': 252},
        'reading_state': 'COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS',
        'platform_reference': False,
    },
    'CORPUS-SRC-105': {
        'status_id': 'CORPUS-STATUS-105', 'witness_id': 'CORPUS-WIT-105', 'study_id': 'CORPUS-STUDY-009',
        'internal_study_id': 'COHEN-STUDY-001',
        'study_path': 'studies/theologico-political/introductory-essay-hermann-cohen-religion-of-reason/sequential-reconstruction.yaml',
        'witness_record_path': 'studies/theologico-political/introductory-essay-hermann-cohen-religion-of-reason/reviewed-witness.yaml',
        'printed_page_range': {'start': 233, 'end': 247}, 'pdf_page_range_one_based': {'start': 237, 'end': 251},
        'reading_state': 'COMPLETE_FOR_REVIEWED_1983_COLLECTED_WITNESS', 'platform_reference': False,
    },
    'CORPUS-SRC-109': {
        'status_id': 'CORPUS-STATUS-109', 'witness_id': 'CORPUS-WIT-109', 'study_id': 'CORPUS-STUDY-008',
        'internal_study_id': 'JA-STUDY-001',
        'study_path': 'studies/theologico-political/jerusalem-and-athens/sequential-reconstruction.yaml',
        'witness_record_path': None,
        'printed_page_range': {'start': 147, 'end': 173}, 'pdf_page_range_one_based': {'start': 151, 'end': 177},
        'reading_state': 'COMPLETE_FOR_REVIEWED_1983_COLLECTED_WITNESS', 'platform_reference': False,
    },
    'CORPUS-SRC-111': {
        'status_id': 'CORPUS-STATUS-111', 'witness_id': 'CORPUS-WIT-111', 'study_id': 'CORPUS-STUDY-010',
        'internal_study_id': 'TALMON-STUDY-001',
        'study_path': 'studies/theologico-political/review-talmon-nature-of-jewish-history/sequential-reconstruction.yaml',
        'witness_record_path': 'studies/theologico-political/review-talmon-nature-of-jewish-history/reviewed-witness.yaml',
        'printed_page_range': {'start': 232, 'end': 232}, 'pdf_page_range_one_based': {'start': 236, 'end': 236},
        'reading_state': 'COMPLETE_FOR_REVIEWED_1983_COLLECTED_WITNESS', 'platform_reference': False,
    },
}

witness_only = {}
for n in range(101, 120):
    source_id = f'CORPUS-SRC-{n:03d}'
    if source_id in complete:
        continue
    w = witnesses[source_id]
    witness_only[source_id] = {
        'status_id': f'CORPUS-STATUS-{n:03d}',
        'witness_id': f'CORPUS-WIT-{n:03d}',
        'witness_record_path': w['witness_record_path'],
        'printed_page_range': w['printed_page_range'],
        'pdf_page_range_one_based': w['pdf_page_range_one_based'],
        'container_sha256': w['container_sha256'],
        'container_file_size_bytes': w['container_file_size_bytes'],
        'container_page_count': w['container_page_count'],
    }

path = ROOT / 'corpus_registry.py'
text = path.read_text(encoding='utf-8')
region = (
    'COMPLETE_TP_ITEMS: dict[str, dict[str, Any]] = ' + pformat(complete, width=110, sort_dicts=False) + '\n\n'
    'WITNESS_ONLY_TP_ITEMS: dict[str, dict[str, Any]] = ' + pformat(witness_only, width=110, sort_dicts=False) + '\n\n\n'
)
text, count = re.subn(
    r'COMPLETE_TP_ITEMS: dict\[str, dict\[str, Any\]\] = \{.*?\n\nclass CorpusRegistryError',
    region + 'class CorpusRegistryError',
    text,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit('Could not replace corpus registry state-table region')
path.write_text(text, encoding='utf-8')
print('Repaired corpus registry complete/witness-only state tables.')
