from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "findings/index.yaml"
data = yaml.safe_load(path.read_text(encoding="utf-8"))

new_id = "FINDSET-158"
new_path = "problems/ancients-vs-moderns/synthesis/how-to-study-spinozas-theologico-political-treatise.yaml"

if not any(item.get("finding_set_id") == new_id for item in data["finding_sets"]):
    data["finding_sets"].append({
        "finding_set_id": new_id,
        "path": new_path,
        "record_class": "PROBLEM_LOCAL_SYNTHESIS",
        "record_role": "SOURCE_TO_PROBLEM_SYNTHESIS",
        "source_bindings": ["CORPUS-SRC-103"],
        "problem_bindings": ["ancients-vs-moderns"],
        "theologico_political_reference": "theologico-political",
        "wise_vulgar_reference": "wise-vs-vulgar",
        "derived_from": ["FINDSET-012"],
        "status": "PROVISIONAL_NOT_CERTIFIED",
        "certification": "NOT_CERTIFIED",
        "successor_effect": "NONE",
    })

for index_name, key, value in (
    ("by_problem", "ancients-vs-moderns", new_id),
    ("by_source", "CORPUS-SRC-103", new_id),
    ("by_record_class", "PROBLEM_LOCAL_SYNTHESIS", new_id),
):
    values = data["indexes"][index_name].setdefault(key, [])
    if value not in values:
        values.append(value)

identity = data["identity"]
identity["version"] = "1.17.0"
data["revision_history"] = {
    "predecessor_version": "1.16.0",
    "predecessor_blob_sha": "100b0e489da3d0553418bd3eac5ecb83f769cbc3",
    "transformation": "ADDITIVE_FORWARD_CORRECTION",
    "reason": (
        "Register the previously committed SRC-103 Ancients-vs-Moderns synthesis that was harvested "
        "without a corresponding findings-index revision. Preserve its provisional status, source-local "
        "derivation, uncertainty, and non-certification."
    ),
}

coverage = data["coverage"]
coverage["finding_sets_registered"] = 89
coverage["problem_syntheses_registered"] = 58
coverage["current_problem_synthesis_tree_yaml_records_accounted_for"] = 58

path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

# Remove this one-shot repair and its temporary workflow before committing.
(ROOT / "tools/apply_src103_findings_registry_fix.py").unlink()
(ROOT / ".github/workflows/apply-src103-registry-fix.yml").unlink()
