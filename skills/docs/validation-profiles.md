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

For routing changes, the policy validator must validate schema-v2 `skills/skill-catalog.json` and verify that `skills/SKILL-MAP.md`, `skills/docs/skill-index.md`, and `skills/docs/skill-decision-tree.md` match their generated content.

## Release
Use Release for:

1. governed files
2. CI or validator changes
3. release-readiness claims
4. skill membership changes
5. governance artifact changes

Run Standard plus:

```sh
TASK_ID=YOUR_CURRENT_TASK_ID
BASE_SHA=FULL_BASE_COMMIT_SHA
CANDIDATE_SHA=FULL_CANDIDATE_COMMIT_SHA
ATTESTATION_PATH="/tmp/${TASK_ID}.attestation.json"

python3 skills/skill-governance/scripts/validate_governance_artifact.py \
  --artifact "docs/governance/${TASK_ID}.governance.json" \
  --strict \
  --require-recommendation go

test "$(git rev-parse HEAD)" = "$CANDIDATE_SHA"
test -z "$(git status --porcelain --untracked-files=all)"

python3 skills/skill-governance/scripts/enforce_governance_ci.py \
  --base-sha "$BASE_SHA" \
  --head-sha "$CANDIDATE_SHA" \
  --skills-root skills \
  --repo-root . \
  --strict \
  --require-recommendation go \
  --release-check \
  --attestation-out "$ATTESTATION_PATH"
```

Release is heavier by design. Use it when the repo needs to support a ready-to-push or ready-to-release claim. Resolve every placeholder to the current task and immutable commit identifiers. Run the exact-head checks from a clean checkout, then bind the version, changelog, release notes, skill count, test count, validation output, governance evidence, and attestation to `CANDIDATE_SHA`.

If an authorized local release tag already exists, verify that it resolves to the same commit:

```sh
TAG_NAME=INTENDED_RELEASE_TAG
test "$(git rev-parse "${TAG_NAME}^{commit}")" = "$CANDIDATE_SHA"
```

Running this profile does not perform a release. It does not create or move a tag, publish release notes, push changes, verify a remote tag, or configure remote branch protection. Remote protection and required-check verification remain external repository-administration actions. See [release-provenance.md](./release-provenance.md).

## Profile Selection Rule
1. start with Quick
2. move to Standard when docs, skills, tests, or policy change
3. move to Release when governed files, CI, validators, governance artifacts, or release claims change
4. do not run Release for tiny non-governed changes unless the user asks

If a lower profile fails, fix that first. Do not jump to a heavier profile to create noise around a simpler failure.
