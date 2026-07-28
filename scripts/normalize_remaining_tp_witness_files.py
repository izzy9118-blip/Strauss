#!/usr/bin/env python3
"""Rewrite the fourteen new reviewed-witness and source-status records as valid canonical YAML."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SHA = "43e98521c28a9ef8ede1eb7a6507d8ee78d605d0a531624d5dd20075220bda66"
SIZE = 39287307
PAGES = 526
FILE = "jewish-philosophy-and-the-crisis-of-modernity-essays-and-lectures-in-modern-jewish-thought_compress(1).pdf"
COLLECTION = "Jewish Philosophy and the Crisis of Modernity"
EDITOR = "Kenneth Hart Green"
PUBLISHER = "State University of New York Press"

META = {
    1: dict(sid="CORPUS-SRC-101", wid="CORPUS-WIT-101", d="progress-or-return", title="Progress or Return?", date=1952, pp=(87,136), pdf=(106,155), note="The collection states that the work was delivered as lectures at the Hillel House, University of Chicago, in November 1952. The collected text combines sections I-II from Progress or Return? The Contemporary Crisis in Western Civilization, Modern Judaism 1 (1981): 17-45, and section III from The Mutual Influence of Theology and Philosophy, The Independent Journal of Philosophy 3 (1979): 111-18."),
    4: dict(sid="CORPUS-SRC-104", wid="CORPUS-WIT-104", d="preface-to-isaac-husik-philosophical-essays", title="Preface to Isaac Husik, Philosophical Essays", date=1952, pp=(235,266), pdf=(254,285), note="The collection states that the preface first appeared in Isaac Husik, Philosophical Essays: Ancient, Medieval, and Modern, edited by Milton Nahm and Leo Strauss (Oxford: Basil Blackwell, 1952), vii-xli."),
    6: dict(sid="CORPUS-SRC-106", wid="CORPUS-WIT-106", d="freud-on-moses-and-monotheism", title="Freud on Moses and Monotheism", date=1958, pp=(285,309), pdf=(304,328), note="The 1997 collection acknowledges publication with permission of Joseph Cropsey and the Estate of Leo Strauss; its Sources section supplies no earlier publication citation for this item."),
    7: dict(sid="CORPUS-SRC-107", wid="CORPUS-WIT-107", d="why-we-remain-jews", title="Why We Remain Jews", date=1962, pp=(311,356), pdf=(330,375), note="The 1997 collection acknowledges publication with permission of Joseph Cropsey and the Estate of Leo Strauss; its Sources section supplies no earlier publication citation for this item."),
    8: dict(sid="CORPUS-SRC-108", wid="CORPUS-WIT-108", d="on-the-interpretation-of-genesis", title="On the Interpretation of Genesis", date=1957, pp=(359,376), pdf=(378,395), note="The collection states that On the Interpretation of Genesis first appeared in L'Homme 21 (1981): 5-36; the active predecessor preserves the 1957 source date."),
    10: dict(sid="CORPUS-SRC-110", wid="CORPUS-WIT-110", d="what-is-political-philosophy", title="What Is Political Philosophy?", date=1954, pp=(409,409), pdf=(428,428), scope="first paragraph", note="The collection states that the first paragraph of What Is Political Philosophy? (1954) first appeared in Leo Strauss, What Is Political Philosophy? (New York: Free Press, 1959), 9-10."),
    12: dict(sid="CORPUS-SRC-112", wid="CORPUS-WIT-112", d="letter-to-editor-state-of-israel", title="Letter to the Editor — The State of Israel", date=1957, pp=(413,414), pdf=(432,433), note="The collection states that Letter to the Editor: The State of Israel first appeared in National Review 3, no. 1 (5 January 1957): 23."),
    13: dict(sid="CORPUS-SRC-113", wid="CORPUS-WIT-113", d="introduction-to-persecution-and-the-art-of-writing", title="Introduction to Persecution and the Art of Writing", date=1952, pp=(417,429), pdf=(436,448), note="The collection states that Introduction to Persecution and the Art of Writing first appeared in Leo Strauss, Persecution and the Art of Writing (Glencoe, Illinois: Free Press, 1952), 7-21."),
    14: dict(sid="CORPUS-SRC-114", wid="CORPUS-WIT-114", d="perspectives-on-the-good-society", title="Perspectives on the Good Society", date=1963, pp=(431,445), pdf=(450,464), note="The collection states that Perspectives on the Good Society first appeared in Criterion 2, no. 3 (Summer 1963): 2-9."),
    15: dict(sid="CORPUS-SRC-115", wid="CORPUS-WIT-115", d="an-unspoken-prologue", title="An Unspoken Prologue", date=1959, pp=(449,452), pdf=(468,471), note="The collection states that An Unspoken Prologue to a Public Lecture at St. John's College first appeared in Interpretation 7, no. 3 (1978): 1-3; the active predecessor preserves the 1959 source date."),
    16: dict(sid="CORPUS-SRC-116", wid="CORPUS-WIT-116", d="preface-to-hobbes-politische-wissenschaft", title="Preface to Hobbes Politische Wissenschaft", date=1965, pp=(453,456), pdf=(472,475), note="The collection states that Preface to Hobbes Politische Wissenschaft first appeared in Interpretation 8, no. 1 (1979-80): 1-3, translated by Donald J. Maletz; the active predecessor preserves the 1965 source date."),
    17: dict(sid="CORPUS-SRC-117", wid="CORPUS-WIT-117", d="a-giving-of-accounts", title="A Giving of Accounts", date=1970, pp=(457,466), pdf=(476,485), note="The collection states that A Giving of Accounts first appeared in The College 22, no. 1 (April 1970): 1-5."),
    18: dict(sid="CORPUS-SRC-118", wid="CORPUS-WIT-118", d="plan-philosophy-and-the-law-historical-essays", title="Plan of a Book Tentatively Entitled Philosophy and the Law — Historical Essays", date=1946, pp=(467,470), pdf=(486,489), note="The collection publishes this plan with permission of Joseph Cropsey and the Estate of Leo Strauss. Its Sources section supplies no earlier publication citation; the active predecessor preserves the 1946 source date."),
    19: dict(sid="CORPUS-SRC-119", wid="CORPUS-WIT-119", d="restatement-on-xenophons-hiero", title="Restatement on Xenophon's Hiero", date=1950, pp=(471,473), pdf=(490,492), scope="last paragraph", note="The collection publishes the last paragraph of Restatement on Xenophon's Hiero with permission of Joseph Cropsey and the Estate of Leo Strauss. Its Sources section supplies no separate earlier-publication citation for this excerpt; the active predecessor preserves the 1950 source date."),
}

predecessor = yaml.safe_load((ROOT / "problems/theologico-political.yaml").read_text(encoding="utf-8"))
contrib = {x["sequence"]: x["contribution"].strip() for x in predecessor["documentary_source_basis"]["sources"]}

def r(pair):
    return {"start": pair[0], "end": pair[1]}

def dump(path: Path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")

for seq, m in META.items():
    base = ROOT / "studies/theologico-political" / m["d"]
    identity = {
        "witness_id": m["wid"], "source_id": m["sid"],
        "title": f"Reviewed item witness — {m['title']}", "version": "1.0.0",
    }
    source_identity = {
        "author": "Leo Strauss", "canonical_title": m["title"], "date": m["date"],
        "corpus_source_id": m["sid"], "source_status_id": f"CORPUS-STATUS-{m['sid'][-3:]}",
    }
    if m.get("scope"):
        source_identity["registered_scope"] = m["scope"]
    locators = {
        "printed_page_range": r(m["pp"]), "pdf_page_range_one_based": r(m["pdf"]),
        "item_completeness": "COMPLETE_REGISTERED_SCOPE", "locator_reproducibility": "COMPLETE_FOR_REVIEWED_1997_COLLECTED_ITEM",
    }
    if m.get("scope"):
        locators["registered_scope"] = m["scope"]
    witness = {
        "schema_version": 1.0, "document_type": "reviewed_item_witness_record", "identity": identity,
        "status": {"lifecycle": "REVIEWED_ITEM_WITNESS_REGISTERED", "certification": "NOT_CERTIFIED", "independent_sequential_study": "NOT_YET_COMPLETED", "original_edition_comparison": "PENDING", "source_text_admission": "NOT_REQUESTED", "successor_effect": "NONE"},
        "source_identity": source_identity,
        "publication_provenance": {"reviewed_container": COLLECTION, "editor": EDITOR, "publisher": PUBLISHER, "publication_place": "Albany", "year": 1997, "collection_source_note": m["note"], "separately_reviewed_original_or_earlier_printing": False},
        "container_witness": {"local_filename_recorded": FILE, "witness_type": "ITEM_WITHIN_SEARCHABLE_PDF_WITH_PAGE_IMAGES", "container_page_count": PAGES, "container_file_size_bytes": SIZE, "container_sha256": SHA, "repository_copy_status": "NOT_DISTRIBUTED_BY_ITEM_REGISTRY"},
        "item_locators": locators,
        "textual_condition": {"searchable_text": True, "page_images_available": True, "wording_rule": "PAGE_IMAGES_GOVERN_WHERE_EXTRACTED_TEXT_IS_UNCERTAIN_OR_CONFLICTS", "original_or_earlier_printing_compared": False},
        "jurisdiction_and_limits": {"governing_problem": "theologico-political", "distinctions": ["reviewed 1997 collected presentation from separately reviewed original or earlier textual states", "witness registration from independent sequential reconstruction", "source-level reconstruction from predecessor synthesis"], "non_effects": ["no source-level proposition promotion", "no predecessor synthesis confirmation", "no doctrinal certification", "no migration certification", "no successor activation", "no predecessor displacement"]},
        "next_required_action": {"action": "INDEPENDENT_SEQUENTIAL_RECONSTRUCTION", "range": f"printed pages {m['pp'][0]} through {m['pp'][1]}", "prerequisites_satisfied": "REVIEWED_ITEM_WITNESS_REGISTERED"},
        "termination": {"witness_state": "REGISTERED", "study_state": "INCOMPLETE", "original_edition_comparison": "PENDING", "certification": "NOT_CERTIFIED", "successor_effect": "NONE"},
    }
    dump(base / "reviewed-witness.yaml", witness)

    status_identity = {"status_id": f"CORPUS-STATUS-{m['sid'][-3:]}", "corpus_source_id": m["sid"], "canonical_title": m["title"], "author": "Leo Strauss", "date": m["date"], "version": "1.1.0"}
    if m.get("scope"):
        status_identity["registered_scope"] = m["scope"]
    reviewed = {"witness_id": m["wid"], "witness_record_path": f"studies/theologico-political/{m['d']}/reviewed-witness.yaml", "printed_page_range": r(m["pp"]), "pdf_page_range_one_based": r(m["pdf"]), "container_sha256": SHA, "container_file_size_bytes": SIZE}
    if m.get("scope"):
        reviewed["registered_scope"] = m["scope"]
    status = {
        "schema_version": 1.0, "document_type": "source_status_record", "identity": status_identity,
        "status": {"lifecycle": "REVIEWED_ITEM_WITNESS_REGISTERED", "certification": "NOT_CERTIFIED", "source_text_admission": "NOT_REQUESTED", "reviewed_witness": m["wid"], "independent_sequential_study": "NOT_YET_COMPLETED", "active_predecessor_use": "INCLUDED_IN_NINETEEN_SOURCE_SYNTHESIS"},
        "revision_history": {"predecessor_version": "1.0.0", "transformation": "FORWARD_WITNESS_REGISTRATION", "reason": "Register the fingerprinted 1997 SUNY collected witness with exact locators while preserving incomplete independent sequential reconstruction, pending original or earlier textual-state comparison, predecessor authority, noncertification, and no successor effect."},
        "registration_basis": {"active_predecessor": "problems/theologico-political.yaml", "active_predecessor_source_sequence": seq, "corpus_registry": "corpus/index.yaml", "corpus_source_id": m["sid"], "governing_problem": "theologico-political", "preserved_predecessor": "history/foundational-problems/theologico-political/STR-PROBLEM-002-v1.1-active-predecessor.yaml"},
        "verified_documentary_facts": [f"The reviewed 1997 SUNY collected witness occupies printed pages {m['pp'][0]}-{m['pp'][1]} and one-based PDF pages {m['pdf'][0]}-{m['pdf'][1]}.", f"The reviewed container has SHA-256 {SHA}, file size {SIZE} bytes, and {PAGES} PDF pages.", m["note"]],
        "predecessor_contribution_record": {"evidence_status": "PREDECESSOR_SYNTHESIS_CLAIM_NOT_YET_RETESTED_AGAINST_INDEPENDENT_SEQUENTIAL_RECONSTRUCTION", "statement": contrib[seq], "preservation_rule": "Witness registration does not independently confirm, promote, revise, or certify this predecessor statement."},
        "publication_and_witness_condition": {"reviewed_collection": COLLECTION, "editor": EDITOR, "publisher": PUBLISHER, "year": 1997, "printed_page_range": r(m["pp"]), "pdf_page_range_one_based": r(m["pdf"]), "local_file": FILE, "file_size_bytes": SIZE, "sha256": SHA, "fingerprint": "AVAILABLE", "text_condition": "SEARCHABLE_TEXT_WITH_PAGE_IMAGES", "locator_reproducibility": "COMPLETE_FOR_REVIEWED_1997_COLLECTED_ITEM", "original_or_earlier_printing_comparison": "PENDING"},
        "reviewed_witness": reviewed,
        "source_classification": {"author_relation": "PRIMARY_STRAUSS_WRITING", "documentary_rank": "REVIEWED_PRIMARY_STRAUSS_WITNESS", "analytical_use": "SOURCE_GROUNDING_AVAILABLE_SEQUENTIAL_RECONSTRUCTION_REQUIRED", "independence_limit": "The witness is documentary access to the source, not independent corroboration of claims or predecessor synthesis."},
        "prohibitions": ["Do not count witness registration as an independent sequential reconstruction.", "Do not treat the 1997 collected witness as proof of identity with an unreviewed original or earlier textual state.", "Do not certify doctrine, migration, successor activation, or predecessor displacement."],
        "next_required_actions": [f"conduct an independent sequential reading of printed pages {m['pp'][0]}-{m['pp'][1]}", "classify source-level findings by evidence status", "compare the source-level reconstruction with the active predecessor without silent harmonization", "compare separately reviewed original or earlier textual states when available"],
        "termination": {"source_identity_state": "REGISTERED", "reviewed_witness_state": "REGISTERED", "study_state": "INCOMPLETE", "independent_corroboration": "INCOMPLETE", "original_edition_comparison": "PENDING", "certification": "NOT_CERTIFIED", "successor_effect": "NONE"},
    }
    if m.get("scope"):
        status["publication_and_witness_condition"]["registered_scope"] = m["scope"]
    dump(base / "source-status.yaml", status)

print("Normalized fourteen new reviewed-witness and source-status YAML records.")
