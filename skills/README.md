# Agent Command Center

This directory is the actual skillpack. The root README explains the project from the outside; this README is for people who are installing, editing, or reviewing the skills themselves.

The pack gives AI assistants and similar coding agents a reusable operating system for software work: pick the right process, keep the work local by default, validate what changed, and leave enough evidence that another pass can understand what happened.

## Start Here
If you are new to the pack, use these in order:

1. [../START_HERE.md](../START_HERE.md) for the fastest orientation
2. [USAGE.md](./USAGE.md) for setup and day-to-day use
3. [docs/install-profiles.md](./docs/install-profiles.md) to choose how much process to install
4. [docs/skill-decision-tree.md](./docs/skill-decision-tree.md) to pick skills without overloading a task
5. [docs/known-limitations.md](./docs/known-limitations.md) for the tradeoffs

## What A Skill Is
Each skill is a folder with a `SKILL.md` file. That file tells the agent:

1. when the skill should apply
2. what order it should run in with nearby skills
3. what evidence, files, or validation it expects
4. what the agent should avoid doing

Some skills are lightweight routing helpers. Others are stricter governance or validation workflows. They are meant to work together, but they should not all run on every task.

## Included Skills
This pack currently includes 29 skills:

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
The main routing docs are:

1. [SKILL-MAP.md](./SKILL-MAP.md) for the high-level ownership model
2. [docs/skill-index.md](./docs/skill-index.md) for detailed triggers and cross-skill relationships
3. [skill-catalog.json](./skill-catalog.json) for machine-readable inventory data
4. [docs/conflict-resolution-matrix.md](./docs/conflict-resolution-matrix.md) for overlap decisions
5. [docs/validation-profiles.md](./docs/validation-profiles.md) for choosing the right check depth

When a skill changes, these files usually need to stay in sync. If they drift, the pack becomes harder for an agent to use reliably.

## How To Use It Day To Day
For most tasks, start small:

1. use `token-reduction` to keep output focused
2. use `order-of-operations` when the task has more than one meaningful step
3. add `scripted-command-execution` when local commands are part of the work
4. add `doc-maintenance` when behavior, workflow, or policy docs change
5. add governance only when risk, ambiguity, or release impact justifies it

The decision tree and install profiles exist because too much process can be just as harmful as too little process.

Use `--quizme` when you want exhaustive clarification before execution. The mode persists for the active conversation until toggled off. Optional immediate arguments are `--mc`, `--one-at-a-time`, `--confirm`, and `--record`.

## Validation
For a normal skillpack documentation or policy update, run:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
```

For governed changes, also validate the generated governance artifact and run the CI enforcement script. The exact commands are in [docs/governance-walkthrough.md](./docs/governance-walkthrough.md).

## Maintenance Expectations
When adding or changing a skill:

1. update the skill folder
2. update `SKILL-MAP.md`
3. update `docs/skill-index.md`
4. update `skill-catalog.json`
5. update examples or install profiles when routing changed
6. update `CHANGELOG.md`
7. update `user-instructions.md` when a user directive or fulfillment state changed
8. run the relevant validation profile

Keep the pack useful, not just larger. If a new idea is only a checklist, example, or rubric, it may not need to become a new skill.
