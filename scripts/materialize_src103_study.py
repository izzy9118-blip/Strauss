#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = "CORPUS-SRC-103"
WIT = "CORPUS-WIT-103"
STUDY = "SPINOZA-TREATISE-STUDY-001"
CORPUS_STUDY = "CORPUS-STUDY-012"
STUDY_PATH = "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/sequential-reconstruction.yaml"
TP_SYN = "problems/theologico-political/synthesis/how-to-study-spinozas-theologico-political-treatise.yaml"
WVG_SYN = "problems/wise-vs-vulgar/synthesis/how-to-study-spinozas-theologico-political-treatise.yaml"


def load(path: str):
    with (ROOT / path).open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def dump(path: str, data) -> None:
    (ROOT / path).write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")


def replace_recursive(value, replacements: dict[str, str]):
    if isinstance(value, str):
        for old, new in replacements.items():
            value = value.replace(old, new)
        return value
    if isinstance(value, list):
        return [replace_recursive(v, replacements) for v in value]
    if isinstance(value, dict):
        return {k: replace_recursive(v, replacements) for k, v in value.items()}
    return value


def replace_text(path: str, replacements: dict[str, str]) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    for old, new in replacements.items():
        if old not in text:
            continue
        text = text.replace(old, new)
    p.write_text(text, encoding="utf-8")


def update_corpus() -> None:
    path = "corpus/index.yaml"
    d = load(path)
    d["identity"]["version"] = "1.13.0"
    d["revision_history"] = {
        "predecessor_version": "1.12.0",
        "predecessor_blob_sha": "aa9e00e2272f35a773e3be89fa1269650642924f",
        "transformation": "SUBSTANTIVE_FORWARD_REVISION",
        "reason": "Register SPINOZA-TREATISE-STUDY-001 as the fifth complete provisional Theologico-Political item study, preserving the reviewed 1997 witness, pending 1948 comparison, independent-corroboration limits, noncertification, predecessor authority, and no successor effect.",
    }
    source = next(x for x in d["source_entities"] if x["source_id"] == SRC)
    source["study_records"] = [CORPUS_STUDY]
    source["item_level_source_status"] = "REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION"
    source["study_status"] = "COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS"
    source["limits"] = [
        "reviewed witness is the fingerprinted 1997 SUNY collected reprint, not a separately reviewed 1948 journal printing",
        "printed pages 181-233 correspond to one-based PDF pages 200-252 in the reviewed file",
        "the argumentative body is printed pages 181-224 and notes continue through printed page 233",
        "the collection acknowledgment identifies the original publication as Proceedings of the American Academy for Jewish Research 17 (1948), 69-131",
        "SPINOZA-TREATISE-STUDY-001 is source-local and not independent corroboration of Spinoza or represented traditions",
        "original 1948 journal comparison remains pending",
    ]
    if not any(x.get("study_id") == CORPUS_STUDY for x in d["study_records"]):
        d["study_records"].append({
            "study_id": CORPUS_STUDY,
            "source_id": SRC,
            "path": STUDY_PATH,
            "record_role": "SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION",
            "completion": "COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS",
            "certification": "NOT_CERTIFIED",
        })
    c = d["coverage"]
    c["study_records_registered"] = 12
    c["theologico_political_independent_item_studies_registered"] = 5
    c["current_studies_tree_yaml_records_accounted_for"] = 52
    gap = next(x for x in d["corpus_gaps"] if x["gap_id"] == "CORPUS-GAP-003")
    gap["statement"] = "All nineteen predecessor writings have bounded source identities and reviewed item witnesses; CORPUS-SRC-102, CORPUS-SRC-103, CORPUS-SRC-105, CORPUS-SRC-109, and CORPUS-SRC-111 have complete provisional sequential studies, while the remaining fourteen lack independent item studies."
    d["validation_rules"] = [
        x.replace("CORPUS-SRC-103 preserves fingerprinted witness-only safeguards while sequential reconstruction remains pending", "CORPUS-SRC-103 preserves fingerprinted reviewed-witness safeguards and complete provisional sequential reconstruction while original-edition comparison remains pending")
        for x in d["validation_rules"]
    ]
    t = d["termination"]
    t["theologico_political_independent_study_state"] = "INCOMPLETE_5_OF_19"
    t["next_required_units"] = [
        "conduct independent sequential reconstruction of CORPUS-SRC-108 from CORPUS-WIT-108",
        "compare the reviewed 1997 CORPUS-WIT-103 item with the original 1948 journal printing when available",
        "compare the 1997 CORPUS-WIT-102 composite with separately reviewed 1965 and 1968 textual states",
        "conduct independent sequential reconstruction for the remaining fourteen writings",
        "acquire and reconstruct Talmon's reviewed work",
    ]
    dump(path, d)


