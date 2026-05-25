# Codex Adapter

Use this repository's default instructions directly with Codex.

Codex can read project instructions and local skill files, so this is the most direct setup path. Keep the repository policy close to the codebase where you want the behavior enforced.

## Recommended Setup
1. keep `AGENTS.md` at the repository root
2. keep skills under `skills/` for this public repo or install them into Codex's configured skills directory
3. keep startup declarations enabled
4. run validators from the repository root before pushing governed changes

## Codex-Specific Behavior
Codex should:

1. declare selected skills at task start
2. use local-first execution
3. request approval before deployment or destructive operations
4. update `skills/user-instructions.md` when directives change
5. use `process-budget-controller` to avoid over-selecting skills

The startup declaration matters because it shows whether Codex understood the task shape before it starts editing.

## Validation
Use:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
```

For governed changes, use the release profile in [../validation-profiles.md](../validation-profiles.md).
