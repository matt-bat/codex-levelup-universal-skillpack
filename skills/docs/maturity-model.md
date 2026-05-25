# Maturity Model

Use this model to adopt the skillpack gradually instead of enabling every process at once.

## Level 1: Baseline Assistance
Goal: make simple work clearer and cheaper.

Required:
1. `token-reduction`
2. `order-of-operations`
3. `process-budget-controller`

Evidence:
1. startup declaration uses a small skill set
2. small tasks avoid governance artifacts
3. final answers stay concise

## Level 2: Developer Workflow
Goal: make normal coding work safer.

Required:
1. Level 1 skills
2. `scripted-command-execution`
3. `diagnose-before-fix`
4. `regression-prevention`
5. `effective-testing-methods`
6. `doc-maintenance`

Evidence:
1. bugs are reproduced before fixes when practical
2. behavior changes get targeted validation
3. docs update when workflows change

## Level 3: Governed Validation
Goal: make risky or release-affecting changes auditable.

Required:
1. Level 2 skills
2. `skill-governance`
3. `governance-enforcement`
4. `semantic-policy-audit`
5. `interdependent-change-planning`
6. `user-instructions-tracker`

Evidence:
1. governance artifacts exist for governed changes
2. strict artifact validation passes
3. CI checks enforce governed-change rules
4. user directives have evidence rows

## Level 4: Lifecycle Management
Goal: keep the skillpack maintainable as it grows.

Required:
1. Level 3 skills
2. `skill-usage-review`
3. `deprecation-management`
4. `file-maintenance`
5. `artifact-budget-enforcement`

Evidence:
1. overused and underused skills are reviewed
2. deprecated paths have replacements
3. cached artifacts stay bounded
4. stale docs are pruned or refreshed

## Level 5: Evidence-Driven Improvement
Goal: improve from real task outcomes, not speculation.

Required:
1. field notes
2. task logs
3. scenario refreshes
4. usage-review findings
5. pruning decisions

Evidence:
1. repeated friction creates concrete improvements
2. rarely used skills are merged, deprecated, or justified
3. examples reflect real tasks
4. validation profiles match actual risk

## Advancement Rule
Move up a level only when the previous level is being used consistently.

## Regression Rule
If users report process friction, drop one level for routine tasks and keep higher levels only for governed work.
