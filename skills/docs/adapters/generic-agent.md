# Generic Agent Adapter

Use this adapter when an agent cannot load the repository's skills directly.

The portable idea is simple: turn the skills into operating modes, keep the routing rules, and replace agent-specific tool behavior with the target agent's own command and approval flow.

## Portable Core
Copy or summarize:

1. `AGENTS.md`
2. `skills/docs/skill-decision-tree.md`
3. `skills/docs/install-profiles.md`
4. the specific `SKILL.md` files for the chosen profile

Do not copy the whole pack into a tool that cannot honor most of it. Start with the chosen profile and add more only when the target agent can use it.

## Required Behaviors
The agent should:

1. allow zero selected skills and state selected modes only when explicitly requested or when governed/audited work needs a durable routing record
2. use router contract 2.1's smallest-sufficient process budget
3. execute locally by default
4. maintain docs when behavior or workflow changes
5. record validation evidence for governed changes
6. support persistent conversation-local `--quizme` clarification mode when the target agent can preserve turn state

## Non-Portable Assumptions
Some commands, approval flows, sandbox rules, and skill-loading behavior are implementation-specific. Replace them with the target agent's local command, approval, and artifact mechanisms.

If a feature cannot be ported cleanly, document the gap instead of pretending the agent has the same controls.

Preserve the contract boundaries: the catalog is schema v2, the router contract is 2.1, and new governance artifacts are schema v3. Keep schema-v1 and schema-v2 governance artifacts readable as historical evidence. When publication is authorized and `main` is protected, use the target platform's feature-branch and pull-request flow rather than bypassing required checks.

For `--quizme`, replace the source agent's interactive clarification console with the target agent's equivalent prompt UI. Preserve supported options when possible: `--mc`, `--one-at-a-time`, `--confirm`, and `--record`.

## Minimum Profile
For generic agents, make these packages available first:

1. `requirement-clarifier`
2. `regression-prevention`
3. `scripted-command-execution`
4. `doc-maintenance`

Availability does not imply activation. The core policy and task router handle routine work without a skill, and each package activates only when its catalog trigger matches.
