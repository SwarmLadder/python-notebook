# Level 3 — Advanced Python: Complete Practical Course

Learn the engineering techniques required to build reliable and maintainable Python systems. This course builds on the [Basics](../basics/README.md) and [Intermediate](../intermediate/README.md) levels.

## At a glance

| Material | Count | Purpose |
|---|---:|---|
| Lessons | **20 notebooks** | Short rules, a demo, then graded exercises from easy to hard |
| Fill-in exercises | **162** | Each one checked as soon as you run it |
| Named practice checks | **57** | Lesson checks that run the shared practice suite |
| Independent builds | **20** | One per lesson, including builds with dedicated acceptance cases |
| Auto-graded practice | **4 modules, 95 tests** | Instant feedback; answers stay hidden |
| Advanced portfolio projects | **3** | Async crawler simulator, streaming text analytics, transactional event processor |
| Companion application | **1 installable package** | SQLite event processor CLI with unit tests |
| Standalone parallelism example | **1 Python script** | Portable ProcessPoolExecutor demonstration |

The notebooks use the **Python standard library**. **Python 3.11+** is required for TaskGroup and ExceptionGroup examples (CI tests Python 3.11 and 3.13). No API keys or live network services are required.

## Detailed lesson index

| Lesson | Topic |
|---:|---|
| 00 | [Python data model and special methods](notebooks/00_python_data_model.ipynb) |
| 01 | [Descriptors, properties, metaclass concepts](notebooks/01_descriptors_and_metaclasses.ipynb) |
| 02 | [Memory, references, copying, and weakrefs](notebooks/02_memory_references_weakrefs.ipynb) |
| 03 | [Generics, overloads, and Protocols](notebooks/03_advanced_typing.ipynb) |
| 04 | [Imports, introspection, and plugins](notebooks/04_imports_introspection_plugins.ipynb) |
| 05 | [asyncio event loops and coroutines](notebooks/05_asyncio_event_loop.ipynb) |
| 06 | [TaskGroup, cancellation, and timeouts](notebooks/06_taskgroups_cancellation_timeouts.ipynb) |
| 07 | [Threading, locks, and queues](notebooks/07_threading_locks_queues.ipynb) |
| 08 | [Process pools and parallelism](notebooks/08_multiprocessing_and_parallelism.ipynb) |
| 09 | [Retries, rate limiting, and idempotency](notebooks/09_retries_rate_limits_idempotency.ipynb) |
| 10 | [Profiling and memory measurement](notebooks/10_profiling_memory_benchmarks.ipynb) |
| 11 | [Algorithms, heaps, and caching](notebooks/11_algorithms_complexity_caching.ipynb) |
| 12 | [Ports, adapters, and dependency injection](notebooks/12_architecture_dependency_injection.ipynb) |
| 13 | [Security and untrusted input boundaries](notebooks/13_security_safe_parsing_secrets.ipynb) |
| 14 | [Property-style testing and integration tests](notebooks/14_testing_property_integration.ipynb) |
| 15 | [Observability, SLIs, and SLOs](notebooks/15_observability_and_slos.ipynb) |
| 16 | [API contracts and versioning](notebooks/16_api_design_versioning_contracts.ipynb) |
| 17 | [Transactions, integrity, and idempotency](notebooks/17_sqlite_transactions_integrity.ipynb) |
| 18 | [Packaging, CI, and deployment hygiene](notebooks/18_production_quality_ci_deployment.ipynb) |
| 19 | [Advanced review and capstone preparation](notebooks/19_advanced_review_capstone.ipynb) |

## Learning modules

| Module | Lessons | Core mastery |
|---|---|---|
| Python internals | 00–04 | Data model, class mechanics, object lifetime, generic contracts, trusted plugins |
| Concurrency and reliability | 05–09 | asyncio, TaskGroup, cancellation, threads, processes, bounded retries |
| Correctness and systems design | 10–14 | profiling, algorithms, injection, secure parsing, tests and integration |
| Production engineering | 15–19 | SLIs/SLOs, API evolution, transactional idempotency, CI and capstone |

## Challenges

The challenges live inside the lessons that teach their topic. Each one is a function or
class you finish, and `check('name')` grades it with the tests in
[`practice/`](../practice/README.md), the same tests used to verify an achievement claim.
Prefer a terminal? Solve them in `practice/exercises/advanced_*.py` and run
`python -m pytest practice -k advanced`.

## Advanced portfolio projects

1. [Bounded asynchronous crawler simulator](projects/01_async_crawler_simulator.ipynb) — TaskGroup, deduplication, bounded concurrency, failure reports, fake offline pages.
2. [Streaming text analytics and performance lab](projects/02_streaming_text_analytics.ipynb) — generators, normalized tokenization, Counter, timeit, tracemalloc, tests.
3. [Transactional event processor](projects/03_transactional_event_processor.ipynb) — SQLite uniqueness, idempotent processing, safe metrics, rollback tests.
   - [Installable event-processor CLI package](projects/event_processor_package/README.md) — pyproject.toml, src layout, tests.

For portable multiprocessing, run [the standalone process-pool demonstration](examples/process_pool_demo.py) from the terminal rather than from a notebook cell.

## Study schedule — 10 weeks

| Week | Course work | Deliverable |
|---|---|---|
| 1 | Lessons 00–02 | Value object, descriptor, memory case study |
| 2 | Lessons 03–04 | Type-safe plugin interface |
| 3 | Lessons 05–06 | Cancel-safe TaskGroup pipeline |
| 4 | Lessons 07–09 | Concurrency and retries |
| 5 | Lessons 10–11 | Profiling report and algorithm review |
| 6 | Lessons 12–13 | Architecture and security assessment |
| 7 | Lesson 14 | Testing strategy |
| 8 | Lessons 15–16 | SLO metrics and versioned API |
| 9 | Lessons 17–18 | Transactional application |
| 10 | Lesson 19 | Portfolio project completion and final assessment |

See [CURRICULUM.md](CURRICULUM.md) for module checkpoints and [ASSESSMENT.md](ASSESSMENT.md) for a 100-point rubric.

## Quick start

From the repository root:

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
jupyter lab
```

Open `advanced/notebooks/00_python_data_model.ipynb`.

To validate syntax and run deterministic examples:

```bash
python tools/validate_notebooks.py
python tools/smoke_test_advanced.py
```

To test the installable CLI's core directly without installation:

```bash
PYTHONPATH=advanced/projects/event_processor_package/src python -m unittest discover -s advanced/projects/event_processor_package/tests -v
```

## Graduation criteria

- [ ] All 20 notebooks can be explained and run from a fresh kernel.
- [ ] Review your independent-build report and explain one boundary test from each project.
- [ ] Completed and tested all three capstone projects.
- [ ] Can reason about cancellation, rate limits, rollback, and idempotency.
- [ ] Can justify benchmarks with measured evidence, not assumptions.
- [ ] Can demonstrate secure input validation and secret-free logging.
- [ ] Completed the [final assessment](ASSESSMENT.md).

**Note:** These lessons are educational simulations. They are not production-deployment advice for high-risk financial, medical, or security systems without specialist review.

## Worked examples and quizzes

- [Worked examples](worked_examples/01_worked_examples.ipynb): six problems solved step by step (plan → code → why → common mistake → your turn).
- Every lesson ends with a **Quick quiz** of three questions. Answers are hidden but checked when you run the cell.
