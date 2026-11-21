# Auto-graded practice ✅

There are 15 practice modules: four guided modules and one independent-build module per level. Guided exercises use `___` blanks and salted answer fingerprints; independent builds start unimplemented and are assessed by observable behavior (including boundaries, invalid input, mutation and regression cases). No private reference implementations are published.

Most learners solve these as the **challenges in the lessons**, where a `check("name")` cell after each one runs these same tests. This folder is the terminal version, and it is what an [achievement claim](../RECOGNITION.md) is verified against.

## Start

```bash
python -m pip install -r requirements-dev.txt
python -m pytest practice -k basics_01
```

No install? Open the repo in **GitHub Codespaces** (see the main README). Everything is preinstalled there.

## The loop

1. Open a module in [`exercises/`](exercises). Each task's docstring says what to build. Guided tasks supply examples and progressive hints; independent builds give the contract without an algorithm.
2. For guided work, fill the `___` blanks. For independent builds, implement the named function (or the two introductory variables) and copy it to the corresponding `*_independent_builds.py` file.
3. Run `python -m pytest practice -k <module or function name>`.
4. Read the result:

   ```
   Not correct yet: check(m.split_minutes(minutes))
     your result: (2, 16)
     test inputs: minutes=135
   ```

   Work out the right answer for that input by hand, then fix your code.
5. Repeat until the table says `complete!`:

   ```
   basics_02_control_flow   [####----------------]  18/86  2 failing, 66 to do
   ```

Functions whose blanks you haven't filled yet count as **to do**, not failures.

**Guided hints unlock step by step.** The first time a test fails you see hint 1, a nudge. If it fails again you see hint 2, which describes the method. You never see the answer. Independent tests do not unlock hints or count repeated failed attempts as mastery. Your guided progress is saved locally in `practice/.progress.json`.

**Infinite loop?** Each test is stopped after 10 seconds with an explanation instead of running forever. If Python is stuck inside a built-in like `sum()`, pytest stops after 30 seconds and prints `Timeout` with the exact line of your code.

Tips:
- Equivalent answers count: a list or a tuple, `5` or `5.0`, and float rounding differences beyond 6 decimals.
- Read the test file in [`tests/`](tests). It shows every input and every rule, e.g. "the original list must not change".
- To start a module over: `git checkout -- practice/exercises/<module>.py`.

| Level | Modules |
|---|---|
| Basics | [fundamentals](exercises/basics_01_fundamentals.py) · [control flow](exercises/basics_02_control_flow.py) · [data structures](exercises/basics_03_data_structures.py) · [functions & files](exercises/basics_04_functions_and_files.py) · [independent builds](exercises/basics_independent_builds.py) |
| Intermediate | [OOP & collections](exercises/intermediate_01_oop_and_collections.py) · [iteration](exercises/intermediate_02_iteration_and_abstractions.py) · [data quality](exercises/intermediate_03_data_quality_and_testing.py) · [SQL, HTTP, CLI](exercises/intermediate_04_sql_http_cli.py) · [independent builds](exercises/intermediate_independent_builds.py) |
| Advanced | [internals & typing](exercises/advanced_01_internals_typing_architecture.py) · [concurrency](exercises/advanced_02_concurrency_resilience.py) · [security & performance](exercises/advanced_03_security_testing_performance.py) · [production](exercises/advanced_04_production_systems.py) · [independent builds](exercises/advanced_independent_builds.py) |

## For maintainers

Reference solutions are kept **outside this repository**, in a private `practice_solutions/` folder. After changing a test or a solution, rebuild the answer keys and the stubs:

```bash
python -m pytest practice --record-answers=PATH/TO/practice_solutions
python tools/make_practice_stubs.py --solutions PATH/TO/practice_solutions --force
python tools/make_workbooks.py
```

`make_practice_stubs.py` turns each solution into a fill-in exercise by blanking its key expressions (conditions, loop ranges, returned values). `make_workbooks.py` rebuilds the workbook notebooks from those files.

`--record-answers` writes `answers/*.json` only if every test passes, and never from a run filtered with `-k`. `tests/test_practice_stubs.py` fails if an exercise function has no blank, a workbook is out of date, or a test has no answer key.

A determined learner could brute-force a hash with very few possible answers, such as `True` or `False`. The point is that nobody sees an answer by accident. It is not exam security.

Independent builds intentionally have no keyed answer files or progressive hint files. Their publicly inspectable tests specify inputs and observable acceptance criteria but do not include private reference solutions. The existing guided exercise answer keys and hint progression are unchanged.
