---
name: doc-maintenance
description: Update existing canonical documentation when an authorized change alters behavior, interfaces, commands, setup, operations, policy, or user-facing usage. Use when documentation would otherwise become inaccurate; do not create unrelated README, tracker, architecture, or runbook artifacts merely because the skill activated.
---

# Doc Maintenance

## Mission

Keep documentation true to implemented and verified behavior without expanding repository scope.

## Activation Boundary

Activate when:

1. an authorized change makes an existing canonical document inaccurate
2. documentation is an explicit deliverable
3. a new command, interface, migration, operational procedure, or compatibility rule requires user or operator guidance

Do not activate for answer-only work, behavior-neutral internal edits, or speculative documentation.

## Authority and Artifact Policy

1. Activating this skill grants no authority to create new repository structures.
2. Update an existing canonical document before creating another file.
3. Create a new document only when the task authorizes it and no suitable canonical surface exists.
4. Do not create or update trackers, project indexes, histories, governance records, backup systems, or release notes unless their own scoped trigger applies.
5. Preserve historical evidence; document supersession instead of rewriting history.

## Documentation Impact Map

Identify:

1. changed behavior or workflow
2. affected audience
3. canonical document that currently describes it
4. exact stale statement, command, path, or example
5. required validation

Skip unaffected documentation.

## Update Rules

1. Describe verified behavior, not intended future behavior.
2. Keep commands, paths, options, and examples exact.
3. Preserve the repository's voice and organization.
4. Link to one source of truth instead of duplicating detailed policy.
5. Mark lifecycle changes with replacement and compatibility guidance.
6. Capture non-obvious rationale only where a maintainer will need it.

For complex cross-document changes, read [documentation-validation.md](references/documentation-validation.md).

## Validation

1. Confirm referenced local paths exist or are explicitly external.
2. Run documented commands when safe and relevant, or mark them unexecuted.
3. Check related canonical documents for contradictions.
4. Review the final diff for duplicated prose and unrelated rewriting.
5. Never claim documentation is current beyond the surfaces inspected.

## Output Contract

Provide:

1. canonical documents changed
2. behavior or workflow synchronized
3. validation performed
4. remaining documentation risk

## Quality Gates

1. Every changed document corresponds to an authorized behavior or documentation deliverable.
2. No unrelated artifact was created.
3. Commands, paths, and lifecycle claims are verifiable.
4. Historical records remain historically accurate.

## Related Skills

- [User Instructions Tracker](../user-instructions-tracker/SKILL.md): durable directive records when explicitly triggered.
- [File Maintenance](../file-maintenance/SKILL.md): periodic factuality and staleness audits.
- [Deprecation Management](../deprecation-management/SKILL.md): lifecycle and compatibility guidance.
