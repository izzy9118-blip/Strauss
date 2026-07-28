#!/usr/bin/env python3
"""Materialize complete 19-of-19 Theologico-Political reviewed-witness coverage.

This is a bounded forward-revision utility for the current production branch. It does not
admit source text, complete sequential studies, certify doctrine or migration, activate
successors, or displace predecessors.
"""
from __future__ import annotations

from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
SHA = "43e98521c28a9ef8ede1eb7a6507d8ee78d605d0a531624d5dd20075220bda66"
SIZE = 39287307
PAGES = 526
FILE = "jewish-philosophy-and-the-crisis-of-modernity-essays-and-lectures-in-modern-jewish-thought_compress(1).pdf"
CONTAINER = "Jewish Philosophy and the Crisis of Modernity"

COMPLETE_STUDY_IDS = {
    "CORPUS-SRC-102": "CORPUS-WIT-102",
    "CORPUS-SRC-105": "CORPUS-WIT-105",
    "CORPUS-SRC-109": "CORPUS-WIT-109",
    "CORPUS-SRC-111": "CORPUS-WIT-111",
}

META = {
    "CORPUS-SRC-101": dict(wit="CORPUS-WIT-101", d="progress-or-return", title="Progress or Return?", pp=(87,136), pdf=(106,155), note="1952 Hillel House lectures; 1997 text combines Modern Judaism 1 (1981): 17-45 and The Independent Journal of Philosophy 3 (1979): 111-18"),
    "CORPUS-SRC-103": dict(wit="CORPUS-WIT-103", d="how-to-study-spinozas-theologico-political-treatise", title="How to Study Spinoza's Theologico-Political Treatise", pp=(181,233), pdf=(200,252), note="Proceedings of the American Academy for Jewish Research 17 (1948): 69-131"),
    "CORPUS-SRC-104": dict(wit="CORPUS-WIT-104", d="preface-to-isaac-husik-philosophical-essays", title="Preface to Isaac Husik, Philosophical Essays", pp=(235,266), pdf=(254,285), note="Isaac Husik, Philosophical Essays: Ancient, Medieval, and Modern (Basil Blackwell, 1952), vii-xli"),
    "CORPUS-SRC-106": dict(wit="CORPUS-WIT-106", d="freud-on-moses-and-monotheism", title="Freud on Moses and Monotheism", pp=(285,309), pdf=(304,328), note="1997 collection supplies no earlier publication citation in its Sources section"),
    "CORPUS-SRC-107": dict(wit="CORPUS-WIT-107", d="why-we-remain-jews", title="Why We Remain Jews", pp=(311,356), pdf=(330,375), note="1997 collection supplies no earlier publication citation in its Sources section"),
    "CORPUS-SRC-108": dict(wit="CORPUS-WIT-108", d="on-the-interpretation-of-genesis", title="On the Interpretation of Genesis", pp=(359,376), pdf=(378,395), note="L'Homme 21 (1981): 5-36; active predecessor preserves source date 1957"),
    "CORPUS-SRC-110": dict(wit="CORPUS-WIT-110", d="what-is-political-philosophy", title="What Is Political Philosophy?", pp=(409,409), pdf=(428,428), note="first-paragraph scope; What Is Political Philosophy? (Free Press, 1959), 9-10", scope="first paragraph"),
    "CORPUS-SRC-112": dict(wit="CORPUS-WIT-112", d="letter-to-editor-state-of-israel", title="Letter to the Editor — The State of Israel", pp=(413,414), pdf=(432,433), note="National Review 3, no. 1 (5 January 1957): 23"),
    "CORPUS-SRC-113": dict(wit="CORPUS-WIT-113", d="introduction-to-persecution-and-the-art-of-writing", title="Introduction to Persecution and the Art of Writing", pp=(417,429), pdf=(436,448), note="Persecution and the Art of Writing (Free Press, 1952), 7-21"),
    "CORPUS-SRC-114": dict(wit="CORPUS-WIT-114", d="perspectives-on-the-good-society", title="Perspectives on the Good Society", pp=(431,445), pdf=(450,464), note="Criterion 2, no. 3 (Summer 1963): 2-9"),
    "CORPUS-SRC-115": dict(wit="CORPUS-WIT-115", d="an-unspoken-prologue", title="An Unspoken Prologue", pp=(449,452), pdf=(468,471), note="Interpretation 7, no. 3 (1978): 1-3; active predecessor preserves source date 1959"),
    "CORPUS-SRC-116": dict(wit="CORPUS-WIT-116", d="preface-to-hobbes-politische-wissenschaft", title="Preface to Hobbes Politische Wissenschaft", pp=(453,456), pdf=(472,475), note="Interpretation 8, no. 1 (1979-80): 1-3, translated by Donald J. Maletz; active predecessor preserves source date 1965"),
    "CORPUS-SRC-117": dict(wit="CORPUS-WIT-117", d="a-giving-of-accounts", title="A Giving of Accounts", pp=(457,466), pdf=(476,485), note="The College 22, no. 1 (April 1970): 1-5"),
    "CORPUS-SRC-118": dict(wit="CORPUS-WIT-118", d="plan-philosophy-and-the-law-historical-essays", title="Plan of a Book Tentatively Entitled Philosophy and the Law — Historical Essays", pp=(467,470), pdf=(486,489), note="1997 collection supplies no earlier publication citation in its Sources section; active predecessor preserves source date 1946"),
    "CORPUS-SRC-119": dict(wit="CORPUS-WIT-119", d="restatement-on-xenophons-hiero", title="Restatement on Xenophon's Hiero", pp=(471,473), pdf=(490,492), note="last-paragraph scope; 1997 collection supplies no separate earlier-publication citation for the excerpt; active predecessor preserves source date 1950", scope="last paragraph"),
}
ALL_TP = [f"CORPUS-SRC-{i:03d}" for i in range(101,120)]
WITNESS_ONLY = sorted(META)


def load(path: str):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def dump(path: str, data) -> None:
    (ROOT / path).write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8"
    )


