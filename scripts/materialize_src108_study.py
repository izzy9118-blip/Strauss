#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from pprint import pformat
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = "CORPUS-SRC-108"
WIT = "CORPUS-WIT-108"
STUDY = "GENESIS-STUDY-001"
CORPUS_STUDY = "CORPUS-STUDY-013"
STUDY_PATH = "studies/theologico-political/on-the-interpretation-of-genesis/sequential-reconstruction.yaml"
TP_SYN = "problems/theologico-political/synthesis/on-the-interpretation-of-genesis.yaml"
AVJ_SYN = "problems/athens-vs-jerusalem/synthesis/on-the-interpretation-of-genesis.yaml"
NVP_SYN = "problems/nomos-vs-physis/synthesis/on-the-interpretation-of-genesis.yaml"


def load(path: str):
    with (ROOT / path).open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def dump(path: str, data) -> None:
    (ROOT / path).write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")


def uniq(values):
    out = []
    for value in values:
        if value not in out:
            out.append(value)
    return out


def dedupe_records(records):
    order, by_path = [], {}
    for record in records:
        key = record.get("path") if isinstance(record, dict) else None
        if key is None:
            order.append((None, record))
            continue
        if key not in by_path:
            order.append((key, None))
        by_path[key] = record
    result = []
    for key, raw in order:
        result.append(raw if key is None else by_path[key])
    return result


def update_corpus():
    path = "corpus/index.yaml"
    d = load(path)
    d["identity"]["version"] = "1.14.0"
    d["revision_history"] = {
        "predecessor_version": "1.13.0",
        "predecessor_blob_sha": "973271f34e1377eff4e818c0e10a95fc3d9485ac",
        "transformation": "SUBSTANTIVE_FORWARD_REVISION",
        "reason": "Register GENESIS-STUDY-001 as the sixth complete provisional Theologico-Political item study, correct the reviewed collection's publication provenance for the 1981 English text, and preserve pending textual-state comparison, noncorroboration, noncertification, predecessor authority, and no successor effect.",
    }
    source = next(x for x in d["source_entities"] if x["source_id"] == SRC)
    source["study_records"] = [CORPUS_STUDY]
    source["item_level_source_status"] = "REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION"
    source["study_status"] = "COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS"
    source["limits"] = [
        "reviewed witness is the fingerprinted 1997 SUNY collected text, not a separately reviewed 1981 L'Homme publication or 1957 typed lecture manuscript",
        "printed pages 359-376 correspond to one-based PDF pages 378-395",
        "Strauss's lecture body occupies printed pages 359-375; editorial notes begin on page 375 and continue through page 376",
        "GENESIS-STUDY-001 is source-local and not independent corroboration of Genesis, Greek philosophy, or represented traditions",
        "comparison with the 1981 English publication and the typed 1957 lecture manuscript remains pending",
    ]
    witness = next(x for x in d["reviewed_witnesses"] if x["witness_id"] == WIT)
    witness["publication_provenance_note"] = "Lecture delivered 25 January 1957; editor states the prepared English text first appeared posthumously in L'Homme 21, no. 1 (January-March 1981): 5-20, followed by a French translation"
    witness["original_edition_comparison"] = "PENDING"
    status_entry = next(x for x in d["source_status_records"] if x["source_id"] == SRC)
    status_entry["completion"] = "REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION"
    # Repair the prior SRC103 registry-entry lag while preserving the already-completed source record.
    src103_entry = next(x for x in d["source_status_records"] if x["source_id"] == "CORPUS-SRC-103")
    src103_entry["completion"] = "REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION"
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
    c["study_records_registered"] = 13
    c["theologico_political_independent_item_studies_registered"] = 6
    c["current_studies_tree_yaml_records_accounted_for"] = 53
    gap = next(x for x in d["corpus_gaps"] if x["gap_id"] == "CORPUS-GAP-003")
    gap["statement"] = "All nineteen predecessor writings have bounded source identities and reviewed item witnesses; CORPUS-SRC-102, CORPUS-SRC-103, CORPUS-SRC-105, CORPUS-SRC-108, CORPUS-SRC-109, and CORPUS-SRC-111 have complete provisional sequential studies, while the remaining thirteen lack independent item studies."
    rules = []
    for rule in d["validation_rules"]:
        if rule.startswith("all fifteen witness-only Theologico-Political sources") or rule.startswith("all fourteen witness-only Theologico-Political sources"):
            continue
        if "CORPUS-SRC-108" in rule and "completed" in rule.lower():
            continue
        rules.append(rule)
    rules.append("CORPUS-SRC-108 preserves fingerprinted reviewed-witness safeguards and complete provisional sequential reconstruction while earlier textual-state comparison remains pending")
    rules.append("all thirteen witness-only Theologico-Political sources preserve registered-witness, pending-study, edition-comparison, noncertification, and no-successor safeguards")
    d["validation_rules"] = uniq(rules)
    t = d["termination"]
    t["theologico_political_independent_study_state"] = "INCOMPLETE_6_OF_19"
    t["next_required_units"] = [
        "conduct independent sequential reconstruction of CORPUS-SRC-113 from CORPUS-WIT-113",
        "compare the reviewed 1997 CORPUS-WIT-108 item with the 1981 L'Homme English text and the 1957 typed lecture manuscript when lawful witnesses are available",
        "compare the reviewed 1997 CORPUS-WIT-103 item with the original 1948 journal printing when available",
        "conduct independent sequential reconstruction for the remaining thirteen writings",
        "expand independent biblical, Greek, medieval, modern, and reviewed-work witnesses",
    ]
    dump(path, d)


