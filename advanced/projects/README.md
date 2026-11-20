# Advanced Python Portfolio Projects

The three capstones demonstrate engineering design and error handling rather than just syntax.

| Project | Key skills | Notebook |
|---|---|---|
| Bounded Async Crawler Simulator | TaskGroup, Semaphore, structured task lifecycle, deduplication, simulated failures | [Open](01_async_crawler_simulator.ipynb) |
| Streaming Text Analytics | Generators, Unicode tokenization, Counters, timeit, tracemalloc, property-style tests | [Open](02_streaming_text_analytics.ipynb) |
| Transactional Event Processor | SQLite, unique idempotency keys, atomic updates, safe status reporting, unittest | [Open](03_transactional_event_processor.ipynb) |

The [event_processor_package](event_processor_package/README.md) contains a separate installable CLI with source modules, pyproject.toml, and tests.

For a strong portfolio submission, provide a README with setup instructions, contracts, architecture diagram, testing evidence, failure policies, benchmark limitations and at least one design alternative.

Examples use fake networks or in-memory data. Real external services introduce authentication, terms of service, data privacy and operational limits that are outside this educational course.
