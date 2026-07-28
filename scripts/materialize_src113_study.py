#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from pprint import pformat
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = "CORPUS-SRC-113"
WIT = "CORPUS-WIT-113"
STUDY = "PERSECUTION-INTRO-STUDY-001"
CORPUS_STUDY = "CORPUS-STUDY-014"
STUDY_PATH = "studies/theologico-political/introduction-to-persecution-and-the-art-of-writing/sequential-reconstruction.yaml"
TP_SYN = "problems/theologico-political/synthesis/introduction-to-persecution-and-the-art-of-writing.yaml"
WVG_SYN = "problems/wise-vs-vulgar/synthesis/introduction-to-persecution-and-the-art-of-writing.yaml"


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


def update_corpus():
    path = "corpus/index.yaml"
    d = load(path)
    d["identity"]["version"] = "1.15.0"
    d["revision_history"] = {
        "predecessor_version": "1.14.0",
        "predecessor_blob_sha": "775981647f6c78af09a0edeeeb53e8a19c6409b3",
        "transformation": "SUBSTANTIVE_FORWARD_REVISION",
        "reason": "Register PERSECUTION-INTRO-STUDY-001 as the seventh complete provisional Theologico-Political item study while preserving pending 1952-printing comparison, independent-corroboration limits, noncertification, predecessor authority, and no successor effect.",
    }
    source = next(x for x in d["source_entities"] if x["source_id"] == SRC)
    source["study_records"] = [CORPUS_STUDY]
    source["item_level_source_status"] = "REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION"
    source["study_status"] = "COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS"
    source["limits"] = [
        "reviewed witness is the fingerprinted 1997 SUNY collected reprint, not a separately reviewed 1952 Free Press printing",
        "printed pages 417-429 correspond to one-based PDF pages 436-448",
        "Strauss's argumentative body occupies printed pages 417-428 and notes continue through printed page 429",
        "PERSECUTION-INTRO-STUDY-001 is source-local and not independent corroboration of Farabi, Maimonides, Plato, religious traditions, or institutional history",
        "original 1952 printing comparison remains pending",
    ]
    entry = next(x for x in d["source_status_records"] if x["source_id"] == SRC)
    entry["completion"] = "REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION"
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
    c["study_records_registered"] = 14
    c["theologico_political_independent_item_studies_registered"] = 7
    c["current_studies_tree_yaml_records_accounted_for"] = 54
    gap = next(x for x in d["corpus_gaps"] if x["gap_id"] == "CORPUS-GAP-003")
    gap["statement"] = "All nineteen predecessor writings have bounded source identities and reviewed item witnesses; seven have complete provisional sequential studies, while the remaining twelve lack independent item studies."
    rules = [x for x in d["validation_rules"] if not ("witness-only Theologico-Political sources" in x)]
    rules.append("CORPUS-SRC-113 preserves fingerprinted reviewed-witness safeguards and complete provisional sequential reconstruction while original-1952 comparison remains pending")
    rules.append("all twelve witness-only Theologico-Political sources preserve registered-witness, pending-study, edition-comparison, noncertification, and no-successor safeguards")
    d["validation_rules"] = uniq(rules)
    t = d["termination"]
    t["theologico_political_independent_study_state"] = "INCOMPLETE_7_OF_19"
    t["next_required_units"] = [
        "conduct independent sequential reconstruction of CORPUS-SRC-116 from CORPUS-WIT-116",
        "compare the reviewed 1997 CORPUS-WIT-113 item with the original 1952 Free Press printing when available",
        "conduct independent sequential reconstruction for the remaining twelve writings",
        "expand independent Farabian, Maimonidean, biblical, Greek, medieval, modern, and reviewed-work witnesses",
    ]
    dump(path, d)


