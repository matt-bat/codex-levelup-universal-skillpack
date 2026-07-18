---
name: skill-governance
description: Govern release-affecting, policy-changing, externally mutating, destructive, or otherwise high-risk work through typed effects, mandatory evidence, independent safety gates, and an explicit go/no-go decision. Do not use for ordinary answers, read-only inspection, tiny reversible edits, or a task made "multi-skill" only by optional process helpers.
---

# Skill Governance

## Mission

Apply enforceable controls to material risk without governing routine work by default.

## Activation Boundary

Activate when at least one condition applies:

1. Publish, release, deploy, or change protected remote repository settings.
2. Perform an authorized external-state mutation with material user, business, security, or data impact.
3. Perform a destructive, irreversible, recovery-sensitive, or uncertainty-critical operation.
4. Change cross-cutting routing, validation, governance, or release policy.
5. Produce an explicitly requested go/no-go decision or governed evidence record.

Do not activate only because several optional skills are adjacent to the task.

## Typed Governance Input

Consume a router 2.1 task descriptor that records:

1. Deliverables and acceptance criteria.
2. Action, operations, execution mode, command effect, test intent, and checkpoint.
3. Mutation, data-loss risk, recovery requirement, effects, surfaces, and domains.
4. Operation-specific authority, constraints, non-goals, and explicit skill requests.
5. Material uncertainties, rollback state, and typed evidence.

Resolve material ambiguity before creating durable evidence. Treat accepted router 2.0 descriptors as compatibility input only; do not infer explicit skills or artifact evidence from prompt text.

Choose `scripted-command-execution` for a deterministic shell or API workflow and `pseudo-agentic-automation` for adaptive browser or GUI interaction. Never select both execution owners.

## Authority Boundary

Treat every operation as separately authorized:

1. `configure_remote` authorizes only the named remote-configuration effect. It never grants commit, push, publish, deploy, or other authority.
2. Commit, push, publish, deploy, delete, migrate, message, and file writes each require their matching authority.
3. A skill supplies a workflow, not authority.
4. Read-only permits no writes, generated artifacts, installs, commits, remote changes, messages, deployments, or releases.
5. A command may run only when its typed effect and every authority it can exercise remain allowed.

## Independent Safety Kernel

Apply safety gates outside the optional skill budget:

1. Fail unknown or conflicting critical state closed.
2. Reject a mutating operation that conflicts with read-only scope.
3. Require an exact authority grant for every requested operation.
4. Require a `pre_external_action` reroute before external or irreversible execution.
5. Reclassify newly discovered effects before continuing.
6. Preserve every veto in the final decision.

## Remote Desired-State Verification

Use `.github/branch-protection-policy.json` as the machine-readable GitHub branch-protection desired state. Validate it against the closed `schemas/remote-configuration-policy.schema.json`, then compare a fresh API response with `scripts/verify_remote_configuration.py`.

Treat the verifier as read-only evidence collection. It neither grants nor exercises `configure_remote` authority. Fail closed when the policy is invalid, the API target differs, the API contains an unsupported field, or normalized actual state drifts from desired state. Never auto-remediate drift without separate `configure_remote` authority and a successful pre-action reroute.

## Router Artifact Boundary

Treat existing evidence and creation permission as independent:

1. Accept a passed router artifact only when its catalog kind, repository-relative path, and SHA-256 match a real repository file.
2. Let verified existing evidence satisfy a required governed-artifact gate even when new artifact creation is forbidden.
3. Grant artifact creation allowance only when policy permits it and file-write authority is requested and granted.
4. Never treat write authority or creation allowance as proof that required evidence exists.

Treat the repository manifest as content binding for the local change record, not proof of remote state. Record the exact external target, before and desired state, rollback path, and post-operation readback in typed evidence and audit references.

## Effect-Based Risk

Classify the planned effect rather than topic keywords:

1. `routine_local`: reversible local work with bounded effect.
2. `significant_local`: cross-cutting local behavior or policy work.
3. `external_reversible`: authorized external mutation with verified target identity, rollback, and post-operation checks.
4. `external_critical`: destructive, irreversible, production-sensitive, remote-policy, publication, or recovery-uncertain work.

