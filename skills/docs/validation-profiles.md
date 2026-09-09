# Validation Profiles

[Documentation home](./README.md) · [Governance walkthrough](./governance-walkthrough.md) · [Validator severity levels](./validator-severity-levels.md)

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

1. normal skillpack documentation changes
2. non-critical skill updates
3. examples, profiles, or rubrics
4. changes where routing or wording should stay synchronized

Run:

```sh
python3 -m pip install --disable-pip-version-check -r skills/skill-governance/requirements.txt
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 skills/skill-governance/scripts/generate_routing_views.py --repo-root . --check
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
git diff --check
```

Standard is the best default for most edits in this repo. For routing changes, the policy validator checks schema-v2 `skills/skill-catalog.json`, router contract 2.1, and exact generated content for `skills/SKILL-MAP.md`, `skills/docs/skill-index.md`, and `skills/docs/skill-decision-tree.md`.

The same validator checks `.github/branch-protection-policy.json` against its closed schema and requires an explicit `Authority and Artifact Policy` section in every `authorized_only` skill. These are repository-structure checks; they do not observe GitHub or grant artifact-write authority.

When runtime commands or lifecycle behavior change, also run `python3 -m unittest skills.skill-governance.tests.test_runtime_adapter -v`. When advanced SVG behavior or references change, run the bundled smoke asset through `advanced-svg/scripts/render_svg.py`; compatibility-sensitive claims require both librsvg and Chromium.

## Release

Use Release-depth validation for:

1. governed files
2. CI or validator changes
3. ready-to-push claims for a governed candidate
4. release-publication claims
5. skill membership or governance artifact changes

Run Standard first. New governed changes require a unique, append-only schema-v3 governance JSON and canonical Markdown pair. Schema v3 binds operation-specific authority, typed gate evidence, the exact catalog, and the exact governed manifest. Historical schema-v1 and schema-v2 artifacts remain readable but cannot authorize a new change.

For an ordinary governed candidate, validate its artifact and run exact-head enforcement without `--release-check`:

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
  --attestation-out "$ATTESTATION_PATH"
```

For a release-publication claim, create exactly one strict schema-v3 artifact with purpose=`release`, explicit `publish` authority, exact release metadata, and a binding over the full candidate diff. Version, tag, changelog, release notes, skill count, and governance test count must all describe the same candidate. Then run:

```sh
python3 skills/skill-governance/scripts/enforce_governance_ci.py \
  --head-sha "$CANDIDATE_SHA" \
  --skills-root skills \
  --repo-root . \
  --strict \
  --require-recommendation go \
  --release-check \
  --attestation-out "$ATTESTATION_PATH"
```

If an authorized local release tag already exists, verify that it resolves to the same commit:

```sh
TAG_NAME=INTENDED_RELEASE_TAG
test "$(git rev-parse "${TAG_NAME}^{commit}")" = "$CANDIDATE_SHA"
```

Running this profile does not push, create or move a tag, publish release notes, deploy, or alter remote settings. `main` protection and its required `governance` check were verified on 2026-07-18, but remote state is mutable and must be rechecked before a current-state claim.

Use the single read-only operator workflow in [release-provenance.md](./release-provenance.md) for that live comparison. The verifier fails closed on unknown fields or desired-state drift and grants no `configure_remote` authority; a remote-setting change remains a separate operation requiring explicit authorization.

The governance job runs on every branch push and every pull request targeting `main`, so runtime and renderer conformance are exercised before merge. Strict main-push enforcement still applies only to `main`; pull requests require a new v3 plan only when the diff contains governed paths, while non-governed diffs still receive policy and regression checks.

## Profile Selection Rule

1. start with Quick
2. move to Standard when docs, skills, tests, or policy change
3. move to Release when governed files, CI, validators, governance artifacts, or release claims change
4. do not run Release for tiny non-governed changes unless the user asks

If a lower profile fails, fix that first. Do not jump to a heavier profile to create noise around a simpler failure.
