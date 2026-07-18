# Start Here

This is the fastest way to figure out how much of the skillpack you actually need.

The short version: do not start by turning everything on. Pick the smallest profile that fits the work, then grow from there only when the task needs more safety, evidence, or continuity.

## I Just Want To Try It
Start with the `Developer` profile in `skills/docs/install-profiles.md`.

That gives you enough structure for normal coding work without forcing the full governance system onto every task.

Basic setup:
1. copy `AGENTS.md` into the project where you want the assistant to follow these rules
2. copy the relevant skill folders from `skills/`
3. allow the router to select zero or more skills; zero skills is valid when core policy already covers the work
4. run one validation command once the files are in place

Ask for a startup skill declaration only when you explicitly want one or when the work is governed or audited.

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
```

## I Want Minimal Process
Start with the zero-skill route for answer-only work and tasks already covered by core policy. Add a skill only when its trigger is present:

1. `token-reduction` for a real context or output-budget constraint
2. `order-of-operations` for meaningful dependencies or sequencing risk
3. `scripted-command-execution` for a repeatable local command workflow

For routine work, target a median of no more than two selected skills and a normal cap of five. Mandatory safety skills and gates are never omitted or capped to meet that budget.

`process-budget-controller` is a deprecated compatibility wrapper. New integrations should rely on the router's built-in budget instead.

## I Want Exhaustive Clarification
Install `quizme-mode`, then write:

```text
--quizme
```

Quizme mode persists for the conversation until toggled off with `--quizme` again.

Optional arguments:
1. `--mc`: prefer interactive multiple-choice questions
2. `--one-at-a-time`: ask one adaptive question per round
3. `--confirm`: require approval of the final task contract
4. `--record`: save the approved contract when a suitable artifact exists; implies `--confirm`

Combine options directly after `--quizme`, for example:

```text
--quizme --mc --one-at-a-time --confirm
```

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
5. `user-instructions-tracker` when durable directive tracking was explicitly enabled

Run the policy validator, order sync validator, governance artifact validator, and governance unit tests before pushing.

Documentation work does not publish a release. The next release must validate and attest one exact candidate commit; configuring remote branch protection remains an external repository-administration step.

## I Want To Add Or Change A Skill
Read these in order:

1. `CONTRIBUTING.md`
2. `skills/docs/conflict-resolution-matrix.md`
3. `skills/docs/pruning-policy.md`
4. `skills/docs/validator-severity-levels.md`
5. `skills/skill-catalog.json`
6. `skills/docs/skill-index.md`
7. `skills/SKILL-MAP.md`

`skills/skill-catalog.json` schema version 2 is canonical. It generates `skills/SKILL-MAP.md`, `skills/docs/skill-index.md`, and `skills/docs/skill-decision-tree.md`; do not maintain those views independently.

The key question is not “can this be a skill?” The better question is “does this skill remove repeated manual work, add enforceable safety, or simplify something else?”

## I Want To Avoid Over-Process
Use:

1. the router budget in `skills/skill-catalog.json`
2. `skills/docs/skill-decision-tree.md`
3. `skills/docs/install-profiles.md`
4. `skills/docs/pruning-policy.md`

A good default is: if the next skill does not change execution, validation, safety, or durable evidence, do not add it.

Use `process-budget-controller` only when an older integration still invokes that compatibility name.

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
