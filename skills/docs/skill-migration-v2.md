# Skill Migration Version 2

## Policy

Version 2 narrows activation and introduces typed routing without immediately deleting public skill names. Existing explicit commands and supported names continue through the observation window.

## Immediate Changes

1. Universal behavior moves into core policy instead of automatic skill selection.
2. `process-budget-controller` becomes a compatibility wrapper for router budget policy.
3. `internal-lang` remains available through explicit `/internal-lang` commands.
4. `hyperfocus-discovery` becomes an explicit bounded branch-management mode.
5. Plain review no longer activates weighted scoring.
6. Spatial Canvas activates only when explicitly requested or established by repository policy.
7. Test design becomes surface-driven; Playwright is browser-only.
8. Tracker persistence becomes opt-in and lifecycle-aware.
9. The canonical instruction ledger moves to root `user-instructions.md`; `skills/user-instructions.md` remains a one-way compatibility pointer during the observation window.

## Compatibility Rules

1. Use one-way aliases or wrappers only.
2. Emit canonical version 2 names and relations in new governance evidence.
3. Validate historical artifacts with their recorded schema and names.
4. Exclude wrappers from active skill-count budgets.
5. Warn on new use of discouraged names without breaking existing explicit use.
6. Record only bounded operational routing metadata; never prompts, source content, secrets, credentials, hidden reasoning, or private user data.

## Observation Gate

Do not remove or merge public names until:

1. all safety scenarios have equivalent or stricter outcomes
2. at least 30 representative tasks or two releases are recorded
3. aliases have zero unexplained failures
4. corrections, backtracking, validation failures, and task time do not materially worsen
5. an exact-commit release attestation passes

If a replacement changes command behavior, omits a safety gate, breaks artifact compatibility, or exceeds the accepted regression threshold, restore the previous routing entry and keep the compatibility name active.

Record content-free checkpoints with `skill-governance/scripts/record_routing_observation.py`. The recorder enforces the 100-record cache limit, catalog skill names, typed task classes/checkpoints, and aggregate-only summaries. Do not use field notes or the instruction ledger as a substitute for this bounded migration evidence.
