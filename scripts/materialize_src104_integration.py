#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "production/corpus-src-104-sequential-reconstruction"
STUDY_PATH = "studies/theologico-political/preface-to-isaac-husik-philosophical-essays/sequential-reconstruction.yaml"
STATUS_PATH = "studies/theologico-political/preface-to-isaac-husik-philosophical-essays/source-status.yaml"
TP_SYNTHESIS_PATH = "problems/theologico-political/synthesis/preface-to-isaac-husik-philosophical-essays.yaml"
AVJ_SYNTHESIS_PATH = "problems/athens-vs-jerusalem/synthesis/preface-to-isaac-husik-philosophical-essays.yaml"

YAML = YAML()
YAML.preserve_quotes = True
YAML.width = 120


def load(path: str):
    with (ROOT / path).open(encoding="utf-8") as handle:
        return YAML.load(handle)


def save(path: str, data) -> None:
    with (ROOT / path).open("w", encoding="utf-8") as handle:
        YAML.dump(data, handle)


def item(records, key: str, value: str):
    return next(record for record in records if record.get(key) == value)


def append_unique(seq, value) -> None:
    if value not in seq:
        seq.append(value)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one occurrence, found {count}: {old!r}")
    return text.replace(old, new, 1)


def update_corpus_index() -> None:
    path = "corpus/index.yaml"
    data = load(path)
    if data["identity"]["version"] != "1.17.0":
        raise RuntimeError("Unexpected corpus registry predecessor version")
    data["identity"]["version"] = "1.18.0"
    data["revision_history"]["predecessor_version"] = "1.17.0"
    data["revision_history"]["predecessor_blob_sha"] = "PRESERVED_BY_GIT"
    data["revision_history"]["transformation"] = "SUBSTANTIVE_FORWARD_REVISION"
    data["revision_history"]["reason"] = (
        "Register HUSIK-PREFACE-STUDY-001 as the tenth complete provisional Theologico-Political item study, "
        "register CORPUS-STUDY-017, preserve the collective-editorial-layer distinction and pending original-1952 "
        "comparison, and retain noncorroboration, noncertification, predecessor authority, and no successor effect."
    )

    src = item(data["source_entities"], "source_id", "CORPUS-SRC-104")
    src["item_level_source_status"] = "REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION"
    src["study_status"] = "COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS"
    src["study_records"] = ["CORPUS-STUDY-017"]
    src["limits"] = [
        "reviewed witness is the fingerprinted 1997 SUNY collected text, not a separately reviewed 1952 Basil Blackwell printing",
        "printed pages 235-266 correspond to one-based PDF pages 254-285",
        "the closing plural statement on printed page 264 is preserved as a collective 1952 editorial layer and later bracketed Ed. notes remain a distinct 1997 editorial layer",
        "HUSIK-PREFACE-STUDY-001 is source-local and not independent corroboration of Husik, Judaism, medieval Jewish philosophy, Greek philosophy, or jurisprudential interlocutors",
        "original 1952 printing comparison remains pending",
    ]

    status = item(data["source_status_records"], "status_id", "CORPUS-STATUS-104")
    status["completion"] = "REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION"

    if not any(record.get("study_id") == "CORPUS-STUDY-017" for record in data["study_records"]):
        data["study_records"].append(CommentedMap([
            ("study_id", "CORPUS-STUDY-017"),
            ("source_id", "CORPUS-SRC-104"),
            ("path", STUDY_PATH),
            ("record_role", "SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION"),
            ("completion", "COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS"),
            ("certification", "NOT_CERTIFIED"),
        ]))

    coverage = data["coverage"]
    coverage["study_records_registered"] = 17
    coverage["theologico_political_independent_item_studies_registered"] = 10
    coverage["current_studies_tree_yaml_records_accounted_for"] = 57

    gap = item(data["corpus_gaps"], "gap_id", "CORPUS-GAP-003")
    gap["statement"] = (
        "All nineteen predecessor writings have bounded source identities and reviewed item witnesses; ten have complete "
        "provisional sequential studies, while the remaining nine lack independent item studies."
    )

    rule = (
        "CORPUS-SRC-104 preserves the fingerprinted reviewed witness, collective 1952 editorial-layer distinction, "
        "complete provisional sequential reconstruction, pending original-1952 comparison, noncorroboration, "
        "noncertification, and no-successor safeguards"
    )
    append_unique(data["validation_rules"], rule)
    data["validation_rules"] = [
        r.replace("all ten witness-only Theologico-Political sources", "all nine witness-only Theologico-Political sources")
        if isinstance(r, str) else r
        for r in data["validation_rules"]
    ]

    term = data["termination"]
    term["theologico_political_independent_study_state"] = "INCOMPLETE_10_OF_19"
    term["next_required_units"] = [
        "conduct independent sequential reconstruction of CORPUS-SRC-106 from CORPUS-WIT-106",
        "compare the reviewed 1997 CORPUS-WIT-104 item with the original 1952 Basil Blackwell printing when available",
        "conduct independent sequential reconstruction for the remaining nine writings",
        "expand independent biblical, Greek, Jewish, Christian, Spinozist, medieval, modern, Husik, and reviewed-work witnesses",
    ]
    save(path, data)


