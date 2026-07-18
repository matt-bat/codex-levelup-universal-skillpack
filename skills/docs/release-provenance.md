# Release Provenance

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
5. does not prove remote branch-protection settings

Record the exact pushed commit and its governance attestation without describing the branch push as a release.

## Next-Release Gate

Before publishing the next release:

1. version, tag, changelog, notes, skill count, and test count must describe the same commit
2. all required validators and semantic scenarios must pass on that commit
3. a governance plan and CI attestation must bind the governed diff to the exact commit
4. no required gate may be pending, failed, or unsupported by evidence
5. remote repository protection should require the governance check; configuring that protection is an external administrative action
