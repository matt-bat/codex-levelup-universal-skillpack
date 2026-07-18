# Task Contract Schema

Use this reference for multi-deliverable, governed, or authorization-sensitive work.

## Contents

1. Contract shape
2. Requirement records
3. Authority records
4. Completion ledger

## Contract Shape

```yaml
deliverables:
  - id: D1
    outcome: "Observable result"
    acceptance_criteria: [A1]
requirements:
  - id: R1
    text: "Requirement in full language"
    source: explicit_user
    confidence: certain
    materiality: high
    status: active
constraints:
  - id: C1
    text: "Do not push"
    kind: prohibition
authority:
  inspect: allowed
  write_local_files: allowed
  run_commands: allowed
  commit: denied
  push: denied
  publish: denied
  deploy: denied
uncertainties: []
```

## Requirement Records

Use `confidence` values `certain`, `high`, `medium`, or `low`. Use `materiality` values `low`, `medium`, `high`, or `critical`.

Ask when an uncertainty is both material and outcome-changing. Do not ask merely because multiple safe implementation details exist.

Use `status` values:

1. `active`
2. `superseded`
3. `satisfied`
4. `verified`
5. `unverified`
6. `deferred`
7. `blocked`

Keep a superseded record and identify its successor instead of silently replacing history.

## Authority Records

Track authority separately for:

1. inspection
2. local file mutation
3. command execution
4. dependency installation
5. commit
6. push
7. deletion or migration
8. external messages
9. deployment
10. publication or release

General permission to edit code does not imply authority for external or irreversible actions.

## Completion Ledger

At handoff, include every deliverable, prohibition, and acceptance criterion once. A response compositor may shorten wording but may not remove status, evidence, uncertainty, or a safety veto.
