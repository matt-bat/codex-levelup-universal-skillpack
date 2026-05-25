# Generic Agent Adapter

Use this adapter when an agent cannot load Codex skills directly.

The portable idea is simple: turn the skills into operating modes, keep the routing rules, and replace Codex-specific tool behavior with the target agent's own command and approval flow.

## Portable Core
Copy or summarize:

1. `AGENTS.md`
2. `skills/docs/skill-decision-tree.md`
3. `skills/docs/install-profiles.md`
4. the specific `SKILL.md` files for the chosen profile

Do not copy the whole pack into a tool that cannot honor most of it. Start with the chosen profile and add more only when the target agent can use it.

## Required Behaviors
The agent should:

1. state selected skills or operating modes before substantial work
2. choose the smallest process budget that fits the task
3. execute locally by default
4. maintain docs when behavior or workflow changes
5. record validation evidence for governed changes

## Non-Portable Assumptions
Some commands, approval flows, sandbox rules, and skill-loading behavior are Codex-specific. Replace them with the target agent's local command, approval, and artifact mechanisms.

If a feature cannot be ported cleanly, document the gap instead of pretending the agent has the same controls.

## Minimum Profile
For generic agents, start with:

1. `token-reduction`
2. `order-of-operations`
3. `process-budget-controller`
4. `scripted-command-execution`

That profile carries the core workflow without requiring the heavier governance machinery.
