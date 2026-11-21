# Writing a SwarmLadder exercise

Start with the rule the learner needs, one executable example, and the boundary where intuition often fails. Ask for a prediction before showing the result. Use blanks to teach mechanics, then ask learners to repair a defect or solve a smaller problem before the independent build.

Write the build as a short contract. Name the interface, input domain, return value or side effect, and any ordering, failure or resource guarantee a caller relies on. Give one example that distinguishes plausible interpretations. Supply a signature when useful. Leave algorithm and data structures to the learner unless the lesson explicitly assesses one.

Use the smallest realistic ticket that calls for the skill. Check observable behavior offline with ordinary, boundary and applicable invalid inputs. Accept equivalent implementations. Guided hints should begin with a diagnostic question and reveal more only on request. Ask the learner to contribute a counterexample and explain one decision.

Record the assessed skill, prerequisites, reused concepts and evidence in the concept map. Revisit the skill later in a different context. Mark worked code clearly in projects and assess a separate change against the level rubric.

Preserve the existing practice contract and fingerprints. For new behavior add independent checks outside the keyed cases. Run the repository CI commands before submitting.

## Mastery and retention requirements

Every lesson must have `mastery_module` naming a tested `practice/exercises/<module>.py` submission; the matching `practice/tests/test_<module>.py` must refer to the build's public name. Set `independently_reinforced` to a *subset* of `reused_concepts` only when the independent acceptance contract exercises those earlier skills. Add a delayed revision ticket in a later lesson when it teaches transfer rather than a repeated calculation.

Guided checks retain salted fingerprints and progressive hints. Independent tests accept different correct algorithms, cover empty/edge/invalid cases where relevant, and deliberately include no staged hints. An unimplemented build must never count as mastery, even if some tests execute successfully. Before Lesson 10, provide the `def` and `return` bridge wherever an assessment requires a function; before Lesson 14, supply all imports in example/setup cells.
