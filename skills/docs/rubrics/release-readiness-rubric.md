# Release Readiness Rubric

Use this rubric before calling governed changes ready to push.

The question is not "did the edit look right?" The question is whether the repository state, validation evidence, documentation, and residual risk support a push-ready claim.

| Category | Weight | Checks |
|---|---:|---|
| Git state | 15 | branch known; remote known; worktree intentional; generated files excluded |
| Governance | 20 | artifact present; strict validation passes; recommendation is acceptable |
| Validation | 20 | policy validator, order sync, tests, and changed-path enforcement pass |
| Documentation | 15 | README, usage docs, changelog, tracker, and examples reflect the change |
| Safety | 15 | no deployment unless requested; rollback or restore gates addressed when needed |
| Portability | 10 | line endings stable; commands use repo-root paths; public docs are coherent |
| Residual risk | 5 | remaining risks are explicit and acceptable |

Score each category from 0 to 5, multiply by weight, then divide by 5.

## Blocking Conditions
1. strict governance artifact validation fails
2. skill map and skill index order diverge
3. generated cache files are staged
4. worktree contains unexplained changes
5. recommendation is below required release threshold

If any blocking condition is present, do not call the change ready to push. Fix the blocker or clearly report that readiness is not achieved.
