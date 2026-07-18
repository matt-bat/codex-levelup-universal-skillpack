---
name: semantic-policy-audit
description: Audit whether a task descriptor, selected skills, authority, gates, artifacts, execution, and completion claims semantically match user intent and actual effects. Use for policy-system audits or high-confidence governed review; do not use for ordinary implementation or mechanical schema checks.
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
1. a policy or routing system itself is being audited for intent-level correctness
2. governed work requires an explicit high-confidence semantic review beyond mechanical checks
3. governance artifacts exist but their applicability or evidence claims are uncertain
4. the user requests a strict semantic policy or compliance review

Do not use merely because:
1. an implementation touches several files or selects several skills
2. a task is ordinary implementation with no policy-conformance decision
3. schema, snippet, or command checks fully answer the validation question

## Scope Boundary
This skill audits semantic correctness.

Use [Governance Enforcement](../governance-enforcement/SKILL.md) for:
1. mechanical/script-based validation execution

## Audit Dimensions
1. intent-to-skill alignment:
   - requested task intent matches selected skills
   - action and operational effect are classified separately from topic words
2. gate applicability alignment:
   - required/conditional gates are actually appropriate
   - mandatory safety gates are not suppressed by budgets
3. declaration-to-execution alignment:
   - startup declaration reflects true execution path
4. status-to-evidence alignment:
   - artifacts claim only what evidence supports
5. policy conflict detection:
   - identify contradictory instructions across policy docs/skills
6. authority and mutation alignment:
   - every write, external action, or irreversible effect has matching authority
7. response-composition alignment:
   - deliverables, prohibitions, must-surface evidence, and vetoes survive final composition

## Audit Workflow
1. ingest the task descriptor, selected skills, governance artifacts, execution evidence, and key docs
2. derive expected skills/gates from action, effects, authority, and material uncertainty
3. compare expected vs declared/applied
4. classify gaps:
   - `missing_skill`
   - `extra_skill`
   - `missing_gate`
   - `misapplied_gate`
   - `evidence_mismatch`
   - `policy_conflict`
5. provide corrective actions with minimal disruption

Read-only audits must not update policy, trackers, indexes, or governance artifacts unless the user separately authorizes remediation.

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
