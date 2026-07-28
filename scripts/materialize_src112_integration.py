#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

ROOT = Path(__file__).resolve().parents[1]
STUDY = "studies/theologico-political/letter-to-editor-state-of-israel/sequential-reconstruction.yaml"
STATUS = "studies/theologico-political/letter-to-editor-state-of-israel/source-status.yaml"
TP_SYN = "problems/theologico-political/synthesis/letter-to-editor-state-of-israel.yaml"
AVM_SYN = "problems/ancients-vs-moderns/synthesis/letter-to-editor-state-of-israel.yaml"
y = YAML(); y.preserve_quotes = True; y.width = 120

def load(p):
    with (ROOT/p).open(encoding="utf-8") as f: return y.load(f)
def save(p,d):
    with (ROOT/p).open("w",encoding="utf-8") as f: y.dump(d,f)
def one(rs,k,v): return next(r for r in rs if r.get(k)==v)
def add(seq,v):
    if v not in seq: seq.append(v)
def repl(t,a,b,label):
    n=t.count(a)
    if n!=1: raise RuntimeError(f"{label}: expected 1 occurrence, got {n}")
    return t.replace(a,b,1)

def corpus():
    p="corpus/index.yaml"; d=load(p)
    if d["identity"]["version"]!="1.20.0": raise RuntimeError("corpus predecessor mismatch")
    d["identity"]["version"]="1.21.0"; d["revision_history"]["predecessor_version"]="1.20.0"; d["revision_history"]["predecessor_blob_sha"]="PRESERVED_BY_GIT"
    d["revision_history"]["reason"]="Register STATE-ISRAEL-LETTER-STUDY-001 as the thirteenth complete provisional Theologico-Political item study and CORPUS-STUDY-020 while preserving pending National Review comparison, material qualification of the predecessor's theological wording, noncorroboration, noncertification, predecessor authority, and no successor effect."
    s=one(d["source_entities"],"source_id","CORPUS-SRC-112")
    s["item_level_source_status"]="REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION"
    s["study_status"]="COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS"
    s["study_records"]=["CORPUS-STUDY-020"]
    s["limits"]=["reviewed witness is the fingerprinted 1997 SUNY collected reprint, not a separately reviewed 1957 National Review printing","printed pages 413-414 correspond to one-based PDF pages 432-433","the source strongly supports political dignity and moral force but does not explicitly state the predecessor's redemption, messianic-fulfillment, or providence language","STATE-ISRAEL-LETTER-STUDY-001 is source-local and not independent corroboration of Israeli institutions, Herzl, emancipation history, or represented theological claims"]
    one(d["source_status_records"],"status_id","CORPUS-STATUS-112")["completion"]="REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION"
    if not any(r.get("study_id")=="CORPUS-STUDY-020" for r in d["study_records"]):
        d["study_records"].append(CommentedMap([("study_id","CORPUS-STUDY-020"),("source_id","CORPUS-SRC-112"),("path",STUDY),("record_role","SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION"),("completion","COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS"),("certification","NOT_CERTIFIED")]))
    c=d["coverage"]; c["study_records_registered"]=20; c["theologico_political_independent_item_studies_registered"]=13; c["current_studies_tree_yaml_records_accounted_for"]=60
    one(d["corpus_gaps"],"gap_id","CORPUS-GAP-003")["statement"]="All nineteen predecessor writings have bounded source identities and reviewed item witnesses; thirteen have complete provisional sequential studies, while the remaining six lack independent item studies."
    add(d["validation_rules"],"CORPUS-SRC-112 preserves the fingerprinted reviewed witness, complete provisional sequential reconstruction, pending original National Review comparison, material predecessor qualification, noncorroboration, noncertification, and no-successor safeguards")
    d["validation_rules"]=[r.replace("all seven witness-only Theologico-Political sources","all six witness-only Theologico-Political sources") if isinstance(r,str) else r for r in d["validation_rules"]]
    d["termination"]["theologico_political_independent_study_state"]="INCOMPLETE_13_OF_19"
    d["termination"]["next_required_units"]=["conduct independent sequential reconstruction of CORPUS-SRC-110 from CORPUS-WIT-110","compare the reviewed CORPUS-SRC-112 item with National Review 3, no. 1 (5 January 1957): 23 when separately available","conduct independent sequential reconstruction for the remaining six writings","expand independent Herzl, Israeli institutional, emancipation-history, biblical, Jewish, and political witnesses"]
    save(p,d)

