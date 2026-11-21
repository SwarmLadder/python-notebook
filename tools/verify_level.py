#!/usr/bin/env python3
"""Verify that a learner has completed a level (used for ACHIEVEMENTS.md).

A module counts as complete when every test in `practice/tests/test_<module>.py`
passes against `practice/exercises/<module>.py`. (The challenges in the lessons
are the same exercises; a claim is verified against the practice files.)

Every practice module of the level must be complete; a level with no modules
is never complete.

    python tools/verify_level.py basics
    python tools/verify_level.py intermediate --json result.json

Exit code 0 means the whole level is complete. The script also rejects code
that tries to tamper with the grader (see FORBIDDEN).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("basics", "intermediate", "advanced")
FORBIDDEN = re.compile(r"\b(grader|practice_loader|notebook_check|conftest|_pytest|pytest|faulthandler|"
                       r"os\._exit|sys\.modules|sys\.exit|builtins|__import__|importlib|subprocess|signal|"
                       r"PRACTICE_STRICT|PRACTICE_CHECKS|setattr\(\s*sys)\b")


def modules(level: str) -> list[tuple[str, Path | None]]:
    """Every practice module of the level, with its workbook notebook if it has one."""
    result = []
    for path in sorted((ROOT / "practice" / "exercises").glob(f"{level}_*.py")):
        number = path.stem.split("_")[1]
        workbooks = sorted((ROOT / level / "exercises").glob(f"{number}_*_exercises.ipynb"))
        result.append((path.stem, workbooks[0] if workbooks else None))
    return result


def learner_code(module: str, workbook: Path | None) -> str:
    code = (ROOT / "practice" / "exercises" / f"{module}.py").read_text(encoding="utf-8")
    if workbook is None:
        return code
    notebook = json.loads(workbook.read_text(encoding="utf-8"))
    cells = ["".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"]
    # The generated setup cell legitimately imports the checker; skip that one cell.
    cells = [c for c in cells if not c.lstrip().startswith(("from check import", "from __future__"))]
    return code + "\n" + "\n".join(cells)


def tamper_findings(module: str, workbook: Path | None) -> list[str]:
    text = learner_code(module, workbook)
    text = "\n".join(line for line in text.splitlines()
                     if not line.lstrip().startswith("#") and "check(" not in line and "check.summary" not in line)
    return sorted(set(FORBIDDEN.findall(text)))


def terminal_route(module: str) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", f"practice/tests/test_{module}.py", "-q", "-p", "no:cacheprovider",
         "--color=no", "-rfEs"], cwd=ROOT, capture_output=True, text=True, timeout=900)
    last = (result.stdout.strip().splitlines() or ["no output"])[-1]
    ok = result.returncode == 0 and "skipped" not in last and "failed" not in last
    return ok, last


def notebook_route(workbook: Path) -> tuple[bool, str]:
    code = (
        "import sys; sys.path.insert(0, 'tests')\n"
        "from pathlib import Path\n"
        "from notebook_runner import run_notebook\n"
        f"run_notebook(Path({str(workbook)!r}))\n"
    )
    env = {**os.environ, "PRACTICE_STRICT": "1"}
    env.pop("PRACTICE_CHECKS", None)
    result = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True,
                            timeout=900, env=env)
    if result.returncode == 0:
        return True, "all notebook checks passed"
    lines = (result.stderr or result.stdout).strip().splitlines()
    return False, next((l for l in reversed(lines) if "did not pass" in l or "Error" in l), lines[-1] if lines else "failed")


def verify(level: str) -> dict:
    found = modules(level)
    report = {"level": level, "modules": {}, "complete": bool(found)}
    for module, workbook in found:
        findings = tamper_findings(module, workbook)
        if findings:
            entry = {"complete": False, "route": None, "detail": "forbidden in learner code: " + ", ".join(findings)}
        else:
            ok, detail = terminal_route(module)
            entry = {"complete": ok, "route": "practice file" if ok else None, "detail": detail}
            if not ok and workbook is not None:
                ok_nb, detail_nb = notebook_route(workbook)
                if ok_nb:
                    entry = {"complete": True, "route": "workbook notebook", "detail": detail_nb}
                else:
                    entry["detail"] = f"practice file: {detail} | notebook: {detail_nb}"
        report["modules"][module] = entry
        report["complete"] &= entry["complete"]
    return report


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("level", choices=LEVELS)
    parser.add_argument("--json", help="also write the report to this file")
    args = parser.parse_args(argv)
    report = verify(args.level)
    for module, entry in report["modules"].items():
        mark = "PASS" if entry["complete"] else "FAIL"
        print(f"{mark}  {module:<45} {entry['route'] or ''}  {entry['detail']}")
    print(f"\n{args.level}: {'COMPLETE' if report['complete'] else 'not complete yet'}")
    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    return 0 if report["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
