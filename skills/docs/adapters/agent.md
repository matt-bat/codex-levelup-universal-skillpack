# Agent Adapter

Use this repository's default instructions directly with an agent that can read project instructions and local skill files.

That is the most direct setup path. Keep the repository policy close to the codebase where you want the behavior enforced.

## Recommended Setup
1. keep `AGENTS.md` at the repository root
2. keep skills under `skills/` for this public repo or install them into the assistant's configured skills directory
3. use `skills/skill-catalog.json` as the routing source and treat its Markdown views as generated
4. run validators from the repository root before pushing governed changes

## Agent-Specific Behavior
The agent should:

1. allow zero selected skills for routine work and declare selections only for governed/audited work or when explicitly requested
2. use local-first execution
3. request approval before deployment or destructive operations
4. update the root `user-instructions.md` only for opted-in durable instruction tracking
5. let the task router enforce the optional-skill budget; keep `process-budget-controller` only as an explicit legacy alias
6. toggle persistent conversation-local clarification with `--quizme`
7. prefer the interactive clarification console while quizme mode is active
8. support intuitive quizme options: `--mc`, `--one-at-a-time`, `--confirm`, and `--record`

For governed work, the declaration is routing evidence. Omitting it on routine work avoids making ceremony look like a safety guarantee.

## Validation
Use:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
```

For governed changes, use the release profile in [../validation-profiles.md](../validation-profiles.md).
