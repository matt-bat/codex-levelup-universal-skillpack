# Governance Walkthrough

This walkthrough shows the release-readiness path I expect for governed skillpack changes in this repository.

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
Run from the repository root:

```sh
python3 skills/skill-governance/scripts/generate_governance_artifact.py \
  --task-id PUSH-READY-20260524 \
  --project-id codex-levelup-skillpack \
  --profile internal \
  --project-language Markdown/Python \
  --project-description-max4 "Codex skillpack governance" \
  --model-runs-test-build-default yes \
  --skills-in-use "token-reduction,order-of-operations,skill-governance,interdependent-change-planning,regression-prevention,scripted-command-execution,doc-maintenance,user-instructions-tracker" \
  --skills-execution-order "token-reduction,order-of-operations,skill-governance,interdependent-change-planning,regression-prevention,scripted-command-execution,doc-maintenance,user-instructions-tracker" \
  --skills-selection-rationale "Release-readiness work touching governed skillpack policy, CI, documentation, and validation surfaces." \
  --execution-skill scripted-command-execution \
  --data-impact 0 \
  --business-impact 1 \
  --change-complexity 2 \
  --dependency-uncertainty 1 \
  --recoverability 1 \
  --behavior-or-workflow-changed
```

The generator writes:

1. `docs/governance/<task-id>.governance.json`
2. `docs/governance/<task-id>.governance.md`
3. `docs/project-index.md`

Use a task id that describes the change. The example above is only a template.

## Complete Gate Evidence
Before strict validation, update the generated artifact gate statuses after the checks pass.

Required gates for the standard release-readiness path:

1. `order-of-operations`
2. `scripted-command-execution`
3. `regression-prevention`
4. `token-reduction`
5. `doc-maintenance`

Use `pass` only when the related evidence exists. Use `waived` only with a concrete reason in artifact notes. If a gate is still unknown, leave it that way until you have evidence.

## Validate Locally
Use [validation-profiles.md](./validation-profiles.md) to choose `quick`, `standard`, or `release` validation depth.

For governed changes, run from the repository root:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
python3 skills/skill-governance/scripts/validate_governance_artifact.py \
  --artifact docs/governance/PUSH-READY-20260524.governance.json \
  --project-index-path docs/project-index.md \
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
4. validate skill ordering sync

## Ready-To-Push Checklist
Before pushing:

1. `git status --short` shows only intentional source, docs, workflow, and governance artifact changes
2. no tracked `__pycache__` or `*.pyc` files remain
3. policy validation passes
4. order sync validation passes
5. governance unit tests pass
6. changed governance artifacts pass strict validation
7. residual risk is written down if anything could not be checked

When all of that is true, the repo is in a much better state to push with confidence.
