#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

ROOT=Path(__file__).resolve().parents[1]
y=YAML(); y.preserve_quotes=True; y.width=120

def load(p):
    with (ROOT/p).open(encoding='utf-8') as f: return y.load(f)
def save(p,d):
    with (ROOT/p).open('w',encoding='utf-8') as f: y.dump(d,f)
def one(rs,k,v): return next(r for r in rs if r.get(k)==v)
def add(seq,v):
    if v not in seq: seq.append(v)
def replace_once(t,a,b,label):
    n=t.count(a)
    if n!=1: raise RuntimeError(f'{label}: expected one occurrence of {a!r}, got {n}')
    return t.replace(a,b,1)

SOURCES={
'CORPUS-SRC-114': dict(status='CORPUS-STATUS-114', witness='CORPUS-WIT-114', study='CORPUS-STUDY-022', internal='GOOD-SOCIETY-STUDY-001', dir='perspectives-on-the-good-society', title='Perspectives on the Good Society', pages=(431,445), pdf=(450,464), reading='COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS', problems=['theologico-political','theory-vs-practice','ancients-vs-moderns'], comparison='original_1963_criterion_comparison', comparison_label='1963 Criterion printing', findset='FINDSET-022', synth=[('FINDSET-144','theologico-political','perspectives-on-the-good-society.yaml'),('FINDSET-145','theory-vs-practice','perspectives-on-the-good-society.yaml'),('FINDSET-146','ancients-vs-moderns','perspectives-on-the-good-society.yaml')], retest='STRONG_CONFIRMATION_WITH_QUALIFICATION'),
'CORPUS-SRC-115': dict(status='CORPUS-STATUS-115', witness='CORPUS-WIT-115', study='CORPUS-STUDY-023', internal='UNSPOKEN-PROLOGUE-STUDY-001', dir='an-unspoken-prologue', title='An Unspoken Prologue', pages=(449,452), pdf=(468,471), reading='COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS', problems=['theologico-political','ancients-vs-moderns'], comparison='original_1978_interpretation_comparison', comparison_label='1978 Interpretation printing', findset='FINDSET-023', synth=[('FINDSET-147','theologico-political','an-unspoken-prologue.yaml'),('FINDSET-148','ancients-vs-moderns','an-unspoken-prologue.yaml')], retest='MATERIAL_NONCONFIRMATION_AND_PROBABLE_SOURCE_MISALLOCATION'),
'CORPUS-SRC-117': dict(status='CORPUS-STATUS-117', witness='CORPUS-WIT-117', study='CORPUS-STUDY-024', internal='GIVING-ACCOUNTS-STUDY-001', dir='a-giving-of-accounts', title='A Giving of Accounts', pages=(457,466), pdf=(476,485), reading='COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS', problems=['theologico-political','wise-vs-vulgar','ancients-vs-moderns'], comparison='original_1970_college_comparison', comparison_label='1970 The College printing', findset='FINDSET-024', synth=[('FINDSET-149','theologico-political','a-giving-of-accounts.yaml'),('FINDSET-150','wise-vs-vulgar','a-giving-of-accounts.yaml'),('FINDSET-151','ancients-vs-moderns','a-giving-of-accounts.yaml')], retest='STRONG_CONFIRMATION_AND_SUBSTANTIVE_DEEPENING'),
'CORPUS-SRC-118': dict(status='CORPUS-STATUS-118', witness='CORPUS-WIT-118', study='CORPUS-STUDY-025', internal='PHILOSOPHY-LAW-PLAN-STUDY-001', dir='plan-philosophy-and-the-law-historical-essays', title='Plan of a Book Tentatively Entitled Philosophy and the Law — Historical Essays', pages=(467,470), pdf=(486,489), reading='COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS', problems=['theologico-political','athens-vs-jerusalem','wise-vs-vulgar'], comparison='earlier_textual_state_comparison', comparison_label='earlier textual state', findset='FINDSET-025', synth=[('FINDSET-152','theologico-political','plan-philosophy-and-the-law-historical-essays.yaml'),('FINDSET-153','athens-vs-jerusalem','plan-philosophy-and-the-law-historical-essays.yaml'),('FINDSET-154','wise-vs-vulgar','plan-philosophy-and-the-law-historical-essays.yaml')], retest='STRONG_CONFIRMATION_WITH_DOCUMENTARY_LIMIT'),
'CORPUS-SRC-119': dict(status='CORPUS-STATUS-119', witness='CORPUS-WIT-119', study='CORPUS-STUDY-026', internal='HIERO-RESTATEMENT-LAST-PARAGRAPH-STUDY-001', dir='restatement-on-xenophons-hiero', title="Restatement on Xenophon's Hiero", pages=(471,473), pdf=(490,492), reading='COMPLETE_FOR_REGISTERED_LAST_PARAGRAPH_OF_REVIEWED_1997_COLLECTED_WITNESS', problems=['theologico-political','ancients-vs-moderns','theory-vs-practice'], comparison='earlier_textual_state_comparison', comparison_label='earlier textual state', findset='FINDSET-026', synth=[('FINDSET-155','theologico-political','restatement-on-xenophons-hiero-last-paragraph.yaml'),('FINDSET-156','ancients-vs-moderns','restatement-on-xenophons-hiero-last-paragraph.yaml'),('FINDSET-157','theory-vs-practice','restatement-on-xenophons-hiero-last-paragraph.yaml')], retest='STRONG_CONFIRMATION_WITH_REGISTERED_SCOPE_QUALIFICATION', scope='LAST_PARAGRAPH_ONLY'),
}

