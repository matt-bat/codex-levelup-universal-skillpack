# Install Profiles

Use install profiles to adopt only the amount of process you actually need. The full pack is useful, but it is not the right starting point for every project or every task.

Profiles control which skills are available; they do not activate every installed skill. Routing architecture version 2 starts from zero selected skills and adds a skill only when its trigger applies. For routine tasks, target a median of no more than two selected skills and a normal cap of five. Mandatory safety skills and gates are never capped.

`internal-lang`, `hyperfocus-discovery`, and `quizme-mode` are optional conversation controls in every profile. Install them when you want their explicit modes; none is an always-on baseline. Startup skill declarations are required only when explicitly requested or for governed or audited work.

## Minimal
Use Minimal when you mainly want local assistance, simple edits, and a cleaner task flow.

Skills:

1. `token-reduction`
2. `order-of-operations`
3. `scripted-command-execution`

This profile provides focused output, dependency sequencing, and repeatable shell-command guidance when their triggers apply. Routine answer-only work and tiny edits may still use zero skills.

Do not add `process-budget-controller` to new installations. It is a deprecated compatibility wrapper for older integrations; the schema-v2 router owns process budgeting.

## Developer
Use Developer for normal software work where changes should be validated and docs should stay aligned.

Includes Minimal plus:

1. `regression-prevention`
2. `effective-testing-methods`
3. `doc-maintenance`
4. `file-maintenance`
5. `diagnose-before-fix`

This is the best default for most coding repositories. It adds enough quality control to catch common mistakes without requiring a governance artifact for every small change.

## Governed
Use Governed for release-sensitive, policy-heavy, or multi-skill workflows.

Includes Developer plus:

1. `skill-governance`
2. `governance-enforcement`
3. `semantic-policy-audit`
4. `interdependent-change-planning`
5. `user-instructions-tracker`
6. `skill-usage-review`
7. `deprecation-management`

This profile is meant for changes where traceability matters: skill behavior, CI policy, validation rules, release readiness, instruction tracking, or anything that could create confusing agent behavior if it drifts.

Availability still does not imply activation. Select only the governed and safety gates required by the task; do not cap mandatory safety gates to satisfy the routine budget.

## Frontend
Use Frontend for layout, interaction, visual system, and user experience work.

Includes Developer plus:

1. `thoughtful-approach`
2. `ui-design-skills`
3. `ui-spatial-canvas`
4. `pseudo-agentic-automation`

This profile supports end-user experience, screenshots, browser checks, layout behavior, and dynamic interaction. Use `ui-spatial-canvas` only for explicit spatial-canvas work or an established spatial-canvas system, not for every frontend task.

## Full
Use the full pack when you want strict continuity, lifecycle management, and governance across the whole repository.

Full includes every active skill and every supporting doc in this repository. It is best for maintaining this skillpack or for teams that already know they want the heavier process. Include deprecated or compatibility entries only when an existing integration still depends on them.

## Recommendation
Start with `Developer` unless you are maintaining this skillpack or publishing governed policy changes.

Move to `Governed` when changes affect skill behavior, CI, validation, release posture, instruction tracking, or other files that define how the agent should operate.

Move back down to `Minimal` for very small tasks. The point is to choose the right amount of process, not the maximum amount of process.

In every profile, use schema-v2 `skills/skill-catalog.json` as the canonical routing source. It generates `skills/SKILL-MAP.md`, `skills/docs/skill-index.md`, and `skills/docs/skill-decision-tree.md`; do not maintain those views independently.