def findings():
    p="findings/index.yaml"; d=load(p)
    if d["identity"]["version"]!="1.12.0": raise RuntimeError("findings predecessor mismatch")
    d["identity"]["version"]="1.13.0"; d["revision_history"]["predecessor_version"]="1.12.0"; d["revision_history"]["predecessor_blob_sha"]="PRESERVED_BY_GIT"
    d["revision_history"]["reason"]="Register STATE-ISRAEL-LETTER-STUDY-001 as FINDSET-020 and jurisdiction-preserving syntheses FINDSET-140 and FINDSET-141 while preserving pending National Review comparison, predecessor qualification, noncorroboration, noncertification, and no-successor safeguards."
    fs=d["finding_sets"]
    if not any(r.get("finding_set_id")=="FINDSET-020" for r in fs):
        i=next(i for i,r in enumerate(fs) if r.get("finding_set_id")=="FINDSET-101")
        fs.insert(i,CommentedMap([("finding_set_id","FINDSET-020"),("path",STUDY),("record_class","SOURCE_SPECIFIC_STUDY"),("record_role","SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION"),("source_bindings",["CORPUS-SRC-112"]),("problem_bindings",["theologico-political","ancients-vs-moderns"]),("status","COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS"),("certification","NOT_CERTIFIED"),("derived_local_syntheses",["FINDSET-140","FINDSET-141"]),("witness_id","CORPUS-WIT-112"),("original_1957_national_review_comparison","PENDING"),("predecessor_retest_state","PARTIAL_CONFIRMATION_WITH_MATERIAL_QUALIFICATION"),("independent_corroboration","INCOMPLETE"),("successor_effect","NONE")]))
    if not any(r.get("finding_set_id")=="FINDSET-140" for r in fs):
        i=next(i for i,r in enumerate(fs) if r.get("finding_set_id")=="FINDSET-201")
        fs.insert(i,CommentedMap([("finding_set_id","FINDSET-140"),("path",TP_SYN),("record_class","PROBLEM_LOCAL_SYNTHESIS"),("record_role","SOURCE_TO_PROBLEM_SYNTHESIS"),("source_bindings",["CORPUS-SRC-112"]),("problem_bindings",["theologico-political"]),("adjacent_problem_references",["ancients-vs-moderns"]),("derived_from",["FINDSET-020"]),("status","PROVISIONAL_NOT_CERTIFIED"),("certification","NOT_CERTIFIED"),("successor_effect","NONE")]))
        fs.insert(i+1,CommentedMap([("finding_set_id","FINDSET-141"),("path",AVM_SYN),("record_class","PROBLEM_LOCAL_SYNTHESIS"),("record_role","SOURCE_TO_PROBLEM_SYNTHESIS"),("source_bindings",["CORPUS-SRC-112"]),("problem_bindings",["ancients-vs-moderns"]),("theologico_political_reference","theologico-political"),("derived_from",["FINDSET-020"]),("status","PROVISIONAL_NOT_CERTIFIED"),("certification","NOT_CERTIFIED"),("successor_effect","NONE")]))
    keys=[r["canonical_key"] for r in load("problems/registry.yaml")["canonical_problems"]]; bp=CommentedMap((k,[]) for k in keys)
    direct=["CORPUS-SRC-001","CORPUS-SRC-002","CORPUS-SRC-003","CORPUS-SRC-101","CORPUS-SRC-102","CORPUS-SRC-103","CORPUS-SRC-104","CORPUS-SRC-105","CORPUS-SRC-106","CORPUS-SRC-107","CORPUS-SRC-108","CORPUS-SRC-111","CORPUS-SRC-112","CORPUS-SRC-113","CORPUS-SRC-116"]; bs=CommentedMap((k,[]) for k in direct); bs["CORPUS-SRC-101-119"]=[]
    pred={f"CORPUS-SRC-{n:03d}" for n in range(101,120)}; separate=set(direct)&pred; bc=CommentedMap((k,[]) for k in ["SOURCE_SPECIFIC_STUDY","INTEGRATION_GOVERNANCE_RECORD","PROBLEM_LOCAL_SYNTHESIS","MIGRATION_TRANSACTION_LEDGER","PRESERVED_FINDING_BASIS"])
    for r in fs:
        fid=r["finding_set_id"]
        for k in r.get("problem_bindings",[]):
            if k in bp: bp[k].append(fid)
        binds=set(r.get("source_bindings",[]))
        for k in direct:
            if k in binds: bs[k].append(fid)
        if binds & pred and not (len(binds)==1 and next(iter(binds)) in separate): bs["CORPUS-SRC-101-119"].append(fid)
        cl=r.get("record_class")
        if cl in {"ACTIVE_PREDECESSOR_FINDING_BASIS","ACCEPTED_MIGRATION_SOURCE_FINDING_BASIS"}: bc["PRESERVED_FINDING_BASIS"].append(fid)
        elif cl in bc: bc[cl].append(fid)
    d["indexes"]["by_problem"]=bp; d["indexes"]["by_source"]=bs; d["indexes"]["by_record_class"]=bc
    c=d["coverage"]; c["finding_sets_registered"]=66; c["source_specific_and_integration_records_registered"]=20; c["problem_syntheses_registered"]=41; c["current_problem_synthesis_tree_yaml_records_accounted_for"]=41; c["corpus_study_records_accounted_for"]=20
    one(d["findings_gaps"],"gap_id","FINDINGS-GAP-003")["statement"]="Thirteen of the nineteen Theologico-Political writings now have complete provisional item studies; the remaining six lack individual sequential studies."
    add(d["validation_rules"],"FINDSET-020 must derive only FINDSET-140 and FINDSET-141, preserve CORPUS-WIT-112, pending National Review comparison, material predecessor qualification, noncorroboration, and no-successor safeguards")
    save(p,d)

