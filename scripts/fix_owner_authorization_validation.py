from pathlib import Path
from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 120
OWNER_CERT = "OWNER_CERTIFIED_FOR_OPERATIONAL_USE"


def load(rel):
    with (ROOT / rel).open("r", encoding="utf-8") as f:
        return yaml.load(f)


def save(rel, data):
    with (ROOT / rel).open("w", encoding="utf-8") as f:
        yaml.dump(data, f)


def replace(rel, old, new):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"expected text not found in {rel}: {old!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


# Synchronize version pointers advanced by the authorization revision.
m = load("manifest.yaml")
m["audit"]["version"] = "3.8.0"
m["corpus"]["registry_version"] = "1.24.0"
m["findings"]["registry_version"] = "1.16.0"
save("manifest.yaml", m)

mapping = load("migrations/lean-operational-interface.yaml")
mapping["completion_audit"]["version"] = "3.8.0"
mapping["mappings"]["corpus"]["interface"]["registry_version"] = "1.24.0"
mapping["mappings"]["findings"]["interface"]["registry_version"] = "1.16.0"
mapping["mappings"]["speech"]["completion"] = "OPERATIONAL_AND_OWNER_AUTHORIZED"
mapping["mappings"]["runtime"]["completion"] = "OPERATIONAL_AND_OWNER_AUTHORIZED"
mapping["mappings"]["runtime"]["limit"] = (
    "Runtime remains evidence-bound and provenance-preserving. STRAUSS-AUTH-001 authorizes ministerial use, successor activation, "
    "and repinning without turning research gaps into established facts."
)
save("migrations/lean-operational-interface.yaml", mapping)

process = load("history/production-plans/2026-07-27-ten-step-completion-process.yaml")
for step in process["steps"]:
    if step["sequence"] == 1:
        step["current_version"] = "3.8.0"
    elif step["sequence"] == 2:
        step["current_version"] = "1.20.0"
save("history/production-plans/2026-07-27-ten-step-completion-process.yaml", process)

# Advance only the assertions whose governing state actually changed. Source-local
# NOT_CERTIFIED assertions deliberately remain untouched because they describe evidence,
# not repository-owner operational authority.
replace(
    "tests/test_adapter.py",
    'self.assertTrue(manifest["status"]["runtime_readiness"].startswith("LIMITED"))',
    'self.assertEqual(manifest["status"]["runtime_readiness"], "FULL_OPERATIONAL_USE_WITH_EVIDENTIARY_QUALIFICATIONS")',
)
replace(
    "tests/test_adapter.py",
    'self.assertEqual(manifest["migration"]["mode"], "ADDITIVE_NON_DESTRUCTIVE")',
    'self.assertEqual(manifest["migration"]["mode"], "AUTHORIZED_ADDITIVE_NON_DESTRUCTIVE")',
)

replace(
    "tests/test_corpus_registry.py",
    'self.assertEqual(registry["status"]["certification"], "NOT_CERTIFIED")',
    'self.assertEqual(registry["status"]["certification"], "OWNER_CERTIFIED_FOR_OPERATIONAL_USE")',
)
replace(
    "tests/test_corpus_registry.py",
    'self.assertEqual(context["authority"], "READ_ONLY_DISCOVERY_AND_PROVENANCE_CONTEXT")\n        self.assertIn("no source-text admission", context["non_effects"])\n        self.assertIn("no doctrinal certification", context["non_effects"])\n        self.assertIn("no successor activation", context["non_effects"])\n        self.assertIn("no Assembly authority", context["non_effects"])',
    'self.assertEqual(context["authority"], "OWNER_AUTHORIZED_CORPUS_CONTEXT")\n        self.assertIn("no source-text admission through the registry", context["preserved_limits"])\n        self.assertIn("no witness ranking as truth merely from registration", context["preserved_limits"])\n        self.assertIn("no erasure of documentary gaps or uncertainty", context["preserved_limits"])',
)

replace(
    "tests/test_findings_registry.py",
    'self.assertEqual(registry["status"]["certification"], "NOT_CERTIFIED")',
    'self.assertEqual(registry["status"]["certification"], "OWNER_CERTIFIED_FOR_OPERATIONAL_USE")',
)

# Undo the earlier blanket schedule-version replacement: this schedule was not revised.
replace(
    "tests/test_pr21_talmon_completion.py",
    'self.assertEqual(schedule["identity"]["version"], "1.20.0")',
    'self.assertEqual(schedule["identity"]["version"], "1.19.0")',
)

replace(
    "tests/test_final_tp_sequence_completion.py",
    'self.assertEqual(m["status"]["doctrinal_certification"],"NOT_CERTIFIED")',
    'self.assertEqual(m["status"]["doctrinal_certification"],"OWNER_CERTIFIED_FOR_OPERATIONAL_USE")',
)

replace(
    "tests/test_interface_consistency.py",
    'self.assertEqual(manifest["status"]["doctrinal_certification"], "NOT_CERTIFIED")',
    'self.assertEqual(manifest["status"]["doctrinal_certification"], "OWNER_CERTIFIED_FOR_OPERATIONAL_USE")',
)
replace(
    "tests/test_interface_consistency.py",
    'self.assertEqual(audit["status"]["repository_completion"], "INCOMPLETE")',
    'self.assertEqual(audit["status"]["repository_completion"], "OPEN_RESEARCH_REPOSITORY_OPERATIONALLY_CERTIFIED")',
)

replace(
    "tests/test_problem_bundles.py",
    'self.assertEqual(context["authority"], "CANDIDATE_RUNTIME_CONTEXT_ONLY")',
    'self.assertEqual(context["authority"], "AUTHORIZED_STRAUSS_RUNTIME_CONTEXT")',
)

# The earlier materializer intentionally leaves the priority schedule itself unchanged.
# Repair any blanket expected-version substitution in other tests without touching records.
for test in (ROOT / "tests").glob("test_*.py"):
    text = test.read_text(encoding="utf-8")
    if "theologico-political-reviewed-witness-priority.yaml" in text:
        # Only schedule version assertions are reset; manifest/mapping 1.20 assertions remain.
        text = text.replace('schedule["identity"]["version"], "1.20.0"', 'schedule["identity"]["version"], "1.19.0"')
    test.write_text(text, encoding="utf-8")

# Update findings validator's human-readable success message to the authorized semantics.
fr = ROOT / "findings_registry.py"
text = fr.read_text(encoding="utf-8")
text = text.replace(
    "Typed findings registry validation passed for the current committed findings state; findings remain open, materially incomplete, and not certified.",
    "Typed findings registry validation passed for the current committed findings state; the open findings store is owner-certified for operational use while evidentiary limits remain explicit.",
)
fr.write_text(text, encoding="utf-8")

print("owner authorization validation alignment complete")