PROBLEM_KEY={'theologico-political':'theologico_political','theory-vs-practice':'theory_vs_practice','ancients-vs-moderns':'ancients_vs_moderns','athens-vs-jerusalem':'athens_vs_jerusalem','wise-vs-vulgar':'wise_vs_vulgar'}

def study_path(s): return f"studies/theologico-political/{s['dir']}/sequential-reconstruction.yaml"
def status_path(s): return f"studies/theologico-political/{s['dir']}/source-status.yaml"
def witness_path(s): return f"studies/theologico-political/{s['dir']}/reviewed-witness.yaml"

def update_statuses():
    for sid,s in SOURCES.items():
        p=status_path(s); d=load(p); st=load(study_path(s))
        d['identity']['version']='1.2.0'
        d['status']['lifecycle']='REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION'
        d['status']['independent_sequential_study']=s['internal']
        d['revision_history']={'predecessor_version':'1.1.0','transformation':'FORWARD_SEQUENTIAL_RECONSTRUCTION','reason':f"Complete {s['internal']} from the fingerprinted 1997 collected witness while preserving witness/study distinction, textual-state limits, predecessor authority, noncorroboration, noncertification, and no successor effect."}
        cmp=st.get('comparison_with_active_predecessor',{})
        d['predecessor_contribution_record']['evidence_status']='PROVISIONALLY_RETESTED_'+s['retest']
        d['predecessor_contribution_record']['retest_state']=cmp.get('state')
        d['predecessor_contribution_record']['retest_result']='; '.join(cmp.get('confirmations',[])+cmp.get('qualifications',[]))
        d['predecessor_contribution_record']['preservation_rule']='Retest does not silently rewrite, certify, activate, or displace the active predecessor.'
        d['source_classification']['analytical_use']='COMPLETE_PROVISIONAL_SOURCE_SPECIFIC_RECONSTRUCTION_FOR_REVIEWED_WITNESS'
        d['source_classification']['independence_limit']='The completed study is source-local and is not independent corroboration of represented persons, traditions, institutions, or doctrines.'
        d['study_record']={'internal_study_id':s['internal'],'corpus_study_id':s['study'],'path':study_path(s),'reading_state':s['reading'],'independent_corroboration':'INCOMPLETE'}
        d['next_required_actions']=[f"compare the reviewed witness with the {s['comparison_label']} when separately available",'expand independent primary witnesses where warranted','preserve source-specific findings without doctrinal promotion']
        term=d['termination']; term['study_state']='COMPLETE_PROVISIONAL'; term['study_id']=s['internal']; term['independent_corroboration']='INCOMPLETE'; term[s['comparison']]='PENDING'; term['certification']='NOT_CERTIFIED'; term['successor_effect']='NONE'
        if 'scope' in s:
            term['registered_scope']=s['scope']; term['study_scope_state']='COMPLETE_PROVISIONAL_FOR_REGISTERED_SCOPE'
        save(p,d)

def write_syntheses():
    for sid,s in SOURCES.items():
        st=load(study_path(s)); pfs=st.get('permanent_findings',[]); cmp=st.get('comparison_with_active_predecessor',{})
        for fid,problem,filename in s['synth']:
            section=st.get('problem_jurisdiction',{}).get(PROBLEM_KEY[problem],{})
            out=CommentedMap()
            out['schema_version']=1.0; out['record_type']='problem_local_synthesis'
            out['identity']={'id':fid+'-SYNTHESIS','title':f"{s['title']} — {problem} local synthesis",'version':'1.0.0'}
            out['status']={'lifecycle':'PROVISIONAL_SOURCE_DERIVED_SYNTHESIS','certification':'NOT_CERTIFIED','successor_effect':'NONE','predecessor_effect':'NONE'}
            out['derivation']={'source_finding_set':s['findset'],'source_id':sid,'study_id':s['internal'],'witness_id':s['witness'],'rule':'Derived only from the completed source-specific reconstruction; repetition does not create independent corroboration.'}
            out['problem']={'canonical_key':problem,'role':section.get('role'),'receives':section.get('receives',[]),'non_absorption':section.get('non_absorption')}
            out['source_findings']=[{'id':x.get('id'),'classification':x.get('classification'),'proposition':x.get('proposition')} for x in pfs]
            out['predecessor_retest']={'state':cmp.get('state'),'predecessor_effect':'NONE'}
            out['limits']=['source-specific derivation only','independent corroboration remains incomplete',f"{s['comparison_label']} comparison remains pending",'no doctrinal certification, migration certification, successor activation, or predecessor displacement']
            path=f'problems/{problem}/synthesis/{filename}'; (ROOT/path).parent.mkdir(parents=True,exist_ok=True); save(path,out)