def rebuild_findings_indexes(d):
    problems = ["nomos-vs-physis", "philosophy-vs-poetry", "theory-vs-practice", "theologico-political", "athens-vs-jerusalem", "wise-vs-vulgar", "ancients-vs-moderns"]
    by_problem = {p: [] for p in problems}
    classes = {"SOURCE_SPECIFIC_STUDY": [], "INTEGRATION_GOVERNANCE_RECORD": [], "PROBLEM_LOCAL_SYNTHESIS": [], "MIGRATION_TRANSACTION_LEDGER": [], "PRESERVED_FINDING_BASIS": []}
    direct = ["CORPUS-SRC-001", "CORPUS-SRC-002", "CORPUS-SRC-003", "CORPUS-SRC-102", "CORPUS-SRC-103", "CORPUS-SRC-105", "CORPUS-SRC-108", "CORPUS-SRC-111"]
    by_source = {s: [] for s in direct}
    by_source["CORPUS-SRC-101-119"] = []
    pred = {f"CORPUS-SRC-{i:03d}" for i in range(101, 120)}
    separate = {"CORPUS-SRC-102", "CORPUS-SRC-103", "CORPUS-SRC-105", "CORPUS-SRC-108", "CORPUS-SRC-111"}
    for item in d["finding_sets"]:
        fid = item["finding_set_id"]
        for p in item.get("problem_bindings", []):
            if p in by_problem:
                by_problem[p].append(fid)
        rc = item.get("record_class")
        if rc in {"ACTIVE_PREDECESSOR_FINDING_BASIS", "ACCEPTED_MIGRATION_SOURCE_FINDING_BASIS"}:
            classes["PRESERVED_FINDING_BASIS"].append(fid)
        elif rc in classes:
            classes[rc].append(fid)
        binds = set(item.get("source_bindings", []))
        for s in direct:
            if s in binds:
                by_source[s].append(fid)
        if binds & pred and not (len(binds) == 1 and next(iter(binds)) in separate):
            by_source["CORPUS-SRC-101-119"].append(fid)
    d["indexes"] = {"by_problem": by_problem, "by_source": by_source, "by_record_class": classes}


def update_findings():
    path = "findings/index.yaml"
    d = load(path)
    d["identity"]["version"] = "1.6.0"
    d["revision_history"] = {
        "predecessor_version": "1.5.0",
        "predecessor_blob_sha": "bbd286d4f85b4779a056365cc9d6bc6e93721bc8",
        "transformation": "SUBSTANTIVE_FORWARD_REVISION",
        "reason": "Register GENESIS-STUDY-001 as FINDSET-013 and its jurisdiction-preserving Theologico-Political, Athens-versus-Jerusalem, and Nomos-versus-Physis syntheses as FINDSET-124 through FINDSET-126 while preserving textual-state, noncorroboration, noncertification, and no-successor safeguards.",
    }
    additions = [
        {"finding_set_id": "FINDSET-013", "path": STUDY_PATH, "record_class": "SOURCE_SPECIFIC_STUDY", "record_role": "SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION", "source_bindings": [SRC], "problem_bindings": ["theologico-political", "athens-vs-jerusalem", "nomos-vs-physis"], "status": "COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS", "certification": "NOT_CERTIFIED", "derived_local_syntheses": ["FINDSET-124", "FINDSET-125", "FINDSET-126"], "witness_id": WIT, "earlier_published_text_comparison": "PENDING", "independent_corroboration": "INCOMPLETE", "successor_effect": "NONE"},
        {"finding_set_id": "FINDSET-124", "path": TP_SYN, "record_class": "PROBLEM_LOCAL_SYNTHESIS", "record_role": "SOURCE_TO_PROBLEM_SYNTHESIS", "source_bindings": [SRC], "problem_bindings": ["theologico-political"], "adjacent_problem_references": ["athens-vs-jerusalem", "nomos-vs-physis"], "derived_from": ["FINDSET-013"], "status": "PROVISIONAL_NOT_CERTIFIED", "certification": "NOT_CERTIFIED", "successor_effect": "NONE"},
        {"finding_set_id": "FINDSET-125", "path": AVJ_SYN, "record_class": "PROBLEM_LOCAL_SYNTHESIS", "record_role": "SOURCE_TO_PROBLEM_SYNTHESIS", "source_bindings": [SRC], "problem_bindings": ["athens-vs-jerusalem"], "theologico_political_reference": "theologico-political", "derived_from": ["FINDSET-013"], "status": "PROVISIONAL_NOT_CERTIFIED", "certification": "NOT_CERTIFIED", "successor_effect": "NONE"},
        {"finding_set_id": "FINDSET-126", "path": NVP_SYN, "record_class": "PROBLEM_LOCAL_SYNTHESIS", "record_role": "SOURCE_TO_PROBLEM_SYNTHESIS", "source_bindings": [SRC], "problem_bindings": ["nomos-vs-physis"], "theologico_political_reference": "theologico-political", "derived_from": ["FINDSET-013"], "status": "PROVISIONAL_NOT_CERTIFIED", "certification": "NOT_CERTIFIED", "successor_effect": "NONE"},
    ]
    existing = {x["finding_set_id"] for x in d["finding_sets"]}
    for item in additions:
        if item["finding_set_id"] in existing:
            continue
        if item["record_class"] == "SOURCE_SPECIFIC_STUDY":
            pos = next(i for i, x in enumerate(d["finding_sets"]) if int(x["finding_set_id"].split("-")[1]) >= 100)
        else:
            pos = next(i for i, x in enumerate(d["finding_sets"]) if int(x["finding_set_id"].split("-")[1]) >= 200)
        d["finding_sets"].insert(pos, item)
        existing.add(item["finding_set_id"])
    rebuild_findings_indexes(d)
    d["coverage"].update({
        "finding_sets_registered": 44,
        "source_specific_and_integration_records_registered": 13,
        "problem_syntheses_registered": 26,
        "current_problem_synthesis_tree_yaml_records_accounted_for": 26,
        "corpus_study_records_accounted_for": 13,
    })
    gap = next(x for x in d["findings_gaps"] if x["gap_id"] == "FINDINGS-GAP-003")
    gap["statement"] = "Six of the nineteen Theologico-Political writings now have complete provisional item studies; the remaining thirteen lack individual sequential studies."
    rules = [x for x in d["validation_rules"] if not x.startswith("FINDSET-013 must")]
    rules.append("FINDSET-013 must derive only FINDSET-124 through FINDSET-126, preserve CORPUS-WIT-108 and pending earlier-text comparison, and retain noncorroboration and no-successor safeguards")
    d["validation_rules"] = uniq(rules)
    d["termination"]["next_required_units"] = [
        "conduct the remaining thirteen Theologico-Political independent sequential studies beginning with CORPUS-SRC-113",
        "compare the CORPUS-SRC-108 reviewed 1997 witness with the 1981 English text and 1957 typed lecture manuscript when lawful witnesses are available",
        "expand independent biblical, Greek, medieval, modern, and reviewed-work witness studies",
        "normalize proposition-level identifiers only where source records support reproducible extraction",
        "preserve later corrections, dissent, and supersession through forward registry revision",
    ]
    dump(path, d)


