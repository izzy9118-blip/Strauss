#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

ROOT = Path(__file__).resolve().parents[1]
STUDY = "studies/theologico-political/why-we-remain-jews/sequential-reconstruction.yaml"
STATUS = "studies/theologico-political/why-we-remain-jews/source-status.yaml"
TP_SYN = "problems/theologico-political/synthesis/why-we-remain-jews.yaml"
AVJ_SYN = "problems/athens-vs-jerusalem/synthesis/why-we-remain-jews.yaml"
LIMIT = "NOT_REVIEWED_OR_FORMALLY_APPROVED_BY_STRAUSS_AS_REPORTED_BY_TRANSCRIBERS"
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
    if d["identity"]["version"]!="1.19.0": raise RuntimeError("corpus predecessor mismatch")
    d["identity"]["version"]="1.20.0"; d["revision_history"]["predecessor_version"]="1.19.0"; d["revision_history"]["predecessor_blob_sha"]="PRESERVED_BY_GIT"
    d["revision_history"]["reason"]="Register WHY-REMAIN-JEWS-STUDY-001 as the twelfth complete provisional Theologico-Political item study and CORPUS-STUDY-019 while preserving the tape-transcription, speaker-layer, editorial-intervention, noncorroboration, noncertification, predecessor-authority, and no-successor safeguards."
    s=one(d["source_entities"],"source_id","CORPUS-SRC-107")
    s["item_level_source_status"]="REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION"
    s["study_status"]="COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS_WITH_TRANSCRIPTION_AND_EDITORIAL_LIMIT"
    s["study_records"]=["CORPUS-STUDY-019"]
    s["limits"]=["reviewed witness is the fingerprinted 1997 SUNY posthumous tape-based transcription, not an authorially reviewed manuscript","printed pages 311-356 correspond to one-based PDF pages 330-375","Cropsey, questioners, Green notes and additions, and the editorial Aleinu translation remain distinct from Strauss evidence","Dannhauser and Lane report that Strauss neither reviewed nor formally approved the transcribed version","WHY-REMAIN-JEWS-STUDY-001 is source-local and not independent corroboration of represented traditions"]
    one(d["source_status_records"],"status_id","CORPUS-STATUS-107")["completion"]="REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION"
    if not any(r.get("study_id")=="CORPUS-STUDY-019" for r in d["study_records"]):
        d["study_records"].append(CommentedMap([("study_id","CORPUS-STUDY-019"),("source_id","CORPUS-SRC-107"),("path",STUDY),("record_role","SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION"),("completion","COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS_WITH_TRANSCRIPTION_AND_EDITORIAL_LIMIT"),("certification","NOT_CERTIFIED")]))
    c=d["coverage"]; c["study_records_registered"]=19; c["theologico_political_independent_item_studies_registered"]=12; c["current_studies_tree_yaml_records_accounted_for"]=59
    one(d["corpus_gaps"],"gap_id","CORPUS-GAP-003")["statement"]="All nineteen predecessor writings have bounded source identities and reviewed item witnesses; twelve have complete provisional sequential studies, while the remaining seven lack independent item studies."
    add(d["validation_rules"],"CORPUS-SRC-107 preserves the fingerprinted reviewed transcript, speaker and editorial-layer distinctions, complete provisional sequential reconstruction, noncorroboration, noncertification, and no-successor safeguards")
    d["validation_rules"]=[r.replace("all eight witness-only Theologico-Political sources","all seven witness-only Theologico-Political sources") if isinstance(r,str) else r for r in d["validation_rules"]]
    d["termination"]["theologico_political_independent_study_state"]="INCOMPLETE_12_OF_19"
    d["termination"]["next_required_units"]=["conduct independent sequential reconstruction of CORPUS-SRC-112 from CORPUS-WIT-112","compare any separately verified earlier or authorially checked textual state of CORPUS-SRC-107 if later acquired","conduct independent sequential reconstruction for the remaining seven writings","expand independent biblical, rabbinic, Zionist, Nietzschean, Cohenian, Scholemian, Christian, scientific, and historical witnesses"]
    save(p,d)