def update_findings() -> None:
    path = "findings/index.yaml"
    d = load(path)
    d["identity"]["version"] = "1.5.0"
    d["revision_history"] = {
        "predecessor_version": "1.4.0",
        "predecessor_blob_sha": "820aacb74d7dbd340b75222a73d78eaa62b8f2db",
        "transformation": "SUBSTANTIVE_FORWARD_REVISION",
        "reason": "Register SPINOZA-TREATISE-STUDY-001 as FINDSET-012 and its jurisdiction-preserving Theologico-Political and Wise-versus-Vulgar syntheses as FINDSET-122 and FINDSET-123, preserving original-edition, noncorroboration, noncertification, and no-successor safeguards.",
    }
    by_id = {x["finding_set_id"]: x for x in d["finding_sets"]}
    additions = [
        {
            "finding_set_id": "FINDSET-012", "path": STUDY_PATH,
            "record_class": "SOURCE_SPECIFIC_STUDY", "record_role": "SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION",
            "source_bindings": [SRC], "problem_bindings": ["theologico-political", "wise-vs-vulgar"],
            "status": "COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS", "certification": "NOT_CERTIFIED",
            "derived_local_syntheses": ["FINDSET-122", "FINDSET-123"], "witness_id": WIT,
            "original_1948_journal_comparison": "PENDING", "independent_corroboration": "INCOMPLETE", "successor_effect": "NONE",
        },
        {
            "finding_set_id": "FINDSET-122", "path": TP_SYN,
            "record_class": "PROBLEM_LOCAL_SYNTHESIS", "record_role": "SOURCE_TO_PROBLEM_SYNTHESIS",
            "source_bindings": [SRC], "problem_bindings": ["theologico-political"],
            "adjacent_problem_reference": "wise-vs-vulgar", "derived_from": ["FINDSET-012"],
            "status": "PROVISIONAL_NOT_CERTIFIED", "certification": "NOT_CERTIFIED", "successor_effect": "NONE",
        },
        {
            "finding_set_id": "FINDSET-123", "path": WVG_SYN,
            "record_class": "PROBLEM_LOCAL_SYNTHESIS", "record_role": "SOURCE_TO_PROBLEM_SYNTHESIS",
            "source_bindings": [SRC], "problem_bindings": ["wise-vs-vulgar"],
            "theologico_political_reference": "theologico-political", "derived_from": ["FINDSET-012"],
            "status": "PROVISIONAL_NOT_CERTIFIED", "certification": "NOT_CERTIFIED", "successor_effect": "NONE",
        },
    ]
    for item in additions:
        if item["finding_set_id"] not in by_id:
            # keep source studies before problem-local syntheses, and new syntheses before migrations
            if item["record_class"] == "SOURCE_SPECIFIC_STUDY":
                pos = next(i for i,x in enumerate(d["finding_sets"]) if x["finding_set_id"].startswith("FINDSET-1" ) and int(x["finding_set_id"].split('-')[1]) >= 100)
            else:
                pos = next(i for i,x in enumerate(d["finding_sets"]) if x["finding_set_id"].startswith("FINDSET-2"))
            d["finding_sets"].insert(pos, item)
            by_id[item["finding_set_id"]] = item
    problems = ["nomos-vs-physis","philosophy-vs-poetry","theory-vs-practice","theologico-political","athens-vs-jerusalem","wise-vs-vulgar","ancients-vs-moderns"]
    by_problem = {p: [] for p in problems}
    classes = {"SOURCE_SPECIFIC_STUDY": [], "INTEGRATION_GOVERNANCE_RECORD": [], "PROBLEM_LOCAL_SYNTHESIS": [], "MIGRATION_TRANSACTION_LEDGER": [], "PRESERVED_FINDING_BASIS": []}
    direct = ["CORPUS-SRC-001","CORPUS-SRC-002","CORPUS-SRC-003","CORPUS-SRC-102","CORPUS-SRC-103","CORPUS-SRC-105","CORPUS-SRC-111"]
    by_source = {s: [] for s in direct}; by_source["CORPUS-SRC-101-119"] = []
    pred = {f"CORPUS-SRC-{i:03d}" for i in range(101,120)}
    separate = {"CORPUS-SRC-102","CORPUS-SRC-103","CORPUS-SRC-105","CORPUS-SRC-111"}
    for item in d["finding_sets"]:
        fid = item["finding_set_id"]
        for p in item.get("problem_bindings", []):
            if p in by_problem: by_problem[p].append(fid)
        rc = item.get("record_class")
        if rc in {"ACTIVE_PREDECESSOR_FINDING_BASIS","ACCEPTED_MIGRATION_SOURCE_FINDING_BASIS"}: classes["PRESERVED_FINDING_BASIS"].append(fid)
        elif rc in classes: classes[rc].append(fid)
        binds = set(item.get("source_bindings", []))
        for s in direct:
            if s in binds: by_source[s].append(fid)
        if binds & pred and not (len(binds)==1 and next(iter(binds)) in separate): by_source["CORPUS-SRC-101-119"].append(fid)
    d["indexes"] = {"by_problem": by_problem, "by_source": by_source, "by_record_class": classes}
    d["coverage"].update({
        "finding_sets_registered": 40,
        "source_specific_and_integration_records_registered": 12,
        "problem_syntheses_registered": 23,
        "current_problem_synthesis_tree_yaml_records_accounted_for": 23,
        "corpus_study_records_accounted_for": 12,
    })
    gap = next(x for x in d["findings_gaps"] if x["gap_id"] == "FINDINGS-GAP-003")
    gap["statement"] = "Five of the nineteen Theologico-Political writings now have complete provisional item studies; the remaining fourteen lack individual sequential studies."
    d["validation_rules"] = [x for x in d["validation_rules"] if not x.startswith("FINDSET-011 must derive only")]
    d["validation_rules"].append("FINDSET-011 must retain its three jurisdiction-preserving local syntheses and platform-reference limitations")
    d["validation_rules"].append("FINDSET-012 must derive only FINDSET-122 and FINDSET-123, preserve CORPUS-WIT-103 and pending 1948 comparison, and retain noncorroboration and no-successor safeguards")
    d["termination"]["next_required_units"] = [
        "conduct the remaining fourteen Theologico-Political independent sequential studies beginning with CORPUS-SRC-108",
        "compare the CORPUS-SRC-103 reviewed 1997 witness with the original 1948 journal printing when available",
        "compare the Preface to Spinoza's Critique of Religion 1997 composite with separately reviewed 1965 and 1968 textual states",
        "acquire and reconstruct Talmon's reviewed work",
        "expand source-specific and independent witness studies",
        "normalize proposition-level identifiers only where source records support reproducible extraction",
        "validate actual ministerial reports against source, method, hermeneutic, problem, corpus, and speech contracts",
        "preserve later corrections, dissent, and supersession through forward registry revision",
    ]
    dump(path, d)


