---
name: governance-enforcement
description: Generate, validate, and enforce content-bound governance plans and exact-head release attestations for governed work. Use when governance tooling or CI enforcement is being run or debugged; do not activate for policy-only decisions, ordinary project tests, or routine validation.
---

# Governance Enforcement

## Mission
Turn an independently selected governance policy into deterministic, fail-closed evidence checks.

## Scope Boundary
This skill owns tooling and CI enforcement only. It does not decide task meaning, authorize mutation, select governance mode, waive a gate, or make a release decision.

Use [Skill Governance](../skill-governance/SKILL.md) for risk classification, gate selection, and the final go/no-go decision. Use [Semantic Policy Audit](../semantic-policy-audit/SKILL.md) for intent-level conformance review.

## Trigger Rule
Use this skill when:
1. generating or upgrading a governance plan
2. validating content binding, gate evidence, or waivers
3. producing or checking an exact-head release attestation
4. enforcing governed-change scope in CI
5. debugging those checks

Do not use it merely because ordinary unit tests, linters, or project checks will run.

## Primary Tooling
1. `skills/skill-governance/scripts/generate_governance_artifact.py`
2. `skills/skill-governance/scripts/validate_governance_artifact.py`
3. `skills/skill-governance/scripts/enforce_governance_ci.py`
4. `skills/skill-governance/scripts/validate_skill_policy.py`
5. `skills/skill-governance/scripts/validate_skill_order_sync.py`
6. `skills/skill-governance/scripts/generate_routing_views.py`
7. `skills/skill-governance/scripts/resolve_task_route.py`
8. `skills/skill-governance/schemas/*.json`
9. `.github/workflows/skills-governance-ci.yml` (active repository workflow)
10. `skills/docs/ci/skills-governance-ci.yml` (copyable workflow template)

## Enforcement Workflow
1. Resolve an immutable base commit and generate a schema-version-2 plan bound to the governed working-tree manifest.
2. Keep the recommendation `no-go` while any mandatory gate is pending, blocked, missing evidence, or supported only by an invalid waiver.
3. Record evidence-bearing gate objects; a status word alone is not evidence.
4. Rebind after the final governed diff. The governance artifact cannot satisfy a different change set merely by existing in the tree.
5. Validate the catalog and generated views, repository policy, artifact pair, governed scope, and regression tests.
6. For release readiness, use a clean checkout of the exact candidate commit and create an exact-head attestation. Verify any release tag resolves to that same commit.
7. Report failures precisely and rerun the narrow failing check before the full enforcement profile.

Schema-version-1 artifacts remain immutable historical evidence. They may still be validated under their legacy contract, but do not rewrite them or use them as schema-version-2 release attestations.

## Required Validation Targets
1. catalog schema, executable routing clauses, package membership, frontmatter descriptions, typed relations, alias direction, and hard-graph acyclicity
2. exact generated-view equality with the catalog
3. root instruction-ledger schema and active/superseded lifecycle
4. governance JSON/Markdown pairing and immutable legacy compatibility
5. schema-version-2 base SHA, governed manifest, manifest digest, task identity, and final content binding
6. evidence or an explicitly allowed, justified waiver for every mandatory gate
7. governed-path scope, including additions, modifications, deletions, and untracked files
8. candidate/head SHA and attestation equality for release checks
9. clean-checkout and release/tag verification at the external boundary
10. semantic route fixtures and adversarial catalog mutation tests

## Regression Test Command
Run after governance-script changes:
```bash
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py' -v
```

## Failure Handling
If enforcement fails:
1. report the exact condition, path, and expected binding
2. classify it as `schema`, `policy`, `scope`, `binding`, `evidence`, `attestation`, or `external-control`
3. preserve the failure as `no-go`; never weaken the check to make an artifact pass
4. correct the source contract or evidence, then rerun the targeted validator and full enforcement

## Output Contract
When applying this skill, provide:
1. commands run
2. pass/fail summary per validator
3. failing checks and remediations
4. final local enforcement state and any separately unverified external control

## Related Skills
- [Skill Governance](../skill-governance/SKILL.md): governance policy and risk logic.
- [Doc Maintenance](../doc-maintenance/SKILL.md): policy artifact updates after enforcement changes.
- [File Maintenance](../file-maintenance/SKILL.md): lifecycle accuracy checks for policy and operational artifacts.