def findings():
    p="findings/index.yaml"; d=load(p)
    if d["identity"]["version"]!="1.11.0": raise RuntimeError("findings predecessor mismatch")
    d["identity"]["version"]="1.12.0"; d["revision_history"]["predecessor_version"]="1.11.0"; d["revision_history"]["predecessor_blob_sha"]="PRESERVED_BY_GIT"
    d["revision_history"]["reason"]="Register WHY-REMAIN-JEWS-STUDY-001 as FINDSET-019 and jurisdiction-preserving syntheses FINDSET-138 and FINDSET-139 while preserving transcription, speaker-layer, editorial-intervention, noncorroboration, noncertification, and no-successor safeguards."
    fs=d["finding_sets"]
    if not any(r.get("finding_set_id")=="FINDSET-019" for r in fs):
        i=next(i for i,r in enumerate(fs) if r.get("finding_set_id")=="FINDSET-101")
        fs.insert(i,CommentedMap([("finding_set_id","FINDSET-019"),("path",STUDY),("record_class","SOURCE_SPECIFIC_STUDY"),("record_role","SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION"),("source_bindings",["CORPUS-SRC-107"]),("problem_bindings",["theologico-political","athens-vs-jerusalem"]),("status","COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS_WITH_TRANSCRIPTION_AND_EDITORIAL_LIMIT"),("certification","NOT_CERTIFIED"),("derived_local_syntheses",["FINDSET-138","FINDSET-139"]),("witness_id","CORPUS-WIT-107"),("transcript_authorial_approval",LIMIT),("documentary_transmission_limit","ACTIVE"),("original_or_earlier_printing_comparison","PENDING"),("independent_corroboration","INCOMPLETE"),("successor_effect","NONE")]))
    if not any(r.get("finding_set_id")=="FINDSET-138" for r in fs):
        i=next(i for i,r in enumerate(fs) if r.get("finding_set_id")=="FINDSET-201")
        fs.insert(i,CommentedMap([("finding_set_id","FINDSET-138"),("path",TP_SYN),("record_class","PROBLEM_LOCAL_SYNTHESIS"),("record_role","SOURCE_TO_PROBLEM_SYNTHESIS"),("source_bindings",["CORPUS-SRC-107"]),("problem_bindings",["theologico-political"]),("adjacent_problem_references",["athens-vs-jerusalem"]),("derived_from",["FINDSET-019"]),("status","PROVISIONAL_NOT_CERTIFIED"),("certification","NOT_CERTIFIED"),("successor_effect","NONE")]))
        fs.insert(i+1,CommentedMap([("finding_set_id","FINDSET-139"),("path",AVJ_SYN),("record_class","PROBLEM_LOCAL_SYNTHESIS"),("record_role","SOURCE_TO_PROBLEM_SYNTHESIS"),("source_bindings",["CORPUS-SRC-107"]),("problem_bindings",["athens-vs-jerusalem"]),("theologico_political_reference","theologico-political"),("derived_from",["FINDSET-019"]),("status","PROVISIONAL_NOT_CERTIFIED"),("certification","NOT_CERTIFIED"),("successor_effect","NONE")]))
    keys=[r["canonical_key"] for r in load("problems/registry.yaml")["canonical_problems"]]; bp=CommentedMap((k,[]) for k in keys)
    direct=["CORPUS-SRC-001","CORPUS-SRC-002","CORPUS-SRC-003","CORPUS-SRC-101","CORPUS-SRC-102","CORPUS-SRC-103","CORPUS-SRC-104","CORPUS-SRC-105","CORPUS-SRC-106","CORPUS-SRC-107","CORPUS-SRC-108","CORPUS-SRC-111","CORPUS-SRC-113","CORPUS-SRC-116"]; bs=CommentedMap((k,[]) for k in direct); bs["CORPUS-SRC-101-119"]=[]
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
    c=d["coverage"]; c["finding_sets_registered"]=63; c["source_specific_and_integration_records_registered"]=19; c["problem_syntheses_registered"]=39; c["current_problem_synthesis_tree_yaml_records_accounted_for"]=39; c["corpus_study_records_accounted_for"]=19
    one(d["findings_gaps"],"gap_id","FINDINGS-GAP-003")["statement"]="Twelve of the nineteen Theologico-Political writings now have complete provisional item studies; the remaining seven lack individual sequential studies."
    add(d["validation_rules"],"FINDSET-019 must derive only FINDSET-138 and FINDSET-139, preserve CORPUS-WIT-107, the transcription and editorial-layer limits, pending earlier-textual-state comparison, noncorroboration, and no-successor safeguards")
    save(p,d)

