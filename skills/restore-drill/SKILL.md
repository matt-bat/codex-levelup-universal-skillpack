---
name: restore-drill
description: Use for recurring backup-restore validation and disaster-recovery simulation, including restore runbooks, drill frequency, pass/fail gates, evidence capture, and remediation tracking.
---

# Restore Drill

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Scope`
3. `Trigger Examples`
4. `Required Preconditions`
5. `Drill Types`
6. `Frequency Policy`

### Action Modules (Read As Needed)
1. Planning drills:
   - `Drill Environment Policy`
   - `Recovery Objectives (RPO/RTO) Enforcement`
   - `Mandatory Drill Workflow` Step 1-2
2. Executing and validating drills:
   - `Mandatory Drill Workflow` Step 3-8
   - `Pass/Fail Gate Model`
   - `Evidence Requirements`
3. Operational hardening:
   - `Restore Runbook Quality Standard`
   - `Common Failure Scenarios to Simulate`
   - `Metrics and Trend Tracking`
   - `Checklists`

### Escalation & Output
1. `Escalation Rules`
2. `Deliverable Format`

## Mission
Prove backups are restorable under realistic failure conditions and within defined recovery objectives.

## Scope
This skill governs planning, execution, evidence capture, remediation, and recurring validation.

## Trigger Examples
Use for restore validation, DR simulation, and release-gate recovery checks.

## Relationship to Other Skills
- Use [Project Backup](../project-backup/SKILL.md) to establish backup creation, retention, and storage policy.
- Use this skill to validate that those backups restore successfully.
- Use [Regression Prevention](../regression-prevention/SKILL.md) when drills are part of pre-release or pre-change risk gating.

## Required Preconditions
Do not start a drill until these exist:
1. current backup artifact(s) identified
2. restore target environment available
3. restore runbook draft exists
4. owner/on-call roles identified
5. recovery objectives (RPO/RTO) defined

If any precondition is missing, mark drill status as blocked and fix prerequisites first.

## Drill Types
Run multiple drill types; a single happy-path drill is insufficient.

1. `tabletop` (planning simulation):
- no system restore performed
- validates people/process/sequence

2. `technical_partial`:
- restore one subsystem (e.g., DB only or media only)
- validates component-level recoverability

3. `technical_full`:
- restore full stack (code + DB + media + config)
- validates end-to-end recovery path

4. `chaos_variant`:
- inject one controlled failure during restore (missing file, bad credential, partial archive)
- validates operator response and runbook quality

## Frequency Policy
Minimum cadence:
1. tabletop: monthly
2. technical_partial: monthly
3. technical_full: quarterly
4. pre-major-release or pre-high-risk migration: ad hoc mandatory full drill or last-full-drill freshness check

Freshness rule:
- if no successful full drill within the last 90 days, risky production changes are blocked.

Date tracking requirement:
1. record `last_successful_full_drill_at`
2. evaluate freshness before every high-risk release gate

## Drill Environment Policy
Prefer isolated environments that mirror production characteristics.

Requirements:
1. environment parity documented (version/runtime/schema deltas)
2. destructive operations isolated from production
3. enough representative data volume to test performance realism
4. access/permissions available for restore operators

## Recovery Objectives (RPO/RTO) Enforcement
Each drill must evaluate:
1. achieved RPO: recovered data currency vs target
2. achieved RTO: elapsed time to service readiness vs target

Pass criteria:
1. achieved RPO <= target RPO
2. achieved RTO <= target RTO

If either fails, drill is failed even if app eventually starts.

## Mandatory Drill Workflow
Follow in order.

### Step 1: Drill Charter
Document:
1. drill type
2. scope/assets included
3. target RPO/RTO
4. participants and roles
5. planned start/end
6. success/failure criteria

### Step 2: Artifact Verification
Before restore starts:
1. confirm backup artifact timestamp and source
2. verify integrity checksums/signatures
3. verify encryption/decryption path (if encrypted)
4. verify artifact completeness (expected files present)

If integrity fails, stop and escalate.

### Step 3: Restore Execution
Execute restore runbook step-by-step:
1. code/config restore
2. database restore
3. media/object restore
4. service startup
5. dependency/service connectivity checks

Capture timestamps for each phase.

### Step 4: Functional Validation
After restore, run mandatory checks:
1. app boots without critical errors
2. auth/login path works
3. at least one critical business flow succeeds
4. key API health and core endpoints respond correctly
5. representative media/assets are accessible

### Step 5: Data Validation
Verify restored data quality:
1. key table/entity counts in expected range
2. referential integrity/basic constraint sanity
3. recent critical records exist (within RPO tolerance)
4. no obvious corruption/truncation signals

### Step 6: Security Validation
Confirm:
1. secrets/credentials are not leaked in logs/artifacts
2. restored permissions are least-privilege compliant
3. encryption expectations remain intact after restore

### Step 7: Timing Evaluation
Compute:
1. actual RTO (start restore -> service ready)
2. actual RPO (backup point -> incident point simulated)

Compare against targets and mark pass/fail.

### Step 8: Debrief and Remediation
For any issue found:
1. classify severity
2. assign owner
3. set due date
4. track remediation status

No unresolved critical findings should remain open for next high-risk release.

## Pass/Fail Gate Model
Drill passes only if all are true:
1. restore completed without unrecoverable errors
2. integrity checks passed
3. functional/data/security validations passed
4. RPO target met
5. RTO target met

Drill is conditional pass if:
1. core restore succeeded but non-critical checks failed
2. remediation ticket created with committed due date

Drill fails if:
1. restore cannot complete
2. integrity fails
3. critical flow fails
4. RPO/RTO miss on critical systems

Release-gate implication:
1. failed or stale full drill blocks high-risk release until remediation and re-validation

## Evidence Requirements
Every drill must produce evidence bundle:
1. drill charter
2. artifact identity (name/hash/timestamp)
3. step-by-step execution log with timestamps
4. validation results
5. RPO/RTO calculations
6. issues + remediation tracker links/IDs
7. final pass/fail decision

If evidence is missing, drill is considered invalid.

## Restore Runbook Quality Standard
Runbook must be:
1. deterministic and ordered
2. executable by an operator other than original author
3. explicit about prerequisites
4. explicit about rollback/retry paths
5. explicit about validation checkpoints

Runbook anti-patterns:
1. "Restore DB somehow."
2. hidden tribal knowledge steps
3. missing environment variable requirements
4. missing failure branching

## Role Model
Minimum roles per drill:
1. drill lead (coordinates)
2. operator (executes restore)
3. observer/scribe (captures evidence)
4. approver (signs pass/fail)

For small teams, one person may hold multiple roles, but approver should be distinct where possible.

## Common Failure Scenarios to Simulate
Cycle through these over time:
1. latest backup artifact corrupted
2. backup decrypt key unavailable
3. DB version mismatch on restore target
4. missing object/media segment
5. network dependency temporarily unavailable
6. expired credential during restore

## Metrics and Trend Tracking
Track over time:
1. drill pass rate
2. median/95th percentile restore time
3. RPO misses count
4. mean remediation closure time
5. repeated failure categories

Use trend data to improve runbook and backup architecture.

## Escalation Rules
Escalate immediately if:
1. two consecutive full drills fail
2. critical system misses RTO by >25%
3. critical data misses RPO target
4. restore depends on undocumented manual steps

High-risk releases must pause until corrective actions are implemented.

## Checklists
### Pre-Drill Checklist
- [ ] scope and objectives documented
- [ ] backup artifact selected and verified
- [ ] environment prepared
- [ ] roles assigned
- [ ] runbook accessible
- [ ] pass/fail criteria agreed

### Execution Checklist
- [ ] integrity checks passed
- [ ] restore phases completed
- [ ] service startup validated
- [ ] functional checks validated
- [ ] data checks validated
- [ ] security checks validated
- [ ] RPO/RTO calculated

### Post-Drill Checklist
- [ ] evidence bundle archived
- [ ] pass/fail decision recorded
- [ ] remediation items created
- [ ] owners and deadlines assigned
- [ ] next drill date scheduled

## Deliverable Format
When applying this skill, produce:
1. drill charter
2. execution transcript summary
3. validation and timing results
4. pass/fail verdict
5. remediation plan
6. next scheduled drill date
7. release-gate status (`pass`, `conditional`, `block`)

## Related Skills
- [Project Backup](../project-backup/SKILL.md): establish backup coverage and artifacts to validate.
- [Regression Prevention](../regression-prevention/SKILL.md): incorporate drill freshness/pass status into release risk decisions.
- [Doc Maintenance](../doc-maintenance/SKILL.md): keep restore runbooks and drill evidence templates current.