def update_manifest() -> None:
    path = "manifest.yaml"; d = load(path)
    d["identity"]["version"] = "1.9.0"
    d["revision_history"] = {"predecessor_version":"1.8.0","predecessor_blob_sha":"b488f608a560cd8c1098ce3022d7061967d13e1a","reason":"Register SPINOZA-TREATISE-STUDY-001 as the fifth complete provisional Theologico-Political item study and synchronize corpus v1.13.0, findings v1.5.0, audit v2.7.0, mapping v1.9.0, process v1.11.0, and schedule v1.9.0 while preserving fourteen pending studies, original-edition limits, noncertification, predecessor authority, and the Sanctum repin block."}
    d["audit"]["version"] = "2.7.0"
    d["component_completion"]["theologico_political_item_level_source_statuses"] = "19_OF_19_IDENTITIES_19_OF_19_REVIEWED_ITEM_WITNESSES_5_OF_19_COMPLETE_PROVISIONAL_ITEM_STUDIES"
    d["corpus"]["registry_version"] = "1.13.0"
    s = d["corpus"]["theologico_political_item_level_statuses"]
    s["independent_sequential_study_count"] = 5
    s["remaining_without_independent_sequential_study"] = 14
    if STUDY not in s["completed_study_ids"]: s["completed_study_ids"].append(STUDY)
    s["rule"] = "All nineteen predecessor items have reviewed witnesses and five have complete provisional source studies. Witness and study completion remain distinct from independent corroboration, doctrinal certification, migration completion, successor activation, or repository completion."
    d["corpus"]["limitation"] = "All nineteen predecessor writings have bounded identities and reviewed item witnesses. Five have complete provisional sequential studies, including CORPUS-SRC-103 from the fingerprinted 1997 collected witness; fourteen still lack independent studies. Original-edition comparisons, independent witnesses, and source-text access remain incomplete."
    d["findings"]["registry_version"] = "1.5.0"
    d["findings"]["newly_registered"] = ["FINDSET-012","FINDSET-122","FINDSET-123"]
    dump(path, d)


