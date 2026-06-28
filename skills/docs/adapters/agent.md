# Agent Adapter

Use this repository's default instructions directly with an agent that can read project instructions and local skill files.

That is the most direct setup path. Keep the repository policy close to the codebase where you want the behavior enforced.

## Recommended Setup
1. keep `AGENTS.md` at the repository root
2. keep skills under `skills/` for this public repo or install them into the assistant's configured skills directory
3. keep startup declarations enabled
4. run validators from the repository root before pushing governed changes

## Agent-Specific Behavior
The agent should:

1. declare selected skills at task start
2. use local-first execution
3. request approval before deployment or destructive operations
4. update `skills/user-instructions.md` when directives change
5. use `process-budget-controller` to avoid over-selecting skills
6. toggle persistent conversation-local clarification with `--quizme`
7. prefer the interactive clarification console while quizme mode is active
8. support intuitive quizme options: `--mc`, `--one-at-a-time`, `--confirm`, and `--record`

The startup declaration matters because it shows whether the agent understood the task shape before it starts editing.

## Validation
Use:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
```

For governed changes, use the release profile in [../validation-profiles.md](../validation-profiles.md).
