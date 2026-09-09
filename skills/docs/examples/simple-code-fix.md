# Example: Simple Code Fix

[Documentation home](../README.md) · [Bug investigation](./bug-investigation.md) · [Frontend layout](./frontend-layout-task.md)

## Scenario
The user asks for a narrow bug fix with a clear file and expected behavior.

The task does not need heavy governance, but it still needs basic inspection and a targeted check.

## Minimal Route
Use the zero-skill route when the fix is mechanical, reversible, and already covered by core policy. Select `regression-prevention` when the fix changes non-trivial logic or behavior.

Add `diagnose-before-fix` only if the cause is unverified. Running an existing targeted command is incidental and does not by itself activate `scripted-command-execution`; obvious local ordering does not activate `order-of-operations`.

This routine route does not need a startup declaration unless the user explicitly asks for one or the work becomes governed or audited.

## Why
1. inspect before editing
2. preserve the touched behavior and repository conventions
3. add diagnosis or implementation workflow only when its trigger applies
4. run proportionate targeted checks

## Enough Validation
1. targeted unit or static check for the touched code
2. affected test update when behavior changed
3. final `git status --short`

## Stop Rule
Do not generate a governance artifact unless the changed path is governed or the fix is release-affecting.
