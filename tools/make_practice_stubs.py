#!/usr/bin/env python3
"""Generate learner stubs in practice/exercises/ from the PRIVATE reference solutions.

Every function and method keeps its signature and docstring, but its body is
replaced by ``raise NotImplementedError``. Classes, constants and imports are
kept so the tests can import the stub straight away.

    python tools/make_practice_stubs.py --solutions DIR           # (re)write untouched stubs
    python tools/make_practice_stubs.py --solutions DIR --check   # exit 1 if a stub is stale
    python tools/make_practice_stubs.py --solutions DIR --force   # overwrite edited stubs

DIR is the private practice_solutions folder (or set PRACTICE_SOLUTIONS).
Learners: to reset a module, use  git checkout -- practice/exercises/<module>.py

Without --force, an existing stub is only rewritten if it is still untouched
(contains no implemented functions), so your work is never overwritten.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXERCISES = ROOT / "practice" / "exercises"
HEADER = (
    "# Auto-graded practice. Replace each `raise NotImplementedError` with your code.\n"
    "# Check your work:  python -m pytest practice -k {name}\n"
    "# Stuck? Re-read the docstring hint, then the lesson notebook it names.\n"
    "# Reset to a blank copy:  git checkout -- practice/exercises/{name}.py\n\n"
)


class _Stubber(ast.NodeTransformer):
    def _stub(self, node):
        body = []
        if ast.get_docstring(node, clean=False) is not None:
            body.append(node.body[0])
        body.append(ast.parse("raise NotImplementedError('TODO: implement " + node.name + "')").body[0])
        node.body = body
        return node

    visit_FunctionDef = _stub
    visit_AsyncFunctionDef = _stub


def stub_source(solution: Path) -> str:
    tree = _Stubber().visit(ast.parse(solution.read_text(encoding="utf-8")))
    ast.fix_missing_locations(tree)
    code = ast.unparse(tree)
    # ast.unparse leaves one blank line between definitions; PEP 8 wants two at top level.
    out: list[str] = []
    for line in code.splitlines():
        if line.startswith(("def ", "class ", "async def ", "@")) and out and out[-1] == "" \
                and not (len(out) > 1 and out[-2].startswith("@")):
            out.append("")
        out.append(line)
    return HEADER.format(name=solution.stem) + "\n".join(out) + "\n"


def is_untouched(path: Path) -> bool:
    """True if every function in the file still only raises NotImplementedError."""
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = [n for n in node.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
            if not (len(body) == 1 and isinstance(body[0], ast.Raise)):
                return False
    return True


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
    check, force = args.check, args.force
    EXERCISES.mkdir(parents=True, exist_ok=True)
    stale = []
    for solution in sorted(solutions_dir.glob("*.py")):
        target = EXERCISES / solution.name
        expected = stub_source(solution)
        current = target.read_text(encoding="utf-8") if target.exists() else None
        if current == expected:
            continue
        if check:
            stale.append(target.name)
        elif current is None or force or is_untouched(target):
            target.write_text(expected, encoding="utf-8")
            print(f"wrote {target.relative_to(ROOT)}")
        else:
            print(f"skipped {target.relative_to(ROOT)} (contains your work; use --force to replace)")
    if stale:
        print("out-of-date stubs: " + ", ".join(stale) + " — run python tools/make_practice_stubs.py")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
