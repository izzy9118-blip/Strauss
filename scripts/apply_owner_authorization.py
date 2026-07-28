from pathlib import Path
from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 120

OWNER_CERT = "OWNER_CERTIFIED_FOR_OPERATIONAL_USE"
ACTIVE = "ACTIVE_OWNER_AUTHORIZED"
AUTH_PATH = "governance/repository-authorization.yaml"


def load(rel):
    p = ROOT / rel
    with p.open("r", encoding="utf-8") as f:
        return yaml.load(f)


def save(rel, data):
    p = ROOT / rel
    with p.open("w", encoding="utf-8") as f:
        yaml.dump(data, f)


def bump(data, new_version, predecessor):
    if "identity" in data:
        data["identity"]["version"] = new_version
    rh = data.setdefault("revision_history", {})
    rh["predecessor_version"] = predecessor
    rh["predecessor_blob_sha"] = "PRESERVED_BY_GIT"


# Manifest: certify and authorize current state without pretending the open corpus is complete.
m = load("manifest.yaml")
bump(m, "1.20.0", "1.19.0")
m["revision_history"]["reason"] = (
    "Apply the repository-owner directive of 2026-07-28: certify and authorize the current committed repository state for "
    "operational use, activate the validated successor architecture, remove candidate-only and repin gates, and preserve "
    "evidentiary uncertainty without treating open research gaps as authority blockers."
)
st = m["status"]
st["doctrinal_certification"] = OWNER_CERT
st["runtime_readiness"] = "FULL_OPERATIONAL_USE_WITH_EVIDENTIARY_QUALIFICATIONS"
st["activation"] = ACTIVE
st["constitutional_effect"] = "FOUNDATIONAL_SUCCESSORS_ACTIVE_OWNER_AUTHORIZED"
st["governing_notice"] = (
    "The repository owner has certified and authorized the current committed state for operational use. Certification is "
    "administrative and does not erase source limits, uncertainties, edition gaps, or the open-ended nature of research."
)
m["audit"]["repinning_rule"] = (
    "Operational repinning is authorized. A pin must identify the certified commit and preserve recorded evidentiary limits; "
    "semantic incompletion is no longer an activation or repin blocker."
)
m["problem_bundle_completion"]["state"] = "SUBSTANTIVE_BUNDLES_ACTIVE_OPEN_RESEARCH"
m["problem_bundle_completion"]["limitation"] = (
    "Bundle loading preserves identity, relation coverage, path integrity, and evidence qualifications. The owner authorization "
    "permits active use without requiring a second certification ceremony."
)
m["speech"]["completion"] = "OPERATIONAL_AND_OWNER_AUTHORIZED"
m["runtime"]["permitted_operations"] = [
    "validate declared paths and substantive contracts",
    "load bounded operational context",
    "load complete foundational problem bundles",
    "load typed current-state corpus and findings registries",
    "validate reviewed-witness metadata, locators, study bindings, derivations, and jurisdiction",
    "validate typed speech requests",
    "produce authoritative Strauss ministerial reports with explicit evidence classifications",
    "use all seven owner-authorized foundational successor problems",
]
m["runtime"]["prohibited_operations"] = [
    "admit or distribute source texts through a registry",
    "allow a local filename to override title-page or copyright-page evidence",
    "treat OCR as authoritative where page images disagree or remain unclear",
    "treat source-study completion as independent corroboration",
    "promote a finding beyond its record-local evidence status without stating the promotion basis",
    "erase uncertainty, documentary limits, dissent, or predecessor history",
    "silently rewrite source findings or cross-problem jurisdiction",
]
m["sanctum_contract"]["completed_interface_repin_status"] = "AUTHORIZED_FOR_CERTIFIED_OPERATIONAL_REPIN"
m["sanctum_contract"]["output_rule"] = (
    "Validated Strauss ministerial reports are authorized outputs of this repository. Sanctum validates provenance, inquiry "
    "envelope conformance, and Assembly integration; it need not re-certify Strauss repository authority."
)
m["migration"]["mode"] = "AUTHORIZED_ADDITIVE_NON_DESTRUCTIVE"
m["migration"]["flat_problem_projection_deferred"] = False
m["migration"]["reason"] = (
    "The owner authorization activates the validated successor architecture while preserving predecessor records as history and "
    "reference. No destructive rewrite is required."
)
m["authorization"] = {"path": AUTH_PATH, "state": ACTIVE, "certification": OWNER_CERT}
save("manifest.yaml", m)

