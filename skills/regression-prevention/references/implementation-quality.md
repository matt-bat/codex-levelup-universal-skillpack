# Implementation Quality

Use this reference for non-trivial construction or refactoring.

## Repository Discovery

1. Read applicable instructions before editing.
2. Inspect the dirty worktree and separate user changes from task changes.
3. Locate neighboring implementations, tests, types, and error conventions.
4. Trace inputs, outputs, callers, persistence, and external boundaries.
5. Prefer repository-native utilities and patterns over new abstractions.

## Construction Standard

1. Implement the smallest coherent behavior change.
2. Keep functions and modules single-purpose at the repository's existing granularity.
3. Preserve static types; avoid broad casts or suppressed errors without a documented reason.
4. Make error behavior explicit, actionable, and compatible with callers.
5. Validate inputs at trust boundaries, not redundantly everywhere.
6. Avoid speculative generalization and premature framework work.
7. Remove superseded code only when callers and compatibility windows are resolved.

## Conditional Reviews

Run only when the changed surface warrants them:

### Security

Check authorization, validation, secret handling, injection, session state, privilege changes, and sensitive logging.

### Performance

Check algorithmic growth, repeated I/O, query count, memory retention, bundle size, or hot-path latency.

### Concurrency and State

Check races, idempotency, retries, transaction boundaries, partial failure, and stale state.

## Final-Diff Review

1. Compare the diff against each requirement.
2. Remove accidental formatting churn and debug output.
3. Check unused imports, dead branches, duplicated helpers, and stale comments.
4. Verify names describe behavior and public contracts remain intentional.
5. Confirm docs and tests reference current commands, paths, and behavior.
6. Ensure no secrets, generated noise, or unrelated files entered the diff.