def range_dict(pair):
    return {"start": pair[0], "end": pair[1]}


def witness_entry(source_id: str):
    m = META[source_id]
    entry = {
        "witness_id": m["wit"],
        "source_id": source_id,
        "witness_type": "ITEM_WITHIN_SEARCHABLE_PDF_WITH_PAGE_IMAGES",
        "witness_class": "FINGERPRINTED_LOCAL_REVIEW_WITNESS",
        "container_title": CONTAINER,
        "container_editor": "Kenneth Hart Green",
        "publisher": "State University of New York Press",
        "publication_year": 1997,
        "collected_title": m["title"],
        "publication_provenance_note": m["note"],
        "printed_page_range": range_dict(m["pp"]),
        "pdf_page_range_one_based": range_dict(m["pdf"]),
        "local_filename_recorded": FILE,
        "container_page_count": PAGES,
        "container_file_size_bytes": SIZE,
        "container_sha256": SHA,
        "source_status_path": f"studies/theologico-political/{m['d']}/source-status.yaml",
        "witness_record_path": f"studies/theologico-political/{m['d']}/reviewed-witness.yaml",
        "text_condition": "SEARCHABLE_TEXT_WITH_PAGE_IMAGES",
        "wording_rule": "PAGE_IMAGES_GOVERN_WHERE_EXTRACTED_TEXT_IS_UNCERTAIN_OR_CONFLICTS",
        "repository_copy_status": "NOT_DISTRIBUTED_BY_ITEM_REGISTRY",
        "original_edition_comparison": "PENDING",
    }
    if m.get("scope"):
        entry["registered_scope"] = m["scope"]
    return entry


def update_corpus():
    path = "corpus/index.yaml"
    c = load(path)
    c["identity"]["version"] = "1.12.0"
    c["revision_history"] = {
        "predecessor_version": "1.11.0",
        "predecessor_blob_sha": "b23efa44e354894bb22cfd6b0b0d65312b5c3ad0",
        "transformation": "SUBSTANTIVE_FORWARD_REVISION",
        "reason": "Register the remaining fourteen fingerprinted 1997 SUNY collected witnesses so all nineteen Theologico-Political predecessor source identities have reviewed witnesses, while preserving fifteen pending independent sequential studies, edition-comparison limits, noncorroboration, noncertification, predecessor authority, and no successor effect.",
    }
    sources = {x["source_id"]: x for x in c["source_entities"]}
    for sid in ALL_TP:
        src = sources[sid]
        wit = COMPLETE_STUDY_IDS.get(sid) or META[sid]["wit"]
        src["reviewed_witnesses"] = [wit]
        if sid not in COMPLETE_STUDY_IDS:
            src.pop("study_records", None)
            src["item_level_source_status"] = "REVIEWED_ITEM_WITNESS_REGISTERED_SEQUENTIAL_RECONSTRUCTION_REQUIRED"
            src["study_status"] = "INDEPENDENT_RECONSTRUCTION_REQUIRED"
            limits = list(src.get("limits", []))
            note = "reviewed witness is registered; independent sequential reconstruction remains pending"
            if note not in limits:
                limits.append(note)
            if sid in META and META[sid].get("scope"):
                scope_note = f"registered witness covers only the predecessor-defined {META[sid]['scope']} scope"
                if scope_note not in limits:
                    limits.append(scope_note)
            src["limits"] = limits
    existing = {x["witness_id"]: x for x in c["reviewed_witnesses"]}
    for sid in META:
        if sid != "CORPUS-SRC-103":
            existing[META[sid]["wit"]] = witness_entry(sid)
    # retain CORPUS-WIT-103's richer prior record
    c["reviewed_witnesses"] = sorted(existing.values(), key=lambda x: x["witness_id"])
    for entry in c["source_status_records"]:
        sid = entry["source_id"]
        if sid in META:
            entry["completion"] = "REVIEWED_ITEM_WITNESS_REGISTERED_SEQUENTIAL_RECONSTRUCTION_REQUIRED"
    coverage = c["coverage"]
    coverage["reviewed_witnesses_registered"] = 22
    coverage["theologico_political_reviewed_item_witnesses_registered"] = 19
    coverage["theologico_political_independent_item_studies_registered"] = 4
    coverage["current_studies_tree_yaml_records_accounted_for"] = len(list((ROOT / "studies").rglob("*.yaml")))
    gap = next(x for x in c["corpus_gaps"] if x["gap_id"] == "CORPUS-GAP-003")
    gap["statement"] = "All nineteen predecessor writings have bounded source identities and reviewed witnesses. Four have complete provisional independent sequential studies; the remaining fifteen have registered witnesses but still require independent sequential reconstruction."
    rules = c["validation_rules"]
    rules[:] = [r for r in rules if "CORPUS-SRC-103 preserves fingerprinted witness-only safeguards" not in r]
    if "all fifteen witness-only Theologico-Political sources preserve registered-witness, pending-study, edition-comparison, noncertification, and no-successor safeguards" not in rules:
        rules.append("all fifteen witness-only Theologico-Political sources preserve registered-witness, pending-study, edition-comparison, noncertification, and no-successor safeguards")
    t = c["termination"]
    t["theologico_political_reviewed_witness_state"] = "COMPLETE_19_OF_19"
    t["theologico_political_independent_study_state"] = "INCOMPLETE_4_OF_19"
    t["next_required_units"] = [
        "conduct independent sequential reconstruction for the remaining fifteen writings, beginning with CORPUS-SRC-103",
        "compare collected witnesses with separately reviewed original or earlier textual states where available and material",
        "compare the 1997 CORPUS-WIT-102 composite with separately reviewed 1965 and 1968 textual states",
        "acquire and reconstruct Talmon's reviewed work and other independent classical, biblical, medieval, Spinozist, Cohenian, Kantian, and modern witnesses",
    ]
    dump(path, c)