def manifest():
    p="manifest.yaml"; d=load(p)
    if d["identity"]["version"]!="1.16.0": raise RuntimeError("manifest predecessor mismatch")
    d["identity"]["version"]="1.17.0"; d["revision_history"]["predecessor_version"]="1.16.0"; d["revision_history"]["predecessor_blob_sha"]="PRESERVED_BY_GIT"
    d["revision_history"]["reason"]="Register STATE-ISRAEL-LETTER-STUDY-001 as the thirteenth complete provisional Theologico-Political item study and synchronize corpus v1.21.0, findings v1.13.0, audit v3.5.0, mapping v1.17.0, process v1.19.0, and schedule v1.17.0 while preserving six pending studies, National Review comparison, noncertification, predecessor authority, and the Sanctum repin block."
    d["audit"]["version"]="3.5.0"; d["component_completion"]["theologico_political_item_level_source_statuses"]="19_OF_19_IDENTITIES_19_OF_19_REVIEWED_ITEM_WITNESSES_13_OF_19_COMPLETE_PROVISIONAL_ITEM_STUDIES"
    d["corpus"]["registry_version"]="1.21.0"; s=d["corpus"]["theologico_political_item_level_statuses"]; s["independent_sequential_study_count"]=13; s["remaining_without_independent_sequential_study"]=6; add(s["completed_study_ids"],"STATE-ISRAEL-LETTER-STUDY-001")
    s["rule"]="All nineteen predecessor items have reviewed witnesses and thirteen have complete provisional source studies. Witness and study completion remain distinct from independent corroboration, doctrinal certification, migration completion, successor activation, or repository completion."
    d["corpus"]["limitation"]="All nineteen predecessor writings have bounded identities and reviewed item witnesses. Thirteen have complete provisional sequential studies; explicit omission, transcription, editorial, textual-state, and predecessor-qualification limits remain active, and six sources still lack independent studies."
    d["findings"]["registry_version"]="1.13.0"; d["findings"]["newly_registered"]=["FINDSET-020","FINDSET-140","FINDSET-141"]
    save(p,d)

