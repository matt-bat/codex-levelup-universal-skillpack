---
name: conversation-retention-summary
description: Use for maintaining a rolling summary of only the last 10 conversations and refreshing matched history entries instead of appending unbounded cache.
---

# Conversation Retention Summary

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Trigger Rule`
3. `Canonical Artifact`
4. `Retention Policy`

### Action Modules (Read As Needed)
1. Updating the rolling summary:
   - `Update Workflow`
2. Handling matches and continuations:
   - `Match Refresh Rule`
3. Keeping entries compact:
   - `Summary Budget`

### Output
1. `Output Contract`

## Mission
Keep a tiny, recent-only conversation memory that supports handoff without bloating context.

## Trigger Rule
Use this skill when:
1. a short recent-history summary is needed
2. the user resumes a prior topic from cached history
3. the session needs a compact recent-context artifact

This skill only maintains the last 10 conversations.

## Anti-Overuse Rules
Use when:
1. a compact recent handoff is needed
2. a resumed topic matches a recent conversation
3. the last 10 conversations are enough context

Do not use when:
1. full historical indexing is required
2. the session has no reusable recent context
3. the task does not need a retained artifact

Stop after:
1. the matching row is refreshed or a new row is added
2. the table is trimmed to 10 entries
3. no transcript-level detail remains

## Canonical Artifact
1. `docs/chat-history-summary.md`

## Retention Policy
1. retain at most 10 conversation entries
2. keep the newest relevant entries at the top
3. remove the oldest entry when the cap is exceeded
4. do not expand the artifact into a full transcript archive

## Required Structure
1. one-line scope note
2. summary table with:
   - `Entry ID`
   - `Conversation Key`
   - `Topic Tags`
   - `Summary`
   - `Updated Flag`
   - `Last Updated UTC`
3. brief conflict/override notes if needed

## Update Workflow
1. identify the conversation key
2. summarize the latest state in compact language
3. add or update the matching row
4. move the refreshed row to the top
5. trim the table back to 10 rows

## Match Refresh Rule
If a new conversation matches an existing cached history item:
1. update the existing row instead of duplicating it
2. set `Updated Flag` to `updated`
3. move the row to the top
4. preserve the original conversation key

## Summary Budget
Keep each summary short enough to scan quickly:
1. one to three sentences
2. no transcript-style detail
3. no duplicate restatements of older entries

## Output Contract
When using this skill, provide:
1. rows added or updated
2. whether a match was refreshed
3. whether the table was trimmed to 10
4. any ambiguity around conversation matching

## Related Skills
- [History Indexing](../history-indexing/SKILL.md): use for the broader detailed index when needed.
- [Token Reduction](../token-reduction/SKILL.md): keep the summary compact and low-overhead.
- [Artifact Budget Enforcement](../artifact-budget-enforcement/SKILL.md): enforce the cap and field budgets.
