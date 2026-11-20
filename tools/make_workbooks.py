#!/usr/bin/env python3
"""Build the exercise workbook notebooks from the fill-in-the-blank practice modules.

Each workbook (basics/exercises/01_..._exercises.ipynb, ...) becomes:
  setup cell -> for each exercise: short description, code with ___ blanks, check cell
  -> a final summary cell.
The checks run the hidden-answer tests in practice/tests/, so the notebook and
`python -m pytest practice` grade exactly the same way.

    python tools/make_workbooks.py           # rewrite all workbooks
    python tools/make_workbooks.py --check   # exit 1 if a workbook is out of date
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "practice"))
from notebook_check import tests_by_exercise  # noqa: E402

sys.path.insert(0, str(ROOT / "tools"))
from colab_setup import setup_code  # noqa: E402

LEVELS = ("basics", "intermediate", "advanced")


def _src(text: str) -> list[str]:
    lines = text.strip("\n").split("\n")
    return [line + "\n" for line in lines[:-1]] + [lines[-1]]


def _segment(source_lines: list[str], node: ast.AST) -> str:
    first = min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])])
    return "".join(source_lines[first - 1:node.end_lineno])


def build(workbook: Path, module: str) -> dict:
    path = ROOT / "practice" / "exercises" / f"{module}.py"
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines(keepends=True)
    tree = ast.parse(source)
    assignment = tests_by_exercise(module)
    old = json.loads(workbook.read_text(encoding="utf-8"))
    title = "".join(old["cells"][0]["source"]).splitlines()[0]
    topic = (ast.get_docstring(tree) or "").splitlines()[0].split("— ", 1)[-1].rstrip(".")

    setup, exercises = [], []
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue  # module docstring
        is_def = isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        code = _segment(lines, node)
        if is_def and (assignment.get(node.name) or "___" in code):
            exercises.append((node, code))
        else:
            setup.append(code.rstrip())

    cells = []

    def md(text):
        cells.append({"cell_type": "markdown", "metadata": {}, "source": _src(text)})

    def code(text):
        cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": _src(text)})

    md(f"{title}\n\n{topic}.\n\n**How it works:** each exercise is almost-finished code with a few `___` blanks. "
       "Fill them in, run the cell, then run the `check(...)` cell below it. ✅ means move on. "
       "❌ shows your result and the test input, never the answer, and failing twice unlocks a hint.\n\n"
       f"Prefer a terminal? The same exercises are in [`practice/exercises/{module}.py`](../../practice/exercises/{module}.py).")
    code(setup_code(workbook.parents[1].name, "exercises"))
    md("## Setup\n\nRun this cell first.")
    future = [line for line in setup if line.startswith("from __future__")]
    rest = [line for line in setup if not line.startswith("from __future__")]
    imports = [line for line in rest if line.startswith(("import ", "from "))]
    others = [line for line in rest if not line.startswith(("import ", "from "))]
    parts = ["\n".join(future + ["from check import Checker, ___  # ___ marks the blanks you fill in"]),
             f"check = Checker({module!r})"]
    if imports:
        parts.append("\n".join(imports))
    parts += others
    code("\n\n".join(parts))
    md("## Exercises")
    for number, (node, text) in enumerate(exercises, start=1):
        doc = (ast.get_docstring(node) or "").splitlines()[0] if ast.get_docstring(node) else ""
        if assignment.get(node.name):
            md(f"### {number}. `{node.name}`\n\n{doc}")
            code(text)
            code(f"check({node.name!r})")
        else:
            md(f"### {number}. `{node.name}`\n\n{doc}\n\n*Checked together with a later exercise that uses it.*")
            code(text)
    md("## Finished?")
    code("check.summary()")
    nb = {"cells": [], "metadata": old["metadata"], "nbformat": 4, "nbformat_minor": 5}
    for index, cell in enumerate(cells, start=1):
        cell["id"] = "colab-setup" if "".join(cell["source"]).startswith("# Setup: run this first") else f"cell-{index:03d}"
        nb["cells"].append({k: cell[k] for k in ("cell_type", "execution_count", "id", "metadata", "outputs", "source") if k in cell})
    return nb


def workbooks():
    for level in LEVELS:
        for workbook in sorted((ROOT / level / "exercises").glob("*_exercises.ipynb")):
            number = workbook.name.split("_", 1)[0]
            module = sorted((ROOT / "practice" / "exercises").glob(f"{level}_{number}_*.py"))[0].stem
            yield workbook, module


def main(argv: list[str]) -> int:
    stale = []
    for workbook, module in workbooks():
        text = json.dumps(build(workbook, module), indent=2, ensure_ascii=False) + "\n"
        if workbook.read_text(encoding="utf-8") != text:
            if "--check" in argv:
                stale.append(workbook.relative_to(ROOT).as_posix())
            else:
                workbook.write_text(text, encoding="utf-8")
                print(f"wrote {workbook.relative_to(ROOT)}")
    if stale:
        print("out-of-date workbooks: " + ", ".join(stale) + " — run python tools/make_workbooks.py")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