def update_schedule() -> None:
    path = "history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml"; d=load(path)
    d["identity"]["version"]="1.9.0"
    d["revision_history"]={"predecessor_version":"1.8.0","predecessor_blob_sha":"432005d900258d2fc0eac1c76a655fb02ee77b08","reason":"Complete SPINOZA-TREATISE-STUDY-001 from CORPUS-WIT-103, advancing independent sequential study coverage to 5-of-19 and the next study unit to CORPUS-SRC-108 while preserving complete 19-of-19 witness coverage and all edition, corroboration, certification, migration, and successor limits."}
    d["status"]["independent_sequential_study_completion"]="INCOMPLETE_5_OF_19"
    item = next(x for g in d["priority_groups"] for x in g["items"] if x["source_id"]==SRC)
    item["study_id"] = STUDY; item["state"]="REVIEWED_WITNESS_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDY"; item["next_action"]="ORIGINAL_1948_JOURNAL_COMPARISON_AND_INDEPENDENT_SPINOZIST_WITNESS_EXPANSION"
    if STUDY not in d["selection"]["completed_study_ids"]: d["selection"]["completed_study_ids"].append(STUDY)
    d["selection"]["selection_state"]="NINETEEN_REVIEWED_ITEM_WITNESSES_FIVE_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDIES"
    d["selection"]["completed_units"]=["all nineteen predecessor source identities have reviewed witnesses","five source studies are complete provisional","fourteen witness-only sources remain pending independent sequential reconstruction","all original-edition and independent-corroboration limits remain explicit"]
    d["termination"]["independent_sequential_reconstruction"]="INCOMPLETE_5_OF_19"; d["termination"]["next_item_study"]="CORPUS-SRC-108"
    d["next_item_study_unit"]={"source_id":"CORPUS-SRC-108","title":"On the Interpretation of Genesis","action":"INDEPENDENT_SEQUENTIAL_RECONSTRUCTION_FROM_REGISTERED_WITNESS","prerequisite":"SATISFIED_CORPUS_WIT_108_REGISTERED","following_source":"CORPUS-SRC-113"}
    dump(path,d)


def update_process() -> None:
    path="history/production-plans/2026-07-27-ten-step-completion-process.yaml"; d=load(path)
    d["identity"]["version"]="1.11.0"; d["revision_history"]={"predecessor_version":"1.10.0","predecessor_blob_sha":"2f43687b7d4994ff216abb3d3cd64128c9aaefed","reason":"Complete SPINOZA-TREATISE-STUDY-001 as the fifth provisional Theologico-Political sequential reconstruction and advance the next study unit to CORPUS-SRC-108 while preserving 19-of-19 witness coverage and fourteen remaining studies."}
    next(x for x in d["steps"] if x["sequence"]==1)["current_version"]="2.7.0"; next(x for x in d["steps"] if x["sequence"]==2)["current_version"]="1.9.0"
    s7=next(x for x in d["steps"] if x["sequence"]==7); s7["completed"].append("How to Study Spinoza's Theologico-Political Treatise supplies distinct provisional syntheses to Theologico-Political and Wise-versus-Vulgar")
    s8=next(x for x in d["steps"] if x["sequence"]==8); s8["completed"].append("SPINOZA-TREATISE-STUDY-001 is complete provisional for CORPUS-WIT-103"); s8["remaining"][0]="conduct fourteen independent sequential item studies, beginning with CORPUS-SRC-108"
    s9=next(x for x in d["steps"] if x["sequence"]==9); s9["completed_in_current_sequence"]=["tests cover all nineteen Theologico-Political reviewed-witness registrations and distinguish the fourteen witness-only states from the five completed-study states","tests preserve qualified platform-reference, fingerprint, locator, scope, edition-comparison, noncertification, and no-successor safeguards","tests cover CORPUS-SRC-103 study completion, findings derivation, problem jurisdiction, and completion-language consistency"]
    d["current_production_unit"]={"step":8,"completed_subunit":{"title":"How to Study Spinoza's Theologico-Political Treatise independent sequential reconstruction","state":"COMPLETE_PROVISIONAL_PENDING_BRANCH_VALIDATION_AND_MERGE","source_id":SRC,"witness_id":WIT,"study_id":STUDY,"witness_coverage":"COMPLETE_19_OF_19","study_coverage":"INCOMPLETE_5_OF_19","non_effect":"Source-study completion does not supply independent corroboration, doctrine, certified migration, successor activation, predecessor displacement, or completed-interface readiness."},"next_subunit":{"title":"On the Interpretation of Genesis independent sequential reconstruction","source_id":"CORPUS-SRC-108","witness_id":"CORPUS-WIT-108","first_action":"Reconstruct printed pages 359-376 in textual order before comparing with the active predecessor.","following_source":"CORPUS-SRC-113"},"non_effects":["no source-text admission through registries","no doctrinal or migration certification","no successor activation or predecessor displacement","no Sanctum repin as a completed interface"]}
    dump(path,d)