Force critical mode for `configure_remote`, `delete`, `deploy`, `migrate`, or `publish`, even when numeric risk scores are zero. Require both backup and restore controls for authorized `delete` or `migrate`. Require an actionable rollback path for remote configuration and deployment; add backup or restore gates only when typed loss or recovery risk requires them.

Read [risk-and-gates.md](references/risk-and-gates.md) for the gate matrix.

## Decision-Domain Ownership

1. Let governance own governed mode, mandatory gates, and the final recommendation.
2. Let the task router own task classification and skill selection.
3. Let requirement clarification own unresolved task meaning.
4. Let regression prevention own implementation and change-safety evidence.
5. Let effective testing own test design.
6. Let governance enforcement own schemas, validators, CI, canonical pairs, and attestations.
7. Let backup and restore skills own recovery evidence when gated.

Allow supporters to mark evidence `must_surface`. Allow safety and enforcement owners to veto `go`, `verified`, `complete`, or `release-ready`.

## Dynamic Checkpoints

Reclassify:

1. Before work.
2. After repository inspection.
3. After planning.
4. After the final diff.
5. Immediately before an external or irreversible action.

Record route changes as bounded operational facts without exposing hidden reasoning.

## Governance Evidence

Create a schema-v3 governance pair for new governed changes. Record:

1. Purpose, immutable task identity, exact base revision, and authorized operations.
2. Full risk inputs, required gates, residual risk, and recommendation.
3. A governed manifest for `change` purpose or full-diff manifest for `release` purpose.
4. The exact catalog path, digest, version, router contract, components, and selected-skill relation snapshots.
5. Typed gate evidence with `kind`, concrete `reference`, `result=pass`, timezone-bearing observation time, and a revision SHA or content digest.
6. Accountable break-glass metadata when a permitted gate is waived.

Pending or failed required gates force `no-go`. Use `no-go` or `go-with-risk`, never `go`, when an enabled break-glass record supports an allowed waiver. Never waive `governance-enforcement`, `project-backup`, or `restore-drill` in schema v3.

Keep the JSON and canonical Markdown pair exact and append-only after the first commit. Historical evidence is immutable after its first commit. Validate schema-v1 and schema-v2 records under their historical contracts, but never modify or rebind a committed historical plan. Add a new superseding task ID instead.

Read [governance-artifacts.md](references/governance-artifacts.md) for lifecycle rules.

## Startup Declaration Scope

Declare skills in user-facing prose only when the user explicitly requests a declaration or governed/audited work needs a durable routing record. Always populate the schema-v3 artifact's startup declaration because it binds the governed skill set and execution order to the exact catalog snapshot.

## Release Integrity

Treat release as a distinct schema-v3 purpose. Require:

1. Explicit `publish` authority and non-local execution scope.
2. A semantic version and matching `v<version>` tag name.
3. Exact version, dated changelog, release-note marker, skill-count, and governance-test-count metadata.
4. A full-diff binding containing every release metadata path.
5. Green mandatory gates and exactly one matching release artifact for the exact candidate commit.
6. Require a CI attestation bound to that commit and no unresolved release veto.

Do not treat a normal change artifact as release authorization. Do not retag or rewrite historical release evidence; publish a superseding patch or minor release when authorized.

## Output Contract

Provide:

1. Operation effect and governed mode.
2. Required gates and evidence state.
3. Authority limits, vetoes, and residual uncertainty.
4. Final recommendation and exact scope.

## Quality Gates

1. Keep routine work ungoverned unless a real trigger applies.
2. Derive safety gates from typed effects and authority.
3. Require concrete, appropriately typed evidence for every pass or waiver.
4. Bind new evidence to the exact catalog and change set.
5. Verify protected-branch state against the closed desired-state policy when that external control matters.
6. Attest the exact release commit before a release-readiness claim.
7. Never hide a failed gate, veto, skipped check, or external uncertainty.

## Related Skills

- [Governance Enforcement](../governance-enforcement/SKILL.md): deterministic tooling and CI.
- [Requirement Clarifier](../requirement-clarifier/SKILL.md): stabilize ambiguous scope before governance.
- [Regression Prevention](../regression-prevention/SKILL.md): implementation and change-safety evidence.
- [Project Backup](../project-backup/SKILL.md): external-state recovery-point evidence.
- [Restore Drill](../restore-drill/SKILL.md): operational restore proof.
