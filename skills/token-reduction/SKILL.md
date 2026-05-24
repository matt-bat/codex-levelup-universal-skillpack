---
name: token-reduction
description: Use for minimizing token usage while preserving quality, through strict context filtering, indexed history retrieval, concise reasoning formats, output budgeting, and low-overhead execution patterns.
---

# Token Reduction

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Scope Boundary`
3. `Core Rule`
4. `Non-Negotiable Constraints`

### Action Modules (Read As Needed)
1. New project handling:
   - `New-Project Startup Handshake (Required)`
   - `Project Intake Index (Required for New Projects)`
   - `Local-First / No-Deploy Default (Required)`
2. Retrieval efficiency:
   - `History Indexing Handoff`
   - `Context Retrieval Policy`
3. Response/output compression:
   - `Output Compression Policy`
   - `Compressed Planning Syntax (Internal Use)`
   - `Reasoning Externalization Policy (Required)`
4. Execution efficiency:
   - `Tool Usage Token Controls`
   - `Editing Token Controls`
5. Quality safeguards:
   - `Quality Guardrails Under Compression`
   - `Risk-Based Detail Policy`
   - `Anti-Patterns`

### Optional Reference Sections (Read Only If Needed)
1. `Pros/Cons of Requested Principles`
2. `Additional Token-Saving Strategies (Proposed)`
3. `Operational Modes`
4. `Success Metrics`

### Output
1. `Deliverable Format`

## Mission
Deliver correct results with the fewest practical tokens.

## Scope Boundary
This skill governs concise output, targeted reads, and low-overhead execution discipline.

Use [History Indexing](../history-indexing/SKILL.md) for:
1. building/maintaining `docs/chat-history-index.md`
2. long-session retrieval indexing workflows
3. index schema and staleness management

Primary objective:
1. maximize signal
2. minimize context bloat
3. avoid unnecessary reads/writes
4. keep responses outcome-first

## Core Rule
Users want outcomes, not internal deliberation.

Default behavior:
1. show result first
2. include only necessary rationale
3. omit internal scratch reasoning from final output
4. do not restate/reiterate the user's last request
5. keep user-facing responses as concise as possible while preserving correctness
6. use bullet points and minimal full sentences for user-facing responses

## New-Project Startup Handshake (Required)
`New project` means a project the model has not worked on before.

At the start of every conversation involving a new project, ask this once before running costly verification work:
1. whether the model should run tests/build/execution checks by default, or
2. whether the user prefers to run them manually to save tokens/time.

Recommended prompt:
- "For this new project, do you want me to run tests/build checks by default, or would you rather run them yourself to save tokens?"

Policy:
1. do not assume model-run verification by default on a brand-new project
2. record preference and reuse it for the project unless user changes it
3. if preference is unknown, ask before starting broad test/build runs

## Project Intake Index (Required for New Projects)
Maintain `docs/project-index.md` with one entry per project.

Each entry must include:
1. `project_id` (short unique key)
2. `language` (primary language)
3. `description` (max 4 words)
4. `model_default_test_build` (`yes` or `no`)
5. `last_confirmed_utc`

Rules:
1. create index file if missing
2. add entry when first encountering a new project
3. update `model_default_test_build` when user preference changes
4. keep descriptions <= 4 words
5. when using governance automation, treat generated governance artifacts as intake source and keep the index synchronized from those artifacts

Template:
```md
# Project Index

