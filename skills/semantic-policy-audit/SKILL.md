---
name: semantic-policy-audit
description: Use for intent-level policy compliance checks beyond snippet presence, including whether selected skills, declared gates, and execution behavior semantically match task intent and risk.
---

# Semantic Policy Audit

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Trigger Rule`
3. `Scope Boundary`

### Action Modules (Read As Needed)
1. Performing intent-level audits:
   - `Audit Dimensions`
   - `Audit Workflow`
2. Reporting compliance gaps:
   - `Output Contract`

## Mission
Detect policy drift that passes simple text checks but fails intent-level correctness.

## Trigger Rule
Use this skill when:
1. policy compliance confidence is important
2. tasks are high-risk or multi-skill
3. governance artifacts exist but applicability is uncertain
4. user requests strict audit/compliance review

## Scope Boundary
This skill audits semantic correctness.

Use [Governance Enforcement](../governance-enforcement/SKILL.md) for:
1. mechanical/script-based validation execution

## Audit Dimensions
1. intent-to-skill alignment:
   - requested task intent matches selected skills
2. gate applicability alignment:
   - required/conditional gates are actually appropriate
3. declaration-to-execution alignment:
   - startup declaration reflects true execution path
4. status-to-evidence alignment:
   - artifacts claim only what evidence supports
5. policy conflict detection:
   - identify contradictory instructions across policy docs/skills

## Audit Workflow
1. ingest task intent, selected skills, governance artifacts, and key docs
2. derive expected skills/gates from intent heuristics
3. compare expected vs declared/applied
4. classify gaps:
   - `missing_skill`
   - `extra_skill`
   - `missing_gate`
   - `misapplied_gate`
   - `evidence_mismatch`
   - `policy_conflict`
5. provide corrective actions with minimal disruption

## Output Contract
When applying this skill, provide:
1. expected-vs-observed matrix
2. gap classification list
3. severity per gap (`low/medium/high`)
4. remediation plan and residual risk

## Related Skills
- [Skill Governance](../skill-governance/SKILL.md): source policy and risk model.
- [Governance Enforcement](../governance-enforcement/SKILL.md): executes validator scripts.
- [Thoroughly Rate Review](../thoroughly-rate-review/SKILL.md): weighted scoring when audit results need a formal score.
