# Example: Documentation-Only Update

## Scenario
The user asks to update copy, usage docs, policy docs, or release notes without changing runtime behavior.

This can still matter because docs often define how an agent behaves next. Treat routing, validation, and policy docs more carefully than ordinary wording changes.

## Skills In Use
1. `token-reduction`
2. `order-of-operations`
3. `doc-maintenance`
4. `file-maintenance`

## Why
1. keep the response concise
2. update canonical docs before dependent references
3. preserve consistency across related files
4. verify paths and commands still match the repository

## Enough Validation
1. path or link existence check for changed references
2. policy validator if docs affect skill behavior
3. `git diff --check`

## Stop Rule
Do not add governance artifacts for pure non-governed copy edits unless the changed path or release decision requires them.
