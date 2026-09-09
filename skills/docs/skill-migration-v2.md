# Skill Migration Version 2

[Documentation home](./README.md) · [Routing architecture](./routing-architecture-v2.md) · [Install profiles](./install-profiles.md)

## Policy

Version 2 narrows activation and introduces typed routing without immediately deleting public skill names. The canonical catalog remains schema v2, its current router contract is 2.1, and new governance artifacts use schema v3. Existing explicit commands and supported names continue through the observation window.

## Immediate Changes

1. Universal behavior moves into core policy instead of automatic skill selection.
2. `process-budget-controller` becomes a compatibility wrapper for router budget policy.
3. `internal-lang` uses explicit `--internal-lang` commands so every user-facing activation flag has the `--` prefix.
4. `hyperfocus-discovery` becomes an explicit bounded branch-management mode.
5. Plain review no longer activates weighted scoring.
6. Spatial Canvas activates only when explicitly requested or established by repository policy.
7. Test design becomes surface-driven; Playwright is browser-only.
8. Tracker persistence becomes opt-in and lifecycle-aware.
9. The canonical instruction ledger moves to root `user-instructions.md`; `skills/user-instructions.md` remains a one-way compatibility pointer during the observation window.

## Compatibility Rules

1. Use one-way aliases or wrappers only.
2. Emit current canonical names and typed relations in router-contract-2.1 results and new schema-v3 governance evidence.
3. Keep schema-v1 and schema-v2 governance artifacts readable as historical evidence with their recorded names; never rewrite them into schema v3.
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

When `main` is protected and remote publication is authorized, exercise the migration through a feature branch and pull request so the required governance check evaluates the candidate before merge.

If a replacement changes command behavior, omits a safety gate, breaks artifact compatibility, or exceeds the accepted regression threshold, restore the previous routing entry and keep the compatibility name active.

Record content-free checkpoints with `skill-governance/scripts/record_routing_observation.py`. The recorder enforces the 100-record cache limit, catalog skill names, typed task classes/checkpoints, and aggregate-only summaries. Do not use field notes or the instruction ledger as a substitute for this bounded migration evidence.
