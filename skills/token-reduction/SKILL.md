---
name: token-reduction
description: Use when the user explicitly requests shorter or lower-token output, or when long context is causing concrete retrieval or response overhead. Limit this skill to context selection and output efficiency; do not activate it for routine tasks, project intake, testing ownership, deployment policy, or repository bookkeeping.
---

# Token Reduction

## Purpose
Reduce context and output cost without reducing correctness, requirement coverage, or evidence quality.

This skill owns only:
1. targeted context selection
2. concise tool-result synthesis
3. response length and structure
4. lossless compression of agent-produced summaries

It does not own project initialization, `docs/project-index.md`, test/build responsibility, deployment authorization, history-file maintenance, or durable rationale files.

## Workflow
1. Identify the result and evidence the user actually needs.
2. Read task-local sources before broad policy or history.
3. Batch related reads and request only useful output ranges.
4. Stop retrieval when the decision is supported and no required uncertainty remains.
5. Return the result first, followed by essential evidence and a next action only when needed.

## Quality Floor
Compression must preserve:
1. every user constraint and requested deliverable
2. material uncertainty and blockers
3. safety or authorization boundaries
4. reproducible validation evidence
5. exact commands, errors, schemas, and code when their exact form matters

Do not replace analysis with vague conclusions, omit a required caveat, or claim checks that were not run.

## Artifact Boundary
Activation alone grants no permission to create or update indexes, summaries, comments, documentation, trackers, or other files. Write only artifacts already authorized by the task or a separate applicable policy.

## Conditional References
1. Read [Context and Output Controls](./references/context-and-output-controls.md) only when retrieval needs pruning, tool output is large, or a concrete output budget is needed.
2. Read [Legacy Project Intake Compatibility](./references/legacy-project-intake-compatibility.md) only when older repository policy still associates this skill with project intake, `docs/project-index.md`, testing ownership, or deployment rules.

## Completion Check
1. The result is complete despite being concise.
2. Reads and tool output were targeted.
3. Risk and uncertainty remain visible.
4. No unrelated durable artifact was created or changed.
