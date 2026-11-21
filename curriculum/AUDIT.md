# Coverage audit

The baseline has 18 Basics, 20 Intermediate and 20 Advanced lessons. All have short sections, executable examples, numbered fill-ins and quizzes. Named challenge cells share the terminal practice tests. They often supply the loop, branches or data structure that the learner should eventually choose.

| Area | Baseline finding | Editorial action |
|---|---|---|
| Basics 06 and 10 | Good tracing and arithmetic practice. The final functions still show most implementation decisions. | Pilot a defect, an independent order-processing ticket and executable acceptance examples. |
| Remaining lessons with named checks | A separate grader already evaluates behavior. Recreating these tasks would duplicate work. | Promote one suitable contract per lesson to an independent implementation with the existing check. |
| Basics 00, 15–17; Intermediate 00, 14, 18–19; Advanced 08, 10, 14, 19 | No named challenge check in the notebook. These cover orientation, investigation, testing and synthesis. | Assess a small artifact or investigation specific to the lesson. |
| Nine projects and three assessments | Projects mix running examples with extension requests. Assessments already have rubrics. | Label the handoff, specify evidence for the independent change, and use the existing rubric. |
| Retention | Projects revisit earlier material, but prerequisite and reuse relationships are implicit. | Map each lesson to an observable task and earlier concepts. |

The practice files are also achievement inputs. Notebook-only work is formative. Keep keyed tests, hints, claim verification, environment bootstrap and the CI version matrix in place.

## Phase 2 implementation

All 58 lesson builds now map to named practice-module assessments via `mastery_module` in `concepts.json`. Fifteen previously notebook-only builds (7 Basics, 4 Intermediate, 4 Advanced) now receive separate behavioral grading, so a finished notebook alone does not constitute achievement evidence. Existing named challenges retain salted fingerprints and hints; new independent tests use no staged hints.

The `independently_reinforced` field records selected delayed, mixed-concept demonstrations, including Basics scanner/stock reports, Intermediate reconciliation, and Advanced idempotency/replay audits. The existing concept prerequisite/reuse map remains the source of truth. Lesson build descriptions now include spaced engineering revision tickets; future audits should inspect the rest of the guided questions for redundancy.

Build checks test observable results and missing implementations rather than merely printing acceptance examples. Real-kernel Colab exercises are still instructor- or learner-reviewed; CI uses clean isolated Python namespaces for notebook execution. Project rubric reviews remain human-assessed.
