---
name: project-backup
description: Establish or verify backup readiness for an explicitly authorized operation that could irreversibly alter external, production, or otherwise non-reconstructable state. Use for backup implementation/audits or real data-loss exposure; do not use for ordinary local source edits, source-only migration design, or topics such as authentication without an external-state operation.
---

# Project Backup

## Mission

Ensure non-reconstructable state has a verified recovery point before an authorized risky operation.

## Activation Gate

Activate only when at least one condition holds:

1. the user requests a backup system or backup audit
2. an authorized operation may delete, overwrite, corrupt, or irreversibly migrate external state
3. a production or release policy explicitly requires backup evidence

Repository history and a temporary working-copy backup are sufficient for reversible local source refactors unless the task includes non-reconstructable assets.

## Authority Boundary

This skill does not authorize:

1. accessing production systems
2. reading or exporting secrets
3. creating remote storage
4. running a migration
5. deleting or restoring data

Obtain separate authority for every external target and operation.

## Backup Contract

Define:

1. target identity and environment
2. critical assets and exclusions
3. recovery point objective and recovery time objective
4. backup mechanism, location, retention, and access controls
5. integrity verification
6. restore procedure and freshness
7. artifact identity used by the change gate

For implementation and operational detail, read [backup-runbook.md](references/backup-runbook.md).

## Pre-Operation Gate

Before the risky operation:

1. identify a current backup within the required recovery window
2. verify checksum, signature, archive readability, or platform-native integrity
3. confirm the backup covers every exposed critical asset
4. confirm a compatible restore target and ordered runbook exist
5. record the artifact identity without exposing secrets

Fail closed when the target, coverage, integrity, or restore path is unknown.

## Local Workspace Baseline

For a high-risk local refactor with uncommitted work:

1. preserve the complete writable workspace outside the repository
2. verify the copy against the source
3. record the backup location and exclusions
4. avoid treating that local copy as production disaster recovery

## Output Contract

Provide:

1. exposed assets and target
2. backup artifact identity and integrity result
3. restore readiness
4. gate decision and residual risk

## Related Skills

- [Restore Drill](../restore-drill/SKILL.md): prove operational restoration when required.
- [Regression Prevention](../regression-prevention/SKILL.md): handle local implementation and rollback safety.
- [Skill Governance](../skill-governance/SKILL.md): determine whether external-state gates are mandatory.
