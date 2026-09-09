---
name: clean-slate
description: Provide an explicit conversation-local fresh-context boundary when the user sends --clean-slate, excluding optional user-history, memory, preference, summary, and history-index sources from subsequent greenfield tasks. Use only after direct activation; never ignore the current request, current conversation decisions, applicable instructions, repository evidence, safety controls, or authority boundaries.
---

# Clean Slate

## State Model

Remain inactive until the user sends `--clean-slate`.

1. `--clean-slate` enables clean-slate mode for the active conversation.
2. `--clean-slate off` disables it.
3. The newest valid command wins.
4. Do not claim persistence into another conversation unless the runtime explicitly provides it.
5. On state change, briefly confirm whether the boundary is on or off.

## Fresh-Context Boundary

While enabled, do not read, retrieve, or apply optional historical context solely to personalize or infer a new task, including:

1. cross-conversation memory or preference stores
2. chat-history indexes, summaries, retention caches, and archived transcripts
3. user-profile or instruction-tracker files that contain historical preferences rather than currently applicable instructions
4. prior-task notes, scratchpads, generated research caches, and unrelated governance history
5. stale inferred preferences from earlier turns

For a greenfield task, build the contract from the current request, current-turn clarifications, applicable active instructions, and task-local repository or external evidence.

## Context That Must Remain

Clean-slate mode cannot erase already loaded model context and must not suppress:

1. system, developer, organization, and repository instructions that apply now
2. the current request and user decisions made after the boundary was enabled
3. safety, legal, security, privacy, and authority constraints
4. repository files directly relevant to the current task
5. current branch, worktree, runtime, dependency, and environment state
6. evidence needed to preserve user work or prevent destructive action

If optional history and an applicable current instruction are mixed in one file, read only the minimum required portion when feasible. If they cannot be separated safely, state the limitation and ask before using the file.

## Interaction Rules

- Do not activate `history-indexing`, `conversation-retention-summary`, or `user-instructions-tracker` merely to establish context while this mode is on.
- Do not delete, rewrite, or hide history. This is a retrieval and application boundary, not data erasure.
- Do not reinterpret "clean" as permission to reset a repository, discard changes, clear caches, remove files, or start a new branch.
- When the current task explicitly asks to inspect history, identify the conflict and ask whether to disable the boundary for that task.
- When `eliminate-assumptions` is active, ask rather than importing a historical preference to fill a missing choice.

## Output Contract

On activation, state that optional history will be ignored for fresh tasks while current instructions, safety rules, repository facts, and explicit current decisions remain in force. Surface any runtime limitation that prevents full isolation.

Do not create or update a file solely because clean-slate mode changed.
