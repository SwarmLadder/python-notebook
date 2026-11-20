# Advanced Python Glossary

| Term | Meaning |
|---|---|
| Backpressure | Reducing or stopping intake when downstream processing cannot keep up. |
| Cancellation | Requesting that a coroutine stop, typically observed at an await point. |
| Context manager | Protocol for setup/cleanup through with or async with. |
| Correlation ID | Identifier connecting log and trace events from one request or operation. |
| Coroutine | Awaitable execution state produced by calling an async def function. |
| Descriptor | Object controlling attribute lookup and optional assignment through special methods. |
| Error budget | Allowed unreliability under a stated service-level objective. |
| Event loop | Scheduler coordinating asynchronous I/O-oriented tasks. |
| Generic type | Type declaration expressing relationships among input and output types. |
| GIL | Interpreter-level lock in common CPython builds affecting bytecode parallelism. |
| Idempotency | Repeating the same logical operation does not multiply its intended effects. |
| Invariance | Generic type relation that does not automatically permit subtype substitution. |
| Latency percentile | A threshold under which a specified proportion of observed durations falls. |
| Memory leak | Retained resources or memory that are no longer needed. |
| Metaclass | Class whose instances are class objects. |
| Port | Interface expressing operations needed by domain or application logic. |
| Adapter | Concrete implementation of a port for storage, network or user interface. |
| Protocol | Structural contract describing required attributes/methods in typing. |
| Rate limiting | Controlling operations over time, not merely simultaneous work. |
| Retry policy | Defined conditions, attempts and delays for repeating failed operations. |
| Semaphore | Concurrency primitive bounding simultaneous access to a resource. |
| SLI | Service-level indicator, an observed reliability measure. |
| SLO | Service-level objective, target for an SLI in a defined window. |
| Structured concurrency | Model that binds child task lifetime to a structured parent scope. |
| Transaction | Database unit committed fully or rolled back together. |
| Tracemalloc | Python facility tracing memory allocations, not full process RSS. |
| Weak reference | Reference that does not keep its target object alive. |
