---
name: deprecation-management
description: Use for managing the lifecycle of obsolete, superseded, merged, or renamed skills and docs with clear replacement paths, migration notes, validator warnings, and removal criteria.
---

# Deprecation Management

## Mission
Keep the skillpack from accumulating obsolete skills, duplicate docs, and stale policy paths.

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

## Output Contract
When applying this skill, provide:
1. deprecated item(s)
2. replacement path
3. migration impact
4. validator or documentation changes
5. removal criteria
