#!/usr/bin/env python3
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'studies/theologico-political/how-to-study-spinozas-theologico-political-treatise/sequential-reconstruction.yaml'
text = PATH.read_text(encoding='utf-8')
lines = []
for line in text.splitlines():
    m = re.match(r'^(\s+)proposition: (?![>|])(.*)$', line)
    if m:
        indent, value = m.groups()
        lines.append(f'{indent}proposition: >')
        lines.append(f'{indent}  {value}')
    else:
        lines.append(line)
text = '\n'.join(lines) + '\n'
# Validate before writing so a repair cannot silently make the record worse.
yaml.safe_load(text)
PATH.write_text(text, encoding='utf-8')
print('Normalized and validated SRC103 sequential-reconstruction YAML.')