def update_manifest():
    path = "manifest.yaml"
    m = load(path)
    m["identity"]["version"] = "1.8.0"
    m["revision_history"] = {
        "predecessor_version": "1.7.0",
        "predecessor_blob_sha": "583017561cc0f5425600fc545da2f64e1db39d7e",
        "reason": "Register the remaining fourteen fingerprinted 1997 SUNY collected witnesses, completing 19-of-19 reviewed-witness coverage for the active Theologico-Political predecessor sequence while preserving fifteen pending independent sequential studies, edition-comparison limits, noncertification, predecessor authority, and the Sanctum repin block.",
    }
    m["audit"]["version"] = "2.6.0"
    cc = m["component_completion"]
    cc["reviewed_source_witnesses"] = "TWENTY_TWO_REVIEWED_WITNESSES_TOTAL_WITH_ALL_NINETEEN_THEOLOGICO_POLITICAL_PREDECESSOR_ITEMS_WITNESSED"
    cc["theologico_political_item_level_source_statuses"] = "19_OF_19_IDENTITIES_19_OF_19_REVIEWED_ITEM_WITNESSES_4_OF_19_COMPLETE_PROVISIONAL_ITEM_STUDIES"
    cc["behavioral_tests"] = "SPEECH_HERMENEUTIC_METHOD_PROBLEM_BUNDLE_CORPUS_FINDINGS_AND_COMPLETE_THEOLOGICO_POLITICAL_WITNESS_COVERAGE_CONTRACTS_REQUIRE_VALIDATION"
    corpus = m["corpus"]
    corpus["registry_version"] = "1.12.0"
    by_wit = {x["witness_id"]: x for x in corpus["reviewed_witnesses"]}
    for sid, md in META.items():
        if sid == "CORPUS-SRC-103":
            continue
        x = {
            "source": md["title"], "witness_id": md["wit"],
            "witness_class": "FINGERPRINTED_LOCAL_REVIEW_WITNESS", "container": CONTAINER,
            "publication_year": 1997, "printed_pages": f"{md['pp'][0]}-{md['pp'][1]}",
            "pdf_pages_one_based": f"{md['pdf'][0]}-{md['pdf'][1]}",
            "container_sha256": SHA, "container_file_size_bytes": SIZE,
            "original_or_earlier_printing_comparison": "PENDING",
            "item_status": f"studies/theologico-political/{md['d']}/source-status.yaml",
        }
        if md.get("scope"):
            x["registered_scope"] = md["scope"]
        by_wit[md["wit"]] = x
    corpus["reviewed_witnesses"] = sorted(by_wit.values(), key=lambda x: x["witness_id"])
    state = corpus["theologico_political_item_level_statuses"]
    state["reviewed_witness_count"] = 19
    state["remaining_without_reviewed_item_witness"] = 0
    state["independent_sequential_study_count"] = 4
    state["remaining_without_independent_sequential_study"] = 15
    state["rule"] = "All nineteen predecessor items now have reviewed witnesses. Only four have complete provisional independent sequential studies. Witness coverage is documentary availability, not independent corroboration, doctrinal certification, migration completion, successor activation, or repository completion."
    corpus["limitation"] = "All nineteen predecessor writings now have bounded identities and reviewed witnesses, but fifteen still lack independent sequential studies. Original-edition comparisons, independent source traditions, source-text admission, doctrinal certification, migration certification, and successor activation remain incomplete."
    dump(path, m)


def update_audit():
    path = "audits/operational-completeness.yaml"
    a = load(path)
    a["identity"]["version"] = "2.6.0"
    a["revision_history"] = {
        "predecessor_version": "2.5.0",
        "predecessor_blob_sha": "7760cc9b56795190560b12a33c38d5247e9437e8",
        "reason": "Register the remaining fourteen fingerprinted 1997 SUNY collected witnesses and record complete 19-of-19 reviewed-witness coverage for the active Theologico-Political predecessor sequence while preserving fifteen pending independent sequential studies, edition-comparison limits, noncorroboration, noncertification, and the Sanctum repin block.",
    }
    a["basis"]["current_revision_scope"] = "production/complete-remaining-fourteen-theologico-political-witnesses"
    s = a["summary"]
    units = s["completed_operational_units"]
    units[:] = [u for u in units if not str(u).startswith("eight reviewed witnesses")]
    units.append("twenty-two reviewed witnesses total, including all nineteen active Theologico-Political predecessor items")
    units.append("remaining-fourteen Theologico-Political witness acquisition and fingerprint registration batch complete")
    tp = s["theologico_political_item_level_status"]
    tp["reviewed_item_witness_count"] = 19
    tp["registered_without_reviewed_witness_count"] = 0
    tp["remaining_without_item_level_status_count"] = 0
    tp["independently_reconstructed_count_within_this_sequence"] = 4
    tp["remaining_without_independent_sequential_study"] = 15
    tp["witness_only_source_ids"] = [sid for sid in ALL_TP if sid not in COMPLETE_STUDY_IDS]
    tp["witness_only_witness_ids"] = [META[sid]["wit"] for sid in tp["witness_only_source_ids"]]
    tp["registered_witness_source_ids"] = ALL_TP
    tp["registered_witness_ids"] = [COMPLETE_STUDY_IDS.get(sid) or META[sid]["wit"] for sid in ALL_TP]
    tp["interpretation_limit"] = "All nineteen predecessor items now have reviewed witnesses, but only four completed studies are independent reconstructions relative to predecessor and collection-level synthesis. The other fifteen witness registrations do not constitute completed studies or independent corroboration."
    deficiencies = [d for d in s["remaining_major_deficiencies"] if not str(d).startswith("fourteen Theologico-Political item identities lack reviewed item witnesses")]
    deficiencies.insert(0, "fifteen Theologico-Political writings still require independent sequential item studies")
    s["remaining_major_deficiencies"] = deficiencies
    # Keep the audit record list bounded; add one batch record and update corpus/manifest summaries where present.
    batch_path = "history/reviewed-witness-acquisitions/2026-07-28-remaining-fourteen-theologico-political-witnesses.yaml"
    if not any(r.get("path") == batch_path for r in a.get("records", [])):
        a.setdefault("records", []).append({
            "path": batch_path,
            "classification": "SUBSTANTIVELY_RECONSTRUCTED",
            "identity": "TP-WITNESS-ACQUISITION-REMAINING-14-2026-07-28",
            "present_function": ["records the fingerprinted 1997 SUNY container and exact locators for the remaining fourteen predecessor items", "completes documentary reviewed-witness coverage at 19-of-19 without claiming study completion"],
            "remaining": ["fifteen independent sequential studies", "original or earlier textual-state comparisons where available", "independent corroborating source traditions"],
        })
    for r in a.get("records", []):
        if r.get("path") == "corpus/index.yaml":
            r["registry_version"] = "1.12.0"
            r["present_function"] = ["22 typed source entities", "22 reviewed witnesses", "22 source-status records", "11 analytical and integration study records", "all 51 YAML records in the studies tree accounted for", "all 7 problem witness registries", "19 Theologico-Political identities, 19 reviewed item witnesses, and 4 complete provisional item studies", "7 positive corpus-gap records"]
            r["remaining"] = ["fifteen independent item studies", "complete Strauss bibliography and edition-specific comparisons", "broader independent classical, biblical, medieval, Spinozist, Cohenian, Kantian, and modern corpora", "source-text admission and runtime source access remain separate"]
        if r.get("path") == "manifest.yaml":
            r["present_function"] = ["registers corpus v1.12.0, findings v1.4.0, 19 Theologico-Political identities, 19 reviewed item witnesses, and 4 completed provisional item studies", "preserves structural, semantic, runtime, migration, predecessor, and certification limits", "blocks completed-interface Sanctum repinning"]
    po = a.get("production_order", {})
    po["next"] = ["run complete structural and behavioral validation for 19-of-19 witness coverage", "conduct CORPUS-SRC-103 independent sequential reconstruction from printed pages 181-233", "continue the remaining fourteen independent sequential reconstructions", "expand independent source-tradition witnesses and original-edition comparisons", "validate actual ministerial reports against the full contract stack"]
    dump(path, a)


