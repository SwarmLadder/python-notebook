"""pytest configuration for the auto-graded practice modules.

Learners:     python -m pytest practice
Maintainers:  python -m pytest practice --record-answers=PATH/TO/practice_solutions

Unstarted functions (still raising NotImplementedError) are reported as
"TO DO" instead of failures, and a progress table is printed at the end.
"""
from __future__ import annotations

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


_progress: dict[str, dict[str, int]] = defaultdict(lambda: {"passed": 0, "failed": 0, "todo": 0})


def _not_started(error: BaseException | None) -> bool:
    """True if a stub's NotImplementedError caused this error (Python may wrap it)."""
    seen = set()
    while error is not None and id(error) not in seen:
        if isinstance(error, NotImplementedError):
            return True
        seen.add(id(error))
        error = error.__cause__ or error.__context__
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
    if call.excinfo is not None and _not_started(call.excinfo.value) and not grader.RECORDING:
        report.outcome = "skipped"
        report.longrepr = (str(path), item.location[1], "TO DO: not implemented yet")
        _progress[module]["todo"] += 1
    elif report.passed:
        _progress[module]["passed"] += 1
    elif report.failed:
        _progress[module]["failed"] += 1


_partial_modules: set[str] = set()


def pytest_deselected(items):
    """Never write a partial answer key: remember modules with deselected tests."""
    for item in items:
        _partial_modules.add(Path(str(item.fspath)).stem.removeprefix("test_"))


def pytest_sessionfinish(session, exitstatus):
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
    if not grader.RECORDING and any(c["failed"] or c["todo"] for c in _progress.values()):
        tr.write_line("")
        tr.write_line("Next: pick one module, e.g.  python -m pytest practice -k basics_01 -q")
