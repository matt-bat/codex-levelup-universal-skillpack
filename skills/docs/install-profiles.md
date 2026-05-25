# Install Profiles

Use install profiles to adopt only the amount of process you actually need. The full pack is useful, but it is not the right starting point for every project or every task.

## Minimal
Use Minimal when you mainly want local assistance, simple edits, and a cleaner task flow.

Skills:

1. `token-reduction`
2. `order-of-operations`
3. `scripted-command-execution`
4. `process-budget-controller`

This profile keeps the agent concise, makes it inspect before acting, and gives it a basic shell-command workflow.

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

## Frontend
Use Frontend for layout, interaction, visual system, and user experience work.

Includes Developer plus:

1. `thoughtful-approach`
2. `ui-design-skills`
3. `ui-spatial-canvas`
4. `pseudo-agentic-automation`

This profile pushes the agent to think about the actual user experience, not just code completion. It is most useful when screenshots, browser checks, layout behavior, or dynamic interaction matter.

## Full
Use the full pack when you want strict continuity, lifecycle management, and governance across the whole repository.

Full includes every skill and every supporting doc in this repository. It is best for maintaining this skillpack or for teams that already know they want the heavier process.

## Recommendation
Start with `Developer` unless you are maintaining this skillpack or publishing governed policy changes.

Move to `Governed` when changes affect skill behavior, CI, validation, release posture, instruction tracking, or other files that define how the agent should operate.

Move back down to `Minimal` for very small tasks. The point is to choose the right amount of process, not the maximum amount of process.
