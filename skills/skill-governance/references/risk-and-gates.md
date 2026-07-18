# Risk and Gates

## Routine Local

Examples: bounded answer, inspection, or tiny reversible edit.

Create no governance artifact. Apply core authorization policy and proportional validation.

## Significant Local

Examples: cross-cutting source refactor, routing policy, validator logic, or compatibility-sensitive API design without live execution.

Require:

1. Stable task contract.
2. Dirty-worktree preservation.
3. Impact and rollback analysis.
4. Relevant regression evidence.
5. Governance enforcement when governance or release controls change.
6. Documentation evidence when behavior or workflow paths change.

## External Reversible

Require significant-local controls plus:

1. Exact operation-specific authority.
2. Target identity and environment verification.
3. Actionable rollback or recovery evidence.
4. Post-operation validation.
5. Exact operation audit evidence.

Treat `configure_remote`, push, publish, deploy, delete, migrate, and message as distinct authorities. Never infer one from another.

### GitHub Branch-Protection Verification

Compare current state with the checked-in desired state using the read-only canonical command in [Protected-Main Snapshot](../../docs/release-provenance.md#protected-main-snapshot).

Require repository read access and an authenticated `gh` session, but do not require or infer `configure_remote` authority for this verification. Fail closed on an invalid closed-schema policy, target mismatch, unsupported API field, malformed response, or drift. Do not repair drift unless `configure_remote` is separately authorized and every critical pre-action gate passes. Re-run the same verifier after an authorized change and record the fresh result as post-operation evidence.

## External Critical

Force critical mode for authorized `configure_remote`, `delete`, `deploy`, `migrate`, or `publish`, regardless of numeric score. Also use critical mode for explicit critical overrides, release purpose, and other destructive, irreversible, production-sensitive, or recovery-unknown work.

Require external-reversible controls plus:

1. Stop conditions and a named risk owner.
2. No unresolved critical validation gap.
3. Explicit final approval when active policy requires it.
4. A current backup when non-reconstructable state has credible loss exposure.
5. A verified restore path when execution requires recovery proof.

Always require both backup and restore controls for authorized `delete` or `migrate`. Require rollback evidence for remote configuration and deployment; do not add backup or restore solely because an operation is external.

## Deterministic Mode Gates

The schema-v3 generator derives gates from mode:

| Mode | Required gates |
|---|---|
| Quick | Execution skill |
| Standard | Execution skill; `regression-prevention` |
| Critical | Execution skill; `regression-prevention`; `semantic-policy-audit`; `governance-enforcement` |

Add `doc-maintenance` when behavior or workflow paths change. Add `project-backup` for typed backup risk. Add both `project-backup` and `restore-drill` when restore proof is required.

Use gate-specific evidence kinds:

| Gate | Accepted evidence kinds |
|---|---|
| `scripted-command-execution` | `attestation`, `command`, `test` |
| `pseudo-agentic-automation` | `artifact`, `attestation`, `test` |
| `regression-prevention` | `attestation`, `command`, `test` |
| `semantic-policy-audit` | `artifact`, `attestation`, `review` |
| `governance-enforcement` | `attestation`, `command`, `test` |
| `doc-maintenance` | `artifact`, `attestation`, `review` |
| `project-backup` | `artifact`, `attestation` |
| `restore-drill` | `artifact`, `attestation`, `test` |

Every passing evidence record must include a concrete reference, `result=pass`, a timezone-bearing observation time, and a revision SHA or SHA-256 digest.

## Break Glass

Allow break glass only for a permitted waiver with a concrete reason, risk owner, remediation ticket, and 1-to-168-hour expiry. Use `no-go` or `go-with-risk`; break glass can never support `go`.

Never waive:

1. `governance-enforcement`.
2. `project-backup`.
3. `restore-drill`.

## Conditional Domains

Add domain checks without automatically changing operational effect:

- Authentication/security: authorization, privilege, session, secret, and sensitive logging.
- Financial: precision, idempotency, reconciliation, and audit trail.
- Schema/data: mixed-version reads, malformed legacy rows, reversibility, and integrity.
- Public API: consumer inventory, compatibility, deprecation, and versioning.
- Release: exact commit, provenance, metadata, and immutable evidence.

Never limit mandatory safety gates by a skill-count or process budget.
