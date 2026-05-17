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
| `skill-governance` | multi-step or risk-sensitive tasks | `order-of-operations`, `regression-prevention`, `effective-testing-methods`, `project-backup`, `restore-drill`, `doc-maintenance`, conditionals | `docs/governance/*.governance.json`, `docs/governance/*.governance.md`, `.codex/skills/docs/verification/constrained-environment-verification.md` | 2026-05-14T05:31:44Z |
| `governance-enforcement` | governance scripts or CI policy checks | `doc-maintenance`, `file-maintenance` | `.codex/skills/skill-governance/scripts/*` | 2026-05-13T15:43:58Z |
| `requirement-clarifier` | ambiguous requirements | `order-of-operations`, `doc-maintenance` | clarified acceptance contract in task artifacts/docs | 2026-05-13T15:43:58Z |
| `semantic-policy-audit` | intent-level policy audit | `skill-governance`, `doc-maintenance` | policy audit notes/docs | 2026-05-13T15:43:58Z |
| `thoughtful-approach` | end-user expectation modeling | `ui-design-skills`, `ui-spatial-canvas`, `regression-prevention`, `effective-testing-methods` | feature expectation notes/docs | 2026-05-13T15:43:58Z |
| `thoroughly-rate-review` | review/rate/score/evaluate requests | `semantic-policy-audit`, `skill-governance`, `doc-maintenance` | scoring artifact/report | 2026-05-13T15:43:58Z |
| `user-instructions-tracker` | new/changed directives or status audit | `doc-maintenance`, `file-maintenance`, `skill-governance` | `user-instructions.md` | 2026-05-13T15:43:58Z |
| `history-indexing` | long-session context retrieval overhead | `token-reduction`, `doc-maintenance` | `docs/chat-history-index.md` | 2026-05-13T15:43:58Z |
| `ui-spatial-canvas` | viewport-first frontend architecture | `ui-design-skills`, `regression-prevention`, `effective-testing-methods`, `doc-maintenance` | UI architecture/interaction docs | 2026-05-13T15:43:58Z |
| `ui-design-skills` | trusted-source UX principle application | `ui-spatial-canvas`, `thoughtful-approach`, `doc-maintenance` | UX checklist/review notes | 2026-05-13T15:43:58Z |
| `effective-testing-methods` | feature/behavior changes requiring test updates | `regression-prevention`, `scripted-command-execution`, `doc-maintenance` | test impact maps, coverage evidence, constrained-environment blocker evidence | 2026-05-14T05:31:44Z |
| `scripted-command-execution` | deterministic local shell workflows | `effective-testing-methods`, `doc-maintenance`, `regression-prevention` | command logs/evidence + prerequisite probes | 2026-05-14T05:31:44Z |
| `pseudo-agentic-automation` | dynamic browser/GUI automation | `regression-prevention`, `doc-maintenance` | automation scripts/logs | 2026-05-13T15:43:58Z |
| `token-reduction` | context or output compression needed | `history-indexing` | `docs/project-index.md` | 2026-05-13T15:43:58Z |
| `order-of-operations` | multi-step sequencing and dependency order | execution skill + validation/documentation skills | sequencing notes/evidence + constrained verification branch | 2026-05-14T05:31:44Z |
| `regression-prevention` | risky non-trivial changes | `effective-testing-methods`, `doc-maintenance` | risk map + test evidence + blocked-layer risk classification | 2026-05-14T05:31:44Z |
| `file-structure-optimization` | repository structure drift or duplication risk | `order-of-operations`, `doc-maintenance`, `file-maintenance` | structure audit and move/consolidation plan | 2026-05-13T15:43:58Z |
| `doc-maintenance` | behavior/workflow/policy doc drift risk | `file-maintenance`, `user-instructions-tracker` | `README.md`, `docs/*` | 2026-05-13T15:43:58Z |
| `file-maintenance` | ongoing file correctness/factuality/freshness maintenance | `doc-maintenance`, `file-structure-optimization` | file audit report and remediation notes | 2026-05-13T15:43:58Z |
| `project-backup` | high-risk mutation readiness | `restore-drill`, `doc-maintenance` | backup runbook/artifacts | 2026-05-13T15:43:58Z |
| `restore-drill` | restore validation and freshness | `doc-maintenance` | drill evidence/runbooks | 2026-05-13T15:43:58Z |

## Maintenance Workflow
1. update row(s) when skill trigger behavior changes
2. keep trigger relationships aligned with `SKILL-MAP.md`
3. update timestamp for changed rows
4. reference this file in cross-skill handoff summaries
