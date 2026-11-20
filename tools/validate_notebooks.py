#!/usr/bin/env python3
"""Validate structural metadata and Python syntax for educational notebooks."""
from __future__ import annotations
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
notebooks = sorted(path for level in ("basics", "intermediate") for path in (ROOT / level).rglob("*.ipynb"))
if not notebooks:
    raise SystemExit("No notebooks found")
errors = []
for path in notebooks:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
        if document.get("nbformat") != 4 or not isinstance(document.get("cells"), list):
            raise ValueError("Not a notebook v4 with cells")
        for index, cell in enumerate(document["cells"], start=1):
            if cell.get("cell_type") == "code":
                source = cell.get("source", "")
                source = "".join(source) if isinstance(source, list) else source
                try:
                    ast.parse(source, filename=f"{path}:{index}")
                except SyntaxError as error:
                    errors.append(f"{path.relative_to(ROOT)} cell {index}: {error}")
    except (OSError, json.JSONDecodeError, ValueError) as error:
        errors.append(f"{path.relative_to(ROOT)}: {error}")
if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print(f"Validated {len(notebooks)} notebooks: JSON structure and code-cell syntax OK")