def update_mapping() -> None:
    path="migrations/lean-operational-interface.yaml"; d=load(path)
    d["identity"]["version"]="1.9.0"; d["revision_history"]={"predecessor_version":"1.8.0","predecessor_blob_sha":"8cfbda404a0e553599f7308b97fbd9161681f3da","reason":"Synchronize SPINOZA-TREATISE-STUDY-001, corpus registry v1.13.0, findings v1.5.0, audit v2.7.0, process v1.11.0, and schedule v1.9.0 while preserving fourteen pending studies, noncorroboration, noncertification, predecessor authority, and repository incompleteness."}
    d["completion_audit"]["version"]="2.7.0"; d["production_process"]["completed_study_subunit"]="FIVE_OF_19_COMPLETE_PROVISIONAL_FOURTEEN_PENDING"
    c=d["mappings"]["corpus"]; c["interface"]["registry_version"]="1.13.0"; s=c["theologico_political_item_level_statuses"]; s["independent_sequential_study_count"]=5; s["remaining_without_independent_sequential_study"]=14; 
    if STUDY not in s["completed_study_ids"]: s["completed_study_ids"].append(STUDY)
    s["witness_only_source_ids"]=[x for x in s.get("witness_only_source_ids",[]) if x!=SRC]
    c["present_function"].append("validate SPINOZA-TREATISE-STUDY-001 as a complete provisional reconstruction with pending 1948 comparison and no successor effect")
    c["limit"]="Current-state exhaustiveness, nineteen reviewed item witnesses, and five complete provisional item studies do not create a complete corpus, supply independent corroboration, certify findings, or authorize migration and activation."
    f=d["mappings"]["findings"]; f["interface"]["registry_version"]="1.5.0"; f["newly_registered"]=[{"finding_set_id":"FINDSET-012","path":STUDY_PATH},{"finding_set_id":"FINDSET-122","path":TP_SYN,"derived_from":"FINDSET-012"},{"finding_set_id":"FINDSET-123","path":WVG_SYN,"derived_from":"FINDSET-012"}]
    dump(path,d)


