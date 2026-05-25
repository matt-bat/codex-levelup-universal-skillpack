# Validation Profiles

Use validation profiles to match check depth to task risk. The point is not to run every command every time; the point is to make the validation claim honest.

## Quick
Use Quick for:

1. answer-only work
2. tiny non-governed text edits
3. local exploratory checks
4. early work where you just need to catch formatting mistakes

Run:

```sh
git diff --check
```

Optional:

```sh
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
```

Quick is enough when the change cannot affect skill behavior, release policy, CI, or validation logic.

## Standard
Use Standard for:

1. normal skillpack docs changes
2. non-critical skill updates
3. examples, profiles, or rubrics
4. changes where routing or wording should stay synchronized

Run:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
git diff --check
```

Standard is the best default for most edits in this repo.

## Release
Use Release for:

1. governed files
2. CI or validator changes
3. release-readiness claims
4. skill membership changes
5. governance artifact changes

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

Release is heavier by design. Use it when the repo needs to support a ready-to-push or ready-to-release claim.

## Profile Selection Rule
1. start with Quick
2. move to Standard when docs, skills, tests, or policy change
3. move to Release when governed files, CI, validators, governance artifacts, or release claims change
4. do not run Release for tiny non-governed changes unless the user asks

If a lower profile fails, fix that first. Do not jump to a heavier profile to create noise around a simpler failure.