def update_findings_index() -> None:
    path = "findings/index.yaml"
    data = load(path)
    if data["identity"]["version"] != "1.9.0":
        raise RuntimeError("Unexpected findings registry predecessor version")
    data["identity"]["version"] = "1.10.0"
    data["revision_history"]["predecessor_version"] = "1.9.0"
    data["revision_history"]["predecessor_blob_sha"] = "PRESERVED_BY_GIT"
    data["revision_history"]["transformation"] = "SUBSTANTIVE_FORWARD_REVISION"
    data["revision_history"]["reason"] = (
        "Register HUSIK-PREFACE-STUDY-001 as FINDSET-017 and jurisdiction-preserving syntheses FINDSET-134 and "
        "FINDSET-135 while preserving the collective-editorial-layer distinction, pending original-1952 comparison, "
        "noncorroboration, noncertification, and no-successor safeguards."
    )

    sets = data["finding_sets"]
    if not any(x.get("finding_set_id") == "FINDSET-017" for x in sets):
        insert_at = next(i for i, x in enumerate(sets) if x.get("finding_set_id") == "FINDSET-101")
        sets.insert(insert_at, CommentedMap([
            ("finding_set_id", "FINDSET-017"),
            ("path", STUDY_PATH),
            ("record_class", "SOURCE_SPECIFIC_STUDY"),
            ("record_role", "SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION"),
            ("source_bindings", ["CORPUS-SRC-104"]),
            ("problem_bindings", ["theologico-political", "athens-vs-jerusalem"]),
            ("status", "COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS"),
            ("certification", "NOT_CERTIFIED"),
            ("derived_local_syntheses", ["FINDSET-134", "FINDSET-135"]),
            ("witness_id", "CORPUS-WIT-104"),
            ("original_1952_printing_comparison", "PENDING"),
            ("independent_corroboration", "INCOMPLETE"),
            ("successor_effect", "NONE"),
        ]))
    if not any(x.get("finding_set_id") == "FINDSET-134" for x in sets):
        insert_at = next(i for i, x in enumerate(sets) if x.get("finding_set_id") == "FINDSET-201")
        sets.insert(insert_at, CommentedMap([
            ("finding_set_id", "FINDSET-134"),
            ("path", TP_SYNTHESIS_PATH),
            ("record_class", "PROBLEM_LOCAL_SYNTHESIS"),
            ("record_role", "SOURCE_TO_PROBLEM_SYNTHESIS"),
            ("source_bindings", ["CORPUS-SRC-104"]),
            ("problem_bindings", ["theologico-political"]),
            ("adjacent_problem_references", ["athens-vs-jerusalem"]),
            ("derived_from", ["FINDSET-017"]),
            ("status", "PROVISIONAL_NOT_CERTIFIED"),
            ("certification", "NOT_CERTIFIED"),
            ("successor_effect", "NONE"),
        ]))
        sets.insert(insert_at + 1, CommentedMap([
            ("finding_set_id", "FINDSET-135"),
            ("path", AVJ_SYNTHESIS_PATH),
            ("record_class", "PROBLEM_LOCAL_SYNTHESIS"),
            ("record_role", "SOURCE_TO_PROBLEM_SYNTHESIS"),
            ("source_bindings", ["CORPUS-SRC-104"]),
            ("problem_bindings", ["athens-vs-jerusalem"]),
            ("theologico_political_reference", "theologico-political"),
            ("derived_from", ["FINDSET-017"]),
            ("status", "PROVISIONAL_NOT_CERTIFIED"),
            ("certification", "NOT_CERTIFIED"),
            ("successor_effect", "NONE"),
        ]))

    problem_keys = [x["canonical_key"] for x in load("problems/registry.yaml")["canonical_problems"]]
    by_problem = CommentedMap((key, []) for key in problem_keys)
    direct_keys = [
        "CORPUS-SRC-001", "CORPUS-SRC-002", "CORPUS-SRC-003", "CORPUS-SRC-101", "CORPUS-SRC-102",
        "CORPUS-SRC-103", "CORPUS-SRC-104", "CORPUS-SRC-105", "CORPUS-SRC-108", "CORPUS-SRC-111",
        "CORPUS-SRC-113", "CORPUS-SRC-116",
    ]
    by_source = CommentedMap((key, []) for key in direct_keys)
    by_source["CORPUS-SRC-101-119"] = []
    predecessor_sources = {f"CORPUS-SRC-{number:03d}" for number in range(101, 120)}
    separately_indexed = set(direct_keys) & predecessor_sources
    by_class = CommentedMap((key, []) for key in [
        "SOURCE_SPECIFIC_STUDY", "INTEGRATION_GOVERNANCE_RECORD", "PROBLEM_LOCAL_SYNTHESIS",
        "MIGRATION_TRANSACTION_LEDGER", "PRESERVED_FINDING_BASIS",
    ])
    for record in sets:
        fid = record["finding_set_id"]
        for key in record.get("problem_bindings", []):
            if key in by_problem:
                by_problem[key].append(fid)
        bindings = set(record.get("source_bindings", []))
        for key in direct_keys:
            if key in bindings:
                by_source[key].append(fid)
        if bindings & predecessor_sources and not (len(bindings) == 1 and next(iter(bindings)) in separately_indexed):
            by_source["CORPUS-SRC-101-119"].append(fid)
        cls = record.get("record_class")
        if cls in {"ACTIVE_PREDECESSOR_FINDING_BASIS", "ACCEPTED_MIGRATION_SOURCE_FINDING_BASIS"}:
            by_class["PRESERVED_FINDING_BASIS"].append(fid)
        elif cls in by_class:
            by_class[cls].append(fid)
    data["indexes"]["by_problem"] = by_problem
    data["indexes"]["by_source"] = by_source
    data["indexes"]["by_record_class"] = by_class

    data["coverage"]["finding_sets_registered"] = 57
    data["coverage"]["source_specific_and_integration_records_registered"] = 17
    data["coverage"]["problem_syntheses_registered"] = 35
    data["coverage"]["current_problem_synthesis_tree_yaml_records_accounted_for"] = 35
    data["coverage"]["corpus_study_records_accounted_for"] = 17

    gap = item(data["findings_gaps"], "gap_id", "FINDINGS-GAP-003")
    gap["statement"] = "Ten of the nineteen Theologico-Political writings now have complete provisional item studies; the remaining nine lack individual sequential studies."
    rule = (
        "FINDSET-017 must derive only FINDSET-134 and FINDSET-135, preserve CORPUS-WIT-104, pending original-1952 "
        "comparison, the collective-editorial-layer distinction, noncorroboration, and no-successor safeguards"
    )
    append_unique(data["validation_rules"], rule)
    save(path, data)


