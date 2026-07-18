# Test Patterns

## Unit Tests

1. Use arrange-act-assert or the repository's established equivalent.
2. Keep one behavioral intent per case.
3. Use table-driven cases for branch-heavy logic.
4. Cover invalid, empty, boundary, retry, and error behavior where relevant.
5. Avoid order dependence and uncontrolled global state.

## Integration and Contract Tests

1. Exercise the real boundary with the smallest practical controlled environment.
2. Assert observable contracts, not internal call counts unless the call itself is the contract.
3. Cover serialization, status, error, idempotency, and compatibility behavior.
4. Isolate external services with stable fakes only when the real boundary cannot safely run.

## Browser Tests

1. Prefer accessible roles, labels, text, and stable test identifiers.
2. Use web-first assertions and built-in waiting; avoid fixed sleeps.
3. Keep authentication and state setup explicit and reusable.
4. Validate loading, success, error, and recovery states for critical flows.
5. Capture traces or screenshots on failure when the runner supports them.

## Flake Handling

1. Allow at most one diagnostic retry unless repository policy differs.
2. Mark a retry-pass as suspected flakiness, not an unconditional success.
3. Fix or quarantine with ownership and evidence; do not normalize repeated retries.
