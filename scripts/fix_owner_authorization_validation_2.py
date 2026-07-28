from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "tests" / "test_problem_bundles.py"
text = p.read_text(encoding="utf-8")
replacements = [
    ('self.assertIn("no doctrinal certification", context["non_effects"])',
     'self.assertIn("evidence classifications remain binding", context["preserved_limits"])'),
    ('self.assertIn("no predecessor displacement", context["non_effects"])',
     'self.assertIn("predecessor history remains recoverable", context["preserved_limits"])'),
    ('"READ_ONLY_NONCERTIFYING_OPERATIONAL_CONTEXT",',
     '"AUTHORIZED_OPERATIONAL_PROBLEM_CONTEXT",'),
]
for old, new in replacements:
    if old not in text:
        raise RuntimeError(f"expected test contract not found: {old}")
    text = text.replace(old, new)
p.write_text(text, encoding="utf-8")
print("problem-bundle authorization test alignment complete")
