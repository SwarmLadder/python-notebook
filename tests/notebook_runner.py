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
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("basics", "intermediate", "advanced")


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


@dataclass
class RunResult:
    executed_cells: int
    stdout: str


def run_notebook(path: Path) -> RunResult:
    """Execute every non-placeholder code cell; raise NotebookCellError on failure."""
    notebook = load(path)
    namespace = {"__name__": "__main__", "__file__": str(path)}
    stdout = io.StringIO()
    executed = 0
    previous_cwd = Path.cwd()
    original_input = builtins.input
    builtins.input = _no_input
    try:
        os.chdir(path.parent)  # relative data paths behave as they do in Jupyter
        for number, source in code_cells(notebook):
            if is_placeholder(source):
                continue
            code = compile(strip_ipython_magics(source), f"{notebook_id(path)}#cell{number}", "exec")
            try:
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
                    exec(code, namespace)
            except NotebookCellError:
                raise
            except BaseException as error:  # SystemExit included: notebooks must not exit
                first_line = source.strip().splitlines()[0][:80]
                raise NotebookCellError(
                    f"{notebook_id(path)}: code cell {number} raised "
                    f"{type(error).__name__}: {error}\n    cell starts with: {first_line!r}"
                ) from error
            executed += 1
    finally:
        builtins.input = original_input
        os.chdir(previous_cwd)
    return RunResult(executed, stdout.getvalue())


def syntax_errors(notebook: dict, label: str) -> list[str]:
    errors = []
    for number, source in code_cells(notebook):
        try:
            ast.parse(strip_ipython_magics(source))
        except SyntaxError as error:
            errors.append(f"{label} cell {number}: {error.msg} (line {error.lineno})")
    return errors
