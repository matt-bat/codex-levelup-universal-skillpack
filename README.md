# Agent Command Center

Agent Command Center is the workflow layer I use to make AI assistants more consistent, more careful, and easier to audit.

At a high level, it gives the assistant a set of reusable operating habits: plan in the right order, keep scope under control, validate risky work, update docs when behavior changes, and leave behind enough evidence that future work can pick up cleanly.

If you are looking for `agent skills`, an `ai agent skillpack`, or an `agent workflow governance` setup, this repo is meant to be a practical starting point rather than a theoretical prompt collection.

## Quick Implementation Guide
1. Put this repository in the assistant's workspace.
2. Load `AGENTS.md` and the relevant skill files for the task.
3. Ask the assistant to declare the active skills and execution order before it edits anything.

## Detailed Overview
This repository is the workflow layer that makes AI assistants more consistent, more careful, and easier to audit.

At a high level, it gives the assistant a set of reusable operating habits: plan in the right order, keep scope under control, validate risky work, update docs when behavior changes, and leave behind enough evidence that future work can pick up cleanly.

## Start Here
If you are new to the pack, start with [START_HERE.md](./START_HERE.md). It gives you the shortest path based on what you want to do:

1. try the pack quickly
2. use minimal process
3. run governed release-readiness checks
4. add or change a skill
5. reduce over-process
6. improve the pack over time

## Using With Common AIs
This repository is designed to work with ChatGPT, Claude, Gemini, Cursor, GitHub Copilot, and other assistants that can read markdown instructions.

Use [Common AI Instructions](./skills/docs/adapters/common-ai.md) as the shared setup guide. The short version:

1. keep the repository in the assistant's workspace
2. load the root `AGENTS.md`
3. load the relevant skill files for the task
4. ask the assistant to declare active skills and execution order at task start
5. use the assistant's project instructions or custom prompt area for the repo policy summary
6. when a task needs exhaustive clarification, use `--quizme` or the assistant's equivalent clarification flow if it has one

## Why I Built This
I built this because agent workflows can get messy fast. Without explicit operating rules, the model can over-plan small tasks, under-validate risky tasks, forget user instructions, or leave documentation behind.

This pack is designed to improve:
1. delivery consistency on multi-step engineering tasks
2. release safety through explicit risk and validation gates
3. traceability through synchronized docs and instruction tracking
4. execution speed without lowering quality standards
5. restraint, so small tasks stay small

## Release Metadata
- Version: `1.0.0` ([VERSION](./skills/VERSION))
- Start here: [START_HERE.md](./START_HERE.md)
- Usage guide: [USAGE.md](./skills/USAGE.md)
- Changelog: [CHANGELOG.md](./skills/CHANGELOG.md)
- License: [LICENSE](./skills/LICENSE)
- Governance walkthrough: [governance-walkthrough.md](./skills/docs/governance-walkthrough.md)
- Decision tree: [skill-decision-tree.md](./skills/docs/skill-decision-tree.md)
- Install profiles: [install-profiles.md](./skills/docs/install-profiles.md)
- Known limitations: [known-limitations.md](./skills/docs/known-limitations.md)
- Contributing guide: [CONTRIBUTING.md](./CONTRIBUTING.md)
- Security policy: [SECURITY.md](./SECURITY.md)

## Included Skills
The pack currently includes 29 interoperable skills:

1. `skill-governance`
2. `process-budget-controller`
3. `governance-enforcement`
4. `requirement-clarifier`
5. `quizme-mode`
6. `diagnose-before-fix`
7. `semantic-policy-audit`
8. `interdependent-change-planning`
9. `thoughtful-approach`
10. `thoroughly-rate-review`
11. `user-instructions-tracker`
12. `history-indexing`
13. `conversation-retention-summary`
14. `ui-spatial-canvas`
15. `ui-design-skills`
16. `effective-testing-methods`
17. `scripted-command-execution`
18. `pseudo-agentic-automation`
19. `token-reduction`
20. `artifact-budget-enforcement`
21. `order-of-operations`
22. `regression-prevention`
23. `file-structure-optimization`
24. `doc-maintenance`
25. `file-maintenance`
26. `skill-usage-review`
27. `deprecation-management`
28. `project-backup`
29. `restore-drill`

## How The Pack Is Organized
The skills are grouped by the kind of decision they own. This matters because the pack is intentionally broad, and broad systems need clear ownership.

1. Policy and release posture:
   - `skill-governance`
   - `governance-enforcement`
   - `semantic-policy-audit`
2. Process restraint:
   - `process-budget-controller`
   - `token-reduction`
3. Diagnosis, planning, and sequencing:
   - `quizme-mode`
   - `requirement-clarifier`
   - `diagnose-before-fix`
   - `interdependent-change-planning`
   - `order-of-operations`