def audit():
    p="audits/operational-completeness.yaml"; d=load(p)
    if d["identity"]["version"]!="3.4.0": raise RuntimeError("audit predecessor mismatch")
    d["identity"]["version"]="3.5.0"; d["revision_history"]["predecessor_version"]="3.4.0"; d["revision_history"]["predecessor_blob_sha"]="PRESERVED_BY_GIT"; d["revision_history"]["reason"]="Complete STATE-ISRAEL-LETTER-STUDY-001, advance study coverage to thirteen of nineteen, preserve six pending studies, National Review comparison, and the material predecessor qualification."
    d["basis"]["current_revision_scope"]="production/corpus-src-112-sequential-reconstruction"
    for v in ["STATE-ISRAEL-LETTER-STUDY-001 complete provisional sequential reconstruction","CORPUS-STUDY-020 and FINDSET-020 typed registrations","FINDSET-140 and FINDSET-141 jurisdiction-preserving problem-local syntheses"]: add(d["summary"]["completed_operational_units"],v)
    s=d["summary"]["theologico_political_item_level_status"]; s["independently_reconstructed_count_within_this_sequence"]=13; s["remaining_without_independent_sequential_study"]=6; add(s["completed_source_ids"],"CORPUS-SRC-112"); add(s["completed_witness_ids"],"CORPUS-WIT-112"); add(s["completed_study_ids"],"STATE-ISRAEL-LETTER-STUDY-001"); s["witness_only_source_ids"]=[x for x in s["witness_only_source_ids"] if x!="CORPUS-SRC-112"]; s["witness_only_witness_ids"]=[x for x in s["witness_only_witness_ids"] if x!="CORPUS-WIT-112"]
    s["interpretation_limit"]="All nineteen predecessor items have reviewed witnesses and thirteen completed studies are independent reconstructions relative to predecessor and collection-level synthesis. Six witness registrations remain study-pending; none is independent corroboration, and SRC112 materially qualifies rather than silently confirms the predecessor's theological separation language."
    d["summary"]["remaining_major_deficiencies"][0]="six Theologico-Political writings still require independent sequential item studies"
    add(d["production_order"]["completed_in_current_sequence"],"STATE-ISRAEL-LETTER-STUDY-001 with FINDSET-020, FINDSET-140, and FINDSET-141")
    d["production_order"]["next"]=["run complete structural and behavioral validation for the thirteenth Theologico-Political item study","conduct CORPUS-SRC-110 independent sequential reconstruction from its registered witness","continue the remaining five independent sequential reconstructions after CORPUS-SRC-110","expand independent source-tradition witnesses and textual-state comparisons","validate actual ministerial reports against the full contract stack"]
    save(p,d)

def mapping():
    p="migrations/lean-operational-interface.yaml"; d=load(p)
    if d["identity"]["version"]!="1.16.0": raise RuntimeError("mapping predecessor mismatch")
    d["identity"]["version"]="1.17.0"; d["revision_history"]["predecessor_version"]="1.16.0"; d["revision_history"]["predecessor_blob_sha"]="PRESERVED_BY_GIT"; d["revision_history"]["reason"]="Synchronize STATE-ISRAEL-LETTER-STUDY-001, corpus v1.21.0, findings v1.13.0, audit v3.5.0, process v1.19.0, and schedule v1.17.0 while preserving six pending studies, National Review comparison, material predecessor qualification, noncorroboration, and no successor effect."
    d["completion_audit"]["version"]="3.5.0"; d["production_process"]["completed_study_subunit"]="THIRTEEN_OF_19_COMPLETE_PROVISIONAL_SIX_PENDING"
    c=d["mappings"]["corpus"]; c["interface"]["registry_version"]="1.21.0"; s=c["theologico_political_item_level_statuses"]; s["independent_sequential_study_count"]=13; s["remaining_without_independent_sequential_study"]=6; add(s["completed_study_ids"],"STATE-ISRAEL-LETTER-STUDY-001"); s["witness_only_source_ids"]=[x for x in s["witness_only_source_ids"] if x!="CORPUS-SRC-112"]
    c["limit"]="Current-state exhaustiveness, nineteen reviewed item witnesses, and thirteen complete provisional item studies do not create a complete corpus, supply independent corroboration, resolve textual-state or predecessor-qualification limits, certify findings, or authorize migration and activation."
    for rel in [CommentedMap([("path",TP_SYN),("source","CORPUS-SRC-112"),("derivation","FINDSET-020_TO_FINDSET-140")]),CommentedMap([("path",AVM_SYN),("source","CORPUS-SRC-112"),("derivation","FINDSET-020_TO_FINDSET-141")])]:
        if not any(x.get("path")==rel["path"] for x in d["mappings"]["problems"]["new_source_relations"]): d["mappings"]["problems"]["new_source_relations"].append(rel)
    for sec in ("hermeneutics","method"):
        apps=d["mappings"][sec].setdefault("source_applications",[])
        if not any(x.get("record")==STUDY for x in apps):
            e=CommentedMap([("record",STUDY),("state","COMPLETE_PROVISIONAL_FOR_ONE_REVIEWED_ITEM")]);
            if sec=="method": e["reading_units"]=4
            apps.append(e)
    f=d["mappings"]["findings"]; f["interface"]["registry_version"]="1.13.0"; f["newly_registered"]=[CommentedMap([("finding_set_id","FINDSET-020"),("path",STUDY)]),CommentedMap([("finding_set_id","FINDSET-140"),("path",TP_SYN),("derived_from","FINDSET-020")]),CommentedMap([("finding_set_id","FINDSET-141"),("path",AVM_SYN),("derived_from","FINDSET-020")])]
    d["completed_production_units"]=["speech, hermeneutic, and method operational contracts","complete read-only foundational problem bundles","typed current-state corpus and findings registries","complete 19-of-19 Theologico-Political source-identity and reviewed-witness range","thirteen complete provisional Theologico-Political sequential reconstructions through STATE-ISRAEL-LETTER-STUDY-001","jurisdiction-preserving source-to-problem syntheses through FINDSET-141"]
    d["next_production_units"]=["validate and merge the bounded CORPUS-SRC-112 production unit","conduct CORPUS-SRC-110 independent sequential reconstruction","continue the remaining five item studies after CORPUS-SRC-110","expand independent witness reconstruction and textual-state comparison","validate actual candidate ministerial reports"]
    save(p,d)