def update_corpus():
    p='corpus/index.yaml'; d=load(p)
    if d['identity']['version']!='1.22.0': raise RuntimeError('unexpected corpus predecessor')
    d['identity']['version']='1.23.0'; d['revision_history']['predecessor_version']='1.22.0'; d['revision_history']['predecessor_blob_sha']='PRESERVED_BY_GIT'; d['revision_history']['reason']='Complete the final five Theologico-Political independent sequential reconstructions, reaching 19-of-19 within registered scopes while preserving source corrections, textual-state limits, noncorroboration, noncertification, predecessor authority, and no successor effect.'
    for sid,s in SOURCES.items():
        e=one(d['source_entities'],'source_id',sid); e['problem_bindings']=s['problems']; e['item_level_source_status']='REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION'; e['study_status']='COMPLETE_PROVISIONAL_FOR_REGISTERED_SCOPE' if 'scope' in s else 'COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS'; e['study_records']=[s['study']]
        limits=[f"{s['internal']} is source-local and not independent corroboration",f"{s['comparison_label']} comparison remains PENDING"]
        if sid=='CORPUS-SRC-115': limits.append('predecessor-attributed orthodoxy, unbelief, Zionism, and medieval-philosophy material is absent from this prologue; probable source conflation is preserved rather than silently harmonized')
        if sid=='CORPUS-SRC-117': limits.append('speaker layers, autobiography limit, and tape break remain explicit')
        if sid=='CORPUS-SRC-118': limits.append("Green's mature-view judgment is editorial and projected architecture is not completed argument")
        if sid=='CORPUS-SRC-119': limits.append('LAST_PARAGRAPH_ONLY scope remains governing; Green theological interpretation and predecessor universal-state wording are not imported')
        e['limits']=limits
        one(d['source_status_records'],'status_id',s['status'])['completion']='REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION'
        if not any(r.get('study_id')==s['study'] for r in d['study_records']): d['study_records'].append(CommentedMap([('study_id',s['study']),('source_id',sid),('path',study_path(s)),('record_role','SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION'),('completion','COMPLETE_PROVISIONAL_FOR_REGISTERED_SCOPE' if 'scope' in s else 'COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS'),('certification','NOT_CERTIFIED')]))
    c=d['coverage']; c['study_records_registered']=26; c['theologico_political_independent_item_studies_registered']=19; c['current_studies_tree_yaml_records_accounted_for']=66
    gap=one(d['corpus_gaps'],'gap_id','CORPUS-GAP-003'); gap['statement']='All nineteen predecessor writings have bounded source identities, reviewed item witnesses, and complete provisional independent sequential reconstructions within their registered scopes. Original or earlier textual-state comparisons, independent corroboration, broader corpus work, and certification remain incomplete.'; gap['effect']='SEQUENCE_RECONSTRUCTED_BUT_COMPARATIVE_SYNTHESIS_AND_CERTIFICATION_REMAIN_PROVISIONAL'
    d['validation_rules']=[r for r in d['validation_rules'] if not (isinstance(r,str) and 'witness-only Theologico-Political sources' in r)]
    add(d['validation_rules'],'all nineteen Theologico-Political predecessor sources preserve distinct source, witness, study, edition-comparison, noncorroboration, noncertification, and no-successor states after complete provisional registered-scope reconstruction')
    add(d['validation_rules'],'CORPUS-SRC-115 preserves material nonconfirmation of predecessor-attributed orthodoxy, unbelief, Zionism, and medieval-philosophy content rather than silently harmonizing source conflation')
    add(d['validation_rules'],'CORPUS-SRC-119 preserves LAST_PARAGRAPH_ONLY scope and excludes Green editorial theological interpretation from Strauss evidence')
    term=d['termination']; term['theologico_political_independent_study_state']='COMPLETE_19_OF_19'; term['next_required_units']=['compare original or earlier textual states where available and material','expand independent biblical, Greek, medieval, modern, and reviewed-work witnesses','continue broader corpus and proposition-level work without treating 19-of-19 sequence reconstruction as repository completion','preserve predecessor authority until separately authorized certified transition']
    save(p,d)

