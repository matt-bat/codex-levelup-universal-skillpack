# Skill Decision Tree

Use the smallest skill set that covers the task. Add process only when it changes the outcome, safety, or evidence quality.

## First Decision
1. Is the user asking only for an answer?
   - use `token-reduction`
2. Is the task a deterministic local command?
   - add `scripted-command-execution`
3. Does the task require multiple dependent steps?
   - add `order-of-operations`
4. Does the task change behavior, workflow, policy, or docs?
   - add `doc-maintenance`
5. Is the task risky, ambiguous, multi-skill, or release-affecting?
   - add `skill-governance`

## Common Paths
| Task Type | Minimum Skill Set |
|---|---|
| Simple answer | `token-reduction` |
| One local command | `token-reduction`, `scripted-command-execution` |
| Small isolated edit | `token-reduction`, `order-of-operations`, `scripted-command-execution` |
| Documentation-only update | `token-reduction`, `order-of-operations`, `doc-maintenance` |
| Bug report | `token-reduction`, `order-of-operations`, `diagnose-before-fix`, `scripted-command-execution` |
| Non-trivial code change | `token-reduction`, `order-of-operations`, `scripted-command-execution`, `regression-prevention` |
| Frontend layout or interaction work | `token-reduction`, `order-of-operations`, `thoughtful-approach`, `ui-design-skills`, `ui-spatial-canvas` |
| Browser or GUI runtime loop | `token-reduction`, `order-of-operations`, `pseudo-agentic-automation` |
| Release-readiness or governed policy change | `token-reduction`, `order-of-operations`, `skill-governance`, `governance-enforcement`, `regression-prevention`, `doc-maintenance` |
| Quality review or rating | `token-reduction`, `thoroughly-rate-review` |

## Escalation Rules
Add `requirement-clarifier` when the answer could change based on missing acceptance criteria.

Add `interdependent-change-planning` when the change touches coupled files, flows, or data paths.

Add `effective-testing-methods` when tests must be created, amended, or mapped to changed behavior.

Add `project-backup` and `restore-drill` only for high-risk mutation, destructive operations, or unclear rollback paths.

Add `history-indexing`, `conversation-retention-summary`, or `artifact-budget-enforcement` only when cached history or bounded artifacts are actually in scope.

## Stop Rules
1. Do not add a skill just because it exists.
2. Do not add governance artifacts for tiny isolated text changes unless a governed path or release decision is involved.
3. Do not update history artifacts for short sessions.
4. Do not broaden validation after a cheaper required check already fails.
5. If two skills overlap, use `SKILL-MAP.md` ownership order to select one owner.
