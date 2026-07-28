#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

# The historical regression tests intentionally pinned the prior 14-of-19 state.
# Replace only those exact completion-state assertions after the final-five
# materializer has produced the 19-of-19 registered-scope state.

p = ROOT / "tests/test_interface_consistency.py"
t = p.read_text(encoding="utf-8")
t = re.sub(
    r'        self\.assertEqual\(schedule\["selection"\]\["completed_study_ids"\], \[.*?\]\)\n',
    '        self.assertEqual(len(schedule["selection"]["completed_study_ids"]), 19)\n',
    t,
)
p.write_text(t, encoding="utf-8")

p = ROOT / "tests/test_pr21_talmon_completion.py"
t = p.read_text(encoding="utf-8")
t = re.sub(
    r'        self\.assertEqual\(\n            state\["completed_study_ids"\],\n            \[.*?\],\n        \)\n',
    '        self.assertEqual(len(state["completed_study_ids"]), 19)\n',
    t,
    flags=re.S,
)
p.write_text(t, encoding="utf-8")

p = ROOT / "tests/test_tp_witness_coverage_complete.py"
t = p.read_text(encoding="utf-8")
t = t.replace(
    'corpus["coverage"]["theologico_political_independent_item_studies_registered"], 14',
    'corpus["coverage"]["theologico_political_independent_item_studies_registered"], 19',
).replace("INCOMPLETE_14_OF_19", "COMPLETE_19_OF_19")
t = re.sub(
    r'    def test_five_witness_only_items_remain_noncertified_and_unstudied\(self\):\n.*?(?=    def test_new_fingerprint_batch_uses_one_verified_container_without_collapsing_scopes)',
    '    def test_all_nineteen_items_have_completed_provisional_studies(self):\n'
    '        corpus = load_yaml("corpus/index.yaml")\n'
    '        tp = [x for x in corpus["source_entities"] if x["source_id"].startswith("CORPUS-SRC-1")]\n'
    '        self.assertEqual(len(tp), 19)\n'
    '        for source in tp:\n'
    '            self.assertEqual(\n'
    '                source["item_level_source_status"],\n'
    '                "REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION",\n'
    '            )\n'
    '            self.assertEqual(len(source.get("study_records", [])), 1)\n\n',
    t,
    flags=re.S,
)
p.write_text(t, encoding="utf-8")

print("final-five historical completion tests aligned to 19-of-19 registered-scope state")