4. Execution and validation:
   - `scripted-command-execution`
   - `pseudo-agentic-automation`
   - `regression-prevention`
   - `effective-testing-methods`
5. Documentation and continuity:
   - `doc-maintenance`
   - `file-maintenance`
   - `file-structure-optimization`
   - `user-instructions-tracker`
   - `history-indexing`
   - `conversation-retention-summary`
   - `artifact-budget-enforcement`
6. Lifecycle management:
   - `skill-usage-review`
   - `deprecation-management`
7. Product and UX quality:
   - `thoughtful-approach`
   - `ui-design-skills`
   - `ui-spatial-canvas`

## Key Routing Docs
These are the docs I use when I need to understand or maintain the pack:

- [SKILL-MAP.md](./skills/SKILL-MAP.md): quick routing and ownership overview
- [skill-index.md](./skills/docs/skill-index.md): canonical trigger index
- [skill-catalog.json](./skills/skill-catalog.json): machine-readable skill inventory
- [skill-decision-tree.md](./skills/docs/skill-decision-tree.md): how to choose the smallest useful skill set
- [install-profiles.md](./skills/docs/install-profiles.md): minimal, developer, governed, frontend, and full adoption paths
- [conflict-resolution-matrix.md](./skills/docs/conflict-resolution-matrix.md): who owns a decision when skills overlap
- [validation-profiles.md](./skills/docs/validation-profiles.md): quick, standard, and release validation depth
- [maturity-model.md](./skills/docs/maturity-model.md): how to grow into the pack over time
- [pruning-policy.md](./skills/docs/pruning-policy.md): how to avoid uncontrolled growth
- [field-notes.md](./skills/docs/field-notes.md): where real usage evidence should be recorded

## Who This Is For
This pack is best for people who want:

1. explicit agent operating rules
2. repeatable validation and release-readiness gates
3. stronger documentation and instruction tracking
4. less ambiguity on multi-step engineering tasks
5. a way to keep process useful without letting it sprawl

It is probably too much if you only want a few lightweight prompt snippets. In that case, start with the `Minimal` profile in [install-profiles.md](./skills/docs/install-profiles.md).

## Governance And Enforcement
The pack is governance-first, but not governance-only. The goal is to use serious process only when the task actually needs it.

Core controls:
1. the assistant declares selected skills, rationale, and execution order at task start
2. governance artifacts record mode, risk, gates, and recommendation
3. validators check policy, skill order, catalog sync, and governance artifacts
4. CI can enforce governed-change rules before merge or release
5. process-budget rules keep small tasks from becoming paperwork

Key tooling:
- `skills/skill-governance/scripts/generate_governance_artifact.py`
- `skills/skill-governance/scripts/validate_governance_artifact.py`
- `skills/skill-governance/scripts/validate_skill_policy.py`
- `skills/skill-governance/scripts/validate_skill_order_sync.py`
- `skills/skill-governance/scripts/enforce_governance_ci.py`
- `.github/workflows/skills-governance-ci.yml`
- `docs/governance/*.governance.json`

## Practical Default
For normal use, do not start with every skill.

Use this shortcut:
1. answer-only request: `token-reduction`
2. one deterministic command: `token-reduction`, `scripted-command-execution`
3. small local edit: `token-reduction`, `order-of-operations`, targeted validation
4. normal code change: add `regression-prevention`
5. governed or release-affecting work: use the governance path

Optional clarification control:
1. write `--quizme` to toggle persistent conversation-local exhaustive clarification on or off
2. write `--quizme --mc` to prefer interactive multiple-choice questions
3. write `--quizme --one-at-a-time` for one adaptive question per round
4. write `--quizme --confirm` to approve the final task contract before execution
5. write `--quizme --record` to persist the approved contract when a suitable artifact exists; this implies confirmation
6. combine supported arguments in any order directly after `--quizme`

## Intended Outcomes
The expected result is not “more process.” The expected result is better judgment about when process is worth it.

The pack should help produce:
1. clearer task starts
2. fewer regressions on non-trivial changes
3. better release-readiness evidence
4. fewer forgotten docs or user directives
5. more controlled growth as the workflow matures

## Suggested GitHub Topics
Use these tags for discoverability:

- `agent-command-center`
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

1. update `SKILL-MAP.md` and `docs/skill-index.md` together
2. update `skill-catalog.json` when skill membership, triggers, dependencies, or artifacts change
3. update README, usage docs, and examples when public behavior changes
4. update `skills/user-instructions.md` for directive evidence
5. include or update a governance artifact for governed changes
6. run the validators and tests listed in [validation-profiles.md](./skills/docs/validation-profiles.md)
