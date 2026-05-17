---
name: regression-prevention
description: Use for planning and executing code changes with strict regression controls, including risk scoring, test impact analysis, compatibility checks, release gates, and rollback readiness.
---

# Regression Prevention

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Core Principles`
3. `Trigger Examples`
4. `Regression Taxonomy`

### Action Modules (Read As Needed)
1. Planning and risk setup:
   - `Required Workflow` Step 1-5
   - `Dependency Update Rules`
   - `Database and Migration Safety`
2. Validation execution:
   - `Required Workflow` Step 6-10
   - `Frontend Regression Controls`
   - `Backend Regression Controls`
3. Evidence and release decisions:
   - `PR/Change Checklist Template`
   - `Minimum Evidence Standard`
   - `Deliverable Format`

### Failure & Escalation
1. `Escalation Conditions`
2. `Anti-Patterns to Avoid`

## Mission
Ship changes without breaking existing behavior, data integrity, performance, or operational stability.

Use this skill for any non-trivial change (features, refactors, upgrades, schema/API/runtime/tooling changes).

## Core Principles
1. Preserve existing behavior unless change is explicitly requested.
2. Detect breakage early with layered checks (static, unit, integration, E2E, runtime).
3. Require proof before confidence: every assumption must be validated by a check or a test.
4. Prefer reversible changes over hard-to-undo changes.
5. Never rely on "it should be fine" for risky updates.

## Trigger Examples
Apply when users ask for changes that must preserve existing behavior and reliability.

## Non-Goals
Does not replace product decision-making, incident response, or dedicated security review.

## Regression Taxonomy
Classify risk before implementation:

1. Functional regressions:
- existing user flows fail
- outputs differ unexpectedly
- state transitions break

2. Data regressions:
- schema mismatches
- lost/duplicated records
- incorrect migrations
- serialization/deserialization breakage

3. Contract regressions:
- API request/response incompatibility
- changed status codes
- header/cookie/session contract changes
- event payload changes

4. UX regressions:
- navigation breaks
- accessibility regressions
- mobile layout breakage
- broken forms/interactions

5. Performance regressions:
- slower endpoint/page latency
- increased memory/CPU usage
- larger bundle/build artifacts

6. Operational regressions:
- deploy/startup failures
- missing env/runtime dependencies
- broken jobs/workers/webhooks
- logging/observability blind spots

For small/low-risk changes, this taxonomy can be captured in compact form (affected categories only).

## Required Workflow
Follow in order.

### Step 1: Baseline Capture (Before Changes)
Record current behavior first.

Minimum baseline:
1. Current branch status and uncommitted work.
2. Existing test results (or explicit gaps if tests unavailable).
3. Key runtime smoke checks for core flows.
4. Current API/CLI/UI behaviors that must remain stable.
5. Current performance snapshots for high-risk paths (if relevant).

Output required:
- A short "baseline checkpoint" note listing:
  - what was checked
  - what passed
  - what is untested and risky

### Step 2: Change Impact Mapping

For each touched module:
1. Identify direct callers.
2. Identify transitive dependencies.
3. Identify contracts (API, schema, events, files, env vars).
4. Identify user-visible surfaces.
5. Identify jobs/background tasks/webhooks impacted.

Mandatory artifact:
- Impact map with:
  - touched files
  - affected flows
  - required validation scope

### Step 3: Risk Scoring
Assign a risk level before editing.

Low risk:
- isolated text/style copy change
- no contract/data impact

Medium risk:
- logic changes in non-critical path
- small dependency update
- internal refactor

High risk:
- auth/session changes
- payment/order/financial logic
- DB schema/migrations
- API contract changes
- large dependency/runtime upgrades
- concurrency/state management changes

Risk gates:
1. Low: unit/smoke checks required.
2. Medium: unit + integration + targeted E2E required.
3. High: full regression pass + rollback plan required.

If tests are missing in a required layer:
1. create temporary targeted checks (scripted smoke/contract checks),
2. record the gap explicitly,
3. mark residual risk as elevated,
4. avoid claiming regression-safe coverage.

Blocking rule:
1. high-risk changes with missing critical validation layers must not be marked release-ready
2. proceed only with explicit risk acceptance and remediation plan

### Step 4: Guardrail Design (Before Coding)
Define safeguards before edits.

Possible safeguards:
- feature flags
- backward-compatible adapters
- dual-write/dual-read strategies
- deprecation windows
- schema expand-then-contract approach
- kill switches for risky behavior

For high-risk changes, require at least one explicit rollback mechanism.

### Step 5: Implement in Small, Verifiable Slices
Do not batch unrelated risky changes.

Rules:
1. Keep changes scoped.
2. Validate after each slice.
3. Avoid mixed refactor + behavior changes in one step when possible.
4. Preserve interfaces until migration path is complete.

### Step 6: Regression Test Matrix
Use layered validation; do not rely on one test type.

Required matrix:
1. Static checks:
- type checks/lint/format consistency checks

2. Unit tests:
- pure logic and edge cases

3. Integration tests:
- service boundaries (DB/API/external mocks)

4. E2E/smoke:
- user-critical flows
- happy path + at least one failure path

5. Contract checks:
- response shape/status invariants
- backward compatibility checks

6. Data checks:
- migration up/down where possible
- integrity assertions for modified models

7. Operational checks:
- app starts cleanly
- key routes/commands work
- no missing env vars/runtime errors

### Step 6A: Unit Tests vs Playwright
Use [Effective Testing Methods](../effective-testing-methods/SKILL.md) for detailed patterns when amending or adding unit and Playwright tests.

Use both; they protect different failure modes.

Unit tests are for:
1. pure business logic
2. edge-case branching
3. deterministic fast feedback
4. preventing localized logic regressions

Playwright tests are for:
1. real browser rendering and interaction regressions
2. route/navigation/form flows
3. auth/session/cookie behavior from user perspective
4. integration issues between frontend/backend at runtime boundaries

Rules:
1. Unit tests do not replace Playwright for user-flow validation.
2. Playwright does not replace unit tests for exhaustive logic branching.
3. Run fast layers first (static + unit + integration), then Playwright.
4. Fail early: do not spend E2E time if foundational checks are red.

Recommended sequence:
1. static/type/lint
2. unit tests
3. integration/contract tests
4. Playwright targeted regression tests
5. Playwright full suite for high-risk or broad-impact changes

Playwright execution scope policy:
1. UI-only low-risk change: targeted route test set
2. medium-risk frontend logic change: targeted + neighboring route tests
3. auth/navigation/session change: full critical-flow Playwright pass
4. high-risk release candidate: full Playwright matrix (desktop/mobile where applicable)

Artifact policy for Playwright:
1. persist trace/video/screenshot artifacts on failure
2. include failing URL, selector context, and test name in evidence
3. treat flaky tests as unresolved risk until triaged

Flake handling:
1. allow one controlled retry for diagnostics
2. if retry passes, mark as flaky-suspect and log
3. if retry fails again, treat as hard failure

### Step 6C: Constrained-Environment Adaptation
If a required layer cannot run because of host/runtime constraints:

1. capture blocker evidence:
   - command
   - exact error
   - missing dependency/runtime constraint
2. execute fallback checks:
   - static/type/lint
   - test discovery/listing for blocked suites
   - available non-blocked regression checks
3. update impacted tests/specs anyway (do not defer test updates solely because execution is blocked)
4. classify residual risk as elevated for blocked critical layers
5. provide exact rerun command for full validation once dependency is available

Reference:
- `.codex/skills/docs/verification/constrained-environment-verification.md`

### Step 6B: Coverage Mapping Artifact (Required for Medium/High Risk)
Create a change-to-test map:
1. changed module/route
2. impacted behavior
3. unit tests covering logic
4. integration/contract tests covering boundaries
5. Playwright specs covering user flow
6. remaining untested risk

### Step 7: Negative and Edge-Case Validation

Minimum edge-case checks:
1. invalid inputs
2. unauthorized access
3. empty/null/absent data
4. duplicate/retry behavior
5. timeout/external service failure behavior

### Step 8: Compatibility Rules
For APIs, data, and events, preserve compatibility unless explicitly approved.

Rules:
1. Additive changes preferred over destructive changes.
2. Do not silently rename/remove fields without migration path.
3. Keep old consumers functioning during transition.
4. Document compatibility breaks with explicit dates and mitigation.

### Step 9: Release Readiness Gate
Before considering complete, verify:
1. Risk-tier checks passed.
2. Critical flows pass.
3. Observability is sufficient (errors/logging/metrics for changed paths).
4. Rollback plan is documented and actionable.
5. Known residual risks are listed explicitly.

### Step 10: Post-Change Verification
After merge/deploy (or local equivalent), run:
1. immediate smoke checks
2. targeted regression checks for changed flows
3. quick scan of logs/errors for new anomalies
4. document observed deviations and owner for follow-up

## Dependency Update Rules
Checklist:
1. Read release notes/changelogs for breaking changes.
2. Upgrade smallest necessary scope first.
3. Avoid simultaneous major upgrades unless required.
4. Re-run full affected test matrix after upgrade.
5. Validate runtime startup and critical paths.
6. Document behavior changes introduced by dependency updates.

For major version upgrades:
1. create a compatibility checklist
2. identify removed APIs/features
3. patch incrementally
4. run full regression suite

## Database and Migration Safety
For any schema/data updates:
1. Prefer expand-then-contract migration strategy.
2. Never assume data shape quality; validate existing rows.
3. Add default/backfill strategy for new required columns.
4. Ensure read paths handle both old/new states during rollout.
5. Test migration with representative data volume when possible.
6. Verify rollback path (or explicit non-reversible documentation).

## Frontend Regression Controls
When UI is changed:
1. Validate desktop/mobile layout, keyboard/focus, and route transitions.
2. Validate loading/error/empty states.
3. Re-run E2E route smoke checks.
4. Ensure unit/component and Playwright coverage for impacted flows.

## Backend Regression Controls
When backend is changed:
1. Validate auth boundaries, status/error contracts, and idempotency.
2. Validate external failure handling and serialization/deserialization.
3. Ensure behavior changes are reflected in integration/contract tests used by frontend flows.

## PR/Change Checklist Template
Use this checklist for every non-trivial update:

- [ ] Baseline captured
- [ ] Impact map created
- [ ] Risk tier assigned
- [ ] Guardrails selected (feature flag/rollback/adapter)
- [ ] Tests added/updated for changed behavior
- [ ] Edge/failure paths validated
- [ ] Compatibility verified
- [ ] Release gate passed
- [ ] Post-change verification plan documented

## Minimum Evidence Standard
Do not claim "no regression" without evidence.

Evidence must include:
1. commands/checks run
2. key pass/fail outcomes
3. any skipped checks and why
4. residual risk statement

## Escalation Conditions
Stop and escalate if:
1. baseline cannot be established
2. high-risk change lacks rollback
3. critical tests cannot run
4. compatibility impact is unknown
5. behavior differences appear without clear explanation

## Anti-Patterns to Avoid
1. Large multi-domain refactors without intermediate validation.
2. Changing behavior and contracts in same step without compatibility layer.
3. Upgrading many dependencies at once with no isolation.
4. Assuming test coverage equals regression safety.
5. Skipping negative-path validation.

Compact-mode note:
1. keep evidence compact, but never omit risk tier, validation scope, or release recommendation.

## Deliverable Format
When using this skill, produce outputs in this order:
1. Risk summary
2. Impact map
3. Validation plan
4. Changes made
5. Evidence from checks/tests
6. Residual risks + rollback notes
7. explicit release recommendation (`go`, `go-with-risk`, `no-go`)

Validation plan must explicitly list:
1. unit-test scope
2. integration/contract scope
3. Playwright scope (targeted vs full)
4. rationale for any omitted layer

## Related Skills
- [Effective Testing Methods](../effective-testing-methods/SKILL.md): detailed unit and Playwright implementation guidance for changed behavior.
- [Scripted Command Execution](../scripted-command-execution/SKILL.md): deterministic command workflows for running checks, scripts, and release gates.
- [Pseudo-Agentic Automation](../pseudo-agentic-automation/SKILL.md): browser/GUI-intensive validation when deterministic checks are insufficient.
- [Order of Operations](../order-of-operations/SKILL.md): enforce dependency-correct sequencing for risky multi-step changes.
- [Doc Maintenance](../doc-maintenance/SKILL.md): keep regression plans, runbooks, and release notes aligned with implemented behavior.
