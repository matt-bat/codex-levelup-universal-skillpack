# Start Here

Use this page to choose the smallest useful path through the skillpack.

## I Want To Try It Quickly
1. read `skills/docs/install-profiles.md`
2. start with the `Developer` profile
3. copy `AGENTS.md` and the matching skill folders into your project
4. ask the agent to declare selected skills at task start
5. run one validation command after setup:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
```

## I Want Minimal Process
Use only:
1. `token-reduction`
2. `order-of-operations`
3. `scripted-command-execution`
4. `process-budget-controller`

This is enough for answer-only work, simple commands, and small local edits.

## I Want Governed Release Readiness
Use:
1. `skills/docs/governance-walkthrough.md`
2. `skills/docs/rubrics/release-readiness-rubric.md`
3. `docs/governance/*.governance.json`
4. `.github/workflows/skills-governance-ci.yml`

Run the policy validator, order sync validator, governance artifact validator, and governance unit tests before pushing.

## I Want To Add Or Change A Skill
Read in this order:
1. `CONTRIBUTING.md`
2. `skills/docs/conflict-resolution-matrix.md`
3. `skills/docs/validator-severity-levels.md`
4. `skills/skill-catalog.json`
5. `skills/docs/skill-index.md`
6. `skills/SKILL-MAP.md`

## I Want To Avoid Over-Process
Use:
1. `process-budget-controller`
2. `skills/docs/skill-decision-tree.md`
3. `skills/docs/install-profiles.md`
4. `skills/docs/pruning-policy.md`

## I Want To Improve The Pack Over Time
Use:
1. `skill-usage-review`
2. `deprecation-management`
3. `skills/docs/field-notes.md`
4. `skills/docs/maturity-model.md`

## First Validation Set
Run from the repository root:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
```
