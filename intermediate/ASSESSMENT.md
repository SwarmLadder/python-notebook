# Intermediate Python — Final Assessment

The goal is to establish readiness for advanced Python topics by showing correctness, design reasoning, and reproducible tests.

## Required submissions

1. **An OOP domain model:** extend the Library Lending System with due dates, duplicate-book checks, and a clear state model.
2. **A data boundary:** adapt the offline API pipeline to accept malformed records, report rejections, and produce a CSV summary.
3. **A persistent CLI:** extend the SQLite Task Manager package with a new command and tests.
4. **A short design review:** explain why you chose composition or inheritance, what is validated, how external dependencies are isolated, and where transactions are required.

## Rubric (100 points)

| Criterion | Points | Evidence |
|---|---:|---|
| Correctness and completeness | 30 | All requested features behave as specified |
| Validation and error handling | 15 | Invalid, missing, and boundary inputs produce predictable outcomes |
| Code architecture | 20 | Focused functions, owned state, clear data model, testable dependencies |
| Automated testing | 20 | Unit tests plus realistic integration checks; no live network dependency |
| Documentation and reproducibility | 10 | README, setup instructions, clean notebook execution, path hygiene |
| Engineering reflection | 5 | Clear explanation of trade-offs and potential improvements |

**Suggested pass threshold:** 80/100. This is an educational target, not a formal certification.

## Minimum test cases

- A valid record is accepted and round-tripped through its storage boundary.
- An invalid record is rejected with an actionable error.
- Duplicate identifiers are handled according to an explicit policy.
- An empty dataset produces a deliberate result.
- A failed transaction leaves the database in a valid state.
- A mock dependency proves that tests do not call live network services.
- A CLI command works with injected arguments and returns a meaningful status.
- The project runs from a fresh environment after installing declared dependencies.

## Oral or written self-review prompts

- Explain a concrete case where a dictionary is better than a class, and vice versa.
- Explain why a generator saves memory but may be exhausted.
- Explain how a decorator changes call behavior and why wraps matters.
- Explain why type annotations do not validate JSON at runtime.
- Explain why a SQL query should use bound parameters.
- Explain why retrying a POST operation can cause duplicate actions.
- Explain what profiling can tell you that a Big-O explanation cannot.

Complete the [20-lesson course](README.md) and all three [portfolio projects](projects/README.md) before moving to [Advanced](../advanced/README.md).
