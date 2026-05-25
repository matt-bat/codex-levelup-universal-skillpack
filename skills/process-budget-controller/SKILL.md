---
name: process-budget-controller
description: Use for capping process overhead by task size, limiting skill count, validation depth, artifact creation, and user-facing ceremony before other governance or documentation skills expand scope.
---

# Process Budget Controller

## Mission
Keep the skillpack useful without letting process become the product.

## Trigger Rule
Use this skill when:
1. several skills could plausibly apply
2. the task is small but the policy surface is large
3. governance or documentation work risks becoming disproportionate
4. the user asks for speed, low overhead, or minimal ceremony

## Scope Boundary
This skill owns process budget limits.

Use [Skill Governance](../skill-governance/SKILL.md) for risk mode and release gate policy.
Use [Order of Operations](../order-of-operations/SKILL.md) for dependency sequencing.

## Budget Tiers
1. `tiny`: maximum 2 skills, no artifacts, one cheap check
2. `small`: maximum 4 skills, no governance artifact unless governed paths change
3. `standard`: maximum 8 skills, targeted artifacts and validation
4. `critical`: no fixed cap; required safety gates override budget

## Selection Rules
1. pick the smallest tier that can satisfy safety and user intent
2. add skills only when they change execution, validation, or durable evidence
3. prefer existing canonical artifacts over new artifacts
4. stop expansion when the next skill only adds explanation

## Anti-Overuse Rules
Use when:
1. skill selection is likely to sprawl
2. the task should remain lightweight
3. a governed workflow needs explicit process limits

Do not use when:
1. critical safety gates already determine the workflow
2. the user explicitly asks for exhaustive review or full governance
3. the task has only one obvious skill

Stop after:
1. tier is selected
2. maximum skill count and artifact allowance are stated
3. exceptions are tied to safety, validation, or user intent

## Output Contract
When applying this skill, provide:
1. selected tier
2. maximum skill set
3. allowed artifacts
4. validation depth
5. escalation condition if the budget must expand
