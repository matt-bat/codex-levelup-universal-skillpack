# Governance Walkthrough

This walkthrough shows the release-readiness path for governed skillpack changes in this repository.

Use it when you need more than "I edited the files and it looks fine." The goal is to leave a clear trail: what changed, why it was governed, what checks ran, and whether the result is safe to push.

## When To Use This
Use this flow when a change touches:

1. `skills/**`
2. `AGENTS.md`
3. `.github/workflows/**`
4. `docs/governance/**`
5. `docs/project-index.md`

Those paths are governed because they can change agent behavior, validation gates, release policy, or the evidence used to make release decisions.

## Generate A Governance Artifact
Choose a task ID for the current change and resolve the exact base commit before running the generator. Replace the placeholder values below; do not reuse a dated artifact from another task.

```sh
TASK_ID=YOUR_CURRENT_TASK_ID
BASE_SHA=FULL_BASE_COMMIT_SHA

python3 skills/skill-governance/scripts/generate_governance_artifact.py \
  --task-id "$TASK_ID" \
  --base-sha "$BASE_SHA" \
  --repo-root . \
  --skills-root skills \
  --project-id agent-command-center \
  --profile internal \
  --project-language Markdown/Python \
  --project-description-max4 "Agent command center" \
  --model-runs-test-build-default yes \
  --execution-scope local_only \
  --quizme-mode off \
  --skills-in-use "skill-governance,regression-prevention,scripted-command-execution" \
  --skills-execution-order "skill-governance,regression-prevention,scripted-command-execution" \
  --skills-selection-rationale "Governed local change, regression evidence, and deterministic validation are in scope." \
  --execution-skill scripted-command-execution \
  --data-impact 0 \
  --business-impact 1 \
  --change-complexity 2 \
  --dependency-uncertainty 1 \
  --recoverability 1
```

The generator writes:

1. `docs/governance/<task-id>.governance.json`
2. `docs/governance/<task-id>.governance.md`
3. `docs/project-index.md`

The three selected skills above satisfy this standard-mode local example. Add other skills only when their catalog triggers apply. For example:

1. add `governance-enforcement` when governance tooling or release enforcement changes
2. add `doc-maintenance` and `--behavior-or-workflow-changed` when the authorized change makes canonical docs inaccurate
3. add `user-instructions-tracker` only when durable instruction tracking is already opted in or explicitly requested
4. while quizme mode is active, pass `--quizme-mode on` and include both `quizme-mode` and its required `requirement-clarifier` prerequisite

Add governed options that match the user request:
1. `--quizme-mc` for `--mc`
2. `--quizme-one-at-a-time` for `--one-at-a-time`
3. `--quizme-confirm` for `--confirm`
4. `--quizme-record` for `--record`; this implies confirmation

Use a task id that describes the change. The example above is only a template.

Recovery controls are effect-gated, not mode-gated. For an authorized deployment operation with credible external or non-reconstructable data-loss exposure, add `--requires-backup` and include `project-backup`. Add `--requires-restore` and include both `project-backup` and `restore-drill` only when the external operation actually requires a proven restore path. These flags are invalid for `local_only` scope.

## Complete Gate Evidence
Before strict validation, update the current task's paired governance artifact with evidence from checks that actually ran.

For the standard-mode example above, the generator emits these evidence gates:

1. `scripted-command-execution`
2. `regression-prevention`

Critical mode additionally gates `semantic-policy-audit` and `governance-enforcement`. The generator adds `doc-maintenance`, `project-backup`, and `restore-drill` only when their independent behavior or recovery flags are present. It never adds `token-reduction` or `order-of-operations` merely because a governance mode was selected.

Use `pass` only when the related evidence exists. A pending, failed, or waived required gate cannot support a `go` recommendation under schema version 2.

## Validate Locally
Use [validation-profiles.md](./validation-profiles.md) to choose `quick`, `standard`, or `release` validation depth.

For governed changes, run from the repository root:

```sh
TASK_ID=YOUR_CURRENT_TASK_ID

python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 skills/skill-governance/scripts/generate_routing_views.py --repo-root . --check
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
python3 skills/skill-governance/scripts/validate_governance_artifact.py \
  --artifact "docs/governance/${TASK_ID}.governance.json" \
  --strict \
  --require-recommendation go
```

If a command cannot run because of the environment, record the blocker and residual risk. Do not silently downgrade the claim.

## CI Enforcement
The active repository workflow is:

1. `.github/workflows/skills-governance-ci.yml`

The copyable workflow template is:

1. `skills/docs/ci/skills-governance-ci.yml`

Both run the same core checks:

1. compile governance scripts
2. run governance validator regression tests
3. enforce governed-change artifact requirements
4. validate catalog-derived routing views
5. enforce exact-revision governance evidence for release checks

## Bind The Exact Candidate Commit
After an authorized commit exists, check out that exact candidate commit with a clean worktree. Set `CANDIDATE_SHA` from the intended release commit, not from a moving branch name.

```sh
TASK_ID=YOUR_CURRENT_TASK_ID
BASE_SHA=FULL_BASE_COMMIT_SHA
CANDIDATE_SHA=FULL_CANDIDATE_COMMIT_SHA
ATTESTATION_PATH="/tmp/${TASK_ID}.attestation.json"

test "$(git rev-parse HEAD)" = "$CANDIDATE_SHA"
test -z "$(git status --porcelain --untracked-files=all)"

python3 skills/skill-governance/scripts/enforce_governance_ci.py \
  --repo-root . \
  --skills-root skills \
  --base-sha "$BASE_SHA" \
  --head-sha "$CANDIDATE_SHA" \
  --strict \
  --require-recommendation go \
  --release-check \
  --attestation-out "$ATTESTATION_PATH"
```

Version, changelog, release notes, skill count, and test count must all describe `CANDIDATE_SHA`. If an authorized local release tag already exists, verify that it resolves to the same commit:

```sh
TAG_NAME=INTENDED_RELEASE_TAG
test "$(git rev-parse "${TAG_NAME}^{commit}")" = "$CANDIDATE_SHA"
```

This proves only local checkout and local tag equality. It does not verify a remote tag, remote branch protection, or required remote checks; those remain separate authorized administrative checks.

## Ready-To-Push Checklist
Before pushing:

1. the checkout is clean and `HEAD` equals the exact candidate commit
2. no tracked `__pycache__` or `*.pyc` files remain
3. policy, generated-view, and governance unit validation passes on that commit
4. the current task artifact passes strict validation and binds the intended base and manifest
5. `--release-check` produces an exact-head attestation
6. release metadata and any authorized local tag equal the candidate commit
7. residual risk and unverified remote controls are stated explicitly

Passing this checklist supports a local release-readiness claim. Pushing, publishing, creating a tag, or changing remote protection still requires separate authority.
