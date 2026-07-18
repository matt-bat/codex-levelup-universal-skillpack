# Risk and Gates

## Routine Local

Examples: bounded answer, inspection, tiny reversible edit.

Governance artifact: none. Use proportional validation and core authorization policy.

## Significant Local

Examples: cross-cutting source refactor, routing policy, validator logic, compatibility-sensitive API design without live execution.

Require:

1. stable task contract
2. dirty-worktree preservation
3. impact and rollback analysis
4. relevant regression evidence
5. governance enforcement when policy or release controls change

## External Reversible

Require significant-local gates plus:

1. target-specific authority
2. target identity and environment check
3. rollback mechanism tested or independently verified
4. post-operation validation
5. exact operation audit evidence

## External Critical

Require external-reversible gates plus:

1. current backup covering exposed non-reconstructable state
2. verified restore path or policy-approved freshness evidence
3. stop conditions and named risk owner
4. no unresolved critical validation gap
5. explicit final approval where repository policy requires it

## Conditional Domains

Domain review adds checks without automatically changing operational effect:

- authentication/security: authorization, privilege, session, secret, and sensitive logging
- financial: precision, idempotency, reconciliation, audit trail
- schema/data: mixed-version reads, malformed legacy rows, reversibility, integrity
- public API: consumer inventory, compatibility, deprecation, versioning
- release: exact commit, provenance, immutable evidence

Mandatory safety gates are never limited by a skill-count or token budget.
