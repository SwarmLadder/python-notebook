# Auto-graded practice ✅

There are 12 modules, one per exercise workbook, with 428 tests. You write the code and the tests tell you whether it's correct. **The answers are never shown.** The repo stores only fingerprints (hashes) of the correct results.

## Start

```bash
python -m pip install -r requirements-dev.txt
python -m pytest practice -k basics_01
```

No install? Open the repo in **GitHub Codespaces** (see the main README). Everything is preinstalled there.

## The loop

1. Open a module in [`exercises/`](exercises). Each function's docstring says what to build, often with an example and a hint.
2. Replace `raise NotImplementedError(...)` with your code.
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

Functions you haven't started count as **to do**, not failures.

**Hints unlock step by step.** The first time a test fails you see hint 1, a nudge. If it fails again you see hint 2, which describes the method. You never see the answer. Your progress is saved locally in `practice/.progress.json`.

**Infinite loop?** Each test is stopped after 10 seconds with an explanation instead of running forever. If Python is stuck inside a built-in like `sum()`, pytest stops after 30 seconds and prints `Timeout` with the exact line of your code.

Tips:
- Equivalent answers count: a list or a tuple, `5` or `5.0`, and float rounding differences beyond 6 decimals.
- Read the test file in [`tests/`](tests). It shows every input and every rule, e.g. "the original list must not change".
- To start a module over: `git checkout -- practice/exercises/<module>.py`.

| Level | Modules |
|---|---|
| Basics | [fundamentals](exercises/basics_01_fundamentals.py) · [control flow](exercises/basics_02_control_flow.py) · [data structures](exercises/basics_03_data_structures.py) · [functions & files](exercises/basics_04_functions_and_files.py) |
| Intermediate | [OOP & collections](exercises/intermediate_01_oop_and_collections.py) · [iteration](exercises/intermediate_02_iteration_and_abstractions.py) · [data quality](exercises/intermediate_03_data_quality_and_testing.py) · [SQL, HTTP, CLI](exercises/intermediate_04_sql_http_cli.py) |
| Advanced | [internals & typing](exercises/advanced_01_internals_typing_architecture.py) · [concurrency](exercises/advanced_02_concurrency_resilience.py) · [security & performance](exercises/advanced_03_security_testing_performance.py) · [production](exercises/advanced_04_production_systems.py) |

## For maintainers

Reference solutions are kept **outside this repository**, in a private `practice_solutions/` folder. After changing a test or a solution, rebuild the answer keys and the stubs:

```bash
python -m pytest practice --record-answers=PATH/TO/practice_solutions
python tools/make_practice_stubs.py --solutions PATH/TO/practice_solutions
```

`--record-answers` writes `answers/*.json` only if every test passes, and never from a run filtered with `-k`. `tests/test_practice_stubs.py` fails if a stub contains an implementation or a test has no answer key.

A determined learner could brute-force a hash with very few possible answers, such as `True` or `False`. The point is that nobody sees an answer by accident. It is not exam security.
