"""Check exercises written in a Jupyter notebook with the hidden-answer practice tests.

Used by the workbook notebooks:

    from check import Checker
    check = Checker("basics_01_fundamentals")
    ...
    check("split_minutes")      # after filling in the ___ blanks of split_minutes

Each check runs the tests in practice/tests/ for that exercise against the code
you just ran in the notebook. Answers are never shown. Set PRACTICE_STRICT=1 to
make a failed check raise (used to verify achievements).
"""
from __future__ import annotations

import ast
import contextlib
import io
import os
import sys
import threading
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import grader  # noqa: E402
import practice_loader  # noqa: E402

ANSI = __import__("re").compile(r"\x1b\[[0-9;]*m")


class BlankNotFilled(NotImplementedError):
    """Raised when an exercise uses a ___ blank that hasn't been filled in."""

    def __init__(self):
        super().__init__("fill in the ___ blanks")


class _Blank:
    """The ___ placeholder. IPython already defines ___ (an old output), so the workbooks
    import this one: any use of it stops with BlankNotFilled, which the checks report as "to do"."""

    def _stop(self, *args, **kwargs):
        raise BlankNotFilled()

    __call__ = __getattr__ = __getitem__ = __iter__ = __next__ = __len__ = __bool__ = __index__ = _stop
    __add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = __truediv__ = __rtruediv__ = _stop
    __floordiv__ = __rfloordiv__ = __mod__ = __rmod__ = __pow__ = __rpow__ = __neg__ = _stop
    __lt__ = __le__ = __gt__ = __ge__ = __eq__ = __ne__ = __contains__ = __format__ = _stop
    __int__ = __float__ = __enter__ = __exit__ = __hash__ = _stop

    def __repr__(self):
        return "___"


___ = _Blank()


def _top_level_names(module: str) -> list[str]:
    tree = ast.parse((HERE / "exercises" / f"{module}.py").read_text(encoding="utf-8"))
    names = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.append(node.name)
        elif isinstance(node, ast.Assign):
            names.extend(target.id for target in node.targets if isinstance(target, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.append(node.target.id)
    return names


def tests_by_exercise(module: str) -> dict[str, list[str]]:
    """Assign each test to the LAST exercise it uses, so a check never needs later work."""
    order = _top_level_names(module)
    tree = ast.parse((HERE / "tests" / f"test_{module}.py").read_text(encoding="utf-8"))
    assignment: dict[str, list[str]] = {name: [] for name in order}
    for node in tree.body:
        if not (isinstance(node, ast.FunctionDef) and node.name.startswith("test_")):
            continue
        used = {n.attr for n in ast.walk(node) if isinstance(n, ast.Attribute)
                and isinstance(n.value, ast.Name) and n.value.id == "m" and n.attr in assignment}
        if used:
            assignment[max(used, key=order.index)].append(node.name)
    return assignment


class _Collector:
    def __init__(self):
        self.reports = []

    def pytest_runtest_logreport(self, report):
        if report.when == "call" or (report.when == "setup" and not report.passed):
            self.reports.append(report)


def _failure_text(report) -> str:
    text = ANSI.sub("", str(report.longrepr))
    keep = [line[1:].strip() for line in text.splitlines() if line.startswith("E ")]
    keep = [line.removeprefix("AssertionError: ") for line in keep if line]
    message = "\n".join(keep[:8]) or text.splitlines()[-1]
    for title, content in report.sections:
        if title.endswith("hints"):
            message += "\n" + ANSI.sub("", content)
    return message


class Checker:
    def __init__(self, module: str):
        self.module = module
        self.assignment = tests_by_exercise(module)
        self.passed: set[str] = set()

    def __call__(self, name: str, namespace: dict | None = None) -> bool | None:
        if namespace is None:
            namespace = sys._getframe(1).f_globals
        tests = self.assignment.get(name)
        if tests is None:
            print(f"Unknown exercise {name!r}. Exercises: {', '.join(self.assignment)}")
            return None
        if not tests:
            print(f"✔ {name}: no separate check; it is tested together with a later exercise.")
            return None
        if os.environ.get("PRACTICE_CHECKS") == "skip":
            print(f"(check for {name} skipped)")
            return None
        module = types.ModuleType(f"notebook_{self.module}")
        module.__dict__.update({k: v for k, v in namespace.items() if not k.startswith("__")})
        practice_loader.OVERRIDES[self.module] = module
        grader._counters.clear()
        for key in [k for k in sys.modules if k.endswith(f"test_{self.module}")]:
            del sys.modules[key]
        test_file = HERE / "tests" / f"test_{self.module}.py"
        collector = _Collector()
        import pytest
        args = [f"{test_file}::{t}" for t in tests] + [
            "-q", "-p", "no:cacheprovider", "--color=no", "--tb=short",
            f"--rootdir={ROOT}", "-c", str(ROOT / "pytest.ini")]
        status = {}
        def run():
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                status["exit_code"] = int(pytest.main(args, plugins=[collector]))

        # A worker thread has no running event loop, so tests may call asyncio.run()
        # even though Jupyter itself runs one in the main thread. Where threads are not
        # available (e.g. Python in the browser via Pyodide) run the tests directly.
        try:
            try:
                worker = threading.Thread(target=run, daemon=True)
                worker.start()
                worker.join()
            except RuntimeError:  # "can't start new thread"
                run()
        finally:
            practice_loader.OVERRIDES.pop(self.module, None)
        return self._report(name, collector.reports, tests, status.get("exit_code"))

    def _report(self, name: str, reports, expected_tests: list[str], exit_code: int | None) -> bool:
        # A passing subset is not mastery: collection errors, missing test functions,
        # interrupted runs and skipped tests must all block success.
        observed = {r.nodeid.split("::")[-1].split("[", 1)[0] for r in reports}
        missing = set(expected_tests) - observed
        total = len(reports)
        todo = [r for r in reports if r.skipped]
        failed = [r for r in reports if r.failed]
        if exit_code == 0 and not missing and not failed and not todo and total:
            self.passed.add(name)
            checks = "check" if total == 1 else f"{total} checks"
            print(f"✅ {name}: {'the' if total == 1 else 'all'} {checks} passed. Move on to the next exercise!")
            return True
        self.passed.discard(name)
        if todo and not failed and not missing and exit_code in (0, 5):
            print(f"✏️  {name}: fill in every ___ blank, run the code cell, then run this check again.")
        else:
            print(f"❌ {name}: mastery check incomplete ({total - len(failed) - len(todo)}/{total} executed checks passed).")
            if missing:
                print("Missing test coverage: " + ", ".join(sorted(missing)))
            if exit_code != 0:
                print(f"Test runner exited with status {exit_code}; no mastery credit.")
            if failed:
                print("First problem:\n" + _failure_text(failed[0]))
        ok = False
        if os.environ.get("PRACTICE_STRICT") == "1":
            raise AssertionError(f"{self.module}.{name} did not pass its checks")
        return ok

    def summary(self) -> None:
        checkable = [n for n, tests in self.assignment.items() if tests]
        done = [n for n in checkable if n in self.passed]
        print(f"{len(done)}/{len(checkable)} exercises passed in this session.")
        missing = [n for n in checkable if n not in self.passed]
        if missing:
            print("Still to do: " + ", ".join(missing))
        else:
            print("🎉 Workbook complete! See ACHIEVEMENTS.md to get your name on the course.")
