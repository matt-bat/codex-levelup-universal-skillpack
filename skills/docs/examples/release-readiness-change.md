# Example: Release-Readiness Change

## Scenario

The user asks to prepare governed skillpack, CI, policy, or release artifacts for push.

This path is heavier because the change can affect future agent behavior or the evidence used to decide whether a change is safe to publish.

## Governed Route And Declaration

Because this governed work needs a durable routing record, record the startup declaration. The minimal route for a repeatable release-validation workflow is:

1. `skill-governance`
2. `governance-enforcement`
3. `scripted-command-execution`

Add `doc-maintenance`, `interdependent-change-planning`, or `regression-prevention` only when their catalog triggers apply. Add `user-instructions-tracker` only when durable tracking is explicitly requested or an existing repository contract would otherwise become inaccurate. Do not add another skill merely because it is adjacent to release work.

## Why

1. governed files can alter future agent behavior
2. exact-commit CI and governance evidence must stay coherent
3. validation evidence must be durable and task-specific
4. optional documentation, planning, implementation, and tracking owners remain conditional

## Choose The Artifact Purpose

For an ordinary governed feature-branch push or pull request, add a unique schema-v3 artifact with purpose=`change`. Record only the operations actually authorized. The plan binds the exact catalog and governed diff.

For a release-publication claim, add a separate purpose=`release` v3 artifact. It requires explicit `publish` authority, exact version/tag/path/count metadata, and a binding over the full candidate diff. Exactly one matching strict release artifact may authorize the exact release head.

In both cases, gate evidence is typed, timestamped, and anchored to a revision or digest. The paired Markdown must be the generator's canonical rendering, and committed governance records are append-only.

## Enough Validation

1. policy, catalog, and generated-view validation
2. governance unit tests and routing scenarios
3. strict validation of the current task's schema-v3 artifact and canonical Markdown pair
4. a clean checkout whose `HEAD` equals the exact candidate commit
5. exact-head enforcement and an attestation output
6. for a release only, `--release-check` plus exact version, tag, changelog, release notes, skill count, governance test count, and any authorized tag target
7. `git diff --check`

## Protected-Main Flow

`main` is protected as verified on 2026-07-18. Push an authorized feature branch, open a pull request, and wait for the required `governance` check. The job runs on every pull request targeting `main`; only governed diffs require a v3 plan.

## Stop Rule

Do not push, publish, create or move a tag, deploy, or change remote settings unless the user separately authorizes that exact operation and the evidence exists. Recheck mutable remote protection before claiming its current state.