# Foundational problem registry: all seven successors active; predecessors preserved historically.
r = load("problems/registry.yaml")
bump(r, "1.8.0", "1.7.0")
r["status"]["lifecycle"] = "ACTIVE_FOUNDATIONAL_REGISTRY"
r["status"]["certification"] = OWNER_CERT
r["status"]["activation"] = ACTIVE
r["revision_history"]["reason"] = (
    "Owner certification activates all seven foundational successor problems and converts predecessor retention from an activation "
    "gate into historical preservation."
)
for p in r["canonical_problems"]:
    p["migration_status"] = "CERTIFIED_ACTIVE_OWNER_AUTHORIZED"
    if p.get("predecessor_records"):
        for pred in p["predecessor_records"]:
            pred["status"] = "PRESERVED_HISTORICAL_OR_REFERENCE_PREDECESSOR"
r["activation_rule"] = (
    "All seven successor problems are active under STRAUSS-AUTH-001. Predecessors remain recoverable as historical or reference "
    "records. New research gaps or unresolved evidentiary questions do not suspend activation."
)
r["owner_authorization"] = AUTH_PATH
save("problems/registry.yaml", r)

# Foundational architecture constitution: certified and active.
a = load("governance/foundational-problem-architecture.yaml")
bump(a, "1.1.0", "1.0.0")
a["status"]["lifecycle"] = "ACTIVE_CONSTITUTION"
a["status"]["certification"] = OWNER_CERT
a["status"]["activation"] = ACTIVE
a.setdefault("owner_authorization", {})["path"] = AUTH_PATH
a["owner_authorization"]["effect"] = (
    "Certification and activation conditions are satisfied administratively for the current validated architecture; evidentiary "
    "uncertainty remains a research property rather than an activation veto."
)
a["certification"]["authority"] = "REPOSITORY_OWNER_DIRECTIVE_2026_07_28"
a["certification"]["state"] = OWNER_CERT
a["certification"]["operational_effect"] = "ALL_SEVEN_SUCCESSORS_ACTIVE"
save("governance/foundational-problem-architecture.yaml", a)

# Source-status protocol: active and certified as a governing protocol.
p = load("protocols/source-status.yaml")
p["identity"]["protocol_version"] = "1.1.0"
p["status"]["lifecycle"] = "ACTIVE_PROTOCOL"
p["status"]["certification"] = OWNER_CERT
p["owner_authorization"] = AUTH_PATH
save("protocols/source-status.yaml", p)

# Speech mechanism: authorized ministerial output, not candidate-only.
s = load("speech/speech-mechanism.yaml")
bump(s, "1.2.0", "1.1.0")
s["status"]["lifecycle"] = "OPERATIONAL_AUTHORIZED_CONTRACT"
s["status"]["semantic_completion"] = "OPERATIONALLY_SUFFICIENT_OPEN_TO_REVISION"
s["status"]["doctrinal_certification"] = OWNER_CERT
s["status"]["runtime_limit"] = (
    "The mechanism remains evidence-bound and source-grounded, but its validated reports are authorized ministerial outputs under "
    "STRAUSS-AUTH-001 rather than candidate-only drafts."
)
s["revision_history"]["reason"] = (
    "Apply owner certification, remove candidate-only authority gating, and preserve evidence classification, uncertainty, and "
    "source-grounded reasoning as substantive safeguards."
)
s["output_contract"]["authority"] = "AUTHORIZED_STRAUSS_MINISTERIAL_REPORT"
s["output_contract"]["authorization_record"] = AUTH_PATH
if "sanctum_interoperability" in s:
    s["sanctum_interoperability"]["authority_rule"] = (
        "Sanctum validates provenance and Assembly integration; Strauss ministerial authority is already conferred by STRAUSS-AUTH-001."
    )
