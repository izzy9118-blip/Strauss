from pathlib import Path
from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 120
OWNER_CERT = "OWNER_CERTIFIED_FOR_OPERATIONAL_USE"
ACTIVE = "ACTIVE_OWNER_AUTHORIZED"


def load(rel):
    with (ROOT / rel).open("r", encoding="utf-8") as f:
        return yaml.load(f)


def save(rel, data):
    with (ROOT / rel).open("w", encoding="utf-8") as f:
        yaml.dump(data, f)


# Manifest: remove stale pre-authorization completion language while keeping open-research limits.
m = load("manifest.yaml")
cc = m["component_completion"]
cc["manifest"] = "OPERATIONAL_OWNER_AUTHORIZED_OPEN_TO_REVISION"
cc["adapter"] = "OPERATIONAL_OWNER_AUTHORIZED"
cc["problem_bundle_loader"] = "OPERATIONAL_OWNER_AUTHORIZED"
cc["speech_mechanism"] = "OPERATIONAL_OWNER_AUTHORIZED_OPEN_TO_REVISION"
cc["problem_objects"] = "ACTIVE_OWNER_AUTHORIZED_OPEN_RESEARCH"
cc["migration_mapping"] = "ACTIVE_OWNER_AUTHORIZED_NON_DESTRUCTIVE"
cc["behavioral_tests"] = "CONTINUOUS_VALIDATION_OF_AUTHORIZED_EVIDENCE_BOUND_RUNTIME"

tp = m["corpus"]["theologico_political_item_level_statuses"]
tp["rule"] = (
    "All nineteen predecessor items have reviewed witnesses and complete provisional source studies within their registered scopes. "
    "Original-edition comparison, independent corroboration, and broader corpus research remain open evidentiary work; "
    "STRAUSS-AUTH-001 separately authorizes operational use, successor activation, and repinning."
)
m["corpus"]["limitation"] = (
    "All nineteen predecessor writings have bounded identities, reviewed item witnesses, and complete provisional sequential studies "
    "within their registered scopes. Omission, transcription, editorial, textual-state, and predecessor-qualification limits remain "
    "active as evidentiary qualifications; no Theologico-Political item in this nineteen-source sequence remains study-pending."
)
m["findings"]["limitation"] = (
    "Proposition-level normalization, source-asymmetry repair, independent witness expansion, and comparative testing remain open. "
    "These are research tasks rather than certification, activation, or repinning gates under STRAUSS-AUTH-001."
)
save("manifest.yaml", m)

# Audit: distinguish open research from operational authority.
aud = load("audits/operational-completeness.yaml")
aud["basis"]["governing_rule"] = (
    "Witness registration, source-study completion, corroboration, textual-state comparison, and claim strength remain distinct. "
    "STRAUSS-AUTH-001 confers operational authority without converting unresolved evidence into fact or making the open corpus complete."
)
aud["summary"]["doctrinal_certification"] = OWNER_CERT
aud["summary"]["runtime_readiness"] = "FULL_OPERATIONAL_USE_WITH_EVIDENTIARY_QUALIFICATIONS"
units = aud["summary"]["completed_operational_units"]
for i, value in enumerate(units):
    if value == "speech mechanism and candidate-report contract":
        units[i] = "speech mechanism and authorized ministerial-report contract"
    elif value == "seven read-only foundational problem bundles":
        units[i] = "seven owner-authorized foundational problem bundles"
aud_tp = aud["summary"]["theologico_political_item_level_status"]
aud_tp["interpretation_limit"] = (
    "All nineteen predecessor items have complete provisional independent sequential reconstructions within registered scopes. "
    "These studies are not independent corroboration and textual-state comparisons remain pending where noted; operational authority, "
    "successor activation, and repinning are conferred separately by STRAUSS-AUTH-001."
)
deficiencies = []
for value in aud["summary"]["remaining_major_deficiencies"]:
    if value == "actual candidate ministerial reports have not been validated against the full contract stack":
        continue
    if value == "doctrinal certification, migration certification, and successor activation remain unauthorized":
        continue
    deficiencies.append(value)
aud["summary"]["remaining_major_deficiencies"] = deficiencies
save("audits/operational-completeness.yaml", aud)

# Lean mapping: remove stale read-only/candidate and 13-of-19 language.
mp = load("migrations/lean-operational-interface.yaml")
problems = mp["mappings"]["problems"]
problems["target_role"] = "permanent_questions_and_owner_authorized_operational_bundles"
problems["transformation"] = "REFERENCE_WITH_STATUS_PRESERVATION_AND_OWNER_AUTHORIZED_BUNDLE_LOADING"
problems["completion"] = "ACTIVE_OWNER_AUTHORIZED_OPEN_RESEARCH"
corpus = mp["mappings"]["corpus"]
corpus["present_function"] = [
    "register source entities separately from witnesses and studies",
    "account for all 66 YAML records in the current studies tree",
    "validate all nineteen Theologico-Political identities, aliases, scopes, reviewed-witness states, study states, fingerprints, locators, and record-local evidence limits",
    "preserve CORPUS-WIT-102 platform-reference safeguards",
    "preserve corpus gaps and textual-state comparison limits without treating them as operational authority blockers",
]
corpus["limit"] = (
    "Current-state exhaustiveness and nineteen complete provisional Theologico-Political item studies do not create a closed corpus, "
    "supply independent corroboration, resolve textual-state questions, or establish final philosophical truth. Operational use and "
    "successor activation are nevertheless authorized by STRAUSS-AUTH-001."
)
findings = mp["mappings"]["findings"]
findings["limit"] = (
    "Findings registration does not normalize every proposition or establish independent corroboration. Record-local evidence classes, "
    "uncertainty, contradiction, and derivation remain governing inside the owner-authorized runtime."
)
runtime = mp["mappings"]["runtime"]
runtime["target_role"] = "deterministic_loaders_contract_validators_and_authorized_report_builder"
runtime["completion"] = "OPERATIONAL_AND_OWNER_AUTHORIZED"
runtime["limit"] = (
    "Runtime authority does not erase evidentiary limits, admit source text through registries, or convert open research questions into settled facts."
)
save("migrations/lean-operational-interface.yaml", mp)

