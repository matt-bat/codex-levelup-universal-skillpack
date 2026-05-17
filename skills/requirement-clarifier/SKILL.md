---
name: requirement-clarifier
description: Use for converting ambiguous requests into explicit implementation contracts via assumptions, acceptance criteria, non-goals, constraints, and scope boundaries before major execution.
---

# Requirement Clarifier

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Trigger Rule`
3. `Clarification Contract`

### Action Modules (Read As Needed)
1. Clarifying ambiguous requests:
   - `Workflow`
2. Preventing scope drift:
   - `Scope Drift Controls`

### Output
1. `Output Contract`

## Mission
Prevent misbuilds by making requirements testable and unambiguous before implementation.

## Trigger Rule
Use this skill when:
1. request is ambiguous or high-impact
2. multiple interpretations are plausible
3. acceptance criteria are missing
4. constraints/non-goals are unclear

## Clarification Contract
Produce and maintain:
1. `Goal`
2. `In-Scope`
3. `Out-of-Scope`
4. `Assumptions`
5. `Constraints`
6. `Acceptance Criteria` (verifiable)
7. `Open Questions` (only if blocking)

## Workflow
1. infer initial contract from user prompt and repo context
2. state assumptions explicitly
3. propose acceptance checks tied to outcomes
4. proceed with safest reasonable assumptions unless high-risk ambiguity remains
5. update contract when user clarifies or requirements evolve

## Scope Drift Controls
1. do not add enhancements that violate explicit user intent
2. separate must-have from optional improvements
3. capture deferred ideas explicitly

## Output Contract
When applying this skill, provide:
1. clarified requirement block
2. acceptance criteria list
3. non-goals list
4. assumption/risk notes

## Related Skills
- [Thoughtful Approach](../thoughtful-approach/SKILL.md): user-value-oriented enhancements after must-haves are clear.
- [Order of Operations](../order-of-operations/SKILL.md): sequence clarified requirements into execution.
- [Skill Governance](../skill-governance/SKILL.md): choose process strictness for ambiguous/high-risk requests.