def update_manifest():
    path = "manifest.yaml"
    d = load(path)
    d["identity"]["version"] = "1.10.0"
    d["revision_history"] = {"predecessor_version": "1.9.0", "predecessor_blob_sha": "17c3d070d98b8ba08a9b5fff3ab1964018c13229", "reason": "Register GENESIS-STUDY-001 as the sixth complete provisional Theologico-Political item study and synchronize corpus v1.14.0, findings v1.6.0, audit v2.8.0, mapping v1.10.0, process v1.12.0, and schedule v1.10.0 while preserving thirteen pending studies, textual-state limits, noncertification, predecessor authority, and the Sanctum repin block."}
    d["audit"]["version"] = "2.8.0"
    d["component_completion"]["theologico_political_item_level_source_statuses"] = "19_OF_19_IDENTITIES_19_OF_19_REVIEWED_ITEM_WITNESSES_6_OF_19_COMPLETE_PROVISIONAL_ITEM_STUDIES"
    d["corpus"]["registry_version"] = "1.14.0"
    s = d["corpus"]["theologico_political_item_level_statuses"]
    s["independent_sequential_study_count"] = 6
    s["remaining_without_independent_sequential_study"] = 13
    s["completed_study_ids"] = uniq(s.get("completed_study_ids", []) + [STUDY])
    s["rule"] = "All nineteen predecessor items have reviewed witnesses and six have complete provisional source studies. Witness and study completion remain distinct from independent corroboration, doctrinal certification, migration completion, successor activation, or repository completion."
    d["corpus"]["limitation"] = "All nineteen predecessor writings have bounded identities and reviewed item witnesses. Six have complete provisional sequential studies, including CORPUS-SRC-108 from the fingerprinted 1997 collected witness; thirteen still lack independent studies. Earlier textual-state comparisons, independent witnesses, and source-text access remain incomplete."
    d["findings"]["registry_version"] = "1.6.0"
    d["findings"]["newly_registered"] = ["FINDSET-013", "FINDSET-124", "FINDSET-125", "FINDSET-126"]
    dump(path, d)


def update_schedule():
    path = "history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml"
    d = load(path)
    d["identity"]["version"] = "1.10.0"
    d["revision_history"] = {"predecessor_version": "1.9.0", "predecessor_blob_sha": "bfef8527585a7e6c87f33b519717135bb2b08ccd", "reason": "Complete GENESIS-STUDY-001 from CORPUS-WIT-108, advancing independent sequential study coverage to 6-of-19 and the next study unit to CORPUS-SRC-113 while preserving complete 19-of-19 witness coverage and all textual-state, corroboration, certification, migration, and successor limits."}
    d["status"]["independent_sequential_study_completion"] = "INCOMPLETE_6_OF_19"
    item = next(x for g in d["priority_groups"] for x in g["items"] if x["source_id"] == SRC)
    item["study_id"] = STUDY
    item["state"] = "REVIEWED_WITNESS_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDY"
    item["next_action"] = "1981_LHOMME_AND_1957_MANUSCRIPT_COMPARISON_AND_INDEPENDENT_BIBLICAL_GREEK_WITNESS_EXPANSION"
    d["selection"]["completed_study_ids"] = uniq(d["selection"].get("completed_study_ids", []) + [STUDY])
    d["selection"]["selection_state"] = "NINETEEN_REVIEWED_ITEM_WITNESSES_SIX_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDIES"
    d["selection"]["completed_units"] = ["all nineteen predecessor source identities have reviewed witnesses", "six source studies are complete provisional", "thirteen witness-only sources remain pending independent sequential reconstruction", "all original or earlier textual-state and independent-corroboration limits remain explicit"]
    d["termination"]["independent_sequential_reconstruction"] = "INCOMPLETE_6_OF_19"
    d["termination"]["next_item_study"] = "CORPUS-SRC-113"
    d["next_item_study_unit"] = {"source_id": "CORPUS-SRC-113", "title": "Introduction to Persecution and the Art of Writing", "action": "INDEPENDENT_SEQUENTIAL_RECONSTRUCTION_FROM_REGISTERED_WITNESS", "prerequisite": "SATISFIED_CORPUS_WIT_113_REGISTERED", "following_source": "CORPUS-SRC-116"}
    dump(path, d)


