# Governance Artifact: LIFECYCLE-SKILLPACK-20260524

- `created_at_utc`: 2026-05-25T03:34:23.041834+00:00
- `project_id`: agent-command-center
- `profile`: internal
- `project_language`: Markdown/Python
- `project_description_max4`: Agent skillpack governance
- `model_runs_test_build_default`: yes
- `execution_scope`: local_only
- `deployment_requested`: false
- `execution_skill`: scripted-command-execution
- `quizme_mode`: off
- `quizme_multiple_choice`: false
- `quizme_one_at_a_time`: false
- `quizme_confirm`: false
- `quizme_record`: false
- `selected_mode`: standard
- `total_score`: 5
- `recommendation`: go

## Scores
- `data_impact`: 0
- `business_impact`: 1
- `change_complexity`: 2
- `dependency_uncertainty`: 1
- `recoverability`: 1

## Critical Overrides
- none

## Required Gates
- [x] `order-of-operations` (status: pass)
- [x] `scripted-command-execution` (status: pass)
- [x] `regression-prevention` (status: pass)
- [x] `token-reduction` (status: pass)
- [x] `doc-maintenance` (status: pass)

## Startup Declaration
### Skills In Use
- `token-reduction`
- `process-budget-controller`
- `order-of-operations`
- `skill-governance`
- `interdependent-change-planning`
- `regression-prevention`
- `scripted-command-execution`
- `doc-maintenance`
- `user-instructions-tracker`
### Skill Selection Rationale
Governed lifecycle improvement batch adding process restraint, usage review, deprecation management, adoption profiles, conflict matrix, rubrics, adapters, and validator severity guidance.
### Skill Execution Order
- `token-reduction`
- `process-budget-controller`
- `order-of-operations`
- `skill-governance`
- `interdependent-change-planning`
- `regression-prevention`
- `scripted-command-execution`
- `doc-maintenance`
- `user-instructions-tracker`

## Evidence Requirements
- [x] mode + score
- [x] impact map
- [x] validation scope by layer
- [x] residual risks

## Break Glass
- enabled: false

## Notes
Lifecycle improvement batch added process-budget control, usage review, deprecation management, install profiles, conflict matrix, validator severity guidance, rubrics, and adapter docs.

Validation scope:
1. policy validator
2. skill order sync validator
3. strict governance artifact validation
4. governance unit tests
5. Python compile checks
6. git diff hygiene
7. tracked-cache scan

Residual risk:
1. GitHub Actions must run after push in GitHub's hosted environment