def manifest():
    p="manifest.yaml"; d=load(p)
    if d["identity"]["version"]!="1.15.0": raise RuntimeError("manifest predecessor mismatch")
    d["identity"]["version"]="1.16.0"; d["revision_history"]["predecessor_version"]="1.15.0"; d["revision_history"]["predecessor_blob_sha"]="PRESERVED_BY_GIT"
    d["revision_history"]["reason"]="Register WHY-REMAIN-JEWS-STUDY-001 as the twelfth complete provisional Theologico-Political item study and synchronize corpus v1.20.0, findings v1.12.0, audit v3.4.0, mapping v1.16.0, process v1.18.0, and schedule v1.16.0 while preserving seven pending studies, transcription limits, noncertification, predecessor authority, and the Sanctum repin block."
    d["audit"]["version"]="3.4.0"; d["component_completion"]["theologico_political_item_level_source_statuses"]="19_OF_19_IDENTITIES_19_OF_19_REVIEWED_ITEM_WITNESSES_12_OF_19_COMPLETE_PROVISIONAL_ITEM_STUDIES"
    d["corpus"]["registry_version"]="1.20.0"; s=d["corpus"]["theologico_political_item_level_statuses"]; s["independent_sequential_study_count"]=12; s["remaining_without_independent_sequential_study"]=7; add(s["completed_study_ids"],"WHY-REMAIN-JEWS-STUDY-001")
    s["rule"]="All nineteen predecessor items have reviewed witnesses and twelve have complete provisional source studies. Witness and study completion remain distinct from independent corroboration, doctrinal certification, migration completion, successor activation, or repository completion."
    d["corpus"]["limitation"]="All nineteen predecessor writings have bounded identities and reviewed item witnesses. Twelve have complete provisional sequential studies; CORPUS-SRC-116 retains an omission limit, CORPUS-SRC-106 and CORPUS-SRC-107 retain posthumous-transcription/editorial limits, and seven sources still lack independent studies."
    d["findings"]["registry_version"]="1.12.0"; d["findings"]["newly_registered"]=["FINDSET-019","FINDSET-138","FINDSET-139"]
    save(p,d)

def audit():
    p="audits/operational-completeness.yaml"; d=load(p)
    if d["identity"]["version"]!="3.3.0": raise RuntimeError("audit predecessor mismatch")
    d["identity"]["version"]="3.4.0"; d["revision_history"]["predecessor_version"]="3.3.0"; d["revision_history"]["predecessor_blob_sha"]="PRESERVED_BY_GIT"; d["revision_history"]["reason"]="Complete WHY-REMAIN-JEWS-STUDY-001, advance study coverage to twelve of nineteen, preserve seven pending studies and the transcription/editorial limits."
    d["basis"]["current_revision_scope"]="production/corpus-src-107-sequential-reconstruction"
    for v in ["WHY-REMAIN-JEWS-STUDY-001 complete provisional sequential reconstruction with active transcription and editorial limits","CORPUS-STUDY-019 and FINDSET-019 typed registrations","FINDSET-138 and FINDSET-139 jurisdiction-preserving problem-local syntheses"]: add(d["summary"]["completed_operational_units"],v)
    s=d["summary"]["theologico_political_item_level_status"]; s["independently_reconstructed_count_within_this_sequence"]=12; s["remaining_without_independent_sequential_study"]=7; add(s["completed_source_ids"],"CORPUS-SRC-107"); add(s["completed_witness_ids"],"CORPUS-WIT-107"); add(s["completed_study_ids"],"WHY-REMAIN-JEWS-STUDY-001"); s["witness_only_source_ids"]=[x for x in s["witness_only_source_ids"] if x!="CORPUS-SRC-107"]; s["witness_only_witness_ids"]=[x for x in s["witness_only_witness_ids"] if x!="CORPUS-WIT-107"]
    s["interpretation_limit"]="All nineteen predecessor items have reviewed witnesses and twelve completed studies are independent reconstructions relative to predecessor and collection-level synthesis. Seven witness registrations remain study-pending; none is independent corroboration, and SRC107 retains active transcription, speaker-layer, and editorial limits."
    d["summary"]["remaining_major_deficiencies"][0]="seven Theologico-Political writings still require independent sequential item studies"
    add(d["production_order"]["completed_in_current_sequence"],"WHY-REMAIN-JEWS-STUDY-001 with FINDSET-019, FINDSET-138, and FINDSET-139")
    d["production_order"]["next"]=["run complete structural and behavioral validation for the twelfth Theologico-Political item study","conduct CORPUS-SRC-112 independent sequential reconstruction from its registered witness","continue the remaining six independent sequential reconstructions after CORPUS-SRC-112","expand independent source-tradition witnesses and textual-state comparisons","validate actual ministerial reports against the full contract stack"]
    save(p,d)

