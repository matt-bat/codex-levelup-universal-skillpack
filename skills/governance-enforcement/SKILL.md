---
name: governance-enforcement
description: Generate, validate, and enforce content-bound governance plans and exact-head release attestations for governed work. Use when governance tooling or CI enforcement is being run or debugged; do not activate for policy-only decisions, ordinary project tests, or routine validation.
---

# Governance Enforcement

## Mission

Turn an independently selected governance policy into deterministic, fail-closed evidence checks.

## Scope Boundary

Own governance tooling and CI enforcement only. Do not decide task meaning, authorize mutation, select governed mode, waive a gate, or make a release decision.

Use [Skill Governance](../skill-governance/SKILL.md) for risk classification, gate selection, and the final recommendation. Use [Semantic Policy Audit](../semantic-policy-audit/SKILL.md) for intent-level conformance review.

## Trigger Rule

Use this skill when:

1. Generate or validate a governance plan.
2. Change or debug governance schemas, validators, catalog enforcement, or CI policy.
3. Validate content binding, typed evidence, break-glass records, or canonical artifact pairs.
4. Produce or check an exact-head release attestation.
5. Enforce governed-change history and scope in CI.
6. Validate the checked-in remote desired-state policy or compare it with live read-only evidence.

Do not activate merely because ordinary unit tests, linters, or project checks run.

## Primary Tooling

1. `skills/skill-governance/scripts/generate_governance_artifact.py`
2. `skills/skill-governance/scripts/validate_governance_artifact.py`
3. `skills/skill-governance/scripts/enforce_governance_ci.py`
4. `skills/skill-governance/scripts/validate_skill_policy.py`
5. `skills/skill-governance/scripts/validate_skill_order_sync.py`
6. `skills/skill-governance/scripts/generate_routing_views.py`
7. `skills/skill-governance/scripts/resolve_task_route.py`
8. `skills/skill-governance/scripts/verify_remote_configuration.py`
9. `skills/skill-governance/schemas/governance-artifact.schema.json`
10. `skills/skill-governance/schemas/task-descriptor.schema.json`
11. `skills/skill-governance/schemas/routing-result.schema.json`
12. `skills/skill-governance/schemas/remote-configuration-policy.schema.json`
13. `.github/branch-protection-policy.json`
14. `skills/skill-governance/requirements.txt`
15. `.github/workflows/skills-governance-ci.yml`
16. `skills/docs/ci/skills-governance-ci.yml`

## Enforcement Workflow

1. Resolve an immutable base commit and finalize the intended diff.
2. Generate a new schema-v3 artifact with a task ID absent at that base.
3. Record only operations that active instructions explicitly authorize; treat `configure_remote`, push, and publish as distinct authorities.
4. Keep every newly generated gate pending and the recommendation `no-go` until real evidence is recorded.
5. Record typed evidence objects with an allowed gate-specific kind, concrete reference, `result=pass`, timezone-bearing timestamp, and revision SHA or SHA-256 digest.
6. Keep the JSON and Markdown pair exact; schema-v3 Markdown must equal the generator's canonical rendering of its JSON.
7. Validate JSON structure with Draft 2020-12 JSON Schema and format checking, then apply semantic policy checks.
8. Validate the exact base, manifest, catalog binding, pair, governed scope, and regression tests.
9. Commit the finished pair once. Add a new superseding task ID for later corrections or phase changes.
10. For release readiness, use a clean checkout of the exact candidate commit and require exactly one matching release-purpose artifact.

Do not modify, delete, or rebind a committed governance pair. CI rejects historical changes at the base and add-then-modify or add-then-delete sequences inside the enforced commit range.

## Version Policy

Treat schema v3 as the only format for new governed changes. Preserve schema-v1 and schema-v2 artifacts as readable, immutable historical evidence under their recorded contracts. Never use a historical v1 or v2 plan as a new release artifact.

## Schema-v3 Contract

Enforce:

