# Skill Map

## Purpose
Quick routing guide for when to apply each skill and how multiple skills should be sequenced together.

## Global Defaults
1. Local-first execution: do not deploy unless explicitly requested by the user.
2. New-project intake: if the model has not worked on the project before, ask whether model should run tests/build by default or user will run them to save tokens.
3. For new projects, maintain `docs/project-index.md` with:
   - project language
   - 4-word max project description
   - test/build preference (`yes`/`no`)
   - keep values synchronized with governance artifact intake fields when governance scripts are used
4. User-facing communication:
   - concise bullet points
   - minimal full sentences
   - no reiteration of the user's last request
   - no shorthand abbreviations in user responses
5. Internal planning and rationale capture:
   - keep internal planning shorthand ultra-concise
   - prefer writing important rationale as code comments or repo docs/artifacts
6. Cross-skill trigger routing:
   - when one skill triggers another, consult `docs/skill-index.md` first

## Skill Index
1. `skill-governance`
2. `governance-enforcement`
3. `requirement-clarifier`
4. `semantic-policy-audit`
5. `thoughtful-approach`
6. `thoroughly-rate-review`
7. `user-instructions-tracker`
8. `history-indexing`
9. `ui-spatial-canvas`
10. `ui-design-skills`
11. `effective-testing-methods`
12. `scripted-command-execution`
13. `pseudo-agentic-automation`
14. `token-reduction`
15. `order-of-operations`
16. `regression-prevention`
17. `file-structure-optimization`
18. `doc-maintenance`
19. `file-maintenance`
20. `project-backup`
21. `restore-drill`

## Trigger Matrix
| Skill | Primary Trigger | Typical Output |
|---|---|---|
| `skill-governance` | multi-skill or risk-sensitive tasks | selected mode + required gates + go/no-go |
| `governance-enforcement` | governance tooling, validators, CI policy checks | artifact generation/validation + enforcement pass/fail remediation |
| `requirement-clarifier` | ambiguous requests or missing acceptance criteria | clarified scope/assumptions/non-goals/acceptance contract |
| `semantic-policy-audit` | intent-level policy compliance review | expected-vs-observed skill/gate audit + gap classification |
| `thoughtful-approach` | feature planning requiring end-user expectation modeling | must-have/nice-to-have/deferred map + scope-safe enhancement decisions |
| `thoroughly-rate-review` | review/rate/score/assess/evaluate intent | weighted scoring model + category breakdown + final score + action plan |
| `user-instructions-tracker` | new directives, status tracking, fulfillment audit requests | updated `user-instructions.md` rows + status/evidence transitions |
| `history-indexing` | long-session context retrieval and indexing | `docs/chat-history-index.md` updates + targeted retrieval map |
| `ui-spatial-canvas` | frontend UI/UX architecture or redesign | no-scrollbar-first viewport interaction model + flow-level UX decisions |
| `ui-design-skills` | need a trusted-source UX principles framework | source-grounded design checklist + acceptance gates + references |
| `effective-testing-methods` | feature/behavior change requiring robust test updates | unit + Playwright change-to-test coverage map and quality gates |
| `scripted-command-execution` | deterministic shell/setup/batch tasks | executed command plan + validation |
| `pseudo-agentic-automation` | dynamic browser/GUI automation | script loop artifacts + pass/fail |
| `token-reduction` | long/expensive chats, concise-result preference | compressed context + concise result |
| `order-of-operations` | multi-step requests with dependencies | dependency-correct execution order |
| `regression-prevention` | risky code changes, upgrades, refactors | risk map + test evidence + release recommendation |
| `file-structure-optimization` | repo architecture drift or duplication risk | structure audit + consolidation/migration plan |
| `doc-maintenance` | behavior/workflow/config changes | updated docs + doc impact map |
| `file-maintenance` | file correctness/factuality/freshness maintenance needs | file accuracy audit + staleness/duplication remediation |
| `project-backup` | backup readiness, pre-risk safety | backup compliance state + gate decision |
| `restore-drill` | restore validation / DR simulation | drill evidence + pass/fail + gate status |

## Ownership Boundaries (Anti-Overlap)
Use this matrix to prevent process duplication.

1. `skill-governance` owns:
   - mode selection
   - required gate set
   - release recommendation policy
2. `order-of-operations` owns:
   - dependency-correct execution sequence
   - parallelization decisions
   - validation ordering
3. `regression-prevention` owns:
   - regression risk taxonomy and risk tier
   - release-readiness evidence standard
   - residual-risk classification
4. `effective-testing-methods` owns:
   - test impact mapping
   - unit and Playwright coverage expectations
   - test quality gates
5. `scripted-command-execution` owns:
   - deterministic command orchestration
   - retry policy
   - execution logs

Conflict rule:
1. if two skills appear to own the same decision, apply this ownership order:
   - policy (`skill-governance`) -> sequencing (`order-of-operations`) -> risk (`regression-prevention`) -> test design (`effective-testing-methods`) -> command execution (`scripted-command-execution`)

## Constrained Verification Protocol
When local environment limitations block required test layers (for example missing browser/system libraries):

1. capture blocker evidence precisely:
   - failing command
   - exact error line
   - blocked layer (`unit`, `integration`, `Playwright`, `build`)
2. execute fallback evidence path:
   - static checks
   - test discovery/listing
   - targeted non-browser checks
   - impacted test/spec updates
3. classify residual risk:
   - `low` if blocked layer is non-critical for touched behavior
   - `medium` if one critical layer is blocked but alternatives exist
   - `high` if critical user-flow/browser validation is blocked
4. never claim full regression safety when critical layers are blocked
5. produce explicit follow-up action:
   - what dependency must be installed
   - what exact command must be rerun

