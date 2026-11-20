# Advanced Python — Final Assessment (100 points)

Complete the 20 guided notebooks, 80 independent challenges, and the three portfolio projects.

## Required submissions

1. **Async crawler simulator:** bounded concurrency, max-page/depth limits, deduplication, errors and cancellation-safe cleanup.
2. **Streaming text analytics:** validated tokenization, lazy stream processing, deterministic top-k output, timed benchmark and memory notes.
3. **Transactional event processor:** idempotency key enforcement in SQLite, atomic update, conflict detection, safe metrics, and test suite.
4. **Architecture decision record (ADR):** compare at least two alternatives for worker model, storage, observability, and reliability trade-offs.

## Rubric

| Category | Points | Evidence |
|---|---:|---|
| Correctness | 25 | Meets all requirements, clear invariants and behavior |
| Reliability and concurrency | 20 | Bounded work, ownership, cancellation, timeout and retry policy |
| Security and validation | 15 | Correct trust boundaries, no secrets, validated input, safe queries |
| Architecture | 15 | Focused interfaces, dependency injection, clear storage boundaries |
| Automated tests | 15 | Unit/integration, invalid, duplicate, and resource-cleanup cases |
| Measurements and documentation | 10 | Benchmarks justified, README and reproducible setup |

**Suggested readiness target:** 80/100 or more, with no unresolved critical security, data-integrity or cancellation failures.

## Required reasoning questions

- Why is __hash__ required to agree with equality?
- When does TaskGroup cancel siblings, and what cleanup is guaranteed?
- When are threads preferable to processes or asyncio?
- What is the difference between a semaphore and a per-second rate limiter?
- Why must idempotency keys be stored atomically with side effects?
- Why can an apparently faster algorithm be slower for tiny inputs?
- What is the distinction between a unit test, integration test, and property-style test?
- How do you keep logs useful without recording credentials or sensitive payloads?
- What is the difference between an SLI and SLO?

## Running tests

```bash
python tools/validate_notebooks.py
python tools/smoke_test_advanced.py
PYTHONPATH=advanced/projects/event_processor_package/src python -m unittest discover -s advanced/projects/event_processor_package/tests -v
```

Passing tests shows the checked examples work on the tested Python environment; it is not a guarantee of correctness in every production deployment.
