# Known Limitations

This skillpack improves agent consistency, but it does not remove the need for judgment. It gives the agent a better workflow; it does not prove the agent made the best possible decision.

## Process Weight
The pack can feel too heavy for small tasks if every related skill is selected. Use [skill-decision-tree.md](./skill-decision-tree.md), [install-profiles.md](./install-profiles.md), and the minimum viable rules in `AGENTS.md` to keep simple work simple.

When in doubt, start with fewer skills and add process only when it changes safety, clarity, or evidence.

## Model Compliance
Many skills are behavioral instructions. Validators can enforce files, routing, artifacts, schema, and required sections, but they cannot fully prove that a model followed every instruction semantically.

That is why the pack still relies on visible evidence: commands run, files changed, checks passed, and residual risk recorded.

`quizme-mode` is also behavioral. The policy and governed artifacts can record whether it is active and which options are enabled, but the runtime must preserve conversation state and expose an interactive clarification tool for the full experience. When that tool is unavailable, use concise conversational questions. `--record` only writes evidence when an appropriate durable artifact exists.

## Semantic Quality
Governance scripts validate structure and readiness evidence. They do not prove that every policy choice is optimal, every test is meaningful, or every risk assessment is complete.

For intent-level questions, use `semantic-policy-audit` and human review where the decision matters.

## Environment Constraints
Local machines may lack browsers, system libraries, network access, credentials, or deployment permissions. When that happens, use [verification/constrained-environment-verification.md](./verification/constrained-environment-verification.md) and record the exact blocker.

Do not replace a blocked check with a vague claim that validation was clean.

## Public Reuse
The license is intentionally restrictive and non-commercial without written permission. That protects ownership but may limit outside adoption and contribution.

If you want broader community adoption, the licensing model would need to be revisited deliberately.

## Timestamp Maintenance
`skills/docs/skill-index.md` includes `Last Updated UTC` fields. These are useful for auditability, but they require discipline when changing triggers or skill ownership.

If those timestamps are ignored, they become noise. Keep them current when the indexed behavior changes.

## Controlled Growth
The pack can still become too broad if every good idea becomes a new skill. Use [pruning-policy.md](./pruning-policy.md), [field-notes.md](./field-notes.md), and `skill-usage-review` before adding more skills.

Good additions should replace repeated manual work, remove complexity elsewhere, or add enforceable safety value.
