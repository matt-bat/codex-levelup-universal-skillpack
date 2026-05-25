# Start Here

This is the fastest way to figure out how much of the skillpack you actually need.

The short version: do not start by turning everything on. Pick the smallest profile that fits the work, then grow from there only when the task needs more safety, evidence, or continuity.

## I Just Want To Try It
Start with the `Developer` profile in `skills/docs/install-profiles.md`.

That gives you enough structure for normal coding work without forcing the full governance system onto every task.

Basic setup:
1. copy `AGENTS.md` into the project where you want Codex to follow these rules
2. copy the relevant skill folders from `skills/`
3. ask Codex to declare the skills it is using at the start of each task
4. run one validation command once the files are in place

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
```

## I Want Minimal Process
Use only:

1. `token-reduction`
2. `order-of-operations`
3. `scripted-command-execution`
4. `process-budget-controller`

This is the right path for answer-only work, simple local commands, and small edits where a governance artifact would be overkill.

## I Want Governed Release Readiness
Use this path when a change affects skills, CI, validation policy, release posture, or user instruction tracking.

Read:
1. `skills/docs/governance-walkthrough.md`
2. `skills/docs/validation-profiles.md`
3. `skills/docs/rubrics/release-readiness-rubric.md`

Expect to use:
1. `skill-governance`
2. `governance-enforcement`
3. `regression-prevention`
4. `doc-maintenance`
5. `user-instructions-tracker`

Run the policy validator, order sync validator, governance artifact validator, and governance unit tests before pushing.

## I Want To Add Or Change A Skill
Read these in order:

1. `CONTRIBUTING.md`
2. `skills/docs/conflict-resolution-matrix.md`
3. `skills/docs/pruning-policy.md`
4. `skills/docs/validator-severity-levels.md`
5. `skills/skill-catalog.json`
6. `skills/docs/skill-index.md`
7. `skills/SKILL-MAP.md`

The key question is not “can this be a skill?” The better question is “does this skill remove repeated manual work, add enforceable safety, or simplify something else?”

## I Want To Avoid Over-Process
Use:

1. `process-budget-controller`
2. `skills/docs/skill-decision-tree.md`
3. `skills/docs/install-profiles.md`
4. `skills/docs/pruning-policy.md`

A good default is: if the next skill does not change execution, validation, safety, or durable evidence, do not add it.

## I Want To Improve The Pack Over Time
Use:

1. `skill-usage-review`
2. `deprecation-management`
3. `skills/docs/field-notes.md`
4. `skills/docs/maturity-model.md`

Field notes matter here. The best future improvements should come from real friction, repeated missed triggers, or repeated over-selection, not from adding structure just because it sounds useful.

## First Validation Set
Run from the repository root:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
```

For more detail, use `skills/docs/validation-profiles.md`.