def update_process():
    path = "history/production-plans/2026-07-27-ten-step-completion-process.yaml"
    d = load(path)
    d["identity"]["version"] = "1.12.0"
    d["revision_history"] = {"predecessor_version": "1.11.0", "predecessor_blob_sha": "CURRENT_MAIN_PREDECESSOR_PRESERVED_BY_GIT", "reason": "Complete GENESIS-STUDY-001 as the sixth provisional Theologico-Political sequential reconstruction and advance the next study unit to CORPUS-SRC-113 while preserving 19-of-19 witness coverage and thirteen remaining studies."}
    for step in d["steps"]:
        if step["sequence"] == 1:
            step["current_version"] = "2.8.0"
        elif step["sequence"] == 2:
            step["current_version"] = "1.10.0"
        elif step["sequence"] == 7:
            step["completed"] = uniq(step.get("completed", []) + ["On the Interpretation of Genesis supplies distinct provisional syntheses to Theologico-Political, Athens-versus-Jerusalem, and Nomos-versus-Physis"])
        elif step["sequence"] == 8:
            step["completed"] = uniq(step.get("completed", []) + ["GENESIS-STUDY-001 is complete provisional for CORPUS-WIT-108"])
            step["remaining"] = ["conduct thirteen independent sequential item studies, beginning with CORPUS-SRC-113"] + [x for x in step.get("remaining", [])[1:]]
    d["current_production_unit"] = {"step": 8, "completed_subunit": {"title": "On the Interpretation of Genesis independent sequential reconstruction", "state": "COMPLETE_PROVISIONAL_PENDING_BRANCH_VALIDATION_AND_MERGE", "source_id": SRC, "witness_id": WIT, "study_id": STUDY, "witness_coverage": "COMPLETE_19_OF_19", "study_coverage": "INCOMPLETE_6_OF_19", "non_effect": "Source-study completion does not supply independent corroboration, doctrine, certified migration, successor activation, predecessor displacement, or completed-interface readiness."}, "next_subunit": {"title": "Introduction to Persecution and the Art of Writing independent sequential reconstruction", "source_id": "CORPUS-SRC-113", "witness_id": "CORPUS-WIT-113", "first_action": "Reconstruct printed pages 417-429 in textual order before comparing with the active predecessor.", "following_source": "CORPUS-SRC-116"}, "non_effects": ["no source-text admission through registries", "no doctrinal or migration certification", "no successor activation or predecessor displacement", "no Sanctum repin as a completed interface"]}
    dump(path, d)


def update_mapping():
    path = "migrations/lean-operational-interface.yaml"
    d = load(path)
    d["identity"]["version"] = "1.10.0"
    d["revision_history"] = {"predecessor_version": "1.9.0", "predecessor_blob_sha": "598e358d8b2f1d4f15845fa8e4bca320540ad10a", "reason": "Synchronize GENESIS-STUDY-001, corpus registry v1.14.0, findings v1.6.0, audit v2.8.0, process v1.12.0, and schedule v1.10.0 while preserving thirteen pending studies, noncorroboration, noncertification, predecessor authority, and repository incompleteness."}
    d["completion_audit"]["version"] = "2.8.0"
    d["production_process"]["completed_study_subunit"] = "SIX_OF_19_COMPLETE_PROVISIONAL_THIRTEEN_PENDING"
    c = d["mappings"]["corpus"]
    c["interface"]["registry_version"] = "1.14.0"
    s = c["theologico_political_item_level_statuses"]
    s["independent_sequential_study_count"] = 6
    s["remaining_without_independent_sequential_study"] = 13
    s["completed_study_ids"] = uniq(s.get("completed_study_ids", []) + [STUDY])
    s["witness_only_source_ids"] = [x for x in s.get("witness_only_source_ids", []) if x != SRC]
    c["present_function"] = uniq(c.get("present_function", []) + ["validate GENESIS-STUDY-001 as a complete provisional reconstruction with pending 1981 and manuscript comparison and no successor effect"])
    c["limit"] = "Current-state exhaustiveness, nineteen reviewed item witnesses, and six complete provisional item studies do not create a complete corpus, supply independent corroboration, certify findings, or authorize migration and activation."
    f = d["mappings"]["findings"]
    f["interface"]["registry_version"] = "1.6.0"
    f["newly_registered"] = [{"finding_set_id": "FINDSET-013", "path": STUDY_PATH}, {"finding_set_id": "FINDSET-124", "path": TP_SYN, "derived_from": "FINDSET-013"}, {"finding_set_id": "FINDSET-125", "path": AVJ_SYN, "derived_from": "FINDSET-013"}, {"finding_set_id": "FINDSET-126", "path": NVP_SYN, "derived_from": "FINDSET-013"}]
    dump(path, d)