def update_manifest() -> None:
    path = "manifest.yaml"
    data = load(path)
    data["identity"]["version"] = "1.14.0"
    data["revision_history"]["predecessor_version"] = "1.13.0"
    data["revision_history"]["predecessor_blob_sha"] = "PRESERVED_BY_GIT"
    data["revision_history"]["reason"] = (
        "Register HUSIK-PREFACE-STUDY-001 as the tenth complete provisional Theologico-Political item study and "
        "synchronize corpus v1.18.0, findings v1.10.0, audit v3.2.0, mapping v1.14.0, process v1.16.0, and schedule "
        "v1.14.0 while preserving nine pending studies, original-1952 comparison, noncertification, predecessor authority, "
        "and the Sanctum repin block."
    )
    data["audit"]["version"] = "3.2.0"
    data["component_completion"]["theologico_political_item_level_source_statuses"] = "19_OF_19_IDENTITIES_19_OF_19_REVIEWED_ITEM_WITNESSES_10_OF_19_COMPLETE_PROVISIONAL_ITEM_STUDIES"
    data["corpus"]["registry_version"] = "1.18.0"
    state = data["corpus"]["theologico_political_item_level_statuses"]
    state["independent_sequential_study_count"] = 10
    state["remaining_without_independent_sequential_study"] = 9
    append_unique(state["completed_study_ids"], "HUSIK-PREFACE-STUDY-001")
    state["rule"] = "All nineteen predecessor items have reviewed witnesses and ten have complete provisional source studies. Witness and study completion remain distinct from independent corroboration, doctrinal certification, migration completion, successor activation, or repository completion."
    data["corpus"]["limitation"] = "All nineteen predecessor writings have bounded identities and reviewed item witnesses. Ten have complete provisional sequential studies; CORPUS-SRC-116 retains an explicit documentary-omission limit, and nine sources still lack independent studies. Textual-state comparisons, independent witnesses, and source-text access remain incomplete."
    data["findings"]["registry_version"] = "1.10.0"
    data["findings"]["newly_registered"] = ["FINDSET-017", "FINDSET-134", "FINDSET-135"]
    save(path, data)


