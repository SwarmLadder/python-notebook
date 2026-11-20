#!/usr/bin/env python3
"""Execute Advanced lesson, reference and capstone notebook cells in isolation.

This smoke test checks reproducibility of documented code examples using the
Python standard library; it does not replace a complete interactive Jupyter run.
"""
from __future__ import annotations

from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import json
from pathlib import Path
import sys
import traceback

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = [
    ROOT / "advanced" / "notebooks",
    ROOT / "advanced" / "solutions",
    ROOT / "advanced" / "projects",
]
notebooks = sorted(path for folder in FOLDERS for path in folder.glob("*.ipynb"))
if not notebooks:
    raise SystemExit("No Advanced notebooks were found")

failures: list[tuple[Path, int, str]] = []
for path in notebooks:
    executed = 0
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        namespace = {"__name__": "__main__", "__file__": str(path)}
        sys.path.insert(0, str(path.parent))  # like Jupyter: import helpers (quiz.py) beside the notebook
        sys.modules.pop("quiz", None)
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            for cell_number, cell in enumerate(notebook["cells"], start=1):
                if cell.get("cell_type") != "code":
                    continue
                source = cell.get("source", "")
                source = "".join(source) if isinstance(source, list) else source
                if not source.strip() or all(
                    not line.strip() or line.strip().startswith("#")
                    for line in source.splitlines()
                ):
                    continue
                try:
                    exec(compile(source, f"{path}:{cell_number}", "exec"), namespace)
                    executed += 1
                except Exception as error:
                    failures.append((path, cell_number, f"{type(error).__name__}: {error}"))
                    break
        print(f"{'FAIL' if failures and failures[-1][0] == path else 'PASS'} "
              f"{path.relative_to(ROOT)} ({executed} code cells)")
    except Exception as error:
        failures.append((path, 0, f"{type(error).__name__}: {error}"))
        traceback.print_exc()
if failures:
    for path, number, error in failures:
        print(f"FAILED: {path.relative_to(ROOT)} cell {number}: {error}", file=sys.stderr)
    raise SystemExit(1)
print(f"Advanced smoke tests passed for {len(notebooks)} notebooks.")
