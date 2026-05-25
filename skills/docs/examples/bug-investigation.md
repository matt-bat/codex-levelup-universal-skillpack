# Example: Bug Investigation

## Scenario
The user reports a failure or suggests a possible cause, but the root cause is not proven.

In this path, the agent should avoid patching based only on the first plausible explanation. Reproduce or inspect enough to separate symptoms from cause.

## Skills In Use
1. `token-reduction`
2. `order-of-operations`
3. `diagnose-before-fix`
4. `scripted-command-execution`
5. `regression-prevention`

## Why
1. keep investigation focused
2. reproduce before patching when practical
3. separate symptoms from verified cause
4. run deterministic diagnostics
5. choose validation based on affected behavior

## Enough Validation
1. reproduction command or documented blocked reproduction
2. root-cause evidence
3. targeted regression test or rationale when not practical
4. final residual-risk note

## Stop Rule
Do not patch multiple suspected causes at once unless evidence shows they are coupled.
