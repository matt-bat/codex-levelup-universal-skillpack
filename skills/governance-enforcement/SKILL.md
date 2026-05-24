---
name: governance-enforcement
description: Use for executing and enforcing governance tooling (artifact generation/validation/CI policy checks), including startup declaration checks, project-index sync checks, and repository skill-policy validation.
---

# Governance Enforcement

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Scope Boundary`
3. `Trigger Rule`

### Action Modules (Read As Needed)
1. Running enforcement commands:
   - `Primary Tooling`
   - `Enforcement Workflow`
2. Diagnosing failures:
   - `Required Validation Targets`
   - `Failure Handling`

### Output
1. `Output Contract`

## Mission
Turn governance policy into deterministic machine-enforced checks.

## Scope Boundary
This skill is tooling/enforcement only.

Use [Skill Governance](../skill-governance/SKILL.md) for:
1. risk scoring
2. mode selection
3. gate policy decisions

## Trigger Rule
Use this skill when:
1. generating governance artifacts
2. validating artifact readiness
3. enforcing governance/skill policy in CI
4. debugging governance check failures

## Primary Tooling
1. `skills/skill-governance/scripts/generate_governance_artifact.py`
2. `skills/skill-governance/scripts/validate_governance_artifact.py`
3. `skills/skill-governance/scripts/enforce_governance_ci.py`
4. `skills/skill-governance/scripts/validate_skill_policy.py`
5. `skills/skill-governance/scripts/validate_skill_order_sync.py`
6. `.github/workflows/skills-governance-ci.yml` (active repository workflow)
7. `skills/docs/ci/skills-governance-ci.yml` (copyable workflow template)

## Enforcement Workflow
1. generate artifact at task start with required intake/startup fields
2. update gate statuses during execution
3. validate artifact before release recommendation
4. validate skill ordering sync (`SKILL-MAP.md` vs `docs/skill-index.md`)
5. run CI enforcement for changed governance scope
6. resolve failures with precise remediation
7. run validator regression tests for script changes

## Required Validation Targets
1. `AGENTS.md` policy snippets
2. required skill snippet presence
3. `user-instructions.md` schema/status/timestamp/evidence rules
4. governance JSON/MD pairing
5. startup declaration completeness
6. project-index consistency checks
7. skill-catalog consistency checks (`*/SKILL.md` vs `SKILL-MAP.md` vs `docs/skill-index.md`)
8. governed-path scope checks (`skills/**`, `.codex/skills/**`, `docs/governance/**`, `docs/project-index.md`, `AGENTS.md`, `.github/workflows/**`)

## Regression Test Command
Run after governance-script changes:
```bash
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py' -v
```

## Failure Handling
If enforcement fails:
1. report exact failing condition and file
2. classify failure type (`schema`, `policy`, `artifact`, `staleness`, `gate-state`)
3. propose minimal corrective patch
4. rerun targeted validator first, then full enforcement

## Output Contract
When applying this skill, provide:
1. commands run
2. pass/fail summary per validator
3. failing checks and remediations
4. final enforcement state

## Related Skills
- [Skill Governance](../skill-governance/SKILL.md): governance policy and risk logic.
- [Doc Maintenance](../doc-maintenance/SKILL.md): policy artifact updates after enforcement changes.
- [File Maintenance](../file-maintenance/SKILL.md): lifecycle accuracy checks for policy and operational artifacts.
