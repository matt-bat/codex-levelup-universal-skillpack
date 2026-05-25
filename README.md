# Level-Up Codex Skillpack

I built Level-Up Codex Skillpack as a governance-first skillpack for Codex and AI coding agents.
It provides reusable agent skills for workflow automation, planning, regression prevention, testing, documentation sync, and policy enforcement.

If you are looking for `codex skills`, an `ai agent skillpack`, or `agent workflow governance`, this is the package for you!

I have noticed a significant increase in UI quality, reliability, and instruction-following accuracy. There have also been fewer regressions, faster actions, and consistently better outputs from Codex in my usage so far. 

## Why This Skillpack
This pack is built to improve:
1. delivery consistency on multi-step engineering tasks
2. release safety through explicit risk and validation gates
3. traceability through synchronized docs and instruction tracking
4. execution speed without lowering quality standards

## Release Metadata
- Version: `1.0.0` ([VERSION](./skills/VERSION))
- Start here: [START_HERE.md](./START_HERE.md)
- Usage guide: [USAGE.md](./skills/USAGE.md)
- Changelog: [CHANGELOG.md](./skills/CHANGELOG.md)
- License: [LICENSE](./skills/LICENSE)
- Governance walkthrough: [governance-walkthrough.md](./skills/docs/governance-walkthrough.md)
- Decision tree: [skill-decision-tree.md](./skills/docs/skill-decision-tree.md)
- Known limitations: [known-limitations.md](./skills/docs/known-limitations.md)
- Contributing guide: [CONTRIBUTING.md](./CONTRIBUTING.md)
- Security policy: [SECURITY.md](./SECURITY.md)

## Included Skills
I currently include 28 interoperable skills:
1. `skill-governance`
2. `process-budget-controller`
3. `governance-enforcement`
4. `requirement-clarifier`
5. `diagnose-before-fix`
6. `semantic-policy-audit`
7. `interdependent-change-planning`
8. `thoughtful-approach`
9. `thoroughly-rate-review`
10. `user-instructions-tracker`
11. `history-indexing`
12. `conversation-retention-summary`
13. `ui-spatial-canvas`
14. `ui-design-skills`
15. `effective-testing-methods`
16. `scripted-command-execution`
17. `pseudo-agentic-automation`
18. `token-reduction`
19. `artifact-budget-enforcement`
20. `order-of-operations`
21. `regression-prevention`
22. `file-structure-optimization`
23. `doc-maintenance`
24. `file-maintenance`
25. `skill-usage-review`
26. `deprecation-management`
27. `project-backup`
28. `restore-drill`

## Skill Architecture and Interconnectedness
I use layered ownership to reduce overlap and conflicts:

1. Policy selection:
   - `skill-governance`
2. Process restraint:
   - `process-budget-controller`
3. Diagnosis and coupling:
   - `diagnose-before-fix`
   - `interdependent-change-planning`
4. Scope and sequencing:
   - `requirement-clarifier`
   - `order-of-operations`
5. Execution routing:
   - `scripted-command-execution`
   - `pseudo-agentic-automation`
6. Risk and validation:
   - `regression-prevention`
   - `effective-testing-methods`
7. Policy enforcement and audit:
   - `governance-enforcement`
   - `semantic-policy-audit`
8. Documentation continuity:
   - `doc-maintenance`
   - `file-maintenance`
   - `file-structure-optimization`
   - `user-instructions-tracker`
   - `history-indexing`
   - `conversation-retention-summary`
   - `artifact-budget-enforcement`
9. Lifecycle management:
   - `skill-usage-review`
   - `deprecation-management`
10. Product and UX quality:
   - `thoughtful-approach`
   - `ui-design-skills`
   - `ui-spatial-canvas`

Canonical routing references:
- [docs/skill-index.md](./skills/docs/skill-index.md)
- [SKILL-MAP.md](./skills/SKILL-MAP.md)
- [skill-catalog.json](./skills/skill-catalog.json)
- [skill-decision-tree.md](./skills/docs/skill-decision-tree.md)
- [install-profiles.md](./skills/docs/install-profiles.md)
- [conflict-resolution-matrix.md](./skills/docs/conflict-resolution-matrix.md)
- [validation-profiles.md](./skills/docs/validation-profiles.md)
- [maturity-model.md](./skills/docs/maturity-model.md)
- [pruning-policy.md](./skills/docs/pruning-policy.md)
- [field-notes.md](./skills/docs/field-notes.md)

## Who This Is For
This pack is best for people who want:
1. explicit agent operating rules
2. repeatable validation and release-readiness gates
3. stronger documentation and instruction tracking
4. less ambiguity on multi-step engineering tasks

It is probably too heavy if you only want lightweight one-off prompt snippets.

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
- `.github/workflows/skills-governance-ci.yml`
- `docs/governance/*.governance.json`

## Prioritization Model
Default baseline:
1. `token-reduction`
2. `order-of-operations`
3. `doc-maintenance` (when behavior/workflow/policy changes)

Minimum viable use:
1. answer-only request: `token-reduction`
2. one deterministic local command: `token-reduction`, `scripted-command-execution`
3. small isolated edit: `token-reduction`, `order-of-operations`, optional validation skill
4. governed or release-affecting change: full governance path

Conflict resolution order:
1. `skill-governance`
2. `order-of-operations`
3. `regression-prevention`
4. `effective-testing-methods`
5. execution mode skill (`scripted-command-execution` or `pseudo-agentic-automation`)

## Intended Outcomes
Expected outcomes from this skillpack:
1. predictable process strictness for ambiguous or risky work
2. fewer regressions on non-trivial changes
3. auditable evidence for release readiness
4. tighter alignment between user intent and execution behavior
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
2. update `skill-catalog.json` when skill membership, triggers, dependencies, or artifacts change
3. run governance validators and related tests
4. update docs and release metadata when behavior changes
5. update `user-instructions.md` for directive/fulfillment evidence
6. include or update a strict-validating governance artifact for governed changes
