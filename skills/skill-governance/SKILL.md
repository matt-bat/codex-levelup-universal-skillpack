---
name: skill-governance
description: Govern release-affecting, policy-changing, externally mutating, destructive, or otherwise high-risk work through typed effects, mandatory evidence, independent safety gates, and an explicit go/no-go decision. Do not use for ordinary answers, read-only inspection, tiny reversible edits, or a task made "multi-skill" only by optional process helpers.
---

# Skill Governance

## Mission

Apply enforceable controls to material risk without making routine work governed by default.

## Activation Boundary

Activate when at least one applies:

1. publishing, releasing, deploying, or changing protected repository policy
2. authorized external-state mutation with material user, business, security, or data impact
3. destructive or irreversible action
4. cross-cutting validation or governance policy change
5. an explicit go/no-go or governed evidence requirement

Do not activate merely because several optional skills could apply.

## Typed Governance Input

Governance consumes a stable task descriptor containing:

1. deliverables and acceptance criteria
2. action, command execution mode/effect, test intent, and checkpoint
3. mutation, data-loss risk, recovery requirement, and external effects
4. surfaces and domains
5. authority granted
6. prohibitions and non-goals
7. material uncertainties
8. rollback and recovery exposure

Resolve material ambiguity before creating durable governance artifacts.

## Independent Safety Kernel

The safety kernel overrides routing and process budgets:

1. `read_only` permits no writes, generated artifacts, installs, commits, pushes, messages, deployments, or releases.
2. Commit, push, publish, deploy, delete, migrate, message, and external writes each require matching authority.
3. Unknown or conflicting critical state fails closed.
4. Newly discovered effects trigger rerouting before work continues.
5. A safety veto cannot be omitted or downgraded by a response owner.
6. A command may run only when its typed effect and every authority it can exercise remain allowed.

## Effect-Based Risk

Classify the planned operation rather than domain keywords:

1. `routine_local`: reversible local work with bounded effect
2. `significant_local`: cross-cutting local behavior or policy work
3. `external_reversible`: authorized external mutation with a proven rollback
4. `external_critical`: destructive, irreversible, production-sensitive, or recovery-uncertain action

Authentication, payment, schema, or migration source work receives domain-specific review. It becomes externally critical only when the planned operation exposes live state, users, or recovery.

Deployment requires an actionable rollback path. It activates backup or restore controls only when credible data-loss exposure or a required recovery path is separately established.

Read [risk-and-gates.md](references/risk-and-gates.md) for the gate matrix.

## Decision-Domain Ownership

1. Governance owns governed mode, mandatory gates, and the final go/no-go decision.
2. The task router owns task classification and skill selection.
3. Requirement clarification owns unresolved task meaning.
4. Regression prevention owns implementation and change-safety evidence.
5. Effective testing owns test design.
6. Governance enforcement owns schemas, validators, CI, and attestations.
7. Backup and restore skills own external recovery evidence when gated.

Supporters may mark evidence `must_surface`. Safety and enforcement owners may veto `go`, `verified`, `complete`, or `release-ready`.

## Dynamic Checkpoints

Reclassify:

1. before work
2. after repository inspection
3. after the implementation plan
4. after the final diff
5. immediately before an external or irreversible action

Record route changes without exposing hidden reasoning.

## Governance Evidence

For governed work, record:

1. schema and task identity
2. task descriptor summary and authority
3. base revision and normalized changed-file manifest
4. required gates with per-gate evidence
5. waivers with concrete reason, owner, and expiry where permitted
6. residual risk and rollback/recovery state
7. recommendation: `no-go`, `go-with-risk`, or `go`

Pending or failed required gates force `no-go`. Historical evidence is immutable after release or supersession.

Read [governance-artifacts.md](references/governance-artifacts.md) for artifact lifecycle rules.

## Release Integrity

Release requires:

1. explicit publication authority
2. known version, tag, changelog, and release-note consistency
3. green mandatory checks for the exact release commit
4. a CI attestation bound to that commit and governance plan
5. no unresolved release veto

Do not retag or rewrite a historical release to correct provenance. Publish a superseding patch or minor release.

## Output Contract

Provide:

1. operation effect and governed mode
2. required gates and evidence state
3. immutable vetoes or uncertainty
4. final recommendation and exact scope

## Quality Gates

1. Routine work remains ungoverned unless a real trigger applies.
2. Safety gates derive from effects and authority.
3. Every pass or waiver has evidence.
4. The exact release commit is attested.
5. No response hides a failed gate or veto.

## Related Skills

- [Governance Enforcement](../governance-enforcement/SKILL.md): deterministic tooling and CI.
- [Requirement Clarifier](../requirement-clarifier/SKILL.md): stabilize ambiguous scope before governance.
- [Regression Prevention](../regression-prevention/SKILL.md): implementation and change-safety evidence.
- [Project Backup](../project-backup/SKILL.md): external-state recovery point evidence.
- [Restore Drill](../restore-drill/SKILL.md): operational restore proof.
