---
name: history-indexing
description: Use for building and maintaining compact chat/session indexes (`docs/chat-history-index.md`) so long conversations can be queried precisely without re-reading broad transcript history.
---

# History Indexing

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Trigger Rule`
3. `Canonical Artifact`

### Action Modules (Read As Needed)
1. Creating/updating index structure:
   - `Required Structure`
   - `Maintenance Workflow`
2. Performing retrieval:
   - `Retrieval Policy`
3. Validating index quality:
   - `Quality Gates`

### Output
1. `Output Contract`

## Mission
Reduce retrieval token waste and stale-context errors by maintaining a structured history index for long-running sessions.

## Authority and Artifact Policy
1. Activating this skill grants no authority to create or update `docs/chat-history-index.md`.
2. Maintain the index only when durable history indexing is explicitly requested or already authorized by the repository workflow.
3. Read-only retrieval may use an existing index but must not refresh it as a side effect.

## Trigger Rule
Use this skill when:
1. conversation history is large enough to cause retrieval overhead
2. multiple historical decisions must be referenced repeatedly
3. user requests context recall, summaries, or prior-decision traceability

Do not use for short sessions where direct retrieval is cheaper.

## Anti-Overuse Rules
Use when:
1. prior decisions must be retrieved repeatedly
2. broad transcript reads would waste context
3. the user requests historical traceability

Do not use when:
1. the session is short enough to inspect directly
2. the task does not depend on prior decisions
3. a rolling recent summary is enough

Stop after:
1. the index points to the smallest useful retrieval scope
2. duplicate or superseded entries are marked
3. summaries remain compact enough to scan

## Canonical Artifact
1. `docs/chat-history-index.md`

## Required Structure
1. one-line session overview
2. index table with:
   - `Entry ID`
   - `Topic Tags`
   - `Turn/Line Range`
   - `Summary`
   - `Last Updated UTC`
3. compact notes on conflicts/overrides

## Retrieval Policy
1. match new request to topic tags first
2. read only referenced ranges
3. if no match, avoid broad transcript reads unless necessary
4. prefer repository `.md` instructions over ambiguous memory

## Maintenance Workflow
1. append a new index entry for major decision blocks
2. update existing entry when decision changes
3. annotate superseded decisions explicitly
4. keep summaries short and high-signal

## Quality Gates
Non-compliant index conditions:
1. missing required columns
2. stale `Last Updated UTC` for recently changed decisions
3. duplicate Entry IDs
4. summaries too vague to retrieve by topic

## Output Contract
When applying this skill, provide:
1. entries added/updated
2. retrieval scope used
3. unresolved ambiguity/conflict notes

## Related Skills
- [Skill Catalog](../skill-catalog.json): canonical routing source for trigger and relationship decisions.
- [Skill Index](../docs/skill-index.md): generated operator view of the catalog; do not edit it independently.
- [Token Reduction](../token-reduction/SKILL.md): response and execution efficiency discipline.
- [Doc Maintenance](../doc-maintenance/SKILL.md): keep index artifact synchronized when decision context changes.
- [Conversation Retention Summary](../conversation-retention-summary/SKILL.md): maintain the rolling last-10 summary alongside the detailed index.