def process():
    p="history/production-plans/2026-07-27-ten-step-completion-process.yaml"; d=load(p)
    if d["identity"]["version"]!="1.18.0": raise RuntimeError("process predecessor mismatch")
    d["identity"]["version"]="1.19.0"; d["revision_history"]["predecessor_version"]="1.18.0"; d["revision_history"]["predecessor_blob_sha"]="PRESERVED_BY_GIT"; d["revision_history"]["reason"]="Complete STATE-ISRAEL-LETTER-STUDY-001 as the thirteenth provisional Theologico-Political sequential reconstruction and advance the next study unit to CORPUS-SRC-110 while preserving the National Review comparison and material predecessor qualification."
    st={x["sequence"]:x for x in d["steps"]}; st[1]["current_version"]="3.5.0"; st[2]["current_version"]="1.17.0"; add(st[7]["completed"],"Letter to the Editor — The State of Israel supplies distinct provisional syntheses to Theologico-Political and Ancients-versus-Moderns while materially qualifying the predecessor's unexpressed theological language"); add(st[8]["completed"],"STATE-ISRAEL-LETTER-STUDY-001 is complete provisional for CORPUS-WIT-112"); st[8]["remaining"][0]="conduct six independent sequential item studies, beginning with CORPUS-SRC-110"; st[9]["completed_in_current_sequence"][0]="tests cover all nineteen Theologico-Political reviewed-witness registrations and distinguish the six witness-only states from the thirteen completed-study states"
    d["current_production_unit"]=CommentedMap([("step",8),("completed_subunit",CommentedMap([("title","Letter to the Editor — The State of Israel independent sequential reconstruction"),("state","COMPLETE_PROVISIONAL_PENDING_BRANCH_VALIDATION_AND_MERGE"),("source_id","CORPUS-SRC-112"),("witness_id","CORPUS-WIT-112"),("study_id","STATE-ISRAEL-LETTER-STUDY-001"),("study_coverage","INCOMPLETE_13_OF_19"),("documentary_limit","ORIGINAL_1957_NATIONAL_REVIEW_COMPARISON_PENDING_AND_PREDECESSOR_THEOLOGICAL_LANGUAGE_MATERIALLY_QUALIFIED") ])),("next_subunit",CommentedMap([("title","What Is Political Philosophy? first-paragraph independent sequential reconstruction"),("source_id","CORPUS-SRC-110"),("witness_id","CORPUS-WIT-110"),("following_source","CORPUS-SRC-114")]))])
    save(p,d)

