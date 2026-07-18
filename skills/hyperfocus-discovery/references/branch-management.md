# Branch Management

Use this reference only while `hyperfocus-discovery` is active and the task has real competing branches.

## Compact Stack

```text
Now: <current action>
Resume: <paused action and exact next step>
Spark: <candidate and why it matters>
Done: <completed action and evidence>
```

Keep only active notes. Collapse or discard notes once completed, rejected, or reported.

## Switch Gate

Switch only when at least two are true:
1. the branch may prevent a bug, rework, or missed requirement
2. it can be validated quickly
3. it unlocks a blocked required step
4. it materially improves the requested result
5. the current branch has a precise resume point

User approval is required before a branch introduces a new dependency, migration, design direction, external side effect, or materially broader deliverable.

## Priority

Choose branches in this order:
1. prevent data loss, security issues, or irreversible mistakes
2. recover a missed explicit requirement
3. unblock reproduction or validation
4. reduce rework inside the approved implementation path
5. improve quality without broadening scope

Defer everything else.

## Convergence Sweep

1. List active `Resume` and `Spark` notes privately.
2. Mark each `done`, `deferred`, or `rejected`.
3. Restore the primary task's exact next step.
4. Recheck requirements, authorization, and validation.
5. Surface a deferred item only if it is useful to the user.

Do not expose the full private stack unless the user asks for it.