save("speech/speech-mechanism.yaml", s)

# Lean mapping: certified, active, repin unblocked.
l = load("migrations/lean-operational-interface.yaml")
bump(l, "1.20.0", "1.19.0")
l["status"]["lifecycle"] = "IMPLEMENTED_CERTIFIED_ACTIVE_MAPPING"
l["status"]["certification"] = OWNER_CERT
l["status"]["destructive_actions_authorized"] = False
l["revision_history"]["reason"] = (
    "Owner certification activates the current lean operational interface and removes predecessor, certification, and repin gates "
    "without authorizing destructive historical rewrites."
)
l["production_process"]["state"] = "AUTHORIZED_OPEN_RESEARCH"
l["production_process"]["current_step"] = 10
l["production_process"]["final_repin_status"] = "AUTHORIZED"
l["mapping_rules"] = [
    "No source record is deleted, moved, or silently rewritten merely to satisfy the operational interface.",
    "STRAUSS-AUTH-001 governs operational certification and activation of the current committed state.",
    "Forward revision preserves predecessor blob identity and states substantive change.",
    "Interface validity, evidence strength, corroboration, and research completeness remain distinct from operational authority.",
    "Source entity, reviewed edition, local file, OCR layer, page image, source-status record, study, synthesis, and migration ledger remain distinct.",
    "A source-specific study does not constitute independent corroboration of sources represented within it.",
    "Registry inclusion does not admit source text or erase record-local proposition classifications.",
    "Predecessors remain preserved as historical/reference records rather than activation vetoes.",
]
l["owner_authorization"] = AUTH_PATH
save("migrations/lean-operational-interface.yaml", l)

# Audit: operational certification does not pretend the open research corpus is complete.
aud = load("audits/operational-completeness.yaml")
bump(aud, "3.8.0", "3.7.0")
aud["status"]["certification"] = OWNER_CERT
aud["status"]["repository_completion"] = "OPEN_RESEARCH_REPOSITORY_OPERATIONALLY_CERTIFIED"
aud["status"]["operational_authorization"] = ACTIVE
aud["revision_history"]["reason"] = (
    "Record repository-owner certification and full operational authorization while retaining all factual, edition, witness, and "
    "corroboration gaps as open research rather than bureaucratic blockers."
)
aud["owner_authorization"] = AUTH_PATH
save("audits/operational-completeness.yaml", aud)

# Corpus and findings registries: globally certified for operational use while remaining open stores.
c = load("corpus/index.yaml")
bump(c, "1.24.0", "1.23.0")
c["status"]["certification"] = OWNER_CERT
c["revision_history"]["reason"] = (
    "Apply STRAUSS-AUTH-001 to certify the current corpus registry for operational use while preserving its explicit open-corpus gaps."
)
c["termination"]["certification"] = OWNER_CERT
c["termination"]["authorization"] = ACTIVE
c["owner_authorization"] = AUTH_PATH
save("corpus/index.yaml", c)

f = load("findings/index.yaml")
bump(f, "1.16.0", "1.15.0")
f["status"]["certification"] = OWNER_CERT
f["revision_history"]["reason"] = (
    "Apply STRAUSS-AUTH-001 to authorize the current findings store for operational use while preserving each finding's evidence class, derivation, uncertainty, and local limits."
)
f["owner_authorization"] = AUTH_PATH
save("findings/index.yaml", f)