def schedule():
    p="history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml"; d=load(p)
    if d["identity"]["version"]!="1.16.0": raise RuntimeError("schedule predecessor mismatch")
    d["identity"]["version"]="1.17.0"; d["status"]["independent_sequential_study_completion"]="INCOMPLETE_13_OF_19"; d["revision_history"]["predecessor_version"]="1.16.0"; d["revision_history"]["predecessor_blob_sha"]="PRESERVED_BY_GIT"; d["revision_history"]["reason"]="Complete STATE-ISRAEL-LETTER-STUDY-001 from CORPUS-WIT-112, advancing independent sequential study coverage to 13-of-19 and the next study unit to CORPUS-SRC-110 while preserving complete witness coverage, pending National Review comparison, and predecessor qualification."
    src=None
    for g in d["priority_groups"]:
        for r in g.get("items",[]):
            if r.get("source_id")=="CORPUS-SRC-112": src=r
    if src is None: raise RuntimeError("SRC112 schedule item missing")
    src["state"]="REVIEWED_WITNESS_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDY"
    src["study_id"]="STATE-ISRAEL-LETTER-STUDY-001"
    src["next_action"]="ORIGINAL_1957_NATIONAL_REVIEW_COMPARISON_AND_INDEPENDENT_HERZL_ISRAEL_EMANCIPATION_WITNESS_EXPANSION"
    add(d["selection"]["completed_study_ids"],"STATE-ISRAEL-LETTER-STUDY-001"); d["selection"]["selection_state"]="NINETEEN_REVIEWED_ITEM_WITNESSES_THIRTEEN_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDIES"; d["selection"]["completed_units"]=["all nineteen predecessor source identities have reviewed witnesses","thirteen source studies are complete provisional","six witness-only sources remain pending independent sequential reconstruction","all textual-state, transmission, predecessor-qualification, and independent-corroboration limits remain explicit"]
    d["termination"]["independent_sequential_reconstruction"]="INCOMPLETE_13_OF_19"; d["termination"]["next_item_study"]="CORPUS-SRC-110"; d["next_item_study_unit"]=CommentedMap([("source_id","CORPUS-SRC-110"),("title","What Is Political Philosophy?"),("scope","FIRST_PARAGRAPH_ONLY_AS_REGISTERED_BY_PREDECESSOR"),("action","INDEPENDENT_SEQUENTIAL_RECONSTRUCTION_FROM_REGISTERED_WITNESS"),("prerequisite","SATISFIED_CORPUS_WIT_110_REGISTERED"),("following_source","CORPUS-SRC-114")])
    save(p,d)

def validators():
    p=ROOT/"corpus_registry.py"; t=p.read_text()
    marker=" 'CORPUS-SRC-113': {'status_id': 'CORPUS-STATUS-113',"
    block=" 'CORPUS-SRC-112': {'status_id': 'CORPUS-STATUS-112',\n                    'witness_id': 'CORPUS-WIT-112',\n                    'study_id': 'CORPUS-STUDY-020',\n                    'internal_study_id': 'STATE-ISRAEL-LETTER-STUDY-001',\n                    'study_path': 'studies/theologico-political/letter-to-editor-state-of-israel/sequential-reconstruction.yaml',\n                    'witness_record_path': 'studies/theologico-political/letter-to-editor-state-of-israel/reviewed-witness.yaml',\n                    'printed_page_range': {'start': 413, 'end': 414},\n                    'pdf_page_range_one_based': {'start': 432, 'end': 433},\n                    'reading_state': 'COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS',\n                    'platform_reference': False},\n"
    if "'CORPUS-SRC-112': {'status_id': 'CORPUS-STATUS-112',\n                    'witness_id': 'CORPUS-WIT-112',\n                    'study_id': 'CORPUS-STUDY-020'" not in t: t=repl(t,marker,block+marker,"complete contract")
    a,b=t.split("WITNESS_ONLY_TP_ITEMS",1); start=b.find(" 'CORPUS-SRC-112':")
    if start>=0:
        end=b.find(" 'CORPUS-SRC-114':",start)
        if end<0: raise RuntimeError("cannot bound witness-only SRC112")
        b=b[:start]+b[end:]
    t=a+"WITNESS_ONLY_TP_ITEMS"+b
    for a,b in [('identity.get("version") != "1.20.0"','identity.get("version") != "1.21.0"'),('identity.version must be 1.20.0','identity.version must be 1.21.0'),('"study records": (len(study_ids), 19)','"study records": (len(study_ids), 20)'),('"theologico_political_independent_item_studies_registered": 12','"theologico_political_independent_item_studies_registered": 13'),('!= "INCOMPLETE_12_OF_19"','!= "INCOMPLETE_13_OF_19"'),('must be INCOMPLETE_12_OF_19','must be INCOMPLETE_13_OF_19')]: t=t.replace(a,b)
    p.write_text(t)
    p=ROOT/"findings_registry.py"; t=p.read_text()
    for marker,extra in [('    "problems/ancients-vs-moderns/synthesis/talmon-nature-of-jewish-history.yaml",\n','    "problems/ancients-vs-moderns/synthesis/letter-to-editor-state-of-israel.yaml",\n'),('    "problems/theologico-political/synthesis/talmon-nature-of-jewish-history.yaml",\n','    "problems/theologico-political/synthesis/letter-to-editor-state-of-israel.yaml",\n')]:
        if extra.strip() not in t: t=repl(t,marker,extra+marker,"synthesis path")
    if '    "CORPUS-SRC-112",\n' not in t.split("SOURCE_STUDY_CONTRACTS",1)[0]: t=repl(t,'    "CORPUS-SRC-111",\n','    "CORPUS-SRC-111",\n    "CORPUS-SRC-112",\n',"direct key")
    t=t.replace('"CORPUS-SRC-111", "CORPUS-SRC-113"','"CORPUS-SRC-111", "CORPUS-SRC-112", "CORPUS-SRC-113"')
    if '    "FINDSET-020": {' not in t:
        marker="\n}\n\n\nclass FindingsRegistryError"; block='''\n    "FINDSET-020": {\n        "source_id": "CORPUS-SRC-112",\n        "local_syntheses": ["FINDSET-140", "FINDSET-141"],\n        "problem_bindings": {"FINDSET-140": "theologico-political", "FINDSET-141": "ancients-vs-moderns"},\n        "required_limits": {"witness_id": "CORPUS-WIT-112", "original_1957_national_review_comparison": "PENDING", "predecessor_retest_state": "PARTIAL_CONFIRMATION_WITH_MATERIAL_QUALIFICATION", "independent_corroboration": "INCOMPLETE"},\n    },'''; t=repl(t,marker,block+marker,"contract")
    for a,b in [('identity.get("version") != "1.12.0"','identity.get("version") != "1.13.0"'),('identity.version must be 1.12.0','identity.version must be 1.13.0'),('if len(finding_ids) != 63:','if len(finding_ids) != 66:'),('expected 63 finding sets','expected 66 finding sets')]: t=t.replace(a,b)
    p.write_text(t)

