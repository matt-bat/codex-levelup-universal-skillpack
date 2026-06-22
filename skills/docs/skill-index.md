# Skill Index

## Purpose
Canonical routing index for all local skills.

Use this file when:
1. selecting a primary skill for a task
2. a skill triggers or recommends another skill
3. resolving overlap between similar skills

## Cross-Skill Trigger Rule (Required)
If one skill triggers another skill:
1. consult this index first
2. confirm trigger condition match
3. choose the minimum skill set that covers the task
4. record selected skill order in startup declaration

## Index Table
| Skill | Primary Trigger | Typical Triggers Another Skill | Canonical Artifacts | Last Updated UTC |
|---|---|---|---|---|
| `skill-governance` | multi-step or risk-sensitive tasks | `order-of-operations`, `regression-prevention`, `effective-testing-methods`, `project-backup`, `restore-drill`, `doc-maintenance`, conditionals | `docs/governance/*.governance.json`, `docs/governance/*.governance.md`, `skills/docs/verification/constrained-environment-verification.md` | 2026-05-24T13:00:00Z |
| `process-budget-controller` | multiple skills could apply and process needs explicit caps | `token-reduction`, `skill-governance`, `order-of-operations` | process tier and maximum skill/artifact allowance | 2026-05-24T15:00:00Z |
| `governance-enforcement` | governance scripts or CI policy checks | `doc-maintenance`, `file-maintenance` | `skills/skill-governance/scripts/*`, `.github/workflows/skills-governance-ci.yml` | 2026-05-24T13:00:00Z |
| `requirement-clarifier` | ambiguous requirements | `order-of-operations`, `doc-maintenance` | clarified acceptance contract in task artifacts/docs | 2026-05-13T15:43:58Z |
| `quizme-mode` | `--quizme` invoked or persistent conversation-local quizme state active | `requirement-clarifier`, `skill-governance` when governed task state must be recorded | interactive clarification rounds, aligned task contract, optional durable contract evidence | 2026-05-30T05:11:28Z |
| `diagnose-before-fix` | bug reports or failures where the root cause is not yet verified | `regression-prevention`, `effective-testing-methods`, `scripted-command-execution`, `requirement-clarifier` | symptom report, reproduction notes, verified-cause notes | 2026-05-22T18:30:00Z |
| `semantic-policy-audit` | intent-level policy audit | `skill-governance`, `doc-maintenance` | policy audit notes/docs | 2026-05-13T15:43:58Z |
| `interdependent-change-planning` | changes that touch coupled files, flows, or data paths | `thoughtful-approach`, `regression-prevention`, `order-of-operations`, `doc-maintenance` | impact map, dependency ring notes | 2026-05-22T18:30:00Z |
| `thoughtful-approach` | end-user expectation modeling | `ui-design-skills`, `ui-spatial-canvas`, `regression-prevention`, `effective-testing-methods` | feature expectation notes/docs | 2026-05-13T15:43:58Z |
| `thoroughly-rate-review` | review/rate/score/evaluate requests | `semantic-policy-audit`, `skill-governance`, `doc-maintenance` | scoring artifact/report | 2026-05-13T15:43:58Z |
| `user-instructions-tracker` | new/changed directives or status audit | `doc-maintenance`, `file-maintenance`, `skill-governance` | `user-instructions.md` | 2026-05-13T15:43:58Z |
| `history-indexing` | long-session context retrieval overhead | `token-reduction`, `conversation-retention-summary`, `artifact-budget-enforcement`, `doc-maintenance` | `docs/chat-history-index.md` | 2026-05-13T15:43:58Z |
| `conversation-retention-summary` | rolling summary of the last 10 conversations | `history-indexing`, `artifact-budget-enforcement`, `token-reduction`, `doc-maintenance`, `file-maintenance` | `docs/chat-history-summary.md` | 2026-05-22T18:30:00Z |
| `ui-spatial-canvas` | viewport-first frontend architecture | `ui-design-skills`, `regression-prevention`, `effective-testing-methods`, `doc-maintenance` | UI architecture/interaction docs | 2026-05-13T15:43:58Z |
| `ui-design-skills` | trusted-source UX principle application | `ui-spatial-canvas`, `thoughtful-approach`, `doc-maintenance` | UX checklist/review notes | 2026-05-13T15:43:58Z |
| `effective-testing-methods` | feature/behavior changes requiring test updates | `regression-prevention`, `scripted-command-execution`, `doc-maintenance` | test impact maps, coverage evidence, constrained-environment blocker evidence | 2026-05-14T05:31:44Z |
| `scripted-command-execution` | deterministic local shell workflows | `effective-testing-methods`, `doc-maintenance`, `regression-prevention` | command logs/evidence + prerequisite probes | 2026-05-14T05:31:44Z |
| `pseudo-agentic-automation` | dynamic browser/GUI automation | `regression-prevention`, `doc-maintenance` | automation scripts/logs | 2026-05-13T15:43:58Z |
| `token-reduction` | context or output compression needed | `history-indexing`, `artifact-budget-enforcement` | `docs/project-index.md` | 2026-05-13T15:43:58Z |
| `artifact-budget-enforcement` | cached artifacts, indexes, or summaries need explicit caps | `token-reduction`, `history-indexing`, `file-maintenance` | `docs/cache-budgets.md` | 2026-05-22T18:30:00Z |
| `order-of-operations` | multi-step sequencing and dependency order | execution skill + validation/documentation skills | sequencing notes/evidence + constrained verification branch | 2026-05-14T05:31:44Z |
| `regression-prevention` | risky non-trivial changes | `effective-testing-methods`, `doc-maintenance` | risk map + test evidence + blocked-layer risk classification | 2026-05-14T05:31:44Z |
| `file-structure-optimization` | repository structure drift or duplication risk | `order-of-operations`, `doc-maintenance`, `file-maintenance` | structure audit and move/consolidation plan | 2026-05-13T15:43:58Z |
| `doc-maintenance` | behavior/workflow/policy doc drift risk | `file-maintenance`, `user-instructions-tracker` | `README.md`, `docs/*` | 2026-05-13T15:43:58Z |
| `file-maintenance` | ongoing file correctness/factuality/freshness maintenance | `doc-maintenance`, `file-structure-optimization` | file audit report and remediation notes | 2026-05-13T15:43:58Z |
| `skill-usage-review` | recent task evidence should be reviewed for skill overuse, underuse, missing triggers, or friction | `thoroughly-rate-review`, `deprecation-management`, `doc-maintenance` | usage review report from governance artifacts, trackers, handoffs, or commits | 2026-05-24T15:00:00Z |
| `deprecation-management` | skills, docs, or workflows are superseded, merged, renamed, discouraged, deprecated, or removed | `file-maintenance`, `doc-maintenance`, `skill-usage-review` | deprecation record with replacement, migration notes, and removal criteria | 2026-05-24T15:00:00Z |
| `project-backup` | high-risk mutation readiness | `restore-drill`, `doc-maintenance` | backup runbook/artifacts | 2026-05-13T15:43:58Z |
| `restore-drill` | restore validation and freshness | `doc-maintenance` | drill evidence/runbooks | 2026-05-13T15:43:58Z |

## Maintenance Workflow
1. update row(s) when skill trigger behavior changes
2. keep trigger relationships aligned with `SKILL-MAP.md`
3. update timestamp for changed rows
4. reference this file in cross-skill handoff summaries