# Completion process: certification/activation/repin bureaucracy is closed; research remains open.
proc = load("history/production-plans/2026-07-27-ten-step-completion-process.yaml")
bump(proc, "1.22.0", "1.21.0")
proc["status"]["lifecycle"] = "AUTHORIZED_OPEN_RESEARCH_SEQUENCE"
proc["status"]["certification"] = OWNER_CERT
proc["status"]["completion"] = "OPERATIONAL_CERTIFICATION_COMPLETE_RESEARCH_CONTINUES"
proc["status"]["governing_rule"] = (
    "STRAUSS-AUTH-001 closes internal certification and activation gates. Research continues under source hierarchy, uncertainty, provenance, and non-absorption safeguards."
)
proc["revision_history"]["reason"] = (
    "Owner directive certifies and activates the current repository and authorizes repinning without falsely declaring the open research corpus exhaustive."
)
for step in proc["steps"]:
    if step["sequence"] == 4:
        step["state"] = "IMPLEMENTED_AND_AUTHORIZED"
        step["limit"] = "The adapter validates evidence-bound contracts and emits authorized Strauss operational context and reports."
    elif step["sequence"] == 7:
        step["state"] = "IMPLEMENTED_ACTIVE_OPEN_RESEARCH"
    elif step["sequence"] == 8:
        step["state"] = "IMPLEMENTED_ACTIVE_OPEN_RESEARCH"
    elif step["sequence"] == 10:
        step["state"] = "AUTHORIZED"
        step.pop("prohibition", None)
        step["authorization"] = "STRAUSS-AUTH-001 permits operational repinning of the certified current state; future research advances by forward revision."
proc["current_production_unit"]["step"] = 10
proc["current_production_unit"]["next_subunit"] = {
    "title": "Open research expansion after certification",
    "state": "AUTHORIZED_CONTINUOUS",
}
proc["termination"]["state"] = "OPERATIONALLY_CERTIFIED_RESEARCH_CONTINUES"
proc["owner_authorization"] = AUTH_PATH
save("history/production-plans/2026-07-27-ten-step-completion-process.yaml", proc)

# Patch runtime validators so certification is checked against owner authorization rather than prohibited.
def patch(rel, replacements):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    for old, new in replacements:
        if old not in text:
            raise RuntimeError(f"expected text not found in {rel}: {old[:80]!r}")
        text = text.replace(old, new)
    p.write_text(text, encoding="utf-8")

patch("adapter.py", [
    ('if status.get("doctrinal_certification") != "NOT_CERTIFIED":\n        errors.append("speech mechanism must remain doctrinally NOT_CERTIFIED")',
     'if status.get("doctrinal_certification") != "OWNER_CERTIFIED_FOR_OPERATIONAL_USE":\n        errors.append("speech mechanism must carry owner operational certification")'),
    ('if output.get("authority") != "CANDIDATE_ONLY_UNTIL_SANCTUM_VALIDATION":\n        errors.append("speech output authority must remain candidate-only")',
     'if output.get("authority") != "AUTHORIZED_STRAUSS_MINISTERIAL_REPORT":\n        errors.append("speech output authority must be owner-authorized")'),
    ('if status.get("doctrinal_certification") != "NOT_CERTIFIED":\n        errors.append("manifest must state doctrinal_certification: NOT_CERTIFIED")',
     'if status.get("doctrinal_certification") != "OWNER_CERTIFIED_FOR_OPERATIONAL_USE":\n        errors.append("manifest must state owner operational certification")'),
    ('if not str(status.get("runtime_readiness", "")).startswith("LIMITED"):\n        errors.append("manifest runtime_readiness must remain explicitly LIMITED")',
     'if status.get("runtime_readiness") != "FULL_OPERATIONAL_USE_WITH_EVIDENTIARY_QUALIFICATIONS":\n        errors.append("manifest runtime_readiness must state full authorized operational use")'),
    ('if speech.get("completion") != "PARTIALLY_RECONSTRUCTED":\n        errors.append("manifest must state speech completion as PARTIALLY_RECONSTRUCTED")',
     'if speech.get("completion") != "OPERATIONAL_AND_OWNER_AUTHORIZED":\n        errors.append("manifest must state speech completion as operational and owner-authorized")'),
    ('if migration.get("mode") != "ADDITIVE_NON_DESTRUCTIVE":\n        errors.append("migration mode must remain ADDITIVE_NON_DESTRUCTIVE")',
     'if migration.get("mode") != "AUTHORIZED_ADDITIVE_NON_DESTRUCTIVE":\n        errors.append("migration mode must be authorized additive non-destructive")'),
])

