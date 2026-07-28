#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "studies/theologico-political/progress-or-return/source-status.yaml"
data = yaml.safe_load(path.read_text(encoding="utf-8"))
publication = data["publication_and_witness_condition"]
publication["sha256"] = "43e98521c28a9ef8ede1eb7a6507d8ee78d605d0a531624d5dd20075220bda66"
publication["fingerprint_state"] = "AVAILABLE"
path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")
print("Repaired CORPUS-SRC-101 source-status fingerprint compatibility.")
