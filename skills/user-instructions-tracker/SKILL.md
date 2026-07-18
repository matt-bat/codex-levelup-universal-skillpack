---
name: user-instructions-tracker
description: Use only when the user explicitly asks to record or audit instructions, when a durable cross-task directive changes in a repository that already opts into tracking, or when maintaining an existing instruction ledger is the requested work. Do not activate for ordinary task requests, transient acceptance criteria, status questions without a ledger, or merely because a tracker file is missing.
---

# User Instructions Tracker

## Purpose
Maintain an explicitly authorized durable ledger of cross-task directives while keeping current instruction truth separate from historical fulfillment evidence.

Activation alone never authorizes creating, migrating, or updating a tracker.

## Canonical Path
Required file:
1. prefer `user-instructions.md` at repository root

Resolve the active path in this order:
1. an explicit path configured by the user or repository
2. an existing root `user-instructions.md`
3. one existing configured legacy path, including `skills/user-instructions.md`
4. the root path only when the user explicitly asks to initialize or record a ledger

Do not create a second ledger, copy a legacy ledger, or migrate paths without explicit authorization. Once resolved, use one canonical path for the task.

## Recordability Gate
Record an instruction only when it is intended to survive the current task or conversation, such as:
1. repository policy or a durable constraint
2. an ongoing priority or ownership decision
3. a cross-task commitment whose fulfillment must be audited
4. an explicit user request to record it

Do not record ordinary requests, transient implementation details, speculative preferences, or inferred instructions.

## Current Truth and History
Maintain two concepts:
1. `Current Directives`: only directives that still govern future work
2. `Fulfillment History`: evidence of what happened under a directive at a point in time

A `done` historical row proves past fulfillment; it does not prove the instruction is still current.

Directive lifecycle values:
1. `active`: current and applicable
2. `superseded`: replaced by a newer directive, with successor identified
3. `stale`: applicability or evidence can no longer be confirmed
4. `retired`: intentionally no longer applicable

Allowed status values:

These values describe fulfillment history, not directive lifecycle:
1. `pending`
2. `in_progress`
3. `blocked`
4. `done`
5. `won_t_do`

Never delete or rewrite history to make a superseded directive appear current.

## Update Workflow
1. Confirm the instruction is durable and recording is authorized.
2. Resolve the single active ledger path.
3. Compare the new directive with current active directives.
4. Mark a conflicting older directive `superseded` and link its successor.
5. Update current truth independently from fulfillment status.
6. Attach concrete evidence only for work actually performed.
7. Mark uncertainty `stale` rather than guessing.

## Conditional Reference
Read [Tracker Schema and Lifecycle](./references/tracker-schema-and-lifecycle.md) only when creating an explicitly requested ledger, migrating an authorized legacy ledger, changing lifecycle state, or performing an audit.

## Routing Compatibility
Consult canonical `skill-catalog.json` only when the separately authorized tracker change alters cross-skill routing policy. Regenerate its views through `skill-governance/scripts/generate_routing_views.py`; do not hand-edit `docs/skill-index.md` or update routing merely because a directive was recorded.

## Output
When a ledger was actually changed, report:
1. canonical path used
2. current directives added or changed
3. lifecycle and fulfillment transitions
4. evidence recorded
5. stale, blocked, or superseded items requiring attention
