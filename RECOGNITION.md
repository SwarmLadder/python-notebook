# Recognition rules

There are two ways to get your name on this course. Both are checked automatically, then confirmed by a maintainer.

| Track | Who it's for | Where your name goes | How you qualify |
|---|---|---|---|
| **1. Contributors** | People who improve the course | [CONTRIBUTORS.md](CONTRIBUTORS.md) | A pull request that improves the course is **merged** |
| **2. Achievers** | Learners who finish a level | [ACHIEVEMENTS.md](ACHIEVEMENTS.md) | Every graded exercise of a level **passes**, verified by CI and approved by a maintainer |

## Track 1: Contributors

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) and open a pull request: a fix, a clearer explanation, a new exercise, a translation, a better test...
2. CI must pass (`python -m pytest`).
3. When a maintainer merges it, the **Credit contributors** workflow adds you to `CONTRIBUTORS.md`. You don't need to edit that file yourself.

**Counts:** content fixes, new or improved lessons, exercises, tests, tooling, translations, accessibility improvements.
**Doesn't count:** whitespace-only changes, mass automated edits, or PRs labelled `no-credit` by a maintainer (e.g. reverts).

## Track 2: Achievers

You qualify for a level (Basics, Intermediate or Advanced) when **all four practice modules of that level pass**. The lesson challenges are the same exercises; to claim, put your solutions in the **practice files** (`practice/exercises/<module>.py`), where `python -m pytest practice -k <module>` must pass with nothing left "to do".

Check yourself before claiming:

```bash
python tools/verify_level.py basics
```

### How to claim

1. **Fork** this repository and solve the exercises in your fork.
2. Add a claim file named after your GitHub login, `achievements/claims/<your-login>.md`:
   ```
   level: basics
   name: Your Name        # optional, how you want to be listed
   ```
3. Open a pull request from your fork. It may change **only** your exercise files and your claim file.
4. The **Verify achievement** check runs `tools/verify_level.py` on your work.
5. A maintainer reviews the PR. If everything is green and honest, they add the label `achievement-approved`.
6. The **Record achievement** workflow adds you to `ACHIEVEMENTS.md`, thanks you, and **closes the PR without merging**, so your solutions never become part of the course.

Claim one level at a time. Each level has its own row.

### Honesty rules

- Your work must be your own. Discussing ideas is fine; copying someone else's solutions is not.
- Don't modify or bypass the tests, the grader or the workflows. The verifier rejects code that imports or patches the grader, pytest internals, `sys.modules`, `builtins` and similar. A claim that tries anyway is closed, and the account may be barred from future claims.
- Be aware that a pull request is public: anyone can read the solutions in it. That's normal for open source, but please don't copy from other people's claim PRs.

## For maintainers

Before adding `achievement-approved`:

- [ ] The **Verify achievement** check is green on the latest commit.
- [ ] The PR touches only `practice/exercises/*.py` and the author's own claim file. The record workflow re-checks this through the API, but look anyway.
- [ ] Skim the solutions for obvious tampering or copied code.

The record workflow never runs code from the PR. It reads the changed-file list, the claim file and the check result through the GitHub API, then edits `ACHIEVEMENTS.md` on `main`. If `main` is protected, allow the GitHub Actions bot to push, or record achievements by hand with `python tools/recognition.py achievement ...`.