def mapping():
    p="migrations/lean-operational-interface.yaml"; d=load(p)
    if d["identity"]["version"]!="1.15.0": raise RuntimeError("mapping predecessor mismatch")
    d["identity"]["version"]="1.16.0"; d["revision_history"]["predecessor_version"]="1.15.0"; d["revision_history"]["predecessor_blob_sha"]="PRESERVED_BY_GIT"; d["revision_history"]["reason"]="Synchronize WHY-REMAIN-JEWS-STUDY-001, corpus v1.20.0, findings v1.12.0, audit v3.4.0, process v1.18.0, and schedule v1.16.0 while preserving seven pending studies and transcription/editorial limits."
    d["completion_audit"]["version"]="3.4.0"; d["production_process"]["completed_study_subunit"]="TWELVE_OF_19_COMPLETE_PROVISIONAL_SEVEN_PENDING"
    c=d["mappings"]["corpus"]; c["interface"]["registry_version"]="1.20.0"; s=c["theologico_political_item_level_statuses"]; s["independent_sequential_study_count"]=12; s["remaining_without_independent_sequential_study"]=7; add(s["completed_study_ids"],"WHY-REMAIN-JEWS-STUDY-001"); s["witness_only_source_ids"]=[x for x in s["witness_only_source_ids"] if x!="CORPUS-SRC-107"]
    c["limit"]="Current-state exhaustiveness, nineteen reviewed item witnesses, and twelve complete provisional item studies do not create a complete corpus, supply independent corroboration, resolve documentary limits, certify findings, or authorize migration and activation."
    for rel in [CommentedMap([("path",TP_SYN),("source","CORPUS-SRC-107"),("derivation","FINDSET-019_TO_FINDSET-138")]),CommentedMap([("path",AVJ_SYN),("source","CORPUS-SRC-107"),("derivation","FINDSET-019_TO_FINDSET-139")])]:
        if not any(x.get("path")==rel["path"] for x in d["mappings"]["problems"]["new_source_relations"]): d["mappings"]["problems"]["new_source_relations"].append(rel)
    for sec in ("hermeneutics","method"):
        apps=d["mappings"][sec].setdefault("source_applications",[])
        if not any(x.get("record")==STUDY for x in apps):
            e=CommentedMap([("record",STUDY),("state","COMPLETE_PROVISIONAL_FOR_ONE_REVIEWED_ITEM_WITH_DOCUMENTARY_LIMIT")]);
            if sec=="method": e["reading_units"]=12
            apps.append(e)
    f=d["mappings"]["findings"]; f["interface"]["registry_version"]="1.12.0"; f["newly_registered"]=[CommentedMap([("finding_set_id","FINDSET-019"),("path",STUDY)]),CommentedMap([("finding_set_id","FINDSET-138"),("path",TP_SYN),("derived_from","FINDSET-019")]),CommentedMap([("finding_set_id","FINDSET-139"),("path",AVJ_SYN),("derived_from","FINDSET-019")])]
    d["completed_production_units"]=["speech, hermeneutic, and method operational contracts","complete read-only foundational problem bundles","typed current-state corpus and findings registries","complete 19-of-19 Theologico-Political source-identity and reviewed-witness range","twelve complete provisional Theologico-Political sequential reconstructions through WHY-REMAIN-JEWS-STUDY-001","jurisdiction-preserving source-to-problem syntheses through FINDSET-139"]
    d["next_production_units"]=["validate and merge the bounded CORPUS-SRC-107 production unit","conduct CORPUS-SRC-112 independent sequential reconstruction","continue the remaining six item studies after CORPUS-SRC-112","expand independent witness reconstruction and textual-state comparison","validate actual candidate ministerial reports"]
    save(p,d)

