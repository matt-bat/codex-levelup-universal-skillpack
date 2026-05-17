# Level-Up Codex Skillpack: Governance-First Delivery Framework

## Summary
This skillpack is a policy-driven operating framework for Codex that improves delivery quality on complex software tasks.

It combines:
1. deterministic governance decisions
2. dependency-correct execution ordering
3. regression-aware testing and validation
4. synchronized documentation and instruction tracking
5. UX-focused skills for frontend work

The pack is designed to make outputs safer, more reproducible, and easier to audit.

## Release Metadata
- Current version: `1.0.0` (see [VERSION](./skills/VERSION))
- Change history: [CHANGELOG.md](./skills/CHANGELOG.md)
- License: [LICENSE](.skills/LICENSE)

## Skillset Overview
The pack currently contains 21 skills:
1. `skill-governance`
2. `governance-enforcement`
3. `requirement-clarifier`
4. `semantic-policy-audit`
5. `thoughtful-approach`
6. `thoroughly-rate-review`
7. `user-instructions-tracker`
8. `history-indexing`
9. `ui-spatial-canvas`
10. `ui-design-skills`
11. `effective-testing-methods`
12. `scripted-command-execution`
13. `pseudo-agentic-automation`
14. `token-reduction`
15. `order-of-operations`
16. `regression-prevention`
17. `file-structure-optimization`
18. `doc-maintenance`
19. `file-maintenance`
20. `project-backup`
21. `restore-drill`

## Interconnectedness Model
The skillpack is intentionally layered to avoid overlap and conflicting ownership.

### Layer 1: Policy and Mode Selection
- `skill-governance` selects mode, mandatory gates, and go or no-go posture.

### Layer 2: Sequencing and Scope Clarity
- `order-of-operations` enforces dependency-correct task flow.
- `requirement-clarifier` turns ambiguous requests into explicit acceptance contracts.

### Layer 3: Execution Path
- `scripted-command-execution` handles deterministic local command workflows.
- `pseudo-agentic-automation` handles dynamic browser or GUI runtime loops.

### Layer 4: Risk and Test Integrity
- `regression-prevention` classifies risk and controls release confidence.
- `effective-testing-methods` maps code changes to unit and Playwright coverage updates.

### Layer 5: Governance and Intent Assurance
- `governance-enforcement` executes validators and CI policy checks.
- `semantic-policy-audit` verifies intent-level compliance beyond string or schema checks.
- `thoroughly-rate-review` applies weighted quality scoring when evaluation is requested.

### Layer 6: Documentation and Continuity
- `doc-maintenance`, `file-maintenance`, `file-structure-optimization`, `user-instructions-tracker`, and `history-indexing` preserve long-horizon accuracy and traceability.

### Layer 7: Product and UX Value
- `thoughtful-approach`, `ui-design-skills`, and `ui-spatial-canvas` drive user-value decisions and coherent interaction architecture.

The canonical cross-skill routing source is [docs/skill-index.md](./docs/skill-index.md), with execution scenarios in [SKILL-MAP.md](./SKILL-MAP.md).

## Governance System
Governance is not optional in risky or multi-step work.

Key controls:
1. startup declaration requires explicit `skills_in_use`, rationale, and execution order
2. validator checks enforce policy snippets, startup declaration integrity, skill catalog sync, and artifact pairing
3. ordering sync check fails if `SKILL-MAP.md` and `docs/skill-index.md` drift
4. CI entrypoint enforces governed scope and requires governance artifacts when governed files change
5. regression tests cover governance validator behavior

Primary governance tooling:
- `skill-governance/scripts/generate_governance_artifact.py`
- `skill-governance/scripts/validate_governance_artifact.py`
- `skill-governance/scripts/validate_skill_policy.py`
- `skill-governance/scripts/validate_skill_order_sync.py`
- `skill-governance/scripts/enforce_governance_ci.py`
- `docs/ci/skills-governance-ci.yml` (workflow template)

## Prioritization and Decision Order
Default baseline:
1. `token-reduction`
2. `order-of-operations`
3. `doc-maintenance` when behavior, workflow, or policy changes

Conditional priorities:
1. choose governance first for risky, ambiguous, or multi-skill tasks
2. choose command execution mode (`scripted-command-execution` or `pseudo-agentic-automation`)
3. apply risk and testing controls before release recommendation
4. enforce documentation and instruction tracker updates before completion

Conflict resolution order:
1. policy (`skill-governance`)
2. sequence (`order-of-operations`)
3. risk (`regression-prevention`)
4. test design (`effective-testing-methods`)
5. execution (`scripted-command-execution`)

## Intended Outcome
This skillpack is intended to produce:
1. consistent decisions on process strictness and gates
2. fewer regressions on non-trivial changes
3. auditable validation evidence for release readiness
4. tighter alignment between user intent and execution behavior
5. durable documentation and instruction-state continuity
6. faster task completion without reducing safety standards

## Public Release Readiness Criteria
Recommended checklist before publishing this skillpack externally:
1. all governance validators pass
2. governance validator unit tests pass
3. `SKILL-MAP.md` and `docs/skill-index.md` are synchronized
4. `AGENTS.md` and this README reflect current skill behavior
5. packaging includes explicit versioning and changelog
6. packaging includes a license file for external reuse clarity

## Maintenance Notes
When adding or changing skills:
1. update `SKILL-MAP.md` and `docs/skill-index.md` in the same change
2. update related skill cross-links
3. run governance validators and tests
4. update `user-instructions.md` with directive and fulfillment evidence
