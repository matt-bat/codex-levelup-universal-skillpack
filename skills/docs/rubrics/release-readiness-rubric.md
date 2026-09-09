# Release Readiness Rubric

[Documentation home](../README.md) · [Documentation quality](./documentation-quality-rubric.md) · [Skillpack quality](./skillpack-quality-rubric.md)

Use this rubric before making a local ready-to-push or ready-to-release claim for governed changes.

The question is not "did the edit look right?" The question is whether the repository state, validation evidence, documentation, authority, and residual risk support the exact claim being made.

| Category | Governed push weight | Release weight | Checks |
|---|---:|---:|---|
| Git state | 15 | 10 | exact candidate commit known; `HEAD` equals it; checkout is clean, including untracked files |
| Governance | 25 | 20 | new append-only schema-v3 artifact; typed evidence; exact catalog binding; canonical JSON/Markdown pair; strict validation returns `go` |
| Validation | 25 | 20 | policy, catalog-derived views, tests, exact-head enforcement, and attestation pass for the candidate |
| Release provenance | 0 | 20 | exactly one purpose=`release` v3 artifact; explicit `publish` authority; full-diff binding; exact version, tag, changelog, notes, skill count, and governance test count |
| Documentation | 15 | 10 | README, usage docs, changelog, and examples reflect the candidate; tracker changes appear only when required by scope or contract |
| Safety | 10 | 10 | no push, publication, deployment, tag mutation, deletion, migration, message, or remote-setting change occurs without operation-specific authority |
| Residual risk | 10 | 10 | remaining risks, skipped checks, mutable remote facts, and external blockers are explicit and acceptable |

Choose the weight column that matches the claim. Score each category from 0 to 5, multiply by its weight, then divide the total by 5. A zero-weight release-provenance category does not apply to an ordinary governed push.

## Blocking Conditions For Any Governed Claim

1. `HEAD` differs from the intended candidate or the checkout is not clean
2. the current task lacks a new schema-v3 artifact binding the exact base, catalog, and applicable manifest
3. a committed governance artifact was modified or deleted instead of superseded by a new task record
4. the governance JSON and canonical Markdown pair differ
5. catalog validation fails or any generated routing view differs from catalog output
6. a required test, exact-head enforcement, or attestation fails
7. a required gate is pending, failed, waived, or unsupported by typed evidence for a `go` recommendation
8. the worktree contains unexplained changes

## Additional Release Blocking Conditions

1. there is not exactly one matching strict purpose=`release` schema-v3 artifact
2. explicit `publish` authority is absent
3. the artifact binds only governed paths instead of the full candidate diff
4. release metadata differs from the exact version, tag, changelog, release notes, skill inventory, or governance test inventory at the candidate
5. an existing local or remote tag resolves to another commit
6. the remote protection or required-check state is assumed from an old observation instead of reverified for the release claim

If any applicable blocking condition is present, do not call the change ready. Fix the blocker or clearly report that readiness is not achieved.

## Remote Boundary

The workflow runs the `governance` job on every pull request targeting protected `main`, but it requires a v3 plan only for governed diffs. `main` protection, administrator enforcement, force-push/deletion blocks, and the required `governance` check were verified on 2026-07-18. That evidence is mutable and must be rechecked before making a current remote-state claim.

This rubric does not grant authority to push, publish, create or move tags, deploy, or configure remote settings. Those are separate operations.
