---
name: internal-lang
description: Optional compact-notation controls for explicit `/internal-lang on|off` and `/internal-lang --response on|off` commands, or when the user directly requests shorthand scratch or response notation. Do not activate for routine tasks, generic planning, or general concision.
---

# Internal Lang

## Purpose
Provide an explicit, conversation-local switch for compact notation without changing normal task behavior.

Remain inactive unless the user invokes a supported command or directly requests this notation. Activation does not authorize repository changes or durable note creation.

## State Model
Before explicit activation, assume no `internal-lang` behavior.

On the first explicit activation in a conversation, initialize:
1. `internal=true`
2. `response=false`

Then apply commands in message order:
1. `/internal-lang on` sets `internal=true`.
2. `/internal-lang off` sets `internal=false` and leaves `response` unchanged.
3. `/internal-lang --response on` sets `response=true` and does not force `internal=true`.
4. `/internal-lang --response off` sets `response=false`.
5. The newest explicit command wins for the state it changes.
6. Ignore malformed or unsupported command tokens and briefly identify what was ignored.

Do not assume state persists into a new conversation unless the runtime explicitly preserves it.

## Response Boundary
When `response=false`:
1. keep user-facing language normal
2. omit compact scratch notation from the final response
3. mention state only when it changes

When `response=true`:
1. use compact notation sparingly
2. provide a key when meaning may be ambiguous
3. expand safety-critical, user-actionable, or validation-critical content into normal language

## Safety Gate
Never use compact notation to obscure or lossy-compress:
1. user requirements or acceptance criteria
2. legal, security, financial, or credential material
3. commands, code, schemas, or exact error messages
4. blockers, uncertainty, or validation evidence

Do not expose hidden chain of thought or claim that this switch changes the model's internal neural representation.

## Conditional Reference
Read [Notation and Safety](./references/notation-and-safety.md) only when compact notation will actually be used, expanded, or saved in an explicitly requested artifact.

## Completion Check
1. Every explicit command produced the documented state transition.
2. Normal responses remained normal while `response=false`.
3. Compact content remained reversible and non-lossy.
4. No file was created or changed solely because this skill activated.