def update_audit() -> None:
    path = "audits/operational-completeness.yaml"
    data = load(path)
    data["identity"]["version"] = "3.2.0"
    data["revision_history"]["predecessor_version"] = "3.1.0"
    data["revision_history"]["predecessor_blob_sha"] = "PRESERVED_BY_GIT"
    data["revision_history"]["reason"] = "Complete HUSIK-PREFACE-STUDY-001, advance Theologico-Political study coverage to ten of nineteen, preserve nine pending studies, and retain the original-1952 comparison and noncorroboration limits."
    data["basis"]["current_revision_scope"] = BRANCH
    completed = data["summary"]["completed_operational_units"]
    for line in [
        "HUSIK-PREFACE-STUDY-001 complete provisional sequential reconstruction",
        "CORPUS-STUDY-017 and FINDSET-017 typed registrations",
        "FINDSET-134 and FINDSET-135 jurisdiction-preserving problem-local syntheses",
    ]:
        append_unique(completed, line)
    state = data["summary"]["theologico_political_item_level_status"]
    state["independently_reconstructed_count_within_this_sequence"] = 10
    state["remaining_without_independent_sequential_study"] = 9
    append_unique(state["completed_source_ids"], "CORPUS-SRC-104")
    append_unique(state["completed_witness_ids"], "CORPUS-WIT-104")
    append_unique(state["completed_study_ids"], "HUSIK-PREFACE-STUDY-001")
    state["witness_only_source_ids"] = [x for x in state["witness_only_source_ids"] if x != "CORPUS-SRC-104"]
    state["witness_only_witness_ids"] = [x for x in state["witness_only_witness_ids"] if x != "CORPUS-WIT-104"]
    state["interpretation_limit"] = "All nineteen predecessor items have reviewed witnesses and ten completed studies are independent reconstructions relative to predecessor and collection-level synthesis. Nine witness registrations remain study-pending; none of the source studies is independent corroboration of represented traditions."
    deficiencies = data["summary"]["remaining_major_deficiencies"]
    deficiencies[0] = "nine Theologico-Political writings still require independent sequential item studies"

    records = data.get("records", [])
    for record in [
        CommentedMap([("path", STUDY_PATH), ("classification", "SUBSTANTIVELY_RECONSTRUCTED"), ("identity", "HUSIK-PREFACE-STUDY-001"), ("present_function", ["reconstructs printed pages 235-266 in ten ordered units while separating argumentative, collective-1952-editorial, and later-1997-editorial layers", "reconstructs free inquiry versus revealed Law, the objectivity problem, the critique of radical historicism, and the jurisprudential justice-science mediation", "preserves Theologico-Political primary and Athens-versus-Jerusalem controlled secondary jurisdiction"]), ("remaining", ["original 1952 Basil Blackwell comparison", "independent Husik, medieval Jewish, Jewish, Greek, Cohenian, Singer, Stammler, and Kelsen witness reconstruction", "later authorized proposition-level migration review"])]),
        CommentedMap([("path", STATUS_PATH), ("classification", "SUBSTANTIVELY_RECONSTRUCTED"), ("present_function", ["registers CORPUS-WIT-104 and HUSIK-PREFACE-STUDY-001 as distinct documentary layers", "preserves printed pages 235-266 / PDF pages 254-285 and the container fingerprint", "preserves collective 1952 editorial and later 1997 Ed. note-layer distinctions"]), ("remaining", ["original 1952 printing comparison", "independent source-tradition reconstruction"])]),
        CommentedMap([("path", TP_SYNTHESIS_PATH), ("classification", "SUBSTANTIVELY_RECONSTRUCTED"), ("identity", "TP-HUSIK-PREFACE-001"), ("present_function", ["supplies the source-local Theologico-Political synthesis without predecessor displacement"]), ("remaining", ["independent witness expansion and any later certified proposition-level migration"])]),
        CommentedMap([("path", AVJ_SYNTHESIS_PATH), ("classification", "SUBSTANTIVELY_RECONSTRUCTED"), ("identity", "AVJ-HUSIK-PREFACE-001"), ("present_function", ["supplies the source-local Hebraism-Hellenism and justice-science synthesis without certifying harmonization"]), ("remaining", ["independent Jewish and Greek witness reconstruction"])]),
    ]:
        if not any(x.get("path") == record["path"] for x in records):
            records.append(record)
    data["records"] = records

    prod = data["production_order"]
    for line in [
        "HUSIK-PREFACE-STUDY-001 with FINDSET-017, FINDSET-134, and FINDSET-135",
    ]:
        append_unique(prod["completed_in_current_sequence"], line)
    prod["next"] = [
        "run complete structural and behavioral validation for the tenth Theologico-Political item study",
        "conduct CORPUS-SRC-106 independent sequential reconstruction from printed pages 285-309",
        "continue the remaining eight independent sequential reconstructions after CORPUS-SRC-106",
        "expand independent source-tradition witnesses and original-edition comparisons",
        "validate actual ministerial reports against the full contract stack",
    ]
    save(path, data)


