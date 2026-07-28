#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "production/corpus-src-106-sequential-reconstruction"
STUDY_PATH = "studies/theologico-political/freud-on-moses-and-monotheism/sequential-reconstruction.yaml"
STATUS_PATH = "studies/theologico-political/freud-on-moses-and-monotheism/source-status.yaml"
TP_SYNTHESIS_PATH = "problems/theologico-political/synthesis/freud-on-moses-and-monotheism.yaml"
AVM_SYNTHESIS_PATH = "problems/ancients-vs-moderns/synthesis/freud-on-moses-and-monotheism.yaml"
TRANSCRIPT_LIMIT = "NOT_REVIEWED_OR_FORMALLY_APPROVED_BY_STRAUSS_AS_FAR_AS_COLLECTION_EDITOR_CAN_DETERMINE"

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
    if data["identity"]["version"] != "1.18.0":
        raise RuntimeError("Unexpected corpus registry predecessor version")
    data["identity"]["version"] = "1.19.0"
    data["revision_history"]["predecessor_version"] = "1.18.0"
    data["revision_history"]["predecessor_blob_sha"] = "PRESERVED_BY_GIT"
    data["revision_history"]["transformation"] = "SUBSTANTIVE_FORWARD_REVISION"
    data["revision_history"]["reason"] = (
        "Register FREUD-MOSES-STUDY-001 as the eleventh complete provisional Theologico-Political item study, "
        "register CORPUS-STUDY-018, preserve the posthumous unknown-transcriber and editor-emendation limits, and "
        "retain noncorroboration, noncertification, predecessor authority, and no successor effect."
    )

    src = item(data["source_entities"], "source_id", "CORPUS-SRC-106")
    src["item_level_source_status"] = "REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION"
    src["study_status"] = "COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS_WITH_TRANSCRIPTION_LIMIT"
    src["study_records"] = ["CORPUS-STUDY-018"]
    src["limits"] = [
        "reviewed witness is the fingerprinted 1997 SUNY collected publication of a lecture transcription, not an authorially reviewed manuscript",
        "printed pages 285-309 correspond to one-based PDF pages 304-328; lecture body ends and Green's notes begin on printed page 306",
        "the collection editor reports an unknown transcriber worked from a tape and that Strauss appears not to have reviewed or formally approved the transcribed version",
        "the collection editor reports limited additions and corrections to spoken verb tenses in one paragraph and states the notes are entirely his work",
        "FREUD-MOSES-STUDY-001 is source-local and not independent corroboration of Freud, biblical sources, psychoanalysis, Egyptology, ethnology, Plato, Nietzsche, or represented traditions",
    ]

    status = item(data["source_status_records"], "status_id", "CORPUS-STATUS-106")
    status["completion"] = "REVIEWED_ITEM_WITNESS_REGISTERED_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_RECONSTRUCTION"

    if not any(record.get("study_id") == "CORPUS-STUDY-018" for record in data["study_records"]):
        data["study_records"].append(CommentedMap([
            ("study_id", "CORPUS-STUDY-018"),
            ("source_id", "CORPUS-SRC-106"),
            ("path", STUDY_PATH),
            ("record_role", "SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION"),
            ("completion", "COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS_WITH_TRANSCRIPTION_LIMIT"),
            ("certification", "NOT_CERTIFIED"),
        ]))

    coverage = data["coverage"]
    coverage["study_records_registered"] = 18
    coverage["theologico_political_independent_item_studies_registered"] = 11
    coverage["current_studies_tree_yaml_records_accounted_for"] = 58

    gap = item(data["corpus_gaps"], "gap_id", "CORPUS-GAP-003")
    gap["statement"] = (
        "All nineteen predecessor writings have bounded source identities and reviewed item witnesses; eleven have "
        "complete provisional sequential studies, while the remaining eight lack independent item studies."
    )

    append_unique(
        data["validation_rules"],
        "CORPUS-SRC-106 preserves the fingerprinted reviewed transcript, unknown-transcriber and editorial-emendation limits, complete provisional sequential reconstruction, noncorroboration, noncertification, and no-successor safeguards",
    )
    data["validation_rules"] = [
        r.replace("all nine witness-only Theologico-Political sources", "all eight witness-only Theologico-Political sources")
        if isinstance(r, str) else r
        for r in data["validation_rules"]
    ]

    term = data["termination"]
    term["theologico_political_independent_study_state"] = "INCOMPLETE_11_OF_19"
    term["next_required_units"] = [
        "conduct independent sequential reconstruction of CORPUS-SRC-107 from CORPUS-WIT-107",
        "seek any surviving tape, prepared notes, authorially reviewed transcript, or earlier textual state of CORPUS-SRC-106 only through later separately verified documentary acquisition",
        "conduct independent sequential reconstruction for the remaining eight writings",
        "expand independent biblical, Greek, Jewish, Christian, Spinozist, Freudian, psychoanalytic, medieval, modern, and reviewed-work witnesses",
    ]
    save(path, data)