def process():
    p="history/production-plans/2026-07-27-ten-step-completion-process.yaml"; d=load(p)
    if d["identity"]["version"]!="1.17.0": raise RuntimeError("process predecessor mismatch")
    d["identity"]["version"]="1.18.0"; d["revision_history"]["predecessor_version"]="1.17.0"; d["revision_history"]["predecessor_blob_sha"]="PRESERVED_BY_GIT"; d["revision_history"]["reason"]="Complete WHY-REMAIN-JEWS-STUDY-001 as the twelfth provisional Theologico-Political sequential reconstruction and advance the next study unit to CORPUS-SRC-112 while preserving transcription/editorial limits and seven remaining studies."
    st={x["sequence"]:x for x in d["steps"]}; st[1]["current_version"]="3.4.0"; st[2]["current_version"]="1.16.0"; add(st[7]["completed"],"Why We Remain Jews supplies distinct provisional syntheses to Theologico-Political and Athens-versus-Jerusalem with explicit speaker/transcription/editorial limits"); add(st[8]["completed"],"WHY-REMAIN-JEWS-STUDY-001 is complete provisional for CORPUS-WIT-107 with active transcription and editorial limits"); st[8]["remaining"][0]="conduct seven independent sequential item studies, beginning with CORPUS-SRC-112"; st[9]["completed_in_current_sequence"][0]="tests cover all nineteen Theologico-Political reviewed-witness registrations and distinguish the seven witness-only states from the twelve completed-study states"
    d["current_production_unit"]=CommentedMap([("step",8),("completed_subunit",CommentedMap([("title","Why We Remain Jews independent sequential reconstruction"),("state","COMPLETE_PROVISIONAL_PENDING_BRANCH_VALIDATION_AND_MERGE"),("source_id","CORPUS-SRC-107"),("witness_id","CORPUS-WIT-107"),("study_id","WHY-REMAIN-JEWS-STUDY-001"),("study_coverage","INCOMPLETE_12_OF_19"),("documentary_limit","POSTHUMOUS_TAPE_TRANSCRIPTION_SPEAKER_AND_EDITORIAL_LAYERS") ])),("next_subunit",CommentedMap([("title","Letter to the Editor — The State of Israel independent sequential reconstruction"),("source_id","CORPUS-SRC-112"),("witness_id","CORPUS-WIT-112"),("following_source","CORPUS-SRC-110")]))])
    save(p,d)

