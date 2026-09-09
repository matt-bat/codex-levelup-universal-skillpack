---
name: eliminate-assumptions
description: Block substantive execution whenever any unresolved ambiguity, conflict, missing choice, or unsupported inferred requirement could require an assumption. Use automatically when unresolved_uncertainty is present; inspect safely discoverable facts, then ask the user immediately for every decision that cannot be established from authoritative instructions or evidence.
---

# Eliminate Assumptions

## Mission

Prevent agents from silently filling gaps in task meaning. Resolve every ambiguity or conflict before execution instead of selecting a plausible default.

## No-Assumption Gate

Before substantive execution and at every reclassification checkpoint:

1. Separate explicit requirements, higher-priority rules, repository facts, logical consequences, and unresolved choices.
2. Inspect facts that are safely discoverable from the authorized local environment or explicitly permitted research.
3. Treat preference, scope, compatibility, behavior, target, format, risk tolerance, and acceptance-criterion gaps as unresolved when evidence does not determine them.
4. Stop before mutation, implementation, recommendation, or external action when any unresolved item remains.
5. Present the exact issue and ask the user how to handle it. Do not continue in parallel while waiting.

This gate applies even when an ambiguity appears low-impact. Do not record a bounded assumption and proceed. Do not turn an inferred convention, common default, previous preference, or likely intent into authorization.

## Allowed Conclusions

The following are not assumptions when they are directly supported and applicable:

1. an explicit current user instruction
2. a higher-priority instruction or active repository policy
3. a fact verified in the authorized environment
4. a fact established by a suitable current authoritative source
5. a necessary logical consequence with no plausible alternative

If applicability, freshness, identity, or interpretation is uncertain, the conclusion remains unresolved.

## Question Contract

For each pause:

1. state the ambiguity or conflict in plain language
2. state why available evidence cannot decide it
3. give a small mutually exclusive choice set when it represents the real options
4. describe the material consequence of each choice
5. ask only the smallest number of questions needed to unblock the next coherent phase

Ask immediately after discovering the issue. Combine tightly related issues, but do not bury one decision inside another.

## Interaction With Other Skills

- Let `requirement-clarifier` structure the task contract; this skill vetoes execution until its unresolved set is empty.
- When `quizme-mode` is active, preserve its exhaustive questioning and confirmation options.
- Let `advanced-r-and-d` resolve external factual uncertainty, but ask the user about preferences, authorization, or product choices that research cannot decide.
- Re-run this gate when research, planning, implementation, testing, or the final diff reveals a new ambiguity.

## Authority and Artifact Policy

Keep the unresolved-question set conversation-local unless the user requested recording or a governed workflow requires an authorized durable contract. This skill never grants permission to inspect prohibited history, search externally, write files, or perform any mutation.

## Completion Gates

1. No unresolved ambiguity, conflict, missing choice, or unsupported inferred requirement remains.
2. Every user decision is recorded faithfully in the task contract.
3. No action was taken while a question that could change it remained unanswered.
4. Any new uncertainty discovered later re-opened the gate.
