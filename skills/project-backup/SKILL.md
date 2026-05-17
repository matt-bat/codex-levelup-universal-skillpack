---
name: project-backup
description: Use for implementing and enforcing project backup safety, including mandatory backup scripts or scheduled backups, restore verification, retention policies, and pre-change backup gates.
---

# Project Backup

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Hard Policy`
3. `Trigger Examples`
4. `Backup Scope Model`
5. `Data Classification`
6. `RPO/RTO Definitions (Required)`

### Action Modules (Read As Needed)
1. Establishing backup coverage:
   - `Mandatory Workflow` (Step 1-8)
   - `Backup Script Requirements`
   - `Backup Targets and Exclusions`
2. Security and durability:
   - `Encryption and Access Control`
   - `Offsite/Redundancy Guidance`
   - `Monitoring and Alerting`
3. Change-time protection:
   - `Pre-Change Backup Gates`
   - `Restore Runbook Requirements`
   - `Verification Checklist`

### Risk & Failure Handling
1. `Common Failure Modes`
2. `Anti-Patterns to Avoid`
3. `This Project: Practical Baseline`

### Output
1. `Deliverable Format`

## Mission
Ensure every project has reliable, restorable backups before risky changes can cause data/code loss.

## Hard Policy
Every project must satisfy at least one of these:
1. A versioned, executable local backup script in the repository.
2. A documented and verifiable scheduled backup process with restore evidence.

Preferred policy:
- Have both script-based on-demand backup and scheduled backups.

If neither exists, create one before proceeding with high-risk changes.

Compliance states:
1. `script_only`: compliant
2. `scheduled_only`: compliant
3. `script_and_scheduled`: preferred
4. `none`: non-compliant (block risky changes)

Enforcement:
1. if state is `none`, create remediation plan immediately
2. risky changes remain blocked until state is compliant

## Trigger Examples
Use for backup setup, backup audits, or any risky change requiring recovery guarantees.

## Backup Scope Model
Define scope first. Backups that miss critical assets are not valid.

Potential assets:
1. Source code and config
2. Dependency lockfiles
3. Environment templates (not raw secrets)
4. Databases
5. Media/uploads/object storage
6. Build/deploy metadata
7. Infra config (compose/manifests/terraform)
8. Generated business-critical artifacts

## Data Classification
Classify data by criticality:

Tier 1 (business critical):
- production database dumps
- customer media/assets
- payment/order records
- auth/account records

Tier 2 (operationally important):
- source code
- deployment config
- CI/CD definitions

Tier 3 (reconstructable):
- caches
- local temp artifacts
- dependency installs

Backup design must guarantee Tier 1 and Tier 2 protection.

## RPO/RTO Definitions (Required)
Before finalizing backup strategy, define:
1. RPO (Recovery Point Objective): maximum acceptable data loss window.
2. RTO (Recovery Time Objective): maximum acceptable restore time.

Minimum recommendations for active development:
- RPO: <= 24 hours
- RTO: <= 4 hours

For high-value production data, tighten further.

## Mandatory Workflow
Follow in order.

### Step 1: Inventory
Create a backup inventory:
1. what must be backed up
2. where it lives
3. how often it changes
4. whether it already has backup coverage

### Step 2: Gap Analysis
For each critical asset, determine:
1. Is it currently backed up?
2. Is backup automated?
3. Is retention defined?
4. Has restore been tested?

Any "no" for Tier 1 assets is a blocker for risky changes.

### Step 3: Strategy Selection
Define strategy per asset:
1. snapshot/archive backup
2. database dump backup
3. object/media sync backup
4. git mirror/offsite replication

### Step 4: Backup Implementation Policy Enforcement
Enforce at least one valid implementation path:

Path A: Repository backup script
1. script path documented (example: `scripts/backup.sh` or `scripts/backup.ps1`)
2. script executable and non-interactive by default
3. timestamped output artifact
4. integrity verification step
5. clear exit codes

Path B: Scheduled backup process
1. scheduler location documented (CI job, cron, platform scheduler, etc.)
2. schedule cadence documented and within defined RPO
3. job output location documented
4. integrity verification documented
5. restore evidence documented and current

If project is cross-platform and using Path A, provide platform-specific scripts or one portable runtime script.

### Step 5: Scheduling
Define cadence appropriate to compliance state:
1. If `scheduled_only` or `script_and_scheduled`: periodic scheduled backups (daily minimum for active projects).
2. For all states: pre-release backups.
3. For all states: pre-migration/pre-refactor backups.

Notes:
1. If project is `script_only`, a minimal scheduler recommendation should still be documented.
2. If project is `scheduled_only`, include a manual "run-now" procedure in the runbook.

### Step 6: Retention and Rotation
Define retention windows:
1. short-term frequent backups (for quick restore)
2. medium-term weekly backups
3. long-term monthly backups

Example baseline:
- keep 7 daily backups
- keep 4 weekly backups
- keep 6 monthly backups

### Step 7: Restore Verification
Backups are incomplete without restore testing.

Required:
1. run a restore drill on representative backup
2. verify data integrity and app startup against restored state
3. document restore duration and issues

### Step 8: Ongoing Validation
At regular intervals:
1. verify backup jobs succeeded
2. verify artifacts are readable
3. run periodic restore drills
4. rotate/expire old backups safely

## Backup Script Requirements
Backup scripts should implement:

1. Strict mode/safety:
- fail fast on command failure
- treat unset vars as errors

2. Input parameters:
- output destination
- optional mode/profile (full/incremental)

3. Timestamped output:
- backup folder/file names include UTC timestamp

4. Coverage:
- include required project paths
- include DB dump command where applicable
- include media/assets sync where applicable

5. Integrity:
- checksum file generation (example: sha256)
- optional archive verification step

6. Logging:
- concise progress logs
- explicit success/failure summaries

7. Exit semantics:
- non-zero on partial or total failure

8. Security:
- never print secrets to logs
- avoid embedding credentials in script body

## Backup Targets and Exclusions
Default include candidates:
- repository files
- migrations
- schema files
- docs
- runtime config templates
- DB dumps
- user media content

Default exclusions:
- dependency caches (`node_modules`, `.venv`, build caches)
- ephemeral artifacts (`.next`, temp files)
- sensitive local-only secrets that should be stored in secret manager

Note:
- Excluding `.env` from repo is correct, but production secret values still need secure backup in a secrets system.

## Encryption and Access Control
For offsite backups or sensitive data:
1. encrypt backup archives at rest.
2. restrict access by least privilege.
3. rotate encryption keys/credentials.
4. maintain auditability of who can restore.

## Offsite/Redundancy Guidance
Follow 3-2-1 principle where possible:
1. 3 copies of data
2. 2 different media/storage types
3. 1 offsite copy

Local-only backups are not sufficient for disaster scenarios.

## Pre-Change Backup Gates
Before risky operations (schema migration, mass refactor, dependency major upgrade):
1. run backup script (or confirm latest scheduled backup within RPO)
2. verify backup artifact integrity
3. confirm restore instructions exist
4. proceed only after gate passes
5. record backup artifact ID/hash used for this gate

## Restore Runbook Requirements
Maintain a concise restore runbook that includes:
1. backup artifact location
2. restore commands
3. DB restore sequence
4. media restore sequence
5. post-restore validation checklist
6. expected recovery time

## Verification Checklist
Use this checklist for completion:

- [ ] Critical asset inventory complete
- [ ] Gaps identified and resolved for Tier 1/Tier 2 assets
- [ ] Compliance state is `script_only`, `scheduled_only`, or `script_and_scheduled`
- [ ] Backup script exists OR scheduled backups are fully documented and verified
- [ ] Schedule and retention defined
- [ ] Integrity checks implemented
- [ ] Restore drill completed and documented
- [ ] Pre-change backup gate defined
- [ ] Ownership assigned for ongoing backup monitoring

## Monitoring and Alerting
If automation exists, require:
1. backup success/failure notifications
2. alert on missed backup windows
3. alert on integrity check failures
4. alert on storage quota exhaustion

## Common Failure Modes
1. Backup job "succeeds" but excludes critical paths.
2. DB dump exists but not restorable due to version mismatch.
3. Media backups omit recent uploads due to wrong path filter.
4. Retention policy deletes latest valid restore point.
5. Backups exist but no one has tested restore.

## Anti-Patterns to Avoid
1. "Git is enough backup."
2. Manual one-off backups with no repeatability.
3. No integrity checks.
4. No restore tests.
5. Backups stored only on same machine/disk.

## Deliverable Format
When applying this skill, produce:
1. Asset inventory
2. Gap analysis
3. Backup implementation plan
4. Script/schedule details
5. Restore runbook summary
6. Verification evidence and remaining risks
7. compliance state and go/no-go for risky change execution

## This Project: Practical Baseline
For projects like this stack (frontend/backend/media):
1. back up repository (excluding heavy caches)
2. back up database (dump)
3. back up uploads/media paths
4. run integrity hash generation
5. store backup artifacts in timestamped directory
6. validate with test restore on a regular cadence

## Related Skills
- [Scripted Command Execution](../scripted-command-execution/SKILL.md): implement deterministic backup scripts and scheduled command workflows.
- [Regression Prevention](../regression-prevention/SKILL.md): enforce backup gates before risky updates to reduce irreversible regressions.
- [Restore Drill](../restore-drill/SKILL.md): validate that backup artifacts are actually restorable.
- [Doc Maintenance](../doc-maintenance/SKILL.md): keep backup and restore runbooks synchronized with implementation.
