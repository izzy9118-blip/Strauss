#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return yaml.safe_load((ROOT / path).read_text(encoding='utf-8'))


def dump(path, data):
    (ROOT / path).write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120), encoding='utf-8')


def find(items, key, value):
    return next(x for x in items if x.get(key) == value)

# Corpus registry
cp = 'corpus/index.yaml'
c = load(cp)
c['identity']['version'] = '1.13.0'
c['revision_history'] = {
    'predecessor_version': '1.12.0',
    'predecessor_blob_sha': 'aa9e00e2272f35a773e3be89fa1269650642924f',
    'transformation': 'SUBSTANTIVE_FORWARD_REVISION',
    'reason': ('Register SPINOZA-TREATISE-STUDY-001 as CORPUS-STUDY-012 and its two jurisdiction-preserving local syntheses, '
               'raising Theologico-Political independent sequential study coverage to five of nineteen while preserving '
               'fourteen pending studies, original-edition comparison limits, noncorroboration, noncertification, predecessor authority, and no successor effect.'),
}
src = find(c['source_entities'], 'source_id', 'CORPUS-SRC-103')
src['study_records'] = ['CORPUS-STUDY-012']
src['item_level_source_status'] = 'REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION'
src['study_status'] = 'COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS'
src['limits'] = [
    'reviewed witness is the fingerprinted 1997 SUNY collected reprint, not a separately reviewed 1948 journal printing',
    'printed pages 181-233 correspond to one-based PDF pages 200-252 in the reviewed file',
    'original 1948 journal comparison remains pending',
    'SPINOZA-TREATISE-STUDY-001 is source-local and not independent corroboration of Spinoza or represented traditions',
    'no doctrinal certification, migration, predecessor displacement, or successor effect follows from study completion',
]
st = find(c['source_status_records'], 'status_id', 'CORPUS-STATUS-103')
st['completion'] = 'REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION'
if not any(x.get('study_id') == 'CORPUS-STUDY-012' for x in c['study_records']):
    c['study_records'].append({
        'study_id': 'CORPUS-STUDY-012', 'source_id': 'CORPUS-SRC-103',
        'path': 'studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/sequential-reconstruction.yaml',
        'record_role': 'SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION',
        'completion': 'COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS', 'certification': 'NOT_CERTIFIED'
    })
c['coverage']['study_records_registered'] = 12
c['coverage']['theologico_political_independent_item_studies_registered'] = 5
c['coverage']['current_studies_tree_yaml_records_accounted_for'] = 52
gap = find(c['corpus_gaps'], 'gap_id', 'CORPUS-GAP-003')
gap['statement'] = ('All nineteen predecessor writings have bounded source identities and reviewed witnesses. Five have complete provisional '
                    'independent sequential studies; the remaining fourteen have registered witnesses but still require independent sequential reconstruction.')
c['validation_rules'] = [s.replace('all fifteen witness-only Theologico-Political sources', 'all fourteen witness-only Theologico-Political sources') for s in c['validation_rules']]
c['termination']['theologico_political_independent_study_state'] = 'INCOMPLETE_5_OF_19'
c['termination']['next_required_units'][0] = 'conduct independent sequential reconstruction for the remaining fourteen writings according to the production schedule'
dump(cp, c)

# Findings registry
fp = 'findings/index.yaml'
f = load(fp)
f['identity']['version'] = '1.5.0'
f['revision_history'] = {
    'predecessor_version': '1.4.0', 'predecessor_blob_sha': '820aacb74d7dbd340b75222a73d78eaa62b8f2db',
    'transformation': 'SUBSTANTIVE_FORWARD_REVISION',
    'reason': ('Register SPINOZA-TREATISE-STUDY-001 as FINDSET-012 and its Theologico-Political and Wise-versus-Vulgar '
               'local syntheses as FINDSET-122 and FINDSET-123 while preserving source-local derivation, pending 1948 comparison, '
               'incomplete independent corroboration, noncertification, and no successor effect.')
}
newsets = [
 {'finding_set_id':'FINDSET-012','path':'studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/sequential-reconstruction.yaml','record_class':'SOURCE_SPECIFIC_STUDY','record_role':'SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION','source_bindings':['CORPUS-SRC-103'],'problem_bindings':['theologico-political','wise-vs-vulgar'],'status':'COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS','certification':'NOT_CERTIFIED','successor_effect':'NONE','witness_id':'CORPUS-WIT-103','original_edition_comparison':'PENDING','independent_corroboration':'INCOMPLETE','derived_local_syntheses':['FINDSET-122','FINDSET-123']},
 {'finding_set_id':'FINDSET-122','path':'problems/theologico-political/synthesis/how-to-study-spinozas-theologico-political-treatise.yaml','record_class':'PROBLEM_LOCAL_SYNTHESIS','record_role':'SOURCE_TO_PROBLEM_SYNTHESIS','source_bindings':['CORPUS-SRC-103'],'problem_bindings':['theologico-political'],'derived_from':['FINDSET-012'],'status':'PROVISIONAL_NOT_CERTIFIED','certification':'NOT_CERTIFIED','successor_effect':'NONE'},
 {'finding_set_id':'FINDSET-123','path':'problems/wise-vs-vulgar/synthesis/how-to-study-spinozas-theologico-political-treatise.yaml','record_class':'PROBLEM_LOCAL_SYNTHESIS','record_role':'SOURCE_TO_PROBLEM_SYNTHESIS','source_bindings':['CORPUS-SRC-103'],'problem_bindings':['wise-vs-vulgar'],'derived_from':['FINDSET-012'],'status':'PROVISIONAL_NOT_CERTIFIED','certification':'NOT_CERTIFIED','successor_effect':'NONE'},
]
ids={x['finding_set_id'] for x in f['finding_sets']}
# keep numeric source studies before 100-series syntheses
pos=next(i for i,x in enumerate(f['finding_sets']) if x['finding_set_id']=='FINDSET-101')
for x in newsets:
    if x['finding_set_id']=='FINDSET-012' and x['finding_set_id'] not in ids:
        f['finding_sets'].insert(pos,x); pos += 1
