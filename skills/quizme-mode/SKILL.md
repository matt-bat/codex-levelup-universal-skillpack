---
name: quizme-mode
description: Use when the user invokes --quizme to persistently require exhaustive task clarification before substantive execution, with intuitive options for multiple-choice questions, one-at-a-time questioning, explicit confirmation, and durable contract recording.
---

# Quizme Mode

## Mission
Create a conversation-local clarification gate that prevents substantive execution until the user and agent have a fully aligned task contract.

## Trigger Rule
Use this skill when:
1. the user writes `--quizme`
2. quizme mode was enabled earlier in the active conversation and has not been toggled off

Trigger parsing is exact:
1. `--quizme` toggles quizme mode on when off
2. `--quizme` toggles quizme mode off when already on
3. mode persists throughout the active conversation until toggled off
4. only arguments placed directly after `--quizme` are considered
5. supported arguments are `--mc`, `--one-at-a-time`, `--confirm`, and `--record`
6. arguments may appear in any order
7. duplicate arguments are harmless
8. unsupported arguments make the command invalid; briefly report them, leave state unchanged, and do not consume the message
9. toggling quizme mode off clears every option
10. while mode is active, plain `--quizme` toggles it off; `--quizme` with supported arguments keeps it on and replaces active options

## Multiple-Choice Preference
When invoked as `--quizme --mc`:
1. enable quizme mode if it is off
2. prefer multiple-choice clarification questions
3. ask short-form questions only when multiple-choice options would distort the answer
4. include an optional short-form choice when listed options may be incomplete

## Optional Behaviors
`--one-at-a-time`:
1. ask exactly one adaptive clarification question per round
2. use each response to shape the next question
3. do not reduce clarification depth

`--confirm`:
1. show the finalized task contract after clarification
2. wait for explicit user approval before substantive execution

`--record`:
1. implies `--confirm`
2. persist the approved contract in governance evidence or the most suitable task artifact when one exists
3. do not create a durable artifact for answer-only tasks unless the user asks

Automatically require confirmation for destructive, public, production, payment, authentication, or irreversible tasks even when `--confirm` was not supplied.

## Clarification Gate
Before substantive execution, keep questioning until no material doubt remains about:
1. goal
2. in-scope work
3. out-of-scope work
4. constraints
5. acceptance criteria
6. risk tolerance and side-effect boundaries

Questioning rules:
1. ask one to three high-value questions per round unless `--one-at-a-time` is active
2. continue follow-up rounds while material uncertainty remains
3. do not ask about facts safely discoverable from repository or environment inspection
4. do not ask questions whose answers cannot change execution
5. do not start implementation, mutation, or governed execution until the clarification gate passes

## Interactive Clarification
Use the same interactive clarification flow as plan-mode questioning when the runtime exposes it.

1. prefer the interactive clarification console for quizme questions
2. use mutually exclusive multiple-choice options when `--mc` is active
3. allow short-form input only when needed or as an optional additional choice
4. if the interactive clarification console is unavailable, ask concise questions in normal conversation

## Scope Boundary
This skill owns:
1. toggle state
2. immediate argument parsing
3. clarification depth
4. pre-execution blocking behavior

Use [Requirement Clarifier](../requirement-clarifier/SKILL.md) for the resulting implementation contract.
Use [Skill Governance](../skill-governance/SKILL.md) to record active quizme state for governed tasks.

## Output Contract
Before execution begins, confirm:
1. quizme mode state (`on` or `off`)
2. multiple-choice preference (`on` or `off`)
3. one-at-a-time preference (`on` or `off`)
4. confirmation requirement (`on` or `off`)
5. recording requirement (`on` or `off`)
6. clarified task contract
7. remaining open questions (`none` before substantive execution)

## Anti-Overuse Rules
Use when:
1. the user explicitly invokes `--quizme`
2. quizme mode remains active from an earlier turn

Do not use when:
1. the user has not enabled quizme mode
2. quizme mode was toggled off

Stop after:
1. the task contract is fully clear
2. substantive execution may begin for the current request
3. quizme mode remains active for later requests until explicitly toggled off