def update_mapping():
    path = "migrations/lean-operational-interface.yaml"
    m = load(path)
    m["identity"]["version"] = "1.8.0"
    m["revision_history"] = {
        "predecessor_version": "1.7.0",
        "predecessor_blob_sha": "2ce5cf4b5ec6f78c19a2a6b4c1c1acf34b1f792c",
        "reason": "Synchronize complete 19-of-19 Theologico-Political reviewed-witness coverage, corpus registry v1.12.0, audit v2.6.0, process v1.10.0, and witness schedule v1.8.0 while preserving fifteen pending studies, edition-comparison limits, noncorroboration, noncertification, predecessor authority, and repository incompleteness.",
    }
    m["completion_audit"]["version"] = "2.6.0"
    pp = m["production_process"]
    pp["completed_witness_subunit"] = "THEOLOGICO_POLITICAL_REVIEWED_WITNESSES_19_OF_19_COMPLETE"
    pp["completed_study_subunit"] = "FOUR_OF_19_COMPLETE_PROVISIONAL_FIFTEEN_PENDING"
    c = m["mappings"]["corpus"]
    c["interface"]["registry_version"] = "1.12.0"
    c["transformation"] = "SUBSTANTIVE_FORWARD_REVISION_WITH_COMPLETE_NINETEEN_ITEM_REVIEWED_WITNESS_COVERAGE"
    c["reviewed_witnesses"]["count"] = 22
    c["reviewed_witnesses"]["source_ids"] = ["CORPUS-SRC-001", "CORPUS-SRC-002", "CORPUS-SRC-003"] + ALL_TP
    st = c["theologico_political_item_level_statuses"]
    st["reviewed_witness_count"] = 19
    st["remaining_without_reviewed_witness"] = 0
    st["independent_sequential_study_count"] = 4
    st["remaining_without_independent_sequential_study"] = 15
    st["witness_only_source_ids"] = [sid for sid in ALL_TP if sid not in COMPLETE_STUDY_IDS]
    c["present_function"] = ["register source entities separately from witnesses and studies", "account for all 51 YAML records in the current studies tree", "validate all nineteen identities, aliases, scopes, reviewed-witness states, study states, fingerprints, locators, and noncertification", "preserve CORPUS-WIT-102 platform-reference safeguards", "validate the fingerprinted 1997 SUNY witness batch without converting witness registration into sequential study completion", "preserve corpus gaps and original-edition comparison limits"]
    c["limit"] = "Current-state exhaustiveness and 19-of-19 reviewed item witness coverage do not create a complete corpus, complete the fifteen pending sequential studies, admit source text, supply independent corroboration, certify findings, or authorize migration and activation."
    dump(path, m)


