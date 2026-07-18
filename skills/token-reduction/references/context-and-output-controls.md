# Context and Output Controls

Use this reference only when `token-reduction` is active and concrete retrieval or response compression is needed.

## Retrieval Order

1. task-local files and direct evidence
2. relevant repository instructions or documentation
3. a targeted existing index when the task depends on prior decisions
4. broad history only as a last resort

Avoid loading full transcripts, dependency trees, binaries, generated output, or unrelated documentation without a task-specific reason.

## Tool Controls

1. Batch related independent reads.
2. Prefer targeted search and line ranges over full dumps.
3. Avoid rereading unchanged sources.
4. Truncate logs only after preserving the failure and relevant surrounding context.
5. Summarize tool output; do not paste it wholesale unless requested.

## Editing Controls

1. Patch only task-relevant lines.
2. Avoid formatting churn and unrelated cleanup.
3. Consolidate coupled edits when that makes review clearer.
4. Inspect the resulting diff rather than restating every edit from memory.

## Response Budget

Use the smallest shape that remains complete:
1. result
2. essential evidence
3. remaining risk or next action, when present

Adjust detail by consequence:
1. low risk: result and minimal evidence
2. medium risk: result, targeted rationale, validation
3. high risk: safeguards, uncertainty, validation, and residual risk

Do not automatically ask whether the user wants more detail. Expand when requested or when needed for a safe decision.

## Lossless Summary Check

Before relying on a compressed summary, confirm it retains:
1. goal and acceptance conditions
2. constraints and authorization limits
3. decisions and their evidence
4. unresolved questions and blockers
5. exact references needed to recover source detail