## Recommended Skill Ordering by Scenario

### Scenario A: Risky Code Change
1. `skill-governance`
2. `order-of-operations`
3. `project-backup`
4. `restore-drill` (freshness check or drill if stale)
5. `scripted-command-execution`
6. `regression-prevention`
7. `effective-testing-methods`
8. `doc-maintenance`
9. `file-maintenance` (if docs/policy surfaces changed)
10. `token-reduction` (throughout for communication discipline)

### Scenario B: Routine Deterministic Task
1. `skill-governance`
2. `order-of-operations`
3. `scripted-command-execution`
4. `doc-maintenance` (if docs impacted)
5. `token-reduction`

### Scenario C: Browser/GUI Heavy Automation
1. `skill-governance`
2. `order-of-operations`
3. `pseudo-agentic-automation`
4. `regression-prevention` (if validating release quality)
5. `doc-maintenance`
6. `token-reduction`

### Scenario D: Frontend Spatial Canvas Implementation (Any App)
1. `skill-governance`
2. `order-of-operations`
3. `thoughtful-approach`
4. `ui-design-skills`
5. `ui-spatial-canvas`
6. `regression-prevention`
7. `doc-maintenance`
8. `token-reduction`

### Scenario E: Product Feature Implementation (User-Centric)
1. `skill-governance`
2. `requirement-clarifier`
3. `order-of-operations`
4. `thoughtful-approach`
5. `regression-prevention`
6. `effective-testing-methods`
7. `doc-maintenance`
8. `file-maintenance`
9. `token-reduction`

### Scenario F: Quality Review and Rating
1. `thoroughly-rate-review`
2. `thoughtful-approach` (if end-user value is part of the judgment)
3. `semantic-policy-audit` (if intent-level compliance matters)
4. `skill-governance` (if release/risk implications exist)
5. `token-reduction`

### Scenario G: Backup/Recovery Hardening
1. `skill-governance`
2. `order-of-operations`
3. `project-backup`
4. `restore-drill`
5. `doc-maintenance`
6. `token-reduction`

### Scenario H: Instruction Audit and Fulfillment Tracking
1. `order-of-operations`
2. `user-instructions-tracker`
3. `doc-maintenance`
4. `skill-governance` (if release/risk/policy impacts exist)
5. `token-reduction`

### Scenario I: Governance Policy Enforcement
1. `skill-governance`
2. `governance-enforcement`
3. `semantic-policy-audit` (for intent-level correctness)
4. `doc-maintenance`
5. `token-reduction`

### Scenario J: Repo Structure and Documentation Hygiene
1. `order-of-operations`
2. `file-structure-optimization`
3. `doc-maintenance`
4. `file-maintenance`
5. `regression-prevention` (if structural moves affect runtime/test wiring)
6. `token-reduction`

## Conflict Resolution Rules
1. Safety-first skills override speed-first skills:
   - `project-backup`, `restore-drill`, `regression-prevention` take precedence over shortcuts.
2. Sequencing-first skills run before execution-heavy skills:
   - apply `order-of-operations` before `scripted-command-execution` or `pseudo-agentic-automation`.
3. Governance-first for ambiguous or risky tasks:
   - apply `skill-governance` to choose mode/gates before execution.
4. Documentation is part of completion:
   - if behavior/workflow changed, `doc-maintenance` must run before completion.
5. Communication compression cannot remove required safety evidence:
   - `token-reduction` must preserve mandatory validation outputs.
6. Deployment defaults:
   - no deployment actions without explicit user request.

## Fast Selection Heuristics
1. If task is risky, multi-step, or ambiguous: start with `skill-governance`.
2. If governance scripts/CI enforcement are in scope: add `governance-enforcement`.
3. If requirements are ambiguous: add `requirement-clarifier`.
4. If intent-level policy correctness must be audited: add `semantic-policy-audit`.
5. If task is deterministic and local with orchestration needs: choose `scripted-command-execution`.
6. If task requires live browser/GUI adaptation: choose `pseudo-agentic-automation`.
7. If request has many steps or questionable order: add `order-of-operations`.
8. If change is risky or broad: add `regression-prevention`.
9. If backups/restores are relevant: add `project-backup` and `restore-drill`.
10. If task requires end-user expectation modeling: add `thoughtful-approach`.
11. If user asks to review/rate/score/assess/evaluate quality: add `thoroughly-rate-review`.
12. If user gives directives or asks fulfillment/progress status: add `user-instructions-tracker`.
13. If long-history retrieval overhead exists: add `history-indexing`.
14. If task is frontend interaction/layout architecture: add `ui-spatial-canvas`.
15. If task needs trusted UX standards and cross-platform design heuristics: add `ui-design-skills`.
16. If features/behavior changed and tests must be amended or added: add `effective-testing-methods`.
17. If repository layout has drift/duplication or poor discoverability: add `file-structure-optimization`.
18. If file factuality/correctness/staleness maintenance is required: add `file-maintenance`.
19. If outputs are getting verbose or context is ballooning: add `token-reduction`.
20. If any behavior/process changed: add `doc-maintenance`.

## Completion Gate
A multi-skill task should not be considered complete until:
1. governance mode/gates were selected for risky or ambiguous work,
2. dependency-correct sequencing was followed,
3. required safety/quality gates passed,
4. docs were updated when relevant,
5. cross-skill triggers were validated against `docs/skill-index.md`,
6. final response includes concise outcome + required evidence.

## Canonical Routing Artifact
1. `docs/skill-index.md` is the authoritative cross-skill trigger index.
2. If `SKILL-MAP.md` and `docs/skill-index.md` differ, update both in the same change.
3. CI validator: `.codex/skills/skill-governance/scripts/validate_skill_order_sync.py`.