| Project ID | Language | Description (<=4 words) | Model Runs Tests/Build by Default (yes/no) | Last Confirmed UTC |
|---|---|---|---|---|
| universal-app | TypeScript/Python | Cross-platform business app | no | 2026-05-12T17:00:00Z |
```

## Local-First / No-Deploy Default (Required)
Execution scope is local by default.

Rules:
1. perform requested work locally unless user explicitly asks for deployment actions
2. never deploy/release/publish/push to runtime environments implicitly
3. if deployment might be inferred, ask for explicit confirmation first
4. being aware of an existing deployed app does not change this default

## Trigger Examples
Use when users ask for concise output, lower cost/latency, or when conversation length is causing context bloat.

## Non-Negotiable Constraints
1. Do not sacrifice correctness for brevity.
2. Do not omit required safety or high-risk caveats.
3. Do not hide critical uncertainty.
4. Do not skip mandatory checks for medical/legal/financial/security-sensitive requests.
5. Do not perform deployment actions unless explicitly requested.

## Pros/Cons of Requested Principles

### Canonical Requested List (3 Items)
This section is the authoritative pros/cons list for the exact user-requested items:
1. result-focused responses (no internal-thought dump)
2. history indexing + avoid unnecessary history reads
3. very short internal planning style

### 1) Result-focused responses (no internal-thought dump)
Pros:
1. lower token cost
2. faster response delivery
3. clearer, action-oriented outputs

Cons:
1. can feel opaque for complex or high-risk decisions
2. weaker auditability if rationale is removed entirely

Policy:
1. default to concise outcome-first responses
2. include brief rationale when trust/risk/tradeoff context is material

### 2) History indexing + avoid unnecessary history reads
Pros:
1. substantial token savings on long threads
2. lower chance of stale-context contamination
3. faster retrieval of relevant prior decisions

Cons:
1. requires ongoing index maintenance
2. stale/missing index entries can hide relevant dependencies

Policy:
1. use index-first retrieval
2. read only referenced ranges for matched topics
3. skip broad transcript reads for unrelated new inquiries

### 3) Very short internal planning style
Pros:
1. reduced working-token overhead
2. faster planning loops
3. stronger prioritization discipline

Cons:
1. loss of nuance for complex architecture/risk cases
2. weaker handoff/debug readability if over-compressed

Policy:
1. use compressed notation for transient internal planning
2. keep final artifacts precise and unambiguous

### Best-Practice Balance (Required)
1. default to ultra-concise
2. expand only for risk, ambiguity, or explicit user request
3. maintain compact indexed history so precision is retained without transcript bloat

### Additional Principle in This Skill
The skill also includes one extra supporting principle:
- prioritize `.md` files as persistent instruction sources, then use indexed chat only when relevant

Pros:
1. deterministic, durable source of project instructions
2. lower ambiguity than free-form chat memory
3. easier targeted retrieval

Cons:
1. docs can lag behind new clarifications
2. possible conflict between docs and recent user intent

Policy:
1. prefer `.md` by default
2. if conflict appears, ask precedence once and continue

## History Indexing Handoff
For long-session indexing rules and artifact maintenance, apply [History Indexing](../history-indexing/SKILL.md).

## Context Retrieval Policy
Read in this order:
1. task-local files
2. relevant `.md` policy/instruction files
3. indexed history ranges (only if needed)
4. raw full chat history (last resort)

Never-load list:
1. entire transcript without targeting
2. binary/large files without purpose
3. unrelated dependency directories

## Output Compression Policy

### Response Shape
Use minimal structure:
1. result
2. key evidence
3. next action (if needed)

Avoid:
1. repeated restatements
2. excessive hedging
3. verbose process narration
4. repeating the user's most recent request

### Length Controls
1. default to short answers for simple requests
2. expand only when user asks for depth
3. use bullets for dense content instead of prose blocks
4. avoid duplicate examples unless comparison is required
5. user-facing wording must be coherent full-language (no shorthand abbreviations)

## Tool Usage Token Controls
1. batch related file reads in one command call
2. prefer targeted `rg`/`sed` ranges over full-file dumps
3. avoid re-reading unchanged files
4. cache important findings as compact notes in working summary
5. stop exploratory reads once decision confidence threshold is met

## Editing Token Controls
1. patch only touched lines
2. avoid full-file rewrites unless necessary
3. consolidate related edits in one patch
4. avoid formatting churn unrelated to task

## Compressed Planning Syntax (Internal Use)
Use short notation for transient planning notes:
1. `goal: <result>`
2. `ctx: <needed files only>`
3. `do: <next command>`
4. `chk: <validation>`
5. `risk: <main risk>`

Internal style rule:
1. keep internal notes as concise as possible (`ultra-short` target)
2. abbreviations/shorthand are allowed only for internal notes
3. use common short-form text abbreviations where understandable to human readers
4. do not use internal shorthand style in user-facing responses
5. prioritize persistent notes in repo artifacts over expanding internal planning text

Example:
- `goal: add skill`
- `ctx: skills tree + style`
- `do: mkdir + add SKILL.md`
- `chk: find + frontmatter`
- `risk: policy mismatch`

## Reasoning Externalization Policy (Required)
Prefer storing useful detail in durable repo artifacts, not in long hidden reasoning.

Priority order:
1. code-adjacent comments for non-obvious logic/tradeoffs
2. relevant docs (`README.md`, `docs/*.md`, governance artifacts)
3. concise user-facing summary
4. internal transient notes (minimal only)

Rules:
1. if detail helps future maintainers, write it in code comments or docs
2. keep comments/doc notes concise, specific, and directly tied to changed behavior
3. avoid verbose internal deliberation when the same value can be captured in repo notes
4. do not add noisy comments for obvious code
5. when risks/assumptions drive choices, capture them in docs or governance artifacts

## Quality Guardrails Under Compression
Token reduction must still preserve:
1. factual accuracy
2. requirement coverage
3. explicit uncertainty when present
4. reproducible validation evidence

Minimum correctness checklist:
1. all user constraints addressed
2. no contradictory instructions introduced
3. critical commands/results verified
4. unresolved blockers explicitly stated

## Risk-Based Detail Policy
Adjust verbosity by risk:
1. low risk: concise answer + minimal evidence
2. medium risk: concise answer + targeted rationale
3. high risk: concise answer + explicit safeguards + verification summary

## Anti-Patterns
1. "Concise" but missing requested deliverables
2. re-reading broad history by default
3. dumping tool output without synthesis
4. answering with generic templates unrelated to user context
5. over-compressing until ambiguity increases rework

## Additional Token-Saving Strategies (Proposed)
1. **Decision checkpointing**
- save compact "state snapshot" every major turn to avoid repeated re-analysis

2. **Relevance tagging in docs**
- tag project docs by domain (`auth`, `payments`, `deploy`) for precise retrieval

3. **Command output truncation discipline**
- request only needed lines/fields; avoid full logs by default

4. **One-pass synthesis**
- aggregate findings from parallel reads before responding once

5. **Ask-then-expand policy**
- provide short answer first, expand on demand

6. **Stable artifact references**
- link to canonical files instead of repeating content

## Operational Modes
1. `lean` (default): concise answers, targeted reads
2. `ultra-lean`: minimal narration, result-only unless risk requires detail
3. `audit`: still concise, but includes explicit evidence trail

Mode selection:
- if user says "quick", "short", or "just result" => `ultra-lean`
- if user asks "why" or "prove" => `audit`

## Deliverable Format
When using this skill, provide:
1. concise result
2. essential evidence only
3. optional "expand?" prompt when deeper detail may help

## Success Metrics
Track, when practical:
1. reduced average response length for simple tasks
2. reduced redundant file/history reads
3. unchanged or improved task success rate

## Related Skills
- [Scripted Command Execution](../scripted-command-execution/SKILL.md): low-overhead deterministic command workflows.
- [Regression Prevention](../regression-prevention/SKILL.md): retain safety coverage while minimizing unnecessary verbosity.
- [Project Backup](../project-backup/SKILL.md): enforce backup gates without bloated process narration.
- [Artifact Budget Enforcement](../artifact-budget-enforcement/SKILL.md): keep cached summaries, notes, and tables bounded.
- [Conversation Retention Summary](../conversation-retention-summary/SKILL.md): maintain a small rolling recent-history cache.
