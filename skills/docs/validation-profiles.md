# Validation Profiles

Use validation profiles to match check depth to task risk.

## Quick
Use for:
1. answer-only work
2. tiny non-governed text edits
3. local exploratory checks

Run:
```sh
git diff --check
```

Optional:
```sh
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
```

## Standard
Use for:
1. normal skillpack docs changes
2. non-critical skill updates
3. examples, profiles, or rubrics

Run:
```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
git diff --check
```

## Release
Use for:
1. governed files
2. CI or validator changes
3. release-readiness claims
4. skill membership changes

Run Standard plus:
```sh
python3 skills/skill-governance/scripts/validate_governance_artifact.py \
  --artifact docs/governance/<TASK>.governance.json \
  --project-index-path docs/project-index.md \
  --strict \
  --require-recommendation go

python3 skills/skill-governance/scripts/enforce_governance_ci.py \
  --base-sha origin/main \
  --head-sha HEAD \
  --skills-root skills \
  --repo-root . \
  --strict \
  --require-recommendation go
```

## Profile Selection Rule
1. start with Quick
2. move to Standard when docs, skills, tests, or policy change
3. move to Release when governed files, CI, validators, governance artifacts, or release claims change
4. do not run Release for tiny non-governed changes unless the user asks
