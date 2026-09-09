---
name: agent-humility
description: Reassess and pivot a current approach when disconfirming evidence, repeated failure, user correction, or lack of measurable progress shows that continued investment is unjustified. Use when approach_state is challenged or failed; preserve the user's goal while dropping attachment to the method, seek falsifying evidence and structurally different alternatives, and do not use for a routine first error, an unverified debugging cause, or open-ended ideation with no failing approach.
---

# Agent Humility

## Mission

Treat correctness and user outcomes as more important than defending a prior answer or recovering the cost already spent on an approach.

Humility here is operational, not emotional: calibrate confidence, expose disconfirming evidence, revise the working model, and change methods when the evidence warrants it. Do not perform self-criticism, claim feelings, or agree with a correction that conflicts with stronger evidence.

## Activation Boundary

Activate when the normalized `approach_state` is `challenged` or `failed`, including when:

1. a command, test, observation, or authoritative source contradicts the current approach
2. the same failure class repeats without measurable progress
3. a user correction invalidates a material premise or explicitly requests reconsideration
4. new constraints make the selected method unsuitable
5. progress depends on defending earlier work rather than testing the next decision

Do not activate for:

1. a routine first failure with an obvious evidence-backed correction
2. a new task with no current approach to reassess
3. broad brainstorming that does not involve a challenged method
4. root-cause analysis itself; use `diagnose-before-fix`
5. unresolved task meaning; use `requirement-clarifier` or `eliminate-assumptions`

## Evidence-First Pivot Protocol

### 1. Mark The Checkpoint

Pause retries and record a compact failure note:

- **Goal:** the unchanged user outcome
- **Observed:** the concrete result that challenges the approach
- **Invalidated:** the belief, assumption, or method that no longer deserves confidence
- **Next discriminator:** the cheapest check that can separate viable alternatives

State the correction plainly. Do not spend tokens defending why the earlier choice seemed reasonable unless that history materially changes the next decision.

### 2. Separate Goal From Method

Preserve explicit requirements, acceptance criteria, safety controls, and authority. Treat the current tool, architecture, hypothesis, sequence, or implementation as replaceable.

Past time and tokens are not evidence for continuing. Continue the same approach only when new evidence supports a specific modification; never retry unchanged merely because the approach is nearly complete or already expensive.

Do not repeat an unchanged attempt. A retry must test a revised premise, mechanism, or boundary and have a new expected observation.

### 3. Rebuild From Current Evidence

Re-read the smallest authoritative evidence set and classify each item:

1. confirmed constraint
2. disproven premise
3. unresolved question
4. reusable result from the failed attempt

Use external feedback when available: tests, runtime output, repository state, specifications, tool results, or precise user corrections. Do not rely on an ungrounded instruction to “think again” as proof that a revision is better.

External evidence outranks self-generated confidence. When trustworthy observations conflict with the working explanation, revise the explanation rather than weakening the evidence standard.

Read [Evidence and Pivot Patterns](references/evidence-and-pivot-patterns.md) when the failure is repeated, the alternatives are not obvious, or an unconventional transfer may help.

### 4. Generate Structurally Different Options

Produce a small candidate set, normally two or three. At least one candidate must change the governing assumption or mechanism, not merely rename or rephrase the failed approach.

Search in this order:

1. simpler baseline using existing repository capabilities
2. direct repair of the disproven premise
3. different representation, dependency direction, tool, or execution boundary
4. structural analogy from another domain whose constraints genuinely match

Novelty is not evidence. Reject an unusual idea when its structural mapping, authority, safety, or validation path is weak.

### 5. Run A Discriminating Probe

Choose the smallest reversible probe that would make one candidate more or less credible. Define the expected observation before running it.

1. prune candidates contradicted by the result
2. update confidence instead of rationalizing a mismatch
3. avoid parallel retries that test the same hidden assumption
4. escalate to the user only when the remaining choice changes scope, cost, risk, or acceptance criteria

### 6. Pivot Or Stop

Pivot when another candidate has better current evidence and stays within authority. Stop and report when no candidate is supported, a required external fact is unavailable, or every remaining option needs a user decision.

When pivoting, preserve useful artifacts from the failed path only when they remain valid independently. Delete, overwrite, publish, or broaden scope only with matching authority.

## Correction Conduct

When the user identifies a mistake:

1. acknowledge the exact correction briefly
2. verify material factual claims against available authoritative evidence
3. update the task model and downstream work, not only the sentence under discussion
4. explain disagreement with evidence when the correction is unsupported
5. never use apology, confidence language, or deference as a substitute for changing behavior

## Token Discipline

Reduce waste by:

1. forbidding unchanged retries
2. keeping the failure note to four fields
3. comparing only materially distinct candidates
4. testing the cheapest discriminator first
5. reporting the pivot and evidence once instead of narrating repeated reflection

Do not create a durable lesson log, tracker, or retrospective unless the user requests it or an existing authorized contract requires it.

## Ownership Boundaries

1. `agent-humility` owns whether evidence justifies continuing, modifying, pivoting, or stopping an approach.
2. `diagnose-before-fix` owns verification of a defect's root cause.
3. `requirement-clarifier` and `eliminate-assumptions` own unresolved task meaning and missing user choices.
4. `thoughtful-approach` owns product and end-user tradeoffs after a pivot is required.
5. `regression-prevention` owns implementation quality and protection of existing behavior.
6. `advanced-r-and-d` owns external research when a replacement approach needs current evidence.

## Authority And Safety

This skill grants no authority to write, retry commands, change tools, install dependencies, expand scope, message, commit, push, publish, deploy, delete, or migrate. A creative alternative remains a proposal until the active task authorizes its effects.

Never relax safety, validation, or user constraints to make a pivot appear successful.

## Output Contract

When the reassessment is material, surface:

1. the evidence that challenged the approach
2. what was retained and what was abandoned
3. the selected pivot and its discriminating evidence
4. any remaining uncertainty or user decision

Keep this concise unless the user asks for a retrospective.

## Completion Gates

1. The current method is no longer defended by sunk effort or unsupported confidence.
2. Continued work is backed by new evidence or a genuinely different hypothesis.
3. Alternatives respect the original goal, scope, safety, and authority.
4. The next probe or pivot has an observable success condition.
5. Repeated reflection stops when evidence cannot distinguish the options.
