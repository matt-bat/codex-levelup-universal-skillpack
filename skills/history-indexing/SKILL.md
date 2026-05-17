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

## Trigger Rule
Use this skill when:
1. conversation history is large enough to cause retrieval overhead
2. multiple historical decisions must be referenced repeatedly
3. user requests context recall, summaries, or prior-decision traceability

Do not use for short sessions where direct retrieval is cheaper.

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
- [Skill Index](../docs/skill-index.md): canonical cross-skill routing index for trigger decisions.
- [Token Reduction](../token-reduction/SKILL.md): response and execution efficiency discipline.
- [Doc Maintenance](../doc-maintenance/SKILL.md): keep index artifact synchronized when decision context changes.
