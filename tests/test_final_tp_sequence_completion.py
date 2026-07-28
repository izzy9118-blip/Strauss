from pathlib import Path
import unittest
import yaml
ROOT=Path(__file__).resolve().parents[1]
def load(p):
    with (ROOT/p).open(encoding="utf-8") as f:return yaml.safe_load(f)
class FinalTPSequenceCompletionTests(unittest.TestCase):
    def test_final_five_bindings_and_witness_distinction(self):
        corpus=load("corpus/index.yaml")
        expected={"CORPUS-SRC-114":("CORPUS-STUDY-022","GOOD-SOCIETY-STUDY-001"),"CORPUS-SRC-115":("CORPUS-STUDY-023","UNSPOKEN-PROLOGUE-STUDY-001"),"CORPUS-SRC-117":("CORPUS-STUDY-024","GIVING-ACCOUNTS-STUDY-001"),"CORPUS-SRC-118":("CORPUS-STUDY-025","PHILOSOPHY-LAW-PLAN-STUDY-001"),"CORPUS-SRC-119":("CORPUS-STUDY-026","HIERO-RESTATEMENT-LAST-PARAGRAPH-STUDY-001")}
        for sid,(cid,iid) in expected.items():
            src=next(x for x in corpus["source_entities"] if x["source_id"]==sid); self.assertEqual(src["study_records"],[cid])
            status=load(next(x for x in corpus["source_status_records"] if x["source_id"]==sid)["path"]); self.assertEqual(status["status"]["independent_sequential_study"],iid); self.assertEqual(status["termination"]["study_state"],"COMPLETE_PROVISIONAL")
            wit=next(x for x in corpus["reviewed_witnesses"] if x["source_id"]==sid); wr=load(wit["witness_record_path"]); self.assertEqual(wr["termination"]["study_state"],"INCOMPLETE")
    def test_src115_correction_is_preserved(self):
        st=load("studies/theologico-political/an-unspoken-prologue/sequential-reconstruction.yaml"); text=" ".join(st["comparison_with_active_predecessor"]["qualifications"]); self.assertIn("no discussion of orthodoxy, unbelief, Zionism, or medieval philosophy",text); self.assertIn("source conflation",text)
    def test_src117_speaker_layers_and_autobiography_limit(self):
        st=load("studies/theologico-political/a-giving-of-accounts/sequential-reconstruction.yaml"); self.assertIn("jacob_klein",st["speaker_and_documentary_layers"]); self.assertIn("tape_break",st["speaker_and_documentary_layers"]); self.assertIn("starting point", " ".join(st["source_limits"]))
    def test_src118_and_src119_editorial_limits(self):
        a=load("studies/theologico-political/plan-philosophy-and-the-law-historical-essays/sequential-reconstruction.yaml"); self.assertEqual(a["source"]["editorial_provenance"]["editor_mature_view_claim"],"EDITORIAL_INTERPRETATION_NOT_STRAUSS_STATEMENT")
        b=load("studies/theologico-political/restatement-on-xenophons-hiero/sequential-reconstruction.yaml"); self.assertEqual(b["termination"]["registered_scope"],"LAST_PARAGRAPH_ONLY"); self.assertIn("universal state", " ".join(b["comparison_with_active_predecessor"]["qualifications"]))
    def test_sequence_complete_repository_not_certified(self):
        c=load("corpus/index.yaml"); m=load("manifest.yaml"); s=load("history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml"); self.assertEqual(c["coverage"]["theologico_political_independent_item_studies_registered"],19); self.assertEqual(c["termination"]["theologico_political_independent_study_state"],"COMPLETE_19_OF_19"); self.assertEqual(s["termination"]["independent_sequential_reconstruction"],"COMPLETE_19_OF_19"); self.assertEqual(s["termination"]["next_item_study"],"NONE"); self.assertEqual(m["status"]["semantic_completion"],"INCOMPLETE"); self.assertEqual(m["status"]["doctrinal_certification"],"NOT_CERTIFIED")
if __name__=="__main__": unittest.main()
