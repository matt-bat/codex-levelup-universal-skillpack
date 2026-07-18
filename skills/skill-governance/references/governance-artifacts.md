# Governance Artifact Lifecycle

## Version Policy

Use schema v3 for every new governed change. Continue to validate schema-v1 and schema-v2 records under their historical contracts, but treat every committed governance record as immutable.

Never modify, delete, or rebind a committed plan. Create a new task ID and an append-only superseding pair when facts, scope, evidence, or phase changes.

## Schema-v3 Pair

Commit both files together:

1. `docs/governance/<task-id>.governance.json`
2. `docs/governance/<task-id>.governance.md`

Treat JSON as the structured record. Require the Markdown file to equal the generator's canonical rendering of that JSON exactly. Complete and validate the pair before its first commit; CI rejects later modification or deletion, including add-then-modify and add-then-delete sequences inside one enforced commit range.

## Purpose

Use `purpose=change` for governed implementation or policy work. Bind its `change_binding` to the exact base revision and normalized governed-file manifest. Hash the Git-clean-filtered bytes from an isolated temporary index, not platform-specific working-tree bytes, so pre-commit and exact-head manifests remain identical.

Use `purpose=release` only with explicit `publish` authority and non-local execution scope. Bind it to the full base-to-candidate diff and include release metadata for:

1. Semantic version.
2. Matching `v<version>` tag name.
3. Version file path.
4. Dated changelog path.
5. Release-notes path and exact markers.
6. Catalog skill count.
7. Governance test count.

Require every release metadata path in the full manifest. Release enforcement accepts exactly one strict matching release artifact for the candidate head.

## Content and Catalog Binding

Record:

1. Immutable task ID and creation time.
2. Project identity snapshot and full risk inputs.
3. Purpose, execution scope, and operation-specific authority.
4. Exact base revision, normalized manifest, and manifest digest.
5. Required gates, evidence requirements, break-glass state, and recommendation.
6. Startup skills, rationale, and execution order.
7. Exact catalog path, digest, catalog version, router contract, components, and selected-skill relation snapshots.

Validate startup status, prerequisites, ordering, and conflicts against the embedded catalog snapshot. During CI, also verify the catalog digest, version, and router contract against the exact catalog at the enforced head.

Treat `change_binding` as a binding to repository content only. For a remote-only operation, separately record the exact target, before state, desired state, rollback procedure, and post-operation readback in typed evidence and audit references. Never claim that a Git manifest proves mutable external configuration.

## Remote Desired-State Evidence

Use these control surfaces together:

1. `.github/branch-protection-policy.json`: versioned desired state for the named GitHub repository and branch.
2. `skills/skill-governance/schemas/remote-configuration-policy.schema.json`: closed Draft 2020-12 policy shape.
3. `skills/skill-governance/scripts/verify_remote_configuration.py`: read-only target validation, normalization, and exact comparison.

Reject an invalid policy, mismatched response URL, unknown API field, malformed nested value, inconsistent status-check representation, or any normalized drift. Record the successful command result with its observation time and revision or digest when it supports a gate. Treat it as point-in-time evidence, not authority or a guarantee that mutable remote state remains unchanged.

## Typed Gate Evidence

For each schema-v3 evidence record, provide:

1. `kind`: `artifact`, `attestation`, `command`, `review`, or `test`, subject to gate-specific restrictions.
2. `reference`: a concrete, non-placeholder reference.
3. `result`: exactly `pass`.
4. `observed_at_utc`: an ISO-8601 time with timezone.
5. `revision_sha` or `sha256`: at least one exact content anchor.

Keep a gate pending until its real evidence exists. Treat a `pass` without evidence, a placeholder reference, a wrong evidence kind, an unanchored result, or an invalid timestamp as a validation failure.

## Break Glass

Enable break glass only for an allowed waiver. Record a concrete reason, risk owner, remediation ticket, and expiry from 1 through 168 hours.

Use `no-go` or `go-with-risk`, never `go`, when break glass supports a waiver. Do not waive `governance-enforcement`, `project-backup`, or `restore-drill` in schema v3. Keep disabled break-glass metadata empty and its expiry `null`.

## Attestation

Generate a CI attestation after checking out the exact candidate commit. Record:

1. Exact head and base commits.
2. Plan digest.
3. Normalized changed paths and digests.
4. Validation result and recommendation.
5. Whether release checks ran.

Keep the generated attestation outside the plan's self-referential manifest unless a separate repository contract explicitly governs it.

## Historical Artifacts

Preserve released, superseded, and legacy artifacts byte-for-byte. Validate their recorded schema and identity snapshot. Add a project alias, addendum, or superseding artifact instead of changing historical task facts.
