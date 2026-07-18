# Governance Artifact Lifecycle

## Plan

A committed plan records:

1. schema version and immutable task ID
2. project identity snapshot
3. base revision
4. normalized governed-change manifest, excluding the plan's own digest
5. required gates and expected evidence
6. authority and external-effect boundaries

Pending gates imply `no-go`.

## One Diff, One Binding

Every schema-version-2 plan added or modified in the same governed diff must bind the same exact base revision and governed manifest. CI validates every changed plan; one correctly bound plan cannot mask another changed, stale plan.

Commit phase-specific snapshots separately when their manifests differ, or keep intermediate working-tree plans out of the final commit. Rebind every version 2 plan that remains changed after the final diff.

## Evidence

Each gate records status, evidence references, and optional waiver metadata. A `pass` without evidence is invalid. A waiver requires a concrete reason, owner, expiry or removal condition, and must not bypass a non-waivable safety invariant.

## Attestation

CI emits an attestation containing:

1. exact head commit
2. base commit
3. plan digest
4. normalized changed paths and digests
5. validator and test results
6. final recommendation

The attestation is generated after checkout and is not included in the plan's self-referential manifest.

## Historical Artifacts

Released or superseded artifacts are immutable. Validate legacy versions under their recorded schema and identity snapshot. Record a project alias, addendum, or superseding artifact instead of changing old task facts.
