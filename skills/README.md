# Level-Up Codex Skillpack

I built Level-Up Codex Skillpack as a governance-first skillpack for Codex and AI coding agents.
It provides reusable agent skills for workflow automation, planning, regression prevention, testing, documentation sync, and policy enforcement.

If you are looking for a `codex skills`, `ai agent skillpack`, or `agent workflow governance` repository, this is the package I use for that workflow.

## Why This Skillpack
This pack is built to improve:
1. delivery consistency on multi-step engineering tasks
2. release safety through explicit risk and validation gates
3. traceability through synchronized docs and instruction tracking
4. execution speed without lowering quality standards

## Release Metadata
- Version: `1.0.0` ([VERSION](./VERSION))
- Usage guide: [USAGE.md](./USAGE.md)
- Changelog: [CHANGELOG.md](./CHANGELOG.md)
- License: [LICENSE](./LICENSE)
- Governance walkthrough: [docs/governance-walkthrough.md](./docs/governance-walkthrough.md)

## Included Skills
I currently include 25 interoperable skills:
1. `skill-governance`
2. `governance-enforcement`
3. `requirement-clarifier`
4. `diagnose-before-fix`
5. `semantic-policy-audit`
6. `interdependent-change-planning`
7. `thoughtful-approach`
8. `thoroughly-rate-review`
9. `user-instructions-tracker`
10. `history-indexing`
11. `conversation-retention-summary`
12. `ui-spatial-canvas`
13. `ui-design-skills`
14. `effective-testing-methods`
15. `scripted-command-execution`
16. `pseudo-agentic-automation`
17. `token-reduction`
18. `artifact-budget-enforcement`
19. `order-of-operations`
20. `regression-prevention`
21. `file-structure-optimization`
22. `doc-maintenance`
23. `file-maintenance`
24. `project-backup`
25. `restore-drill`

## Skill Architecture and Interconnectedness
I use layered ownership to reduce overlap and conflicts:

1. Policy selection:
   - `skill-governance`
2. Diagnosis and coupling:
   - `diagnose-before-fix`
   - `interdependent-change-planning`
3. Scope and sequencing:
   - `requirement-clarifier`
   - `order-of-operations`
4. Execution routing:
   - `scripted-command-execution`
   - `pseudo-agentic-automation`
5. Risk and validation:
   - `regression-prevention`
   - `effective-testing-methods`
6. Policy enforcement and audit:
   - `governance-enforcement`
   - `semantic-policy-audit`
7. Documentation continuity:
   - `doc-maintenance`
   - `file-maintenance`
   - `file-structure-optimization`
   - `user-instructions-tracker`
   - `history-indexing`
   - `conversation-retention-summary`
   - `artifact-budget-enforcement`
8. Product and UX quality:
   - `thoughtful-approach`
   - `ui-design-skills`
   - `ui-spatial-canvas`

Canonical routing references:
- [docs/skill-index.md](./docs/skill-index.md)
- [SKILL-MAP.md](./SKILL-MAP.md)

## Governance and Enforcement
This is a governance-first pack. For risky or release-affecting tasks, I expect governance to be mandatory.

Core controls:
1. startup declaration with selected skills, rationale, and execution order
2. policy validation and skill catalog synchronization checks
3. ordering sync validation between skill map and skill index
4. CI enforcement for governed changes
5. validator test coverage

Key tooling:
- `skill-governance/scripts/generate_governance_artifact.py`
- `skill-governance/scripts/validate_governance_artifact.py`
- `skill-governance/scripts/validate_skill_policy.py`
- `skill-governance/scripts/validate_skill_order_sync.py`
- `skill-governance/scripts/enforce_governance_ci.py`
- `../.github/workflows/skills-governance-ci.yml`
- `../docs/governance/*.governance.json`

## Prioritization Model
Default baseline:
1. `token-reduction`
2. `order-of-operations`
3. `doc-maintenance` (when behavior/workflow/policy changes)

Conflict resolution order:
1. `skill-governance`
2. `order-of-operations`
3. `regression-prevention`
4. `effective-testing-methods`
5. execution mode skill (`scripted-command-execution` or `pseudo-agentic-automation`)

## Intended Outcomes
Expected outcomes from this skillpack:
1. predictable process strictness for ambiguous or risky work
2. fewer regressions on non-trivial code changes
3. auditable evidence for release readiness
4. tighter alignment between user intent and implementation
5. durable documentation, instruction-state continuity, and bounded cached history

## Suggested GitHub Topics
Use these tags for better discoverability:
- `codex`
- `ai-agent`
- `agent-skills`
- `skillpack`
- `prompt-engineering`
- `workflow-automation`
- `governance`
- `policy-enforcement`
- `software-quality`
- `regression-prevention`
- `testing`
- `documentation`

## Maintenance Checklist
When updating the pack:
1. update `SKILL-MAP.md` and `docs/skill-index.md` in the same change
2. run governance validators and related tests
3. update docs and release metadata when behavior changes
4. update `user-instructions.md` for directive/fulfillment evidence
5. include or update a strict-validating governance artifact for governed changes
