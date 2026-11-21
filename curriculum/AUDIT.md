# Coverage audit

The baseline has 18 Basics, 20 Intermediate and 20 Advanced lessons. All have short sections, executable examples, numbered fill-ins and quizzes. Named challenge cells share the terminal practice tests. They often supply the loop, branches or data structure that the learner should eventually choose.

| Area | Baseline finding | Editorial action |
|---|---|---|
| Basics 06 and 10 | Good tracing and arithmetic practice. The final functions still show most implementation decisions. | Pilot a defect, an independent order-processing ticket and executable acceptance examples. |
| Remaining lessons with named checks | A separate grader already evaluates behavior. Recreating these tasks would duplicate work. | Promote one suitable contract per lesson to an independent implementation with the existing check. |
| Basics 00, 15–17; Intermediate 00, 14, 18–19; Advanced 08, 10, 14, 19 | No named challenge check in the notebook. These cover orientation, investigation, testing and synthesis. | Assess a small artifact or investigation specific to the lesson. |
| Nine projects and three assessments | Projects mix running examples with extension requests. Assessments already have rubrics. | Label the handoff, specify evidence for the independent change, and use the existing rubric. |
| Retention | Projects revisit earlier material, but prerequisite and reuse relationships are implicit. | Map each lesson to an observable task and earlier concepts. |

The practice files are also achievement inputs. Saved independent builds now have a separate local mastery report. Keep keyed tests, hints, claim verification, environment bootstrap and the CI version matrix in place.
