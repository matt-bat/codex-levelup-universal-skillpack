---
name: skill-usage-review
description: Use for periodically reviewing which skills are overused, underused, missing, or creating friction by examining recent governance artifacts, handoffs, instruction trackers, and task outcomes.
---

# Skill Usage Review

## Mission
Improve the skillpack from real usage evidence instead of intuition.

## Authority and Artifact Policy
1. Activating this skill grants no authority to create or update field notes, routing observations, governance artifacts, or policy files.
2. Use existing evidence read-only unless the task separately authorizes a durable review artifact or remediation.
3. Do not retain prompts, source content, hidden reasoning, or unbounded history as usage evidence.

## Trigger Rule
Use this skill when:
1. reviewing recent tasks for process quality
2. checking whether skills are being over-applied
3. deciding whether a skill should be split, merged, deprecated, or promoted
4. preparing a periodic maintenance report

## Scope Boundary
This skill owns usage-pattern review and improvement recommendations.

Use [Deprecation Management](../deprecation-management/SKILL.md) for deprecation lifecycle decisions.
Use [Thoroughly Rate Review](../thoroughly-rate-review/SKILL.md) for scoring quality.

## Evidence Sources
Prefer existing artifacts:
1. `docs/governance/*.governance.json`
2. `docs/governance/*.governance.md`
3. root `user-instructions.md` when the repository has opted into durable tracking
4. `docs/handoffs/*.md` when present
5. recent commit messages or release notes
6. bounded routing-observation summaries when present; never prompts, source content, or hidden reasoning

## Review Checks
1. most frequently selected skills
2. skills selected without clear task value
3. tasks missing expected safety or validation skills
4. skills never selected despite documented triggers
5. repeated user corrections or friction points
6. artifacts created but not maintained

## Anti-Overuse Rules
Use when:
1. there is enough recent task evidence to review
2. process behavior is being tuned
3. the user asks whether the skillpack itself is working well

Do not use when:
1. there is no usage evidence yet
2. the task is a single implementation request
3. a direct policy fix is already obvious and bounded

Stop after:
1. usage findings are grouped by severity
2. concrete skill changes are proposed
3. no more than five next actions are recommended

## Output Contract
When applying this skill, provide:
1. evidence reviewed
2. overused skills
3. underused or missing skills
4. friction points
5. recommended changes with priority