for x in newsets[1:]:
    if x['finding_set_id'] not in ids:
        # insert before migration 201
        p=next(i for i,y in enumerate(f['finding_sets']) if y['finding_set_id']=='FINDSET-201')
        f['finding_sets'].insert(p,x)
# derive indexes exactly as validator does
problems=['nomos-vs-physis','philosophy-vs-poetry','theory-vs-practice','theologico-political','athens-vs-jerusalem','wise-vs-vulgar','ancients-vs-moderns']
by_problem={k:[] for k in problems}
for x in f['finding_sets']:
    for p in x.get('problem_bindings',[]):
        if p in by_problem: by_problem[p].append(x['finding_set_id'])
direct=['CORPUS-SRC-001','CORPUS-SRC-002','CORPUS-SRC-003','CORPUS-SRC-102','CORPUS-SRC-103','CORPUS-SRC-105','CORPUS-SRC-111']
by_source={k:[] for k in direct}; by_source['CORPUS-SRC-101-119']=[]
preds={f'CORPUS-SRC-{n:03d}' for n in range(101,120)}
sep={'CORPUS-SRC-102','CORPUS-SRC-103','CORPUS-SRC-105','CORPUS-SRC-111'}
for x in f['finding_sets']:
    binds=set(x.get('source_bindings',[])); fid=x['finding_set_id']
    for k in direct:
        if k in binds: by_source[k].append(fid)
    if binds & preds and not (len(binds)==1 and next(iter(binds)) in sep): by_source['CORPUS-SRC-101-119'].append(fid)
by_class={k:[] for k in ['SOURCE_SPECIFIC_STUDY','INTEGRATION_GOVERNANCE_RECORD','PROBLEM_LOCAL_SYNTHESIS','MIGRATION_TRANSACTION_LEDGER','PRESERVED_FINDING_BASIS']}
for x in f['finding_sets']:
    rc=x.get('record_class')
    if rc in {'ACTIVE_PREDECESSOR_FINDING_BASIS','ACCEPTED_MIGRATION_SOURCE_FINDING_BASIS'}: by_class['PRESERVED_FINDING_BASIS'].append(x['finding_set_id'])
    elif rc in by_class: by_class[rc].append(x['finding_set_id'])
f['indexes']={'by_problem':by_problem,'by_source':by_source,'by_record_class':by_class}
f['coverage'].update({'finding_sets_registered':40,'source_specific_and_integration_records_registered':12,'problem_syntheses_registered':23,'current_problem_synthesis_tree_yaml_records_accounted_for':23,'corpus_study_records_accounted_for':12})
fg=find(f['findings_gaps'],'gap_id','FINDINGS-GAP-003')
fg['statement']='Five of the nineteen Theologico-Political writings now have complete provisional item studies; the remaining fourteen lack individual sequential studies.'
f['validation_rules'].append('FINDSET-012 may derive only FINDSET-122 and FINDSET-123 and must preserve pending original-edition comparison, incomplete independent corroboration, noncertification, and no successor effect')
f['termination']['next_required_units']=[s.replace('remaining fifteen Strauss item witnesses and studies','remaining fourteen Strauss item studies') for s in f['termination']['next_required_units']]
dump(fp,f)

