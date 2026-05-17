---
name: order-of-operations
description: Use for reordering requested steps into dependency-correct execution order, ensuring optimal and safe operations regardless of the order instructions were provided.
---

# Order of Operations

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Core Principle`
3. `Scope Boundary`
4. `Hard Rule`
5. `Trigger Examples`

### Action Modules (Read As Needed)
1. Building execution graph:
   - `Sequencing Model`
   - `Ideal Execution Phases`
   - `Reordering Rules`
2. Safety gating:
   - `Safety-First Overrides`
   - `Validation Ordering Rules`
3. Concurrency decisions:
   - `Parallelization Rules`
4. Conflict and edge handling:
   - `Conflict Resolution`
   - `Operational Decision Matrix`
   - `Documentation Sequencing`
   - `Escalation Conditions`

### Output
1. `Deliverable Format`
2. `Anti-Patterns`

## Mission
Execute work in the correct operational sequence, even when user instructions are listed in a non-optimal order.

## Core Principle
Instruction order in a prompt is not automatically execution order.
Execution order must follow:
1. dependencies
2. safety constraints
3. validation prerequisites
4. rollback/recovery readiness

## Scope Boundary
Use this skill for explicit multi-step dependency sequencing and risk-aware reordering.

Do not invoke solely for trivial single-step tasks where baseline execution ordering is obvious.

Cross-skill handoff rule:
1. when sequence step N triggers another skill, consult `docs/skill-index.md` before adding it to execution order

## Hard Rule
Always follow the ideal order of operations when instruction order conflicts with required sequencing.

If explicit user ordering is unsafe or dependency-invalid:
1. reorder to safe sequence
2. explain why briefly
3. continue unless user explicitly requests a pause

## Trigger Examples
Use this skill when requests contain:
1. multi-step tasks in mixed order
2. parallel asks with hidden dependencies
3. risky changes before safeguards
4. “do X then Y” where Y is a prerequisite for X

## Sequencing Model
For each requested action, classify:
1. prerequisites
2. side effects
3. verification requirements
4. rollback impact

Then build execution graph:
1. nodes = actions
2. edges = dependencies
3. critical path = must-run sequence
4. parallel path = independent actions safe to run concurrently

## Ideal Execution Phases
Use this default phase order unless context requires variation:
1. **Clarify scope and constraints**
2. **Run new-project intake** (if model has not worked on project: ask test/build ownership preference and index metadata)
3. **Establish safety rails** (backup, rollback, environment checks)
4. **Gather required context/artifacts**
5. **Apply foundational changes** (schema/config/primitives)
6. **Apply dependent changes** (features/integrations/UI)
7. **Run validation layers** (static/unit/integration/E2E as needed)
8. **Update documentation and operational notes**
9. **Final verification + handoff summary**

## Reordering Rules
1. If user order is valid and safe, keep it.
2. If user order violates dependency/safety constraints, reorder and state why briefly.
3. If two steps conflict, prioritize data integrity and reversibility.
4. If ambiguous dependency exists, resolve with minimal clarifying question or safest assumption.
5. If user explicitly insists on unsafe order, escalate and require explicit risk acceptance.

## Safety-First Overrides
These operations must occur before risky mutation:
1. backup gate for high-risk changes
2. environment/credential verification
3. migration plan review for schema changes
4. rollback path identification
5. deployment confirmation gate (explicit user request required)

Never execute destructive or irreversible steps before safeguards.
Never deploy by default.

## Validation Ordering Rules
Pre-validation dependency probe (required for expensive layers):
1. verify layer prerequisites first (runtime binaries, browsers, system libraries, network access)
2. if prerequisite is missing, switch to constrained verification protocol rather than repeatedly re-running blocked commands

1. run fast, cheap checks early
2. block expensive end-to-end tests when foundational checks fail
3. only proceed to next stage when prior gate passes or risk is explicitly accepted

Recommended validation sequence:
1. lint/type/static checks
2. unit tests
3. integration/contract checks
4. E2E/smoke checks
5. post-change runtime sanity checks

Constrained verification branch:
1. static checks
2. test discovery/listing for blocked layers
3. targeted non-blocked checks
4. explicit residual-risk evidence

## Parallelization Rules
Parallelize only independent actions.

Can parallelize:
1. independent file reads
2. independent non-mutating diagnostics
3. unrelated test subsets

Do not parallelize:
1. steps sharing mutable state
2. steps with ordering dependencies
3. operations whose outputs feed each other

Parallelization gate:
1. confirm no shared mutable state
2. confirm deterministic merge of outputs
3. confirm rollback isolation per parallel branch

## Conflict Resolution
When explicit instructions conflict with ideal sequence:
1. preserve user intent
2. reorder execution
3. explain succinctly: "reordered for dependency/safety correctness"
4. continue without unnecessary delay

## Operational Decision Matrix
If request includes:
1. schema changes + feature changes:
   - schema prep first, feature updates second
2. dependency upgrades + bug fixes:
   - dependency compatibility gate first, bug fix implementation after
3. auth/session changes + UI updates:
   - backend/auth contract first, UI adaptation second
4. backup setup + risky refactor:
   - backup and restore checks first, refactor after

## Documentation Sequencing
Doc updates should follow validated implementation state.
Order:
1. critical runbooks during/after risky changes
2. README and usage docs after command/workflow changes
3. architecture docs after stable implementation is confirmed

If documentation is prerequisite for safe operation (for example runbook execution), update before risky steps.

## Escalation Conditions
Pause and escalate when:
1. prerequisites cannot be satisfied
2. execution graph contains unresolved circular dependency
3. rollback path is unknown for high-risk step
4. required validation cannot run
5. user-mandated order conflicts with irreversible-risk constraints

## Anti-Patterns
1. blindly executing user-listed order with dependency violations
2. running expensive validations before basic gates
3. performing doc updates before final behavior is known
4. treating all tasks as parallel when shared state exists
5. skipping reorder explanation when sequence changed

## Deliverable Format
When applying this skill, provide:
1. requested steps (normalized)
2. dependency-correct execution order
3. what was reordered and why
4. validation gates and outcomes
5. remaining risks/blockers

## Related Skills
- [Skill Governance](../skill-governance/SKILL.md): select required process mode and gates before sequencing.
- [Scripted Command Execution](../scripted-command-execution/SKILL.md): execute ordered command plans deterministically.
- [Regression Prevention](../regression-prevention/SKILL.md): ensure reordered execution still satisfies risk-tier validation.
- [Effective Testing Methods](../effective-testing-methods/SKILL.md): sequence unit and Playwright amendments after behavior changes.
- [File Structure Optimization](../file-structure-optimization/SKILL.md): plan safe ordering for file moves and consolidation.
- [Project Backup](../project-backup/SKILL.md): enforce backup-first sequencing for risky changes.
- [Restore Drill](../restore-drill/SKILL.md): validate restore readiness before high-impact operations.
- [Doc Maintenance](../doc-maintenance/SKILL.md): sequence documentation updates correctly relative to implementation.
