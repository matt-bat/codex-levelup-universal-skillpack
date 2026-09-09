# Agent Adapter

[Documentation home](../README.md) · [Common AI setup](./common-ai.md) · [Generic adapter](./generic-agent.md)

Use this repository's default instructions directly with an agent that can read project instructions and local skill files.

That is the most direct setup path. Keep the repository policy close to the codebase where you want the behavior enforced.

## Recommended Setup
1. keep `AGENTS.md` at the repository root
2. keep skills under `skills/` for this public repo or install them into the assistant's configured skills directory
3. use `skills/skill-catalog.json` as the routing source and treat its Markdown views as generated
4. run validators from the repository root before committing governed changes

## Agent-Specific Behavior
The agent should:

1. allow zero selected skills for routine work and declare selections only when explicitly requested or when governed/audited work needs a durable routing record
2. use local-first execution
3. request approval before deployment or destructive operations
4. update the root `user-instructions.md` only for opted-in durable instruction tracking
5. let the task router enforce the optional-skill budget; keep `process-budget-controller` only as an explicit legacy alias
6. toggle persistent conversation-local clarification with `--quizme`
7. prefer the interactive clarification console while quizme mode is active
8. support intuitive quizme options: `--mc`, `--one-at-a-time`, `--confirm`, and `--record`
9. process pack-load and exact-command events with `skills/help/scripts/runtime_adapter.py`; pass lifecycle state within the conversation and allow its writable preference file to persist explicit mode toggles across conversations
10. run the post-install catalog and runtime checks after every skillpack update so the host does not continue using stale generated views

When governed or audited work needs a durable routing record, the declaration is routing evidence. Omitting it on routine work avoids making ceremony look like a safety guarantee.

Use the schema-v2 catalog with router contract 2.1. Create new governed artifacts with governance schema v3; retain schema-v1 and schema-v2 artifacts as readable historical evidence. When publication is authorized and `main` is protected, use a feature branch and pull request rather than attempting a direct push.

## Validation
Use:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 -m unittest skills.skill-governance.tests.test_runtime_adapter -v
```

For governed changes, use the release profile in [../validation-profiles.md](../validation-profiles.md).

The adapter stores only explicit mode booleans in `~/.config/agent-command-center/preferences.json`; set `AGENT_COMMAND_CENTER_PREFERENCES` for a portable or isolated writable location.
