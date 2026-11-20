# Advanced Python — Detailed Curriculum

## What advanced proficiency means

The objective is to reason rigorously about behavior under scale, error, concurrency, and changing requirements, not simply to memorize complicated syntax.

### Module A: Python internals (lessons 00–04)

Learn special methods, descriptor precedence, identity and copy semantics, garbage collection, generics, and safe extensibility. Deliver a value object with documented equality/hash behavior, a validated descriptor, a type-safe dependency port, and a limited plugin registry.

### Module B: Concurrency and resilience (lessons 05–09)

Learn the cooperative scheduling model of asyncio, structured concurrency, cancellation propagation, thread synchronization, spawn-safe process pools, bounded retries, concurrency limits, and idempotency. Deliver a bounded TaskGroup pipeline and a cancellation/error policy. Understand why a semaphore is not a rate limiter.

### Module C: Correctness and systems (lessons 10–14)

Learn Big-O, profiling, tracemalloc, heap/bisect tools, bounded caches, domain boundaries, trust limits, structured input validation, property-style and integration testing. Deliver a measured performance comparison and a testable architecture with fake external adapters.

### Module D: Production engineering (lessons 15–19)

Learn SLI/SLO/error budgets, safe structured logging, API compatibility/versioning, durable idempotency, SQL transaction boundaries, packaging and CI. Deliver a transactionally consistent event pipeline, an installable command-line application, and a final architecture review.

## Weekly recommended checkpoints

| Week | Lessons | Measurable output |
|---|---|---|
| 1 | 00–02 | Data model and object lifetime comparison |
| 2 | 03–04 | Typed plugin and dependency-injection example |
| 3 | 05–06 | Bounded, cancellable async worker pipeline |
| 4 | 07–09 | Thread-safe queue, process demo, retry strategy |
| 5 | 10–11 | Profiling and algorithmic cost report |
| 6 | 12–13 | Ports/adapters design and security review |
| 7 | 14 | Property-style, unit and integration tests |
| 8 | 15–16 | Reliability dashboard design and API versioning |
| 9 | 17–18 | Transactional service and package/CI |
| 10 | 19 | 3 finished projects and [final assessment](ASSESSMENT.md) |

## Evidence standard

For every exercise or project, document expected inputs, invariants, outputs, exceptional behavior, resource lifetime, and at least one alternative design. For concurrency, make cancellation and task ownership explicit. For storage, demonstrate rollback and uniqueness. For performance, state the measurement environment and avoid universal speed claims.

The course is self-contained and uses offline examples so it can be checked with automated CI; production integrations should be added only after relevant security and operational review.
