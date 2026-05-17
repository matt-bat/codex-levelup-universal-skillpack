---
name: user-instructions-tracker
description: Use for creating or updating `user-instructions.md` in each repository to track user directives, implementation status, owners, evidence, and last-updated timestamps with a deterministic workflow.
---

# User Instructions Tracker

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Trigger Rule (Required)`
3. `Canonical Artifact`
4. `Required Schema`
5. `Status Model (Required)`

### Action Modules (Read As Needed)
1. Adding/updating directives:
   - `Instruction ID Rules`
   - `Update Workflow`
2. Historical bootstrap:
   - `Backfill Rule`
3. Compliance checking:
   - `Quality Gates`
   - `Minimal Timestamp Standard`
4. Cross-doc synchronization:
   - `Sync Requirements`

### Output
1. `Output Contract`
2. `Anti-Patterns`

## Mission
Maintain a durable, auditable record of user-provided instructions and their fulfillment state inside each repository.

## Trigger Rule (Required)
Use this skill when:
1. a repository has no `user-instructions.md`
2. user gives a new directive, constraint, or policy
3. instruction status changes (`pending`, `in_progress`, `blocked`, `done`, `won_t_do`)
4. user asks for progress, fulfillment, or instruction audit
5. scope/priorities change and instruction mapping must be updated

## Canonical Artifact
Required file:
1. `user-instructions.md` at repository root

If missing:
1. create it before substantive implementation work continues (except emergency fix paths)

## Required Schema
The file must contain:
1. title: `# User Instructions Tracker`
2. a status model section
3. a tracker table with exact columns:
   - `Instruction ID`
   - `Instruction`
   - `Source`
   - `Status`
   - `Priority`
   - `Owner`
   - `Last Updated UTC`
   - `Evidence`
   - `Notes`

## Status Model (Required)
Allowed status values:
1. `pending`
2. `in_progress`
3. `blocked`
4. `done`
5. `won_t_do`

Rules:
1. every row must use one allowed value
2. `done` requires evidence
3. `blocked` requires blocker detail in notes
4. `won_t_do` requires rationale in notes

## Instruction ID Rules
1. format: `INST-###` (zero-padded)
2. unique and stable across file history
3. never reuse IDs
4. superseded instructions keep original row and link successor in notes

## Update Workflow
### Step 1: Intake
1. add a new row for each materially distinct user directive
2. keep instruction text concise but faithful to user intent
3. include source reference (date/turn summary)

### Step 2: Plan Linkage
1. mark `pending` or `in_progress`
2. assign owner (`model`, `user`, or specific role)
3. set priority (`high`, `medium`, `low`)

### Step 3: Execution Linkage
1. update status as work progresses
2. attach concrete evidence:
   - file references
   - artifact IDs
   - validation command summaries

### Step 4: Closure
1. set `done` only when acceptance condition is satisfied
2. update `Last Updated UTC` on every status transition
3. add brief closure note

## Backfill Rule
When introducing tracker to an existing repo:
1. add `INST-000` backfill task row
2. summarize key historical instructions at high level
3. avoid fabricated certainty; mark unknowns explicitly

## Quality Gates
Tracker is non-compliant if:
1. required table columns missing
2. duplicate instruction IDs exist
3. status value outside allowed set
4. `done` row has empty evidence
5. `blocked`/`won_t_do` row has empty notes
6. missing or invalid `Last Updated UTC`

## Minimal Timestamp Standard
1. use ISO-8601 UTC (example: `2026-05-13T06:10:00Z`)
2. update timestamp whenever status, evidence, or notes change

## Sync Requirements
Keep tracker synchronized with:
1. `AGENTS.md` default behavior/policy changes
2. governance artifacts (`docs/governance/*.governance.*`) when task-level directives are involved
3. docs that declare process constraints (`README.md`, `docs/*.md`)
4. `docs/skill-index.md` when user directives change cross-skill trigger behavior

## Output Contract
When applying this skill, provide:
1. rows added/updated
2. status transitions made
3. evidence links recorded
4. unresolved blocked/won_t_do items

## Anti-Patterns
1. marking `done` without evidence
2. overwriting old rows instead of appending/updating status
3. using vague notes with no actionable blocker/rationale
4. letting tracker drift from actual implementation state
5. storing instruction state only in chat and not in repo artifact

## Related Skills
- [Doc Maintenance](../doc-maintenance/SKILL.md): ensures tracker updates are part of completion.
- [File Maintenance](../file-maintenance/SKILL.md): improves long-horizon tracker factuality and stale-row cleanup quality.
- [Skill Governance](../skill-governance/SKILL.md): aligns instruction state with task governance artifacts.
- [Order of Operations](../order-of-operations/SKILL.md): ensures tracker intake happens before major execution.
- [Token Reduction](../token-reduction/SKILL.md): keeps tracker entries concise and high-signal.
