---
name: process-budget-controller
description: Deprecated compatibility wrapper for explicit legacy invocation of `process-budget-controller`. Do not auto-activate; use the active router's minimum-skill and process-budget policy instead.
---

# Process Budget Controller

## Status
Deprecated compatibility wrapper.

Skill-count caps and process restraint now belong to the active router or repository policy so selecting a budget does not require another skill. This wrapper remains only for older prompts, profiles, and artifacts that explicitly name `process-budget-controller`.

## Explicit Legacy Invocation
When explicitly invoked:
1. identify the smallest process tier compatible with user intent and safety
2. treat the tier as an advisory ceiling, not authority to skip required safety or validation
3. do not activate additional skills, create artifacts, or change files solely to describe the budget
4. hand selection back to the active router

Read [Migration](./references/migration.md) when interpreting an old tier, profile, artifact, or workflow.

## Removal Condition
Remove this wrapper only after active profiles, routing artifacts, governed records, and external consumers no longer reference the legacy name.
