# Example: Quizme Clarification

## Scenario
The user wants exhaustive clarification before any substantive work and writes:

```text
--quizme --mc --one-at-a-time --confirm
```

## Skills In Use
1. `quizme-mode`
2. `requirement-clarifier`
3. task-specific skills only after clarification completes

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
