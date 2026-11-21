# Browser learning experience: verified integration boundary

This note records an inspection of the staging deployment on 2026-11-21.
The authoritative Python lessons live in this repository. The Lab website
is a separate deployed application and is **not** changed by Python commits.

## Confirmed integration behavior

The deployed site's available source maps expose the following component paths:

- `src/workers/runner.ts` sends student code to a Pyodide Web Worker at
  `/assets/py-worker.js`. It does not start an IPython kernel, so
  `lesson.pending_exercise()`'s IPython input transformer cannot be relied on.
- `src/features/notebook/Notebook.tsx` runs the saved editor text, collecting
  stdout/stderr. The shown code has no AST-based preflight for `___` blanks.
  It classifies errors or a `❌` marker as a failed run; other output is
  classified as completed execution or a recognized pass.
- `src/features/progress/store.ts` recognizes guided success using the
  prefix `✅ Exercise <number>: correct`. The Python helper deliberately keeps
  this prefix when printing `correct — Passed`.
- The same progress store records successful keys and currently does not
  remove them when a later edit/rerun fails. Thus *historical practice
  completion* can remain after the current submission becomes incorrect.
- The visible source includes a CodeMirror-based Python editor. Its source
  indicates Python syntax support and indentation commands, but that is not
  a visual or interactive browser test.

Source maps establish code paths, not proof of a successful end-to-end browser
interaction. The staging URL was not accessible through the available web
browser. No deployed site code was modified or redeployed as part of this PR.

## Python-side protection now available

`Exercises.__call__` detects a literal `___` name in the executing Python
code object, including nested functions, before evaluating the submitted
value. This catches even a bare `___` statement in a Pyodide-style
`exec` environment. It does not confuse comments, string literals, or a
Python attribute called `___` with a learner placeholder.

The shared helper prints distinct statuses:

- `Not attempted` — missing placeholder, without counting a wrong attempt
- `Needs improvement` — submitted code executed but produced a wrong result
- `correct — Passed` — graded result matches the exercise fingerprint

The actual Basics 16 running-total cell keeps its original indentation
and open-ended implementation line. Its example and the exercise input agree.

## Required platform work (separate application)

1. On **every run**, classify the current source before execution using an
   AST-aware check. Call `check.pending(number)` or display a first-class
   `not_attempted` outcome for an unresolved `___`. Never use a raw
   `code.includes('___')` check, which misclassifies comments and strings.
2. Separate the result of *running* Python from an actual *graded pass*.
   Parse structured status fields (exercise ID, attempt, hint use, grader
   version and result) rather than relying only on printed text. Do not
   report a pass when a required test was skipped.
3. Invalidate **current mastery** on edit and failed rerun. Historical
   practice-completion timestamps may be retained separately, but cannot
   count as passing evidence for the changed code.
4. Verify saved editor content and indentation round-trip exactly to
   the interpreter. Run the current saved code, not cached output.
5. Deploy an updated course snapshot after merging Python changes; a
   GitHub commit does not automatically update bundled staging assets.
6. Confirm per-student Python runtimes have isolation, bounds on execution,
   and safe handling of long-running code and exceptions.

## Browser acceptance checklist

Reopen Basics 16 Exercise 2 in a clean session. Run untouched `___`,
then an incorrect complete line, then `running.append(total)`, then a
wrong line again. Expect, respectively: Not attempted, Needs improvement,
Passed, Needs improvement. The final run must not retain current-pass
status. Repeat with `running += [total]`, comments and strings containing
`___`, and edits that preserve four-space indentation. Verify the editor's
visible question and code both use `[1, 2, 3, 4]`.

Run a representative import-dependent lesson in an empty browser session
to confirm provided setup imports are executed. Repeat in a genuine Jupyter
kernel to compare semantics. Check that independent builds are not granted
achievement or qualification merely for running a notebook.

The source repository for the deployed Lab frontend has not been identified
from the available access. Do not edit minified production bundles as a
substitute for a reviewed source change.
