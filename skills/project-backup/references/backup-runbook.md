# Backup Runbook

## Asset Inventory

Classify assets as:

1. non-reconstructable business or user data
2. operational configuration and deployment state
3. reconstructable source, dependencies, caches, and build output

Prioritize non-reconstructable data. Do not copy secrets into an ordinary repository archive.

## Implementation Requirements

For scripts or scheduled jobs:

1. accept an explicit destination and target profile
2. use timestamped output and clear exit codes
3. fail on partial backup
4. generate and verify integrity metadata
5. exclude caches and uncontrolled secret files
6. log concise progress without credentials
7. document retention and ownership

For sensitive or offsite data, require encryption at rest, least-privilege access, and key recovery procedures.

## Verification

1. Check expected files, entities, or database sections.
2. Verify checksums or platform-native integrity.
3. Confirm format and version compatibility with restore tooling.
4. Record backup timestamp against the recovery point objective.
5. Use an isolated restore drill when operational policy requires proof.

## Failure Conditions

Block the operation when:

1. the latest artifact is stale
2. integrity fails
3. critical assets are missing
4. restore credentials or tooling are unavailable
5. retention may have removed the last usable recovery point
