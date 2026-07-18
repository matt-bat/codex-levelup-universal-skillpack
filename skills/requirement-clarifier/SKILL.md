---
name: requirement-clarifier
description: Convert materially ambiguous or conflicting requests into a typed task contract before mutation. Use when uncertainty could change user-visible behavior, compatibility, security, data handling, authorization, or acceptance criteria; do not use for clear bounded work or to force clarification of harmless implementation details.
---

# Requirement Clarifier

## Mission

Prevent misbuilds without turning ordinary work into an interview.

## Activation Boundary

Activate only when at least one unresolved choice could materially change:

1. the requested deliverable
2. an authorization or prohibited action
3. user-visible behavior or compatibility
4. security, privacy, or data handling
5. an acceptance criterion

For low-impact uncertainty, record one bounded assumption and continue. When `quizme-mode` is active, keep clarifying until the contract is complete.

## Task Contract

Track these fields for each deliverable:

1. `goal`
2. `in_scope`
3. `out_of_scope`
4. `acceptance_criteria`
5. `constraints`
6. `prohibitions`
7. `authority`
8. `assumptions`
9. `material_uncertainties`

Classify every requirement source as:

1. `explicit_user`
2. `higher_priority_policy`
3. `repository_policy`
4. `necessary_implication`
5. `bounded_assumption`
6. `optional_enhancement`

Never present an assumption or enhancement as an explicit user requirement.

## Precedence and Conflict Rules

1. Follow higher-priority instructions before lower-priority instructions.
2. Prefer the newest valid user directive over stale repository notes.
3. Preserve explicit prohibitions and authorization boundaries verbatim.
4. If two valid instructions conflict materially, pause and ask one focused question.
5. If the conflict is harmless, choose the narrowest reversible interpretation and record it.

## Materiality Gate

Ask only when uncertainty could cause meaningful rework, risk, or a different product outcome.

Always clarify before:

1. destructive or irreversible action with uncertain scope
2. external communication or publication with uncertain authority
3. a security or compatibility tradeoff the user did not choose
4. selecting among materially different product behaviors

## Requirement Trace

Before completion, map every deliverable and acceptance criterion to exactly one status:

1. `satisfied`
2. `verified`
3. `unverified` with reason
4. `deferred` with authorization
5. `blocked` with blocker

No requirement may disappear during planning, implementation, or response composition.

For complex or multi-deliverable work, read [task-contract-schema.md](references/task-contract-schema.md).

## Artifact and Authority Policy

Keep the contract conversation-local by default. Write it to the repository only when:

1. the user requests recording
2. `--quizme --record` is active
3. an authorized governed workflow requires a durable contract

Activating this skill never grants file-write authority.

## Output Contract

When clarification is required, provide:

1. the material uncertainty
2. one focused question or a small choice set
3. the consequence of each materially different option

When proceeding under assumptions, surface only assumptions that affect the result or residual risk.

## Quality Gates

1. Every material uncertainty is resolved or explicitly accepted.
2. Every prohibition and authority constraint survives unchanged.
3. Every acceptance criterion has a final status.
4. Optional enhancements remain separate from required scope.
5. No durable artifact is created without authority.

## Related Skills

- [Quizme Mode](../quizme-mode/SKILL.md): exhaustive conversation-local clarification when explicitly enabled.
- [Order of Operations](../order-of-operations/SKILL.md): sequence work after the contract is stable.
- [Skill Governance](../skill-governance/SKILL.md): apply risk gates after scope and effects are known.
