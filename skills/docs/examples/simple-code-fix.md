# Example: Simple Code Fix

## Scenario
User asks for a narrow bug fix with a clear file and expected behavior.

## Skills In Use
1. `token-reduction`
2. `order-of-operations`
3. `scripted-command-execution`
4. `regression-prevention`

## Why
1. keep output concise
2. inspect before editing
3. run deterministic checks
4. avoid breaking the touched behavior

## Enough Validation
1. targeted unit or static check for the touched code
2. affected test update when behavior changed
3. final `git status --short`

## Stop Rule
Do not generate a governance artifact unless the changed path is governed or the fix is release-affecting.
