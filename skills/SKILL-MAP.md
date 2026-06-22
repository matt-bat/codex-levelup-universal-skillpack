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
7. Quizme clarification mode:
   - `--quizme` toggles persistent conversation-local clarification mode on/off
   - supported immediate arguments are `--mc`, `--one-at-a-time`, `--confirm`, and `--record`
   - when active, apply `quizme-mode` before substantive execution

## Minimum Viable Skill Use
Use the smallest skill set that satisfies the request and safety requirements.

| Task Shape | Maximum Default Skill Set |
|---|---|
| Answer-only request | `token-reduction` |
| One deterministic local command | `token-reduction`, `scripted-command-execution` |
| Tiny isolated text edit | `token-reduction`, `order-of-operations` |
| Small isolated code edit | `token-reduction`, `order-of-operations`, `scripted-command-execution`, optional `regression-prevention` |
| Documentation-only update | `token-reduction`, `order-of-operations`, `doc-maintenance` |
| Governed or release-affecting change | `token-reduction`, `order-of-operations`, `skill-governance`, required gates |

Stop rules:
1. add a skill only when it changes execution, validation, safety, or documentation evidence
2. prefer one owner when skills overlap
3. avoid history/cache skills unless the task explicitly needs retained context or artifact budgets
4. avoid governance artifacts for tiny isolated non-governed changes

## Skill Index
1. `skill-governance`
2. `process-budget-controller`
3. `governance-enforcement`
4. `requirement-clarifier`
5. `quizme-mode`
6. `diagnose-before-fix`
7. `semantic-policy-audit`
8. `interdependent-change-planning`
9. `thoughtful-approach`
10. `thoroughly-rate-review`
11. `user-instructions-tracker`
12. `history-indexing`
13. `conversation-retention-summary`
14. `ui-spatial-canvas`
15. `ui-design-skills`
16. `effective-testing-methods`
17. `scripted-command-execution`
18. `pseudo-agentic-automation`
19. `token-reduction`
20. `artifact-budget-enforcement`
21. `order-of-operations`
22. `regression-prevention`
23. `file-structure-optimization`
24. `doc-maintenance`
25. `file-maintenance`
26. `skill-usage-review`
27. `deprecation-management`
28. `project-backup`
29. `restore-drill`

## Trigger Matrix
| Skill | Primary Trigger | Typical Output |
|---|---|---|
| `skill-governance` | multi-skill or risk-sensitive tasks | selected mode + required gates + go/no-go |
| `process-budget-controller` | multiple skills could apply and process needs explicit caps | process tier + max skill count + artifact allowance |
| `governance-enforcement` | governance tooling, validators, CI policy checks | artifact generation/validation + enforcement pass/fail remediation |
| `requirement-clarifier` | ambiguous requests or missing acceptance criteria | clarified scope/assumptions/non-goals/acceptance contract |
| `quizme-mode` | `--quizme` invoked or persistent quizme state active | interactive clarification rounds + aligned task contract before execution |
| `diagnose-before-fix` | bug reports or failures with unverified causes | symptom vs cause verification + verified root cause or safe mitigation |
| `semantic-policy-audit` | intent-level policy compliance review | expected-vs-observed skill/gate audit + gap classification |
| `interdependent-change-planning` | changes that touch connected system parts | coupled-surface map + coherent update plan |
| `thoughtful-approach` | feature planning requiring end-user expectation modeling | must-have/nice-to-have/deferred map + scope-safe enhancement decisions |
| `thoroughly-rate-review` | review/rate/score/assess/evaluate intent | weighted scoring model + category breakdown + final score + action plan |
| `user-instructions-tracker` | new directives, status tracking, fulfillment audit requests | updated `user-instructions.md` rows + status/evidence transitions |
| `history-indexing` | long-session context retrieval and indexing | `docs/chat-history-index.md` updates + targeted retrieval map |
| `conversation-retention-summary` | rolling summary of the last 10 conversations | `docs/chat-history-summary.md` updates + refresh/trim logic |
| `ui-spatial-canvas` | frontend UI/UX architecture or redesign | no-scrollbar-first viewport interaction model + flow-level UX decisions |
| `ui-design-skills` | need a trusted-source UX principles framework | source-grounded design checklist + acceptance gates + references |
| `effective-testing-methods` | feature/behavior change requiring robust test updates | unit + Playwright change-to-test coverage map and quality gates |
| `scripted-command-execution` | deterministic shell/setup/batch tasks | executed command plan + validation |
| `pseudo-agentic-automation` | dynamic browser/GUI automation | script loop artifacts + pass/fail |
| `token-reduction` | long/expensive chats, concise-result preference | compressed context + concise result |
| `artifact-budget-enforcement` | cached artifacts or summaries need hard limits | caps, pruning rules, and trimmed artifact evidence |
| `order-of-operations` | multi-step requests with dependencies | dependency-correct execution order |
| `regression-prevention` | risky code changes, upgrades, refactors | risk map + test evidence + release recommendation |
| `file-structure-optimization` | repo architecture drift or duplication risk | structure audit + consolidation/migration plan |
| `doc-maintenance` | behavior/workflow/config changes | updated docs + doc impact map |
| `file-maintenance` | file correctness/factuality/freshness maintenance needs | file accuracy audit + staleness/duplication remediation |
| `skill-usage-review` | recent task evidence should be reviewed for skill overuse, underuse, or friction | usage findings + process improvement recommendations |
| `deprecation-management` | skills, docs, or workflows are superseded, merged, renamed, discouraged, or removed | deprecation state + replacement path + migration criteria |
| `project-backup` | backup readiness, pre-risk safety | backup compliance state + gate decision |
| `restore-drill` | restore validation / DR simulation | drill evidence + pass/fail + gate status |