def update_findings():
    p='findings/index.yaml'; d=load(p)
    if d['identity']['version']!='1.14.0': raise RuntimeError('unexpected findings predecessor')
    d['identity']['version']='1.15.0'; d['revision_history']['predecessor_version']='1.14.0'; d['revision_history']['predecessor_blob_sha']='PRESERVED_BY_GIT'; d['revision_history']['reason']='Register FINDSET-022 through FINDSET-026 and fourteen jurisdiction-preserving local syntheses for the final five Theologico-Political source studies, completing 19-of-19 registered-scope studies while preserving noncorroboration and noncertification.'
    fs=d['finding_sets']; source_insert=next(i for i,r in enumerate(fs) if r.get('finding_set_id')=='FINDSET-101')
    for sid,s in SOURCES.items():
        if not any(r.get('finding_set_id')==s['findset'] for r in fs):
            rec=CommentedMap([('finding_set_id',s['findset']),('path',study_path(s)),('record_class','SOURCE_SPECIFIC_STUDY'),('record_role','SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION'),('source_bindings',[sid]),('problem_bindings',s['problems']),('status','COMPLETE_PROVISIONAL_FOR_REGISTERED_SCOPE' if 'scope' in s else 'COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS'),('certification','NOT_CERTIFIED'),('derived_local_syntheses',[x[0] for x in s['synth']]),('witness_id',s['witness']),(s['comparison'],'PENDING'),('predecessor_retest_state',s['retest']),('independent_corroboration','INCOMPLETE'),('successor_effect','NONE')])
            if 'scope' in s: rec['registered_scope']=s['scope']
            fs.insert(source_insert,rec); source_insert+=1
    synth_insert=next(i for i,r in enumerate(fs) if r.get('finding_set_id')=='FINDSET-201')
    for sid,s in SOURCES.items():
        for fid,problem,filename in s['synth']:
            if any(r.get('finding_set_id')==fid for r in fs): continue
            rec=CommentedMap([('finding_set_id',fid),('path',f'problems/{problem}/synthesis/{filename}'),('record_class','PROBLEM_LOCAL_SYNTHESIS'),('record_role','SOURCE_TO_PROBLEM_SYNTHESIS'),('source_bindings',[sid]),('problem_bindings',[problem]),('derived_from',[s['findset']]),('status','PROVISIONAL_NOT_CERTIFIED'),('certification','NOT_CERTIFIED'),('successor_effect','NONE')])
            fs.insert(synth_insert,rec); synth_insert+=1
    keys=[r['canonical_key'] for r in load('problems/registry.yaml')['canonical_problems']]; bp=CommentedMap((k,[]) for k in keys)
    direct=['CORPUS-SRC-001','CORPUS-SRC-002','CORPUS-SRC-003','CORPUS-SRC-101','CORPUS-SRC-102','CORPUS-SRC-103','CORPUS-SRC-104','CORPUS-SRC-105','CORPUS-SRC-106','CORPUS-SRC-107','CORPUS-SRC-108','CORPUS-SRC-110','CORPUS-SRC-111','CORPUS-SRC-112','CORPUS-SRC-113','CORPUS-SRC-114','CORPUS-SRC-115','CORPUS-SRC-116','CORPUS-SRC-117','CORPUS-SRC-118','CORPUS-SRC-119']; bs=CommentedMap((k,[]) for k in direct); bs['CORPUS-SRC-101-119']=[]; pred={f'CORPUS-SRC-{n:03d}' for n in range(101,120)}; sep=set(direct)&pred; bc=CommentedMap((k,[]) for k in ['SOURCE_SPECIFIC_STUDY','INTEGRATION_GOVERNANCE_RECORD','PROBLEM_LOCAL_SYNTHESIS','MIGRATION_TRANSACTION_LEDGER','PRESERVED_FINDING_BASIS'])
    for r in fs:
        fid=r['finding_set_id']
        for k in r.get('problem_bindings',[]):
            if k in bp: bp[k].append(fid)
        b=set(r.get('source_bindings',[]))
        for k in direct:
            if k in b: bs[k].append(fid)
        if b&pred and not(len(b)==1 and next(iter(b)) in sep): bs['CORPUS-SRC-101-119'].append(fid)
        cl=r.get('record_class')
        if cl in {'ACTIVE_PREDECESSOR_FINDING_BASIS','ACCEPTED_MIGRATION_SOURCE_FINDING_BASIS'}: bc['PRESERVED_FINDING_BASIS'].append(fid)
        elif cl in bc: bc[cl].append(fid)
    d['indexes']['by_problem']=bp; d['indexes']['by_source']=bs; d['indexes']['by_record_class']=bc
    c=d['coverage']; c['finding_sets_registered']=88; c['source_specific_and_integration_records_registered']=26; c['problem_syntheses_registered']=57; c['current_problem_synthesis_tree_yaml_records_accounted_for']=57; c['corpus_study_records_accounted_for']=26
    one(d['findings_gaps'],'gap_id','FINDINGS-GAP-002')['statement']='All nineteen registered Theologico-Political predecessor sources now have complete provisional source-specific studies within registered scopes; many sources elsewhere in the open Strauss corpus still lack independent source-specific study records.'
    one(d['findings_gaps'],'gap_id','FINDINGS-GAP-003')['statement']='All nineteen Theologico-Political writings now have complete provisional item studies within registered scopes; textual-state comparisons, independent corroboration, proposition normalization, and certification remain incomplete.'
    add(d['validation_rules'],'FINDSET-022 through FINDSET-026 preserve their registered witnesses, source-specific predecessor retests, pending textual-state comparisons, incomplete independent corroboration, and no-successor safeguards')
    add(d['validation_rules'],'FINDSET-023 preserves material nonconfirmation and probable source misallocation instead of importing orthodoxy, unbelief, Zionism, or medieval-philosophy claims absent from An Unspoken Prologue')
    add(d['validation_rules'],'FINDSET-026 preserves LAST_PARAGRAPH_ONLY scope and excludes Green editorial theological interpretation from Strauss evidence')
    save(p,d)

