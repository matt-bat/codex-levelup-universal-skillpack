# Usage

I built this skillpack for Codex users who want a more consistent agent workflow without having to recreate the same process rules in every project.

The short version:
1. read `../START_HERE.md`
2. choose an install profile
3. put those skill folders where Codex can read them
4. add the default policy from this repository to your project instructions
5. start a task and require Codex to declare which skills it is using
6. keep the docs and governance checks in sync when you change the pack

## What These Skills Are
Each skill is a folder with a `SKILL.md` file.

Codex uses those files as task-specific operating instructions. A skill can define:
1. when it should be used
2. what order it should run in with other skills
3. what files, checks, or evidence should be updated
4. what the assistant should avoid doing

This pack is intentionally process-heavy. I use it to make Codex slow down on the parts where mistakes are expensive: requirements, sequencing, validation, documentation drift, and release readiness.

The pack now includes explicit process-budget controls so simple tasks can stay simple.

## Recommended Setup
Use the `skills/` directory in this repository as the source of truth.

Typical setup:
1. copy the skill folders into your Codex skills directory
2. keep `SKILL-MAP.md`, `docs/skill-index.md`, and `user-instructions.md` with the pack
3. copy the `AGENTS.md` policy into the project where you want these skills enforced
4. restart or refresh Codex so it reloads the available skills

The skill folders are the directories such as:
1. `skill-governance/`
2. `order-of-operations/`
3. `regression-prevention/`
4. `doc-maintenance/`
5. `token-reduction/`

Do not copy only one random `SKILL.md` file unless you know the dependency chain. Several skills deliberately reference each other.

## How I Expect Codex To Use The Pack
At the start of a task, Codex should declare:
1. `Skills in use`
2. why each skill was selected
3. the execution order

The default baseline is:
1. `token-reduction`
2. `order-of-operations`
3. `process-budget-controller` when several skills could apply

Use the smallest skill set that covers the task. The practical routing shortcut is:
1. answer-only request: `token-reduction`
2. one deterministic local command: `token-reduction`, `scripted-command-execution`
3. tiny isolated text edit: `token-reduction`, `order-of-operations`
4. documentation-only update: `token-reduction`, `order-of-operations`, `doc-maintenance`
5. release-sensitive change: full governance path

Use [install-profiles.md](./docs/install-profiles.md) when adopting the pack in stages.

When the task changes behavior, workflows, policy, or documentation, add:
1. `doc-maintenance`

For multi-step, risky, ambiguous, or release-affecting work, add:
1. `skill-governance`

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
4. `docs/adapters/codex.md`
5. `docs/adapters/generic-agent.md`
6. `docs/maturity-model.md`
7. `docs/field-notes.md`
8. `docs/pruning-policy.md`

## Validation Commands
Run these from the `skills/` directory before publishing changes:

```sh
python3 skill-governance/scripts/validate_skill_policy.py --repo-root ..
python3 skill-governance/scripts/validate_skill_order_sync.py
python3 -m unittest discover skill-governance/tests
```

Run this from the repository root when a governed change includes a governance artifact:

```sh
python3 skills/skill-governance/scripts/validate_governance_artifact.py \
  --artifact docs/governance/PUSH-READY-20260524.governance.json \
  --project-index-path docs/project-index.md \
  --strict \
  --require-recommendation go
```

If you are running inside a constrained environment and a check cannot run, record the exact blocker instead of claiming a clean pass.

## How To Add A New Skill
When I add a skill, I keep the change connected across the pack:
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

## Licensing And Attribution
This pack uses an attribution-required non-commercial license.

If you use, copy, modify, or redistribute it, keep the license intact and credit:
1. Matt
2. Level-Up Codex Skillpack
3. the original repository or copy source

Commercial use requires written permission.
