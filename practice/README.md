# Auto-graded practice ✅

Reading code isn't enough. You learn by writing it and getting **fast, specific feedback**. This folder has one auto-graded module for each exercise workbook in the course: 12 modules, 240 tests.

| Level | Module (edit this file) | Matching workbook |
|---|---|---|
| Basics | [`basics_01_fundamentals.py`](exercises/basics_01_fundamentals.py) | [Fundamentals](../basics/exercises/01_fundamentals_exercises.ipynb) |
| Basics | [`basics_02_control_flow.py`](exercises/basics_02_control_flow.py) | [Control flow](../basics/exercises/02_control_flow_exercises.ipynb) |
| Basics | [`basics_03_data_structures.py`](exercises/basics_03_data_structures.py) | [Data structures](../basics/exercises/03_data_structures_exercises.ipynb) |
| Basics | [`basics_04_functions_and_files.py`](exercises/basics_04_functions_and_files.py) | [Functions and files](../basics/exercises/04_functions_and_files_exercises.ipynb) |
| Intermediate | [`intermediate_01_oop_and_collections.py`](exercises/intermediate_01_oop_and_collections.py) | [OOP and collections](../intermediate/exercises/01_oop_and_collections_exercises.ipynb) |
| Intermediate | [`intermediate_02_iteration_and_abstractions.py`](exercises/intermediate_02_iteration_and_abstractions.py) | [Iteration and abstractions](../intermediate/exercises/02_iteration_and_abstractions_exercises.ipynb) |
| Intermediate | [`intermediate_03_data_quality_and_testing.py`](exercises/intermediate_03_data_quality_and_testing.py) | [Data quality and testing](../intermediate/exercises/03_data_quality_and_testing_exercises.ipynb) |
| Intermediate | [`intermediate_04_sql_http_cli.py`](exercises/intermediate_04_sql_http_cli.py) | [SQL, HTTP and CLI](../intermediate/exercises/04_sql_http_cli_performance_exercises.ipynb) |
| Advanced | [`advanced_01_internals_typing_architecture.py`](exercises/advanced_01_internals_typing_architecture.py) | [Internals, typing and architecture](../advanced/exercises/01_internals_typing_architecture_exercises.ipynb) |
| Advanced | [`advanced_02_concurrency_resilience.py`](exercises/advanced_02_concurrency_resilience.py) | [Concurrency and resilience](../advanced/exercises/02_concurrency_resilience_exercises.ipynb) |
| Advanced | [`advanced_03_security_testing_performance.py`](exercises/advanced_03_security_testing_performance.py) | [Security, testing and performance](../advanced/exercises/03_security_testing_performance_exercises.ipynb) |
| Advanced | [`advanced_04_production_systems.py`](exercises/advanced_04_production_systems.py) | [Production systems](../advanced/exercises/04_production_systems_exercises.ipynb) |

## Setup (once)

```bash
python -m pip install -r requirements-dev.txt
```

## The learning loop

1. **Read** the lesson notebooks, then open a module in `practice/exercises/`. Each function has a docstring that says what to build, often with an example and a hint.
2. **Predict** what the function should return for a normal input and for an edge case (empty list, zero, negative number, duplicate).
3. **Write** your code in place of `raise NotImplementedError(...)`.
4. **Check** from the repository root:

   ```bash
   python -m pytest practice -k basics_01
   ```

   Run a single test with `-k test_split_minutes`. Add `-x` to stop at the first failure.
5. **Read the failure.** For example, `assert 4 == 5` means your function returned `4` but `5` was expected. The test file in `practice/tests/` shows the exact inputs. Many tests also explain *why*, e.g. "the original list must not change".
6. **Repeat** until the progress table says `complete!`. Then compare your code with `practice/solutions/`. There's more than one good answer, so look for ideas, not for a copy.

Functions you haven't started show as **TO DO** (skipped) instead of failures. Your progress table stays readable:

```
basics_02_control_flow                     [##------------------]  4/49 1 failing, 44 to do
```

## Tips for learning well

- **Do not open the solution first.** Struggling for 10–20 minutes is when the learning happens.
- **Read the tests.** They are short, real-world pytest examples: `parametrize`, `raises`, `tmp_path`, `capsys`, `caplog` and fixtures. Intermediate lesson 14 explains testing.
- **Write your own extra test** for an edge case you thought of. Add it to the test file and run it.
- **Start over any time:** delete a module in `exercises/` and run `python tools/make_practice_stubs.py` to get a fresh copy. Files you have already edited are never overwritten unless you pass `--force`.

## For contributors

`practice/solutions/` is the source of truth. After changing a solution, regenerate the stubs and check that the tests pass against the solutions:

```bash
python tools/make_practice_stubs.py
python -m pytest practice --solutions
```
