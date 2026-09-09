# Example: Quizme Clarification

[Documentation home](../README.md) · [Documentation update](./documentation-only-update.md) · [Release readiness](./release-readiness-change.md)

## Scenario
The user wants exhaustive clarification before any substantive work and writes:

```text
--quizme --mc --one-at-a-time --confirm
```

## Route
1. `quizme-mode`
2. `requirement-clarifier` as its hard prerequisite
3. task-specific skills only after clarification completes

The command activates clarification mode; it does not by itself request a startup declaration. Declare the route only if the user separately requests it or the clarified work is governed or audited.

## Behavior
1. quizme mode persists for the active conversation until the user writes `--quizme` again
2. `--mc` prefers interactive multiple-choice questions
3. `--one-at-a-time` asks one adaptive question per round
4. `--confirm` waits for approval of the final task contract
5. `--record` may be added to persist the approved contract and implies confirmation
6. short-form answers remain available when choices would be incomplete or misleading
7. substantive execution waits until goal, scope, constraints, acceptance criteria, and risk tolerance are clear

## Stop Rule
Do not begin implementation while material uncertainty remains.
