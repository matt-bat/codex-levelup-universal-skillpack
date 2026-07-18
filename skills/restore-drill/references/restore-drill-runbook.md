# Restore Drill Runbook

## Charter

Record drill type, target, artifact, participants, recovery objectives, scope, start conditions, stop conditions, and cleanup authorization.

## Execution Phases

1. Verify artifact completeness, integrity, encryption access, and version compatibility.
2. Restore code/configuration where applicable.
3. Restore database or state stores.
4. Restore media or object data.
5. Start services and verify dependencies.
6. Validate critical functions, representative data, permissions, and sensitive logging.
7. Calculate achieved recovery point and recovery time.
8. Record remediation, owners, and due dates.

## Failure Variants

Rotate realistic controlled failures:

1. corrupt latest artifact
2. unavailable decryption key
3. database version mismatch
4. incomplete object/media segment
5. expired credential
6. unavailable network dependency

Never inject a failure into production without explicit, target-specific authority.

## Evidence Bundle

Include artifact identity, integrity results, ordered execution log, validation results, timing calculations, remediation, and final gate state. Missing evidence makes the drill invalid.
