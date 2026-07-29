from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "findings_registry.py"
text = path.read_text(encoding="utf-8")

anchor = '    "problems/ancients-vs-moderns/synthesis/preface-to-hobbes-politische-wissenschaft.yaml",\n'
addition = '    "problems/ancients-vs-moderns/synthesis/how-to-study-spinozas-theologico-political-treatise.yaml",\n'
if addition not in text:
    text = text.replace(anchor, addition + anchor)

text = text.replace('if identity.get("version") != "1.16.0":', 'if identity.get("version") != "1.17.0":')
text = text.replace('findings registry identity.version must be 1.16.0', 'findings registry identity.version must be 1.17.0')
text = text.replace('if len(finding_ids) != 88:', 'if len(finding_ids) != 89:')
text = text.replace('expected 88 finding sets, found', 'expected 89 finding sets, found')

path.write_text(text, encoding="utf-8")
(ROOT / "tools/apply_findings_validator_revision.py").unlink()
(ROOT / ".github/workflows/apply-findings-validator-revision.yml").unlink()