def update_process():
    path = "history/production-plans/2026-07-27-ten-step-completion-process.yaml"
    p = load(path)
    p["identity"]["version"] = "1.10.0"
    p["revision_history"] = {
        "predecessor_version": "1.9.0",
        "predecessor_blob_sha": "63d4ecb7e55d39cce6521315b505200e2aea947d",
        "reason": "Complete reviewed-witness acquisition and registration for the remaining fourteen Theologico-Political predecessor items, reaching 19-of-19 witness coverage while preserving fifteen pending independent sequential studies, edition-comparison limits, noncertification, and the Step 10 repin blocker.",
    }
    for step in p["steps"]:
        if step["sequence"] == 1:
            step["current_version"] = "2.6.0"
        elif step["sequence"] == 2:
            step["current_version"] = "1.8.0"
        elif step["sequence"] == 8:
            step["completed"] = ["all 19 Theologico-Political predecessor writings have bounded item identities", "all 19 Theologico-Political predecessor writings now have reviewed witnesses", "CORPUS-WIT-102 remains a qualified platform-reference witness with preserved missing-byte safeguards", "the other eighteen Theologico-Political reviewed witnesses are fingerprinted against their reviewed containers", "SPINOZA-PREFACE-STUDY-001, JA-STUDY-001, COHEN-STUDY-001, and TALMON-STUDY-001 remain complete provisional for their reviewed witnesses", "corpus and findings registries preserve derivation, jurisdiction, gaps, witness/study distinctions, and noncertification"]
            step["remaining"] = ["conduct fifteen independent sequential item studies, beginning with CORPUS-SRC-103", "compare original or earlier textual states where available and material", "materialize and fingerprint CORPUS-WIT-102 only through later forward revision if exact bytes become accessible", "reconstruct Talmon's reviewed work independently", "expand independent primary witnesses beyond Strauss's writings", "normalize propositions where warranted by reproducible extraction", "preserve later additions through forward revision"]
        elif step["sequence"] == 9:
            step["completed_in_current_sequence"] = ["tests cover all nineteen Theologico-Political reviewed-witness registrations and distinguish the fifteen witness-only states from the four completed-study states", "tests preserve qualified platform-reference, fingerprint, locator, scope, edition-comparison, noncertification, and no-successor safeguards", "tests cover corpus and findings coverage, derivation, jurisdiction, and completion-language consistency"]
            step["current_requirement"] = "Run the complete GitHub Actions validation before merge."
    p["current_production_unit"] = {
        "step": 8,
        "completed_subunit": {"title": "Remaining fourteen Theologico-Political reviewed-witness acquisition and registration", "state": "COMPLETE_PENDING_BRANCH_VALIDATION_AND_MERGE", "witness_coverage": "COMPLETE_19_OF_19", "study_coverage": "INCOMPLETE_4_OF_19", "non_effect": "Witness registration does not supply sequential reconstruction, independent corroboration, doctrine, certified migration, successor activation, predecessor displacement, or completed-interface readiness."},
        "next_subunit": {"title": "How to Study Spinoza's Theologico-Political Treatise independent sequential reconstruction", "source_id": "CORPUS-SRC-103", "witness_id": "CORPUS-WIT-103", "first_action": "Reconstruct printed pages 181-233 in textual order before comparing with the active predecessor.", "following_source": "CORPUS-SRC-108"},
        "non_effects": ["no source-text admission through registries", "no doctrinal or migration certification", "no successor activation or predecessor displacement", "no Sanctum repin as a completed interface"],
    }
    dump(path, p)


def update_schedule():
    path = "history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml"
    s = load(path)
    s["identity"]["version"] = "1.8.0"
    s["status"]["reviewed_witness_completion"] = "COMPLETE_19_OF_19"
    s["status"]["independent_sequential_study_completion"] = "INCOMPLETE_4_OF_19"
    s["revision_history"] = {
        "predecessor_version": "1.7.0", "predecessor_blob_sha": "7f3e1679aae66848731454f6f87cd7f0b66a8aca",
        "reason": "Register the remaining fourteen fingerprinted 1997 SUNY collected witnesses, completing reviewed-witness coverage for all nineteen predecessor sources while preserving fifteen pending independent sequential studies, edition-comparison limits, noncorroboration, noncertification, and CORPUS-SRC-103 as the next study unit.",
    }
    rank_order = []
    for group in s["priority_groups"]:
        for item in group["items"]:
            sid = item["source_id"]
            rank_order.append((item.get("rank", 999), sid))
            if sid in META:
                md = META[sid]
                item["status_id"] = f"CORPUS-STATUS-{sid[-3:]}"
                item["witness_id"] = md["wit"]
                item["state"] = "REVIEWED_WITNESS_REGISTERED_SEQUENTIAL_STUDY_PENDING"
                item["witness_locator"] = {"container_title": CONTAINER, "container_sha256": SHA, "printed_pages": f"{md['pp'][0]}-{md['pp'][1]}", "pdf_pages_one_based": f"{md['pdf'][0]}-{md['pdf'][1]}"}
                if md.get("scope"):
                    item["witness_locator"]["registered_scope"] = md["scope"]
                item["next_action"] = "INDEPENDENT_SEQUENTIAL_RECONSTRUCTION_AND_ORIGINAL_TEXTUAL_STATE_COMPARISON_WHERE_AVAILABLE"
    rank_order.sort()
    completed_sources = [sid for _, sid in rank_order]
    completed_wits = [COMPLETE_STUDY_IDS.get(sid) or META[sid]["wit"] for sid in completed_sources]
    sel = s["selection"]
    sel["completed_source_ids"] = completed_sources
    sel["completed_witness_ids"] = completed_wits
    sel["completed_study_ids"] = ["JA-STUDY-001", "COHEN-STUDY-001", "TALMON-STUDY-001", "SPINOZA-PREFACE-STUDY-001"]
    sel["selection_state"] = "NINETEEN_REVIEWED_ITEM_WITNESSES_FOUR_COMPLETE_PROVISIONAL_SEQUENTIAL_STUDIES"
    sel["completed_units"] = ["all nineteen predecessor source identities have reviewed witnesses", "four source studies remain complete provisional", "fifteen witness-only sources remain pending independent sequential reconstruction", "all original-edition and independent-corroboration limits remain explicit"]
    sel["limits"] = ["reviewed-witness coverage does not constitute completed sequential reconstruction", "original or earlier textual-state comparisons remain pending where not separately reviewed", "the studies are not independent Spinozist, biblical, Greek, Cohenian, Talmonian, Kantian, Hobbesian, or other source-tradition corroboration", "no doctrine, migration, or successor certification"]
    s["next_item_witness_unit"] = {"source_id": "NONE", "title": "Reviewed-witness acquisition complete for nineteen-source sequence", "action": "NO_FURTHER_WITNESS_ACQUISITION_REQUIRED_WITHIN_CURRENT_NINETEEN_SOURCE_SEQUENCE", "required_preservations": ["retain exact witness identity and locators", "retain original-edition comparison limits", "retain distinction between witness registration and study completion"]}
    term = s["termination"]
    term["reviewed_item_witness_registration"] = "COMPLETE_19_OF_19"
    term["independent_sequential_reconstruction"] = "INCOMPLETE_4_OF_19"
    term["next_item_witness"] = "NONE"
    term["next_item_study"] = "CORPUS-SRC-103"
    s["next_item_study_unit"] = {"source_id": "CORPUS-SRC-103", "title": "How to Study Spinoza's Theologico-Political Treatise", "action": "INDEPENDENT_SEQUENTIAL_RECONSTRUCTION_FROM_REGISTERED_WITNESS", "prerequisite": "SATISFIED_CORPUS_WIT_103_REGISTERED", "following_source": "CORPUS-SRC-108"}
    dump(path, s)


