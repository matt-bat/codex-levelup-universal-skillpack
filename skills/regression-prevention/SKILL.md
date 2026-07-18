---
name: regression-prevention
description: Implement or review non-trivial code changes while preserving contracts, repository conventions, user work, and affected behavior. Use for logic, refactors, dependencies, APIs, authentication, data, runtime, or tooling changes and for qualitative code review; exclude copy-only edits, explicit scoring requests, and test design that is fully owned by effective-testing-methods.
---

# Regression Prevention

## Mission

Produce the smallest coherent implementation that satisfies the task without breaking affected behavior.

## Operating Modes

1. `implement`: inspect, change, validate, and review the final diff.
2. `code_review`: perform read-only defect analysis with severity-ranked findings.
3. `release_readiness`: provide change-safety evidence to governance; governance owns the final release decision.

Never turn `code_review` into weighted scoring unless the user explicitly requests a score.

## Core Workflow

### 1. Preserve the baseline

1. Inspect repository status and existing user changes.
2. Do not overwrite, revert, reformat, or claim unrelated changes.
3. Capture relevant existing behavior and validation state.
4. Identify a rollback path proportional to the planned effect.

### 2. Discover the implementation context

1. Read repository instructions and nearby implementation patterns.
2. Trace direct callers, data paths, contracts, and user-visible consumers.
3. Reuse established naming, types, error semantics, and abstractions.
4. Identify the exact behavior that must change and remain stable.

Read [implementation-quality.md](references/implementation-quality.md) for detailed construction and final-diff checks.

### 3. Classify effects

Classify actual planned effects—not topic keywords:

1. `local_low`: isolated, reversible local behavior
2. `local_significant`: multi-module or compatibility-sensitive behavior
3. `external_reversible`: authorized external state with tested rollback
4. `external_irreversible`: destructive, migratory, or uncertain recovery

Authentication or migration source code requires domain review. Backup and restore gates activate only when an operation exposes external state or data-loss risk.

### 4. Implement a coherent slice

1. Prefer the simplest implementation that fits existing architecture.
2. Keep behavior changes separate from unrelated cleanup.
3. Preserve interfaces unless a migration is explicitly authorized.
4. Handle failure paths and invalid states deliberately.
5. Add comments only for non-obvious rationale.

### 5. Select validation by changed surface

Use the cheapest layer that can prove the affected behavior, then expand by risk:

1. static/type/lint checks for relevant source
2. unit tests for deterministic logic
3. integration/contract tests for changed boundaries
4. browser tests only for changed browser-visible flows
5. runtime smoke checks only when an executable path changed

Use [Effective Testing Methods](../effective-testing-methods/SKILL.md) when tests must be designed or changed. A missing or blocked layer raises residual risk; it does not justify an unrelated substitute.

### 6. Review the final diff

1. Confirm every changed line serves an authorized requirement.
2. Detect accidental formatting churn, dead code, duplicated logic, and stale references.
3. Re-check contracts, types, error paths, security boundaries, and performance-sensitive paths where applicable.
4. Reconcile every deliverable and prohibition.

### 7. Report evidence honestly

Report commands run, material results, skipped checks, residual risk, and rollback notes. Never claim `no regressions`, `verified`, or `release-ready` beyond the evidence.

## Code Review Mode

For read-only review:

1. inspect the diff and relevant surrounding code
2. prioritize correctness, security, data loss, compatibility, and missing tests
3. report findings by severity with file references and concrete impact
4. distinguish proven defects from questions or suggestions
5. state when no material findings were found and identify residual test gaps

Read [code-review.md](references/code-review.md) for the review checklist.

## Compatibility and Migration

For API, schema, event, dependency, or persisted-data changes, read [compatibility-and-migrations.md](references/compatibility-and-migrations.md).

## Safety Boundaries

1. Activating this skill grants no mutation, command, commit, push, migration, deployment, or release authority.
2. Respect explicit validation ownership and prohibitions.
3. Unknown critical effects fail closed.
4. External or irreversible actions require independent safety gates.

## Output Contract

For implementation, provide:

1. affected behavior and implementation summary
2. validation evidence
3. residual risk and rollback notes

For code review, provide severity-ranked findings first, then questions and residual coverage gaps.

## Quality Gates

1. Repository conventions and existing user changes were preserved.
2. The implementation is minimal and system-complete.
3. Changed contracts and failure paths were checked.
4. Validation matches the actual changed surface.
5. The final diff contains no unauthorized or unexplained work.

## Related Skills

- [Diagnose Before Fix](../diagnose-before-fix/SKILL.md): verify an uncertain root cause before implementation.
- [Effective Testing Methods](../effective-testing-methods/SKILL.md): design or amend tests.
- [Interdependent Change Planning](../interdependent-change-planning/SKILL.md): coordinate coupled surfaces.
- [Skill Governance](../skill-governance/SKILL.md): own governed mode, gates, and release recommendation.