def update_audit() -> None:
    path="audits/operational-completeness.yaml"; d=load(path)
    d["identity"]["version"]="2.7.0"; d["revision_history"]={"predecessor_version":"2.6.0","predecessor_blob_sha":"15bcf2271a372f88cfdf42f24c1337904cf44738","reason":"Complete SPINOZA-TREATISE-STUDY-001 from CORPUS-WIT-103, advance Theologico-Political study coverage to five of nineteen, and preserve fourteen pending studies, original-1948 comparison, noncorroboration, noncertification, predecessor authority, and the Sanctum repin block."}; d["basis"]["current_revision_scope"]="production/corpus-src-103-sequential-reconstruction"
    s=d["summary"]["theologico_political_item_level_status"]; s["independently_reconstructed_count_within_this_sequence"]=5; s["remaining_without_independent_sequential_study"]=14
    for key,val in (("completed_source_ids",SRC),("completed_witness_ids",WIT),("completed_study_ids",STUDY)):
        if val not in s[key]: s[key].append(val)
    s["witness_only_source_ids"]=[x for x in s["witness_only_source_ids"] if x!=SRC]; s["witness_only_witness_ids"]=[x for x in s["witness_only_witness_ids"] if x!=WIT]
    s["interpretation_limit"]="All nineteen predecessor items have reviewed witnesses and five completed studies are independent reconstructions relative to predecessor and collection-level synthesis. Fourteen witness registrations remain study-pending; none of the source studies is independent corroboration of represented traditions."
    d["summary"]["completed_operational_units"].extend(["SPINOZA-TREATISE-STUDY-001 complete provisional sequential reconstruction","CORPUS-STUDY-012 and FINDSET-012 typed registrations","FINDSET-122 and FINDSET-123 jurisdiction-preserving problem-local syntheses"])
    d["summary"]["remaining_major_deficiencies"]=[x for x in d["summary"]["remaining_major_deficiencies"] if "CORPUS-SRC-103 requires" not in x and not x.startswith("fifteen Theologico-Political")]
    d["summary"]["remaining_major_deficiencies"].insert(0,"fourteen Theologico-Political writings still require independent sequential item studies")
    for rec in d["records"]:
        if rec.get("path")=="studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/source-status.yaml":
            rec["present_function"]=["registers CORPUS-WIT-103 and SPINOZA-TREATISE-STUDY-001 as distinct documentary layers","records complete provisional reconstruction with incomplete independent corroboration","preserves original-1948, doctrine, migration, activation, and predecessor-displacement limits"]
            rec["remaining"]=["original 1948 journal comparison","independent source-tradition reconstruction and corroboration"]
        elif rec.get("path")=="corpus/index.yaml":
            rec["registry_version"]="1.13.0"; rec["present_function"]=["22 typed source entities","22 reviewed witnesses","22 source-status records","12 analytical and integration study records","all 52 YAML records in the studies tree accounted for","all 7 problem witness registries","19 Theologico-Political identities, 19 reviewed item witnesses, and 5 complete provisional item studies","7 positive corpus-gap records"]; rec["remaining"][0]="fourteen independent item studies"
        elif rec.get("path")=="findings/index.yaml":
            rec["registry_version"]="1.5.0"; rec["present_function"]=["40 typed finding sets","12 source-specific or integration records","23 problem-local syntheses","3 migration transaction ledgers","2 preserved finding bases","explicit derivation from FINDSET-012 to FINDSET-122 and FINDSET-123","source, problem, record-class, derivation, migration, and preservation indexes"]
        elif rec.get("path")=="corpus_registry.py": rec["present_function"]=["validates exact current studies-tree coverage and all typed counts","validates nineteen predecessor identities, aliases, scopes, and preserved-copy equality","validates CORPUS-WIT-102 as a completed qualified platform-reference study state","validates CORPUS-SRC-103 as a fingerprinted completed-study state with pending original-1948 comparison","validates complete-study states for CORPUS-SRC-105, CORPUS-SRC-109, and CORPUS-SRC-111","validates witness identity, locators, fingerprint or missing-byte safeguards, study binding, noncertification, and successor non-effect"]
        elif rec.get("path")=="findings_registry.py": rec["present_function"]=["validates typed finding sets and exact synthesis records","validates corpus-study exhaustiveness, derivations, indexes, source and problem bindings","validates Cohen, Talmon, Spinoza-Preface, and Spinoza-Treatise source-local jurisdiction and noncorroboration","preserves predecessor equality, noncertification, and no successor effect"]
        elif rec.get("path")=="manifest.yaml": rec["present_function"]=["registers corpus v1.13.0, findings v1.5.0, 19 Theologico-Political identities, 19 reviewed item witnesses, and 5 completed provisional item studies","preserves structural, semantic, runtime, migration, predecessor, and certification limits","blocks completed-interface Sanctum repinning"]
    d["records"].extend([
        {"path":STUDY_PATH,"classification":"SUBSTANTIVELY_RECONSTRUCTED","identity":STUDY,"present_function":["reconstructs printed pages 181-233 in ten ordered units","distinguishes interpretation from explanation and public teaching from controlled concealed reasoning","preserves Theologico-Political primary and Wise-versus-Vulgar secondary jurisdiction","retests the predecessor without promotion, certification, migration, activation, or displacement"],"remaining":["original 1948 journal comparison","independent Spinozist, biblical, medieval, classical, Christian, Jewish, and historical witnesses","later authorized proposition-level migration review"]},
        {"path":TP_SYN,"classification":"SUBSTANTIVELY_RECONSTRUCTED","identity":"TP-SPINOZA-TREATISE-001","present_function":["supplies the source-local Theologico-Political synthesis without predecessor displacement"],"remaining":["independent witness expansion and any later certified proposition-level migration"]},
        {"path":WVG_SYN,"classification":"SUBSTANTIVELY_RECONSTRUCTED","identity":"WVG-SPINOZA-TREATISE-001","present_function":["supplies the source-local audience and accommodation synthesis without mechanical inversion or claimant certification"],"remaining":["independent source-tradition reconstruction and later authorized migration review"]},
    ])
    d["production_order"]["completed_in_current_sequence"].append("SPINOZA-TREATISE-STUDY-001 with FINDSET-012, FINDSET-122, and FINDSET-123")
    d["production_order"]["next"]=["run complete structural and behavioral validation for the fifth Theologico-Political item study","conduct CORPUS-SRC-108 independent sequential reconstruction from printed pages 359-376","continue the remaining thirteen independent sequential reconstructions after CORPUS-SRC-108","expand independent source-tradition witnesses and original-edition comparisons","validate actual ministerial reports against the full contract stack"]
    dump(path,d)


