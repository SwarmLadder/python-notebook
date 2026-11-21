"""Assess a saved independent build or level in fresh processes. See curriculum/MASTERY.md."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def assess_one(row):
    sys.path.insert(0, str(ROOT / "tests"))
    from notebook_runner import run_notebook

    result = run_notebook(ROOT / row["lesson"], assess=row["independent_evidence"])
    lines = result.stdout.strip().splitlines()
    return {"concept": row["concept_id"], "build": row["independent_evidence"],
            "passed": result.mastery_passed, "feedback": "\n".join(lines[-4:])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("selection", help="concept ID (e.g. b06) or level (e.g. basics)")
    parser.add_argument("--json", action="store_true", help="print machine-readable evidence")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    rows = json.loads((ROOT / "curriculum/concepts.json").read_text())
    match = [r for r in rows if args.selection in (r["concept_id"], r["lesson"].split("/")[0])]
    if not match:
        parser.error("unknown concept or level")
    if args.worker:
        print(json.dumps(assess_one(match[0])))
        return 0
    reports = []
    for row in match:
        env = os.environ.copy()
        env.pop("PRACTICE_STRICT", None)
        try:
            proc = subprocess.run([sys.executable, __file__, row["concept_id"], "--worker"],
                                  env=env, cwd=ROOT, capture_output=True, text=True, timeout=90)
            if proc.returncode:
                raise ValueError(proc.stderr.strip().splitlines()[-1] if proc.stderr else "Worker failed")
            report = json.loads(proc.stdout)
        except (ValueError, subprocess.TimeoutExpired) as error:
            report = {"concept": row["concept_id"], "build": row["independent_evidence"],
                      "passed": False, "feedback": str(error)}
        reports.append(report)
        if not args.json:
            print(f"{report['concept']} {report['build']} — "
                  f"{'passed' if report['passed'] else 'needs work'}\n{report['feedback']}")
    if args.json:
        print(json.dumps(reports, indent=2))
    return 0 if all(r["passed"] for r in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
