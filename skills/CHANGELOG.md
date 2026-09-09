# Changelog

All notable changes to Agent Command Center are documented in this file.

## [Unreleased]

### Added

- Added `agent-humility` with typed challenged/failed approach routing, evidence-first pivot checkpoints, structurally different alternative generation, discriminating probes, correction conduct, token discipline, and explicit authority boundaries.
- Added a website-style documentation home with learning paths, section navigation, guide-page return links, and regression tests that reject orphaned pages or broken local links.
- Added `advanced-svg` with a progressive SVG geometry, component, paint, filter, accessibility, security, and performance reference library plus deterministic SVG validation.
- Added dependency-free multi-size SVG rendering, PNG decoding, blank-output detection, and librsvg/Chromium pixel comparison with a reusable smoke asset.
- Added `advanced-r-and-d` with typed advanced-intensity routing, source ranking, version-aware API research, triangulation, and evidence-to-implementation gates.
- Added catalog-derived `--help` output, activation markers, supported-command guidance, and a one-time skillpack startup hint.
- Added a pure host runtime adapter and conformance suite for one-time startup messaging, exact `--` command parsing, conversation-local mode state, message digests, and router-ready patches.
- Added the mandatory `eliminate-assumptions` uncertainty gate and explicit `--clean-slate` fresh-context mode.
- Added router contract 2.1 with typed explicit-skill requests, repository-contained digest-verified artifact evidence, operation-scoped terminal gates, separate `configure_remote` authority, and compatible reads of version 2.0 descriptors and frozen results.
- Added schema-v3 governance artifacts with operation-specific authority, persisted risk inputs, typed gate evidence, exact catalog/relation binding, canonical JSON/Markdown pairs, and append-only history enforcement across the full commit range.
- Added release-purpose v3 metadata and full-diff enforcement for exact version, tag, changelog, release-notes, skill-count, and governance-test-count claims.
- Added a fully pinned governance dependency manifest and executable Draft 2020-12 JSON Schema validation, including a fail-closed RFC 3339 date-time checker.
- Added `.github/branch-protection-policy.json` as a closed desired-state contract plus a read-only GitHub verifier that rejects target mismatch, unsupported remote fields, and exact-setting drift.
- Added `internal-lang` as an optional explicit compact private scratch notation mode with `--internal-lang on/off` and `--internal-lang --response on/off` controls.
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
- Added a deterministic task descriptor and routing-result schema, a catalog-driven route resolver, semantic fixtures, and adversarial tests for trigger, exclusion, prerequisite, ordering, conflict, lifecycle, authority, command-effect, interface, test-intent, and recovery boundaries.
- Added bounded content-free routing observations with privacy and cache limits for the version 2 migration window.
- Added change-bound schema-v2 governance artifacts, exact manifest digests, immutable legacy-artifact checks, exact-head release attestations, and active workflow/template parity tests.
- Added `docs/skill-decision-tree.md`, `docs/known-limitations.md`, and five example workflows under `docs/examples/`.
- Added `USAGE.md` with first-person setup, activation, validation, maintenance, and licensing guidance for people downloading the skillpack from Git.
- Added active GitHub Actions governance CI at `.github/workflows/skills-governance-ci.yml`.
- Added `docs/governance-walkthrough.md` with artifact generation, strict validation, CI, and ready-to-push checklist guidance.
- Added root-level governance artifact and project index support for governed release-readiness changes.

### Changed

- Normalized every user-facing skill activation and toggle flag to the `--` prefix, including the former slash-prefixed `internal-lang` commands.
- Converted startup and conversation-mode behavior from prose-only guidance into an executable, fail-closed host protocol while preserving portable fallback requirements.
- Expanded branch-push CI to run the full governance suite and two-engine SVG smoke matrix with a commit-pinned setup action and exact Chrome-for-Testing version before pull-request integration; strict main-push enforcement remains scoped to `main`.
- Made pre-commit manifests hash Git-clean-filtered content through an isolated temporary index, and made canonical v3 Markdown end with exactly one newline so exact-head binding and diff hygiene cannot conflict.
- Moved passed-artifact routing scenarios to a dedicated byte-stable fixture so checked-in digests do not depend on checkout line-ending settings.
- Made the `governance` pull-request job run on every pull request targeting `main`; governed diffs require a new v3 plan while non-governed diffs still receive policy and regression checks.
- Moved protected-main changes to a feature-branch and pull-request workflow. The required `governance` check, administrator enforcement, and force-push/deletion blocks were verified on 2026-07-18.
- Replaced the universal baseline with routing architecture version 2: zero selected skills is valid, routine selection targets a median of no more than two and a normal cap of five, and mandatory safety skills and gates are never capped.
- Limited startup skill declarations to explicit requests and governed or audited work that needs a durable routing record.
- Narrowed broad skill triggers, made skill activation authority-neutral, and made durable instruction tracking opt-in with an explicit lifecycle.
- Split incidental command validation from deterministic and adaptive workflows; split running existing tests from test design; and made product, interface-quality, sequencing, documentation-sync, governance-tooling, release-enforcement, data-loss, and recovery decisions explicit typed inputs.
- Made backup and restore governance gates effect-driven instead of mode-driven. Deployment still requires rollback evidence but does not imply recovery controls without credible loss exposure or an explicit recovery requirement.
- Replaced hard-coded runtime skill selection with executable catalog routing modes and clauses. `requires`, `runs_after`, `supports`, `conflicts_with`, and lifecycle status now have distinct validated runtime behavior.
- Added exact-candidate-commit release provenance requirements. This work remains Unreleased; a normal source-branch push does not create a tag or publication, and changing remote protection remains a separately authorized `configure_remote` action.
- Preserved schema-v1 and schema-v2 governance records as readable historical evidence while requiring a unique, append-only schema-v3 artifact for every new governed change.
- Required every skill with `authorized_only` artifact durability to define an explicit `Authority and Artifact Policy` section, enforced by catalog validation.
- Made project-index parsing fail closed on malformed structure or fields so governance generation cannot silently discard or overwrite invalid rows.
- Removed non-executable relation-gate labels, required every remaining catalog gate to be exercised by canonical routing scenarios, closed fixture expectation keys, and bound conflict-matrix owners to typed catalog domains.
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
