# Release Provenance

[Documentation home](./README.md) · [Governance walkthrough](./governance-walkthrough.md) · [Release-readiness rubric](./rubrics/release-readiness-rubric.md)

## Version 1.0.0 Record

The published `v1.0.0` release is retained as historical evidence and must not be retagged or rewritten.

Known mismatch:

1. the tag points to commit `c5de9a9`
2. that snapshot contains 29 skill packages and 15 governance test methods across 4 test files
3. the published release body describes 21 skills and 9 tests from an earlier repository state
4. the tagged commit's governance workflow failed
5. later branding commits do not change the contents of the existing tag

This mismatch does not invalidate Git history, but it prevents treating the release description as a reproducible inventory of the tag.

## Correction Policy

1. Do not move or recreate `v1.0.0`.
2. Preserve dated governance artifacts under their original schema and task identity.
3. Record corrections in a subsequent patch or minor release.
4. Generate release notes from the exact candidate commit.
5. Require a green governance attestation for that exact commit before publication.

## Branch Push Versus Release

Routing architecture version 2 remains under the changelog's `Unreleased` section and the version file remains `1.0.0` until a separately authorized release changes them together.

A normal push of the source commit to a repository branch:

1. makes the commit available on that branch
2. does not create or move a version tag
3. does not publish hosted release notes or artifacts
4. does not change the released version
5. does not by itself prove current remote branch-protection settings

Record the exact pushed commit and its governance attestation without describing the branch push as a release.

## Protected-Main Snapshot

Remote controls were verified on 2026-07-18 with this observed state:

1. `main` is protected
2. the strict required status check is `governance` from GitHub App ID `15368`
3. administrator enforcement is enabled
4. force pushes and branch deletion are blocked
5. approving reviews and signed commits are not required
6. no repository rulesets were present
7. governance workflow run `29626961080` completed successfully

The matching desired state is versioned at [../../.github/branch-protection-policy.json](../../.github/branch-protection-policy.json) and validated against the closed [remote-configuration-policy schema](../skill-governance/schemas/remote-configuration-policy.schema.json). The policy rejects unknown fields, but a valid policy is not proof of current remote state.

From the repository root, compare a fresh GitHub branch-protection response with the desired state:

```sh
gh api repos/matt-bat/agent-command-center/branches/main/protection \
  | python3 skills/skill-governance/scripts/verify_remote_configuration.py \
      --policy .github/branch-protection-policy.json \
      --actual -
```

This command is read-only. It verifies the response URL targets the declared repository and branch, normalizes the supported GitHub fields, and exits nonzero on an unknown field or any desired-state drift. It requires authenticated `gh` access and the pinned Python dependencies. It does not inspect repository rulesets or grant authority to run a `configure_remote` mutation.

This remains a point-in-time observation, not a permanent guarantee. Recheck protection and the required check before relying on a current remote-state claim. Changing the policy file does not change GitHub. Changing protection is a separately authorized `configure_remote` operation; pushing a branch does not authorize that change, and configuring the remote does not authorize a push.

With this protection in place, prepare changes on a feature branch and merge through a pull request after the required `governance` job passes. The workflow runs on every pull request targeting `main`. A non-governed diff still receives policy and regression checks but does not require a governance plan; a governed diff requires a new schema-v3 plan.

## Governance Record Lifecycle

New governed changes use schema-v3 JSON and canonical Markdown pairs. Each record includes typed, revision- or digest-bound gate evidence, operation-specific authority, the exact catalog version/digest and selected-skill relations, and the exact governed manifest.

Committed governance records are append-only across the full commit range. Schema-v1 and schema-v2 records remain readable historical evidence, but they must not be edited, deleted, or reused to authorize a new governed change. Later corrections require a new task identity and superseding record.

## Next-Release Gate

Before publishing the next release:

1. use exactly one strict schema-v3 artifact with purpose=`release` and explicit `publish` authority
2. version, tag, changelog, release notes, skill count, and governance test count must match the artifact metadata and describe the same commit
3. the release artifact must bind the full candidate diff, including its version, changelog, and release-notes files
4. all required validators and semantic scenarios must pass on that commit, with typed gate evidence and an exact-head CI attestation
5. no required gate may be pending, failed, waived, or unsupported by evidence for a `go` recommendation
6. reverify the remote tag target, protected `main` settings, and required `governance` check before publication

Generating or validating release evidence does not create a tag, publish a release, push a branch, or alter remote settings. Each external operation requires its own explicit authority.
