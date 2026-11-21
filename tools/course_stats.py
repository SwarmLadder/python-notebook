#!/usr/bin/env python3
"""Generate and verify README course counts from notebook and project files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
START = "<!-- course-stats:start -->"
END = "<!-- course-stats:end -->"
LEVELS = ("basics", "intermediate", "advanced")


def render() -> str:
    mapped = json.loads((ROOT / "curriculum/concepts.json").read_text(encoding="utf-8"))
    lines = [
        "| Level | Lessons | Independently assessed builds | Project notebooks |",
        "|---|---:|---:|---:|",
    ]
    for level in LEVELS:
        lessons = sorted((ROOT / level / "notebooks").glob("*.ipynb"))
        rows = [r for r in mapped if r["lesson"].startswith(level + "/")]
        builds = 0
        for path in lessons:
            doc = json.loads(path.read_text(encoding="utf-8"))
            builds += sum(cell.get("id") == "independent-build" for cell in doc["cells"])
        if len(rows) != len(lessons) or builds != len(lessons):
            raise ValueError(f"{level}: concept map, notebook count or build count disagree")
        projects = len(list((ROOT / level / "projects").glob("*.ipynb")))
        lines.append(f"| [{level.capitalize()}]({level}/README.md) | {len(lessons)} | {builds} | {projects} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="fail when README counts are outdated")
    group.add_argument("--write", action="store_true", help="refresh README counts in place")
    args = parser.parse_args()
    content = README.read_text(encoding="utf-8")
    if content.count(START) != 1 or content.count(END) != 1:
        raise ValueError("README must have exactly one start and end stats marker")
    before, rest = content.split(START, 1)
    previous, after = rest.split(END, 1)
    expected = "\n" + render() + "\n"
    if args.check:
        if previous != expected:
            print("README level counts are stale: run python tools/course_stats.py --write")
            return 1
        print("README course counts match notebooks and concept map")
    elif args.write:
        README.write_text(before + START + expected + END + after, encoding="utf-8")
        print("Updated README course counts")
    else:
        print(render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
