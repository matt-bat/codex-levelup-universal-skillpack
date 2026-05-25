# Example: Release-Readiness Change

## Scenario
The user asks to prepare governed skillpack, CI, policy, or release artifacts for push.

This path is heavier because the change can affect future agent behavior or the evidence used to decide whether a change is safe to publish.

## Skills In Use
1. `token-reduction`
2. `order-of-operations`
3. `skill-governance`
4. `governance-enforcement`
5. `interdependent-change-planning`
6. `regression-prevention`
7. `scripted-command-execution`
8. `doc-maintenance`
9. `user-instructions-tracker`

## Why
1. governed files can alter future agent behavior
2. CI, docs, validators, and artifacts must stay coherent
3. validation evidence must be durable
4. user directives need closure evidence

## Enough Validation
1. policy validator
2. skill ordering sync validator
3. strict governance artifact validation
4. governance unit tests
5. `git diff --check`

## Stop Rule
Do not push automatically unless the user explicitly asks for a push and credentials or network access are available.
