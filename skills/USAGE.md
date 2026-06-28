# Usage

I built this skillpack for people using ChatGPT, Claude, Gemini, Cursor, GitHub Copilot, or another assistant that can read repo instructions and follow them consistently.

The short version:

1. read [../START_HERE.md](../START_HERE.md)
2. choose an install profile
3. put the selected skill folders where the assistant can read them
4. copy the default policy from this repository into your project instructions
5. start a task and have the assistant declare which skills it is using
6. keep docs, trackers, and governance checks in sync when you change the pack

## What These Skills Are
Each skill is a folder with a `SKILL.md` file.

The assistant uses those files as task-specific operating instructions. A skill can define:

1. when it should be used
2. how it should be ordered with other skills
3. what files, checks, or evidence should be updated
4. what the assistant should avoid doing

This pack is intentionally more structured than a single prompt. It is meant to slow the assistant down on the parts where mistakes are expensive: requirements, sequencing, validation, documentation drift, policy changes, and release readiness.

It also includes process-budget controls, so simple work can still stay simple.

## Quizme Clarification Mode
Use `quizme-mode` when you want the agent to clarify every material detail before substantive execution.

Toggle it on:

```text
--quizme
```

Toggle it off by writing `--quizme` again. The mode persists throughout the active conversation until toggled off.

Optional arguments:

```text
--quizme --mc
--quizme --one-at-a-time
--quizme --confirm
--quizme --record
```

Rules:
1. `--mc` prefers multiple-choice questions with free-form fallback
2. `--one-at-a-time` asks one adaptive question per round
3. `--confirm` requires approval of the final task contract
4. `--record` persists the approved contract when a suitable artifact exists and implies `--confirm`
5. arguments must appear directly after `--quizme`, may appear in any order, and can be combined
6. duplicate arguments are harmless
7. unsupported arguments are ignored and briefly reported
8. every option clears when quizme mode is toggled off
9. destructive, public, production, payment, authentication, or irreversible tasks require confirmation automatically
10. the agent should use the plan-mode interactive clarification console when available and concise conversational questions otherwise

Combined example:

```text
--quizme --mc --one-at-a-time --confirm
```

## Recommended Setup
Use the `skills/` directory in this repository as the source of truth.

Typical setup:

1. copy the selected skill folders into your assistant's skills directory
2. keep `SKILL-MAP.md`, `docs/skill-index.md`, and `user-instructions.md` with the pack
3. copy the `AGENTS.md` policy into the project where you want these skills enforced
4. restart or refresh the assistant so it reloads the available skills

The skill folders are directories such as:

1. `skill-governance/`
2. `order-of-operations/`
3. `regression-prevention/`
4. `doc-maintenance/`
5. `token-reduction/`
6. `quizme-mode/`

Avoid copying one random `SKILL.md` by itself unless you already understand the dependency chain. Several skills deliberately reference the same routing docs and validation artifacts.

## How I Expect the Assistant To Use The Pack
At the start of a task, the assistant should declare:

1. `Skills in use`
2. why each skill was selected
3. the execution order

The default baseline is:

1. `token-reduction`
2. `order-of-operations`
3. `process-budget-controller` when several skills could apply

Use the smallest skill set that covers the work. A practical shortcut:

1. answer-only request: `token-reduction`
2. one deterministic local command: `token-reduction`, `scripted-command-execution`
3. tiny isolated text edit: `token-reduction`, `order-of-operations`
4. documentation-only update: `token-reduction`, `order-of-operations`, `doc-maintenance`
5. release-sensitive change: full governance path

Use [install-profiles.md](./docs/install-profiles.md) when adopting the pack in stages.

When the task changes behavior, workflows, policy, or docs, add:

1. `doc-maintenance`

For multi-step, risky, ambiguous, or release-affecting work, add:

1. `skill-governance`

When `--quizme` is active, add before substantive execution:

1. `quizme-mode`
2. `requirement-clarifier`

For non-trivial code changes, add:

1. `regression-prevention`
2. `effective-testing-methods` when tests need to be created or amended

