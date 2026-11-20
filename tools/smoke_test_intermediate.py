#!/usr/bin/env python3
"""Run Intermediate notebook code cells with fresh state and no Jupyter dependency.

Guided notebooks use only standard-library examples and offline data.
This is an execution smoke test, not a substitute for full notebook rendering.
"""

from __future__ import annotations

from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import json
from pathlib import Path
import traceback
import sys

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = (
    ROOT / "intermediate" / "notebooks",
    ROOT / "intermediate" / "solutions",
    ROOT / "intermediate" / "projects",
)
files = sorted(path for folder in FOLDERS for path in folder.glob("*.ipynb"))
if not files:
    raise SystemExit("No Intermediate notebooks found")
failures = []
for path in files:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
        namespace = {"__name__": "__main__", "__file__": str(path)}
        sys.path.insert(0, str(path.parent))  # like Jupyter: import helpers (quiz.py) beside the notebook
        sys.modules.pop("quiz", None)
        executed = 0
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            for index, cell in enumerate(document["cells"], start=1):
                if cell.get("cell_type") != "code":
                    continue
                content = cell.get("source", "")
                content = "".join(content) if isinstance(content, list) else content
                if not content.strip() or all(
                    line.strip().startswith("#") or not line.strip()
                    for line in content.splitlines()
                ):
                    continue
                try:
                    exec(compile(content, f"{path}:{index}", "exec"), namespace)
                    executed += 1
                except Exception as error:
                    if "___" in content:
                        continue  # fill-in exercise left blank on purpose
                    failures.append((path, index, f"{type(error).__name__}: {error}"))
                    break
        print(f"{'PASS' if not failures or failures[-1][0] != path else 'FAIL'} "
              f"{path.relative_to(ROOT)} ({executed} code cells)")
    except Exception as error:
        failures.append((path, 0, f"{type(error).__name__}: {error}"))
        traceback.print_exc()

if failures:
    for path, index, error in failures:
        print(f"FAILED: {path.relative_to(ROOT)} cell {index} — {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"Intermediate notebook execution smoke test passed: {len(files)} notebooks")
