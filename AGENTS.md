# AGENTS.md

## Core Execution Policy

This file defines repository-local defaults. Follow higher-priority instructions first, and prefer a newer applicable instruction over an older conflicting instruction at the same level.

1. Build a task contract from the requested outcome, acceptance criteria, constraints, prohibitions, authority, and repository evidence.
2. Route by requested action and planned effect, not topic words or broad adjacency.
3. Treat zero selected skills as valid. Select the smallest set with one owner per decision domain; routine work should target two or fewer skills and normally use no more than five. Mandatory safety gates are exempt from this budget.
4. A skill supplies a workflow, not authority. Reading, writing, running commands, installing dependencies, committing, pushing, publishing, deploying, deleting, migrating, messaging, and changing external state require authority from the active instructions.
5. Read-only work performs zero writes, including trackers, indexes, caches, generated views, governance artifacts, commits, and external mutations.
6. Preserve user work and unrelated dirty-tree changes. Use local-first execution and do not deploy, publish, push, or alter remote settings unless explicitly authorized.
7. Reclassify the task after material inspection, after planning, after the final diff, and before any external or irreversible action. New effects can add gates; they cannot broaden authority.
8. Validate in proportion to the affected surface and report residual uncertainty, skipped checks, and external blockers accurately.

## Skill Routing

`skills/skill-catalog.json` is the canonical routing source. These files are generated views and must not be edited independently:

- `skills/SKILL-MAP.md`
- `skills/docs/skill-index.md`
- `skills/docs/skill-decision-tree.md`

Typed relations have distinct meanings: `requires` is a hard prerequisite, `gates` may veto a phase, `runs_after` orders already-selected skills, `supports` supplies evidence without activating another skill, `conflicts_with` prevents shared ownership, `consumes` names an input artifact, and `superseded_by` is a lifecycle edge.

Use `process-budget-controller` only as a deprecated compatibility name. Active routing owns process budgets.

## Declarations and Durable Artifacts

Declare `Skills in use`, selection rationale, and execution order only when the user explicitly requests a declaration or when governed/audited work needs a durable routing record. Routine work does not require a startup declaration.

Create or update a durable tracker, index, summary, governance artifact, or generated view only when the task explicitly requests it, an existing repository contract requires it, or the authorized change would otherwise leave that canonical artifact inaccurate.

## Conversation Modes

- `--quizme` toggles conversation-local exhaustive clarification. Supported immediate options are `--mc`, `--one-at-a-time`, `--confirm`, and `--record`. Run clarification before substantive execution while the mode is active.
- `/internal-lang on|off` controls private compact notation. `/internal-lang --response on|off` separately controls user-facing shorthand. Both states are conversation-local.

Keep user-facing responses concise and avoid unexplained abbreviations.