# Python validators: exact controlled forward edits
p=ROOT/'corpus_registry.py'; t=p.read_text(encoding='utf-8')
t=t.replace('"studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/reviewed-witness.yaml",\n}', '"studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/reviewed-witness.yaml",\n    "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/sequential-reconstruction.yaml",\n}')
insert='''    "CORPUS-SRC-103": {\n        "status_id": "CORPUS-STATUS-103",\n        "witness_id": "CORPUS-WIT-103",\n        "study_id": "CORPUS-STUDY-012",\n        "internal_study_id": "SPINOZA-TREATISE-STUDY-001",\n        "study_path": "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/sequential-reconstruction.yaml",\n        "witness_record_path": "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/reviewed-witness.yaml",\n        "printed_page_range": {"start": 181, "end": 233},\n        "pdf_page_range_one_based": {"start": 200, "end": 252},\n        "reading_state": "COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS",\n        "platform_reference": False,\n    },\n'''
t=t.replace('    "CORPUS-SRC-105": {', insert+'    "CORPUS-SRC-105": {',1)
start=t.index('    "CORPUS-SRC-103": {', t.index('WITNESS_ONLY_TP_ITEMS'))
end=t.index('    "CORPUS-SRC-104": {', start)
t=t[:start]+t[end:]
t=t.replace('identity.get("version") != "1.12.0"','identity.get("version") != "1.13.0"').replace('identity.version must be 1.12.0','identity.version must be 1.13.0')
t=t.replace('"study records": (len(study_ids), 11)','"study records": (len(study_ids), 12)')
t=t.replace('"theologico_political_independent_item_studies_registered": 4','"theologico_political_independent_item_studies_registered": 5')
t=t.replace('!= "INCOMPLETE_4_OF_19"','!= "INCOMPLETE_5_OF_19"').replace('must be INCOMPLETE_4_OF_19','must be INCOMPLETE_5_OF_19')
p.write_text(t,encoding='utf-8')

p=ROOT/'findings_registry.py'; t=p.read_text(encoding='utf-8')
t=t.replace('    "problems/theologico-political/synthesis/preface-to-spinozas-critique-of-religion.yaml",','    "problems/theologico-political/synthesis/preface-to-spinozas-critique-of-religion.yaml",\n    "problems/theologico-political/synthesis/how-to-study-spinozas-theologico-political-treatise.yaml",')
t=t.replace('    "problems/wise-vs-vulgar/synthesis/studies-in-platonic-political-philosophy.yaml",','    "problems/wise-vs-vulgar/synthesis/studies-in-platonic-political-philosophy.yaml",\n    "problems/wise-vs-vulgar/synthesis/how-to-study-spinozas-theologico-political-treatise.yaml",')
t=t.replace('    "CORPUS-SRC-102",\n    "CORPUS-SRC-105",','    "CORPUS-SRC-102",\n    "CORPUS-SRC-103",\n    "CORPUS-SRC-105",')
contract='''    "FINDSET-012": {\n        "source_id": "CORPUS-SRC-103",\n        "local_syntheses": ["FINDSET-122", "FINDSET-123"],\n        "problem_bindings": {"FINDSET-122": "theologico-political", "FINDSET-123": "wise-vs-vulgar"},\n        "required_limits": {"witness_id": "CORPUS-WIT-103", "original_edition_comparison": "PENDING", "independent_corroboration": "INCOMPLETE"},\n    },\n'''
t=t.replace('\n}\n\n\nclass FindingsRegistryError', '\n'+contract+'}\n\n\nclass FindingsRegistryError',1)
t=t.replace('separately_indexed = {"CORPUS-SRC-102", "CORPUS-SRC-105", "CORPUS-SRC-111"}','separately_indexed = {"CORPUS-SRC-102", "CORPUS-SRC-103", "CORPUS-SRC-105", "CORPUS-SRC-111"}')
t=t.replace('identity.get("version") != "1.4.0"','identity.get("version") != "1.5.0"').replace('identity.version must be 1.4.0','identity.version must be 1.5.0')
t=t.replace('len(finding_ids) != 37','len(finding_ids) != 40').replace('expected 37 finding sets','expected 40 finding sets')
p.write_text(t,encoding='utf-8')

# Synchronize ancillary operational-state prose without changing certification/activation status.
for path in ['manifest.yaml','audits/operational-completeness.yaml','migrations/lean-operational-interface.yaml','history/production-plans/2026-07-27-ten-step-completion-process.yaml','history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml']:
    p=ROOT/path
    text=p.read_text(encoding='utf-8')
    reps={
      '4_OF_19_COMPLETE_PROVISIONAL_ITEM_STUDIES':'5_OF_19_COMPLETE_PROVISIONAL_ITEM_STUDIES',
      '4_OF_19':'5_OF_19','4 of 19':'5 of 19','four of the nineteen':'five of the nineteen','Four of the nineteen':'Five of the nineteen',
      'fifteen pending independent sequential studies':'fourteen pending independent sequential studies',
      'remaining fifteen':'remaining fourteen','Remaining fifteen':'Remaining fourteen',
      'fifteen writings':'fourteen writings','Fifteen writings':'Fourteen writings',
      '15 independent':'14 independent','15 sequential':'14 sequential',
      'corpus registry v1.12.0':'corpus registry v1.13.0','findings registry v1.4.0':'findings registry v1.5.0',
      'registry_version: 1.12.0':'registry_version: 1.13.0','registry_version: 1.4.0':'registry_version: 1.5.0',
    }
    for a,b in reps.items(): text=text.replace(a,b)
    p.write_text(text,encoding='utf-8')
print('SRC103 integration materialized')
