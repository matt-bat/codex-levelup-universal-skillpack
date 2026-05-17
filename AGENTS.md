# AGENTS.md

## Codex Default Skill Policy

Use skills as a default enhancement to behavior on every task.

### Baseline Skills (Default)
Apply these by default unless clearly irrelevant:
1. `token-reduction`
2. `order-of-operations`

Apply when task changes behavior, workflows, or documentation:
1. `doc-maintenance`

### Conditional Skill Triggers
Apply these when conditions match:
1. `skill-governance`
   - multi-step, risky, ambiguous, or release-affecting tasks
2. `governance-enforcement`
   - when generating/validating governance artifacts or running CI policy enforcement checks
3. `requirement-clarifier`
   - when request ambiguity, missing acceptance criteria, or unclear non-goals could cause misbuilds
4. `semantic-policy-audit`
   - when intent-level policy/gate correctness must be audited beyond text snippet checks
5. `regression-prevention`
   - non-trivial code changes, refactors, dependency updates, auth/payment/data/API changes
6. `project-backup` + `restore-drill`
   - critical/high-risk changes with rollback or recovery risk
7. `thoughtful-approach`
   - feature planning/implementation that should model end-user expectations and scope-safe enhancements
8. `thoroughly-rate-review`
   - any request to review, rate, score, assess, evaluate, grade, benchmark, or compare quality
9. `user-instructions-tracker`
   - when directives are added/changed or when fulfillment/progress/status audit is requested
10. `history-indexing`
   - when long-session indexing/retrieval artifact maintenance is needed
11. `ui-spatial-canvas`
   - frontend UX, layout, navigation, interaction, visual system work
12. `scripted-command-execution`
   - deterministic local command workflows
13. `pseudo-agentic-automation`
   - browser/GUI automation or dynamic runtime interaction

### Trigger Matrix (Explicit Include/Exclude)
| Skill | Include When | Exclude When |
|---|---|---|
| `skill-governance` | Cross-cutting risk, multiple skills, release impact | Tiny isolated text-only change with no behavior impact |
| `governance-enforcement` | Governance scripts/validators/CI enforcement are being run or debugged | Policy-only/risk-model decisions with no tooling execution |
| `requirement-clarifier` | Request ambiguity could alter implementation outcome | Requirements are already explicit, testable, and bounded |
| `semantic-policy-audit` | Need intent-level policy conformance assessment | Only mechanical snippet/schema checks are needed |
| `regression-prevention` | Logic/refactor/dependency/API/auth/payment/data changes | Pure copy/style-only edits with no behavior shift |
| `project-backup` + `restore-drill` | Critical/high-risk or rollback-sensitive mutation | Low-risk reversible local edits |
| `thoughtful-approach` | Feature tasks needing must-have/nice-to-have/end-user expectation balancing | Narrow mechanical tasks with fixed requirements and no product decisions |
| `thoroughly-rate-review` | User asks for review/rating/scoring/evaluation (or synonym) | User asks for implementation only with no evaluation intent |
| `user-instructions-tracker` | New/changed directives or progress/fulfillment tracking is needed | No user directives or status tracking requirement in scope |
| `history-indexing` | Long-session retrieval/indexing overhead exists | Short sessions where direct retrieval is cheaper |
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
