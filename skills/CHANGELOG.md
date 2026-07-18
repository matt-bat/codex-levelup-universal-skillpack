# Changelog

All notable changes to Agent Command Center are documented in this file.

## [Unreleased]
### Added
- Added `internal-lang` as an optional explicit compact private scratch notation mode with `/internal-lang on/off` and `/internal-lang --response on/off` controls.
- Added `hyperfocus-discovery` as a conditionally triggered bounded same-task branching mode with resume notes, switch gates, and completion reconciliation.
- Tightened `internal-lang` and `hyperfocus-discovery` with deterministic state, progressive-disclosure references, compression, switching, convergence, and quality gates plus regression coverage.
- Added `quizme-mode` with persistent conversation-local `--quizme` toggling, exact immediate `--mc` multiple-choice preference, interactive clarification routing, governance artifact state, and policy validation coverage.
- Expanded `quizme-mode` with intuitive `--one-at-a-time`, `--confirm`, and `--record` options; `--record` implies confirmation and governed artifacts persist every option.
- Added `START_HERE.md`, `docs/maturity-model.md`, `docs/field-notes.md`, `docs/pruning-policy.md`, and `docs/validation-profiles.md` to support controlled growth and evidence-driven simplification.
- Added `process-budget-controller` as an initial restraint mechanism, plus `skill-usage-review` and `deprecation-management` for usage feedback and lifecycle management.
- Added adoption and lifecycle docs: `docs/install-profiles.md`, `docs/conflict-resolution-matrix.md`, `docs/validator-severity-levels.md`, adapter docs, and quality rubrics.
- Added root `.gitattributes` and `.editorconfig` to lock LF line endings and editor formatting.
- Added `CONTRIBUTING.md` and `SECURITY.md` for contribution, validation, and policy-bypass reporting guidance.
- Added schema-v2 `skill-catalog.json` as the canonical machine-readable routing source and added generation for `SKILL-MAP.md`, `docs/skill-index.md`, and `docs/skill-decision-tree.md`.
- Added a deterministic task descriptor and routing-result schema, a catalog-driven route resolver, 25 semantic fixtures, and adversarial tests for trigger, exclusion, prerequisite, ordering, conflict, lifecycle, authority, command-effect, interface, test-intent, and recovery boundaries.
- Added bounded content-free routing observations with privacy and cache limits for the version 2 migration window.
- Added change-bound schema-v2 governance artifacts, exact manifest digests, immutable legacy-artifact checks, exact-head release attestations, and active workflow/template parity tests.
- Added `docs/skill-decision-tree.md`, `docs/known-limitations.md`, and five example workflows under `docs/examples/`.
- Added `USAGE.md` with first-person setup, activation, validation, maintenance, and licensing guidance for people downloading the skillpack from Git.
- Added active GitHub Actions governance CI at `.github/workflows/skills-governance-ci.yml`.
- Added `docs/governance-walkthrough.md` with artifact generation, strict validation, CI, and ready-to-push checklist guidance.
- Added root-level governance artifact and project index support for governed release-readiness changes.

### Changed
- Replaced the universal baseline with routing architecture version 2: zero selected skills is valid, routine selection targets a median of no more than two and a normal cap of five, and mandatory safety skills and gates are never capped.
- Limited startup skill declarations to explicit requests and governed or audited work.
- Narrowed broad skill triggers, made skill activation authority-neutral, and made durable instruction tracking opt-in with an explicit lifecycle.
- Split incidental command validation from deterministic and adaptive workflows; split running existing tests from test design; and made product, interface-quality, sequencing, documentation-sync, governance-tooling, release-enforcement, data-loss, and recovery decisions explicit typed inputs.
- Made backup and restore governance gates effect-driven instead of mode-driven. Deployment still requires rollback evidence but does not imply recovery controls without credible loss exposure or an explicit recovery requirement.
- Replaced hard-coded runtime skill selection with executable catalog routing modes and clauses. `requires`, `runs_after`, `supports`, `conflicts_with`, and lifecycle status now have distinct validated runtime behavior.
- Added exact-candidate-commit release provenance requirements. This work remains Unreleased; a normal source-branch push does not create a tag or publication, and remote branch-protection configuration remains a separate administrative action.
- Refreshed user-facing documentation with a more casual tone, fuller explanations, clearer setup guidance, and stronger validation/readiness context across the root docs, usage docs, install/routing docs, adapters, rubrics, examples, and constrained-environment guidance.
- Added minimum viable skill-use rules to reduce over-governance on small tasks.
- Added anti-overuse rules to high-overlap skills covering documentation, file maintenance, history/cache management, and governance.
- Extended policy validation to check the machine-readable catalog and anti-overuse sections.
- Updated `README.md` for stronger GitHub discoverability with agent-centric keywords, refined summary language, and suggested topics/tags.
- Added bounded-memory, root-cause verification, interdependent-change planning, and cache-budget skills; synced routing docs and governance policy for the expanded skillset.
- Updated governance CI paths to support this repository's `skills/` layout directly.

### Deprecated
- Deprecated `process-budget-controller` as a compatibility wrapper. Routing architecture version 2 owns process budgeting directly.

### Removed
- Removed tracked Python cache artifacts from governance script and test directories.

## [1.0.0] - 2026-05-17
### Added
- Public skillpack README with:
  - skillset summary
  - inter-skill architecture and ownership layering
  - governance model and enforcement tooling
  - prioritization and conflict resolution order
  - intended outcomes and maintenance expectations
- Restrictive attribution-required non-commercial license.
- Explicit version file (`VERSION`).
- Governance and release-readiness guidance for external publishing.