def update_mapping() -> None:
    path = "migrations/lean-operational-interface.yaml"
    data = load(path)
    data["identity"]["version"] = "1.14.0"
    data["revision_history"]["predecessor_version"] = "1.13.0"
    data["revision_history"]["predecessor_blob_sha"] = "PRESERVED_BY_GIT"
    data["revision_history"]["reason"] = "Synchronize HUSIK-PREFACE-STUDY-001, corpus v1.18.0, findings v1.10.0, audit v3.2.0, process v1.16.0, and schedule v1.14.0 while preserving nine pending studies, the 1952 textual-state limit, noncorroboration, and no successor effect."
    data["completion_audit"]["version"] = "3.2.0"
    data["production_process"]["completed_study_subunit"] = "TEN_OF_19_COMPLETE_PROVISIONAL_NINE_PENDING"

    mappings = data["mappings"]
    corpus = mappings["corpus"]
    corpus["interface"]["registry_version"] = "1.18.0"
    state = corpus["theologico_political_item_level_statuses"]
    state["independent_sequential_study_count"] = 10
    state["remaining_without_independent_sequential_study"] = 9
    append_unique(state["completed_study_ids"], "HUSIK-PREFACE-STUDY-001")
    state["witness_only_source_ids"] = [x for x in state["witness_only_source_ids"] if x != "CORPUS-SRC-104"]
    corpus["present_function"] = [
        "register source entities separately from witnesses and studies",
        "account for all 57 YAML records in the current studies tree",
        "validate all nineteen identities, aliases, scopes, reviewed-witness states, study states, fingerprints, locators, and noncertification",
        "preserve CORPUS-WIT-102 platform-reference safeguards",
        "validate the fingerprinted 1997 SUNY witness batch without converting witness registration into sequential study completion",
        "preserve corpus gaps and original-edition comparison limits",
        "validate HUSIK-PREFACE-STUDY-001 as a complete provisional reconstruction with pending 1952 comparison and no successor effect",
    ]
    corpus["limit"] = "Current-state exhaustiveness, nineteen reviewed item witnesses, and ten complete provisional item studies do not create a complete corpus, supply independent corroboration, resolve documentary omissions, certify findings, or authorize migration and activation."

    for relation in [
        CommentedMap([("path", TP_SYNTHESIS_PATH), ("source", "CORPUS-SRC-104"), ("derivation", "FINDSET-017_TO_FINDSET-134")]),
        CommentedMap([("path", AVJ_SYNTHESIS_PATH), ("source", "CORPUS-SRC-104"), ("derivation", "FINDSET-017_TO_FINDSET-135")]),
    ]:
        if not any(x.get("path") == relation["path"] for x in mappings["problems"]["new_source_relations"]):
            mappings["problems"]["new_source_relations"].append(relation)

    for section in ("hermeneutics", "method"):
        apps = mappings[section].setdefault("source_applications", [])
        if not any(x.get("record") == STUDY_PATH for x in apps):
            entry = CommentedMap([("record", STUDY_PATH), ("state", "COMPLETE_PROVISIONAL_FOR_ONE_REVIEWED_ITEM")])
            if section == "method":
                entry["reading_units"] = 10
            apps.append(entry)

    findings = mappings["findings"]
    findings["interface"]["registry_version"] = "1.10.0"
    findings["newly_registered"] = [
        CommentedMap([("finding_set_id", "FINDSET-017"), ("path", STUDY_PATH)]),
        CommentedMap([("finding_set_id", "FINDSET-134"), ("path", TP_SYNTHESIS_PATH), ("derived_from", "FINDSET-017")]),
        CommentedMap([("finding_set_id", "FINDSET-135"), ("path", AVJ_SYNTHESIS_PATH), ("derived_from", "FINDSET-017")]),
    ]
    data["non_effects"] = [
        "No successor problem is certified or activated.",
        "No active predecessor is displaced and no accepted migration source is superseded.",
        "No source-specific finding is promoted beyond its record-local status.",
        "No source text is admitted or distributed.",
        "Ten completed Theologico-Political source studies are not independent corroboration or repository completion.",
        "CORPUS-WIT-104 remains distinct from HUSIK-PREFACE-STUDY-001 and the original 1952 printing remains unreviewed.",
        "No Assembly authority is conferred; Sanctum validation remains separate.",
    ]
    validations = data["validation_states"]["structural_interface_valid_when"]
    data["validation_states"]["structural_interface_valid_when"] = [
        x.replace("twenty-one synthesis records", "thirty-five synthesis records").replace("thirty-three finding sets", "fifty-seven finding sets")
        if isinstance(x, str) else x
        for x in validations
    ]
    data["completed_production_units"] = [
        "speech, hermeneutic, and method operational contracts",
        "complete read-only foundational problem bundles",
        "typed current-state corpus and findings registries",
        "complete 19-of-19 Theologico-Political source-identity and reviewed-witness range",
        "ten complete provisional Theologico-Political sequential reconstructions through HUSIK-PREFACE-STUDY-001",
        "jurisdiction-preserving source-to-problem syntheses through FINDSET-135",
    ]
    data["next_production_units"] = [
        "validate and merge the bounded CORPUS-SRC-104 production unit",
        "conduct CORPUS-SRC-106 independent sequential reconstruction from the registered witness",
        "continue the remaining eight item studies after CORPUS-SRC-106",
        "expand independent witness reconstruction and original-edition comparison",
        "validate actual candidate ministerial reports",
    ]
    save(path, data)


