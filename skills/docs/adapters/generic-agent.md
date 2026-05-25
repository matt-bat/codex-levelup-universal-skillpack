# Generic Agent Adapter

Use this adapter when an agent cannot load Codex skills directly.

## Portable Core
Copy or summarize:
1. `AGENTS.md`
2. `skills/docs/skill-decision-tree.md`
3. `skills/docs/install-profiles.md`
4. the specific `SKILL.md` files for the chosen profile

## Required Behaviors
The agent should:
1. state selected skills or operating modes before substantial work
2. choose the smallest process budget that fits the task
3. execute locally by default
4. maintain docs when behavior or workflow changes
5. record validation evidence for governed changes

## Non-Portable Assumptions
Some commands and approval flows are Codex-specific. Replace them with the target agent's local command, approval, and artifact mechanisms.

## Minimum Profile
For generic agents, start with:
1. `token-reduction`
2. `order-of-operations`
3. `process-budget-controller`
4. `scripted-command-execution`
