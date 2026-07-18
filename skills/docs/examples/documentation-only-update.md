# Example: Documentation-Only Update

## Scenario
The user asks to update copy, usage docs, policy docs, or release notes without changing runtime behavior.

This can still matter because docs often define how an agent behaves next. Treat routing, validation, and policy docs more carefully than ordinary wording changes.

## Minimal Route
Select `doc-maintenance` because documentation is the requested deliverable.

Do not also select `file-maintenance` for the same documentation-accuracy decision. Add it only when file hygiene, duplication, or stale-file cleanup is a separate requested outcome. Add `order-of-operations` only when the documents have real dependency order.

This routine route does not need a startup declaration unless the user explicitly asks for one or the work becomes governed or audited.

## Why
1. update the canonical source before dependent references
2. preserve consistency without stacking overlapping owners
3. verify paths and commands still match the repository

## Enough Validation
1. path or link existence check for changed references
2. policy validator if docs affect skill behavior
3. `git diff --check`

## Stop Rule
Do not add governance artifacts for pure non-governed copy edits unless the changed path or release decision requires them.