def update_process() -> None:
    path = "history/production-plans/2026-07-27-ten-step-completion-process.yaml"
    data = load(path)
    data["identity"]["version"] = "1.16.0"
    data["revision_history"]["predecessor_version"] = "1.15.0"
    data["revision_history"]["predecessor_blob_sha"] = "PRESERVED_BY_GIT"
    data["revision_history"]["reason"] = "Complete HUSIK-PREFACE-STUDY-001 as the tenth provisional Theologico-Political sequential reconstruction and advance the next study unit to CORPUS-SRC-106 while preserving the original-1952 comparison limit and nine remaining studies."
    steps = {x["sequence"]: x for x in data["steps"]}
    steps[1]["current_version"] = "3.2.0"
    steps[2]["current_version"] = "1.14.0"
    append_unique(steps[7]["completed"], "the Husik Preface supplies distinct provisional syntheses to Theologico-Political and Athens-versus-Jerusalem")
    append_unique(steps[8]["completed"], "HUSIK-PREFACE-STUDY-001 is complete provisional for CORPUS-WIT-104")
    steps[8]["remaining"][0] = "conduct nine independent sequential item studies, beginning with CORPUS-SRC-106"
    steps[9]["completed_in_current_sequence"][0] = "tests cover all nineteen Theologico-Political reviewed-witness registrations and distinguish the nine witness-only states from the ten completed-study states"
    steps[9]["completed_in_current_sequence"][2] = "tests cover the completed CORPUS-SRC-103, CORPUS-SRC-108, CORPUS-SRC-113, CORPUS-SRC-116, CORPUS-SRC-101, and CORPUS-SRC-104 study integrations while preserving findings derivation, problem jurisdiction, and completion-language consistency"
    data["current_production_unit"] = CommentedMap([
        ("step", 8),
        ("completed_subunit", CommentedMap([
            ("title", "Preface to Isaac Husik, Philosophical Essays independent sequential reconstruction"),
            ("state", "COMPLETE_PROVISIONAL_PENDING_BRANCH_VALIDATION_AND_MERGE"),
            ("source_id", "CORPUS-SRC-104"),
            ("witness_id", "CORPUS-WIT-104"),
            ("study_id", "HUSIK-PREFACE-STUDY-001"),
            ("study_coverage", "INCOMPLETE_10_OF_19"),
        ])),
        ("next_subunit", CommentedMap([
            ("title", "Freud on Moses and Monotheism independent sequential reconstruction"),
            ("source_id", "CORPUS-SRC-106"),
            ("witness_id", "CORPUS-WIT-106"),
            ("following_source", "CORPUS-SRC-107"),
        ])),
    ])
    save(path, data)


def update_schedule() -> None:
    path = "history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml"
    data = load(path)
    data["identity"]["version"] = "1.14.0"
    data["status"]["independent_sequential_study_completion"] = "INCOMPLETE_10_OF_19"
    data["revision_history"]["predecessor_version"] = "1.13.0"
    data["revision_history"]["predecessor_blob_sha"] = "PRESERVED_BY_GIT"
    data["revision_history"]["reason"] = "Complete HUSIK-PREFACE-STUDY-001 from CORPUS-WIT-104, advancing independent sequential study coverage to 10-of-19 and the next study unit to CORPUS-SRC-106 while preserving complete witness coverage, the original-1952 comparison limit, and noncorroboration."
    husik = None
    for group in data["priority_groups"]:
        for rec in group.get("items", []):
            if rec.get("source_id") == "CORPUS-SRC-104":
                husik = rec
                break
    if husik is None:
        raise RuntimeError("SRC104 schedule item missing")
    husik["state"] = "REVIEWED_WITNESS_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDY"
    husik["study_id"] = "HUSIK-PREFACE-STUDY-001"
    husik["next_action"] = "ORIGINAL_1952_PRINTING_COMPARISON_AND_INDEPENDENT_HUSIK_MEDIEVAL_JURISPRUDENTIAL_WITNESS_EXPANSION"
    append_unique(data["selection"]["completed_study_ids"], "HUSIK-PREFACE-STUDY-001")
    data["selection"]["selection_state"] = "NINETEEN_REVIEWED_ITEM_WITNESSES_TEN_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDIES"
    data["selection"]["completed_units"] = [
        "all nineteen predecessor source identities have reviewed witnesses",
        "ten source studies are complete provisional",
        "nine witness-only sources remain pending independent sequential reconstruction",
        "all original-edition and independent-corroboration limits remain explicit",
    ]
    data["termination"]["independent_sequential_reconstruction"] = "INCOMPLETE_10_OF_19"
    data["termination"]["next_item_study"] = "CORPUS-SRC-106"
    data["next_item_study_unit"] = CommentedMap([
        ("source_id", "CORPUS-SRC-106"),
        ("title", "Freud on Moses and Monotheism"),
        ("action", "INDEPENDENT_SEQUENTIAL_RECONSTRUCTION_FROM_REGISTERED_WITNESS"),
        ("prerequisite", "SATISFIED_CORPUS_WIT_106_REGISTERED"),
        ("following_source", "CORPUS-SRC-107"),
    ])
    save(path, data)


