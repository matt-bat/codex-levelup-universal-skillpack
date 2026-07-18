---
name: effective-testing-methods
description: Design, add, or amend tests for changed behavior with surface-appropriate coverage. Use when test design or test-file changes are part of the task; do not activate merely to run an existing test command, and use Playwright only when a browser-visible flow changed.
---

# Effective Testing Methods

## Mission

Create the smallest reliable test set that proves changed behavior and meaningful failure paths.

## Scope Boundary

This skill owns test selection and test implementation quality. It does not own overall change risk, command orchestration, or release decisions.

Use:

1. [Regression Prevention](../regression-prevention/SKILL.md) for implementation and change-safety evidence.
2. [Scripted Command Execution](../scripted-command-execution/SKILL.md) for repeatable test command workflows.

Running existing tests does not automatically activate this skill.

## Test Impact Map

Before editing tests, identify:

1. changed behavior or contract
2. relevant existing tests
3. important success, failure, and edge paths
4. the cheapest layer that observes the behavior
5. residual behavior that cannot be exercised locally

## Surface-Driven Layer Selection

Select only applicable layers:

1. `static`: types, schemas, lint, or compile-time contracts
2. `unit`: deterministic logic and boundary cases
3. `integration`: database, service, file, process, or API boundaries
4. `contract`: request/response, event, serialization, and compatibility
5. `browser`: user-visible rendering and interaction in a web application
6. `runtime_smoke`: executable startup or critical operational path

Playwright is allowed only when a browser-visible flow changed or explicit browser verification was requested. Command-line, library, backend-only, documentation, and policy work must not acquire a browser requirement.

## Test Construction Rules

1. Test observable behavior rather than incidental implementation details.
2. Prefer focused deterministic cases over broad brittle scenarios.
3. Include negative and failure cases proportional to risk.
4. Control time, randomness, network, and global state.
5. Reuse existing fixtures and repository conventions.
6. Ensure each test fails for the intended reason before trusting it.

Read [test-patterns.md](references/test-patterns.md) for unit, integration, contract, and browser patterns.

## Execution Order

Run the cheapest relevant checks first:

1. static or compile checks
2. unit tests
3. integration and contract tests
4. targeted browser or runtime checks
5. broader suites only when impact or release policy requires them

If a prerequisite is unavailable, record the exact blocker, run non-blocked relevant layers, and provide the precise rerun command. Never substitute an unrelated passing layer for a blocked critical layer.

## Authority and Artifact Policy

1. Activating this skill grants no authority to run, create, or modify tests.
2. Respect explicit instructions not to run or modify tests.
3. Test-authoring permission does not imply permission to install dependencies or mutate external state.
4. Report executed, skipped, blocked, and newly authored coverage separately.
5. Do not claim full coverage from test discovery or static inspection alone.

## Output Contract

Provide:

1. behavior-to-test map
2. tests added or amended by applicable layer
3. execution results
4. blocked or residual coverage

## Quality Gates

1. Every test maps to changed or explicitly protected behavior.
2. No irrelevant layer was required.
3. Browser tests exist only for browser behavior.
4. Failure paths and compatibility boundaries receive proportional coverage.
5. Evidence distinguishes authored, executed, and blocked validation.

## Related Skills

- [Regression Prevention](../regression-prevention/SKILL.md): implementation and final-diff safety.
- [Scripted Command Execution](../scripted-command-execution/SKILL.md): deterministic test execution.
- [Pseudo-Agentic Automation](../pseudo-agentic-automation/SKILL.md): adaptive browser or graphical runtime work.
