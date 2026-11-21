# Level 2 — Intermediate Python: Complete Practical Course

Develop software-building skills after mastering the [Python Basics course](../basics/README.md). Intermediate Python focuses on **maintainability, correctness, testability, data modeling, persistence, and reusable components** rather than memorizing more syntax.

## At a glance

| Resource | Count | Purpose |
|---|---:|---|
| Lessons | **20 notebooks** | Short rules, a demo, then graded exercises from easy to hard |
| Fill-in exercises | **185** | Each one checked as soon as you run it |
| Challenges | **73** | Functions and classes in the lessons, graded by the practice tests |
| Auto-graded practice | **4 modules, 102 tests** | Instant feedback; answers stay hidden |
| Portfolio projects | **3 notebooks** | OOP library, offline HTTP/ETL, SQLite task manager |
| Additional working application | **1 installable Python package** | CLI with SQLite, packaging metadata, and unit tests |

All runnable notebook examples use Python 3.10+ and only the **standard library**. External packages are required only to provide the Jupyter environment itself. Examples involving HTTP use fake or injected transports; no live API or secret is necessary.

## Prerequisites

Before starting, you should be comfortable with conditions, loops, list/dict/set/tuple operations, functions, exceptions, basic file handling, CSV, and debugging. Ideally complete the three [Basics projects](../basics/README.md#projects).

## Course syllabus — 20 detailed lessons

| Lesson | Topic |
|---:|---|
| 01 | [Workflow, environments, and clean code](notebooks/00_workflow_and_environments.ipynb) |
| 02 | [Comprehensions and transformations](notebooks/01_comprehensions_and_transformations.ipynb) |
| 03 | [Classes and objects](notebooks/02_classes_and_objects.ipynb) |
| 04 | [Inheritance, polymorphism, composition](notebooks/03_inheritance_and_composition.ipynb) |
| 05 | [Dataclasses and properties](notebooks/04_dataclasses_and_properties.ipynb) |
| 06 | [Iterables and iterators](notebooks/05_iterables_and_iterators.ipynb) |
| 07 | [Generators and lazy pipelines](notebooks/06_generators_and_lazy_pipelines.ipynb) |
| 08 | [Closures and decorators](notebooks/07_closures_and_decorators.ipynb) |
| 09 | [Context managers and resources](notebooks/08_context_managers_and_resources.ipynb) |
| 10 | [Functional tools and itertools](notebooks/09_functional_tools_and_itertools.ipynb) |
| 11 | [Type hints and protocols](notebooks/10_type_hints_and_protocols.ipynb) |
| 12 | [Logging, configuration, and errors](notebooks/11_logging_configuration_and_errors.ipynb) |
| 13 | [Regular expressions](notebooks/12_regular_expressions.ipynb) |
| 14 | [JSON, CSV, and data pipelines](notebooks/13_json_csv_and_data_pipelines.ipynb) |
| 15 | [Unit testing and mocking](notebooks/14_unittest_and_mocking.ipynb) |
| 16 | [SQLite, SQL, and transactions](notebooks/15_sqlite_and_transactions.ipynb) |
| 17 | [HTTP APIs and clients](notebooks/16_http_apis_and_clients.ipynb) |
| 18 | [CLI and packaging](notebooks/17_cli_and_packaging.ipynb) |
| 19 | [Complexity and profiling](notebooks/18_complexity_profiling_and_optimization.ipynb) |
| 20 | [Final review and capstone preparation](notebooks/19_intermediate_review_and_capstone.ipynb) |

## Learning blocks

| Module | Lessons | What you will be able to do |
|---|---|---|
| Project foundations | 00–01 | Maintain clean environments, design functions, transform data idiomatically |
| Object-oriented design | 02–04 | Model entities, preserve invariants, choose composition or inheritance |
| Lazy iteration and abstraction | 05–09 | Design iterators/generators, reusable wrappers, safe resource managers |
| Data contracts and engineering | 10–14 | Annotate types, parse text/JSON/CSV, log safely, write automated tests |
| Real applications | 15–18 | Use SQL transactions, build testable HTTP clients, package a CLI, profile code |
| Integration and assessment | 19 | Combine the concepts and identify readiness gaps |

## Challenges

The challenges live inside the lessons that teach their topic (lessons 01–17). Each one is a
function or class you finish, and `check('name')` grades it with the tests in
[`practice/`](../practice/README.md), the same tests used to verify an achievement claim.
Prefer a terminal? Solve them in `practice/exercises/intermediate_*.py` and run
`python -m pytest practice -k intermediate`.

## Portfolio projects

1. [OOP Library Lending System](projects/01_library_lending_system.ipynb) — models, borrowing rules, tests, JSON persistence.
2. [Offline HTTP API and ETL](projects/02_offline_api_etl_pipeline.ipynb) — transport injection, pagination, validation, data transformations, CSV reports.
3. [SQLite Task Manager and CLI](projects/03_sqlite_task_manager_cli.ipynb) — SQL CRUD, transactions, command parsing, tests.
   - [Installable task-manager package](projects/task_manager_package/README.md) — a real src-layout application with pyproject.toml, modules, and unittest tests.

The [projects index](projects/README.md) explains deliverables and suggested portfolio enhancements.

## Suggested learning schedule — 8 weeks

| Week | Lessons | Practical deliverable |
|---|---|---|
| 1 | 00–02 | Clean function and class design |
| 2 | 03–04 | Dataclass and service model; build library project |
| 3 | 05–07 | Iterator/generator pipelines and decorators |
| 4 | 08–09 | Resource safety, sorting, functional utilities |
| 5 | 10–12 | Type contracts, logging, regex |
| 6 | 13–15 | Data processing, unittest, SQLite |
| 7 | 16–18 | Offline API project, CLI task manager |
| 8 | 19 | Finish projects, review, and final assessment |

The schedule is a guideline, not a requirement. For detailed milestones see [Curriculum](CURRICULUM.md).

## How to run

From the **repository root**:

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
jupyter lab
```

Open `intermediate/notebooks/00_workflow_and_environments.ipynb`. The root README has setup information. Source notebooks are readable on GitHub, but Jupyter or a compatible Python kernel is needed to run cells.

To check your practice work: `python -m pytest practice -k intermediate`.

## Completion checklist

- [ ] Complete the 20 lessons and their exercises.
- [ ] Pass every challenge (`python tools/verify_level.py intermediate`).
- [ ] Explain and extend all three portfolio projects.
- [ ] Write tests covering valid, invalid, empty, and boundary inputs.
- [ ] Run all notebooks with a fresh kernel and resolve hidden-state dependencies.
- [ ] Complete the [final assessment](ASSESSMENT.md) and explain your design decisions.

After finishing, continue with [Advanced](../advanced/README.md).

## Worked examples and quizzes

- [Worked examples](worked_examples/01_worked_examples.ipynb): six problems solved step by step (plan → code → why → common mistake → your turn).
- Every lesson ends with a **Quick quiz** of three questions. Answers are hidden but checked when you run the cell.