For deterministic local shell work, add:

1. `scripted-command-execution`

For browser or GUI automation, add:

1. `pseudo-agentic-automation`

## Basic Task Prompt
Use a direct instruction like this:

```md
Use the skills in this repository. Follow `AGENTS.md`, declare the skills in use, and keep `user-instructions.md` current if my directives change.
```

For release-sensitive work, I would use:

```md
Use the governance skills before making changes. Validate the skill policy, ordering sync, and tests before calling this ready to push.
```

## Governance Files
The main routing files are:

1. `SKILL-MAP.md` for the high-level routing model
2. `docs/skill-index.md` for canonical cross-skill triggers
3. `user-instructions.md` for directive tracking and fulfillment evidence
4. `docs/cache-budgets.md` for bounded history and cached artifact limits
5. `docs/governance-walkthrough.md` for the governed release-readiness workflow
6. `docs/skill-decision-tree.md` for minimum viable skill selection
7. `skill-catalog.json` for machine-readable skill inventory
8. `docs/known-limitations.md` for explicit tradeoffs and residual limits
9. `docs/install-profiles.md` for staged adoption paths
10. `docs/conflict-resolution-matrix.md` for owner decisions across overlapping skills
11. `docs/validator-severity-levels.md` for blocking versus non-blocking validator guidance
12. `docs/validation-profiles.md` for quick, standard, and release check depth
13. `docs/maturity-model.md` for staged improvement levels
14. `docs/pruning-policy.md` for controlled growth and removal criteria
15. `docs/field-notes.md` for real-world usage evidence

When a skill trigger changes, update both:

1. `SKILL-MAP.md`
2. `docs/skill-index.md`

That keeps the pack from drifting into contradictory instructions.

For governed changes in this repository, keep these root-level artifacts current:

1. `.github/workflows/skills-governance-ci.yml`
2. `docs/governance/*.governance.json`
3. `docs/governance/*.governance.md`
4. `docs/project-index.md`

Lifecycle and quality review docs:

1. `docs/rubrics/skillpack-quality-rubric.md`
2. `docs/rubrics/release-readiness-rubric.md`
3. `docs/rubrics/documentation-quality-rubric.md`
4. `docs/adapters/agent.md`
5. `docs/adapters/generic-agent.md`
6. `docs/maturity-model.md`
7. `docs/field-notes.md`
8. `docs/pruning-policy.md`

## Validation Commands
Run these from the repository root before publishing normal skillpack changes:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
```

Run this when a governed change includes a governance artifact:

```sh
python3 skills/skill-governance/scripts/validate_governance_artifact.py \
  --artifact docs/governance/PUSH-READY-20260524.governance.json \
  --project-index-path docs/project-index.md \
  --strict \
  --require-recommendation go
```

If you are in a constrained environment and a check cannot run, record the exact blocker instead of claiming a clean pass.

## How To Add A New Skill
When adding a skill, keep the change connected across the pack:

1. add `<skill-name>/SKILL.md`
2. update `README.md`
3. update `SKILL-MAP.md`
4. update `docs/skill-index.md`
5. update `skill-catalog.json`
6. update governance validation snippets if the new skill becomes required policy
7. update `CHANGELOG.md`
8. update `user-instructions.md` with evidence
9. run the validation commands

## Examples
Use these examples to avoid over-applying skills:

1. [simple-code-fix.md](./docs/examples/simple-code-fix.md)
2. [bug-investigation.md](./docs/examples/bug-investigation.md)
3. [release-readiness-change.md](./docs/examples/release-readiness-change.md)
4. [frontend-layout-task.md](./docs/examples/frontend-layout-task.md)
5. [documentation-only-update.md](./docs/examples/documentation-only-update.md)
6. [quizme-clarification.md](./docs/examples/quizme-clarification.md)

## Licensing And Attribution
This pack uses an attribution-required non-commercial license.

If you use, copy, modify, or redistribute it, keep the license intact and credit:

1. Matt
2. Agent Command Center
3. the original repository or copy source

Commercial use requires written permission.
