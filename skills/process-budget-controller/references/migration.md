# Process Budget Controller Migration

## Deprecation Record

- Item: `process-budget-controller`
- State: `deprecated`
- First deprecated: 2026-07-17
- Replacement: routing architecture version 2 task router
- Reason: selecting a skill to limit skill selection adds process overhead and creates circular routing pressure
- Wrapper behavior: explicit legacy invocation explains the current budget and emits the canonical router name; it never auto-activates or counts as an active selection
- Removal criteria: at least 30 representative tasks or two releases, safety-scenario parity, zero unexplained alias failures, no material outcome regression, and exact-commit green release evidence
- Rollback trigger: preserve or restore the wrapper if explicit legacy invocation breaks, safety gates disappear, historical artifacts stop validating, or measured corrections, retries, failures, or latency materially worsen

## Replacement

Use the active router's minimum-selection policy:
1. select a primary skill only when it changes task execution
2. add a safety or validation skill only when risk requires it
3. add an execution tool skill only when the task needs that tool workflow
4. do not add a skill solely to explain or cap other skills

## Legacy Tier Interpretation

For compatibility with existing artifacts:
1. `tiny`: up to two active skills, no new artifact, one cheap relevant check
2. `small`: up to four active skills, no governance artifact unless governed scope requires one
3. `standard`: up to eight active skills with targeted evidence
4. `critical`: required safety gates override the numeric ceiling

These are legacy advisory limits. New routing policy may use different tiers or no numeric tier.

## Compatibility Handling

1. Preserve legacy tier values when reading historical records.
2. Do not rewrite old artifacts merely to rename the controller.
3. Map the old tier to current router policy only when the task depends on it.
4. Record deprecation or replacement details in shared lifecycle artifacts only when that work is separately authorized.
