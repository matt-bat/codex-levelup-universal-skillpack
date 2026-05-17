---
name: skill-governance
description: Use for selecting and enforcing the right process level across skills via deterministic risk scoring, mode-based gates, critical overrides, break-glass controls, ownership, and KPI review.
---

# Skill Governance

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `When to Use`
3. `Scope Boundary`
4. `Governance Output`
5. `Automation (Required)`

### Action Modules (Read As Needed)
1. Choosing governance mode:
   - `Step 1` through `Step 4`
2. Selecting mandatory/conditional gates:
   - `Step 5: Gate Matrix (Required Skills by Mode)`
3. Defining evidence and exceptions:
   - `Step 6: Evidence Contract by Mode`
   - `Step 7: Break-Glass Policy (Exception Path)`
4. Complex-scope handling:
   - `Step 8` through `Step 10`
5. Governance quality tuning:
   - `KPI Minimum Set`
   - `Guardrails Against Process Bloat`

### Escalation & Output
1. `Escalation Conditions`
2. `Anti-Patterns`
3. `Deliverable Format`

## Mission
Apply the minimum process needed for safety and quality, and the maximum process needed for risk.

This skill prevents:
1. under-governance on critical changes
2. over-governance on small tasks
3. inconsistent gate usage across operators

## When to Use
Use for any task that may involve multiple skills, risk-sensitive changes, or release-affecting work.

## Scope Boundary
This skill defines governance policy:
1. risk scoring
2. mode selection
3. gate selection
4. release recommendation logic
5. cross-skill trigger selection aligned to `docs/skill-index.md`

Use [Governance Enforcement](../governance-enforcement/SKILL.md) for:
1. script execution
2. artifact generation/validation commands
3. CI enforcement operations

## Governance Output
Every governed task must produce:
1. selected mode (`quick`, `standard`, `critical`)
2. risk score and rationale
3. required gates/skills
4. release recommendation (`go`, `go-with-risk`, `no-go`)
5. execution scope (`local_only` by default)
6. verification ownership preference (`model` or `user`) for test/build runs
7. `project_id` aligned to `docs/project-index.md`
8. user-facing summary in concise bullet points using full-language (no shorthand abbreviations)
9. durable rationale notes in code comments/docs/artifacts for non-obvious decisions

## Automation (Required)
Automation must be applied through [Governance Enforcement](../governance-enforcement/SKILL.md), which owns:
1. deterministic artifact tooling
2. CI policy enforcement
3. validator execution and failure remediation

Recommended artifact directory:
- `docs/governance/`

Minimum workflow:
1. generate artifact at task start
2. update gate statuses during execution
3. validate artifact before final recommendation/release decision
4. enforce artifact + validation policy in CI

Example:
```bash
python .codex/skills/skill-governance/scripts/generate_governance_artifact.py \
  --task-id TASK-123 \
  --project-id universal-app \
  --profile internal \
  --project-language TypeScript/Python \
  --project-description-max4 "Cross-platform business app" \
  --model-runs-test-build-default no \
  --skills-in-use "skill-governance,order-of-operations,scripted-command-execution,doc-maintenance,token-reduction" \
  --skills-execution-order "skill-governance,order-of-operations,scripted-command-execution,doc-maintenance,token-reduction" \
  --skills-selection-rationale "Risk-sensitive task requiring governance, deterministic execution, documentation sync, and concise communication discipline." \
  --execution-scope local_only \
  --execution-skill scripted-command-execution \
  --data-impact 1 \
  --business-impact 2 \
  --change-complexity 2 \
  --dependency-uncertainty 1 \
  --recoverability 1 \
  --behavior-or-workflow-changed

python .codex/skills/skill-governance/scripts/validate_governance_artifact.py \
  --artifact docs/governance/TASK-123.governance.json
```

Generator behavior:
1. writes `.governance.json` + `.governance.md`
2. upserts `docs/project-index.md` using artifact intake fields (`project_id`, language, <=4-word description, `yes/no` test-build preference, timestamp)

Strict release-gate validation example:
```bash
python .codex/skills/skill-governance/scripts/validate_governance_artifact.py \
  --artifact docs/governance/TASK-123.governance.json \
  --strict \
  --require-recommendation go
```

CI enforcement example:
```bash
python .codex/skills/skill-governance/scripts/enforce_governance_ci.py \
  --base-sha <base_sha> \
  --head-sha <head_sha> \
  --strict \
  --require-recommendation go
```

CI behavior:
1. if governed files changed and no updated governance artifact exists, fail
2. validate changed governance artifacts
3. in strict mode, fail on pending/failed required gates
4. in strict mode, fail if recommendation is below required threshold
5. validate skill policy artifacts (`AGENTS.md` + startup declaration sections in governance artifacts)
6. fail when `SKILL-MAP.md` and `docs/skill-index.md` skill ordering diverges
7. governed files include `.codex/skills/**`, `docs/governance/**`, `docs/project-index.md`, `AGENTS.md`, `.github/workflows/**`

## Step 1: Repository Profile
Set profile first:
1. `prototype`: experimental, non-production
2. `internal`: operational but limited blast radius
3. `production`: customer/business-critical impact