def schedule():
    p="history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml"; d=load(p)
    if d["identity"]["version"]!="1.15.0": raise RuntimeError("schedule predecessor mismatch")
    d["identity"]["version"]="1.16.0"; d["status"]["independent_sequential_study_completion"]="INCOMPLETE_12_OF_19"; d["revision_history"]["predecessor_version"]="1.15.0"; d["revision_history"]["predecessor_blob_sha"]="PRESERVED_BY_GIT"; d["revision_history"]["reason"]="Complete WHY-REMAIN-JEWS-STUDY-001 from CORPUS-WIT-107, advancing independent sequential study coverage to 12-of-19 and the next study unit to CORPUS-SRC-112 while preserving complete witness coverage and transcription/editorial limits."
    src=None
    for g in d["priority_groups"]:
        for r in g.get("items",[]):
            if r.get("source_id")=="CORPUS-SRC-107": src=r
    if src is None: raise RuntimeError("SRC107 schedule item missing")
    src["state"]="REVIEWED_WITNESS_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDY_WITH_TRANSCRIPTION_AND_EDITORIAL_LIMIT"; src["study_id"]="WHY-REMAIN-JEWS-STUDY-001"; src["next_action"]="EARLIER_TEXTUAL_STATE_COMPARISON_IF_AVAILABLE_AND_INDEPENDENT_SOURCE_TRADITION_EXPANSION"
    add(d["selection"]["completed_study_ids"],"WHY-REMAIN-JEWS-STUDY-001"); d["selection"]["selection_state"]="NINETEEN_REVIEWED_ITEM_WITNESSES_TWELVE_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDIES"; d["selection"]["completed_units"]=["all nineteen predecessor source identities have reviewed witnesses","twelve source studies are complete provisional","seven witness-only sources remain pending independent sequential reconstruction","all textual-state, transcription, speaker-layer, editorial, and independent-corroboration limits remain explicit"]
    d["termination"]["independent_sequential_reconstruction"]="INCOMPLETE_12_OF_19"; d["termination"]["next_item_study"]="CORPUS-SRC-112"; d["next_item_study_unit"]=CommentedMap([("source_id","CORPUS-SRC-112"),("title","Letter to the Editor — The State of Israel"),("action","INDEPENDENT_SEQUENTIAL_RECONSTRUCTION_FROM_REGISTERED_WITNESS"),("prerequisite","SATISFIED_CORPUS_WIT_112_REGISTERED"),("following_source","CORPUS-SRC-110")])
    save(p,d)

def validators():
    p=ROOT/"corpus_registry.py"; t=p.read_text()
    marker=" 'CORPUS-SRC-108': {'status_id': 'CORPUS-STATUS-108',"
    block=" 'CORPUS-SRC-107': {'status_id': 'CORPUS-STATUS-107',\n                    'witness_id': 'CORPUS-WIT-107',\n                    'study_id': 'CORPUS-STUDY-019',\n                    'internal_study_id': 'WHY-REMAIN-JEWS-STUDY-001',\n                    'study_path': 'studies/theologico-political/why-we-remain-jews/sequential-reconstruction.yaml',\n                    'witness_record_path': 'studies/theologico-political/why-we-remain-jews/reviewed-witness.yaml',\n                    'printed_page_range': {'start': 311, 'end': 356},\n                    'pdf_page_range_one_based': {'start': 330, 'end': 375},\n                    'reading_state': 'COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS',\n                    'platform_reference': False},\n"
    if "'CORPUS-SRC-107': {'status_id': 'CORPUS-STATUS-107',\n                    'witness_id': 'CORPUS-WIT-107',\n                    'study_id': 'CORPUS-STUDY-019'" not in t: t=repl(t,marker,block+marker,"complete contract")
    a,b=t.split("WITNESS_ONLY_TP_ITEMS",1); start=b.find("{'CORPUS-SRC-107':")
    if start>=0:
        end=b.find(" 'CORPUS-SRC-110':",start)
        if end<0: raise RuntimeError("cannot bound witness-only SRC107")
        b=b[:start]+"{"+b[end+1:]
    t=a+"WITNESS_ONLY_TP_ITEMS"+b
    for a,b in [('identity.get("version") != "1.19.0"','identity.get("version") != "1.20.0"'),('identity.version must be 1.19.0','identity.version must be 1.20.0'),('"study records": (len(study_ids), 18)','"study records": (len(study_ids), 19)'),('"theologico_political_independent_item_studies_registered": 11','"theologico_political_independent_item_studies_registered": 12'),('!= "INCOMPLETE_11_OF_19"','!= "INCOMPLETE_12_OF_19"'),('must be INCOMPLETE_11_OF_19','must be INCOMPLETE_12_OF_19')]: t=t.replace(a,b)
    p.write_text(t)
    p=ROOT/"findings_registry.py"; t=p.read_text()
    for marker,extra in [('    "problems/athens-vs-jerusalem/synthesis/talmon-nature-of-jewish-history.yaml",\n','    "problems/athens-vs-jerusalem/synthesis/why-we-remain-jews.yaml",\n'),('    "problems/theologico-political/synthesis/talmon-nature-of-jewish-history.yaml",\n','    "problems/theologico-political/synthesis/why-we-remain-jews.yaml",\n')]:
        if extra.strip() not in t: t=repl(t,marker,marker+extra,"synthesis path")
    if '    "CORPUS-SRC-107",\n' not in t.split("SOURCE_STUDY_CONTRACTS",1)[0]: t=repl(t,'    "CORPUS-SRC-106",\n','    "CORPUS-SRC-106",\n    "CORPUS-SRC-107",\n',"direct key")
    t=t.replace('"CORPUS-SRC-106", "CORPUS-SRC-108"','"CORPUS-SRC-106", "CORPUS-SRC-107", "CORPUS-SRC-108"')
    if '    "FINDSET-019": {' not in t:
        marker="\n}\n\n\nclass FindingsRegistryError"; block='''\n    "FINDSET-019": {\n        "source_id": "CORPUS-SRC-107",\n        "local_syntheses": ["FINDSET-138", "FINDSET-139"],\n        "problem_bindings": {"FINDSET-138": "theologico-political", "FINDSET-139": "athens-vs-jerusalem"},\n        "required_limits": {"witness_id": "CORPUS-WIT-107", "transcript_authorial_approval": "NOT_REVIEWED_OR_FORMALLY_APPROVED_BY_STRAUSS_AS_REPORTED_BY_TRANSCRIBERS", "documentary_transmission_limit": "ACTIVE", "original_or_earlier_printing_comparison": "PENDING", "independent_corroboration": "INCOMPLETE"},\n    },'''; t=repl(t,marker,block+marker,"contract")
    for a,b in [('identity.get("version") != "1.11.0"','identity.get("version") != "1.12.0"'),('identity.version must be 1.11.0','identity.version must be 1.12.0'),('if len(finding_ids) != 60:','if len(finding_ids) != 63:'),('expected 60 finding sets','expected 63 finding sets')]: t=t.replace(a,b)
    p.write_text(t)

