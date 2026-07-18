# Known Limitations

This skillpack improves agent consistency, but it does not remove the need for judgment. It gives the agent a better workflow; it does not prove the agent made the best possible decision.

## Process Weight
The pack can feel too heavy for small tasks if every related skill is selected. Routing architecture version 2 treats zero selected skills as valid, targets a routine median of no more than two skills, and sets a normal cap of five. Mandatory safety skills and gates are never capped to meet that budget.

Use [skill-decision-tree.md](./skill-decision-tree.md), [install-profiles.md](./install-profiles.md), and the minimum viable rules in `AGENTS.md` to keep simple work simple. `process-budget-controller` is deprecated and remains only as a compatibility wrapper; the router now owns the budget.

## Model Compliance
Many skills are behavioral instructions. Validators can enforce files, routing, artifacts, schema, and required sections, but they cannot fully prove that a model followed every instruction semantically.

That is why the pack still relies on visible evidence: commands run, files changed, checks passed, and residual risk recorded.

`quizme-mode` is also behavioral. The policy and governed artifacts can record whether it is active and which options are enabled, but the runtime must preserve conversation state and expose an interactive clarification tool for the full experience. When that tool is unavailable, use concise conversational questions. `--record` only writes evidence when an appropriate durable artifact exists.

The version 2 resolver also expects a caller to normalize free-form requests into the typed task descriptor. It validates and routes that descriptor; it does not prove the normalization captured the user's intent. Material uncertainty, unknown command effects, and unknown recovery exposure fail closed, but a confidently incorrect descriptor still requires human or model review.

## Semantic Quality
Governance scripts validate structure and readiness evidence. They do not prove that every policy choice is optimal, every test is meaningful, or every risk assessment is complete.

For intent-level questions, use `semantic-policy-audit` and human review where the decision matters.

## Environment Constraints
Local machines may lack browsers, system libraries, network access, credentials, or deployment permissions. When that happens, use [verification/constrained-environment-verification.md](./verification/constrained-environment-verification.md) and record the exact blocker.

Do not replace a blocked check with a vague claim that validation was clean.

## Public Reuse
The license is intentionally restrictive and non-commercial without written permission. That protects ownership but may limit outside adoption and contribution.

If you want broader community adoption, the licensing model would need to be revisited deliberately.

## Generated View Maintenance
Schema-v2 `skills/skill-catalog.json` is the canonical routing source. `skills/SKILL-MAP.md`, `skills/docs/skill-index.md`, and `skills/docs/skill-decision-tree.md` are generated views and should not be maintained independently.

Generation and drift validation reduce contradictory edits, but they do not prove that the routing policy itself is optimal. Review the catalog semantics when changing triggers or ownership.

## Release Provenance And External Controls
The current routing-architecture work remains Unreleased. A normal branch push can make the source commit available without creating a tag or publishing a release. The next release must still bind its version, notes, changelog, validation results, and governance evidence to one exact candidate commit.

Repository-local checks cannot configure remote branch protection. Requiring the governance check on the protected release branch remains an external repository-administration action; see [release-provenance.md](./release-provenance.md).

## Controlled Growth
The pack can still become too broad if every good idea becomes a new skill. Use [pruning-policy.md](./pruning-policy.md), [field-notes.md](./field-notes.md), and `skill-usage-review` before adding more skills.

Good additions should replace repeated manual work, remove complexity elsewhere, or add enforceable safety value.