## Ownership Boundaries (Anti-Overlap)
Use this matrix to prevent process duplication.

1. `quizme-mode` owns:
   - conversation-local toggle state
   - exact immediate argument handling for `--mc`, `--one-at-a-time`, `--confirm`, and `--record`
   - pre-execution clarification gate
2. `skill-governance` owns:
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
   - explicit quizme clarification gate (`quizme-mode`) -> process cap (`process-budget-controller`) -> policy (`skill-governance`) -> sequencing (`order-of-operations`) -> risk (`regression-prevention`) -> test design (`effective-testing-methods`) -> command execution (`scripted-command-execution`)

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

### Scenario K: Debugging and Root Cause Verification
1. `skill-governance`
2. `order-of-operations`
3. `diagnose-before-fix`
4. `regression-prevention`
5. `effective-testing-methods`
6. `scripted-command-execution`
7. `doc-maintenance`
8. `token-reduction`

### Scenario L: Recent Memory and Cache Boundedness
1. `order-of-operations`
2. `history-indexing`
3. `conversation-retention-summary`
4. `artifact-budget-enforcement`
5. `file-maintenance`
6. `token-reduction`

### Scenario M: Persistent Quizme Clarification
1. `quizme-mode`
2. `requirement-clarifier`
3. `skill-governance` (if risk, release, or policy impact exists)
4. task-specific skills only after the clarification gate passes

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
7. Quizme precedence:
   - when quizme mode is active, `quizme-mode` blocks substantive execution until clarification is complete.

## Fast Selection Heuristics
1. If task is risky, multi-step, or ambiguous: start with `skill-governance`.
2. If governance scripts/CI enforcement are in scope: add `governance-enforcement`.
3. If requirements are ambiguous: add `requirement-clarifier`.
4. If `--quizme` is invoked or remains active: add `quizme-mode` before substantive execution.
5. If intent-level policy correctness must be audited: add `semantic-policy-audit`.
6. If task is deterministic and local with orchestration needs: choose `scripted-command-execution`.
7. If task requires live browser/GUI adaptation: choose `pseudo-agentic-automation`.
8. If request has many steps or questionable order: add `order-of-operations`.
9. If change is risky or broad: add `regression-prevention`.
10. If backups/restores are relevant: add `project-backup` and `restore-drill`.
11. If task requires end-user expectation modeling: add `thoughtful-approach`.
12. If user asks to review/rate/score/assess/evaluate quality: add `thoroughly-rate-review`.
13. If user gives directives or asks fulfillment/progress status: add `user-instructions-tracker`.
14. If long-history retrieval overhead exists: add `history-indexing`.
15. If the request needs a bounded rolling summary of the last 10 conversations: add `conversation-retention-summary`.
16. If cached artifacts or metadata need hard size limits: add `artifact-budget-enforcement`.
17. If task is frontend interaction/layout architecture: add `ui-spatial-canvas`.
18. If task needs trusted UX standards and cross-platform design heuristics: add `ui-design-skills`.
19. If features/behavior changed and tests must be amended or added: add `effective-testing-methods`.
20. If repository layout has drift/duplication or poor discoverability: add `file-structure-optimization`.
21. If file factuality/correctness/staleness maintenance is required: add `file-maintenance`.
22. If outputs are getting verbose or context is ballooning: add `token-reduction`.
23. If any behavior/process changed: add `doc-maintenance`.

## Completion Gate
A multi-skill task should not be considered complete until:
1. active `quizme-mode` clarification finished before substantive execution,
2. governance mode/gates were selected for risky or ambiguous work,
3. dependency-correct sequencing was followed,
4. required safety/quality gates passed,
5. docs were updated when relevant,
6. cross-skill triggers were validated against `docs/skill-index.md`,
7. final response includes concise outcome + required evidence.

## Canonical Routing Artifact
1. `docs/skill-index.md` is the authoritative cross-skill trigger index.
2. If `SKILL-MAP.md` and `docs/skill-index.md` differ, update both in the same change.
3. CI validator: `skills/skill-governance/scripts/validate_skill_order_sync.py`.
