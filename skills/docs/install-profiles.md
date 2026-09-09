# Install Profiles

[Documentation home](./README.md) · [Start here](../../START_HERE.md) · [Common AI setup](./adapters/common-ai.md)

Use install profiles to adopt only the amount of process you actually need. The full pack is useful, but it is not the right starting point for every project or every task.

Profiles control which skills are available; they do not activate every installed skill. Routing architecture version 2, implemented by router contract 2.1, starts from zero selected skills and adds a skill only when its trigger applies. For routine tasks, target a median of no more than two selected skills and a normal cap of five. Mandatory safety skills and gates are never capped.

`internal-lang`, `hyperfocus-discovery`, `quizme-mode`, `clean-slate`, and `user-run-scripts` are optional controls in every profile. Explicit mode preferences persist across conversations when the host runs the reference adapter; it stores only booleans in `~/.config/agent-command-center/preferences.json` (or `AGENT_COMMAND_CENTER_PREFERENCES`). Install `help` with every profile so `--help` and the one-time startup hint remain available. Startup skill declarations are required only when explicitly requested or when governed or audited work needs a durable routing record.

## Minimal
Use Minimal when you mainly want local assistance, simple edits, and a cleaner task flow.

Skills:

1. `help`
2. `eliminate-assumptions`
3. `requirement-clarifier`
4. `token-reduction`
5. `order-of-operations`
6. `scripted-command-execution`
7. `user-run-scripts`

This profile provides focused output, dependency sequencing, and repeatable shell-command guidance when their triggers apply. Routine answer-only work and tiny edits may still use zero skills.

Do not add `process-budget-controller` to new installations. It is a deprecated compatibility wrapper for older integrations; router contract 2.1 owns process budgeting.

## Developer
Use Developer for normal software work where changes should be validated and docs should stay aligned.

Includes Minimal plus:

1. `regression-prevention`
2. `effective-testing-methods`
3. `doc-maintenance`
4. `file-maintenance`
5. `diagnose-before-fix`
6. `advanced-r-and-d`
7. `agent-humility`

This is the best default for most coding repositories. It adds enough quality control to catch common mistakes, research unfamiliar surfaces, and pivot from disproven approaches without requiring a governance artifact for every small change.

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

This profile is meant for changes where traceability matters: skill behavior, CI policy, validation rules, release readiness, instruction tracking, or anything that could create confusing agent behavior if it drifts. New governed records use governance-artifact schema v3; validators keep schema-v1 and schema-v2 records readable as historical evidence.

Availability still does not imply activation. Select only the governed and safety gates required by the task; do not cap mandatory safety gates to satisfy the routine budget.

## Frontend
Use Frontend for layout, interaction, visual system, and user experience work.

Includes Developer plus:

1. `thoughtful-approach`
2. `ui-design-skills`
3. `ui-spatial-canvas`
4. `pseudo-agentic-automation`
5. `advanced-svg`
6. `ui-dynamic-resizing`

This profile supports end-user experience, screenshots, browser checks, layout behavior, and dynamic interaction. Use `ui-spatial-canvas` only for explicit spatial-canvas work or an established spatial-canvas system, not for every frontend task.

## Full
Use the full pack when you want strict continuity, lifecycle management, and governance across the whole repository.

Full includes every active skill and every supporting doc in this repository. It is best for maintaining this skillpack or for teams that already know they want the heavier process. Include deprecated or compatibility entries only when an existing integration still depends on them.

## Recommendation
Start with `Developer` unless you are maintaining this skillpack or publishing governed policy changes.

Move to `Governed` when changes affect skill behavior, CI, validation, release posture, instruction tracking, or other files that define how the agent should operate.

When remote publication is authorized and `main` is protected, send governed changes through a feature branch and pull request so the required governance check can run. Do not treat an installed profile as authority to push or alter branch protection.

Move back down to `Minimal` for very small tasks. The point is to choose the right amount of process, not the maximum amount of process.

In every profile, use catalog schema v2 at `skills/skill-catalog.json` as the canonical routing source. The catalog declares router contract 2.1 and generates `skills/SKILL-MAP.md`, `skills/docs/skill-index.md`, and `skills/docs/skill-decision-tree.md`; do not maintain those views independently.

## Post-install verification

After copying or updating the pack, run these commands from the repository root. They force the host to load the current catalog and verify runtime toggles:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 -m unittest skills.skill-governance.tests.test_runtime_adapter -v
```

Hosts without a writable preference path must report that cross-conversation mode persistence is unavailable.