def tests():
    reps={
      "tests/test_corpus_registry.py":[('"1.20.0"','"1.21.0"'),('            59,','            60,'),('registry["coverage"]["study_records_registered"], 19','registry["coverage"]["study_records_registered"], 20'),('def test_seven_tp_sources_have_witnesses_but_still_require_study','def test_six_tp_sources_have_witnesses_but_still_require_study'),('self.assertEqual(len(sources), 7)','self.assertEqual(len(sources), 6)')],
      "tests/test_findings_registry.py":[('"1.12.0"','"1.13.0"'),('self.assertEqual(len(finding_ids), 63)','self.assertEqual(len(finding_ids), 66)'),('self.assertEqual(len(registered), 39)','self.assertEqual(len(registered), 41)'),('self.assertEqual(len(registered), 19)','self.assertEqual(len(registered), 20)')],
      "tests/test_interface_consistency.py":[('test_nineteen_identity_nineteen_witness_twelve_study_language_matches','test_nineteen_identity_nineteen_witness_thirteen_study_language_matches'),('manifest_state["independent_sequential_study_count"], 12','manifest_state["independent_sequential_study_count"], 13'),('audit_state["independently_reconstructed_count_within_this_sequence"], 12','audit_state["independently_reconstructed_count_within_this_sequence"], 13'),('mapping_state["independent_sequential_study_count"], 12','mapping_state["independent_sequential_study_count"], 13'),('manifest_state["remaining_without_independent_sequential_study"], 7','manifest_state["remaining_without_independent_sequential_study"], 6'),('mapping_state["remaining_without_independent_sequential_study"], 7','mapping_state["remaining_without_independent_sequential_study"], 6'),('"INCOMPLETE_12_OF_19"','"INCOMPLETE_13_OF_19"'),('"WHY-REMAIN-JEWS-STUDY-001"]','"WHY-REMAIN-JEWS-STUDY-001", "STATE-ISRAEL-LETTER-STUDY-001"]'),('schedule["termination"]["next_item_study"], "CORPUS-SRC-112"','schedule["termination"]["next_item_study"], "CORPUS-SRC-110"'),('            "FINDSET-019": [("FINDSET-138", "theologico-political"), ("FINDSET-139", "athens-vs-jerusalem")],\n','            "FINDSET-019": [("FINDSET-138", "theologico-political"), ("FINDSET-139", "athens-vs-jerusalem")],\n            "FINDSET-020": [("FINDSET-140", "theologico-political"), ("FINDSET-141", "ancients-vs-moderns")],\n')],
      "tests/test_tp_witness_coverage_complete.py":[('theologico_political_independent_item_studies_registered"], 12','theologico_political_independent_item_studies_registered"], 13'),('"INCOMPLETE_12_OF_19"','"INCOMPLETE_13_OF_19"'),('def test_seven_witness_only_items_remain_noncertified_and_unstudied','def test_six_witness_only_items_remain_noncertified_and_unstudied'),('"CORPUS-SRC-106", "CORPUS-SRC-107"}','"CORPUS-SRC-106", "CORPUS-SRC-107", "CORPUS-SRC-112"}'),('self.assertEqual(len(witness_only), 7)','self.assertEqual(len(witness_only), 6)')],
      "tests/test_corpus_wit_102_platform_registration.py":[('"INCOMPLETE_12_OF_19"','"INCOMPLETE_13_OF_19"')],
      "tests/test_src104_husik_completion.py":[('"INCOMPLETE_12_OF_19"','"INCOMPLETE_13_OF_19"'),('theologico_political_independent_item_studies_registered"], 12','theologico_political_independent_item_studies_registered"], 13'),('independent_sequential_study_count"], 12','independent_sequential_study_count"], 13'),('schedule["termination"]["next_item_study"], "CORPUS-SRC-112"','schedule["termination"]["next_item_study"], "CORPUS-SRC-110"')],
      "tests/test_src106_freud_moses_completion.py":[('"INCOMPLETE_12_OF_19"','"INCOMPLETE_13_OF_19"'),('theologico_political_independent_item_studies_registered"], 12','theologico_political_independent_item_studies_registered"], 13'),('independent_sequential_study_count"], 12','independent_sequential_study_count"], 13'),('schedule["termination"]["next_item_study"], "CORPUS-SRC-112"','schedule["termination"]["next_item_study"], "CORPUS-SRC-110"')],
      "tests/test_src107_why_we_remain_jews_completion.py":[('test_twelve_of_nineteen_completion_language_is_synchronized','test_forward_completion_language_remains_synchronized_after_src112'),('theologico_political_independent_item_studies_registered"], 12','theologico_political_independent_item_studies_registered"], 13'),('"INCOMPLETE_12_OF_19"','"INCOMPLETE_13_OF_19"'),('independent_sequential_study_count"], 12','independent_sequential_study_count"], 13'),('schedule["termination"]["next_item_study"], "CORPUS-SRC-112"','schedule["termination"]["next_item_study"], "CORPUS-SRC-110"')],
      "tests/test_pr21_talmon_completion.py":[('manifest["identity"]["version"], "1.16.0"','manifest["identity"]["version"], "1.17.0"'),('audit["identity"]["version"], "3.4.0"','audit["identity"]["version"], "3.5.0"'),('mapping["identity"]["version"], "1.16.0"','mapping["identity"]["version"], "1.17.0"'),('process["identity"]["version"], "1.18.0"','process["identity"]["version"], "1.19.0"'),('schedule["identity"]["version"], "1.16.0"','schedule["identity"]["version"], "1.17.0"'),('corpus["identity"]["version"], "1.20.0"','corpus["identity"]["version"], "1.21.0"'),('findings["identity"]["version"], "1.12.0"','findings["identity"]["version"], "1.13.0"'),('state["independent_sequential_study_count"], 12','state["independent_sequential_study_count"], 13'),('state["remaining_without_independent_sequential_study"], 7','state["remaining_without_independent_sequential_study"], 6'),('"WHY-REMAIN-JEWS-STUDY-001"],','"WHY-REMAIN-JEWS-STUDY-001", "STATE-ISRAEL-LETTER-STUDY-001"],'),('schedule["termination"]["next_item_study"], "CORPUS-SRC-112"','schedule["termination"]["next_item_study"], "CORPUS-SRC-110"')]
    }
    for rel,pairs in reps.items():
        p=ROOT/rel
        if not p.exists(): continue
        t=p.read_text()
        for a,b in pairs:
            if a in t: t=t.replace(a,b)
        p.write_text(t)

def main():
    for p in [STUDY,STATUS,TP_SYN,AVM_SYN]:
        if not (ROOT/p).is_file(): raise RuntimeError(f"missing {p}")
    corpus(); findings(); manifest(); audit(); mapping(); process(); schedule(); validators(); tests(); print("SRC112 integration materialized")
if __name__=="__main__": main()