def update_manifest_audit_mapping_process_schedule():
    p='manifest.yaml'; d=load(p); d['identity']['version']='1.19.0'; d['revision_history']['predecessor_version']='1.18.0'; d['revision_history']['predecessor_blob_sha']='PRESERVED_BY_GIT'; d['revision_history']['reason']='Complete the final five Theologico-Political source studies and synchronize corpus v1.23.0, findings v1.15.0, audit v3.7.0, mapping v1.19.0, process v1.21.0, and schedule v1.19.0 while preserving repository semantic incompletion and all noncertification safeguards.'; d['audit']['version']='3.7.0'; d['component_completion']['theologico_political_item_level_source_statuses']='19_OF_19_IDENTITIES_19_OF_19_REVIEWED_ITEM_WITNESSES_19_OF_19_COMPLETE_PROVISIONAL_ITEM_STUDIES_WITHIN_REGISTERED_SCOPES'; d['corpus']['registry_version']='1.23.0'; s=d['corpus']['theologico_political_item_level_statuses']; s['independent_sequential_study_count']=19; s['remaining_without_independent_sequential_study']=0
    for x in SOURCES.values(): add(s['completed_study_ids'],x['internal'])
    s['rule']='All nineteen predecessor items have reviewed witnesses and complete provisional source studies within their registered scopes. This sequence completion remains distinct from original-edition comparison, independent corroboration, doctrinal certification, migration completion, successor activation, or repository completion.'; d['findings']['registry_version']='1.15.0'; d['findings']['newly_registered']=[x['findset'] for x in SOURCES.values()]+[q[0] for x in SOURCES.values() for q in x['synth']]; save(p,d)

    p='audits/operational-completeness.yaml'; d=load(p); d['identity']['version']='3.7.0'; d['revision_history']['predecessor_version']='3.6.0'; d['revision_history']['predecessor_blob_sha']='PRESERVED_BY_GIT'; d['revision_history']['reason']='Complete the final five Theologico-Political source studies, reaching 19-of-19 independent sequential reconstruction within registered scopes while preserving textual-state, corroboration, semantic-completion, and certification limits.'; d['basis']['current_revision_scope']='production/complete-final-five-tp-studies'; s=d['summary']['theologico_political_item_level_status']; s['independently_reconstructed_count_within_this_sequence']=19; s['remaining_without_independent_sequential_study']=0
    for sid,x in SOURCES.items(): add(s['completed_source_ids'],sid); add(s['completed_witness_ids'],x['witness']); add(s['completed_study_ids'],x['internal'])
    s['witness_only_source_ids']=[]; s['witness_only_witness_ids']=[]; s['interpretation_limit']='All nineteen predecessor items now have complete provisional independent sequential reconstructions within registered scopes. These source-specific studies are not independent corroboration, original/earlier textual-state comparisons remain pending where noted, SRC115 materially corrects a predecessor source conflation, and no doctrine, migration, successor, or repository completion is certified.'
    d['summary']['remaining_major_deficiencies'][0]='original/earlier textual-state comparisons and independent corroboration remain incomplete despite 19-of-19 registered-scope sequential reconstruction'; add(d['production_order']['completed_in_current_sequence'],'final five Theologico-Political source studies complete provisional with FINDSET-022 through FINDSET-026 and FINDSET-144 through FINDSET-157'); d['production_order']['next']=['run complete structural and behavioral validation for the nineteen-source reconstruction','expand original/earlier textual-state comparisons','expand independent primary and reviewed-work witnesses','continue proposition-level and broader corpus completion','validate actual ministerial reports against the full contract stack']; save(p,d)

    p='migrations/lean-operational-interface.yaml'; d=load(p); d['identity']['version']='1.19.0'; d['revision_history']['predecessor_version']='1.18.0'; d['revision_history']['predecessor_blob_sha']='PRESERVED_BY_GIT'; d['revision_history']['reason']='Synchronize completion of all nineteen Theologico-Political registered-scope source studies while preserving semantic incompletion, textual-state limits, noncorroboration, noncertification, predecessor authority, and blocked final repin.'; d['completion_audit']['version']='3.7.0'; d['production_process']['completed_study_subunit']='NINETEEN_OF_19_COMPLETE_PROVISIONAL_WITHIN_REGISTERED_SCOPES'; c=d['mappings']['corpus']; c['interface']['registry_version']='1.23.0'; s=c['theologico_political_item_level_statuses']; s['independent_sequential_study_count']=19; s['remaining_without_independent_sequential_study']=0
    for x in SOURCES.values(): add(s['completed_study_ids'],x['internal'])
    s['witness_only_source_ids']=[]; f=d['mappings']['findings']; f['interface']['registry_version']='1.15.0'; f['newly_registered']=[CommentedMap([('finding_set_id',x['findset']),('path',study_path(x))]) for x in SOURCES.values()]+[CommentedMap([('finding_set_id',fid),('path',f'problems/{problem}/synthesis/{filename}'),('derived_from',s0['findset'])]) for s0 in SOURCES.values() for fid,problem,filename in s0['synth']]
    rels=d['mappings']['problems'].setdefault('new_source_relations',[])
    for sid,x in SOURCES.items():
        for fid,problem,filename in x['synth']:
            rec=CommentedMap([('path',f'problems/{problem}/synthesis/{filename}'),('source',sid),('derivation',f"{x['findset']}_TO_{fid}")]);
            if not any(r.get('path')==rec['path'] for r in rels): rels.append(rec)
    save(p,d)

    p='history/production-plans/2026-07-27-ten-step-completion-process.yaml'; d=load(p); d['identity']['version']='1.21.0'; d['revision_history']['predecessor_version']='1.20.0'; d['revision_history']['predecessor_blob_sha']='PRESERVED_BY_GIT'; d['revision_history']['reason']='Complete the final five Theologico-Political item studies and close the nineteen-source sequential-reconstruction subunit while preserving broader corpus, corroboration, migration, certification, and repin blockers.'; d['steps'][0]['current_version']='3.7.0'; d['steps'][1]['current_version']='1.19.0'
    step7=d['steps'][6]['completed'];
    for x in SOURCES.values(): add(step7,f"{x['title']} supplies provisional jurisdiction-preserving synthesis from {x['internal']}")
    step8=d['steps'][7]; add(step8['completed'],'all 19 Theologico-Political predecessor writings now have complete provisional independent sequential reconstructions within registered scopes'); step8['remaining']=[r for r in step8['remaining'] if not (isinstance(r,str) and 'five independent sequential item studies' in r)]
    step9=d['steps'][8]; step9['completed_in_current_sequence']=['tests cover all nineteen Theologico-Political reviewed witnesses and all nineteen complete provisional registered-scope source studies','tests preserve edition-comparison, source-scope, speaker/editorial-layer, predecessor-correction, noncorroboration, noncertification, and no-successor safeguards']; step9['current_requirement']='Run complete GitHub Actions validation before merge; passing tests validate declared contracts, not philosophical truth or repository completion.'
    d['current_production_unit']={'step':8,'completed_subunit':{'title':'Nineteen-source Theologico-Political independent sequential reconstruction','state':'COMPLETE_PROVISIONAL_19_OF_19_WITHIN_REGISTERED_SCOPES','study_coverage':'COMPLETE_19_OF_19'},'next_subunit':{'title':'Textual-state comparison and independent witness expansion','state':'OPEN'}}; save(p,d)

    p='history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml'; d=load(p); d['identity']['version']='1.19.0'; d['revision_history']['predecessor_version']='1.18.0'; d['revision_history']['predecessor_blob_sha']='PRESERVED_BY_GIT'; d['revision_history']['reason']='Complete the final five independent sequential reconstructions, reaching 19-of-19 within registered scopes while preserving textual-state, corroboration, noncertification, and predecessor safeguards.'; d['status']['independent_sequential_study_completion']='COMPLETE_19_OF_19'
    for group in d.get('priority_groups',[]):
        for item in group.get('items',[]):
            sid=item.get('source_id')
            if sid in SOURCES:
                x=SOURCES[sid]; item['state']='REVIEWED_WITNESS_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDY'; item['study_id']=x['internal']; item['next_action']='TEXTUAL_STATE_COMPARISON_AND_INDEPENDENT_WITNESS_EXPANSION_WHERE_AVAILABLE'
    sel=d['selection'];
    for sid,x in SOURCES.items(): add(sel['completed_study_ids'],x['internal'])
    sel['selection_state']='NINETEEN_REVIEWED_ITEM_WITNESSES_NINETEEN_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDIES_WITHIN_REGISTERED_SCOPES'; sel['completed_units']=['all nineteen predecessor source identities have reviewed witnesses','all nineteen source studies are complete provisional within registered scopes','all original/earlier textual-state and independent-corroboration limits remain explicit','source-study completion does not certify doctrine, migration, successor activation, or repository completion']
    term=d['termination']; term['independent_sequential_reconstruction']='COMPLETE_19_OF_19'; term['next_item_study']='NONE'; d['next_item_study_unit']={'source_id':'NONE','title':'Nineteen-source sequential reconstruction complete within registered scopes','action':'PROCEED_TO_TEXTUAL_STATE_COMPARISON_AND_INDEPENDENT_WITNESS_EXPANSION','prerequisite':'ALL_19_REGISTERED_SCOPE_STUDIES_COMPLETE_PROVISIONAL'}; save(p,d)

