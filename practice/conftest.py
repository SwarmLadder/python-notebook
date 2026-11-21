"""pytest configuration for the auto-graded practice modules.

Learners:     python -m pytest practice
Maintainers:  python -m pytest practice --record-answers=PATH/TO/practice_solutions

Functions whose ___ blanks are not filled in yet are reported as "TO DO"
instead of failures, and a progress table is printed at the end.
"""
from __future__ import annotations

import ast
import inspect
import json
import sys
from collections import defaultdict
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import grader  # noqa: E402
import practice_loader  # noqa: E402


def pytest_addoption(parser):
    parser.addoption("--record-answers", metavar="SOLUTIONS_DIR", default=None,
                     help="maintainers: grade the private reference solutions in SOLUTIONS_DIR "
                          "and rewrite practice/answers/*.json from their results")


def pytest_configure(config):
    solutions = config.getoption("--record-answers", default=None)
    if solutions:
        path = Path(solutions).expanduser().resolve()
        if not path.is_dir():
            raise pytest.UsageError(f"--record-answers: {path} is not a directory")
        practice_loader.SOURCE_DIR = path
        grader.RECORDING = True


PROGRESS_FILE = HERE / ".progress.json"  # local only (git-ignored): failure counts and passed tests
_hints_cache: dict[str, dict[str, list[str]]] = {}


def _load_progress() -> dict:
    try:
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"failures": {}, "passed": []}


_saved = _load_progress()
_passed_now: set[str] = set()


def _hints_for(item) -> list[tuple[str, list[str]]]:
    """Hints for the practice functions this test uses (m.<name> references)."""
    module = Path(str(item.fspath)).stem.removeprefix("test_")
    if module not in _hints_cache:
        path = HERE / "hints" / f"{module}.json"
        _hints_cache[module] = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    hints = _hints_cache[module]
    try:
        tree = ast.parse(inspect.getsource(item.function).lstrip())
    except (OSError, TypeError, SyntaxError):
        return []
    names = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name)
                and node.value.id == "m" and node.attr in hints and node.attr not in names):
            names.append(node.attr)
    return [(name, [f"Trace {name} on the failing input. Which part of the stated contract changes the result?",
                    *hints[name]]) for name in names]


_progress: dict[str, dict[str, int]] = defaultdict(lambda: {"passed": 0, "failed": 0, "todo": 0})


def _not_started(error: BaseException | None) -> bool:
    """True if an unfilled ___ blank (or a NotImplementedError) caused this error."""
    pending, seen = [error], set()
    while pending:
        current = pending.pop()
        if current is None or id(current) in seen:
            continue
        seen.add(id(current))
        if isinstance(current, NotImplementedError):
            return True
        if isinstance(current, NameError) and getattr(current, "name", None) == "___":
            return True
        if isinstance(current, (TypeError, AttributeError)) and ("_Blank" in str(current) or "___" in str(current)):
            return True  # a builtin refused the ___ placeholder, e.g. next(___) or heapq.heappush(___, ...)
        pending.extend(getattr(current, "exceptions", ()) or ())  # e.g. asyncio TaskGroup errors
        pending += [current.__cause__, current.__context__]
    return False


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    path = Path(str(item.fspath))
    if path.parent != HERE / "tests":
        return
    # Count each test once: at "call", or at "setup" when a fixture already failed.
    if not (report.when == "call" or (report.when == "setup" and report.failed)):
        return
    module = path.stem.removeprefix("test_")
    blank_in_failure = report.failed and "___" in str(report.longrepr)  # e.g. "assert ___ is <obj>"
    if call.excinfo is not None and (_not_started(call.excinfo.value) or blank_in_failure) and not grader.RECORDING:
        report.outcome = "skipped"
        report.longrepr = (str(path), item.location[1], "TO DO: fill in the ___ blanks")
        if grader.SHOW_HINTS:
            _progress[module]["todo"] += 1
    elif not grader.SHOW_HINTS:
        return  # Mastery attempts do not change guided progress or unlock hints.
    elif report.passed:
        _progress[module]["passed"] += 1
        _passed_now.add(item.nodeid)
    elif report.failed:
        _progress[module]["failed"] += 1
        if not grader.RECORDING and grader.SHOW_HINTS:
            failures = _saved["failures"].get(item.nodeid, 0) + 1
            _saved["failures"][item.nodeid] = failures
            lines = []
            for name, steps in _hints_for(item):
                for number, text in enumerate(steps[:failures], start=1):
                    lines.append(f"{name} hint {number}/{len(steps)}: {text}")
            if lines:
                if failures < max(len(steps) for _, steps in _hints_for(item)):
                    lines.append("(Fail again to unlock the next hint.)")
                report.sections.append(("hints", "\n".join(lines)))


_partial_modules: set[str] = set()


def pytest_deselected(items):
    """Never write a partial answer key: remember modules with deselected tests."""
    for item in items:
        _partial_modules.add(Path(str(item.fspath)).stem.removeprefix("test_"))


def pytest_sessionfinish(session, exitstatus):
    if not grader.RECORDING and grader.SHOW_HINTS and _progress:
        passed = (set(_saved.get("passed", [])) | _passed_now)
        _saved["passed"] = sorted(passed)
        for nodeid in _passed_now:
            _saved["failures"].pop(nodeid, None)
        try:
            PROGRESS_FILE.write_text(json.dumps(_saved, indent=1) + "\n", encoding="utf-8")
        except OSError:
            pass
    if grader.RECORDING:
        if exitstatus == 0:
            for module in _partial_modules:
                grader._recorded.pop(module, None)
            for path in grader.write_recorded():
                print(f"\nwrote {path.relative_to(HERE.parent)}", end="")
        else:
            print("\nNot writing answer keys: the reference solutions failed some tests.")


def pytest_terminal_summary(terminalreporter):
    if not _progress:
        return
    tr = terminalreporter
    tr.section("practice progress" + (" (recording answer keys)" if grader.RECORDING else ""))
    for module in sorted(_progress):
        counts = _progress[module]
        total = sum(counts.values())
        done = counts["passed"]
        filled = round(20 * done / total)
        status = "complete!" if done == total else f"{counts['failed']} failing, {counts['todo']} to do"
        tr.write_line(f"{module:<42} [{'#' * filled}{'-' * (20 - filled)}] {done:>3}/{total:<3} {status}")
    if not grader.RECORDING:
        ever = len(set(_saved.get("passed", [])) | _passed_now)
        tr.write_line("")
        tr.write_line(f"Tests you have solved so far (all runs): {ever}")
        if any(c["failed"] or c["todo"] for c in _progress.values()):
            tr.write_line("Next: pick one module, e.g.  python -m pytest practice -k basics_01 -q")