Profile affects strictness, but critical override triggers still apply.

## Step 1A: New-Project Intake (Required Once per New Project)
`New project` means not previously worked on by the model.

For new projects:
1. ask whether model should run tests/build by default, or user prefers to run them
2. assign/confirm a stable `project_id` (lowercase letters, digits, hyphens)
3. record preference in `docs/project-index.md` (`yes`/`no`)
4. record project language
5. record 4-word max project description
6. default execution scope to `local_only`
7. do not change execution scope to deployment unless user explicitly requests deployment actions

## Step 2: Deterministic Risk Scoring
Score each dimension 0-3:
1. **Data impact**
   - 0 none, 1 low, 2 moderate, 3 destructive/irreversible possible
2. **User/business impact**
   - 0 none, 1 minor, 2 visible degradation, 3 critical flow/payment/auth impact
3. **Change complexity**
   - 0 isolated, 1 small multi-file, 2 cross-module, 3 cross-system
4. **Dependency/runtime uncertainty**
   - 0 none, 1 known stable, 2 some uncertainty, 3 major/unknown compatibility
5. **Recoverability**
   - 0 instant rollback, 1 simple rollback, 2 partial rollback complexity, 3 unclear rollback

Total score = sum of dimensions (0-15).

Default mode by score:
1. `0-4` => `quick`
2. `5-9` => `standard`
3. `10-15` => `critical`

## Step 3: Critical Override Triggers
Force mode to `critical` regardless of numeric score if any trigger is present:
1. auth/session/permission boundary changes
2. payment/order/financial logic changes
3. schema migrations/data deletion/backfills
4. customer-facing API contract breaks
5. production infra/runtime/security boundary changes
6. missing rollback path for risky mutation

## Step 4: Mode Adjustment by Profile
Apply profile modifier after scoring:
1. `prototype`: can downgrade one level only if no critical override
2. `internal`: no modifier
3. `production`: upgrade one level when score is at top of band (`4`, `9`) or uncertainty is high

Never downgrade below `critical` when override triggers apply.

## Step 5: Gate Matrix (Required Skills by Mode)
### Quick
Required:
1. `order-of-operations`
2. `scripted-command-execution` or `pseudo-agentic-automation` (task-dependent)
3. `doc-maintenance` if behavior/workflow/config changed

Validation minimum:
1. smoke/targeted checks
2. concise evidence
3. respect verification ownership preference (`model` vs `user`)

### Standard
Required:
1. `order-of-operations`
2. execution skill (`scripted-command-execution` or `pseudo-agentic-automation`)
3. `regression-prevention`
4. `doc-maintenance` when relevant
5. `token-reduction` for communication discipline

Validation minimum:
1. static/unit/integration scope as applicable
2. targeted E2E for impacted user paths
3. explicit residual risk statement
4. respect verification ownership preference (`model` vs `user`)

### Critical
Required:
1. `order-of-operations`
2. `project-backup`
3. `restore-drill` freshness check or drill if stale
4. execution skill
5. `regression-prevention` full gate set
6. `doc-maintenance`
7. `token-reduction` (cannot suppress required evidence)

Validation minimum:
1. full required regression matrix
2. backup/restore gate status
3. explicit release recommendation (`go`, `go-with-risk`, `no-go`)
4. respect verification ownership preference (`model` vs `user`) unless explicit risk exception is approved

### Conditional Gate Additions (All Modes)
Add these gates when conditions match:
1. `requirement-clarifier`
   - include when requirements/acceptance criteria are ambiguous and could change implementation outcome
2. `thoughtful-approach`
   - include when the task involves product/feature decisions that require end-user expectation modeling
3. `thoroughly-rate-review`
   - include when user intent is review/rating/scoring/assessment/evaluation (or synonyms)
4. `semantic-policy-audit`
   - include when intent-level policy conformance must be audited beyond mechanical checks
5. `user-instructions-tracker`
   - include when directives are added/changed or fulfillment/progress status tracking is requested
6. `effective-testing-methods`
   - include when feature/behavior updates require explicit unit and Playwright test amendments/additions
7. `file-structure-optimization`
   - include when repository layout refactors or duplicate-file cleanup are part of scope
8. `file-maintenance`
   - include when file-level factuality, staleness, or documentation accuracy maintenance is requested

Before adding conditional gates:
1. consult `docs/skill-index.md`
2. verify trigger condition and companion skills
3. choose minimum complete set

Conditional additions are required once triggered and must appear in:
1. startup declaration (`skills_in_use` and execution order)
2. governance evidence contract and final summary

### Step 5A: Ownership Boundary Matrix (Required)
To prevent overlap and process bloat, each required gate must be scoped to its owned decisions:

1. `skill-governance`:
   - mode selection and policy gates
2. `order-of-operations`:
   - execution graph and validation sequence
3. `regression-prevention`:
   - regression risk tier, release-readiness criteria, residual-risk statement
4. `effective-testing-methods`:
   - test impact mapping and test-update completeness
5. execution skill (`scripted-command-execution` or `pseudo-agentic-automation`):
   - command/runtime execution and operational retries