1. Closed top-level and nested object shapes through `governance-artifact.schema.json`.
2. Exact risk inputs, derived mode, required gates, evidence requirements, and recommendation semantics.
3. Exact catalog path, SHA-256, catalog version, router contract, components, and selected-skill relation snapshots.
4. Startup skill completeness, prerequisites, ordering, active status, and conflicts against the embedded catalog snapshot.
5. Typed gate evidence and gate-specific evidence kinds.
6. Accountable break-glass metadata, allowed waivers, and non-waivable safety gates.
7. A governed manifest for change purpose or full-diff manifest for release purpose.
8. Exact canonical Markdown equality.

Fail closed when the pinned `jsonschema` dependency is unavailable. Do not fall back to partial structural validation for governance artifacts.

## External and Release Enforcement

Force critical mode for authorized `configure_remote`, `delete`, `deploy`, `migrate`, or `publish`. Require target identity, rollback or recovery evidence, and post-operation validation/audit evidence for external operations. Require backup and restore controls for delete or migrate.

For release purpose, require:

1. Explicit `publish` authority and non-local scope.
2. Semantic version plus matching `v<version>` tag name.
3. Exact version, dated changelog, release-note, skill-count, and governance-test-count metadata at the candidate head.
4. Every release metadata path in the full bound diff.
5. Exactly one strict schema-v3 release artifact matching the exact head.

Treat `--release-check` as read-only verification. It neither publishes nor changes remote settings.

Treat `verify_remote_configuration.py` the same way: it validates a closed desired-state policy, normalizes a GitHub branch-protection response, verifies the response URL identifies the policy repository and branch, and compares exact state. Reject unknown policy or API fields and any drift. A pass is observation-time evidence only; it does not grant or exercise `configure_remote`.

## Required Validation Targets

1. Catalog schema, executable routing clauses, package membership, frontmatter descriptions, typed relations, alias direction, unique ownership, and combined hard-order graph acyclicity.
2. Exact generated-view equality with the catalog.
3. Instruction-ledger schema and lifecycle when that governed artifact changes.
4. Governance JSON/Markdown pairing and immutable historical compatibility.
5. Schema-v3 base SHA, manifest, manifest digest, catalog binding, task identity, and final content binding.
6. Typed evidence or an allowed, justified break-glass waiver for every mandatory gate.
7. Governed-path additions, modifications, deletions, and untracked files.
8. Candidate/head SHA and attestation equality for release checks.
9. Clean-checkout, release metadata, tag, and external-control verification at the release boundary.
10. Semantic route fixtures and adversarial schema, catalog, history, and evidence tests.
11. Closed-schema validity for `.github/branch-protection-policy.json`, exact target identity, supported GitHub response fields, and zero desired-state drift through `verify_remote_configuration.py`.

## Regression Test Command

Run the focused remote-control contract after desired-state schema or verifier changes:

```bash
python3 -m unittest skills.skill-governance.tests.test_remote_configuration -v
```

Run the full suite after governance-tool changes:

```bash
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py' -v
```

## Failure Handling

If enforcement fails:

1. Report the exact condition, path, and expected binding.
2. Classify the failure as `schema`, `policy`, `scope`, `binding`, `evidence`, `history`, `attestation`, or `external-control`.
3. Preserve `no-go`; never weaken a check to make an artifact pass.
4. Correct the current uncommitted contract or create a superseding artifact for committed evidence.
5. Rerun the narrow failing check, then the full enforcement profile.

## Output Contract

Provide:

1. Commands run.
2. Pass/fail state per validator.
3. Failing checks and remediations.
4. Final local enforcement state and separately unverified external controls.

## Related Skills

- [Skill Governance](../skill-governance/SKILL.md): governance policy and risk logic.
- [Doc Maintenance](../doc-maintenance/SKILL.md): canonical documentation updates after enforcement changes.
- [File Maintenance](../file-maintenance/SKILL.md): lifecycle accuracy checks for policy and operational artifacts.
