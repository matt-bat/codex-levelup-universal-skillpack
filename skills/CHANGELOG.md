# Changelog

All notable changes to Codex Command Center are documented in this file.

## [Unreleased]
### Added
- Added `quizme-mode` with persistent conversation-local `--quizme` toggling, exact immediate `--mc` multiple-choice preference, interactive clarification routing, governance artifact state, and policy validation coverage.
- Expanded `quizme-mode` with intuitive `--one-at-a-time`, `--confirm`, and `--record` options; `--record` implies confirmation and governed artifacts persist every option.
- Added `START_HERE.md`, `docs/maturity-model.md`, `docs/field-notes.md`, `docs/pruning-policy.md`, and `docs/validation-profiles.md` to support controlled growth and evidence-driven simplification.
- Added `process-budget-controller`, `skill-usage-review`, and `deprecation-management` to support restraint, usage feedback, and lifecycle management.
- Added adoption and lifecycle docs: `docs/install-profiles.md`, `docs/conflict-resolution-matrix.md`, `docs/validator-severity-levels.md`, adapter docs, and quality rubrics.
- Added root `.gitattributes` and `.editorconfig` to lock LF line endings and editor formatting.
- Added `CONTRIBUTING.md` and `SECURITY.md` for contribution, validation, and policy-bypass reporting guidance.
- Added `skill-catalog.json` as a machine-readable inventory of skill triggers, dependencies, artifacts, and risk levels.
- Added `docs/skill-decision-tree.md`, `docs/known-limitations.md`, and five example workflows under `docs/examples/`.
- Added `USAGE.md` with first-person setup, activation, validation, maintenance, and licensing guidance for people downloading the skillpack from Git.
- Added active GitHub Actions governance CI at `.github/workflows/skills-governance-ci.yml`.
- Added `docs/governance-walkthrough.md` with artifact generation, strict validation, CI, and ready-to-push checklist guidance.
- Added root-level governance artifact and project index support for governed release-readiness changes.

### Changed
- Refreshed user-facing documentation with a more casual tone, fuller explanations, clearer setup guidance, and stronger validation/readiness context across the root docs, usage docs, install/routing docs, adapters, rubrics, examples, and constrained-environment guidance.
- Added minimum viable skill-use rules to reduce over-governance on small tasks.
- Added anti-overuse rules to high-overlap skills covering documentation, file maintenance, history/cache management, and governance.
- Extended policy validation to check the machine-readable catalog and anti-overuse sections.
- Updated `README.md` for stronger GitHub discoverability with codex/agent-skill keywords, refined summary language, and suggested topics/tags.
- Added bounded-memory, root-cause verification, interdependent-change planning, and cache-budget skills; synced routing docs and governance policy for the expanded skillset.
- Updated governance CI paths to support this repository's `skills/` layout directly.

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