def update_python_validators():
    p=ROOT/'corpus_registry.py'; t=p.read_text()
    insert="""  'CORPUS-SRC-114': {'status_id': 'CORPUS-STATUS-114', 'witness_id': 'CORPUS-WIT-114', 'study_id': 'CORPUS-STUDY-022', 'internal_study_id': 'GOOD-SOCIETY-STUDY-001', 'study_path': 'studies/theologico-political/perspectives-on-the-good-society/sequential-reconstruction.yaml', 'witness_record_path': 'studies/theologico-political/perspectives-on-the-good-society/reviewed-witness.yaml', 'printed_page_range': {'start': 431, 'end': 445}, 'pdf_page_range_one_based': {'start': 450, 'end': 464}, 'reading_state': 'COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS', 'platform_reference': False},\n  'CORPUS-SRC-115': {'status_id': 'CORPUS-STATUS-115', 'witness_id': 'CORPUS-WIT-115', 'study_id': 'CORPUS-STUDY-023', 'internal_study_id': 'UNSPOKEN-PROLOGUE-STUDY-001', 'study_path': 'studies/theologico-political/an-unspoken-prologue/sequential-reconstruction.yaml', 'witness_record_path': 'studies/theologico-political/an-unspoken-prologue/reviewed-witness.yaml', 'printed_page_range': {'start': 449, 'end': 452}, 'pdf_page_range_one_based': {'start': 468, 'end': 471}, 'reading_state': 'COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS', 'platform_reference': False},\n  'CORPUS-SRC-117': {'status_id': 'CORPUS-STATUS-117', 'witness_id': 'CORPUS-WIT-117', 'study_id': 'CORPUS-STUDY-024', 'internal_study_id': 'GIVING-ACCOUNTS-STUDY-001', 'study_path': 'studies/theologico-political/a-giving-of-accounts/sequential-reconstruction.yaml', 'witness_record_path': 'studies/theologico-political/a-giving-of-accounts/reviewed-witness.yaml', 'printed_page_range': {'start': 457, 'end': 466}, 'pdf_page_range_one_based': {'start': 476, 'end': 485}, 'reading_state': 'COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS', 'platform_reference': False},\n  'CORPUS-SRC-118': {'status_id': 'CORPUS-STATUS-118', 'witness_id': 'CORPUS-WIT-118', 'study_id': 'CORPUS-STUDY-025', 'internal_study_id': 'PHILOSOPHY-LAW-PLAN-STUDY-001', 'study_path': 'studies/theologico-political/plan-philosophy-and-the-law-historical-essays/sequential-reconstruction.yaml', 'witness_record_path': 'studies/theologico-political/plan-philosophy-and-the-law-historical-essays/reviewed-witness.yaml', 'printed_page_range': {'start': 467, 'end': 470}, 'pdf_page_range_one_based': {'start': 486, 'end': 489}, 'reading_state': 'COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS', 'platform_reference': False},\n  'CORPUS-SRC-119': {'status_id': 'CORPUS-STATUS-119', 'witness_id': 'CORPUS-WIT-119', 'study_id': 'CORPUS-STUDY-026', 'internal_study_id': 'HIERO-RESTATEMENT-LAST-PARAGRAPH-STUDY-001', 'study_path': 'studies/theologico-political/restatement-on-xenophons-hiero/sequential-reconstruction.yaml', 'witness_record_path': 'studies/theologico-political/restatement-on-xenophons-hiero/reviewed-witness.yaml', 'printed_page_range': {'start': 471, 'end': 473}, 'pdf_page_range_one_based': {'start': 490, 'end': 492}, 'reading_state': 'COMPLETE_FOR_REGISTERED_LAST_PARAGRAPH_OF_REVIEWED_1997_COLLECTED_WITNESS', 'platform_reference': False},\n"""
    marker=" 'CORPUS-SRC-116': {'status_id': 'CORPUS-STATUS-116'"
    idx=t.find(marker); end=t.find("'platform_reference': False}}",idx)
    if idx<0 or end<0: raise RuntimeError('cannot locate complete TP tail')
    end += len("'platform_reference': False}")
    t=t[:end]+",\n"+insert.rstrip(',\n')+t[end:]
    t=re.sub(r"WITNESS_ONLY_TP_ITEMS: dict\[str, dict\[str, Any\]\] = \{.*?\}\n\n\nclass CorpusRegistryError", "WITNESS_ONLY_TP_ITEMS: dict[str, dict[str, Any]] = {}\n\n\nclass CorpusRegistryError", t, flags=re.S)
    for a,b in [('1.22.0','1.23.0'),('study records": (len(study_ids), 21)','study records": (len(study_ids), 26)'),('"theologico_political_independent_item_studies_registered": 14','"theologico_political_independent_item_studies_registered": 19'),('!= "INCOMPLETE_14_OF_19"','!= "COMPLETE_19_OF_19"'),('must be INCOMPLETE_14_OF_19','must be COMPLETE_19_OF_19')]: t=t.replace(a,b)
    p.write_text(t)

    p=ROOT/'findings_registry.py'; t=p.read_text()
    paths=[]
    for x in SOURCES.values():
        for _,problem,filename in x['synth']: paths.append(f'    "problems/{problem}/synthesis/{filename}",\n')
    marker='}\n\nEXPECTED_TRANSACTION_PATHS'
    t=replace_once(t,marker,''.join(paths)+'}\n\nEXPECTED_TRANSACTION_PATHS','synthesis paths')
    direct_marker='    "CORPUS-SRC-116",\n]'
    new_direct='    "CORPUS-SRC-116",\n    "CORPUS-SRC-114",\n    "CORPUS-SRC-115",\n    "CORPUS-SRC-117",\n    "CORPUS-SRC-118",\n    "CORPUS-SRC-119",\n]'
    t=replace_once(t,direct_marker,new_direct,'direct sources')
    contracts='''    "FINDSET-022": {"source_id":"CORPUS-SRC-114","local_syntheses":["FINDSET-144","FINDSET-145","FINDSET-146"],"problem_bindings":{"FINDSET-144":"theologico-political","FINDSET-145":"theory-vs-practice","FINDSET-146":"ancients-vs-moderns"},"required_limits":{"witness_id":"CORPUS-WIT-114","original_1963_criterion_comparison":"PENDING","independent_corroboration":"INCOMPLETE"}},\n    "FINDSET-023": {"source_id":"CORPUS-SRC-115","local_syntheses":["FINDSET-147","FINDSET-148"],"problem_bindings":{"FINDSET-147":"theologico-political","FINDSET-148":"ancients-vs-moderns"},"required_limits":{"witness_id":"CORPUS-WIT-115","original_1978_interpretation_comparison":"PENDING","predecessor_retest_state":"MATERIAL_NONCONFIRMATION_AND_PROBABLE_SOURCE_MISALLOCATION","independent_corroboration":"INCOMPLETE"}},\n    "FINDSET-024": {"source_id":"CORPUS-SRC-117","local_syntheses":["FINDSET-149","FINDSET-150","FINDSET-151"],"problem_bindings":{"FINDSET-149":"theologico-political","FINDSET-150":"wise-vs-vulgar","FINDSET-151":"ancients-vs-moderns"},"required_limits":{"witness_id":"CORPUS-WIT-117","original_1970_college_comparison":"PENDING","independent_corroboration":"INCOMPLETE"}},\n    "FINDSET-025": {"source_id":"CORPUS-SRC-118","local_syntheses":["FINDSET-152","FINDSET-153","FINDSET-154"],"problem_bindings":{"FINDSET-152":"theologico-political","FINDSET-153":"athens-vs-jerusalem","FINDSET-154":"wise-vs-vulgar"},"required_limits":{"witness_id":"CORPUS-WIT-118","earlier_textual_state_comparison":"PENDING","independent_corroboration":"INCOMPLETE"}},\n    "FINDSET-026": {"source_id":"CORPUS-SRC-119","local_syntheses":["FINDSET-155","FINDSET-156","FINDSET-157"],"problem_bindings":{"FINDSET-155":"theologico-political","FINDSET-156":"ancients-vs-moderns","FINDSET-157":"theory-vs-practice"},"required_limits":{"witness_id":"CORPUS-WIT-119","registered_scope":"LAST_PARAGRAPH_ONLY","earlier_textual_state_comparison":"PENDING","independent_corroboration":"INCOMPLETE"}},\n'''
    marker='}\n\n\nclass FindingsRegistryError'
    t=replace_once(t,marker,contracts+'}\n\n\nclass FindingsRegistryError','contracts')
    t=t.replace('1.14.0','1.15.0').replace('if len(finding_ids) != 69:','if len(finding_ids) != 88:').replace('expected 69 finding sets','expected 88 finding sets')
    p.write_text(t)