def rebuild_findings_indexes(d):
    problems = ["nomos-vs-physis", "philosophy-vs-poetry", "theory-vs-practice", "theologico-political", "athens-vs-jerusalem", "wise-vs-vulgar", "ancients-vs-moderns"]
    by_problem = {p: [] for p in problems}
    classes = {"SOURCE_SPECIFIC_STUDY": [], "INTEGRATION_GOVERNANCE_RECORD": [], "PROBLEM_LOCAL_SYNTHESIS": [], "MIGRATION_TRANSACTION_LEDGER": [], "PRESERVED_FINDING_BASIS": []}
    direct = ["CORPUS-SRC-001", "CORPUS-SRC-002", "CORPUS-SRC-003", "CORPUS-SRC-102", "CORPUS-SRC-103", "CORPUS-SRC-105", "CORPUS-SRC-108", "CORPUS-SRC-111", "CORPUS-SRC-113"]
    by_source = {s: [] for s in direct}
    by_source["CORPUS-SRC-101-119"] = []
    pred = {f"CORPUS-SRC-{i:03d}" for i in range(101, 120)}
    separate = {"CORPUS-SRC-102", "CORPUS-SRC-103", "CORPUS-SRC-105", "CORPUS-SRC-108", "CORPUS-SRC-111", "CORPUS-SRC-113"}
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
    d["identity"]["version"] = "1.7.0"
    d["revision_history"] = {
        "predecessor_version": "1.6.0",
        "predecessor_blob_sha": d.get("revision_history", {}).get("predecessor_blob_sha", "PRESERVED_BY_GIT"),
        "transformation": "SUBSTANTIVE_FORWARD_REVISION",
        "reason": "Register PERSECUTION-INTRO-STUDY-001 as FINDSET-014 and its jurisdiction-preserving Theologico-Political and Wise-versus-Vulgar syntheses as FINDSET-127 and FINDSET-128 while preserving original-edition, noncorroboration, noncertification, and no-successor safeguards.",
    }
    additions = [
        {"finding_set_id": "FINDSET-014", "path": STUDY_PATH, "record_class": "SOURCE_SPECIFIC_STUDY", "record_role": "SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION", "source_bindings": [SRC], "problem_bindings": ["theologico-political", "wise-vs-vulgar"], "status": "COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS", "certification": "NOT_CERTIFIED", "derived_local_syntheses": ["FINDSET-127", "FINDSET-128"], "witness_id": WIT, "original_1952_printing_comparison": "PENDING", "independent_corroboration": "INCOMPLETE", "successor_effect": "NONE"},
        {"finding_set_id": "FINDSET-127", "path": TP_SYN, "record_class": "PROBLEM_LOCAL_SYNTHESIS", "record_role": "SOURCE_TO_PROBLEM_SYNTHESIS", "source_bindings": [SRC], "problem_bindings": ["theologico-political"], "adjacent_problem_reference": "wise-vs-vulgar", "derived_from": ["FINDSET-014"], "status": "PROVISIONAL_NOT_CERTIFIED", "certification": "NOT_CERTIFIED", "successor_effect": "NONE"},
        {"finding_set_id": "FINDSET-128", "path": WVG_SYN, "record_class": "PROBLEM_LOCAL_SYNTHESIS", "record_role": "SOURCE_TO_PROBLEM_SYNTHESIS", "source_bindings": [SRC], "problem_bindings": ["wise-vs-vulgar"], "theologico_political_reference": "theologico-political", "derived_from": ["FINDSET-014"], "status": "PROVISIONAL_NOT_CERTIFIED", "certification": "NOT_CERTIFIED", "successor_effect": "NONE"},
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
    d["coverage"].update({"finding_sets_registered": 47, "source_specific_and_integration_records_registered": 14, "problem_syntheses_registered": 28, "current_problem_synthesis_tree_yaml_records_accounted_for": 28, "corpus_study_records_accounted_for": 14})
    gap = next(x for x in d["findings_gaps"] if x["gap_id"] == "FINDINGS-GAP-003")
    gap["statement"] = "Seven of the nineteen Theologico-Political writings now have complete provisional item studies; the remaining twelve lack individual sequential studies."
    d["validation_rules"] = uniq([x for x in d["validation_rules"] if not x.startswith("FINDSET-014 must")] + ["FINDSET-014 must derive only FINDSET-127 and FINDSET-128, preserve CORPUS-WIT-113 and pending 1952 comparison, and retain noncorroboration and no-successor safeguards"])
    d["termination"]["next_required_units"] = ["conduct the remaining twelve Theologico-Political independent sequential studies beginning with CORPUS-SRC-116", "compare the CORPUS-SRC-113 reviewed 1997 witness with the original 1952 Free Press printing when available", "expand independent Farabian, Maimonidean, biblical, Greek, medieval, modern, and reviewed-work witness studies", "preserve later corrections, dissent, and supersession through forward registry revision"]
    dump(path, d)


def update_manifest():
    path = "manifest.yaml"
    d = load(path)
    d["identity"]["version"] = "1.11.0"
    d["revision_history"] = {"predecessor_version": "1.10.0", "predecessor_blob_sha": "17c3d070d98b8ba08a9b5fff3ab1964018c13229", "reason": "Register PERSECUTION-INTRO-STUDY-001 as the seventh complete provisional Theologico-Political item study and synchronize corpus v1.15.0, findings v1.7.0, audit v2.9.0, mapping v1.11.0, process v1.13.0, and schedule v1.11.0 while preserving twelve pending studies, edition-comparison limits, noncertification, predecessor authority, and the Sanctum repin block."}
    d["audit"]["version"] = "2.9.0"
    d["component_completion"]["theologico_political_item_level_source_statuses"] = "19_OF_19_IDENTITIES_19_OF_19_REVIEWED_ITEM_WITNESSES_7_OF_19_COMPLETE_PROVISIONAL_ITEM_STUDIES"
    d["corpus"]["registry_version"] = "1.15.0"
    s = d["corpus"]["theologico_political_item_level_statuses"]
    s["independent_sequential_study_count"] = 7
    s["remaining_without_independent_sequential_study"] = 12
    s["completed_study_ids"] = uniq(s.get("completed_study_ids", []) + [STUDY])
    s["rule"] = "All nineteen predecessor items have reviewed witnesses and seven have complete provisional source studies. Witness and study completion remain distinct from independent corroboration, doctrinal certification, migration completion, successor activation, or repository completion."
    d["corpus"]["limitation"] = "All nineteen predecessor writings have bounded identities and reviewed item witnesses. Seven have complete provisional sequential studies, including CORPUS-SRC-113 from the fingerprinted 1997 collected witness; twelve still lack independent studies. Original-edition comparisons, independent witnesses, and source-text access remain incomplete."
    d["findings"]["registry_version"] = "1.7.0"
    d["findings"]["newly_registered"] = ["FINDSET-014", "FINDSET-127", "FINDSET-128"]
    dump(path, d)


def update_schedule():
    path = "history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml"
    d = load(path)
    d["identity"]["version"] = "1.11.0"
    d["revision_history"] = {"predecessor_version": "1.10.0", "predecessor_blob_sha": "PRESERVED_BY_GIT", "reason": "Complete PERSECUTION-INTRO-STUDY-001 from CORPUS-WIT-113, advancing independent sequential study coverage to 7-of-19 and the next study unit to CORPUS-SRC-116 while preserving complete 19-of-19 witness coverage and all edition, corroboration, certification, migration, and successor limits."}
    d["status"]["independent_sequential_study_completion"] = "INCOMPLETE_7_OF_19"
    item = next(x for g in d["priority_groups"] for x in g["items"] if x["source_id"] == SRC)
    item["study_id"] = STUDY
    item["state"] = "REVIEWED_WITNESS_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDY"
    item["next_action"] = "ORIGINAL_1952_PRINTING_COMPARISON_AND_INDEPENDENT_FARABIAN_MEDIEVAL_WITNESS_EXPANSION"
    d["selection"]["completed_study_ids"] = uniq(d["selection"].get("completed_study_ids", []) + [STUDY])
    d["selection"]["selection_state"] = "NINETEEN_REVIEWED_ITEM_WITNESSES_SEVEN_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDIES"
    d["selection"]["completed_units"] = ["all nineteen predecessor source identities have reviewed witnesses", "seven source studies are complete provisional", "twelve witness-only sources remain pending independent sequential reconstruction", "all original-edition and independent-corroboration limits remain explicit"]
    d["termination"]["independent_sequential_reconstruction"] = "INCOMPLETE_7_OF_19"
    d["termination"]["next_item_study"] = "CORPUS-SRC-116"
    d["next_item_study_unit"] = {"source_id": "CORPUS-SRC-116", "title": "Preface to Hobbes Politische Wissenschaft", "action": "INDEPENDENT_SEQUENTIAL_RECONSTRUCTION_FROM_REGISTERED_WITNESS", "prerequisite": "SATISFIED_CORPUS_WIT_116_REGISTERED", "following_source": "CORPUS-SRC-101"}
    dump(path, d)


def update_process():
    path = "history/production-plans/2026-07-27-ten-step-completion-process.yaml"
    d = load(path)
    d["identity"]["version"] = "1.13.0"
    d["revision_history"] = {"predecessor_version": "1.12.0", "predecessor_blob_sha": "PRESERVED_BY_GIT", "reason": "Complete PERSECUTION-INTRO-STUDY-001 as the seventh provisional Theologico-Political sequential reconstruction and advance the next study unit to CORPUS-SRC-116 while preserving 19-of-19 witness coverage and twelve remaining studies."}
    for step in d["steps"]:
        if step["sequence"] == 1:
            step["current_version"] = "2.9.0"
        elif step["sequence"] == 2:
            step["current_version"] = "1.11.0"
        elif step["sequence"] == 7:
            step["completed"] = uniq(step.get("completed", []) + ["Introduction to Persecution and the Art of Writing supplies distinct provisional syntheses to Theologico-Political and Wise-versus-Vulgar"])
        elif step["sequence"] == 8:
            step["completed"] = uniq(step.get("completed", []) + ["PERSECUTION-INTRO-STUDY-001 is complete provisional for CORPUS-WIT-113"])
            rem = step.get("remaining", [])
            step["remaining"] = ["conduct twelve independent sequential item studies, beginning with CORPUS-SRC-116"] + rem[1:]
    d["current_production_unit"] = {"step": 8, "completed_subunit": {"title": "Introduction to Persecution and the Art of Writing independent sequential reconstruction", "state": "COMPLETE_PROVISIONAL_PENDING_BRANCH_VALIDATION_AND_MERGE", "source_id": SRC, "witness_id": WIT, "study_id": STUDY, "witness_coverage": "COMPLETE_19_OF_19", "study_coverage": "INCOMPLETE_7_OF_19", "non_effect": "Source-study completion does not supply independent corroboration, doctrine, certified migration, successor activation, predecessor displacement, or completed-interface readiness."}, "next_subunit": {"title": "Preface to Hobbes Politische Wissenschaft independent sequential reconstruction", "source_id": "CORPUS-SRC-116", "witness_id": "CORPUS-WIT-116", "first_action": "Reconstruct printed pages 453-456 in textual order before comparing with the active predecessor.", "following_source": "CORPUS-SRC-101"}, "non_effects": ["no source-text admission through registries", "no doctrinal or migration certification", "no successor activation or predecessor displacement", "no Sanctum repin as a completed interface"]}
    dump(path, d)


def update_mapping():
    path = "migrations/lean-operational-interface.yaml"
    d = load(path)
    d["identity"]["version"] = "1.11.0"
    d["revision_history"] = {"predecessor_version": "1.10.0", "predecessor_blob_sha": "PRESERVED_BY_GIT", "reason": "Synchronize PERSECUTION-INTRO-STUDY-001, corpus registry v1.15.0, findings v1.7.0, audit v2.9.0, process v1.13.0, and schedule v1.11.0 while preserving twelve pending studies, noncorroboration, noncertification, predecessor authority, and repository incompleteness."}
    d["completion_audit"]["version"] = "2.9.0"
    d["production_process"]["completed_study_subunit"] = "SEVEN_OF_19_COMPLETE_PROVISIONAL_TWELVE_PENDING"
    c = d["mappings"]["corpus"]
    c["interface"]["registry_version"] = "1.15.0"
    s = c["theologico_political_item_level_statuses"]
    s["independent_sequential_study_count"] = 7
    s["remaining_without_independent_sequential_study"] = 12
    s["completed_study_ids"] = uniq(s.get("completed_study_ids", []) + [STUDY])
    s["witness_only_source_ids"] = [x for x in s.get("witness_only_source_ids", []) if x != SRC]
    c["present_function"] = uniq(c.get("present_function", []) + ["validate PERSECUTION-INTRO-STUDY-001 as a complete provisional reconstruction with pending 1952 comparison and no successor effect"])
    c["limit"] = "Current-state exhaustiveness, nineteen reviewed item witnesses, and seven complete provisional item studies do not create a complete corpus, supply independent corroboration, certify findings, or authorize migration and activation."
    f = d["mappings"]["findings"]
    f["interface"]["registry_version"] = "1.7.0"
    f["newly_registered"] = [{"finding_set_id": "FINDSET-014", "path": STUDY_PATH}, {"finding_set_id": "FINDSET-127", "path": TP_SYN, "derived_from": "FINDSET-014"}, {"finding_set_id": "FINDSET-128", "path": WVG_SYN, "derived_from": "FINDSET-014"}]
    dump(path, d)


def update_audit():
    path = "audits/operational-completeness.yaml"
    d = load(path)
    d["identity"]["version"] = "2.9.0"
    d["revision_history"] = {"predecessor_version": "2.8.0", "predecessor_blob_sha": "PRESERVED_BY_GIT", "reason": "Complete PERSECUTION-INTRO-STUDY-001 from CORPUS-WIT-113, advance Theologico-Political study coverage to seven of nineteen, and preserve twelve pending studies, original-1952 comparison, noncorroboration, noncertification, predecessor authority, and the Sanctum repin block."}
    d["basis"]["current_revision_scope"] = "production/corpus-src-113-sequential-reconstruction"
    s = d["summary"]["theologico_political_item_level_status"]
    s["independently_reconstructed_count_within_this_sequence"] = 7
    s["remaining_without_independent_sequential_study"] = 12
    s["completed_source_ids"] = uniq(s.get("completed_source_ids", []) + [SRC])
    s["completed_witness_ids"] = uniq(s.get("completed_witness_ids", []) + [WIT])
    s["completed_study_ids"] = uniq(s.get("completed_study_ids", []) + [STUDY])
    s["witness_only_source_ids"] = [x for x in uniq(s.get("witness_only_source_ids", [])) if x != SRC]
    s["witness_only_witness_ids"] = [x for x in uniq(s.get("witness_only_witness_ids", [])) if x != WIT]
    s["interpretation_limit"] = "All nineteen predecessor items have reviewed witnesses and seven completed studies are independent reconstructions relative to predecessor and collection-level synthesis. Twelve witness registrations remain study-pending; none of the source studies is independent corroboration of represented traditions."
    summary = d["summary"]
    summary["completed_operational_units"] = uniq(summary.get("completed_operational_units", []) + ["PERSECUTION-INTRO-STUDY-001 complete provisional sequential reconstruction", "CORPUS-STUDY-014 and FINDSET-014 typed registrations", "FINDSET-127 and FINDSET-128 jurisdiction-preserving problem-local syntheses"])
    deficiencies = [x for x in uniq(summary.get("remaining_major_deficiencies", [])) if not re.match(r"^(twelve|thirteen|fourteen|fifteen) Theologico-Political writings", x)]
    summary["remaining_major_deficiencies"] = ["twelve Theologico-Political writings still require independent sequential item studies"] + deficiencies
    # Update core registry audit records without proliferating duplicate records.
    for rec in d.get("records", []):
        if rec.get("path") == "corpus/index.yaml":
            rec["registry_version"] = "1.15.0"
            rec["present_function"] = ["22 typed source entities", "22 reviewed witnesses", "22 source-status records", "14 analytical and integration study records", "all 54 YAML records in the studies tree accounted for", "all 7 problem witness registries", "19 Theologico-Political identities, 19 reviewed item witnesses, and 7 complete provisional item studies", "7 positive corpus-gap records"]
            rec["remaining"] = ["twelve independent item studies", "complete Strauss bibliography and edition-specific comparisons", "broader independent classical, biblical, medieval, Spinozist, Cohenian, Kantian, and modern corpora", "source-text admission and runtime source access remain separate"]
        elif rec.get("path") == "findings/index.yaml":
            rec["registry_version"] = "1.7.0"
            rec["present_function"] = ["47 typed finding sets", "14 source-specific or integration records", "28 problem-local syntheses", "3 migration transaction ledgers", "2 preserved finding bases", "explicit derivation from FINDSET-014 to FINDSET-127 and FINDSET-128", "source, problem, record-class, derivation, migration, and preservation indexes"]
        elif rec.get("path") == "manifest.yaml":
            rec["present_function"] = ["registers corpus v1.15.0, findings v1.7.0, 19 Theologico-Political identities, 19 reviewed item witnesses, and 7 completed provisional item studies", "preserves structural, semantic, runtime, migration, predecessor, and certification limits", "blocks completed-interface Sanctum repinning"]
    d["records"] = [x for i, x in enumerate(d.get("records", [])) if x.get("path") not in {STUDY_PATH, TP_SYN, WVG_SYN} or all(y.get("path") != x.get("path") for y in d.get("records", [])[:i])]
    d["records"].extend([
        {"path": STUDY_PATH, "classification": "SUBSTANTIVELY_RECONSTRUCTED", "identity": STUDY, "present_function": ["reconstructs printed pages 417-429 in eight ordered units", "defines sociology of philosophy through the recurring political danger to philosophy", "reconstructs Farabi's differentiated presentation as evidence of exoteric accommodation under specified conditions", "preserves Theologico-Political primary and Wise-versus-Vulgar secondary jurisdiction"], "remaining": ["original 1952 Free Press comparison", "independent Farabi, Maimonides, Plato, legal, theological, and historical witness reconstruction", "later authorized proposition-level migration review"]},
        {"path": TP_SYN, "classification": "SUBSTANTIVELY_RECONSTRUCTED", "identity": "TP-PERSECUTION-INTRO-001", "present_function": ["supplies the source-local Theologico-Political synthesis without predecessor displacement"], "remaining": ["independent witness expansion and any later certified proposition-level migration"]},
        {"path": WVG_SYN, "classification": "SUBSTANTIVELY_RECONSTRUCTED", "identity": "WVG-PERSECUTION-INTRO-001", "present_function": ["supplies the source-local audience, exposure, concealment, and political-protection synthesis without mechanical inversion or claimant certification"], "remaining": ["independent Farabian and historical reconstruction and later authorized migration review"]},
    ])
    po = d["production_order"]
    po["completed_in_current_sequence"] = uniq(po.get("completed_in_current_sequence", []) + ["PERSECUTION-INTRO-STUDY-001 with FINDSET-014, FINDSET-127, and FINDSET-128"])
    po["next"] = ["run complete structural and behavioral validation for the seventh Theologico-Political item study", "conduct CORPUS-SRC-116 independent sequential reconstruction from printed pages 453-456", "continue the remaining eleven independent sequential reconstructions after CORPUS-SRC-116", "expand independent source-tradition witnesses and original-edition comparisons", "validate actual ministerial reports against the full contract stack"]
    dump(path, d)


def update_python():
    # Rebuild explicit corpus complete/witness-only tables from current typed registry.
    path = ROOT / "corpus_registry.py"
    text = path.read_text(encoding="utf-8")
    complete = {}
    existing_specs = {
        "CORPUS-SRC-102": ("CORPUS-STUDY-011", "SPINOZA-PREFACE-STUDY-001", "studies/theologico-political/preface-to-spinozas-critique-of-religion/sequential-reconstruction.yaml", "studies/theologico-political/preface-to-spinozas-critique-of-religion/reviewed-witness.yaml", "COMPLETE_FOR_QUALIFIED_1997_PLATFORM_REFERENCE_WITNESS", True),
        "CORPUS-SRC-103": ("CORPUS-STUDY-012", "SPINOZA-TREATISE-STUDY-001", "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/sequential-reconstruction.yaml", "studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/reviewed-witness.yaml", "COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS", False),
        "CORPUS-SRC-105": ("CORPUS-STUDY-009", "COHEN-STUDY-001", "studies/theologico-political/introductory-essay-hermann-cohen-religion-of-reason/sequential-reconstruction.yaml", "studies/theologico-political/introductory-essay-hermann-cohen-religion-of-reason/reviewed-witness.yaml", "COMPLETE_FOR_REVIEWED_1983_COLLECTED_WITNESS", False),
        "CORPUS-SRC-108": ("CORPUS-STUDY-013", "GENESIS-STUDY-001", "studies/theologico-political/on-the-interpretation-of-genesis/sequential-reconstruction.yaml", "studies/theologico-political/on-the-interpretation-of-genesis/reviewed-witness.yaml", "COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS", False),
        "CORPUS-SRC-109": ("CORPUS-STUDY-008", "JA-STUDY-001", "studies/theologico-political/jerusalem-and-athens/sequential-reconstruction.yaml", None, "COMPLETE_FOR_REVIEWED_1983_COLLECTED_WITNESS", False),
        "CORPUS-SRC-111": ("CORPUS-STUDY-010", "TALMON-STUDY-001", "studies/theologico-political/review-talmon-nature-of-jewish-history/sequential-reconstruction.yaml", "studies/theologico-political/review-talmon-nature-of-jewish-history/reviewed-witness.yaml", "COMPLETE_FOR_REVIEWED_1983_COLLECTED_WITNESS", False),
        "CORPUS-SRC-113": ("CORPUS-STUDY-014", STUDY, STUDY_PATH, "studies/theologico-political/introduction-to-persecution-and-the-art-of-writing/reviewed-witness.yaml", "COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS", False),
    }
    registry = load("corpus/index.yaml")
    witnesses = {x["source_id"]: x for x in registry["reviewed_witnesses"]}
    for sid, (study_id, internal_id, study_path, witness_path, reading_state, platform) in existing_specs.items():
        w = witnesses[sid]
        spec = {"status_id": sid.replace("CORPUS-SRC", "CORPUS-STATUS"), "witness_id": w["witness_id"], "study_id": study_id, "internal_study_id": internal_id, "study_path": study_path, "witness_record_path": witness_path, "printed_page_range": w["printed_page_range"], "pdf_page_range_one_based": w["pdf_page_range_one_based"], "reading_state": reading_state, "platform_reference": platform}
        if platform:
            spec["platform_object_identifier"] = w["platform_object_identifier"]
        complete[sid] = spec
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
    text = text.replace('identity.get("version") != "1.14.0"', 'identity.get("version") != "1.15.0"').replace('identity.version must be 1.14.0', 'identity.version must be 1.15.0')
    text = text.replace('"study records": (len(study_ids), 13)', '"study records": (len(study_ids), 14)')
    text = text.replace('"theologico_political_independent_item_studies_registered": 6', '"theologico_political_independent_item_studies_registered": 7')
    text = text.replace('!= "INCOMPLETE_6_OF_19"', '!= "INCOMPLETE_7_OF_19"').replace('must be INCOMPLETE_6_OF_19', 'must be INCOMPLETE_7_OF_19')
    path.write_text(text, encoding="utf-8")

    path = ROOT / "findings_registry.py"
    text = path.read_text(encoding="utf-8")
    actual_syntheses = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "problems").glob("*/synthesis/*.yaml") if p.is_file())
    set_text = "EXPECTED_SYNTHESIS_PATHS = {\n" + "".join(f'    "{p}",\n' for p in actual_syntheses) + "}\n\n"
    text, count = re.subn(r"EXPECTED_SYNTHESIS_PATHS = \{.*?\n\}\n\n", set_text, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit("cannot replace expected synthesis set")
    if '    "CORPUS-SRC-113",\n' not in text:
        text = text.replace('    "CORPUS-SRC-111",\n]', '    "CORPUS-SRC-111",\n    "CORPUS-SRC-113",\n]')
    text = text.replace('"CORPUS-SRC-108", "CORPUS-SRC-111"}', '"CORPUS-SRC-108", "CORPUS-SRC-111", "CORPUS-SRC-113"}')
    contract = '''    "FINDSET-014": {\n        "source_id": "CORPUS-SRC-113",\n        "local_syntheses": ["FINDSET-127", "FINDSET-128"],\n        "problem_bindings": {"FINDSET-127": "theologico-political", "FINDSET-128": "wise-vs-vulgar"},\n        "required_limits": {"witness_id": "CORPUS-WIT-113", "original_1952_printing_comparison": "PENDING", "independent_corroboration": "INCOMPLETE"},\n    },\n'''
    if '"FINDSET-014": {' not in text:
        text = text.replace('\n}\n\n\nclass FindingsRegistryError', '\n' + contract + '}\n\n\nclass FindingsRegistryError', 1)
    text = text.replace('identity.get("version") != "1.6.0"', 'identity.get("version") != "1.7.0"').replace('identity.version must be 1.6.0', 'identity.version must be 1.7.0')
    text = text.replace('if len(finding_ids) != 44:', 'if len(finding_ids) != 47:').replace('expected 44 finding sets', 'expected 47 finding sets')
    path.write_text(text, encoding="utf-8")


def update_tests():
    def replace(path, reps):
        p = ROOT / path
        text = p.read_text(encoding="utf-8")
        for old, new in reps.items():
            text = text.replace(old, new)
        p.write_text(text, encoding="utf-8")
    replace("tests/test_corpus_registry.py", {"1.14.0": "1.15.0", "53,": "54,", 'study_records_registered"], 13': 'study_records_registered"], 14', "test_thirteen_tp_sources_have_witnesses_but_still_require_study": "test_twelve_tp_sources_have_witnesses_but_still_require_study", "self.assertEqual(len(sources), 13)": "self.assertEqual(len(sources), 12)"})
    p = ROOT / "tests/test_corpus_registry.py"
    text = p.read_text(encoding="utf-8")
    anchor = '    def test_spinoza_preface_platform_witness_and_study_are_registered(self) -> None:\n'
    if 'def test_persecution_intro_witness_and_study_are_registered' not in text:
        block = '''    def test_persecution_intro_witness_and_study_are_registered(self) -> None:\n        registry = corpus_registry.load_registry()\n        source = next(item for item in registry["source_entities"] if item["source_id"] == "CORPUS-SRC-113")\n        entry = next(item for item in registry["source_status_records"] if item["source_id"] == "CORPUS-SRC-113")\n        witness = next(item for item in registry["reviewed_witnesses"] if item["witness_id"] == "CORPUS-WIT-113")\n        study = next(item for item in registry["study_records"] if item["study_id"] == "CORPUS-STUDY-014")\n        status = corpus_registry.load_yaml(corpus_registry._resolve(entry["path"]))\n        study_record = corpus_registry.load_yaml(corpus_registry._resolve(study["path"]))\n        witness_record = corpus_registry.load_yaml(corpus_registry._resolve(witness["witness_record_path"]))\n        self.assertEqual(source["study_records"], ["CORPUS-STUDY-014"])\n        self.assertEqual(witness["printed_page_range"], {"start": 417, "end": 429})\n        self.assertEqual(witness["pdf_page_range_one_based"], {"start": 436, "end": 448})\n        self.assertEqual(status["status"]["independent_sequential_study"], "PERSECUTION-INTRO-STUDY-001")\n        self.assertEqual(status["termination"]["study_state"], "COMPLETE_PROVISIONAL")\n        self.assertEqual(status["termination"]["original_edition_comparison"], "PENDING")\n        self.assertEqual(study_record["identity"]["id"], "PERSECUTION-INTRO-STUDY-001")\n        self.assertEqual(study_record["termination"]["reading_state"], "COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS")\n        self.assertEqual(study_record["termination"]["successor_effect"], "NONE")\n        self.assertEqual(witness_record["termination"]["study_state"], "INCOMPLETE")\n\n'''
        text = text.replace(anchor, block + anchor)
    p.write_text(text, encoding="utf-8")
    replace("tests/test_findings_registry.py", {"1.6.0": "1.7.0", "len(finding_ids), 44": "len(finding_ids), 47", "len(registered), 26": "len(registered), 28", "len(registered), 13": "len(registered), 14"})
    p = ROOT / "tests/test_findings_registry.py"
    text = p.read_text(encoding="utf-8")
    anchor = '    def test_indexes_are_derived_from_finding_set_bindings(self) -> None:\n'
    if 'def test_persecution_intro_study_and_two_local_syntheses_are_explicitly_derived' not in text:
        block = '''    def test_persecution_intro_study_and_two_local_syntheses_are_explicitly_derived(self) -> None:\n        study = self._assert_source_derivation(\n            study_id="FINDSET-014",\n            source_id="CORPUS-SRC-113",\n            local_syntheses=[("FINDSET-127", "theologico-political"), ("FINDSET-128", "wise-vs-vulgar")],\n        )\n        self.assertEqual(study["witness_id"], "CORPUS-WIT-113")\n        self.assertEqual(study["original_1952_printing_comparison"], "PENDING")\n        self.assertEqual(study["successor_effect"], "NONE")\n\n'''
        text = text.replace(anchor, block + anchor)
    p.write_text(text, encoding="utf-8")
    replace("tests/test_interface_consistency.py", {"six_study": "seven_study", 'study_count"], 6': 'study_count"], 7', 'sequence"], 6': 'sequence"], 7', 'study"], 6': 'study"], 7', 'study"], 13': 'study"], 12', "INCOMPLETE_6_OF_19": "INCOMPLETE_7_OF_19", 'next_item_study"], "CORPUS-SRC-113"': 'next_item_study"], "CORPUS-SRC-116"', '"GENESIS-STUDY-001"]': '"GENESIS-STUDY-001", "PERSECUTION-INTRO-STUDY-001"]'})
    p = ROOT / "tests/test_interface_consistency.py"
    text = p.read_text(encoding="utf-8")
    if '"FINDSET-014":' not in text:
        text = text.replace('"FINDSET-013": [("FINDSET-124", "theologico-political"), ("FINDSET-125", "athens-vs-jerusalem"), ("FINDSET-126", "nomos-vs-physis")],', '"FINDSET-013": [("FINDSET-124", "theologico-political"), ("FINDSET-125", "athens-vs-jerusalem"), ("FINDSET-126", "nomos-vs-physis")],\n            "FINDSET-014": [("FINDSET-127", "theologico-political"), ("FINDSET-128", "wise-vs-vulgar")],')
    p.write_text(text, encoding="utf-8")
    replace("tests/test_pr21_talmon_completion.py", {"1.10.0": "1.11.0", "2.8.0": "2.9.0", "1.12.0": "1.13.0", "1.14.0": "1.15.0", "1.6.0": "1.7.0", 'study_count"], 6': 'study_count"], 7', 'study"], 13': 'study"], 12', 'next_item_study"], "CORPUS-SRC-113"': 'next_item_study"], "CORPUS-SRC-116"', '"GENESIS-STUDY-001"]': '"GENESIS-STUDY-001", "PERSECUTION-INTRO-STUDY-001"]'})
    replace("tests/test_tp_witness_coverage_complete.py", {"INCOMPLETE_6_OF_19": "INCOMPLETE_7_OF_19", 'theologico_political_independent_item_studies_registered"], 6': 'theologico_political_independent_item_studies_registered"], 7', "test_thirteen_witness_only_items_remain_noncertified_and_unstudied": "test_twelve_witness_only_items_remain_noncertified_and_unstudied", "self.assertEqual(len(witness_only), 13)": "self.assertEqual(len(witness_only), 12)", '"CORPUS-SRC-111"}': '"CORPUS-SRC-111", "CORPUS-SRC-113"}'})
    replace("tests/test_corpus_wit_102_platform_registration.py", {"INCOMPLETE_6_OF_19": "INCOMPLETE_7_OF_19"})


def main():
    update_corpus(); update_findings(); update_manifest(); update_schedule(); update_process(); update_mapping(); update_audit(); update_python(); update_tests()
    print("Materialized CORPUS-SRC-113 complete provisional study integration.")


if __name__ == "__main__":
    main()
