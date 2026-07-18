---
name: deprecation-management
description: Manage an explicitly approved rename, merge, supersession, discouragement, deprecation, or removal with compatibility routing and evidence-based exit criteria. Do not activate for ordinary edits, speculative consolidation, or a direct correction with no lifecycle impact.
---

# Deprecation Management

## Mission
Keep the skillpack from accumulating obsolete skills, duplicate docs, and stale policy paths.

## Authority and Artifact Policy
1. Activating this skill grants no authority to change lifecycle state, compatibility behavior, files, or release policy.
2. Apply a lifecycle transition only when the user or an existing repository contract explicitly authorizes that transition.
3. A read-only audit may recommend a transition but must not record or implement it.

## Trigger Rule
Use this skill when:
1. a skill is renamed, merged, split, or superseded
2. a document becomes obsolete but still has external value
3. a validator should warn before a future removal
4. users need migration guidance between old and new workflows

## Scope Boundary
This skill owns lifecycle state and migration policy.

Use [File Maintenance](../file-maintenance/SKILL.md) for factual cleanup.
Use [File Structure Optimization](../file-structure-optimization/SKILL.md) for file moves and layout changes.

## Deprecation States
1. `active`: supported and recommended
2. `discouraged`: still valid but no longer preferred
3. `deprecated`: supported temporarily with replacement guidance
4. `removed`: no longer present; migration notes remain in changelog or docs

## Required Deprecation Record
Every deprecated item must record:
1. item name or path
2. current state
3. replacement
4. reason
5. first deprecated date
6. removal criteria
7. migration notes
8. compatibility alias or wrapper behavior
9. observation evidence and rollback trigger

## Compatibility Rules
1. use one-way aliases or wrappers; do not create alias chains
2. preserve explicit user commands and public names through the announced window
3. exclude compatibility wrappers from active skill-count budgets
4. emit canonical names in new artifacts while accepting supported legacy names
5. preserve historical artifacts under the schema and names that created them

## Evidence Window
Before hard removal, require:
1. shadow-routing parity for all mandatory safety scenarios
2. at least 30 representative tasks or two releases of observation
3. zero unexplained alias failures
4. no material increase in corrections, backtracking, validation failures, or latency
5. exact-commit green release evidence

If evidence is unavailable, prefer `discouraged` or `deprecated` over removal.

## Anti-Overuse Rules
Use when:
1. lifecycle state changes are real
2. compatibility or migration matters
3. an old path or skill may still be referenced

Do not use when:
1. a file is simply edited
2. a typo or stale line can be fixed directly
3. no replacement or compatibility issue exists

Stop after:
1. state and replacement are documented
2. references are updated or intentionally preserved
3. validators or docs warn only where useful

Rollback when the replacement changes explicit command behavior, omits a safety gate, breaks artifact compatibility, or worsens measured outcomes beyond the accepted threshold.

## Output Contract
When applying this skill, provide:
1. deprecated item(s)
2. replacement path
3. migration impact
4. validator or documentation changes
5. removal criteria
