---
name: doc-maintenance
description: Use for keeping repository documentation accurate and synchronized with code changes, including README requirements, cross-skill document updates, and mandatory creation/maintenance of missing core docs.
---

# Doc Maintenance

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Scope Boundary`
3. `Hard Policy`
4. `Trigger Examples`

### Action Modules (Read As Needed)
1. Identifying doc impact:
   - `Required Documentation Inventory`
   - `Documentation Impact Mapping (Required)`
2. Core documentation updates:
   - `README Standard (Required)`
   - `Cross-Skill Documentation Synchronization`
   - `Update Rules`
3. Capturing rationale:
   - `Decision Notes and Code Notes Policy`
4. Validating and closing:
   - `Consistency Checks`
   - `Documentation Quality Gates`
   - `Priority Order for Doc Updates`
   - `New Repo Bootstrapping Rule`

### Output
1. `Deliverable Format`
2. `Anti-Patterns`

## Mission
Ensure all relevant documentation stays current whenever code, configuration, workflows, or operational policies change.

## Scope Boundary
This skill governs documentation currency and consistency.

Use [File Maintenance](../file-maintenance/SKILL.md) for:
1. periodic or deep file-level factuality/freshness audits
2. duplicate/staleness remediation across documentation surfaces

Use [User Instructions Tracker](../user-instructions-tracker/SKILL.md) for:
1. directive-level status tracking (`pending/in_progress/blocked/done/won_t_do`)
2. instruction evidence lifecycle management
3. instruction audit workflows

## Hard Policy
1. If a repository has no `README` (or `README.md`), create one.
2. Once present, README must be maintained with every relevant change.
3. Any document referenced by skills must be updated when triggering changes occur.
4. Documentation updates are part of done criteria, not optional cleanup.

## Trigger Examples
Use this skill when requests involve:
1. feature additions or removals
2. API, schema, config, auth, or deployment changes
3. new scripts, commands, workflows, or tools
4. changes to skill-defined operational artifacts
5. refactors that affect behavior, architecture, or usage

## Anti-Overuse Rules
Use when:
1. behavior, workflow, policy, setup, validation, or user-facing usage changes
2. a referenced documentation artifact must stay synchronized
3. documentation is part of the user's requested deliverable

Do not use when:
1. the task is answer-only and no repo artifact changes
2. a tiny internal code edit has no behavior or workflow impact
3. another skill owns the artifact and no documentation drift exists

Stop after:
1. canonical affected docs are updated
2. related references agree
3. validation confirms paths and commands are plausible or explicitly blocked

## Required Documentation Inventory
At task start, inventory doc surfaces likely impacted:
1. `README.md` / `README`
2. architecture and design docs (`docs/architecture.md`, etc.)
3. setup/run/test docs
4. API and schema docs
5. migration and rollback notes
6. operational runbooks
7. skill-linked docs (for example `docs/chat-history-index.md` from token-reduction practices)
8. release notes/changelog files if present
9. `docs/project-index.md` (new-project intake metadata)
10. `user-instructions.md` (directive tracking and fulfillment state)
11. `docs/skill-index.md` (cross-skill trigger routing)

If a repository lacks a docs directory but non-trivial behavior exists, create `docs/` and add minimum structure.

Inventory output format:
1. doc file/path
2. owner or primary audience
3. impacted by change? (`yes/no`)
4. update action (`edit/create/none`)

## Documentation Impact Mapping (Required)
Before editing docs, produce a mini impact map:
1. changed code paths/features
2. user-facing behavior changes
3. operator/dev workflow changes
4. affected doc files
5. new doc files needed

## README Standard (Required)
README must include, at minimum:
1. project purpose
2. stack summary
3. setup prerequisites
4. local run instructions
5. test/validation commands
6. key environment variables and where examples live
7. high-level repo structure
8. operational caveats (if any)

README update triggers:
1. command changes
2. dependency/runtime changes
3. env var changes
4. service endpoint changes
5. build/test/deploy flow changes

If no README exists:
1. create `README.md`
2. include minimum standard sections
3. link to deeper docs in `docs/`

## Cross-Skill Documentation Synchronization
When other skills define documentation artifacts, keep them synchronized.

Examples:
1. token-reduction references `docs/chat-history-index.md`:
   - create if missing when long-history workflow is used
   - update index when major interaction milestones occur
   - maintain concise response behavior and no-repetition conventions in related templates/docs
2. token-reduction also requires `docs/project-index.md`:
   - create if missing
   - keep project language, <=4-word description, and test/build preference (`yes/no`) current
   - when governance scripts are used, ensure index values match latest governance artifact intake fields
3. backup/restore skills imply runbook maintenance:
   - ensure restore and backup runbook references stay current
4. regression-prevention implies validation evidence format:
   - keep checklists/templates consistent with current test workflow
5. user-instructions-tracker requires `user-instructions.md`:
   - create if missing
   - append/update rows when directives are added/changed
   - keep status, evidence, and `Last Updated UTC` synchronized with actual execution state
6. cross-skill trigger routing requires `docs/skill-index.md`:
   - create if missing
   - update when trigger relationships or recommended companion skills change
7. effective-testing-methods requires accurate test command/documentation surfaces:
   - keep unit and Playwright command docs current
   - keep coverage mapping artifacts aligned with current flows

## Update Rules
1. Prefer direct edits to existing canonical docs over creating duplicates.
2. Keep docs concise but complete; avoid stale boilerplate.
3. Use exact command examples that are currently valid.
4. Update links/paths when files move.
5. Mark deprecated behavior explicitly with migration guidance.
6. Capture decision-driving assumptions/tradeoffs in docs instead of relying on ephemeral chat/internal reasoning.

## Decision Notes and Code Notes Policy
When changes include non-obvious logic or risk-based tradeoffs:
1. add short code comments near complex sections (why, not what)
2. add/update doc notes in the most relevant canonical doc (`README.md`, architecture, runbook, governance artifact, or feature doc)
3. prefer durable repo notes over long assistant narrative
4. keep notes concise and maintainer-focused

If no suitable doc exists for important rationale:
1. create `docs/decision-notes.md`
2. append concise dated entries with context, decision, rationale, and impact
3. link the note from the nearest canonical doc when appropriate

## Consistency Checks
After doc updates, verify:
1. commands in docs execute or are plausibly executable in current repo
2. filenames/paths referenced exist
3. env var names match code/config usage
4. examples match current API/schema behavior
5. related docs do not conflict

Cross-file consistency checks:
1. README command snippets match detailed docs command snippets
2. runbook terminology matches architecture/operations docs
3. skill-referenced artifacts exist at documented paths

## Documentation Quality Gates
A task touching behavior/config/workflow is incomplete unless:
1. affected docs are updated
2. README is present and current
3. cross-skill artifact docs are reconciled
4. known gaps are explicitly recorded

## Priority Order for Doc Updates
1. correctness-critical docs (runbooks, setup, migration/rollback)
2. README and quick-start instructions
3. architecture/design references
4. supplementary examples and notes

If instructions are conflicting across docs:
1. select a canonical source of truth
2. update all non-canonical docs to align
3. record the canonical source in the updated docs

## New Repo Bootstrapping Rule
For repos with minimal docs:
1. create `README.md`
2. create `docs/architecture.md` (or equivalent) if architecture is non-trivial
3. create `docs/operations.md` for run/test/deploy/backup/restore basics
4. add links between these docs

## Anti-Patterns
1. code changes merged without doc updates
2. creating redundant docs instead of updating canonical source
3. command examples that no longer run
4. stale env var lists
5. hidden operational changes only mentioned in chat

## Deliverable Format
When applying this skill, provide:
1. doc impact map
2. files updated/created
3. key doc deltas
4. validation performed (commands/links/path checks)
5. known remaining doc gaps

## Maintenance Cadence
For active repositories:
1. perform lightweight doc drift review at least monthly
2. perform full doc consistency review before major releases

## Related Skills
- [Token Reduction](../token-reduction/SKILL.md): maintain indexed chat artifact rules and concise doc hygiene.
- [Regression Prevention](../regression-prevention/SKILL.md): keep validation and rollback documentation aligned with risk controls.
- [Effective Testing Methods](../effective-testing-methods/SKILL.md): keep unit and Playwright testing documentation aligned with implementation updates.
- [File Maintenance](../file-maintenance/SKILL.md): perform deeper factuality/freshness lifecycle maintenance beyond change-driven doc sync.
- [Project Backup](../project-backup/SKILL.md): ensure backup/restore docs and runbooks remain current.
- [Restore Drill](../restore-drill/SKILL.md): keep drill procedures and evidence requirements documented.
- [Order of Operations](../order-of-operations/SKILL.md): sequence doc updates correctly relative to implementation and safety gates.
