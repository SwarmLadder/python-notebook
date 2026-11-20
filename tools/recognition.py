#!/usr/bin/env python3
"""Update ACHIEVEMENTS.md and CONTRIBUTORS.md (called by the recognition workflows).

    python tools/recognition.py achievement --login ada --level basics --name "Ada L." --pr URL
    python tools/recognition.py contributor --login ada --pr URL --title "Fix typo in lesson 06"
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACHIEVEMENTS = ROOT / "ACHIEVEMENTS.md"
CONTRIBUTORS = ROOT / "CONTRIBUTORS.md"
LEVEL_TITLES = {"basics": "🥉 Basics", "intermediate": "🥈 Intermediate", "advanced": "🥇 Advanced"}
LOGIN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})")


def _clean(text: str) -> str:
    return " ".join(re.sub(r"[|\[\]()<>`*_\\]", " ", text).split())[:80]


def add_achievement(login: str, level: str, name: str, pr: str, today: str | None = None) -> bool:
    if not LOGIN.fullmatch(login) or level not in LEVEL_TITLES:
        raise ValueError("bad login or level")
    text = ACHIEVEMENTS.read_text(encoding="utf-8")
    heading = f"## {LEVEL_TITLES[level]}"
    if f"[@{login}](" in text.split(heading, 1)[1].split("\n## ", 1)[0]:
        return False  # already recorded at this level
    row = f"| [@{login}](https://github.com/{login}) | {_clean(name) or login} | {today or dt.date.today().isoformat()} | [claim]({pr}) |"
    before, after = text.split(heading, 1)
    section, rest = (after.split("\n## ", 1) + [""])[:2]
    section = section.replace("| *Be the first!* | | | |\n", "")
    section = section.rstrip("\n") + "\n" + row + "\n"
    ACHIEVEMENTS.write_text(before + heading + section + ("\n## " + rest if rest else ""), encoding="utf-8")
    return True


def add_contributor(login: str, pr: str, title: str) -> bool:
    if not LOGIN.fullmatch(login):
        raise ValueError("bad login")
    text = CONTRIBUTORS.read_text(encoding="utf-8")
    if f"[@{login}](" in text:
        return False
    line = f"- [@{login}](https://github.com/{login}): first contribution [{_clean(title)}]({pr})\n"
    body = text.replace("- *Your name here!*\n", "").replace("- *Your name here!*", "").rstrip("\n")
    separator = "\n" if body.endswith((")", "\u200b")) or body.splitlines()[-1].startswith("- ") else "\n\n"
    CONTRIBUTORS.write_text(body + separator + line, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="kind", required=True)
    a = sub.add_parser("achievement")
    a.add_argument("--login", required=True)
    a.add_argument("--level", required=True, choices=list(LEVEL_TITLES))
    a.add_argument("--name", default="")
    a.add_argument("--pr", required=True)
    c = sub.add_parser("contributor")
    c.add_argument("--login", required=True)
    c.add_argument("--pr", required=True)
    c.add_argument("--title", default="")
    args = parser.parse_args()
    if args.kind == "achievement":
        changed = add_achievement(args.login, args.level, args.name, args.pr)
    else:
        changed = add_contributor(args.login, args.pr, args.title)
    print("updated" if changed else "already listed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
