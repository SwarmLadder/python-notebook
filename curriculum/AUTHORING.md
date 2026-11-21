# Writing a SwarmLadder exercise

Start with the rule the learner needs, one executable example, and the boundary where intuition often fails. Ask for a prediction before showing the result. Use blanks to teach mechanics, then ask learners to repair a defect or solve a smaller problem before the independent build.

Write the build as a short contract. Name the interface, input domain, return value or side effect, and any ordering, failure or resource guarantee a caller relies on. Give one example that distinguishes plausible interpretations. Supply a signature when useful. Leave algorithm and data structures to the learner unless the lesson explicitly assesses one.

Use the smallest realistic ticket that calls for the skill. Check observable behavior offline with ordinary, boundary and applicable invalid inputs. Accept equivalent implementations. Guided hints should begin with a diagnostic question and reveal more only on request. Ask the learner to contribute a counterexample and explain one decision.

Record the assessed skill, prerequisites, reused concepts and evidence in the concept map. Revisit the skill later in a different context. Mark worked code clearly in projects and assess a separate change against the level rubric.

Preserve the existing practice contract and fingerprints. For new behavior add independent checks outside the keyed cases. Run the repository CI commands before submitting.

## Standalone exercise contexts and code ownership

Every numbered exercise starts with `lesson-setup`. In Jupyter and Colab, run `colab-setup` first. A browser that mounts the course files can omit the download bootstrap. Put shared imports and type definitions in lesson setup, including names used only in annotations. For standalone scripts, copy the relevant imports and helper definitions into the module.

When an exercise integrates earlier learner work, name its cell IDs in `metadata.requires_cells`. List only direct prerequisites. `tools/exercise_context.py` resolves the transitive set and rejects a dependency that follows its consumer. Run the saved versions of these cells. A check cell includes its work cell and any other learner-owned fixtures needed by its tests. Mastery runs take this path automatically.

Use a small answer check for new mechanics. When students can already choose the control flow, give a behavioral contract, an unfinished implementation, and several observations on new inputs. A numbered component cell ends with `check(number, implementation, observe=observe)`. The observer returns the evidence to fingerprint. Include a failure path or changed input where the contract requires it. Debugging tickets also grade a learner-written regression against the original defect and the repair. Preserve the numbering and public interfaces used by achievements.

During review, record `metadata.practice_mode` on a redesigned task. Identify who owns the algorithm, state, interface, tests and failure policy. A supplied function signature delegates its body to the learner. A supplied loop still teaches guided mechanics. When adding an assessed reuse claim, record an executable check and describe its observation in `reuse_evidence` in the concept map.
