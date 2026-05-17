---
name: thoroughly-rate-review
description: Use for any request to review, rate, score, assess, evaluate, grade, benchmark, or otherwise judge quality; applies a custom weighted scoring model with multiple checks per category, explicit evidence, and a clear final score.
---

# Thoroughly Rate Review

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Scope Boundary`
3. `Trigger Rule (Required)`
4. `Core Method`

### Action Modules (Read As Needed)
1. Building weighted rubric:
   - `Weighted Framework Standard`
   - `Assessment Structure`
   - `Scoring Anchors (0-5)`
2. Evidence and confidence handling:
   - `Evidence Discipline`
3. Mode-specific depth:
   - `Review Modes`
4. Comparing multiple options:
   - `Comparison Mode (Optional)`

### Output
1. `Output Contract (Required)`
2. `Anti-Patterns`

## Mission
Provide rigorous, explainable, and repeatable ratings instead of ad-hoc opinions.

## Scope Boundary
This skill evaluates quality with weighted scoring.

Do not use this skill to choose governance mode/gates for execution planning.
Use [Skill Governance](../skill-governance/SKILL.md) for risk-mode and gate policy decisions.

## Trigger Rule (Required)
Use this skill whenever user intent is to evaluate quality, including synonyms such as:
1. review
2. rate
3. score
4. assess
5. evaluate
6. grade
7. benchmark
8. compare quality
9. audit quality

If intent is ambiguous:
1. assume evaluation intent when user asks “how good,” “how strong,” or “how would you rate”
2. proceed with the weighted framework

## Core Method
1. define weighted categories totaling 100%
2. define multiple assessment checks per category
3. score each check on a fixed scale
4. compute category and weighted totals
5. provide final score with strengths, gaps, and upgrade path

## Weighted Framework Standard
Default unless domain requires custom weights:
1. Coverage and Completeness: 14%
2. Correctness and Internal Consistency: 18%
3. Practical Utility and End-User Value: 14%
4. Safety, Risk Control, and Reliability: 14%
5. Enforceability and Operationalization: 14%
6. Clarity and Documentation Quality: 10%
7. Efficiency and Maintainability: 6%
8. Integration and Cohesiveness: 10%

All weights must sum to exactly 100%.

Mandatory rule:
1. for multi-skill systems/frameworks, `Integration and Cohesiveness` is required and cannot be omitted

## Assessment Structure
For each category:
1. define 3-6 concrete checks
2. score each check 0-5
3. compute category raw score:
   - `(sum(check scores) / max possible) * 100`
4. compute weighted contribution:
   - `category raw score * category weight`

Final score:
1. sum all weighted contributions
2. round to one decimal place
3. present as `X.Y / 100`

Integration and Cohesiveness checks (minimum set):
1. cross-component/skill trigger alignment
2. conflict-resolution compatibility
3. sequencing compatibility across scenarios
4. policy/runtime enforcement consistency

## Scoring Anchors (0-5)
1. 0: absent or broken
2. 1: major deficiencies
3. 2: partial and unreliable
4. 3: adequate baseline
5. 4: strong and consistent
6. 5: excellent and robust

## Evidence Discipline
Every non-trivial score must include evidence:
1. direct references to files/behaviors/artifacts
2. brief rationale for each category score
3. explicit assumptions when evidence is incomplete

If evidence is missing:
1. lower confidence
2. cap category score to avoid over-claiming
3. state what would raise confidence

## Output Contract (Required)
Return in this order:
1. framework used (weights + checks summary)
2. category-by-category table
3. final score
4. top strengths
5. top gaps
6. prioritized actions to improve score

## Review Modes
1. quick:
   - fewer checks per category, lower evidence depth
2. standard:
   - full weighted model and concise evidence
3. deep:
   - full weighted model + exhaustive evidence + scenario analysis

Default mode:
1. use `standard`
2. use `deep` if user asks “thorough,” “detailed,” or similar

## Comparison Mode (Optional)
When comparing options:
1. use same weighted framework for all options
2. score each option independently
3. include normalized side-by-side table
4. call out tradeoffs, not just winner

## Anti-Patterns
1. giving a score without explicit framework
2. changing weights mid-review without explanation
3. rating from intuition without evidence
4. ignoring user context or constraints
5. presenting a single number without actionable next steps

## Related Skills
- [Thoughtful Approach](../thoughtful-approach/SKILL.md): improves end-user oriented judgments in the scoring model.
- [Skill Governance](../skill-governance/SKILL.md): provides risk-aware process context for evaluations.
- [Doc Maintenance](../doc-maintenance/SKILL.md): ensures rating rationale is captured in durable docs when needed.
- [Token Reduction](../token-reduction/SKILL.md): keeps scoring outputs concise while preserving evidence.
