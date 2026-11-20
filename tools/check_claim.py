#!/usr/bin/env python3
"""Validate an achievement claim pull request (see RECOGNITION.md).

A claim PR may only change:
  * practice/exercises/<module>.py                   (the learner's solutions)
  * <level>/exercises/<nn>_*_exercises.ipynb          (solutions written in the workbooks)
  * achievements/claims/<github-login>.md             (exactly one claim file, the author's own)

The claim file contains:
    level: basics            # basics | intermediate | advanced
    name: Ada Lovelace       # optional display name

Two modes:
  --base SHA      use `git diff` in a checkout (the read-only verify job)
  --api-pr N      use the GitHub API only, never the PR's code (the trusted record job)
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
import urllib.request

LEVELS = ("basics", "intermediate", "advanced")
ALLOWED = ["practice/exercises/*.py", "basics/exercises/*_exercises.ipynb",
           "intermediate/exercises/*_exercises.ipynb", "advanced/exercises/*_exercises.ipynb"]
NAME_OK = re.compile(r"[^\W_][\w .'-]{0,39}", re.UNICODE)


class ClaimError(Exception):
    pass


def parse_claim(text: str) -> tuple[str, str]:
    fields = {}
    for line in text.splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, value = line.split(":", 1)
            fields[key.strip().lower()] = value.split("#", 1)[0].strip()
    level = fields.get("level", "").lower()
    if level not in LEVELS:
        raise ClaimError(f"claim must say `level: basics`, `level: intermediate` or `level: advanced` (got {level!r})")
    name = fields.get("name", "")
    if name and not NAME_OK.fullmatch(name):
        raise ClaimError("name may only use letters, digits, spaces and . ' - (max 40 characters)")
    return level, name


def validate_files(files: list[str], author: str) -> str:
    claim_path = f"achievements/claims/{author}.md"
    claims = [f for f in files if f.startswith("achievements/claims/") and f != "achievements/claims/README.md"]
    if [c.lower() for c in claims] != [claim_path.lower()]:
        raise ClaimError(f"the PR must add exactly one claim file: {claim_path} (found {claims or 'none'})")
    others = [f for f in files if f not in claims and not any(fnmatch.fnmatch(f, p) for p in ALLOWED)]
    if others:
        raise ClaimError("a claim PR may only change your exercise files and your claim file; remove: " + ", ".join(others))
    return claims[0]


def _api(path: str, raw: bool = False):
    request = urllib.request.Request(f"https://api.github.com/repos/{os.environ['GITHUB_REPOSITORY']}{path}")
    request.add_header("Authorization", f"Bearer {os.environ['GH_TOKEN']}")
    request.add_header("Accept", "application/vnd.github.raw" if raw else "application/vnd.github+json")
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()
    return body.decode("utf-8") if raw else json.loads(body)


def files_from_api(pr: int) -> list[str]:
    files, page = [], 1
    while True:
        batch = _api(f"/pulls/{pr}/files?per_page=100&page={page}")
        files += [f["filename"] for f in batch if f.get("status") != "removed"] + \
                 [f["filename"] for f in batch if f.get("status") == "removed"]
        if len(batch) < 100:
            return files
        page += 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--author", required=True)
    parser.add_argument("--base")
    parser.add_argument("--api-pr", type=int)
    parser.add_argument("--head-sha")
    parser.add_argument("--require-check", help="name of a check run that must have succeeded on --head-sha")
    parser.add_argument("--github-output")
    args = parser.parse_args(argv)
    try:
        if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", args.author):
            raise ClaimError("unexpected GitHub login format")
        if args.api_pr:
            files = files_from_api(args.api_pr)
            claim = validate_files(files, args.author)
            text = _api(f"/contents/{claim}?ref={args.head_sha}", raw=True)
            if args.require_check:
                runs = _api(f"/commits/{args.head_sha}/check-runs?per_page=100")["check_runs"]
                if not any(r["name"] == args.require_check and r["conclusion"] == "success" for r in runs):
                    raise ClaimError(f"the '{args.require_check}' check has not passed on the latest commit")
        else:
            out = subprocess.run(["git", "diff", "--name-only", f"{args.base}...HEAD"], check=True,
                                 capture_output=True, text=True).stdout
            files = [f for f in out.splitlines() if f]
            claim = validate_files(files, args.author)
            text = open(claim, encoding="utf-8").read()
        level, name = parse_claim(text)
    except ClaimError as error:
        print(f"::error::Claim rejected: {error}")
        return 1
    print(f"Claim OK: @{args.author} claims {level}" + (f" as {name}" if name else ""))
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as handle:
            handle.write(f"level={level}\ndisplay_name={name}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
