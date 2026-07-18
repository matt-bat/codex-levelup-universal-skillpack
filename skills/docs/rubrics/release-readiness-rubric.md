# Release Readiness Rubric

Use this rubric before making a local ready-to-push or ready-to-release claim for governed changes.

The question is not "did the edit look right?" The question is whether the repository state, validation evidence, documentation, and residual risk support a push-ready claim.

| Category | Weight | Checks |
|---|---:|---|
| Git state | 15 | exact candidate commit known; `HEAD` equals it; checkout is clean, including untracked files |
| Governance | 20 | current-task schema-v2 artifact binds the exact base and manifest; strict validation returns `go` |
| Validation | 20 | policy, catalog-derived views, tests, and exact-head `--release-check` pass; attestation is written |
| Release provenance | 20 | version, changelog, notes, counts, intended tag, and local tag target all equal the candidate commit |
| Documentation | 10 | README, usage docs, changelog, and examples reflect the candidate; tracker changes are included only when opted in |
| Safety | 10 | no push, publication, deployment, tag mutation, or remote-setting change occurs without separate authority |
| Residual risk | 5 | remaining risks are explicit and acceptable |

Score each category from 0 to 5, multiply by weight, then divide by 5.

## Blocking Conditions
1. `HEAD` differs from the intended candidate or the checkout is not clean
2. the current-task governance artifact does not bind the exact base, manifest, and candidate
3. catalog validation fails or any generated routing view differs from catalog output
4. required tests or exact-head `--release-check` fail, or no attestation is produced
5. version, changelog, release notes, skill/test counts, or an existing local tag describe another commit
6. a required gate is pending, failed, waived, or unsupported by evidence for a `go` recommendation
7. the worktree contains unexplained changes

If any blocking condition is present, do not call the change ready to push. Fix the blocker or clearly report that readiness is not achieved.

This rubric establishes local evidence only. It does not verify remote tag state, branch protection, required remote checks, or publication status; report those as external checks and never imply they were verified locally.