def update_python_validators() -> None:
    path = ROOT / "corpus_registry.py"
    text = path.read_text(encoding="utf-8")
    complete_marker = " 'CORPUS-SRC-105': {'status_id': 'CORPUS-STATUS-105',"
    if "'CORPUS-SRC-104': {'status_id': 'CORPUS-STATUS-104',\n                    'witness_id': 'CORPUS-WIT-104',\n                    'study_id': 'CORPUS-STUDY-017'" not in text:
        block = " 'CORPUS-SRC-104': {'status_id': 'CORPUS-STATUS-104',\n                    'witness_id': 'CORPUS-WIT-104',\n                    'study_id': 'CORPUS-STUDY-017',\n                    'internal_study_id': 'HUSIK-PREFACE-STUDY-001',\n                    'study_path': 'studies/theologico-political/preface-to-isaac-husik-philosophical-essays/sequential-reconstruction.yaml',\n                    'witness_record_path': 'studies/theologico-political/preface-to-isaac-husik-philosophical-essays/reviewed-witness.yaml',\n                    'printed_page_range': {'start': 235, 'end': 266},\n                    'pdf_page_range_one_based': {'start': 254, 'end': 285},\n                    'reading_state': 'COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS',\n                    'platform_reference': False},\n"
        text = replace_once(text, complete_marker, block + complete_marker, "insert SRC104 complete contract")
    prefix, witness = text.split("WITNESS_ONLY_TP_ITEMS", 1)
    start = witness.find("{'CORPUS-SRC-104':")
    if start >= 0:
        end = witness.find(" 'CORPUS-SRC-106':", start)
        if end < 0:
            raise RuntimeError("Could not bound SRC104 witness-only block")
        witness = witness[:start] + "{" + witness[end + 1:]
    text = prefix + "WITNESS_ONLY_TP_ITEMS" + witness
    text = text.replace('identity.get("version") != "1.17.0"', 'identity.get("version") != "1.18.0"')
    text = text.replace('identity.version must be 1.17.0', 'identity.version must be 1.18.0')
    text = text.replace('"study records": (len(study_ids), 16)', '"study records": (len(study_ids), 17)')
    text = text.replace('"theologico_political_independent_item_studies_registered": 9', '"theologico_political_independent_item_studies_registered": 10')
    text = text.replace('!= "INCOMPLETE_9_OF_19"', '!= "INCOMPLETE_10_OF_19"')
    text = text.replace('must be INCOMPLETE_9_OF_19', 'must be INCOMPLETE_10_OF_19')
    path.write_text(text, encoding="utf-8")

    path = ROOT / "findings_registry.py"
    text = path.read_text(encoding="utf-8")
    for marker, addition in [
        ('    "problems/athens-vs-jerusalem/synthesis/on-the-interpretation-of-genesis.yaml",\n', '    "problems/athens-vs-jerusalem/synthesis/preface-to-isaac-husik-philosophical-essays.yaml",\n'),
        ('    "problems/theologico-political/synthesis/on-the-interpretation-of-genesis.yaml",\n', '    "problems/theologico-political/synthesis/preface-to-isaac-husik-philosophical-essays.yaml",\n'),
    ]:
        if addition.strip() not in text:
            text = replace_once(text, marker, marker + addition, "add SRC104 expected synthesis path")
    if '    "CORPUS-SRC-104",\n' not in text.split("SOURCE_STUDY_CONTRACTS", 1)[0]:
        text = replace_once(text, '    "CORPUS-SRC-103",\n', '    "CORPUS-SRC-103",\n    "CORPUS-SRC-104",\n', "add SRC104 direct source key")
    text = text.replace('"CORPUS-SRC-103", "CORPUS-SRC-105"', '"CORPUS-SRC-103", "CORPUS-SRC-104", "CORPUS-SRC-105"')
    if '    "FINDSET-017": {' not in text:
        marker = "\n}\n\n\nclass FindingsRegistryError"
        block = '''\n    "FINDSET-017": {\n        "source_id": "CORPUS-SRC-104",\n        "local_syntheses": ["FINDSET-134", "FINDSET-135"],\n        "problem_bindings": {"FINDSET-134": "theologico-political", "FINDSET-135": "athens-vs-jerusalem"},\n        "required_limits": {"witness_id": "CORPUS-WIT-104", "original_1952_printing_comparison": "PENDING", "independent_corroboration": "INCOMPLETE"},\n    },'''
        text = replace_once(text, marker, block + marker, "add FINDSET017 contract")
    text = text.replace('identity.get("version") != "1.9.0"', 'identity.get("version") != "1.10.0"')
    text = text.replace('identity.version must be 1.9.0', 'identity.version must be 1.10.0')
    text = text.replace('if len(finding_ids) != 54:', 'if len(finding_ids) != 57:')
    text = text.replace('expected 54 finding sets', 'expected 57 finding sets')
    path.write_text(text, encoding="utf-8")


