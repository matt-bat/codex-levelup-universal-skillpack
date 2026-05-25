# Known Limitations

This skillpack improves agent consistency, but it does not remove the need for judgment.

## Process Weight
The pack can be too heavy for small tasks if every related skill is selected. Use `skills/docs/skill-decision-tree.md` and the minimum viable skill rules in `AGENTS.md` to keep simple work simple.

## Model Compliance
Many skills are behavioral instructions. Validators can enforce files, routing, artifacts, and schema, but they cannot fully prove that a model followed every instruction semantically.

## Semantic Quality
Governance scripts validate structure and readiness evidence. They do not prove that every policy choice is optimal, every test is meaningful, or every risk assessment is complete.

## Environment Constraints
Local machines may lack browsers, system libraries, network access, credentials, or deployment permissions. When that happens, use `skills/docs/verification/constrained-environment-verification.md` and record residual risk.

## Public Reuse
The license is intentionally restrictive and non-commercial without written permission. That protects ownership but may limit outside adoption and contribution.

## Timestamp Maintenance
`skills/docs/skill-index.md` includes `Last Updated UTC` fields. These are useful for auditability, but they require discipline when changing triggers or skill ownership.

## Controlled Growth
The pack can still become too broad if new ideas are always implemented as new skills. Use `skills/docs/pruning-policy.md`, `skills/docs/field-notes.md`, and `skill-usage-review` before adding more skills.