patch("problem_bundles.py", [
    ('if not _status_is_noncertifying(constitution):\n        errors.append(f"{key}: constitution may not be certified or activated by the loader")',
     '# Local record status is evidentiary metadata; STRAUSS-AUTH-001 governs operational authority.'),
    ('if not _status_is_noncertifying(profile):\n        errors.append(f"{key}: inquiry profile may not be certified or activated")',
     '# Owner authorization permits active use while preserving local record metadata.'),
    ('if not _status_is_noncertifying(witnesses):\n        errors.append(f"{key}: witness registry may not be certified or activated")',
     '# Witness evidence classes remain local; operational use is owner-authorized.'),
    ('if not _status_is_noncertifying(relation_record):\n        errors.append(f"{key}: relation record may not be certified or activated")',
     '# Relation records are operational under the repository authorization.'),
    ('"authority": "READ_ONLY_NONCERTIFYING_OPERATIONAL_CONTEXT",', '"authority": "AUTHORIZED_OPERATIONAL_PROBLEM_CONTEXT",'),
    ('"authority": "CANDIDATE_RUNTIME_CONTEXT_ONLY",', '"authority": "AUTHORIZED_STRAUSS_RUNTIME_CONTEXT",'),
    ('        "non_effects": [\n            "no successor activation",\n            "no predecessor displacement",\n            "no doctrinal certification",\n            "no source-specific finding promotion",\n            "no Assembly authority",\n        ],',
     '        "authorization": "governance/repository-authorization.yaml",\n        "preserved_limits": [\n            "evidence classifications remain binding",\n            "uncertainty remains visible",\n            "no silent source-specific finding promotion",\n            "predecessor history remains recoverable",\n        ],'),
    ('"Seven complete problem bundles validated for read-only loading; "\n            "source application, migration certification, and activation remain incomplete."',
     '"Seven foundational problem bundles validated for owner-authorized operational loading; "\n            "research gaps remain evidentiary rather than activation blockers."'),
])

patch("corpus_registry.py", [
    ('if identity.get("version") != "1.23.0":\n        errors.append("corpus registry identity.version must be 1.23.0")',
     'if identity.get("version") != "1.24.0":\n        errors.append("corpus registry identity.version must be 1.24.0")'),
    ('if status.get("certification") != "NOT_CERTIFIED":\n        errors.append("corpus registry must remain NOT_CERTIFIED")',
     'if status.get("certification") != "OWNER_CERTIFIED_FOR_OPERATIONAL_USE":\n        errors.append("corpus registry must carry owner operational certification")'),
    ('if termination.get("certification") != "NOT_CERTIFIED":\n        errors.append("registry termination may not certify the corpus")',
     'if termination.get("certification") != "OWNER_CERTIFIED_FOR_OPERATIONAL_USE":\n        errors.append("registry termination must preserve owner operational certification")'),
    ('"authority": "READ_ONLY_DISCOVERY_AND_PROVENANCE_CONTEXT",', '"authority": "OWNER_AUTHORIZED_CORPUS_CONTEXT",'),
    ('        "non_effects": [\n            "no source-text admission",\n            "no doctrinal certification",\n            "no witness ranking as truth",\n            "no migration certification",\n            "no successor activation",\n            "no Assembly authority",\n        ],',
     '        "preserved_limits": [\n            "no source-text admission through the registry",\n            "no witness ranking as truth merely from registration",\n            "no erasure of documentary gaps or uncertainty",\n        ],'),
    ('"study state; corpus remains open, materially incomplete, and not certified."',
     '"study state; the open corpus is owner-certified for operational use while research gaps remain explicit."'),
])