def update_tests() -> None:
    replacements = {
        "tests/test_corpus_registry.py": [
            ('"1.17.0"', '"1.18.0"'),
            ('            56,', '            57,'),
            ('registry["coverage"]["study_records_registered"], 16', 'registry["coverage"]["study_records_registered"], 17'),
            ('def test_ten_tp_sources_have_witnesses_but_still_require_study', 'def test_nine_tp_sources_have_witnesses_but_still_require_study'),
            ('self.assertEqual(len(sources), 10)', 'self.assertEqual(len(sources), 9)'),
        ],
        "tests/test_findings_registry.py": [
            ('"1.9.0"', '"1.10.0"'),
            ('self.assertEqual(len(finding_ids), 54)', 'self.assertEqual(len(finding_ids), 57)'),
            ('self.assertEqual(len(registered), 33)', 'self.assertEqual(len(registered), 35)'),
            ('self.assertEqual(len(registered), 16)', 'self.assertEqual(len(registered), 17)'),
        ],
        "tests/test_interface_consistency.py": [
            ('test_nineteen_identity_nineteen_witness_nine_study_language_matches', 'test_nineteen_identity_nineteen_witness_ten_study_language_matches'),
            ('manifest_state["independent_sequential_study_count"], 9', 'manifest_state["independent_sequential_study_count"], 10'),
            ('audit_state["independently_reconstructed_count_within_this_sequence"], 9', 'audit_state["independently_reconstructed_count_within_this_sequence"], 10'),
            ('mapping_state["independent_sequential_study_count"], 9', 'mapping_state["independent_sequential_study_count"], 10'),
            ('manifest_state["remaining_without_independent_sequential_study"], 10', 'manifest_state["remaining_without_independent_sequential_study"], 9'),
            ('mapping_state["remaining_without_independent_sequential_study"], 10', 'mapping_state["remaining_without_independent_sequential_study"], 9'),
            ('"INCOMPLETE_9_OF_19"', '"INCOMPLETE_10_OF_19"'),
            ('"PROGRESS-RETURN-STUDY-001"]', '"PROGRESS-RETURN-STUDY-001", "HUSIK-PREFACE-STUDY-001"]'),
            ('schedule["termination"]["next_item_study"], "CORPUS-SRC-104"', 'schedule["termination"]["next_item_study"], "CORPUS-SRC-106"'),
            ('            "FINDSET-016": [("FINDSET-131", "theologico-political"), ("FINDSET-132", "athens-vs-jerusalem"), ("FINDSET-133", "ancients-vs-moderns")],\n', '            "FINDSET-016": [("FINDSET-131", "theologico-political"), ("FINDSET-132", "athens-vs-jerusalem"), ("FINDSET-133", "ancients-vs-moderns")],\n            "FINDSET-017": [("FINDSET-134", "theologico-political"), ("FINDSET-135", "athens-vs-jerusalem")],\n'),
        ],
        "tests/test_tp_witness_coverage_complete.py": [
            ('theologico_political_independent_item_studies_registered"], 9', 'theologico_political_independent_item_studies_registered"], 10'),
            ('"INCOMPLETE_9_OF_19"', '"INCOMPLETE_10_OF_19"'),
            ('def test_ten_witness_only_items_remain_noncertified_and_unstudied', 'def test_nine_witness_only_items_remain_noncertified_and_unstudied'),
            ('"CORPUS-SRC-113", "CORPUS-SRC-116", "CORPUS-SRC-101"}', '"CORPUS-SRC-113", "CORPUS-SRC-116", "CORPUS-SRC-101", "CORPUS-SRC-104"}'),
            ('self.assertEqual(len(witness_only), 10)', 'self.assertEqual(len(witness_only), 9)'),
        ],
        "tests/test_corpus_wit_102_platform_registration.py": [
            ('"INCOMPLETE_9_OF_19"', '"INCOMPLETE_10_OF_19"'),
        ],
        "tests/test_pr21_talmon_completion.py": [
            ('manifest["identity"]["version"], "1.13.0"', 'manifest["identity"]["version"], "1.14.0"'),
            ('audit["identity"]["version"], "3.1.0"', 'audit["identity"]["version"], "3.2.0"'),
            ('mapping["identity"]["version"], "1.13.0"', 'mapping["identity"]["version"], "1.14.0"'),
            ('process["identity"]["version"], "1.15.0"', 'process["identity"]["version"], "1.16.0"'),
            ('schedule["identity"]["version"], "1.13.0"', 'schedule["identity"]["version"], "1.14.0"'),
            ('corpus["identity"]["version"], "1.17.0"', 'corpus["identity"]["version"], "1.18.0"'),
            ('findings["identity"]["version"], "1.9.0"', 'findings["identity"]["version"], "1.10.0"'),
            ('state["independent_sequential_study_count"], 9', 'state["independent_sequential_study_count"], 10'),
            ('state["remaining_without_independent_sequential_study"], 10', 'state["remaining_without_independent_sequential_study"], 9'),
            ('"PROGRESS-RETURN-STUDY-001"],', '"PROGRESS-RETURN-STUDY-001", "HUSIK-PREFACE-STUDY-001"],'),
            ('schedule["termination"]["next_item_study"], "CORPUS-SRC-104"', 'schedule["termination"]["next_item_study"], "CORPUS-SRC-106"'),
        ],
    }
    for rel, pairs in replacements.items():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        for old, new in pairs:
            if old in text:
                text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")


def main() -> int:
    for required in [STUDY_PATH, STATUS_PATH, TP_SYNTHESIS_PATH, AVJ_SYNTHESIS_PATH]:
        if not (ROOT / required).is_file():
            raise RuntimeError(f"Required SRC104 production artifact missing: {required}")
    update_corpus_index()
    update_findings_index()
    update_manifest()
    update_audit()
    update_mapping()
    update_process()
    update_schedule()
    update_python_validators()
    update_tests()
    print("SRC104 integration materialized; ordinary repository validation remains required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
