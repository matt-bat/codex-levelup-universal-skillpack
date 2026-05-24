# Changelog

All notable changes to the Level-Up Codex Skillpack are documented in this file.

## [Unreleased]
### Added
- Added `USAGE.md` with first-person setup, activation, validation, maintenance, and licensing guidance for people downloading the skillpack from Git.
- Added active GitHub Actions governance CI at `.github/workflows/skills-governance-ci.yml`.
- Added `docs/governance-walkthrough.md` with artifact generation, strict validation, CI, and ready-to-push checklist guidance.
- Added root-level governance artifact and project index support for governed release-readiness changes.

### Changed
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
