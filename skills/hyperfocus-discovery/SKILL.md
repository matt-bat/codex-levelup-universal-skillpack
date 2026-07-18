---
name: hyperfocus-discovery
description: Use only when the user explicitly requests bounded adjacent exploration or when a task already has multiple active branches that need resumable branch control. Do not activate for routine, single-threaded, answer-only, or one-command work.
---

# Hyperfocus Discovery

## Purpose
Manage necessary same-task branches without losing the primary goal.

This is an optional branch-control workflow, not a general creativity or scope-expansion default. Keep notes transient unless the user requests a durable record.

## Operating Contract
Maintain four transient states:
1. `Now`: current branch
2. `Resume`: exact next step for a paused branch
3. `Spark`: relevant candidate not yet pursued
4. `Done`: completed branch and evidence

Before switching branches:
1. write one concise `Resume` note
2. confirm the branch is necessary to the active task
3. confirm it can prevent rework, resolve a blocker, or materially improve the requested result
4. reject novelty, speculative redesign, and unrelated improvements

## Branch Budget
1. small task: at most two switches
2. non-trivial task: at most three switches before convergence
3. risky work: switch only after required safety and dependency gates

When the budget is reached, park new candidates and reconcile active branches before switching again.

## Invariants
1. Preserve the original goal and explicit acceptance criteria.
2. Do not bypass dependencies, safety gates, or authorization boundaries.
3. Do not implement adjacent work merely because it appears useful.
4. Do not create files, trackers, or artifacts solely because this skill activated.
5. Do not finish with an unresolved required `Resume` item.

## Conditional Reference
Read [Branch Management](./references/branch-management.md) only when a branch is actually paused, a switch decision is ambiguous, or a convergence sweep is required.

## Completion Check
1. Reconcile each active note as `done`, `deferred`, or `rejected`.
2. Confirm no requested outcome was dropped during switching.
3. Validate the completed primary task at its required level.
4. Report only completed work, material deferrals, and remaining risk.