def update_python_and_tests() -> None:
    p=ROOT/"corpus_registry.py"; text=p.read_text(encoding="utf-8")
    if STUDY_PATH not in text.split("REQUIRED_TOP_LEVEL")[0]:
        text=text.replace('    "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/reviewed-witness.yaml",\n', '    "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/reviewed-witness.yaml",\n    "'+STUDY_PATH+'",\n')
    block='''    "CORPUS-SRC-103": {\n        "status_id": "CORPUS-STATUS-103",\n        "witness_id": "CORPUS-WIT-103",\n        "study_id": "CORPUS-STUDY-012",\n        "internal_study_id": "SPINOZA-TREATISE-STUDY-001",\n        "study_path": "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/sequential-reconstruction.yaml",\n        "witness_record_path": "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/reviewed-witness.yaml",\n        "printed_page_range": {"start": 181, "end": 233},\n        "pdf_page_range_one_based": {"start": 200, "end": 252},\n        "reading_state": "COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS",\n        "platform_reference": False,\n    },\n'''
    marker='    "CORPUS-SRC-105": {'
    if block not in text: text=text.replace(marker, block+marker, 1)
    text=re.sub(r'    "CORPUS-SRC-103": \{\n        "status_id": "CORPUS-STATUS-103",.*?\n    \},\n    "CORPUS-SRC-104": \{', '    "CORPUS-SRC-104": {', text, count=1, flags=re.S)
    text=text.replace('identity.version must be 1.12.0','identity.version must be 1.13.0').replace('identity.get("version") != "1.12.0"','identity.get("version") != "1.13.0"')
    text=text.replace('"study records": (len(study_ids), 11)', '"study records": (len(study_ids), 12)')
    text=text.replace('"theologico_political_independent_item_studies_registered": 4', '"theologico_political_independent_item_studies_registered": 5')
    text=text.replace('!= "INCOMPLETE_4_OF_19"', '!= "INCOMPLETE_5_OF_19"').replace('must be INCOMPLETE_4_OF_19','must be INCOMPLETE_5_OF_19')
    p.write_text(text,encoding="utf-8")

    p=ROOT/"findings_registry.py"; text=p.read_text(encoding="utf-8")
    for line in [f'    "{TP_SYN}",\n',f'    "{WVG_SYN}",\n']:
        if line not in text: text=text.replace('    "problems/wise-vs-vulgar/synthesis/plato-apology.yaml",\n', line+'    "problems/wise-vs-vulgar/synthesis/plato-apology.yaml",\n',1)
    text=text.replace('    "CORPUS-SRC-102",\n    "CORPUS-SRC-105",','    "CORPUS-SRC-102",\n    "CORPUS-SRC-103",\n    "CORPUS-SRC-105",')
    text=text.replace('separately_indexed = {"CORPUS-SRC-102", "CORPUS-SRC-105", "CORPUS-SRC-111"}', 'separately_indexed = {"CORPUS-SRC-102", "CORPUS-SRC-103", "CORPUS-SRC-105", "CORPUS-SRC-111"}')
    contract='''    "FINDSET-012": {\n        "source_id": "CORPUS-SRC-103",\n        "local_syntheses": ["FINDSET-122", "FINDSET-123"],\n        "problem_bindings": {"FINDSET-122": "theologico-political", "FINDSET-123": "wise-vs-vulgar"},\n        "required_limits": {"witness_id": "CORPUS-WIT-103", "original_1948_journal_comparison": "PENDING", "independent_corroboration": "INCOMPLETE"},\n    },\n'''
    if contract not in text: text=text.replace('\n}\n\n\nclass FindingsRegistryError', '\n'+contract+'}\n\n\nclass FindingsRegistryError',1)
    text=text.replace('identity.version must be 1.4.0','identity.version must be 1.5.0').replace('identity.get("version") != "1.4.0"','identity.get("version") != "1.5.0"')
    text=text.replace('if len(finding_ids) != 37:', 'if len(finding_ids) != 40:').replace('expected 37 finding sets','expected 40 finding sets')
    p.write_text(text,encoding="utf-8")

    replace_text("tests/test_corpus_registry.py", {"1.12.0":"1.13.0","51":"52","study_records_registered\"], 11":"study_records_registered\"], 12","test_fifteen_tp_sources_have_witnesses_but_still_require_study":"test_fourteen_tp_sources_have_witnesses_but_still_require_study","self.assertEqual(len(sources), 15)":"self.assertEqual(len(sources), 14)","test_spinoza_treatise_witness_is_registered_without_claiming_study_completion":"test_spinoza_treatise_witness_and_study_are_registered","self.assertNotIn(\"study_records\", source)":"self.assertEqual(source[\"study_records\"], [\"CORPUS-STUDY-012\"])","REVIEWED_ITEM_WITNESS_REGISTERED_SEQUENTIAL_RECONSTRUCTION_REQUIRED":"REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION","status[\"status\"][\"independent_sequential_study\"], \"NOT_YET_COMPLETED\"":"status[\"status\"][\"independent_sequential_study\"], \"SPINOZA-TREATISE-STUDY-001\"","status[\"termination\"][\"study_state\"], \"INCOMPLETE\"":"status[\"termination\"][\"study_state\"], \"COMPLETE_PROVISIONAL\""})
    # Rewrite the specific 103 test cleanly to avoid broad replacement collisions.
    p=ROOT/"tests/test_corpus_registry.py"; text=p.read_text(encoding="utf-8")
    start=text.index('    def test_spinoza_treatise_witness_and_study_are_registered')
    end=text.index('    def test_spinoza_preface_platform_witness_and_study_are_registered', start)
    fn='''    def test_spinoza_treatise_witness_and_study_are_registered(self) -> None:\n        registry = corpus_registry.load_registry()\n        source = next(item for item in registry["source_entities"] if item["source_id"] == "CORPUS-SRC-103")\n        entry = next(item for item in registry["source_status_records"] if item["source_id"] == "CORPUS-SRC-103")\n        witness = next(item for item in registry["reviewed_witnesses"] if item["witness_id"] == "CORPUS-WIT-103")\n        study = next(item for item in registry["study_records"] if item["study_id"] == "CORPUS-STUDY-012")\n        status = corpus_registry.load_yaml(corpus_registry._resolve(entry["path"]))\n        study_record = corpus_registry.load_yaml(corpus_registry._resolve(study["path"]))\n        witness_record = corpus_registry.load_yaml(corpus_registry._resolve(witness["witness_record_path"]))\n        self.assertEqual(source["reviewed_witnesses"], ["CORPUS-WIT-103"])\n        self.assertEqual(source["study_records"], ["CORPUS-STUDY-012"])\n        self.assertEqual(witness["printed_page_range"], {"start": 181, "end": 233})\n        self.assertEqual(witness["pdf_page_range_one_based"], {"start": 200, "end": 252})\n        self.assertEqual(status["status"]["independent_sequential_study"], "SPINOZA-TREATISE-STUDY-001")\n        self.assertEqual(status["termination"]["study_state"], "COMPLETE_PROVISIONAL")\n        self.assertEqual(status["termination"]["original_edition_comparison"], "PENDING")\n        self.assertEqual(status["termination"]["certification"], "NOT_CERTIFIED")\n        self.assertEqual(status["termination"]["successor_effect"], "NONE")\n        self.assertEqual(study_record["identity"]["id"], "SPINOZA-TREATISE-STUDY-001")\n        self.assertEqual(study_record["termination"]["reading_state"], "COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS")\n        self.assertEqual(study_record["termination"]["successor_effect"], "NONE")\n        self.assertEqual(witness_record["termination"]["study_state"], "INCOMPLETE")\n\n'''
    p.write_text(text[:start]+fn+text[end:],encoding="utf-8")
    replace_text("tests/test_interface_consistency.py", {"nineteen_witness_four_study":"nineteen_witness_five_study","study_count\"], 4":"study_count\"], 5","sequence\"], 4":"sequence\"], 5","study\"], 4":"study\"], 5","study\"], 15":"study\"], 14","INCOMPLETE_4_OF_19":"INCOMPLETE_5_OF_19","spinoza_treatise_study_next":"spinoza_treatise_complete_genesis_study_next","\"SPINOZA-PREFACE-STUDY-001\"]":"\"SPINOZA-PREFACE-STUDY-001\", \"SPINOZA-TREATISE-STUDY-001\"]","next_item_study\"], \"CORPUS-SRC-103\"":"next_item_study\"], \"CORPUS-SRC-108\""})
    p=ROOT/"tests/test_interface_consistency.py"; text=p.read_text(encoding="utf-8"); text=text.replace('"FINDSET-011": [("FINDSET-119", "theologico-political"), ("FINDSET-120", "athens-vs-jerusalem"), ("FINDSET-121", "ancients-vs-moderns")],','"FINDSET-011": [("FINDSET-119", "theologico-political"), ("FINDSET-120", "athens-vs-jerusalem"), ("FINDSET-121", "ancients-vs-moderns")],\n            "FINDSET-012": [("FINDSET-122", "theologico-political"), ("FINDSET-123", "wise-vs-vulgar")],'); p.write_text(text,encoding="utf-8")
    replace_text("tests/test_pr21_talmon_completion.py", {"1.8.0":"1.9.0","2.6.0":"2.7.0","1.10.0":"1.11.0","1.12.0":"1.13.0","1.4.0":"1.5.0","study_count\"], 4":"study_count\"], 5","study\"], 15":"study\"], 14","\"SPINOZA-PREFACE-STUDY-001\"]":"\"SPINOZA-PREFACE-STUDY-001\", \"SPINOZA-TREATISE-STUDY-001\"]","next_item_study\"], \"CORPUS-SRC-103\"":"next_item_study\"], \"CORPUS-SRC-108\""})
    # Other historical tests assert the global study count string.
    for rel in ["tests/test_corpus_wit_102_platform_registration.py","tests/test_tp_witness_coverage_complete.py"]:
        replace_text(rel,{"INCOMPLETE_4_OF_19":"INCOMPLETE_5_OF_19"})


def main():
    update_corpus(); update_findings(); update_manifest(); update_schedule(); update_process(); update_mapping(); update_audit(); update_python_and_tests()
    print("Materialized CORPUS-SRC-103 complete provisional study integration.")

if __name__ == "__main__": main()