def tests():
    reps={
      "tests/test_corpus_registry.py":[('"1.19.0"','"1.20.0"'),('            58,','            59,'),('registry["coverage"]["study_records_registered"], 18','registry["coverage"]["study_records_registered"], 19'),('def test_eight_tp_sources_have_witnesses_but_still_require_study','def test_seven_tp_sources_have_witnesses_but_still_require_study'),('self.assertEqual(len(sources), 8)','self.assertEqual(len(sources), 7)')],
      "tests/test_findings_registry.py":[('"1.11.0"','"1.12.0"'),('self.assertEqual(len(finding_ids), 60)','self.assertEqual(len(finding_ids), 63)'),('self.assertEqual(len(registered), 37)','self.assertEqual(len(registered), 39)'),('self.assertEqual(len(registered), 18)','self.assertEqual(len(registered), 19)')],
      "tests/test_interface_consistency.py":[('test_nineteen_identity_nineteen_witness_eleven_study_language_matches','test_nineteen_identity_nineteen_witness_twelve_study_language_matches'),('manifest_state["independent_sequential_study_count"], 11','manifest_state["independent_sequential_study_count"], 12'),('audit_state["independently_reconstructed_count_within_this_sequence"], 11','audit_state["independently_reconstructed_count_within_this_sequence"], 12'),('mapping_state["independent_sequential_study_count"], 11','mapping_state["independent_sequential_study_count"], 12'),('manifest_state["remaining_without_independent_sequential_study"], 8','manifest_state["remaining_without_independent_sequential_study"], 7'),('mapping_state["remaining_without_independent_sequential_study"], 8','mapping_state["remaining_without_independent_sequential_study"], 7'),('"INCOMPLETE_11_OF_19"','"INCOMPLETE_12_OF_19"'),('"FREUD-MOSES-STUDY-001"]','"FREUD-MOSES-STUDY-001", "WHY-REMAIN-JEWS-STUDY-001"]'),('schedule["termination"]["next_item_study"], "CORPUS-SRC-107"','schedule["termination"]["next_item_study"], "CORPUS-SRC-112"'),('            "FINDSET-018": [("FINDSET-136", "theologico-political"), ("FINDSET-137", "ancients-vs-moderns")],\n','            "FINDSET-018": [("FINDSET-136", "theologico-political"), ("FINDSET-137", "ancients-vs-moderns")],\n            "FINDSET-019": [("FINDSET-138", "theologico-political"), ("FINDSET-139", "athens-vs-jerusalem")],\n')],
      "tests/test_tp_witness_coverage_complete.py":[('theologico_political_independent_item_studies_registered"], 11','theologico_political_independent_item_studies_registered"], 12'),('"INCOMPLETE_11_OF_19"','"INCOMPLETE_12_OF_19"'),('def test_eight_witness_only_items_remain_noncertified_and_unstudied','def test_seven_witness_only_items_remain_noncertified_and_unstudied'),('"CORPUS-SRC-104", "CORPUS-SRC-106"}','"CORPUS-SRC-104", "CORPUS-SRC-106", "CORPUS-SRC-107"}'),('self.assertEqual(len(witness_only), 8)','self.assertEqual(len(witness_only), 7)')],
      "tests/test_corpus_wit_102_platform_registration.py":[('"INCOMPLETE_11_OF_19"','"INCOMPLETE_12_OF_19"')],
      "tests/test_src104_husik_completion.py":[('"INCOMPLETE_11_OF_19"','"INCOMPLETE_12_OF_19"'),('theologico_political_independent_item_studies_registered"], 11','theologico_political_independent_item_studies_registered"], 12'),('independent_sequential_study_count"], 11','independent_sequential_study_count"], 12'),('schedule["termination"]["next_item_study"], "CORPUS-SRC-107"','schedule["termination"]["next_item_study"], "CORPUS-SRC-112"')],
      "tests/test_src106_freud_moses_completion.py":[('test_eleven_of_nineteen_completion_language_is_synchronized','test_forward_completion_language_remains_synchronized_after_src107'),('theologico_political_independent_item_studies_registered"], 11','theologico_political_independent_item_studies_registered"], 12'),('"INCOMPLETE_11_OF_19"','"INCOMPLETE_12_OF_19"'),('independent_sequential_study_count"], 11','independent_sequential_study_count"], 12'),('schedule["termination"]["next_item_study"], "CORPUS-SRC-107"','schedule["termination"]["next_item_study"], "CORPUS-SRC-112"')],
      "tests/test_pr21_talmon_completion.py":[('manifest["identity"]["version"], "1.15.0"','manifest["identity"]["version"], "1.16.0"'),('audit["identity"]["version"], "3.3.0"','audit["identity"]["version"], "3.4.0"'),('mapping["identity"]["version"], "1.15.0"','mapping["identity"]["version"], "1.16.0"'),('process["identity"]["version"], "1.17.0"','process["identity"]["version"], "1.18.0"'),('schedule["identity"]["version"], "1.15.0"','schedule["identity"]["version"], "1.16.0"'),('corpus["identity"]["version"], "1.19.0"','corpus["identity"]["version"], "1.20.0"'),('findings["identity"]["version"], "1.11.0"','findings["identity"]["version"], "1.12.0"'),('state["independent_sequential_study_count"], 11','state["independent_sequential_study_count"], 12'),('state["remaining_without_independent_sequential_study"], 8','state["remaining_without_independent_sequential_study"], 7'),('"FREUD-MOSES-STUDY-001"],','"FREUD-MOSES-STUDY-001", "WHY-REMAIN-JEWS-STUDY-001"],'),('schedule["termination"]["next_item_study"], "CORPUS-SRC-107"','schedule["termination"]["next_item_study"], "CORPUS-SRC-112"')]
    }
    for rel,pairs in reps.items():
        p=ROOT/rel; t=p.read_text()
        for a,b in pairs:
            if a in t: t=t.replace(a,b)
        p.write_text(t)

def main():
    for p in [STUDY,STATUS,TP_SYN,AVJ_SYN]:
        if not (ROOT/p).is_file(): raise RuntimeError(f"missing {p}")
    corpus(); findings(); manifest(); audit(); mapping(); process(); schedule(); validators(); tests(); print("SRC107 integration materialized")
if __name__=="__main__": main()
