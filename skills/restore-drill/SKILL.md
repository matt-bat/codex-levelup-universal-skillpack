---
name: restore-drill
description: Prove that an identified backup can restore an explicitly scoped external or disaster-recovery target within required recovery objectives. Use for requested restore exercises or recovery-sensitive production operations; do not require a drill for ordinary local code changes or source-only migration design.
---

# Restore Drill

## Mission

Demonstrate recoverability instead of assuming that a backup is usable.

## Preconditions

Require:

1. an identified backup artifact
2. an authorized isolated restore target
3. an ordered restore runbook
4. recovery point and recovery time objectives
5. success, stop, and cleanup criteria

If an external target or authority is missing, remain blocked without creating one implicitly.

## Drill Selection

Choose the smallest drill that proves the exposed risk:

1. `tabletop`: validate people, prerequisites, sequence, and failure branches
2. `technical_partial`: restore one affected subsystem
3. `technical_full`: restore the complete exposed system
4. `failure_variant`: inject a controlled artifact, credential, or dependency failure

A critical production release may require a recent full drill. Local source changes do not.

## Execution Contract

1. Verify artifact identity and integrity before restoration.
2. Restore only into the authorized isolated target.
3. Capture phase timestamps and exact failures.
4. Validate functional, data, security, and compatibility expectations.
5. Compare achieved recovery point and recovery time to targets.
6. Clean up the drill environment according to its authorization.

Read [restore-drill-runbook.md](references/restore-drill-runbook.md) for detailed evidence and failure scenarios.

## Pass and Veto Rules

Pass only when:

1. restoration completes without unrecoverable error
2. integrity and critical functional/data checks pass
3. required recovery objectives are met
4. no unresolved critical remediation remains

A stale, incomplete, unauthorized, or failed drill vetoes the dependent external operation. It does not block unrelated local work.

## Output Contract

Provide:

1. target, artifact, and drill type
2. validation and timing evidence
3. pass, conditional, blocked, or failed result
4. remediation and dependent-operation status

## Related Skills

- [Project Backup](../project-backup/SKILL.md): establish backup identity and coverage.
- [Skill Governance](../skill-governance/SKILL.md): decide when recovery evidence gates an operation.
- [Regression Prevention](../regression-prevention/SKILL.md): validate source and local runtime changes.
