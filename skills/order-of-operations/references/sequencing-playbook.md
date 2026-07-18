# Sequencing Playbook

Use this reference only for an active, genuinely multi-step sequencing problem.

## Dependency Model

For each action, identify:
1. required inputs or state
2. observable outputs
3. mutable side effects
4. rollback or recovery implications
5. checks that can prove completion

Represent actions as nodes and true prerequisites as directed edges. A circular dependency is a blocker until one edge is removed, staged, or clarified.

## Typical Phases

Adapt rather than mechanically applying this order:
1. resolve blocking ambiguity and authority
2. inspect current state and required context
3. establish safeguards for risky mutation
4. make foundational changes
5. make dependent changes
6. run cheapest relevant checks before expensive checks
7. update already-authorized documentation or operational artifacts
8. inspect final state and hand off evidence

## Validation Staging

1. Probe prerequisites before expensive test layers.
2. Run static or fast targeted checks before broader suites.
3. Do not spend on downstream validation while a foundational check is failing unless it provides independent evidence.
4. When a layer is blocked, record the exact blocker and use relevant non-blocked evidence.
5. Never claim full validation when a critical layer did not run.

## Parallelization

Parallelize only when branches:
1. share no mutable state
2. do not consume each other's output
3. have deterministic reconciliation
4. can fail or roll back independently

Independent reads and non-mutating diagnostics are common candidates. Coupled edits, migrations, and dependent commands are not.

## Conflict Handling

1. Preserve user intent and explicit constraints.
2. Prefer reversible, dependency-valid sequencing.
3. Briefly explain a necessary reorder.
4. Ask only when competing valid sequences materially change the outcome or authority required.
5. Refuse or pause rather than execute an irreversible unsafe order.

## Examples

1. Schema plus feature: establish the compatible schema state before dependent code.
2. Backup plus destructive migration: verify the authorized recovery path before mutation.
3. Contract plus consumer: preserve or stage the contract before updating consumers.
4. Implementation plus documentation: document the validated behavior, unless the document itself is an operational prerequisite.