def update_corpus_registry_py():
    path = ROOT / "corpus_registry.py"
    text = path.read_text(encoding="utf-8")
    specs = []
    for sid in WITNESS_ONLY:
        md = META[sid]
        specs.append(
            f'    "{sid}": {{\n'
            f'        "status_id": "CORPUS-STATUS-{sid[-3:]}",\n'
            f'        "witness_id": "{md["wit"]}",\n'
            f'        "witness_record_path": "studies/theologico-political/{md["d"]}/reviewed-witness.yaml",\n'
            f'        "printed_page_range": {range_dict(md["pp"])!r},\n'
            f'        "pdf_page_range_one_based": {range_dict(md["pdf"])!r},\n'
            f'        "container_sha256": "{SHA}",\n'
            f'        "container_file_size_bytes": {SIZE},\n'
            f'        "container_page_count": {PAGES},\n'
            f'    }},'
        )
    block = "WITNESS_ONLY_TP_ITEMS: dict[str, dict[str, Any]] = {\n" + "\n".join(specs) + "\n}\n"
    text = re.sub(r'WITNESS_ONLY_TP_ITEMS: dict\[str, dict\[str, Any\]\] = \{.*?\n\}\n\n\nclass CorpusRegistryError', block + "\n\nclass CorpusRegistryError", text, flags=re.S)
    generic = '''def _validate_witness_only_tp_item(
    registry: dict[str, Any],
    source: dict[str, Any],
    status_record: dict[str, Any],
    source_id: str,
    errors: list[str],
) -> None:
    spec = WITNESS_ONLY_TP_ITEMS[source_id]
    witness_id = spec["witness_id"]
    status_id = spec["status_id"]
    state = status_record.get("status", {})
    termination = status_record.get("termination", {})

    if state.get("reviewed_witness") != witness_id:
        errors.append(f"{status_id} must record {witness_id}")
    if state.get("independent_sequential_study") != "NOT_YET_COMPLETED":
        errors.append(f"{status_id} independent study must remain incomplete")
    if source.get("reviewed_witnesses") != [witness_id]:
        errors.append(f"{source_id} must list {witness_id}")
    if source.get("study_records") not in (None, []):
        errors.append(f"{source_id} may not list a completed study before reconstruction")

    witness = _find_record(registry.get("reviewed_witnesses", []), "witness_id", witness_id)
    if not isinstance(witness, dict):
        errors.append(f"{witness_id} is missing")
        return
    if witness.get("source_id") != source_id:
        errors.append(f"{witness_id} source binding mismatch")
    for field in ("printed_page_range", "pdf_page_range_one_based", "container_sha256", "container_file_size_bytes", "container_page_count"):
        if witness.get(field) != spec[field]:
            errors.append(f"{witness_id} {field} mismatch")
    if witness.get("witness_record_path") != spec["witness_record_path"]:
        errors.append(f"{witness_id} witness record path mismatch")

    reviewed = status_record.get("reviewed_witness", {})
    if not isinstance(reviewed, dict) or reviewed.get("witness_id") != witness_id:
        errors.append(f"{status_id} reviewed_witness block mismatch")
    else:
        for field in ("printed_page_range", "pdf_page_range_one_based", "container_sha256"):
            if reviewed.get(field) != witness.get(field):
                errors.append(f"{witness_id} {field} mismatch between registry and status")

    publication = status_record.get("publication_and_witness_condition", {})
    fingerprint = publication.get("fingerprint")
    if isinstance(fingerprint, dict):
        digest = fingerprint.get("value")
    else:
        digest = publication.get("sha256") if fingerprint == "AVAILABLE" else None
    if digest != spec["container_sha256"]:
        errors.append(f"{status_id} fingerprint mismatch")
    if publication.get("file_size_bytes") != spec["container_file_size_bytes"]:
        errors.append(f"{status_id} file-size mismatch")
    comparison = publication.get("original_or_earlier_printing_comparison", publication.get("original_1948_journal_copy_comparison"))
    if comparison != "PENDING":
        errors.append(f"{status_id} must preserve pending original/earlier textual-state comparison")

    if termination.get("reviewed_witness_state") != "REGISTERED":
        errors.append(f"{status_id} reviewed witness state must be REGISTERED")
    if termination.get("study_state") != "INCOMPLETE":
        errors.append(f"{status_id} study state must remain INCOMPLETE")
    if termination.get("original_edition_comparison") != "PENDING":
        errors.append(f"{status_id} original edition comparison must remain PENDING")
    if termination.get("certification") != "NOT_CERTIFIED":
        errors.append(f"{status_id} must remain NOT_CERTIFIED")
    if termination.get("successor_effect") != "NONE":
        errors.append(f"{status_id} may not affect successor activation")

    witness_record = load_yaml(_resolve(spec["witness_record_path"]))
    if witness_record.get("identity", {}).get("witness_id") != witness_id:
        errors.append(f"{witness_id} record identity mismatch")
    cw = witness_record.get("container_witness", {})
    if cw.get("container_sha256") != spec["container_sha256"] or cw.get("container_file_size_bytes") != spec["container_file_size_bytes"] or cw.get("container_page_count") != spec["container_page_count"]:
        errors.append(f"{witness_id} witness-record container fingerprint mismatch")
    if witness_record.get("status", {}).get("certification") != "NOT_CERTIFIED":
        errors.append(f"{witness_id} record must remain NOT_CERTIFIED")
    if witness_record.get("termination", {}).get("study_state") != "INCOMPLETE":
        errors.append(f"{witness_id} witness record may not claim study completion")
    if witness_record.get("termination", {}).get("successor_effect") != "NONE":
        errors.append(f"{witness_id} record must preserve successor_effect NONE")
'''
    text = re.sub(r'def _validate_witness_only_tp_item\(.*?\n\n\ndef _validate_tp_sources_and_statuses', generic + "\n\n\ndef _validate_tp_sources_and_statuses", text, flags=re.S)
    text = text.replace('identity.get("version") != "1.11.0"', 'identity.get("version") != "1.12.0"')
    text = text.replace('identity.version must be 1.11.0', 'identity.version must be 1.12.0')
    text = text.replace('"reviewed witnesses": (len(witness_ids), 8)', '"reviewed witnesses": (len(witness_ids), 22)')
    text = text.replace('"theologico_political_reviewed_item_witnesses_registered": 5', '"theologico_political_reviewed_item_witnesses_registered": 19')
    text = text.replace('termination.get("theologico_political_reviewed_witness_state") != "INCOMPLETE_5_OF_19"', 'termination.get("theologico_political_reviewed_witness_state") != "COMPLETE_19_OF_19"')
    text = text.replace('TP reviewed-witness state must be INCOMPLETE_5_OF_19', 'TP reviewed-witness state must be COMPLETE_19_OF_19')
    path.write_text(text, encoding="utf-8")


