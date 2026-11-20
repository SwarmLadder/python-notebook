# Intermediate Python — Instructor-Style Curriculum

## Course purpose

This is a transition from writing isolated Python snippets to building reliable, reusable, testable software. Every module should produce evidence: a small well-structured function, a test, a refactoring decision, or a project extension.

## Detailed competency map

| Lessons | Conceptual focus | Practice evidence |
|---|---|---|
| 00–01 | Environments, pure functions, contracts, comprehensions, lazy expressions | A function with typed inputs, tests, and a clear return policy |
| 02–04 | Instance state, methods, inheritance, composition, dataclasses, property validation | A validated model with no shared mutable defaults |
| 05–06 | Iteration protocol, StopIteration, single-pass streams, yield from | A reusable iterable and a lazy data pipeline |
| 07–09 | Closures, nonlocal, wraps, context managers, functools, itertools | A decorator preserving metadata and a context manager cleaning on errors |
| 10–12 | Type annotations, TypedDict, Protocols, logging, regex | A validated parsing boundary with safe log messages |
| 13–14 | JSON/CSV ETL, unit tests, fixtures, mocks | An importer that reports invalid rows and is tested offline |
| 15–16 | SQLite schema, transactions, HTTP methods, pagination, timeout, fake transport | Parameterized queries and a bounded simulated API client |
| 17–18 | argparse, packaging, pyproject, complexity, timeit, cProfile | A callable CLI main function and evidence-backed performance discussion |
| 19 | Integration, assessment, defensive validation | A tested domain-to-storage pipeline |

## Study rhythm for each notebook

1. Read the learning objectives and paraphrase them.
2. Predict every worked code example before running it.
3. Run and alter at least one input per example.
4. Complete all embedded exercises.
5. Record an edge case and a failure mode.
6. Restart the kernel and run all cells.
7. Return to the relevant practice pack and then the reference solution notebook.

## Major checkpoints

### After lesson 04 — Object design
Demonstrate two independent objects with no shared mutable state, an invariant enforced in a method or property, and a concrete argument for composition over inheritance. Complete the Library Lending System project.

### After lesson 09 — Iteration and abstraction
Demonstrate why a generator is single-use, write a bounded lazy pipeline, design a metadata-preserving decorator, and use a context manager whose cleanup executes after failure.

### After lesson 14 — Quality and correctness
Show type annotations plus runtime validation, a data transformation with a rejection report, and unit tests with a fake external dependency. Explain why JSON syntax checks are insufficient.

### After lesson 18 — Practical software
Build an SQLite-backed command-line application with explicit paths, SQL parameters, transaction boundaries, and a test suite. Explain a measured performance observation without making universal speed claims.

### After lesson 19 — Graduation
Review the three projects and identify five design decisions with trade-offs. Complete the final assessment; aim for 80/100 or higher before starting Advanced.

## Recommended software engineering habits

- Keep notebooks educational and self-contained. Move reusable code into .py modules as projects mature.
- Avoid hardcoded file paths, secret tokens, live network tests, and accidental global state.
- Use fixtures and in-memory or temporary storage for deterministic tests.
- Let static types explain contracts, but validate untrusted data at runtime.
- Keep logging operational, restrained, and free of credentials.
- Measure performance before optimizing.