Deduplication rule:
1. if two skills produce the same artifact field, keep only the owner skill artifact and reference it rather than duplicating content.

## Step 6: Evidence Contract by Mode
### Quick evidence
1. mode + score
2. steps executed
3. minimal validation outcomes

### Standard evidence
1. quick evidence +
2. impact map
3. validation scope by layer
4. residual risks

### Critical evidence
1. standard evidence +
2. backup artifact and integrity evidence
3. restore freshness/pass status
4. rollback plan
5. release decision

Constrained-environment addendum (all modes):
1. if any required validation layer is blocked by host/runtime limitations:
   - record exact blocker command and exact error message
   - run fallback evidence path from `.codex/skills/docs/verification/constrained-environment-verification.md`
   - downgrade recommendation to `go-with-risk` or `no-go` when blocked layer affects critical flows

Artifact policy:
1. store both `.governance.json` and `.governance.md`
2. treat JSON as machine source of truth
3. treat markdown as human review checklist
4. include concise rationale for key risk tradeoffs in artifact/docs rather than long transient reasoning

## Step 7: Break-Glass Policy (Exception Path)
Allowed only when urgency blocks normal flow.

Required fields:
1. reason for bypass
2. exact gates bypassed
3. explicit risk acceptance by owner
4. time-bound expiry (default <= 72 hours)
5. mandatory remediation task with owner/date

Break-glass constraints:
1. cannot bypass legal/safety/security non-negotiables
2. cannot be used repeatedly without review
3. two consecutive break-glass uses on same area trigger governance review
4. validator must fail if required break-glass metadata is missing

## Step 8: Conflict and Ambiguity Handling
When signals conflict:
1. safety-first precedence applies
2. if risk score and override disagree, override wins
3. if dependency graph unclear, pause for minimal clarification
4. if test layer unavailable, mode may continue only with explicit elevated risk
5. local-only execution remains default unless explicit deployment request is present

## Step 9: Monorepo and Mixed-Risk Tasks
For mixed scope:
1. score subdomains independently
2. apply highest mode to shared/release-critical path
3. allow lower mode on isolated unaffected subpaths only if boundaries are explicit

## Step 10: Ownership and Review Cadence
Assign governance owner per repository.

Minimum cadence:
1. weekly: review break-glass usage and unresolved critical risks
2. monthly: review KPI trends and mode drift
3. quarterly: recalibrate scoring rubric and override list

Branch protection recommendation:
1. require `Governance Enforcement` workflow status check on `main`
2. disallow bypass except approved emergency process

## KPI Minimum Set
Track:
1. mode distribution (`quick/standard/critical`)
2. regression escape rate
3. % critical tasks with complete gates
4. break-glass frequency and closure SLA
5. restore freshness compliance for critical releases
6. doc drift incidents after release
7. token efficiency trend (cost/turn) without quality drop

## Guardrails Against Process Bloat
1. `quick` mode must stay lightweight
2. do not force critical-style artifacts in quick mode
3. auto-upgrade only on defined criteria
4. remove obsolete gates during periodic review

## Escalation Conditions
Escalate governance review when:
1. repeated high-severity regressions occur in non-critical mode
2. critical overrides are frequently missed
3. break-glass usage trends upward
4. restore freshness gate blocks repeated releases
5. operators disagree repeatedly on scoring interpretation

## Anti-Patterns
1. subjective mode assignment without scoring
2. forcing critical process on low-risk edits by default
3. skipping override triggers due to schedule pressure
4. treating token reduction as permission to omit evidence
5. using break-glass as standard workflow
6. deploying without explicit user request
7. ignoring stated test/build ownership preference

## Deliverable Format
When applying this skill, provide:
1. repository profile
2. risk score table + total
3. selected mode and override status
4. required gates/skills
5. evidence status
6. final recommendation (`go`, `go-with-risk`, `no-go`)
7. artifact paths (`.governance.json`, `.governance.md`)

Style requirement:
1. keep user-facing output concise
2. avoid reiterating the user's last request
3. use bullet points and minimal full sentences

## Related Skills
- [SKILL-MAP](../SKILL-MAP.md): routing and sequencing across skills.
- [Order of Operations](../order-of-operations/SKILL.md): dependency-correct execution after mode selection.
- [Regression Prevention](../regression-prevention/SKILL.md): quality/risk validation gates.
- [Effective Testing Methods](../effective-testing-methods/SKILL.md): detailed unit and Playwright expectations for behavior-changing updates.
- [File Structure Optimization](../file-structure-optimization/SKILL.md): repository-structure refactor and consolidation governance.
- [Project Backup](../project-backup/SKILL.md): pre-risk backup readiness.
- [Restore Drill](../restore-drill/SKILL.md): restore validity and freshness gates.
- [Doc Maintenance](../doc-maintenance/SKILL.md): ensure policy and runbook updates remain synchronized.
- [File Maintenance](../file-maintenance/SKILL.md): ongoing file factuality and staleness control for policy artifacts.
- [Token Reduction](../token-reduction/SKILL.md): keep governance reporting concise but sufficient.