def update_tests():
    p = ROOT / "tests/test_corpus_registry.py"
    t = p.read_text(encoding="utf-8")
    t = t.replace('"1.11.0"', '"1.12.0"').replace('            37,', '            51,').replace('registry["coverage"]["reviewed_witnesses_registered"], 8', 'registry["coverage"]["reviewed_witnesses_registered"], 22')
    start = t.index('    def test_fourteen_tp_sources_remain_without_witness_or_study')
    end = t.index('    def test_spinoza_treatise_witness_is_registered_without_claiming_study_completion', start)
    replacement = '''    def test_fifteen_tp_sources_have_witnesses_but_still_require_study(self) -> None:\n        registry = corpus_registry.load_registry()\n        entries = {item["source_id"]: item for item in registry["source_status_records"] if corpus_registry._tp_sequence_from_source_id(item["source_id"]) is not None}\n        sources = [item for item in registry["source_entities"] if item["source_id"] in corpus_registry.WITNESS_ONLY_TP_ITEMS]\n        self.assertEqual(len(sources), 15)\n        self.assertEqual(set(corpus_registry.WITNESS_ONLY_TP_ITEMS), {item["source_id"] for item in sources})\n        for source in sources:\n            status = corpus_registry.load_yaml(corpus_registry._resolve(entries[source["source_id"]]["path"]))\n            self.assertEqual(source["item_level_source_status"], "REVIEWED_ITEM_WITNESS_REGISTERED_SEQUENTIAL_RECONSTRUCTION_REQUIRED")\n            self.assertEqual(source["reviewed_witnesses"], [corpus_registry.WITNESS_ONLY_TP_ITEMS[source["source_id"]]["witness_id"]])\n            self.assertEqual(status["status"]["independent_sequential_study"], "NOT_YET_COMPLETED")\n            self.assertEqual(status["termination"]["study_state"], "INCOMPLETE")\n            self.assertEqual(status["termination"]["certification"], "NOT_CERTIFIED")\n            self.assertEqual(status["termination"]["successor_effect"], "NONE")\n\n'''
    t = t[:start] + replacement + t[end:]
    p.write_text(t, encoding="utf-8")

    p = ROOT / "tests/test_interface_consistency.py"
    t = p.read_text(encoding="utf-8")
    t = t.replace('def test_nineteen_identity_five_witness_four_study_language_matches', 'def test_nineteen_identity_nineteen_witness_four_study_language_matches')
    t = t.replace('self.assertEqual(manifest_state["reviewed_witness_count"], 5)', 'self.assertEqual(manifest_state["reviewed_witness_count"], 19)')
    t = t.replace('self.assertEqual(audit_state["reviewed_item_witness_count"], 5)', 'self.assertEqual(audit_state["reviewed_item_witness_count"], 19)')
    t = t.replace('self.assertEqual(mapping_state["reviewed_witness_count"], 5)', 'self.assertEqual(mapping_state["reviewed_witness_count"], 19)')
    t = t.replace('self.assertEqual(manifest_state["remaining_without_reviewed_item_witness"], 14)', 'self.assertEqual(manifest_state["remaining_without_reviewed_item_witness"], 0)')
    t = t.replace('self.assertEqual(mapping_state["remaining_without_reviewed_witness"], 14)', 'self.assertEqual(mapping_state["remaining_without_reviewed_witness"], 0)')
    t = t.replace('"INCOMPLETE_5_OF_19",', '"COMPLETE_19_OF_19",')
    start = t.index('    def test_priority_schedule_advances_witness_to_genesis_while_spinoza_treatise_study_is_next')
    end = t.index('    def test_source_derivations_preserve_problem_jurisdiction', start)
    replacement = '''    def test_priority_schedule_marks_witness_acquisition_complete_and_spinoza_treatise_study_next(self) -> None:\n        schedule = load_yaml("history/production-plans/2026-07-27-theologico-political-reviewed-witness-priority.yaml")\n        self.assertEqual(len(schedule["selection"]["completed_source_ids"]), 19)\n        self.assertEqual(len(schedule["selection"]["completed_witness_ids"]), 19)\n        self.assertEqual(set(schedule["selection"]["completed_source_ids"]), {f"CORPUS-SRC-{i:03d}" for i in range(101, 120)})\n        self.assertEqual(schedule["selection"]["completed_study_ids"], ["JA-STUDY-001", "COHEN-STUDY-001", "TALMON-STUDY-001", "SPINOZA-PREFACE-STUDY-001"])\n        self.assertEqual(schedule["termination"]["reviewed_item_witness_registration"], "COMPLETE_19_OF_19")\n        self.assertEqual(schedule["termination"]["independent_sequential_reconstruction"], "INCOMPLETE_4_OF_19")\n        self.assertEqual(schedule["termination"]["next_item_witness"], "NONE")\n        self.assertEqual(schedule["termination"]["next_item_study"], "CORPUS-SRC-103")\n        self.assertEqual(schedule["status"]["certification"], "NOT_CERTIFIED")\n\n'''
    t = t[:start] + replacement + t[end:]
    p.write_text(t, encoding="utf-8")

    p = ROOT / "tests/test_pr21_talmon_completion.py"
    if p.exists():
        t = p.read_text(encoding="utf-8")
        t = t.replace('"1.7.0"', '"1.8.0"').replace('"2.5.0"', '"2.6.0"').replace('"1.9.0"', '"1.10.0"').replace('"1.11.0"', '"1.12.0"')
        t = t.replace('self.assertEqual(state["reviewed_witness_count"], 5)', 'self.assertEqual(state["reviewed_witness_count"], 19)')
        t = t.replace('self.assertEqual(state["remaining_without_reviewed_item_witness"], 14)', 'self.assertEqual(state["remaining_without_reviewed_item_witness"], 0)')
        t = t.replace('self.assertEqual(schedule["termination"]["next_item_witness"], "CORPUS-SRC-108")', 'self.assertEqual(schedule["termination"]["next_item_witness"], "NONE")')
        p.write_text(t, encoding="utf-8")

    p = ROOT / "tests/test_corpus_wit_102_platform_registration.py"
    if p.exists():
        t = p.read_text(encoding="utf-8").replace('"INCOMPLETE_5_OF_19"', '"COMPLETE_19_OF_19"')
        p.write_text(t, encoding="utf-8")

    new = ROOT / "tests/test_tp_witness_coverage_complete.py"
    new.write_text('''from pathlib import Path\nimport unittest\nimport yaml\n\nROOT = Path(__file__).resolve().parents[1]\nSHA = "43e98521c28a9ef8ede1eb7a6507d8ee78d605d0a531624d5dd20075220bda66"\n\ndef load_yaml(path):\n    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))\n\nclass CompleteTPWitnessCoverageTests(unittest.TestCase):\n    def test_all_nineteen_predecessor_sources_have_reviewed_witnesses(self):\n        corpus = load_yaml("corpus/index.yaml")\n        sources = {x["source_id"]: x for x in corpus["source_entities"]}\n        witnesses = {x["source_id"]: x for x in corpus["reviewed_witnesses"] if x["source_id"].startswith("CORPUS-SRC-1")}\n        expected = {f"CORPUS-SRC-{i:03d}" for i in range(101, 120)}\n        self.assertEqual(set(witnesses), expected)\n        for sid in expected:\n            self.assertEqual(sources[sid]["reviewed_witnesses"], [witnesses[sid]["witness_id"]])\n        self.assertEqual(corpus["coverage"]["theologico_political_reviewed_item_witnesses_registered"], 19)\n        self.assertEqual(corpus["termination"]["theologico_political_reviewed_witness_state"], "COMPLETE_19_OF_19")\n\n    def test_fifteen_witness_only_items_remain_noncertified_and_unstudied(self):\n        corpus = load_yaml("corpus/index.yaml")\n        complete = {"CORPUS-SRC-102", "CORPUS-SRC-105", "CORPUS-SRC-109", "CORPUS-SRC-111"}\n        witness_only = [x for x in corpus["source_entities"] if x["source_id"].startswith("CORPUS-SRC-1") and x["source_id"] not in complete]\n        self.assertEqual(len(witness_only), 15)\n        for source in witness_only:\n            self.assertEqual(source["item_level_source_status"], "REVIEWED_ITEM_WITNESS_REGISTERED_SEQUENTIAL_RECONSTRUCTION_REQUIRED")\n            status_entry = next(x for x in corpus["source_status_records"] if x["source_id"] == source["source_id"])\n            status = load_yaml(status_entry["path"])\n            self.assertEqual(status["termination"]["study_state"], "INCOMPLETE")\n            self.assertEqual(status["termination"]["certification"], "NOT_CERTIFIED")\n            self.assertEqual(status["termination"]["successor_effect"], "NONE")\n\n    def test_new_fingerprint_batch_uses_one_verified_container_without_collapsing_scopes(self):\n        corpus = load_yaml("corpus/index.yaml")\n        by_id = {x["witness_id"]: x for x in corpus["reviewed_witnesses"]}\n        new_ids = {f"CORPUS-WIT-{i:03d}" for i in [101,104,106,107,108,110,112,113,114,115,116,117,118,119]}\n        for wid in new_ids:\n            self.assertEqual(by_id[wid]["container_sha256"], SHA)\n            self.assertEqual(by_id[wid]["container_file_size_bytes"], 39287307)\n            self.assertEqual(by_id[wid]["container_page_count"], 526)\n        self.assertEqual(by_id["CORPUS-WIT-110"]["registered_scope"], "first paragraph")\n        self.assertEqual(by_id["CORPUS-WIT-119"]["registered_scope"], "last paragraph")\n        self.assertEqual(by_id["CORPUS-WIT-101"]["printed_page_range"], {"start": 87, "end": 136})\n        self.assertEqual(by_id["CORPUS-WIT-118"]["pdf_page_range_one_based"], {"start": 486, "end": 489})\n\nif __name__ == "__main__":\n    unittest.main()\n''', encoding="utf-8")


def main():
    update_corpus()
    update_manifest()
    update_audit()
    update_mapping()
    update_process()
    update_schedule()
    update_corpus_registry_py()
    update_tests()
    print("Materialized complete 19-of-19 Theologico-Political reviewed-witness coverage.")

if __name__ == "__main__":
    main()
