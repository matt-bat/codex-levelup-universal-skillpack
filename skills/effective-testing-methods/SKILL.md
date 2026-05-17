---
name: effective-testing-methods
description: Use for implementing or amending unit tests and Playwright tests when features or behavior change, ensuring updates are validated with robust, maintainable test coverage.
---

# Effective Testing Methods

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Use This Skill When`
3. `Scope Boundary`
4. `Core Principles`

### Action Modules (Read As Needed)
1. Test planning and selection:
   - `Test Impact Mapping`
   - `Layer Selection Rules`
2. Unit test implementation:
   - `Unit Test Patterns`
   - `Unit Test Quality Gates`
3. Playwright implementation:
   - `Playwright Patterns`
   - `Playwright Stability Gates`
4. Validation and evidence:
   - `Execution Order`
   - `Constrained Environment Verification Path`
   - `Coverage-to-Change Map`
   - `Acceptance Checklist`

### Output
1. `Deliverable Format`
2. `Anti-Patterns`

## Mission
Ensure every feature addition or behavior change is accompanied by targeted, reliable unit and browser-level Playwright coverage.

## Use This Skill When
1. implementing new features or modifying existing behavior
2. fixing regressions that need durable test coverage
3. changing UI flows for web applications that require user-path verification
4. changing business logic requiring deterministic unit test updates

## Scope Boundary
This skill governs test implementation quality and test-change completeness.

Use [Regression Prevention](../regression-prevention/SKILL.md) for:
1. risk-tier policy and release gates
2. rollback and risk acceptance decisions

Use [Scripted Command Execution](../scripted-command-execution/SKILL.md) for:
1. deterministic test command orchestration

## Core Principles
1. test behavior, not implementation trivia
2. keep unit tests fast and deterministic
3. keep Playwright tests user-centric and resilient
4. map each meaningful code change to at least one validating test
5. prefer small focused tests over brittle mega-tests

## Test Impact Mapping
Before writing tests, map:
1. changed module/route
2. user-visible behavior affected
3. logic branches introduced or modified
4. contracts/states that can fail
5. existing tests to reuse or amend

## Layer Selection Rules
1. always update/add unit tests for changed business logic
2. add or amend Playwright for changed user flows in web apps
3. include integration/contract checks when boundaries changed
4. avoid using Playwright as a substitute for branch-level unit coverage

Recommended default split:
1. broad unit coverage for logic edges
2. targeted Playwright coverage for critical user flows

## Unit Test Patterns
1. arrange-act-assert structure with explicit fixtures
2. one behavioral intent per test case
3. table-driven tests for branch-heavy logic
4. explicit edge-case and error-path tests
5. no hidden dependencies on global state or test order

## Unit Test Quality Gates
1. deterministic outcomes across repeated runs
2. no network/time randomness without explicit control
3. meaningful names that describe behavior
4. assertions reflect observable outcomes
5. tests fail for the right reason (avoid broad catch-all assertions)

## Playwright Patterns
1. prefer role/text/test-id locators over brittle CSS/XPath selectors
2. validate user-visible states and critical transitions
3. isolate tests with clean state per test/spec where possible
4. use web-first assertions and built-in auto-waiting behavior
5. keep page object abstractions small and intent-focused

## Playwright Stability Gates
1. no fixed sleeps when reliable waits/assertions are possible
2. avoid third-party dependency assertions outside your control
3. capture trace/artifacts on failure for triage
4. verify at least one failure-path scenario for critical flows
5. keep authentication/session setup explicit and reusable

## Execution Order
1. run static checks and unit tests first
2. run integration/contract tests next
3. run targeted Playwright tests next
4. run expanded Playwright matrix for high-risk changes

## Constrained Environment Verification Path
Use this path when required test layers are blocked by environment constraints (for example missing browser/system libraries).

Required actions:
1. record blocker evidence:
   - command attempted
   - exact error line
   - blocked layer
2. keep moving with non-blocked layers:
   - static checks
   - unit/integration checks (if available)
   - Playwright test discovery/listing
3. still update impacted tests/specs:
   - ensure changed behavior is reflected in test files even if execution is blocked
4. publish residual-risk classification:
   - `medium` when non-critical browser checks are blocked
   - `high` when critical user-flow browser checks are blocked
5. provide explicit rerun command for full verification when environment is fixed

Reference runbook:
- `.codex/skills/docs/verification/constrained-environment-verification.md`

## Coverage-to-Change Map
For medium/high-risk changes, provide:
1. changed component/logic
2. unit tests added or amended
3. Playwright specs added or amended
4. uncovered residual risks

## Acceptance Checklist
1. changed logic has updated unit coverage
2. changed web user flow has updated Playwright coverage
3. critical paths pass in CI/local validation
4. flaky behavior is identified and mitigated
5. evidence links exist for new/updated tests
6. when layers are blocked, blocker evidence + rerun plan is included

## Deliverable Format
When applying this skill, provide:
1. change-to-test impact map
2. tests added/updated by layer
3. execution results summary
4. residual testing risks and follow-up actions

## Source Reference
Primary references:
1. Playwright best practices:
   - https://playwright.dev/docs/best-practices
2. Google testing strategy guidance:
   - https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html
3. MIT software construction testing principles:
   - https://ocw.mit.edu/courses/6-005-software-construction-spring-2016/

## Anti-Patterns
1. shipping behavior changes without test updates
2. relying only on manual QA for changed critical paths
3. brittle Playwright selectors tied to incidental DOM details
4. over-mocking away the behavior under test
5. asserting internals instead of outcomes

## Related Skills
- [Regression Prevention](../regression-prevention/SKILL.md): risk-tier regression policy and release gating.
- [Scripted Command Execution](../scripted-command-execution/SKILL.md): deterministic test run orchestration.
- [Doc Maintenance](../doc-maintenance/SKILL.md): synchronize test docs and run commands.
- [File Maintenance](../file-maintenance/SKILL.md): keep testing docs and evidence accurate over time.