def update_tests():
    for p in (ROOT/'tests').glob('test_*.py'):
        t=p.read_text()
        reps=[('"1.22.0"','"1.23.0"'),('"1.14.0"','"1.15.0"'),('"1.18.0"','"1.19.0"'),('"3.6.0"','"3.7.0"'),('"1.20.0"','"1.21.0"'),('INCOMPLETE_14_OF_19','COMPLETE_19_OF_19'),('theologico_political_independent_item_studies_registered"], 14','theologico_political_independent_item_studies_registered"], 19'),('independent_sequential_study_count"], 14','independent_sequential_study_count"], 19'),('independently_reconstructed_count_within_this_sequence"], 14','independently_reconstructed_count_within_this_sequence"], 19'),('remaining_without_independent_sequential_study"], 5','remaining_without_independent_sequential_study"], 0'),('schedule["termination"]["next_item_study"], "CORPUS-SRC-114"','schedule["termination"]["next_item_study"], "NONE"'),('            61,','            66,'),('registry["coverage"]["study_records_registered"], 21','registry["coverage"]["study_records_registered"], 26'),('self.assertEqual(len(finding_ids), 69)','self.assertEqual(len(finding_ids), 88)'),('self.assertEqual(len(registered), 43)','self.assertEqual(len(registered), 57)'),('self.assertEqual(len(registered), 21)','self.assertEqual(len(registered), 26)')]
        for a,b in reps: t=t.replace(a,b)
        p.write_text(t)
    p=ROOT/'tests/test_corpus_registry.py'; t=p.read_text(); t=re.sub(r'    def test_five_tp_sources_have_witnesses_but_still_require_study\(self\) -> None:\n.*?(?=    def test_spinoza_treatise_witness_and_study_are_registered)', '    def test_all_tp_sources_have_completed_registered_scope_studies(self) -> None:\n        registry = corpus_registry.load_registry()\n        self.assertEqual(corpus_registry.WITNESS_ONLY_TP_ITEMS, {})\n        self.assertEqual(registry["coverage"]["theologico_political_independent_item_studies_registered"], 19)\n        self.assertEqual(registry["termination"]["theologico_political_independent_study_state"], "COMPLETE_19_OF_19")\n\n', t, flags=re.S); p.write_text(t)
    final='''from pathlib import Path\nimport unittest\nimport yaml\nROOT=Path(__file__).resolve().parents[1]\ndef load(p):\n    with (ROOT/p).open(encoding="utf-8") as f:return yaml.safe_load(f)\nclass FinalTPSequenceCompletionTests(unittest.TestCase):\n    def test_final_five_bindings_and_witness_distinction(self):\n        corpus=load("corpus/index.yaml")\n        expected={"CORPUS-SRC-114":("CORPUS-STUDY-022","GOOD-SOCIETY-STUDY-001"),"CORPUS-SRC-115":("CORPUS-STUDY-023","UNSPOKEN-PROLOGUE-STUDY-001"),"CORPUS-SRC-117":("CORPUS-STUDY-024","GIVING-ACCOUNTS-STUDY-001"),"CORPUS-SRC-118":("CORPUS-STUDY-025","PHILOSOPHY-LAW-PLAN-STUDY-001"),"CORPUS-SRC-119":("CORPUS-STUDY-026","HIERO-RESTATEMENT-LAST-PARAGRAPH-STUDY-001")}\n        for sid,(cid,iid) in expected.items():\n            src=next(x for x in corpus["source_entities"] if x["source_id"]==sid); self.assertEqual(src["study_records"],[cid])\n            status=load(next(x for x in corpus["source_status_records"] if x["source_id"]==sid)["path"]); self.assertEqual(status["status"]["independent_sequential_study"],iid); self.assertEqual(status["termination"]["study_state"],"COMPLETE_PROVISIONAL")\n            wit=next(x for x in corpus["reviewed_witnesses"] if x["source_id"]==sid); wr=load(wit["witness_record_path"]); self.assertEqual(wr["termination"]["study_state"],"INCOMPLETE")\n    def test_src115_correction_is_preserved(self):\n        st=load("studies/theologico-political/an-unspoken-prologue/sequential-reconstruction.yaml"); text=" ".join(st["comparison_with_active_predecessor"]["qualifications"]); self.assertIn("no discussion of orthodoxy, unbelief, Zionism, or medieval philosophy",text); self.assertIn("source conflation",text)\n    def test_src117_speaker_layers_and_autobiography_limit(self):\n        st=load("studies/theologico-political/a-giving-of-accounts/sequential-reconstruction.yaml"); self.assertIn("jacob_klein",st["speaker_and_documentary_layers"]); self.assertIn("tape_break",st["speaker_and_documentary_layers"]); self.assertIn("starting point", " ".join(st["source_limits"]))\n    def test_src118_and_src119_editorial_limits(self):\n        a=load("studies/theologico-political/plan-philosophy-and-the-law-historical-essays/sequential-reconstruction.yaml"); self.assertEqual(a["source"]["editorial_provenance"]["editor_mature_view_claim"],"EDITORIAL_INTERPRETATION_NOT_STRAUSS_STATEMENT")\n        b=load("studies/theologico-political/restatement-on-xenophons-hiero/sequential-reconstruction.yaml"); self.assertEqual(b["termination"]["registered_scope"],"LAST_PARAGRAPH_ONLY"); self.assertIn("universal state", " ".join(b["comparison_with_active_predecessor"]["qualifications"]))\n    def test_sequence_complete_repository_not_certified(self):\n        c=load("corpus/index.yaml"); m=load("manifest.yaml"); s=load("history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml"); self.assertEqual(c["coverage"]["theologico_political_independent_item_studies_registered"],19); self.assertEqual(c["termination"]["theologico_political_independent_study_state"],"COMPLETE_19_OF_19"); self.assertEqual(s["termination"]["independent_sequential_reconstruction"],"COMPLETE_19_OF_19"); self.assertEqual(s["termination"]["next_item_study"],"NONE"); self.assertEqual(m["status"]["semantic_completion"],"INCOMPLETE"); self.assertEqual(m["status"]["doctrinal_certification"],"NOT_CERTIFIED")\nif __name__=="__main__": unittest.main()\n'''; (ROOT/'tests/test_final_tp_sequence_completion.py').write_text(final)

def main():
    for x in SOURCES.values():
        if not (ROOT/study_path(x)).is_file(): raise RuntimeError('missing '+study_path(x))
    update_statuses(); write_syntheses(); update_corpus(); update_findings(); update_manifest_audit_mapping_process_schedule(); update_python_validators(); update_tests(); print('final five TP studies materialized')
if __name__=='__main__': main()
