# AGENTS.md

## Codex Default Skill Policy

Use skills as a default enhancement to behavior on every task.

### Baseline Skills (Default)
Apply these by default unless clearly irrelevant:
1. `token-reduction`
2. `order-of-operations`

Apply when task changes behavior, workflows, or documentation:
1. `doc-maintenance`

### Minimum Viable Skill Use
Use the smallest skill set that safely covers the task.

Default caps:
1. answer-only request: `token-reduction`
2. one deterministic local command: `token-reduction`, `scripted-command-execution`
3. tiny isolated text edit: `token-reduction`, `order-of-operations`
4. small isolated code edit: `token-reduction`, `order-of-operations`, `scripted-command-execution`, plus `regression-prevention` when behavior can change
5. documentation-only update: `token-reduction`, `order-of-operations`, `doc-maintenance`
6. governed or release-affecting change: add `skill-governance` and the required gates it selects

Stop rules:
1. do not add a skill only because it is adjacent to the task
2. do not generate governance artifacts for tiny isolated non-governed changes
3. do not update history or cache artifacts unless long-session retrieval or bounded artifact maintenance is actually in scope
4. if two skills overlap, use `SKILL-MAP.md` ownership boundaries to pick the owner

### Conditional Skill Triggers
Apply these when conditions match:
1. `skill-governance`
   - multi-step, risky, ambiguous, or release-affecting tasks
2. `process-budget-controller`
   - when several skills could apply and the task needs an explicit cap on process overhead
3. `governance-enforcement`
   - when generating/validating governance artifacts or running CI policy enforcement checks
4. `requirement-clarifier`
   - when request ambiguity, missing acceptance criteria, or unclear non-goals could cause misbuilds
5. `diagnose-before-fix`
   - when a bug report may describe symptoms rather than the verified root cause, or a user-suggested cause still needs independent verification
6. `semantic-policy-audit`
   - when intent-level policy/gate correctness must be audited beyond text snippet checks
7. `interdependent-change-planning`
   - when changes touch coupled files, flows, or data paths that must remain coherent together
8. `regression-prevention`
   - non-trivial code changes, refactors, dependency updates, auth/payment/data/API changes
9. `project-backup` + `restore-drill`
   - critical/high-risk changes with rollback or recovery risk
10. `thoughtful-approach`
   - feature planning/implementation that should model end-user expectations and scope-safe enhancements
11. `thoroughly-rate-review`
   - any request to review, rate, score, assess, evaluate, grade, benchmark, or compare quality
12. `user-instructions-tracker`
   - when directives are added/changed or when fulfillment/progress/status audit is requested
13. `history-indexing`
   - when long-session indexing/retrieval artifact maintenance is needed
14. `conversation-retention-summary`
   - when a bounded summary of the last 10 conversations needs to be refreshed or continued
15. `artifact-budget-enforcement`
   - when cached artifacts, summaries, indexes, or notes need hard limits and pruning
16. `skill-usage-review`
   - when recent task evidence should be reviewed for skill overuse, underuse, friction, or missing triggers
17. `deprecation-management`
   - when skills, docs, or workflows are renamed, merged, superseded, discouraged, deprecated, or removed
18. `ui-spatial-canvas`
   - frontend UX, layout, navigation, interaction, visual system work
19. `scripted-command-execution`
   - deterministic local command workflows
20. `pseudo-agentic-automation`
   - browser/GUI automation or dynamic runtime interaction

### Trigger Matrix (Explicit Include/Exclude)
| Skill | Include When | Exclude When |
|---|---|---|
| `skill-governance` | Cross-cutting risk, multiple skills, release impact | Tiny isolated text-only change with no behavior impact |
| `process-budget-controller` | Multiple skills could apply and process needs explicit caps | One obvious skill is enough or critical gates already determine the workflow |
| `governance-enforcement` | Governance scripts/validators/CI enforcement are being run or debugged | Policy-only/risk-model decisions with no tooling execution |
| `requirement-clarifier` | Request ambiguity could alter implementation outcome | Requirements are already explicit, testable, and bounded |
| `diagnose-before-fix` | Debugging or remediation needs verified root cause | User already has a proven cause and only wants a direct patch, though verification is still preferred |
| `semantic-policy-audit` | Need intent-level policy conformance assessment | Only mechanical snippet/schema checks are needed |
| `interdependent-change-planning` | Several coupled files, flows, or data paths must change together | Tiny isolated text-only change with no downstream effect |
| `regression-prevention` | Logic/refactor/dependency/API/auth/payment/data changes | Pure copy/style-only edits with no behavior shift |
| `project-backup` + `restore-drill` | Critical/high-risk or rollback-sensitive mutation | Low-risk reversible local edits |
| `thoughtful-approach` | Feature tasks needing must-have/nice-to-have/end-user expectation balancing | Narrow mechanical tasks with fixed requirements and no product decisions |
| `thoroughly-rate-review` | User asks for review/rating/scoring/evaluation (or synonym) | User asks for implementation only with no evaluation intent |
| `user-instructions-tracker` | New/changed directives or progress/fulfillment tracking is needed | No user directives or status tracking requirement in scope |
| `history-indexing` | Long-session retrieval/indexing overhead exists | Short sessions where direct retrieval is cheaper |
| `conversation-retention-summary` | Recent-context handoff needs the latest 10 conversations only | Full transcript retention or long archive reconstruction is needed |
| `artifact-budget-enforcement` | Cached artifacts or summaries need explicit size caps | No bounded-cache surface exists |
| `skill-usage-review` | Recent artifacts or task history should be reviewed for overuse, underuse, or friction | No usage evidence exists yet |
| `deprecation-management` | Compatibility or migration guidance is needed for old skills/docs/workflows | A direct edit fixes the issue without lifecycle impact |
| `ui-spatial-canvas` | Frontend IA, layout, interaction, visual-system work | Backend-only or CLI-only tasks |
| `scripted-command-execution` | Deterministic local shell workflows | Dynamic browser flows requiring runtime adaptation |
| `pseudo-agentic-automation` | Authenticated/dynamic browser or GUI interaction | Deterministic shell/API/file-only work |

### Startup Declaration (Required)
At task start, state:
1. `Skills in use`
2. reason each skill was selected
3. execution order

Task start template:
```md
Skills in use:
- <skill-a>, <skill-b>, <skill-c>

Selection rationale:
- <why skill-a applies>
- <why skill-b applies>
- <why skill-c applies>

Execution order:
1. <skill-a>
2. <skill-b>
3. <skill-c>
```

### Execution Defaults
1. local-first execution; no deployment unless explicitly requested
2. concise user-facing responses in bullet points with minimal full sentences
3. no shorthand abbreviations in user-facing responses
4. keep internal planning compact and prioritize durable rationale in code comments/docs/artifacts
5. keep `user-instructions.md` current when directives or fulfillment state changes

### Conflict Rule
If multiple skills apply, use the minimum set that fully covers the task, in dependency-correct order.
