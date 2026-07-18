# Contributing

Thanks for helping improve the skillpack. This repo is intentionally governed, but the goal is not to make every change feel heavy. The goal is to keep the skills useful, consistent, and safe as they evolve.

## Before You Change Anything

Start by asking what kind of change this is:

1. small docs cleanup
2. new or changed skill behavior
3. validator or CI change
4. release-readiness change
5. cleanup, pruning, or deprecation

For small docs cleanup, keep it light. For skill behavior, validators, CI, or release posture, use the governed path.

## Local Setup

The repo expects LF line endings. The root `.gitattributes` and `.editorconfig` files handle that for normal workflows.

If you see a huge diff where every line changed, it is probably line endings. Run:

```sh
git add --renormalize .
git diff --cached --check
```

## Adding A Skill

When adding a skill, update the whole routing surface so the pack does not drift.

Required updates:

1. create `skills/<skill-name>/SKILL.md`
2. add its typed trigger, exclusions, role, relations, artifact policy, and lifecycle status to `skills/skill-catalog.json`
3. if its artifact durability is `authorized_only`, add an explicit `Authority and Artifact Policy` section to its `SKILL.md`; catalog validation rejects the skill without it
4. regenerate `skills/SKILL-MAP.md`, `skills/docs/skill-index.md`, and `skills/docs/skill-decision-tree.md`
5. update README and usage docs if users need to know about it
6. update the root `user-instructions.md` only when durable instruction tracking is explicitly in scope
7. add or update validator tests for policy behavior

Before adding a skill, check `skills/docs/pruning-policy.md`. A new skill should replace repeated manual behavior, reduce complexity somewhere else, or add enforceable safety or quality value.

## Changing A Skill

When changing an existing skill:

1. update the skill file first
2. update `skills/skill-catalog.json` when triggers, ownership, artifacts, relations, or lifecycle changed
3. regenerate all three routing views from the catalog; never edit a generated view independently
4. keep the explicit `Authority and Artifact Policy` section accurate when the skill uses `authorized_only` artifacts
5. avoid duplicating ownership already covered by another skill
6. record important tradeoffs in docs or governance artifacts
7. use `skills/docs/conflict-resolution-matrix.md` if ownership is unclear

## Governance Expectations

These paths are governed because changes there can affect future agent behavior:

1. `skills/**`
2. `AGENTS.md`
3. `.github/workflows/**`
4. `.github/branch-protection-policy.json`
5. `docs/governance/**`
6. `docs/project-index.md`
7. `user-instructions.md`

For a new governed change, add a unique schema-v3 JSON and Markdown pair under `docs/governance/`. The artifact must bind typed gate evidence, the exact catalog, and the governed diff. Committed governance artifacts are append-only: do not edit or delete v1, v2, or v3 history; add a superseding task artifact when later evidence changes the decision.

Release publication requires its own purpose=`release` v3 artifact. It must record explicit `publish` authority, exact version/tag/path/count metadata, and the full candidate diff rather than only governed paths.

`main` is protected as verified on 2026-07-18. Create a feature branch, push that branch only when authorized, and merge through a pull request after the required `governance` check passes. The pull-request job runs for every pull request targeting `main`; non-governed diffs still run policy and test checks but do not need a governance plan.

`.github/branch-protection-policy.json` is a closed desired-state contract. `validate_skill_policy.py` rejects unknown policy fields or an invalid schema. The read-only live verifier and its single canonical operator command are documented in `skills/docs/release-provenance.md`; verification never grants `configure_remote` authority.

## Validation

Use `skills/docs/validation-profiles.md` to choose the right depth.

For most governed changes, run:

```sh
python3 -m pip install --disable-pip-version-check -r skills/skill-governance/requirements.txt
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 skills/skill-governance/scripts/generate_routing_views.py --repo-root . --check
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
```

If a governance artifact changed, also run:

```sh
TASK_ID=YOUR_CURRENT_TASK_ID

python3 skills/skill-governance/scripts/validate_governance_artifact.py \
  --artifact "docs/governance/${TASK_ID}.governance.json" \
  --strict \
  --require-recommendation go
```

## Commit Hygiene

Before pushing:

1. no `__pycache__` or `*.pyc` files are tracked
2. `git diff --check` passes
3. validator and test commands pass
4. generated routing views match the canonical catalog
5. schema-v3 gate evidence is typed, digest- or revision-bound, and matches actual validation
6. the governance JSON and generated Markdown pair match exactly
7. no committed governance artifact was modified or deleted

If a check cannot run in your environment, record the exact blocker instead of calling the change fully validated.