# Production process: certification bureaucracy is complete; research safeguards remain.
proc = load("history/production-plans/2026-07-27-ten-step-completion-process.yaml")
for step in proc["steps"]:
    if step["sequence"] == 1:
        step["limit"] = "The audit records open research gaps while the current repository remains owner-certified for operational use."
    elif step["sequence"] == 2:
        step["limit"] = "Semantic research completion remains open; operational certification and activation are already in force."
    elif step["sequence"] == 8:
        completed = step.get("completed", [])
        step["completed"] = [
            ("corpus and findings registries preserve derivation, jurisdiction, gaps, witness/study distinctions, and record-local evidence classifications"
             if value == "corpus and findings registries preserve derivation, jurisdiction, gaps, witness/study distinctions, and noncertification"
             else value)
            for value in completed
        ]
    elif step["sequence"] == 9:
        step["completed_in_current_sequence"] = [
            ("tests preserve edition-comparison, source-scope, speaker/editorial-layer, predecessor-correction, noncorroboration, and record-local evidence safeguards"
             if value.startswith("tests preserve edition-comparison")
             else value)
            for value in step.get("completed_in_current_sequence", [])
        ]
    elif step["sequence"] == 10:
        step["action"] = "Repin the certified operational Strauss interface in Sanctum."
save("history/production-plans/2026-07-27-ten-step-completion-process.yaml", proc)

# Corpus gaps: research incompleteness is not an authorization blocker.
c = load("corpus/index.yaml")
for gap in c["corpus_gaps"]:
    if gap["gap_id"] == "CORPUS-GAP-003":
        gap["statement"] = (
            "All nineteen predecessor writings have bounded source identities, reviewed item witnesses, and complete provisional independent sequential reconstructions within their registered scopes. Original or earlier textual-state comparisons, independent corroboration, and broader corpus work remain open."
        )
        gap["effect"] = "SEQUENCE_RECONSTRUCTED_AND_OPERATIONALLY_AUTHORIZED_COMPARATIVE_SYNTHESIS_REMAINS_REVISABLE"
next_units = c["termination"]["next_required_units"]
c["termination"]["next_required_units"] = [
    ("preserve predecessor history and provenance while owner-authorized successor problems remain active"
     if value == "preserve predecessor authority until separately authorized certified transition"
     else value)
    for value in next_units
]
# Clarify that legacy noncertification/no-successor labels are record-local evidence history.
new_rules = []
for value in c["validation_rules"]:
    value = value.replace("noncorroboration, noncertification, and no-successor safeguards", "noncorroboration and record-local historical certification/successor labels")
    value = value.replace("noncorroboration, noncertification, and no-successor states", "noncorroboration and record-local historical certification/successor states")
    new_rules.append(value)
c["validation_rules"] = new_rules
save("corpus/index.yaml", c)

# Findings gaps: an explicit owner authorization now exists; retain only evidentiary gaps.
f = load("findings/index.yaml")
for gap in f["findings_gaps"]:
    if gap["gap_id"] == "FINDINGS-GAP-003":
        gap["statement"] = (
            "All nineteen Theologico-Political writings have complete provisional item studies within registered scopes; textual-state comparisons, independent corroboration, and proposition normalization remain open."
        )
        gap["effect"] = "PREDECESSOR_SYNTHESIS_REMAINS_REVISABLE_WITHIN_AUTHORIZED_RUNTIME"
    elif gap["gap_id"] == "FINDINGS-GAP-005":
        gap["statement"] = (
            "Authorized ministerial reports remain subject to continuing behavioral validation as new inquiry shapes and evidence combinations are exercised."
        )
        gap["effect"] = "REPORT_TESTING_CONTINUES_WITHOUT_SUSPENDING_RUNTIME_AUTHORITY"
    elif gap["gap_id"] == "FINDINGS-GAP-006":
        gap["statement"] = (
            "STRAUSS-AUTH-001 authorizes operational use globally; record-local finding classifications remain evidentiary metadata and are not silently promoted to stronger truth claims."
        )
        gap["effect"] = "LOCAL_EVIDENCE_CLASSES_REMAIN_GOVERNING_WITHIN_OWNER_AUTHORIZED_RUNTIME"
save("findings/index.yaml", f)

print("owner authorization semantics normalized")