def update_audit():
    path = "audits/operational-completeness.yaml"
    d = load(path)
    d["identity"]["version"] = "2.8.0"
    d["revision_history"] = {"predecessor_version": "2.7.0", "predecessor_blob_sha": "1873da932b5302b9f2e4eb06bdcc037f93d849a3", "reason": "Complete GENESIS-STUDY-001 from CORPUS-WIT-108, advance Theologico-Political study coverage to six of nineteen, repair duplicate audit entries from the prior materialization, and preserve thirteen pending studies, textual-state comparison, noncorroboration, noncertification, predecessor authority, and the Sanctum repin block."}
    d["basis"]["current_revision_scope"] = "production/corpus-src-108-sequential-reconstruction"
    summary = d["summary"]
    summary["completed_operational_units"] = uniq(summary.get("completed_operational_units", []))
    summary["completed_operational_units"] = uniq(summary["completed_operational_units"] + ["GENESIS-STUDY-001 complete provisional sequential reconstruction", "CORPUS-STUDY-013 and FINDSET-013 typed registrations", "FINDSET-124 through FINDSET-126 jurisdiction-preserving problem-local syntheses"])
    s = summary["theologico_political_item_level_status"]
    s["independently_reconstructed_count_within_this_sequence"] = 6
    s["remaining_without_independent_sequential_study"] = 13
    s["completed_source_ids"] = uniq(s.get("completed_source_ids", []) + [SRC])
    s["completed_witness_ids"] = uniq(s.get("completed_witness_ids", []) + [WIT])
    s["completed_study_ids"] = uniq(s.get("completed_study_ids", []) + [STUDY])
    s["witness_only_source_ids"] = [x for x in uniq(s.get("witness_only_source_ids", [])) if x != SRC]
    s["witness_only_witness_ids"] = [x for x in uniq(s.get("witness_only_witness_ids", [])) if x != WIT]
    s["interpretation_limit"] = "All nineteen predecessor items have reviewed witnesses and six completed studies are independent reconstructions relative to predecessor and collection-level synthesis. Thirteen witness registrations remain study-pending; none of the source studies is independent corroboration of represented traditions."
    deficiencies = [x for x in uniq(summary.get("remaining_major_deficiencies", [])) if not re.match(r"^(fourteen|thirteen|fifteen) Theologico-Political writings", x) and "CORPUS-SRC-108 requires" not in x]
    summary["remaining_major_deficiencies"] = ["thirteen Theologico-Political writings still require independent sequential item studies"] + deficiencies
    d["records"] = dedupe_records(d.get("records", []))
    def upsert(path_value, record):
        for i, existing in enumerate(d["records"]):
            if existing.get("path") == path_value:
                d["records"][i] = record
                return
        d["records"].append(record)
    upsert("studies/theologico-political/on-the-interpretation-of-genesis/source-status.yaml", {"path": "studies/theologico-political/on-the-interpretation-of-genesis/source-status.yaml", "classification": "SUBSTANTIVELY_RECONSTRUCTED", "present_function": ["registers CORPUS-WIT-108 and GENESIS-STUDY-001 as distinct documentary layers", "records complete provisional reconstruction and corrected 1957/1981 provenance with incomplete independent corroboration", "preserves textual-state, doctrine, migration, activation, and predecessor-displacement limits"], "remaining": ["separate 1981 English-text comparison", "typed 1957 lecture-manuscript comparison if available", "independent biblical and Greek source-tradition reconstruction"]})
    upsert(STUDY_PATH, {"path": STUDY_PATH, "classification": "SUBSTANTIVELY_RECONSTRUCTED", "identity": STUDY, "present_function": ["reconstructs printed pages 359-376 in eight ordered units while separating Strauss's lecture from editorial notes", "distinguishes natural cosmological articulation from the revelatory assertion of createdness", "reconstructs the Bible-philosophy alternative and its different literary forms", "preserves Theologico-Political primary plus Athens-versus-Jerusalem and Nomos-versus-Physis secondary jurisdictions"], "remaining": ["separate 1981 and 1957 textual-state comparison", "independent biblical, Greek, Hegelian, and historical witness reconstruction", "later authorized proposition-level migration review"]})
    upsert(TP_SYN, {"path": TP_SYN, "classification": "SUBSTANTIVELY_RECONSTRUCTED", "identity": "TP-GENESIS-001", "present_function": ["supplies the source-local Theologico-Political synthesis without predecessor displacement"], "remaining": ["independent witness expansion and any later certified proposition-level migration"]})
    upsert(AVJ_SYN, {"path": AVJ_SYN, "classification": "SUBSTANTIVELY_RECONSTRUCTED", "identity": "AVJ-GENESIS-001", "present_function": ["supplies the source-local Bible-Greek alternative without certifying either side or harmonizing them"], "remaining": ["independent biblical and Greek witness reconstruction"]})
    upsert(NVP_SYN, {"path": NVP_SYN, "classification": "SUBSTANTIVELY_RECONSTRUCTED", "identity": "NVP-GENESIS-001", "present_function": ["supplies the source-local command, freedom, responsibility, and autonomous-knowledge synthesis without reducing nomos to convention or physis to doctrine"], "remaining": ["independent biblical, natural, and philosophical witness reconstruction"]})
    for record in d["records"]:
        if record.get("path") == "corpus/index.yaml":
            record["registry_version"] = "1.14.0"
            record["present_function"] = ["22 typed source entities", "22 reviewed witnesses", "22 source-status records", "13 analytical and integration study records", "all 53 YAML records in the studies tree accounted for", "all 7 problem witness registries", "19 Theologico-Political identities, 19 reviewed item witnesses, and 6 complete provisional item studies", "7 positive corpus-gap records"]
            record["remaining"] = ["thirteen independent item studies", "complete Strauss bibliography and edition-specific comparisons", "broader independent classical, biblical, medieval, Spinozist, Cohenian, Kantian, and modern corpora", "source-text admission and runtime source access remain separate"]
        elif record.get("path") == "findings/index.yaml":
            record["registry_version"] = "1.6.0"
            record["present_function"] = ["44 typed finding sets", "13 source-specific or integration records", "26 problem-local syntheses", "3 migration transaction ledgers", "2 preserved finding bases", "explicit derivation from FINDSET-013 to FINDSET-124 through FINDSET-126", "source, problem, record-class, derivation, migration, and preservation indexes"]
        elif record.get("path") == "manifest.yaml":
            record["present_function"] = ["registers corpus v1.14.0, findings v1.6.0, 19 Theologico-Political identities, 19 reviewed item witnesses, and 6 completed provisional item studies", "preserves structural, semantic, runtime, migration, predecessor, and certification limits", "blocks completed-interface Sanctum repinning"]
    po = d["production_order"]
    po["completed_in_current_sequence"] = uniq(po.get("completed_in_current_sequence", []) + ["GENESIS-STUDY-001 with FINDSET-013 and FINDSET-124 through FINDSET-126"])
    po["next"] = ["run complete structural and behavioral validation for the sixth Theologico-Political item study", "conduct CORPUS-SRC-113 independent sequential reconstruction from printed pages 417-429", "continue the remaining twelve independent sequential reconstructions after CORPUS-SRC-113", "expand independent source-tradition witnesses and earlier textual-state comparisons", "validate actual ministerial reports against the full contract stack"]
    dump(path, d)