patch("findings_registry.py", [
    ('if identity.get("version") != "1.15.0":\n        errors.append("findings registry identity.version must be 1.15.0")',
     'if identity.get("version") != "1.16.0":\n        errors.append("findings registry identity.version must be 1.16.0")'),
    ('if status.get("certification") != "NOT_CERTIFIED":\n        errors.append("findings registry must remain NOT_CERTIFIED")',
     'if status.get("certification") != "OWNER_CERTIFIED_FOR_OPERATIONAL_USE":\n        errors.append("findings registry must carry owner operational certification")'),
])

# Historical tests that hard-code current top-level versions/statuses are advanced to the new governing state.
for test in (ROOT / "tests").glob("test_*.py"):
    text = test.read_text(encoding="utf-8")
    text = text.replace('"1.19.0"', '"1.20.0"')
    text = text.replace('"3.7.0"', '"3.8.0"')
    text = text.replace('"1.21.0"', '"1.22.0"')
    text = text.replace('"1.23.0"', '"1.24.0"')
    text = text.replace('"1.15.0"', '"1.16.0"')
    text = text.replace('"BLOCKED_WHILE_SEMANTIC_COMPLETION_IS_INCOMPLETE"', '"AUTHORIZED_FOR_CERTIFIED_OPERATIONAL_REPIN"')
    text = text.replace('"BLOCKED_UNTIL_SUBSTANTIVE_COMPLETION"', '"AUTHORIZED"')
    test.write_text(text, encoding="utf-8")

# Add a focused authorization regression test.
(ROOT / "tests" / "test_owner_authorization.py").write_text('''from pathlib import Path\nimport unittest\nimport yaml\n\nROOT = Path(__file__).resolve().parents[1]\n\ndef load(rel):\n    with (ROOT / rel).open(encoding="utf-8") as f:\n        return yaml.safe_load(f)\n\nclass OwnerAuthorizationTests(unittest.TestCase):\n    def test_repository_is_owner_certified_and_active(self):\n        auth = load("governance/repository-authorization.yaml")\n        manifest = load("manifest.yaml")\n        registry = load("problems/registry.yaml")\n        self.assertEqual(auth["status"]["certification"], "OWNER_CERTIFIED")\n        self.assertEqual(auth["status"]["operational_authorization"], "FULLY_AUTHORIZED")\n        self.assertEqual(manifest["status"]["doctrinal_certification"], "OWNER_CERTIFIED_FOR_OPERATIONAL_USE")\n        self.assertEqual(manifest["status"]["activation"], "ACTIVE_OWNER_AUTHORIZED")\n        self.assertEqual(manifest["sanctum_contract"]["completed_interface_repin_status"], "AUTHORIZED_FOR_CERTIFIED_OPERATIONAL_REPIN")\n        self.assertEqual(registry["status"]["activation"], "ACTIVE_OWNER_AUTHORIZED")\n        self.assertTrue(all(p["migration_status"] == "CERTIFIED_ACTIVE_OWNER_AUTHORIZED" for p in registry["canonical_problems"]))\n\n    def test_certification_does_not_erase_open_research(self):\n        manifest = load("manifest.yaml")\n        corpus = load("corpus/index.yaml")\n        findings = load("findings/index.yaml")\n        self.assertEqual(manifest["status"]["semantic_completion"], "INCOMPLETE")\n        self.assertEqual(corpus["status"]["corpus_completion"], "INCOMPLETE_OPEN_CORPUS")\n        self.assertEqual(findings["status"]["findings_completion"], "INCOMPLETE_OPEN_FINDINGS_STORE")\n        self.assertGreater(len(corpus["corpus_gaps"]), 0)\n        self.assertGreater(len(findings["findings_gaps"]), 0)\n\nif __name__ == "__main__":\n    unittest.main()\n''', encoding="utf-8")

print("owner authorization materialized")
