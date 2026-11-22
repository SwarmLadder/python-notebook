# Phase 4 curriculum review

The Python repository now supplies the dependencies for a selected exercise, grades independent builds from their saved cells, and gives students larger implementation and debugging assignments as they advance. On November 22, 2026, the public SQLite lesson still served the earlier starter. Running its schema challenge first raised a missing-name error even though the page said “Setup ready.”

The [lesson and dependency register](PHASE4_REGISTER.md) indexes all 58 notebooks by file and cell ID. It records teaching sections, demonstrations, first practice, independent builds, mapped later assessments and missing dependencies in the starting revision. The [implementation diff](https://github.com/SwarmLadder/python-notebook/pull/14/files) includes the nine projects.

## Sequencing and assessment changes

| Location | Earlier experience | Revised experience |
|---|---|---|
| Basics 01–06, especially Strings `ex-3`, `ex-13` and `ch-7` | Students encountered dictionaries or comprehension syntax while practicing types, comparisons or strings. | Named predictions, supplied function calls and explicitly supplied loops let the student work on the current concept. The terminal palindrome starter uses the same scaffold as the notebook. |
| Basics 07, `teach-3`, `demo-3`, `ex-7` | The introduction briefly showed list comprehensions, including nested syntax later in the lesson. | The lesson translates an explicit loop into a comprehension, explains the order of evaluation, and guides filtering. Nested traversal uses loops. Intermediate 01 develops nested comprehensions, generators and readability. |
| Basics 07, `ex-9` and `ch-3` | The hint or starter selected `sorted(set(values))` before Sets. | The task can be solved with a list and membership checks. The matching practice hint and generator preserve that sequence. |
| Basics 08 and 09 | Collection-comprehension exercises depended on syntax the learner could imitate without understanding. | Sets introduces brace syntax after membership. Dictionaries explains key/value construction and replacement. Learners build both pass/fail groups and implement grouping functions from a contract. |
| Intermediate 06, `ex-4` and `ex-8` | Loops, filtering and pipeline stages were largely supplied. | Learners implement generators on one-pass input. A guarded source detects an implementation that reads beyond its first result. |
| Intermediate 15, `ex-6`, `ex-9` and `ch-6` | The exercise supplied the query, loop or balances update and asked for a small replacement. | Learners implement database reads against fresh fixtures, then own the atomic transfer. Tests check order, duplicates, missing rows and rollback. |
| Advanced 05, `teach-2` and `ex-5` | A learner could complete a supplied concurrent call with its input sequence. | The learner starts the workers. An event ensures a sequential solution cannot finish successfully. The lesson explains task-group lifetime and failure before the independent build requires it. |
| Advanced 18, `ex-2`, `ex-6`, `ch-1` and the migration build | Students completed largely supplied JSON, settings and persistence logic. | Students distinguish a stored null from malformed data, validate a configuration mapping, implement a durable receipt store and recover a failed migration. |

## What students own

| Level | Numbered implementation or debugging tasks redesigned | Named challenge bodies redesigned | Engineering submissions for review | Independent builds |
|---|---:|---:|---:|---:|
| Basics | 1 | 7 | 0 | 18 |
| Intermediate | 13 | 17 | 18 | 20 |
| Advanced | 13 | 12 | 20 | 20 |

These counts describe particular changes, not mastery or total student effort. For example, the early initials build supplies a loop. A later generator supplies only the public signature. A debugging ticket requires a regression that accepts the repaired behavior and rejects the original defect. Engineering submissions ask learners to select interfaces, connect components and supply tests. They require human review. Many short numbered exercises remain available for targeted practice.

Every existing claim of assessed reuse now names its behavioral check in [the concept map](concepts.json). Intermediate 09, for instance, requires a report to combine nonadjacent adjustments and preserve its input. Advanced 19 requires a one-pass replay audit to retain the first amount through conflicting deliveries. These are later opportunities to demonstrate skills. Long-term retention requires observations across learners and sessions.

## Project review

| Level | Project | Acceptance evidence students produce |
|---|---|---|
| Basics | Calculator | A rejected operation preserves the history of a previous successful call. |
| Basics | Number guessing | Only valid attempts consume the limit. An early win stops input consumption. |
| Basics | Student grades | Tied leaders, empty grade lists and valid zero grades are handled without changing the gradebook. |
| Intermediate | Library lending | Multiple reservations, duplicate requests and successive returns preserve queue ownership. |
| Intermediate | Offline ETL | A repeated page token is rejected before a second fetch. An empty final page terminates normally. |
| Intermediate | Task manager CLI | A subprocess reads open and completed counts from a temporary database without changing it. |
| Advanced | Async crawler | An instrumented provider exposes repeated requests for a shared child. Depth, parent choice and concurrency have explicit acceptance criteria. |
| Advanced | Streaming analytics | Results match the baseline at ties. Peak selection memory is measured separately from the frequency table. |
| Advanced | Transactional event processor | A deliberately inconsistent aggregate is reported on a consistent read without exposing event IDs or altering stored data. |

## Validation

- During the Phase 4 assessment run, two private correct submissions passed each of the 58 independent builds. One plausible faulty submission per build was rejected. Initially, an elapsed-time implementation wrapping hours at midnight passed. A new 100-hour case caught it. Private submissions were excluded from the repository.
- The 27 redesigned numbered component and debugging tasks accepted working submissions. A fresh-namespace sweep exercised 765 starter cells with their declared setup. Expected unfinished-work outcomes counted separately from execution errors.
- Python 3.12.14 on the follow-up branch ran `python -m pytest -q --ignore=tests/test_real_jupyter_kernel.py` with 1,339 passed and 428 skipped before this report was added. The practice harness marks unfinished submissions as skipped. The local sandbox denied the sockets required by the four external Jupyter kernel cases. Two fresh in-process kernel sessions independently reproduced the pending, correct and incorrect outcomes for SQLite Exercise 6.
- The repository workflow runs `python -m pytest` with external Jupyter kernels, then the notebook validator and both legacy smoke tests. The Python 3.11 and 3.13 matrix passed on the merged implementation. The follow-up pull request carries the results for its exact revision. [Implementation CI](https://github.com/SwarmLadder/python-notebook/actions/runs/44957311422)
- The standalone-module regression imports an implementation into a second Python file and runs it in a fresh subprocess. Hosted Colab execution was not verified.

## Public site acceptance

On the [live SQLite lesson](https://swarmladder.bitpyrus.workers.dev/lesson/intermediate/notebooks/15_sqlite_and_transactions), running `create_schema` first raised `NameError: name 'sqlite3' is not defined`. Exercise 1 accepted the correct method name, rejected a saved edit to `"wrong"`, and continued to display “1 of 22 checks passed” after reopening. The recheck reproduced both findings after the Python changes merged. Exercise 6 still showed the earlier comprehension blank.

The [Lab source](https://github.com/SwarmLadder/SwarmLadderlab) is separate. At inspected revision `53c276f`, `build/build_site.py` exports code cell IDs, kind and source but omits prerequisite metadata. `src/features/notebook/Notebook.tsx` queues lesson setup and reads saved editor text. The progress store adds pass keys without invalidating them when source changes. The platform needs a refreshed course bundle, preservation and resolution of declared prerequisites, and invalidation of current credit after an edit or failure. Recheck in a fresh browser with the schema cell first, then run correct → wrong → reload. No website deployment was performed.

The register covers formal sections and the mapped build assessments. Behavioral checks can establish correct outcomes using multiple implementations. They cannot prove a student selected a particular syntax independently, or that a named technique was retained months later.
