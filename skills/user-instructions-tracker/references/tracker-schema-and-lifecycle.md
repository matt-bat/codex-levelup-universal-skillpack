# Tracker Schema and Lifecycle

Use this reference only after the recordability and authorization gates in `SKILL.md` pass.

## Preferred Structure

Use separate sections in a newly initialized or explicitly migrated ledger.

### Current Directives

Recommended columns:
1. `Instruction ID`
2. `Current Directive`
3. `Source`
4. `Lifecycle`
5. `Priority`
6. `Owner`
7. `Last Confirmed UTC`
8. `Successor or Notes`

Keep only `active`, `superseded`, `stale`, or `retired` lifecycle values. Active rows are current truth; other rows remain for lineage.

### Fulfillment History

Compatibility columns:
1. `Instruction ID`
2. `Instruction`
3. `Source`
4. `Status`
5. `Priority`
6. `Owner`
7. `Last Updated UTC`
8. `Evidence`
9. `Notes`

Allowed status values are `pending`, `in_progress`, `blocked`, `done`, and `won_t_do`.

Rules:
1. `done` requires evidence.
2. `blocked` requires the concrete blocker.
3. `won_t_do` requires rationale.
4. Status describes fulfillment, not continuing applicability.

## Stable Identifiers

1. Preserve existing identifier formats.
2. For a new ledger without repository convention, use `INST-###`.
3. Never reuse an identifier.
4. A replacement gets a new identifier; the predecessor links to it.

## Superseded and Stale Semantics

Mark a directive `superseded` when a newer authorized directive changes its meaning, scope, priority, or owner. Identify the successor and preserve the old fulfillment history.

Mark a directive `stale` when:
1. its source can no longer be verified
2. its repository context disappeared
3. evidence is too old to establish current applicability
4. current instructions conflict but no authorized resolution exists

Do not silently reactivate stale or superseded directives.

## Legacy Single-Table Ledgers

Do not automatically rewrite an existing compatible ledger. Until migration is explicitly authorized:
1. keep its columns and identifiers
2. treat fulfillment status as historical evidence only
3. record lifecycle in its existing notes field when necessary
4. identify the currently governing row by explicit source and successor links
5. avoid creating a parallel root or legacy file

## Audit Checks

1. Exactly one canonical ledger path is active.
2. Every current directive has a verifiable source.
3. Conflicting active directives are resolved or flagged.
4. Superseded rows identify their successor.
5. Stale rows are excluded from current truth.
6. Historical `done` rows are not mistaken for active policy.
7. Evidence and timestamps support every claimed transition.
