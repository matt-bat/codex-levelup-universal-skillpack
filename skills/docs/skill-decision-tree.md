# Skill Decision Tree

Use the smallest skill set that covers the task. Add process only when it changes the outcome, safety, clarity, or evidence quality.

## First Decision
Ask these in order:

1. Did the user invoke `--quizme`, or is quizme mode already active?
   - add `quizme-mode` and `requirement-clarifier`
   - finish interactive clarification before substantive execution
2. Is the user only asking for an answer?
   - use `token-reduction`
2. Is the task one deterministic local command?
   - add `scripted-command-execution`
3. Does the task require multiple dependent steps?
   - add `order-of-operations`
4. Does the task change behavior, workflow, policy, or docs?
   - add `doc-maintenance`
5. Is the task risky, ambiguous, multi-skill, or release-affecting?
   - add `skill-governance`
6. Could the skill set grow beyond the value of the task?
   - add `process-budget-controller`

If a skill does not change how the agent acts or what evidence it leaves behind, skip it.

## Common Paths
| Task Type | Minimum Skill Set |
|---|---|
| Simple answer | `token-reduction` |
| Any request while quizme mode is active | `quizme-mode`, `requirement-clarifier`, then the minimum task-specific skills after clarification |
| One local command | `token-reduction`, `scripted-command-execution` |
| Many skills could apply | `token-reduction`, `process-budget-controller`, plus only selected owner skills |
| Small isolated edit | `token-reduction`, `order-of-operations`, `scripted-command-execution` |
| Documentation-only update | `token-reduction`, `order-of-operations`, `doc-maintenance` |
| Bug report | `token-reduction`, `order-of-operations`, `diagnose-before-fix`, `scripted-command-execution` |
| Non-trivial code change | `token-reduction`, `order-of-operations`, `scripted-command-execution`, `regression-prevention` |
| Frontend layout or interaction work | `token-reduction`, `order-of-operations`, `thoughtful-approach`, `ui-design-skills`, `ui-spatial-canvas` |
| Browser or GUI runtime loop | `token-reduction`, `order-of-operations`, `pseudo-agentic-automation` |
| Release-readiness or governed policy change | `token-reduction`, `order-of-operations`, `skill-governance`, `governance-enforcement`, `regression-prevention`, `doc-maintenance` |
| Quality review or rating | `token-reduction`, `thoroughly-rate-review` |
| Skillpack maintenance review | `token-reduction`, `skill-usage-review`, `deprecation-management` when lifecycle state changes |

## Escalation Rules
Add `quizme-mode` when `--quizme` is invoked or remains active. It blocks substantive execution until clarification is complete.

Add `requirement-clarifier` when missing acceptance criteria could change the implementation.

Add `interdependent-change-planning` when the change touches coupled files, flows, or data paths that must stay coherent together.

Add `effective-testing-methods` when tests need to be created, amended, or mapped to changed behavior.

Add `project-backup` and `restore-drill` only for high-risk mutation, destructive operations, or unclear rollback paths.

Add `history-indexing`, `conversation-retention-summary`, or `artifact-budget-enforcement` only when cached history or bounded artifacts are actually part of the task.

## Stop Rules
1. Do not add a skill just because it exists.
2. Do not add governance artifacts for tiny isolated text changes unless a governed path or release decision requires them.
3. Do not update history artifacts for short sessions.
4. Do not broaden validation after a cheaper required check already fails.
5. If two skills overlap, use `SKILL-MAP.md` ownership order to choose one owner.

The decision tree is a guardrail, not a ceremony. It should make the work easier to trust without making small tasks feel inflated.