def update_findings_index() -> None:
    path = "findings/index.yaml"
    data = load(path)
    if data["identity"]["version"] != "1.10.0":
        raise RuntimeError("Unexpected findings registry predecessor version")
    data["identity"]["version"] = "1.11.0"
    data["revision_history"]["predecessor_version"] = "1.10.0"
    data["revision_history"]["predecessor_blob_sha"] = "PRESERVED_BY_GIT"
    data["revision_history"]["transformation"] = "SUBSTANTIVE_FORWARD_REVISION"
    data["revision_history"]["reason"] = (
        "Register FREUD-MOSES-STUDY-001 as FINDSET-018 and jurisdiction-preserving syntheses FINDSET-136 and FINDSET-137 "
        "while preserving the posthumous-transcription, authorial-approval, editorial-emendation, noncorroboration, "
        "noncertification, and no-successor safeguards."
    )

    sets = data["finding_sets"]
    if not any(x.get("finding_set_id") == "FINDSET-018" for x in sets):
        insert_at = next(i for i, x in enumerate(sets) if x.get("finding_set_id") == "FINDSET-101")
        sets.insert(insert_at, CommentedMap([
            ("finding_set_id", "FINDSET-018"),
            ("path", STUDY_PATH),
            ("record_class", "SOURCE_SPECIFIC_STUDY"),
            ("record_role", "SOURCE_SPECIFIC_SEQUENTIAL_RECONSTRUCTION"),
            ("source_bindings", ["CORPUS-SRC-106"]),
            ("problem_bindings", ["theologico-political", "ancients-vs-moderns"]),
            ("status", "COMPLETE_PROVISIONAL_FOR_REVIEWED_1997_COLLECTED_WITNESS_WITH_TRANSCRIPTION_LIMIT"),
            ("certification", "NOT_CERTIFIED"),
            ("derived_local_syntheses", ["FINDSET-136", "FINDSET-137"]),
            ("witness_id", "CORPUS-WIT-106"),
            ("transcript_authorial_approval", TRANSCRIPT_LIMIT),
            ("documentary_transmission_limit", "ACTIVE"),
            ("earlier_publication_or_textual_state_comparison", "PENDING_IF_LATER_IDENTIFIED_OR_ACQUIRED"),
            ("independent_corroboration", "INCOMPLETE"),
            ("successor_effect", "NONE"),
        ]))
    if not any(x.get("finding_set_id") == "FINDSET-136" for x in sets):
        insert_at = next(i for i, x in enumerate(sets) if x.get("finding_set_id") == "FINDSET-201")
        sets.insert(insert_at, CommentedMap([
            ("finding_set_id", "FINDSET-136"),
            ("path", TP_SYNTHESIS_PATH),
            ("record_class", "PROBLEM_LOCAL_SYNTHESIS"),
            ("record_role", "SOURCE_TO_PROBLEM_SYNTHESIS"),
            ("source_bindings", ["CORPUS-SRC-106"]),
            ("problem_bindings", ["theologico-political"]),
            ("adjacent_problem_references", ["ancients-vs-moderns"]),
            ("derived_from", ["FINDSET-018"]),
            ("status", "PROVISIONAL_NOT_CERTIFIED"),
            ("certification", "NOT_CERTIFIED"),
            ("successor_effect", "NONE"),
        ]))
        sets.insert(insert_at + 1, CommentedMap([
            ("finding_set_id", "FINDSET-137"),
            ("path", AVM_SYNTHESIS_PATH),
            ("record_class", "PROBLEM_LOCAL_SYNTHESIS"),
            ("record_role", "SOURCE_TO_PROBLEM_SYNTHESIS"),
            ("source_bindings", ["CORPUS-SRC-106"]),
            ("problem_bindings", ["ancients-vs-moderns"]),
            ("theologico_political_reference", "theologico-political"),
            ("derived_from", ["FINDSET-018"]),
            ("status", "PROVISIONAL_NOT_CERTIFIED"),
            ("certification", "NOT_CERTIFIED"),
            ("successor_effect", "NONE"),
        ]))

    problem_keys = [x["canonical_key"] for x in load("problems/registry.yaml")["canonical_problems"]]
    by_problem = CommentedMap((key, []) for key in problem_keys)
    direct_keys = [
        "CORPUS-SRC-001", "CORPUS-SRC-002", "CORPUS-SRC-003", "CORPUS-SRC-101", "CORPUS-SRC-102",
        "CORPUS-SRC-103", "CORPUS-SRC-104", "CORPUS-SRC-105", "CORPUS-SRC-106", "CORPUS-SRC-108",
        "CORPUS-SRC-111", "CORPUS-SRC-113", "CORPUS-SRC-116",
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

    data["coverage"]["finding_sets_registered"] = 60
    data["coverage"]["source_specific_and_integration_records_registered"] = 18
    data["coverage"]["problem_syntheses_registered"] = 37
    data["coverage"]["current_problem_synthesis_tree_yaml_records_accounted_for"] = 37
    data["coverage"]["corpus_study_records_accounted_for"] = 18

    gap = item(data["findings_gaps"], "gap_id", "FINDINGS-GAP-003")
    gap["statement"] = "Eleven of the nineteen Theologico-Political writings now have complete provisional item studies; the remaining eight lack individual sequential studies."
    append_unique(
        data["validation_rules"],
        "FINDSET-018 must derive only FINDSET-136 and FINDSET-137, preserve CORPUS-WIT-106, the posthumous unknown-transcriber and editor-emendation limits, incomplete independent corroboration, and no-successor safeguards",
    )
    save(path, data)


def update_manifest() -> None:
    path = "manifest.yaml"
    data = load(path)
    if data["identity"]["version"] != "1.14.0":
        raise RuntimeError("Unexpected manifest predecessor version")
    data["identity"]["version"] = "1.15.0"
    data["revision_history"]["predecessor_version"] = "1.14.0"
    data["revision_history"]["predecessor_blob_sha"] = "PRESERVED_BY_GIT"
    data["revision_history"]["reason"] = (
        "Register FREUD-MOSES-STUDY-001 as the eleventh complete provisional Theologico-Political item study and "
        "synchronize corpus v1.19.0, findings v1.11.0, audit v3.3.0, mapping v1.15.0, process v1.17.0, and schedule "
        "v1.15.0 while preserving eight pending studies, the posthumous transcription limit, noncertification, predecessor "
        "authority, and the Sanctum repin block."
    )
    data["audit"]["version"] = "3.3.0"
    data["component_completion"]["theologico_political_item_level_source_statuses"] = "19_OF_19_IDENTITIES_19_OF_19_REVIEWED_ITEM_WITNESSES_11_OF_19_COMPLETE_PROVISIONAL_ITEM_STUDIES"
    data["corpus"]["registry_version"] = "1.19.0"
    state = data["corpus"]["theologico_political_item_level_statuses"]
    state["independent_sequential_study_count"] = 11
    state["remaining_without_independent_sequential_study"] = 8
    append_unique(state["completed_study_ids"], "FREUD-MOSES-STUDY-001")
    state["rule"] = "All nineteen predecessor items have reviewed witnesses and eleven have complete provisional source studies. Witness and study completion remain distinct from independent corroboration, doctrinal certification, migration completion, successor activation, or repository completion."
    data["corpus"]["limitation"] = "All nineteen predecessor writings have bounded identities and reviewed item witnesses. Eleven have complete provisional sequential studies; CORPUS-SRC-116 retains an explicit documentary-omission limit, CORPUS-SRC-106 retains an explicit posthumous-transcription and editorial-emendation limit, and eight sources still lack independent studies. Textual-state comparisons, independent witnesses, and source-text access remain incomplete."
    data["findings"]["registry_version"] = "1.11.0"
    data["findings"]["newly_registered"] = ["FINDSET-018", "FINDSET-136", "FINDSET-137"]
    save(path, data)


def update_audit() -> None:
    path = "audits/operational-completeness.yaml"
    data = load(path)
    if data["identity"]["version"] != "3.2.0":
        raise RuntimeError("Unexpected audit predecessor version")
    data["identity"]["version"] = "3.3.0"
    data["revision_history"]["predecessor_version"] = "3.2.0"
    data["revision_history"]["predecessor_blob_sha"] = "PRESERVED_BY_GIT"
    data["revision_history"]["reason"] = "Complete FREUD-MOSES-STUDY-001, advance Theologico-Political study coverage to eleven of nineteen, preserve eight pending studies, and retain the unknown-transcriber, authorial-approval, editor-emendation, and noncorroboration limits."
    data["basis"]["current_revision_scope"] = BRANCH
    completed = data["summary"]["completed_operational_units"]
    for line in [
        "FREUD-MOSES-STUDY-001 complete provisional sequential reconstruction with active transcription limit",
        "CORPUS-STUDY-018 and FINDSET-018 typed registrations",
        "FINDSET-136 and FINDSET-137 jurisdiction-preserving problem-local syntheses",
    ]:
        append_unique(completed, line)
    state = data["summary"]["theologico_political_item_level_status"]
    state["independently_reconstructed_count_within_this_sequence"] = 11
    state["remaining_without_independent_sequential_study"] = 8
    append_unique(state["completed_source_ids"], "CORPUS-SRC-106")
    append_unique(state["completed_witness_ids"], "CORPUS-WIT-106")
    append_unique(state["completed_study_ids"], "FREUD-MOSES-STUDY-001")
    state["witness_only_source_ids"] = [x for x in state["witness_only_source_ids"] if x != "CORPUS-SRC-106"]
    state["witness_only_witness_ids"] = [x for x in state["witness_only_witness_ids"] if x != "CORPUS-WIT-106"]
    state["interpretation_limit"] = "All nineteen predecessor items have reviewed witnesses and eleven completed studies are independent reconstructions relative to predecessor and collection-level synthesis. Eight witness registrations remain study-pending; none of the source studies is independent corroboration of represented traditions, and CORPUS-SRC-106 retains an active posthumous-transcription and editorial-emendation limit."
    deficiencies = data["summary"]["remaining_major_deficiencies"]
    deficiencies[0] = "eight Theologico-Political writings still require independent sequential item studies"

    records = data.get("records", [])
    for record in [
        CommentedMap([("path", STUDY_PATH), ("classification", "SUBSTANTIVELY_RECONSTRUCTED_WITH_DOCUMENTARY_LIMIT"), ("identity", "FREUD-MOSES-STUDY-001"), ("present_function", ["reconstructs the lecture body on printed pages 285-306 before treating Green's notes on pages 306-309 as a separate editorial layer", "tests historical and psychological explanation against evidence, truth, revelation, ancient law, science, and philosophy", "preserves Theologico-Political primary and Ancients-versus-Moderns controlled secondary jurisdiction", "preserves the unknown-transcriber, apparent nonapproval, and limited editor-emendation transmission conditions"]), ("remaining", ["independent Freud, biblical, psychoanalytic, Egyptological, ethnological, Platonic, and Nietzschean reconstruction", "any later verified tape, prepared notes, authorially checked transcript, or earlier textual state", "later authorized proposition-level migration review"])]),
        CommentedMap([("path", STATUS_PATH), ("classification", "SUBSTANTIVELY_RECONSTRUCTED_WITH_DOCUMENTARY_LIMIT"), ("present_function", ["registers CORPUS-WIT-106 and FREUD-MOSES-STUDY-001 as distinct documentary layers", "preserves printed pages 285-309 / PDF pages 304-328 and the container fingerprint", "preserves the posthumous transcription, authorial-approval, editor-note, and limited-emendation conditions"]), ("remaining", ["independent source-tradition reconstruction", "later textual-state comparison if a separately verified witness becomes available"])]),
        CommentedMap([("path", TP_SYNTHESIS_PATH), ("classification", "SUBSTANTIVELY_RECONSTRUCTED"), ("identity", "TP-FREUD-MOSES-001"), ("present_function", ["supplies the source-local Theologico-Political synthesis without predecessor displacement"]), ("remaining", ["independent witness expansion and any later certified proposition-level migration"])]),
        CommentedMap([("path", AVM_SYNTHESIS_PATH), ("classification", "SUBSTANTIVELY_RECONSTRUCTED"), ("identity", "AVM-FREUD-MOSES-001"), ("present_function", ["supplies the source-local ancient-modern synthesis concerning rationality standards, law, science, mystery, and the last man without absorbing the primary jurisdiction"]), ("remaining", ["independent Platonic, Nietzschean, scientific, and historical witness reconstruction"])]),
    ]:
        if not any(x.get("path") == record["path"] for x in records):
            records.append(record)
    data["records"] = records

    prod = data["production_order"]
    append_unique(prod["completed_in_current_sequence"], "FREUD-MOSES-STUDY-001 with FINDSET-018, FINDSET-136, and FINDSET-137")
    prod["next"] = [
        "run complete structural and behavioral validation for the eleventh Theologico-Political item study",
        "conduct CORPUS-SRC-107 independent sequential reconstruction from printed pages 311-356",
        "continue the remaining seven independent sequential reconstructions after CORPUS-SRC-107",
        "expand independent source-tradition witnesses and textual-state comparisons",
        "validate actual ministerial reports against the full contract stack",
    ]
    save(path, data)


def update_mapping() -> None:
    path = "migrations/lean-operational-interface.yaml"
    data = load(path)
    if data["identity"]["version"] != "1.14.0":
        raise RuntimeError("Unexpected mapping predecessor version")
    data["identity"]["version"] = "1.15.0"
    data["revision_history"]["predecessor_version"] = "1.14.0"
    data["revision_history"]["predecessor_blob_sha"] = "PRESERVED_BY_GIT"
    data["revision_history"]["reason"] = "Synchronize FREUD-MOSES-STUDY-001, corpus v1.19.0, findings v1.11.0, audit v3.3.0, process v1.17.0, and schedule v1.15.0 while preserving eight pending studies, the posthumous-transcription limit, noncorroboration, and no successor effect."
    data["completion_audit"]["version"] = "3.3.0"
    data["production_process"]["completed_study_subunit"] = "ELEVEN_OF_19_COMPLETE_PROVISIONAL_EIGHT_PENDING"

    mappings = data["mappings"]
    corpus = mappings["corpus"]
    corpus["interface"]["registry_version"] = "1.19.0"
    state = corpus["theologico_political_item_level_statuses"]
    state["independent_sequential_study_count"] = 11
    state["remaining_without_independent_sequential_study"] = 8
    append_unique(state["completed_study_ids"], "FREUD-MOSES-STUDY-001")
    state["witness_only_source_ids"] = [x for x in state["witness_only_source_ids"] if x != "CORPUS-SRC-106"]
    corpus["present_function"] = [
        "register source entities separately from witnesses and studies",
        "account for all 58 YAML records in the current studies tree",
        "validate all nineteen identities, aliases, scopes, reviewed-witness states, study states, fingerprints, locators, and noncertification",
        "preserve CORPUS-WIT-102 platform-reference safeguards",
        "validate the fingerprinted 1997 SUNY witness batch without converting witness registration into sequential study completion",
        "preserve corpus gaps and textual-state comparison limits",
        "validate FREUD-MOSES-STUDY-001 as a complete provisional reconstruction with active unknown-transcriber, apparent nonapproval, and editor-emendation limits and no successor effect",
    ]
    corpus["limit"] = "Current-state exhaustiveness, nineteen reviewed item witnesses, and eleven complete provisional item studies do not create a complete corpus, supply independent corroboration, resolve documentary transmission limits, certify findings, or authorize migration and activation."

    for relation in [
        CommentedMap([("path", TP_SYNTHESIS_PATH), ("source", "CORPUS-SRC-106"), ("derivation", "FINDSET-018_TO_FINDSET-136")]),
        CommentedMap([("path", AVM_SYNTHESIS_PATH), ("source", "CORPUS-SRC-106"), ("derivation", "FINDSET-018_TO_FINDSET-137")]),
    ]:
        if not any(x.get("path") == relation["path"] for x in mappings["problems"]["new_source_relations"]):
            mappings["problems"]["new_source_relations"].append(relation)

    for section in ("hermeneutics", "method"):
        apps = mappings[section].setdefault("source_applications", [])
        if not any(x.get("record") == STUDY_PATH for x in apps):
            entry = CommentedMap([("record", STUDY_PATH), ("state", "COMPLETE_PROVISIONAL_FOR_ONE_REVIEWED_ITEM_WITH_DOCUMENTARY_LIMIT")])
            if section == "method":
                entry["reading_units"] = 12
            apps.append(entry)

    findings = mappings["findings"]
    findings["interface"]["registry_version"] = "1.11.0"
    findings["newly_registered"] = [
        CommentedMap([("finding_set_id", "FINDSET-018"), ("path", STUDY_PATH)]),
        CommentedMap([("finding_set_id", "FINDSET-136"), ("path", TP_SYNTHESIS_PATH), ("derived_from", "FINDSET-018")]),
        CommentedMap([("finding_set_id", "FINDSET-137"), ("path", AVM_SYNTHESIS_PATH), ("derived_from", "FINDSET-018")]),
    ]
    data["non_effects"] = [
        "No successor problem is certified or activated.",
        "No active predecessor is displaced and no accepted migration source is superseded.",
        "No source-specific finding is promoted beyond its record-local status.",
        "No source text is admitted or distributed.",
        "Eleven completed Theologico-Political source studies are not independent corroboration or repository completion.",
        "CORPUS-WIT-106 remains distinct from FREUD-MOSES-STUDY-001 and its posthumous transcription and editorial limits remain active.",
        "No Assembly authority is conferred; Sanctum validation remains separate.",
    ]
    data["completed_production_units"] = [
        "speech, hermeneutic, and method operational contracts",
        "complete read-only foundational problem bundles",
        "typed current-state corpus and findings registries",
        "complete 19-of-19 Theologico-Political source-identity and reviewed-witness range",
        "eleven complete provisional Theologico-Political sequential reconstructions through FREUD-MOSES-STUDY-001",
        "jurisdiction-preserving source-to-problem syntheses through FINDSET-137",
    ]
    data["next_production_units"] = [
        "validate and merge the bounded CORPUS-SRC-106 production unit",
        "conduct CORPUS-SRC-107 independent sequential reconstruction from the registered witness",
        "continue the remaining seven item studies after CORPUS-SRC-107",
        "expand independent witness reconstruction and textual-state comparison",
        "validate actual candidate ministerial reports",
    ]
    save(path, data)


def update_process() -> None:
    path = "history/production-plans/2026-07-27-ten-step-completion-process.yaml"
    data = load(path)
    if data["identity"]["version"] != "1.16.0":
        raise RuntimeError("Unexpected process predecessor version")
    data["identity"]["version"] = "1.17.0"
    data["revision_history"]["predecessor_version"] = "1.16.0"
    data["revision_history"]["predecessor_blob_sha"] = "PRESERVED_BY_GIT"
    data["revision_history"]["reason"] = "Complete FREUD-MOSES-STUDY-001 as the eleventh provisional Theologico-Political sequential reconstruction and advance the next study unit to CORPUS-SRC-107 while preserving the posthumous-transcription limit and eight remaining studies."
    steps = {x["sequence"]: x for x in data["steps"]}
    steps[1]["current_version"] = "3.3.0"
    steps[2]["current_version"] = "1.15.0"
    append_unique(steps[7]["completed"], "Freud on Moses and Monotheism supplies distinct provisional syntheses to Theologico-Political and Ancients-versus-Moderns with an explicit posthumous-transcription limit")
    append_unique(steps[8]["completed"], "FREUD-MOSES-STUDY-001 is complete provisional for CORPUS-WIT-106 with an active transcription and editorial-emendation limit")
    steps[8]["remaining"][0] = "conduct eight independent sequential item studies, beginning with CORPUS-SRC-107"
    steps[9]["completed_in_current_sequence"][0] = "tests cover all nineteen Theologico-Political reviewed-witness registrations and distinguish the eight witness-only states from the eleven completed-study states"
    steps[9]["completed_in_current_sequence"][2] = "tests cover the completed study integrations through CORPUS-SRC-106 while preserving findings derivation, problem jurisdiction, transmission limits, and completion-language consistency"
    data["current_production_unit"] = CommentedMap([
        ("step", 8),
        ("completed_subunit", CommentedMap([
            ("title", "Freud on Moses and Monotheism independent sequential reconstruction"),
            ("state", "COMPLETE_PROVISIONAL_PENDING_BRANCH_VALIDATION_AND_MERGE"),
            ("source_id", "CORPUS-SRC-106"),
            ("witness_id", "CORPUS-WIT-106"),
            ("study_id", "FREUD-MOSES-STUDY-001"),
            ("study_coverage", "INCOMPLETE_11_OF_19"),
            ("documentary_limit", "POSTHUMOUS_UNKNOWN_TRANSCRIBER_APPARENT_NONAPPROVAL_AND_LIMITED_EDITORIAL_EMENDATION"),
        ])),
        ("next_subunit", CommentedMap([
            ("title", "Why We Remain Jews independent sequential reconstruction"),
            ("source_id", "CORPUS-SRC-107"),
            ("witness_id", "CORPUS-WIT-107"),
            ("following_source", "CORPUS-SRC-112"),
        ])),
    ])
    save(path, data)


def update_schedule() -> None:
    path = "history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml"
    data = load(path)
    if data["identity"]["version"] != "1.14.0":
        raise RuntimeError("Unexpected schedule predecessor version")
    data["identity"]["version"] = "1.15.0"
    data["status"]["independent_sequential_study_completion"] = "INCOMPLETE_11_OF_19"
    data["revision_history"]["predecessor_version"] = "1.14.0"
    data["revision_history"]["predecessor_blob_sha"] = "PRESERVED_BY_GIT"
    data["revision_history"]["reason"] = "Complete FREUD-MOSES-STUDY-001 from CORPUS-WIT-106, advancing independent sequential study coverage to 11-of-19 and the next study unit to CORPUS-SRC-107 while preserving complete witness coverage, the posthumous-transcription limit, and noncorroboration."
    src = None
    for group in data["priority_groups"]:
        for rec in group.get("items", []):
            if rec.get("source_id") == "CORPUS-SRC-106":
                src = rec
                break
    if src is None:
        raise RuntimeError("SRC106 schedule item missing")
    src["state"] = "REVIEWED_WITNESS_AND_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDY_WITH_TRANSCRIPTION_LIMIT"
    src["study_id"] = "FREUD-MOSES-STUDY-001"
    src["next_action"] = "SEEK_VERIFIED_TAPE_NOTES_OR_AUTHORIAL_TEXTUAL_STATE_AND_EXPAND_INDEPENDENT_FREUD_BIBLICAL_PHILOSOPHICAL_WITNESSES"
    append_unique(data["selection"]["completed_study_ids"], "FREUD-MOSES-STUDY-001")
    data["selection"]["selection_state"] = "NINETEEN_REVIEWED_ITEM_WITNESSES_ELEVEN_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDIES"
    data["selection"]["completed_units"] = [
        "all nineteen predecessor source identities have reviewed witnesses",
        "eleven source studies are complete provisional",
        "eight witness-only sources remain pending independent sequential reconstruction",
        "all textual-state, transcription, and independent-corroboration limits remain explicit",
    ]
    data["termination"]["independent_sequential_reconstruction"] = "INCOMPLETE_11_OF_19"
    data["termination"]["next_item_study"] = "CORPUS-SRC-107"
    data["next_item_study_unit"] = CommentedMap([
        ("source_id", "CORPUS-SRC-107"),
        ("title", "Why We Remain Jews"),
        ("action", "INDEPENDENT_SEQUENTIAL_RECONSTRUCTION_FROM_REGISTERED_WITNESS"),
        ("prerequisite", "SATISFIED_CORPUS_WIT_107_REGISTERED"),
        ("following_source", "CORPUS-SRC-112"),
    ])
    save(path, data)


def update_python_validators() -> None:
    path = ROOT / "corpus_registry.py"
    text = path.read_text(encoding="utf-8")
    complete_marker = " 'CORPUS-SRC-108': {'status_id': 'CORPUS-STATUS-108',"
    if "'CORPUS-SRC-106': {'status_id': 'CORPUS-STATUS-106',\n                    'witness_id': 'CORPUS-WIT-106',\n                    'study_id': 'CORPUS-STUDY-018'" not in text:
        block = " 'CORPUS-SRC-106': {'status_id': 'CORPUS-STATUS-106',\n                    'witness_id': 'CORPUS-WIT-106',\n                    'study_id': 'CORPUS-STUDY-018',\n                    'internal_study_id': 'FREUD-MOSES-STUDY-001',\n                    'study_path': 'studies/theologico-political/freud-on-moses-and-monotheism/sequential-reconstruction.yaml',\n                    'witness_record_path': 'studies/theologico-political/freud-on-moses-and-monotheism/reviewed-witness.yaml',\n                    'printed_page_range': {'start': 285, 'end': 309},\n                    'pdf_page_range_one_based': {'start': 304, 'end': 328},\n                    'reading_state': 'COMPLETE_FOR_REVIEWED_1997_COLLECTED_WITNESS',\n                    'platform_reference': False},\n"
        text = replace_once(text, complete_marker, block + complete_marker, "insert SRC106 complete contract")
    prefix, witness = text.split("WITNESS_ONLY_TP_ITEMS", 1)
    start = witness.find("{'CORPUS-SRC-106':")
    if start >= 0:
        end = witness.find(" 'CORPUS-SRC-107':", start)
        if end < 0:
            raise RuntimeError("Could not bound SRC106 witness-only block")
        witness = witness[:start] + "{" + witness[end + 1:]
    text = prefix + "WITNESS_ONLY_TP_ITEMS" + witness
    text = text.replace('identity.get("version") != "1.18.0"', 'identity.get("version") != "1.19.0"')
    text = text.replace('identity.version must be 1.18.0', 'identity.version must be 1.19.0')
    text = text.replace('"study records": (len(study_ids), 17)', '"study records": (len(study_ids), 18)')
    text = text.replace('"theologico_political_independent_item_studies_registered": 10', '"theologico_political_independent_item_studies_registered": 11')
    text = text.replace('!= "INCOMPLETE_10_OF_19"', '!= "INCOMPLETE_11_OF_19"')
    text = text.replace('must be INCOMPLETE_10_OF_19', 'must be INCOMPLETE_11_OF_19')
    path.write_text(text, encoding="utf-8")

    path = ROOT / "findings_registry.py"
    text = path.read_text(encoding="utf-8")
    for marker, addition in [
        ('    "problems/ancients-vs-moderns/synthesis/hermann-cohen-religion-of-reason.yaml",\n', '    "problems/ancients-vs-moderns/synthesis/freud-on-moses-and-monotheism.yaml",\n'),
        ('    "problems/theologico-political/synthesis/hermann-cohen-religion-of-reason.yaml",\n', '    "problems/theologico-political/synthesis/freud-on-moses-and-monotheism.yaml",\n'),
    ]:
        if addition.strip() not in text:
            text = replace_once(text, marker, addition + marker, "add SRC106 expected synthesis path")
    prefix = text.split("SOURCE_STUDY_CONTRACTS", 1)[0]
    if '    "CORPUS-SRC-106",\n' not in prefix:
        text = replace_once(text, '    "CORPUS-SRC-105",\n', '    "CORPUS-SRC-105",\n    "CORPUS-SRC-106",\n', "add SRC106 direct source key")
    text = text.replace('"CORPUS-SRC-104", "CORPUS-SRC-105", "CORPUS-SRC-108"', '"CORPUS-SRC-104", "CORPUS-SRC-105", "CORPUS-SRC-106", "CORPUS-SRC-108"')
    if '    "FINDSET-018": {' not in text:
        marker = "\n}\n\n\nclass FindingsRegistryError"
        block = '''\n    "FINDSET-018": {\n        "source_id": "CORPUS-SRC-106",\n        "local_syntheses": ["FINDSET-136", "FINDSET-137"],\n        "problem_bindings": {"FINDSET-136": "theologico-political", "FINDSET-137": "ancients-vs-moderns"},\n        "required_limits": {"witness_id": "CORPUS-WIT-106", "transcript_authorial_approval": "NOT_REVIEWED_OR_FORMALLY_APPROVED_BY_STRAUSS_AS_FAR_AS_COLLECTION_EDITOR_CAN_DETERMINE", "documentary_transmission_limit": "ACTIVE", "independent_corroboration": "INCOMPLETE"},\n    },'''
        text = replace_once(text, marker, block + marker, "add FINDSET018 contract")
    text = text.replace('identity.get("version") != "1.10.0"', 'identity.get("version") != "1.11.0"')
    text = text.replace('identity.version must be 1.10.0', 'identity.version must be 1.11.0')
    text = text.replace('if len(finding_ids) != 57:', 'if len(finding_ids) != 60:')
    text = text.replace('expected 57 finding sets', 'expected 60 finding sets')
    path.write_text(text, encoding="utf-8")


def update_tests() -> None:
    replacements = {
        "tests/test_corpus_registry.py": [
            ('"1.18.0"', '"1.19.0"'),
            ('            57,', '            58,'),
            ('registry["coverage"]["study_records_registered"], 17', 'registry["coverage"]["study_records_registered"], 18'),
            ('def test_nine_tp_sources_have_witnesses_but_still_require_study', 'def test_eight_tp_sources_have_witnesses_but_still_require_study'),
            ('self.assertEqual(len(sources), 9)', 'self.assertEqual(len(sources), 8)'),
        ],
        "tests/test_findings_registry.py": [
            ('"1.10.0"', '"1.11.0"'),
            ('self.assertEqual(len(finding_ids), 57)', 'self.assertEqual(len(finding_ids), 60)'),
            ('self.assertEqual(len(registered), 35)', 'self.assertEqual(len(registered), 37)'),
            ('self.assertEqual(len(registered), 17)', 'self.assertEqual(len(registered), 18)'),
        ],
        "tests/test_interface_consistency.py": [
            ('test_nineteen_identity_nineteen_witness_ten_study_language_matches', 'test_nineteen_identity_nineteen_witness_eleven_study_language_matches'),
            ('manifest_state["independent_sequential_study_count"], 10', 'manifest_state["independent_sequential_study_count"], 11'),
            ('audit_state["independently_reconstructed_count_within_this_sequence"], 10', 'audit_state["independently_reconstructed_count_within_this_sequence"], 11'),
            ('mapping_state["independent_sequential_study_count"], 10', 'mapping_state["independent_sequential_study_count"], 11'),
            ('manifest_state["remaining_without_independent_sequential_study"], 9', 'manifest_state["remaining_without_independent_sequential_study"], 8'),
            ('mapping_state["remaining_without_independent_sequential_study"], 9', 'mapping_state["remaining_without_independent_sequential_study"], 8'),
            ('"INCOMPLETE_10_OF_19"', '"INCOMPLETE_11_OF_19"'),
            ('"HUSIK-PREFACE-STUDY-001"]', '"HUSIK-PREFACE-STUDY-001", "FREUD-MOSES-STUDY-001"]'),
            ('schedule["termination"]["next_item_study"], "CORPUS-SRC-106"', 'schedule["termination"]["next_item_study"], "CORPUS-SRC-107"'),
            ('            "FINDSET-017": [("FINDSET-134", "theologico-political"), ("FINDSET-135", "athens-vs-jerusalem")],\n', '            "FINDSET-017": [("FINDSET-134", "theologico-political"), ("FINDSET-135", "athens-vs-jerusalem")],\n            "FINDSET-018": [("FINDSET-136", "theologico-political"), ("FINDSET-137", "ancients-vs-moderns")],\n'),
        ],
        "tests/test_tp_witness_coverage_complete.py": [
            ('theologico_political_independent_item_studies_registered"], 10', 'theologico_political_independent_item_studies_registered"], 11'),
            ('"INCOMPLETE_10_OF_19"', '"INCOMPLETE_11_OF_19"'),
            ('def test_nine_witness_only_items_remain_noncertified_and_unstudied', 'def test_eight_witness_only_items_remain_noncertified_and_unstudied'),
            ('"CORPUS-SRC-101", "CORPUS-SRC-104"}', '"CORPUS-SRC-101", "CORPUS-SRC-104", "CORPUS-SRC-106"}'),
            ('self.assertEqual(len(witness_only), 9)', 'self.assertEqual(len(witness_only), 8)'),
        ],
        "tests/test_corpus_wit_102_platform_registration.py": [
            ('"INCOMPLETE_10_OF_19"', '"INCOMPLETE_11_OF_19"'),
        ],
        "tests/test_src104_husik_completion.py": [
            ('test_ten_of_nineteen_completion_language_is_synchronized', 'test_forward_completion_language_remains_synchronized_after_src106'),
            ('theologico_political_independent_item_studies_registered"], 10', 'theologico_political_independent_item_studies_registered"], 11'),
            ('"INCOMPLETE_10_OF_19"', '"INCOMPLETE_11_OF_19"'),
            ('independent_sequential_study_count"], 10', 'independent_sequential_study_count"], 11'),
            ('schedule["termination"]["next_item_study"], "CORPUS-SRC-106"', 'schedule["termination"]["next_item_study"], "CORPUS-SRC-107"'),
        ],
        "tests/test_pr21_talmon_completion.py": [
            ('manifest["identity"]["version"], "1.14.0"', 'manifest["identity"]["version"], "1.15.0"'),
            ('audit["identity"]["version"], "3.2.0"', 'audit["identity"]["version"], "3.3.0"'),
            ('mapping["identity"]["version"], "1.14.0"', 'mapping["identity"]["version"], "1.15.0"'),
            ('process["identity"]["version"], "1.16.0"', 'process["identity"]["version"], "1.17.0"'),
            ('schedule["identity"]["version"], "1.14.0"', 'schedule["identity"]["version"], "1.15.0"'),
            ('corpus["identity"]["version"], "1.18.0"', 'corpus["identity"]["version"], "1.19.0"'),
            ('findings["identity"]["version"], "1.10.0"', 'findings["identity"]["version"], "1.11.0"'),
            ('state["independent_sequential_study_count"], 10', 'state["independent_sequential_study_count"], 11'),
            ('state["remaining_without_independent_sequential_study"], 9', 'state["remaining_without_independent_sequential_study"], 8'),
            ('"HUSIK-PREFACE-STUDY-001"],', '"HUSIK-PREFACE-STUDY-001", "FREUD-MOSES-STUDY-001"],'),
            ('schedule["termination"]["next_item_study"], "CORPUS-SRC-106"', 'schedule["termination"]["next_item_study"], "CORPUS-SRC-107"'),
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
    for required in [STUDY_PATH, STATUS_PATH, TP_SYNTHESIS_PATH, AVM_SYNTHESIS_PATH]:
        if not (ROOT / required).is_file():
            raise RuntimeError(f"Required SRC106 production artifact missing: {required}")
    update_corpus_index()
    update_findings_index()
    update_manifest()
    update_audit()
    update_mapping()
    update_process()
    update_schedule()
    update_python_validators()
    update_tests()
    print("SRC106 integration materialized; ordinary repository validation remains required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