def update_python():
    # corpus_registry.py: rebuild the explicit complete and witness-only state tables from the typed registry.
    path = ROOT / "corpus_registry.py"
    text = path.read_text(encoding="utf-8")
    complete = {
        "CORPUS-SRC-102": {"status_id": "CORPUS-STATUS-102", "witness_id": "CORPUS-WIT-102", "study_id": "CORPUS-STUDY-011", "internal_study_id": "SPINOZA-PREFACE-STUDY-001", "study_path": "studies/theologico-political/preface-to-spinozas-critique-of-religion/sequential-reconstruction.yaml", "witness_record_path": "studies/theologico-political/preface-to-spinozas-critique-of-religion/reviewed-witness.yaml", "printed_page_range": {"start": 137, "end": 180}, "pdf_page_range_one_based": "PENDING_DIRECT_OFFSET_VERIFICATION", "reading_state": "COMPLETE_FOR_QUALIFIED_1997_PLATFORM_REFERENCE_WITNESS", "platform_reference": True, "platform_object_identifier": "file_0000000073c081fd9fb65f9ea7552cde"},
        "CORPUS-SRC-103": {"status_id": "CORPUS-STATUS-103", "witness_id": "CORPUS-WIT-103", "study_id": "CORPUS-STUDY-012", "internal_study_id": "SPINOZA-TREATISE-STUDY-001", "study_path": "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/sequential-reconstruction.yaml", "witness_record_path": "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/reviewed-witness.yaml", "printed_page_range": {"start": 181, "end": 233}, "pdf_page_range_one_based": {"start": 200, "end": 252}, "reading_state": "COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS", "platform_reference": False},
        "CORPUS-SRC-105": {"status_id": "CORPUS-STATUS-105", "witness_id": "CORPUS-WIT-105", "study_id": "CORPUS-STUDY-009", "internal_study_id": "COHEN-STUDY-001", "study_path": "studies/theologico-political/introductory-essay-hermann-cohen-religion-of-reason/sequential-reconstruction.yaml", "witness_record_path": "studies/theologico-political/introductory-essay-hermann-cohen-religion-of-reason/reviewed-witness.yaml", "printed_page_range": {"start": 233, "end": 247}, "pdf_page_range_one_based": {"start": 237, "end": 251}, "reading_state": "COMPLETE_FOR_REVIEWED_1983_COLLECTED_WITNESS", "platform_reference": False},
        "CORPUS-SRC-108": {"status_id": "CORPUS-STATUS-108", "witness_id": "CORPUS-WIT-108", "study_id": "CORPUS-STUDY-013", "internal_study_id": "GENESIS-STUDY-001", "study_path": STUDY_PATH, "witness_record_path": "studies/theologico-political/on-the-interpretation-of-genesis/reviewed-witness.yaml", "printed_page_range": {"start": 359, "end": 376}, "pdf_page_range_one_based": {"start": 378, "end": 395}, "reading_state": "COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS", "platform_reference": False},
        "CORPUS-SRC-109": {"status_id": "CORPUS-STATUS-109", "witness_id": "CORPUS-WIT-109", "study_id": "CORPUS-STUDY-008", "internal_study_id": "JA-STUDY-001", "study_path": "studies/theologico-political/jerusalem-and-athens/sequential-reconstruction.yaml", "witness_record_path": None, "printed_page_range": {"start": 147, "end": 173}, "pdf_page_range_one_based": {"start": 151, "end": 177}, "reading_state": "COMPLETE_FOR_REVIEWED_1983_COLLECTED_WITNESS", "platform_reference": False},
        "CORPUS-SRC-111": {"status_id": "CORPUS-STATUS-111", "witness_id": "CORPUS-WIT-111", "study_id": "CORPUS-STUDY-010", "internal_study_id": "TALMON-STUDY-001", "study_path": "studies/theologico-political/review-talmon-nature-of-jewish-history/sequential-reconstruction.yaml", "witness_record_path": "studies/theologico-political/review-talmon-nature-of-jewish-history/reviewed-witness.yaml", "printed_page_range": {"start": 232, "end": 232}, "pdf_page_range_one_based": {"start": 236, "end": 236}, "reading_state": "COMPLETE_FOR_REVIEWED_1983_COLLECTED_WITNESS", "platform_reference": False},
    }
    registry = load("corpus/index.yaml")
    witnesses = {x["source_id"]: x for x in registry["reviewed_witnesses"]}
    witness_only = {}
    for n in range(101, 120):
        sid = f"CORPUS-SRC-{n:03d}"
        if sid in complete:
            continue
        w = witnesses[sid]
        witness_only[sid] = {"status_id": f"CORPUS-STATUS-{n:03d}", "witness_id": f"CORPUS-WIT-{n:03d}", "witness_record_path": w["witness_record_path"], "printed_page_range": w["printed_page_range"], "pdf_page_range_one_based": w["pdf_page_range_one_based"], "container_sha256": w["container_sha256"], "container_file_size_bytes": w["container_file_size_bytes"], "container_page_count": w["container_page_count"]}
    region = "COMPLETE_TP_ITEMS: dict[str, dict[str, Any]] = " + pformat(complete, width=110, sort_dicts=False) + "\n\nWITNESS_ONLY_TP_ITEMS: dict[str, dict[str, Any]] = " + pformat(witness_only, width=110, sort_dicts=False) + "\n\n\n"
    text, count = re.subn(r"COMPLETE_TP_ITEMS: dict\[str, dict\[str, Any\]\] = \{.*?\n\nclass CorpusRegistryError", region + "class CorpusRegistryError", text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit("cannot replace corpus registry state tables")
    text = text.replace('identity.get("version") != "1.13.0"', 'identity.get("version") != "1.14.0"').replace('identity.version must be 1.13.0', 'identity.version must be 1.14.0')
    text = text.replace('"study records": (len(study_ids), 12)', '"study records": (len(study_ids), 13)')
    text = text.replace('"theologico_political_independent_item_studies_registered": 5', '"theologico_political_independent_item_studies_registered": 6')
    text = text.replace('!= "INCOMPLETE_5_OF_19"', '!= "INCOMPLETE_6_OF_19"').replace('must be INCOMPLETE_5_OF_19', 'must be INCOMPLETE_6_OF_19')
    path.write_text(text, encoding="utf-8")

    path = ROOT / "findings_registry.py"
    text = path.read_text(encoding="utf-8")
    for synthesis_path in [TP_SYN, AVJ_SYN, NVP_SYN]:
        literal = f'    "{synthesis_path}",\n'
        if literal not in text:
            text = text.replace('EXPECTED_TRANSACTION_PATHS = {', literal + '}\n\nEXPECTED_TRANSACTION_PATHS = {', 1) if False else text
    # Replace the whole expected synthesis set safely.
    actual_syntheses = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "problems").glob("*/synthesis/*.yaml") if p.is_file())
    set_text = "EXPECTED_SYNTHESIS_PATHS = {\n" + "".join(f'    "{p}",\n' for p in actual_syntheses) + "}\n\n"
    text, count = re.subn(r"EXPECTED_SYNTHESIS_PATHS = \{.*?\n\}\n\n", set_text, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit("cannot replace expected synthesis set")
    text = text.replace('    "CORPUS-SRC-105",\n    "CORPUS-SRC-111",', '    "CORPUS-SRC-105",\n    "CORPUS-SRC-108",\n    "CORPUS-SRC-111",')
    text = text.replace('separately_indexed = {"CORPUS-SRC-102", "CORPUS-SRC-103", "CORPUS-SRC-105", "CORPUS-SRC-111"}', 'separately_indexed = {"CORPUS-SRC-102", "CORPUS-SRC-103", "CORPUS-SRC-105", "CORPUS-SRC-108", "CORPUS-SRC-111"}')
    contract = '''    "FINDSET-013": {\n        "source_id": "CORPUS-SRC-108",\n        "local_syntheses": ["FINDSET-124", "FINDSET-125", "FINDSET-126"],\n        "problem_bindings": {"FINDSET-124": "theologico-political", "FINDSET-125": "athens-vs-jerusalem", "FINDSET-126": "nomos-vs-physis"},\n        "required_limits": {"witness_id": "CORPUS-WIT-108", "earlier_published_text_comparison": "PENDING", "independent_corroboration": "INCOMPLETE"},\n    },\n'''
    if '"FINDSET-013": {' not in text:
        text = text.replace('\n}\n\n\nclass FindingsRegistryError', '\n' + contract + '}\n\n\nclass FindingsRegistryError', 1)
    text = text.replace('identity.get("version") != "1.5.0"', 'identity.get("version") != "1.6.0"').replace('identity.version must be 1.5.0', 'identity.version must be 1.6.0')
    text = text.replace('if len(finding_ids) != 40:', 'if len(finding_ids) != 44:').replace('expected 40 finding sets', 'expected 44 finding sets')
    path.write_text(text, encoding="utf-8")


def update_tests():
    def replace(path, replacements):
        p = ROOT / path
        text = p.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        p.write_text(text, encoding="utf-8")
    replace("tests/test_corpus_registry.py", {"1.13.0": "1.14.0", "52,": "53,", 'study_records_registered"], 12': 'study_records_registered"], 13', "test_fourteen_tp_sources_have_witnesses_but_still_require_study": "test_thirteen_tp_sources_have_witnesses_but_still_require_study", "self.assertEqual(len(sources), 14)": "self.assertEqual(len(sources), 13)"})
    p = ROOT / "tests/test_corpus_registry.py"
    text = p.read_text(encoding="utf-8")
    anchor = '    def test_spinoza_preface_platform_witness_and_study_are_registered(self) -> None:\n'
    if 'def test_genesis_witness_and_study_are_registered' not in text:
        block = '''    def test_genesis_witness_and_study_are_registered(self) -> None:\n        registry = corpus_registry.load_registry()\n        source = next(item for item in registry["source_entities"] if item["source_id"] == "CORPUS-SRC-108")\n        entry = next(item for item in registry["source_status_records"] if item["source_id"] == "CORPUS-SRC-108")\n        witness = next(item for item in registry["reviewed_witnesses"] if item["witness_id"] == "CORPUS-WIT-108")\n        study = next(item for item in registry["study_records"] if item["study_id"] == "CORPUS-STUDY-013")\n        status = corpus_registry.load_yaml(corpus_registry._resolve(entry["path"]))\n        study_record = corpus_registry.load_yaml(corpus_registry._resolve(study["path"]))\n        witness_record = corpus_registry.load_yaml(corpus_registry._resolve(witness["witness_record_path"]))\n        self.assertEqual(source["study_records"], ["CORPUS-STUDY-013"])\n        self.assertEqual(witness["printed_page_range"], {"start": 359, "end": 376})\n        self.assertEqual(witness["pdf_page_range_one_based"], {"start": 378, "end": 395})\n        self.assertEqual(status["status"]["independent_sequential_study"], "GENESIS-STUDY-001")\n        self.assertEqual(status["termination"]["study_state"], "COMPLETE_PROVISIONAL")\n        self.assertEqual(status["termination"]["earlier_published_text_comparison"], "PENDING")\n        self.assertEqual(study_record["identity"]["id"], "GENESIS-STUDY-001")\n        self.assertEqual(study_record["termination"]["reading_state"], "COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS")\n        self.assertEqual(study_record["termination"]["successor_effect"], "NONE")\n        self.assertEqual(witness_record["termination"]["study_state"], "INCOMPLETE")\n\n'''
        text = text.replace(anchor, block + anchor)
    p.write_text(text, encoding="utf-8")
    replace("tests/test_findings_registry.py", {"1.5.0": "1.6.0", "len(finding_ids), 40": "len(finding_ids), 44", "len(registered), 23": "len(registered), 26", "len(registered), 12": "len(registered), 13"})
    p = ROOT / "tests/test_findings_registry.py"
    text = p.read_text(encoding="utf-8")
    anchor = '    def test_indexes_are_derived_from_finding_set_bindings(self) -> None:\n'
    if 'def test_genesis_study_and_three_local_syntheses_are_explicitly_derived' not in text:
        block = '''    def test_genesis_study_and_three_local_syntheses_are_explicitly_derived(self) -> None:\n        study = self._assert_source_derivation(\n            study_id="FINDSET-013",\n            source_id="CORPUS-SRC-108",\n            local_syntheses=[\n                ("FINDSET-124", "theologico-political"),\n                ("FINDSET-125", "athens-vs-jerusalem"),\n                ("FINDSET-126", "nomos-vs-physis"),\n            ],\n        )\n        self.assertEqual(study["witness_id"], "CORPUS-WIT-108")\n        self.assertEqual(study["earlier_published_text_comparison"], "PENDING")\n        self.assertEqual(study["successor_effect"], "NONE")\n\n'''
        text = text.replace(anchor, block + anchor)
    p.write_text(text, encoding="utf-8")
    replace("tests/test_interface_consistency.py", {"five_study": "six_study", 'study_count"], 5': 'study_count"], 6', 'sequence"], 5': 'sequence"], 6', 'study"], 5': 'study"], 6', 'study"], 14': 'study"], 13', "INCOMPLETE_5_OF_19": "INCOMPLETE_6_OF_19", 'next_item_study"], "CORPUS-SRC-108"': 'next_item_study"], "CORPUS-SRC-113"', '"SPINOZA-TREATISE-STUDY-001"]': '"SPINOZA-TREATISE-STUDY-001", "GENESIS-STUDY-001"]'})
    p = ROOT / "tests/test_interface_consistency.py"
    text = p.read_text(encoding="utf-8")
    if '"FINDSET-013":' not in text:
        text = text.replace('"FINDSET-012": [("FINDSET-122", "theologico-political"), ("FINDSET-123", "wise-vs-vulgar")],', '"FINDSET-012": [("FINDSET-122", "theologico-political"), ("FINDSET-123", "wise-vs-vulgar")],\n            "FINDSET-013": [("FINDSET-124", "theologico-political"), ("FINDSET-125", "athens-vs-jerusalem"), ("FINDSET-126", "nomos-vs-physis")],')
    p.write_text(text, encoding="utf-8")
    replace("tests/test_pr21_talmon_completion.py", {"1.9.0": "1.10.0", "2.7.0": "2.8.0", "1.11.0": "1.12.0", "1.13.0": "1.14.0", "1.5.0": "1.6.0", 'study_count"], 5': 'study_count"], 6', 'study"], 14': 'study"], 13', 'next_item_study"], "CORPUS-SRC-108"': 'next_item_study"], "CORPUS-SRC-113"', '"SPINOZA-TREATISE-STUDY-001"]': '"SPINOZA-TREATISE-STUDY-001", "GENESIS-STUDY-001"]'})
    replace("tests/test_tp_witness_coverage_complete.py", {"INCOMPLETE_5_OF_19": "INCOMPLETE_6_OF_19", 'theologico_political_independent_item_studies_registered"], 5': 'theologico_political_independent_item_studies_registered"], 6', "test_fourteen_witness_only_items_remain_noncertified_and_unstudied": "test_thirteen_witness_only_items_remain_noncertified_and_unstudied", "self.assertEqual(len(witness_only), 14)": "self.assertEqual(len(witness_only), 13)", '{"CORPUS-SRC-102", "CORPUS-SRC-103", "CORPUS-SRC-105", "CORPUS-SRC-109", "CORPUS-SRC-111"}': '{"CORPUS-SRC-102", "CORPUS-SRC-103", "CORPUS-SRC-105", "CORPUS-SRC-108", "CORPUS-SRC-109", "CORPUS-SRC-111"}'})
    replace("tests/test_corpus_wit_102_platform_registration.py", {"INCOMPLETE_5_OF_19": "INCOMPLETE_6_OF_19"})


def main():
    update_corpus()
    update_findings()
    update_manifest()
    update_schedule()
    update_process()
    update_mapping()
    update_audit()
    update_python()
    update_tests()
    print("Materialized CORPUS-SRC-108 complete provisional study integration.")


if __name__ == "__main__":
    main()
