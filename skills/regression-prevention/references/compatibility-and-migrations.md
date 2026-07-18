# Compatibility and Migrations

## Contract Changes

1. Prefer additive evolution.
2. Identify every current consumer before removing or renaming fields.
3. Provide adapters, deprecation windows, or versioning when consumers cannot move atomically.
4. Test success and failure contracts, serialization, status codes, and idempotency.

## Data and Schema Work

Separate source design from live execution.

For source-only changes:

1. inspect existing data assumptions
2. design expand-then-contract where possible
3. provide backfill/default behavior
4. document reversibility and mixed-version behavior

For authorized execution against external data:

1. require target identity and authority
2. require current backup and verified restore path when loss is possible
3. validate representative volume and malformed legacy rows
4. observe execution and define stop conditions
5. verify post-migration integrity before cleanup

Never infer permission to apply a migration from permission to write its source file.

## Dependency Changes

1. Read authoritative release and migration notes.
2. Upgrade the smallest necessary scope.
3. Identify removed APIs and runtime constraints.
4. Validate startup, affected contracts, and rollback feasibility.
