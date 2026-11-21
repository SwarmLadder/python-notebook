#!/usr/bin/env python3
"""Generate fill-in-the-blank exercises in practice/exercises/ from the PRIVATE solutions.

Learners don't start from an empty function. Each function keeps most of the
reference solution, but its key parts (a condition, a loop range, the value
it returns...) are replaced by ``___``. Running the code before filling a
blank raises ``NameError: name '___' is not defined``, which the practice
tests report as "to do".

    python tools/make_practice_stubs.py --solutions DIR           # (re)write untouched files
    python tools/make_practice_stubs.py --solutions DIR --check   # exit 1 if a file is stale
    python tools/make_practice_stubs.py --solutions DIR --force   # overwrite edited files

DIR is the private practice_solutions folder (or set PRACTICE_SOLUTIONS).
Learners: to reset a module, use  git checkout -- practice/exercises/<module>.py

Without --force, a file is only rewritten if it still matches the previously
generated version (`git diff` clean), so your work is never overwritten.
"""
from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXERCISES = ROOT / "practice" / "exercises"
BLANK = "___"
HEADER = (
    "# Fill in every ___ so the function does what its docstring says.\n"
    "# Check your work:  python -m pytest practice -k {name}   (or run check() in the lesson)\n"
    "# Stuck? Fail a check twice to unlock the hints.\n"
    "# Reset this file:  git checkout -- practice/exercises/{name}.py\n\n"
)
# Expression slots worth blanking, most instructive first.
PRIORITY = {ast.If: 0, ast.While: 0, ast.Return: 1, ast.AugAssign: 2, ast.For: 3, ast.Assign: 4, ast.Expr: 5,
            ast.With: 6, ast.AsyncWith: 6}


def _slot(statement: ast.stmt):
    """The expression inside `statement` that we may replace with ___ (or None)."""
    if isinstance(statement, (ast.If, ast.While)):
        return statement.test
    if isinstance(statement, ast.Return):
        value = statement.value
        return None if value is None or (isinstance(value, ast.Constant) and value.value in (True, False, None)) else value
    if isinstance(statement, (ast.AugAssign, ast.Assign)):
        value = statement.value
        return None if isinstance(value, ast.Constant) else value
    if isinstance(statement, ast.For):
        return statement.iter
    if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call):
        call = statement.value
        if call.args and not isinstance(call.args[0], ast.Constant):
            return call.args[0]
        if len(call.args) > 1:
            return (call.args[1], call.args[-1])  # e.g. logger.info("fmt %s", ___)
        if call.args:
            return call.func  # e.g. ___("CREATE TABLE ...")
    if isinstance(statement, (ast.With, ast.AsyncWith)):
        return statement.items[0].context_expr
    return None


def _statements(body):
    for statement in body:
        if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue  # nested definitions are handled on their own
        yield statement
        for field in ("body", "orelse", "finalbody"):
            yield from _statements(getattr(statement, field, []) or [])
        for handler in getattr(statement, "handlers", []) or []:
            yield from _statements(handler.body)


def _choose_blanks(function: ast.FunctionDef | ast.AsyncFunctionDef) -> list:
    body = function.body[1:] if ast.get_docstring(function) is not None else function.body
    if len(body) == 1 and isinstance(body[0], ast.Raise):
        return []  # e.g. an abstract method that is *supposed* to raise
    candidates = []
    for order, statement in enumerate(_statements(body)):
        expr = _slot(statement)
        if expr is not None:
            rank = PRIORITY.get(type(statement), 9)
            plain = isinstance(expr, (ast.Name, ast.Attribute)) or (
                isinstance(expr, ast.Tuple) and all(isinstance(e, ast.Name) for e in expr.elts))
            if plain and isinstance(statement, ast.Assign):
                continue  # `self.owner = owner` just copies an argument: nothing to learn
            if plain:
                rank = 8  # `return total` would be a giveaway, not a puzzle
            candidates.append((rank, order, expr))
    lines = sum(1 for _ in _statements(body))
    wanted = 1 if lines <= 3 else 2 if lines <= 8 else 3
    chosen: list = []
    for _, _, expr in sorted(candidates, key=lambda c: (c[0], c[1])):
        if len(chosen) == wanted:
            break
        first, last = expr if isinstance(expr, tuple) else (expr, expr)
        if any(first.lineno <= (c[1] if isinstance(c, tuple) else c).end_lineno
               and (c[0] if isinstance(c, tuple) else c).lineno <= last.end_lineno for c in chosen):
            continue  # one blank per line keeps each gap readable
        chosen.append(expr)
    if not chosen and body:
        # Fall back to the first statement with any expression.
        for statement in _statements(body):
            expr = _slot(statement)
            if expr is not None:
                chosen.append(expr)
                break
    return chosen


def scaffold_source(solution: Path) -> str:
    source = solution.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    spans = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for expr in _choose_blanks(node):
                first, last = expr if isinstance(expr, tuple) else (expr, expr)
                start = offsets[first.lineno - 1] + len(lines[first.lineno - 1].encode("utf-8")[:first.col_offset].decode("utf-8"))
                end = offsets[last.end_lineno - 1] + len(lines[last.end_lineno - 1].encode("utf-8")[:last.end_col_offset].decode("utf-8"))
                spans.append((start, end))
    for start, end in sorted(spans, reverse=True):
        source = source[:start] + BLANK + source[end:]
    ast.parse(source)  # the scaffold must stay valid Python
    return HEADER.format(name=solution.stem) + source


def _is_untouched(path: Path) -> bool:
    """True if git reports no local edits (so it is safe to regenerate)."""
    result = subprocess.run(["git", "diff", "--quiet", "--", str(path)], cwd=ROOT)
    return result.returncode == 0


def main(argv: list[str]) -> int:
    import argparse
    import os
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--solutions", default=os.environ.get("PRACTICE_SOLUTIONS"),
                        help="private practice_solutions folder")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    if not args.solutions:
        parser.error("pass --solutions DIR (the private reference solutions)")
    solutions_dir = Path(args.solutions).expanduser()
    EXERCISES.mkdir(parents=True, exist_ok=True)
    stale = []
    for solution in sorted(solutions_dir.glob("*.py")):
        target = EXERCISES / solution.name
        expected = scaffold_source(solution)
        current = target.read_text(encoding="utf-8") if target.exists() else None
        if current == expected:
            continue
        if args.check:
            stale.append(target.name)
        elif current is None or args.force or _is_untouched(target):
            target.write_text(expected, encoding="utf-8")
            print(f"wrote {target.relative_to(ROOT)}")
        else:
            print(f"skipped {target.relative_to(ROOT)} (contains your work; use --force to replace)")
    if stale:
        print("out-of-date exercises: " + ", ".join(stale) + " — run python tools/make_practice_stubs.py")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
