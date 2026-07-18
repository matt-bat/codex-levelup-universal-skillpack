---
name: order-of-operations
description: Use only for explicit multi-step work with real dependencies, mixed or unsafe requested order, hidden prerequisites, or parallel branches that require sequencing. Do not activate for single-step tasks, routine command execution, or obvious local ordering.
---

# Order of Operations

## Purpose
Convert an explicitly multi-step request into a dependency-correct, safe execution sequence while preserving user intent.

## Core Rule
Prompt order is not automatically execution order. Reorder only when dependencies, safety, authorization, validation prerequisites, or rollback readiness require it.

If the requested order is valid, keep it. If it must change:
1. use the smallest necessary reordering
2. explain the reason briefly
3. continue unless the change requires new authority or the user requested a pause

## Sequencing Workflow
1. Normalize the requested actions without adding scope.
2. Identify each action's prerequisites, outputs, side effects, and validation needs.
3. Build dependency edges only where one action truly relies on another.
4. Separate the critical path from independent branches.
5. Place authorization and irreversible-risk gates before their side effects.
6. Run validation after the state it validates exists.
7. Confirm every requested action is completed, deferred with agreement, or blocked with evidence.

## Boundaries
1. Do not invoke other skills solely because they are mentioned in a sequencing example.
2. Do not create plans, trackers, project indexes, documentation, or governance artifacts solely because this skill activated.
3. Do not introduce project-intake questions unrelated to the multi-step dependency graph.
4. Do not use sequencing as permission to override a safe explicit user constraint.
5. Stop for direction when a reordered step needs materially broader authority.

## Conditional Reference
Read [Sequencing Playbook](./references/sequencing-playbook.md) only when the task needs a dependency graph, concurrency decision, validation staging, or conflict resolution beyond the core workflow.

## Output
When sequencing is material, report:
1. dependency-correct order
2. meaningful reordering and reason
3. validation gates and outcomes
4. unresolved blocker or residual risk

For uncomplicated execution, keep the sequence internal and report only the outcome.
