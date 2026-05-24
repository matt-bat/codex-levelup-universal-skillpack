# Contributing

This repository is a governed skillpack. Changes should keep the skills useful without adding unnecessary process.

## Local Setup
Use a Git checkout with LF line endings. The root `.gitattributes` and `.editorconfig` files define the expected formatting.

Before committing line-ending cleanup, run:

```sh
git add --renormalize .
git diff --cached --check
```

## Adding Or Changing A Skill
When adding a skill:
1. create `skills/<skill-name>/SKILL.md`
2. add the skill to `skills/SKILL-MAP.md`
3. add the skill to `skills/docs/skill-index.md`
4. add the skill to `skills/skill-catalog.json`
5. update README and usage docs if public behavior changes
6. update `skills/user-instructions.md` with directive evidence
7. add or update validator tests when policy behavior changes

When changing an existing skill:
1. update the skill file first
2. update routing docs only when triggers, ownership, or artifacts change
3. avoid duplicating ownership already covered by another skill
4. record any important tradeoff in docs or governance artifacts

## Governance Expectations
Governed changes include:
1. `skills/**`
2. `AGENTS.md`
3. `.github/workflows/**`
4. `docs/governance/**`
5. `docs/project-index.md`

For governed changes, include or update a governance artifact under `docs/governance/`.

## Validation
Run from the repository root:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 skills/skill-governance/scripts/validate_governance_artifact.py \
  --artifact docs/governance/PUSH-READY-20260524.governance.json \
  --project-index-path docs/project-index.md \
  --strict \
  --require-recommendation go
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
```

## Commit Hygiene
Before pushing:
1. no `__pycache__` or `*.pyc` files are tracked
2. `git diff --check` passes
3. validator and test commands pass
4. README, usage docs, skill map, skill index, and catalog agree
5. governance artifact status matches actual validation evidence
