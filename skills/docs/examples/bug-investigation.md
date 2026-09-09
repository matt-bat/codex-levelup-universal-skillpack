# Example: Bug Investigation

[Documentation home](../README.md) · [Simple code fix](./simple-code-fix.md) · [Frontend layout](./frontend-layout-task.md)

## Scenario
The user reports a failure or suggests a possible cause, but the root cause is not proven.

In this path, the agent should avoid patching based only on the first plausible explanation. Reproduce or inspect enough to separate symptoms from cause.

## Minimal Route
Select `diagnose-before-fix` because the cause is unverified.

Add another skill only if its independent trigger appears:

1. `regression-prevention` when an authorized fix will change non-trivial behavior
2. `scripted-command-execution` when the deliverable is a repeatable diagnostic command workflow, not merely because an incidental command runs

This routine route does not need a startup declaration unless the user explicitly asks for one or the work becomes governed or audited.

## Why
1. reproduce before patching when practical
2. separate symptoms from verified cause
3. add implementation or command owners only after their effects are known
4. choose validation based on affected behavior

## Enough Validation
1. reproduction command or documented blocked reproduction
2. root-cause evidence
3. targeted regression test or rationale when not practical
4. final residual-risk note

## Stop Rule
Do not patch multiple suspected causes at once unless evidence shows they are coupled.
