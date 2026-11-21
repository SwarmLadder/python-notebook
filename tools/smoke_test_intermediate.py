#!/usr/bin/env python3
"""Legacy smoke command: execute the intermediate notebooks from independent fresh state.

Share the canonical notebook runner with pytest to avoid a second, subtly
different interpreter that may clone the default branch outside the checkout.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
from notebook_runner import run_notebook, NotebookCellError  # noqa: E402

FOLDERS = (
    ROOT / "intermediate" / "notebooks",
    ROOT / "intermediate" / "projects",
)
notebooks = sorted(path for folder in FOLDERS for path in folder.glob("*.ipynb"))
if not notebooks:
    raise SystemExit("No intermediate notebooks found")
failed = []
for path in notebooks:
    try:
        result = run_notebook(path)
        print(f"PASS {path.relative_to(ROOT)} ({result.executed_cells} code cells)")
    except Exception as error:
        failed.append((path, error))
        print(f"FAIL {path.relative_to(ROOT)}: {error}", file=sys.stderr)
if failed:
    raise SystemExit(f"{len(failed)} intermediate notebooks failed")
print(f"intermediate smoke test passed: {len(notebooks)} notebooks")
