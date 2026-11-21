"""Helpers shared by the course test-suite.

The runner executes notebook code cells top-to-bottom in one fresh namespace,
exactly like "Restart kernel and run all" in Jupyter, but without needing a
Jupyter kernel. It is deliberately standard-library only.
"""
from __future__ import annotations

import ast
import builtins
import contextlib
import io
import json
import os
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("basics", "intermediate", "advanced")


sys.path.insert(0, str(ROOT / "tools"))

def all_notebooks() -> list[Path]:
    return sorted(p for level in LEVELS for p in (ROOT / level).rglob("*.ipynb")
                  if ".ipynb_checkpoints" not in p.parts)


def notebook_id(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def cell_source(cell: dict) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else source


def code_cells(notebook: dict) -> list[tuple[int, str]]:
    """Return (1-based cell number, source) for every code cell."""
    return [(n, cell_source(c)) for n, c in enumerate(notebook["cells"], start=1)
            if c.get("cell_type") == "code"]


def is_placeholder(source: str) -> bool:
    """True for empty cells and cells that only contain comments."""
    return all(not line.strip() or line.lstrip().startswith("#")
               for line in source.splitlines())


def strip_ipython_magics(source: str) -> str:
    """Comment out IPython-only lines (%magic, !shell) so plain Python can run them."""
    lines = []
    for line in source.splitlines():
        if line.lstrip().startswith(("%", "!")):
            lines.append("# " + line)
        else:
            lines.append(line)
    return "\n".join(lines)


class NotebookCellError(AssertionError):
    """Raised with a learner-friendly message when a notebook cell fails."""


def _no_input(prompt: str = "") -> str:  # pragma: no cover - only hit on regressions
    raise NotebookCellError(
        "A notebook called input() during an automated run. Keep interactive "
        "input commented out and provide a simulated value instead."
    )


def _stopped_at_blank(error: BaseException, source: str) -> bool:
    """True if a fill-in cell stopped because of one of its own ___ blanks (expected while unanswered).

    Looks at every frame of the traceback and inside exception groups (e.g. asyncio TaskGroup)."""
    lines = source.splitlines()
    pending, seen = [error], set()
    while pending:
        current = pending.pop()
        if current is None or id(current) in seen:
            continue
        seen.add(id(current))
        if type(current).__name__ == "BlankNotFilled":
            return True
        for frame in traceback.extract_tb(current.__traceback__):
            if ("#cell" in frame.filename or frame.filename == "<exercise>") and 0 < frame.lineno <= len(lines) \
                    and "___" in lines[frame.lineno - 1]:
                return True
        pending.extend(getattr(current, "exceptions", ()) or ())
        pending.append(current.__context__)
    return False


@dataclass
class RunResult:
    executed_cells: int
    stdout: str
    mastery_passed: bool = False


def run_notebook(path: Path, *, assess: str | None = None) -> RunResult:
    """Execute every non-placeholder code cell; raise NotebookCellError on failure."""
    notebook = load(path)
    if assess and not __debug__:
        raise ValueError("Run mastery checks without Python optimization so assertions are enabled.")
    if assess:
        from exercise_context import selected_cells
        notebook = {**notebook, "cells": selected_cells(notebook, "build-check")}
    namespace = {"__name__": "__main__", "__file__": str(path)}
    stdout = io.StringIO()
    executed = 0
    previous_cwd = Path.cwd()
    original_input = builtins.input
    builtins.input = _no_input
    previous_checks = os.environ.get("PRACTICE_CHECKS")
    if assess or os.environ.get("PRACTICE_STRICT") != "1":
        os.environ["PRACTICE_CHECKS"] = "skip"  # workbook blanks are meant to be empty in the repo
    sys.path.insert(0, str(path.parent))  # Jupyter can import helpers (quiz.py) next to the notebook
    try:
        os.chdir(path.parent)  # relative data paths behave as they do in Jupyter
        work_source = None
        for number, source in code_cells(notebook):
            cell_id = notebook["cells"][number - 1].get("id")
            if assess and cell_id == "build-work":
                # A worked example earlier in the lesson may use the same name.
                namespace.pop(assess, None)
                work_source = source
            if assess and cell_id == "build-check":
                if work_source is None or assess not in namespace:
                    print(f"Define {assess} in the independent build cell.", file=stdout)
                    return RunResult(executed, stdout.getvalue())
                os.environ.pop("PRACTICE_CHECKS", None)
                namespace["check"].mastery_result = False
            if is_placeholder(source):
                continue
            code = compile(strip_ipython_magics(source), f"{notebook_id(path)}#cell{number}", "exec", dont_inherit=True)
            try:
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
                    exec(code, namespace)
            except NotebookCellError:
                raise
            except Exception as error:
                if _stopped_at_blank(error, source):
                    continue  # fill-in exercise left blank on purpose: that's how the repo ships
                first_line = source.strip().splitlines()[0][:80]
                raise NotebookCellError(
                    f"{notebook_id(path)}: code cell {number} raised "
                    f"{type(error).__name__}: {error}\n    cell starts with: {first_line!r}"
                ) from error
            except BaseException as error:  # SystemExit included: notebooks must not exit
                first_line = source.strip().splitlines()[0][:80]
                raise NotebookCellError(
                    f"{notebook_id(path)}: code cell {number} raised "
                    f"{type(error).__name__}: {error}\n    cell starts with: {first_line!r}"
                ) from error
            executed += 1
            if assess and cell_id == "build-check":
                passed = namespace["check"].mastery_result is True
                if passed and assess == "receipt":
                    # This early exercise uses variables, before functions are taught.
                    variant = dict(namespace, item="notebook", units=0)
                    del variant["receipt"]
                    exec(compile(work_source, "<receipt revision>", "exec"), variant)
                    passed = variant.get("receipt") == "notebook x 0"
                    if not passed:
                        print("Format the supplied item and units again when the order changes.", file=stdout)
                return RunResult(executed, stdout.getvalue(), passed)
    finally:
        builtins.input = original_input
        os.chdir(previous_cwd)
        sys.path.remove(str(path.parent))
        sys.modules.pop("quiz", None)
        sys.modules.pop("check", None)
        sys.modules.pop("lesson", None)
        if previous_checks is None:
            os.environ.pop("PRACTICE_CHECKS", None)
        else:
            os.environ["PRACTICE_CHECKS"] = previous_checks
    return RunResult(executed, stdout.getvalue())


def syntax_errors(notebook: dict, label: str) -> list[str]:
    errors = []
    for number, source in code_cells(notebook):
        try:
            ast.parse(strip_ipython_magics(source))
        except SyntaxError as error:
            errors.append(f"{label} cell {number}: {error.msg} (line {error.lineno})")
    return errors


def smoke_level(level: str) -> None:
    """Exercise lesson, capstone and optional maintainer notebooks in their own directories."""
    paths = sorted(path for folder in ("notebooks", "projects", "solutions")
                   for path in (ROOT / level / folder).glob("*.ipynb"))
    if not paths:
        raise SystemExit(f"No {level} notebooks found")
    failures = []
    for path in paths:
        try:
            result = run_notebook(path)
        except Exception as error:
            failures.append(f"{notebook_id(path)}: {error}")
        else:
            print(f"PASS {notebook_id(path)} ({result.executed_cells} code cells)")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"{level.title()} smoke tests passed for {len(paths)} notebooks.")
