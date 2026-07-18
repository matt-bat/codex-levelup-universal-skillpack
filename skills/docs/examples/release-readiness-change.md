# Example: Release-Readiness Change

## Scenario
The user asks to prepare governed skillpack, CI, policy, or release artifacts for push.

This path is heavier because the change can affect future agent behavior or the evidence used to decide whether a change is safe to publish.

## Governed Route And Declaration
Because this work is governed, record the startup declaration. The minimal route for a repeatable release-validation workflow is:

1. `skill-governance`
2. `governance-enforcement`
3. `scripted-command-execution`

Add `doc-maintenance`, `interdependent-change-planning`, or `regression-prevention` only when their catalog triggers apply. Add `user-instructions-tracker` only when durable tracking is already opted in or the user explicitly requests ledger work. Do not add `token-reduction` or `order-of-operations` without their independent triggers.

## Why
1. governed files can alter future agent behavior
2. exact-commit CI and governance evidence must stay coherent
3. validation evidence must be durable and task-specific
4. optional documentation, planning, implementation, and tracking owners remain conditional

## Enough Validation
1. policy and catalog-derived-view validation
2. governance unit tests
3. strict validation of the current task's schema-v2 governance artifact
4. a clean checkout whose `HEAD` equals the exact candidate commit
5. exact-head enforcement with `--release-check` and an attestation output
6. version, changelog, release notes, skill/test counts, and any authorized local tag all equal the candidate commit
7. `git diff --check`

## Stop Rule
Do not push, publish, create or move a tag, or claim remote protection was verified unless the user separately authorizes that operation and the evidence exists.
