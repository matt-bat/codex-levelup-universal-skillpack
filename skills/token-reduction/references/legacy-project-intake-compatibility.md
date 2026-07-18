# Legacy Project Intake Compatibility

Earlier versions of `token-reduction` also handled new-project questions, `docs/project-index.md`, test/build ownership preferences, and local-versus-deployment policy. Those responsibilities are intentionally outside this skill now.

## Compatibility Rules

1. Do not ask a new-project test/build question merely because `token-reduction` activated.
2. Do not create or update `docs/project-index.md` merely because this skill activated.
3. Do not treat this skill as authorization to run, skip, deploy, publish, or release anything.
4. Follow explicit user instructions, repository policy, and higher-priority execution rules for those decisions.
5. If an existing repository policy explicitly requires the legacy workflow, follow that policy as its own authority and report the compatibility dependency; do not attribute the write or gate to `token-reduction`.
6. Treat an existing project index as ordinary task context only when the current task needs it.

This reference preserves interpretability for older installations without retaining legacy activation side effects.
