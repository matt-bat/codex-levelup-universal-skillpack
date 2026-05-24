---
name: artifact-budget-enforcement
description: Use for enforcing hard limits on cached artifacts, summaries, indexes, and other compact metadata files so they stay bounded and high-signal.
---

# Artifact Budget Enforcement

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Trigger Rule`
3. `Budget Policy`

### Action Modules (Read As Needed)
1. Choosing caps:
   - `Default Budgets`
2. Pruning and consolidation:
   - `Pruning Rule`
   - `Merge Rule`
3. Preventing drift:
   - `Staleness Rule`

### Output
1. `Output Contract`

## Mission
Keep cached artifacts useful by giving them explicit size limits and pruning rules.

## Trigger Rule
Use this skill when:
1. conversation caches, indexes, or trackers can grow without bound
2. summaries or descriptions need strict length limits
3. multiple files hold overlapping cached state
4. a repo needs a repeatable rule for trimming low-value history

## Anti-Overuse Rules
Use when:
1. an artifact has a real growth risk
2. cache-like docs need explicit caps
3. pruning or merging is part of the task

Do not use when:
1. no bounded artifact is being created or maintained
2. a normal documentation edit has no cache behavior
3. the relevant artifact already stays under its cap

Stop after:
1. caps are defined or confirmed
2. oversized artifacts are pruned or merged
3. remaining exceptions are recorded with rationale

## Budget Policy
Every cache-like artifact must have:
1. a hard item cap
2. a per-entry size cap
3. a pruning rule when the cap is exceeded
4. a canonical file of record when multiple files overlap

## Default Budgets
Use these defaults unless a stricter repo rule already exists:
1. rolling conversation summary: 10 entries
2. index summaries: 40 words max
3. short descriptions: 12 words max unless the schema is stricter
4. tracker notes: 25 words max
5. bullet lists in cached artifacts: 10 items max unless the schema is stricter

## Pruning Rule
When a cap is exceeded:
1. remove the oldest low-value entry first
2. merge stable duplicates before removing unique information
3. preserve the newest user-relevant state
4. record what was pruned if the artifact tracks history

## Merge Rule
Merge entries when they are:
1. duplicate
2. superseded
3. too similar to justify separate cache slots

## Staleness Rule
If a cached entry is old but still relevant:
1. keep the newest accurate version
2. mark the older one superseded where the artifact supports it
3. do not keep both unless the artifact explicitly needs lineage

## Default Scope
Common targets include:
1. `docs/chat-history-summary.md`
2. `docs/chat-history-index.md`
3. `user-instructions.md`
4. tracker-style markdown tables

## Output Contract
When using this skill, provide:
1. artifact(s) capped
2. limit(s) applied
3. entries removed or merged
4. residual risk if a stricter cap is still needed

## Related Skills
- [Conversation Retention Summary](../conversation-retention-summary/SKILL.md): maintains the rolling 10-conversation cache.
- [History Indexing](../history-indexing/SKILL.md): maintains the broader detailed index.
- [Token Reduction](../token-reduction/SKILL.md): keep summaries and notes compact.
- [File Maintenance](../file-maintenance/SKILL.md): detect stale or duplicate artifact growth.
