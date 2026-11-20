"""pytest configuration for the auto-graded practice modules.

Learners:  python -m pytest practice            (grades practice/exercises/)
Course CI: python -m pytest practice --solutions (grades practice/solutions/)

While you work, functions that still raise NotImplementedError are reported
as "TO DO" instead of as noisy failures, and a progress table is printed.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import practice_loader  # noqa: E402


def pytest_addoption(parser):
    parser.addoption("--solutions", action="store_true",
                     help="grade the reference solutions instead of your exercises")


def pytest_configure(config):
    practice_loader.USE_SOLUTIONS = bool(config.getoption("--solutions", default=False))


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
    if path.parent.name != "tests" or path.parent.parent != Path(__file__).resolve().parent:
        return
    # Count each test once: at "call", or at "setup" when a fixture already failed.
    if not (report.when == "call" or (report.when == "setup" and report.failed)):
        return
    module = path.stem.removeprefix("test_")
    if call.excinfo is not None and _not_started(call.excinfo.value) and not practice_loader.USE_SOLUTIONS:
        report.outcome = "skipped"
        report.longrepr = (str(path), item.location[1], "TO DO: not implemented yet")
        _progress[module]["todo"] += 1
    elif report.passed:
        _progress[module]["passed"] += 1
    elif report.failed:
        _progress[module]["failed"] += 1


def pytest_terminal_summary(terminalreporter):
    if not _progress:
        return
    target = "solutions" if practice_loader.USE_SOLUTIONS else "exercises"
    tr = terminalreporter
    tr.section(f"practice progress ({target})")
    for module in sorted(_progress):
        counts = _progress[module]
        total = sum(counts.values())
        done = counts["passed"]
        bar = "#" * round(20 * done / total) + "-" * (20 - round(20 * done / total))
        status = "complete!" if done == total else f"{counts['failed']} failing, {counts['todo']} to do"
        tr.write_line(f"{module:<42} [{bar}] {done:>2}/{total:<2} {status}")
    if not practice_loader.USE_SOLUTIONS and any(c["failed"] or c["todo"] for c in _progress.values()):
        tr.write_line("")
        tr.write_line("Tip: run one module with  python -m pytest practice -k basics_01 -q")
        tr.write_line("     and read the failing assertion: it shows the input, expected and actual values.")
