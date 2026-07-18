# Agent Command Center

This directory is the actual skillpack. The root README explains the project from the outside; this README is for people who are installing, editing, or reviewing the skills themselves.

The pack gives AI assistants and similar coding agents a reusable operating system for software work: pick the right process, keep the work local by default, validate what changed, and leave enough evidence that another pass can understand what happened.

## Start Here

If you are new to the pack, use these in order:

1. [../START_HERE.md](../START_HERE.md) for the fastest orientation
2. [USAGE.md](./USAGE.md) for setup and day-to-day use
3. [docs/install-profiles.md](./docs/install-profiles.md) to choose how much process to install
4. [docs/routing-architecture-v2.md](./docs/routing-architecture-v2.md) for the canonical routing contract
5. [docs/skill-decision-tree.md](./docs/skill-decision-tree.md) to pick skills without overloading a task
6. [docs/known-limitations.md](./docs/known-limitations.md) for the tradeoffs

## What A Skill Is

Each skill is a folder with a `SKILL.md` file. That file tells the agent:

1. when the skill should apply
2. what order it should run in with nearby skills
3. what evidence, files, or validation it expects
4. what the agent should avoid doing

Some skills are lightweight routing helpers. Others are stricter governance or validation workflows. They are meant to work together, but they should not all run on every task.

## Included Skills

Use the generated [skill index](./docs/skill-index.md) for the current inventory, lifecycle state, triggers, exclusions, decision domains, and typed relations. `process-budget-controller` remains only as a deprecated compatibility name.

## How The Pack Is Organized

The main routing source is [skill-catalog.json](./skill-catalog.json). Catalog schema version 2 is canonical, implements router contract 2.1, and generates three operator views:

1. [SKILL-MAP.md](./SKILL-MAP.md) for the high-level ownership model
2. [docs/skill-index.md](./docs/skill-index.md) for detailed triggers and cross-skill relationships
3. [docs/skill-decision-tree.md](./docs/skill-decision-tree.md) for minimum viable selection

Do not edit those views independently. Use [docs/conflict-resolution-matrix.md](./docs/conflict-resolution-matrix.md) for overlap decisions and [docs/validation-profiles.md](./docs/validation-profiles.md) for check depth.

## How To Use It Day To Day

For most tasks, route from zero and add only skills with active triggers:

1. zero selected skills is valid when core policy covers the task
2. use `token-reduction` when a real context or output budget applies
3. use `order-of-operations` when dependencies or sequencing risk matter
4. add `scripted-command-execution` for repeatable local command workflows
5. add governance only when risk, ambiguity, audit, or release impact justifies it

Routine selection targets a median of no more than two skills and a normal cap of five. Mandatory safety skills and gates are never capped. Startup declarations are required only when explicitly requested or when governed or audited work needs a durable routing record.

`process-budget-controller` remains only as a deprecated compatibility wrapper; the router owns process budgeting.

The decision tree and install profiles exist because too much process can be just as harmful as too little process.

Use `--quizme` when you want exhaustive clarification before execution. The mode persists for the active conversation until toggled off. Optional immediate arguments are `--mc`, `--one-at-a-time`, `--confirm`, and `--record`.

## Validation

For a normal skillpack documentation or policy update, run:

```sh
python3 -m pip install --disable-pip-version-check -r skills/skill-governance/requirements.txt
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
```

For new governed changes, validate the append-only schema-v3 artifact and its exact generated Markdown pair, then run the CI enforcement script. Release-purpose v3 artifacts additionally require explicit publication authority, exact release metadata, and a full-diff binding. The exact commands are in [docs/governance-walkthrough.md](./docs/governance-walkthrough.md).

The policy validator also checks the closed desired-state contract at [../.github/branch-protection-policy.json](../.github/branch-protection-policy.json). To compare it with current GitHub state, use the read-only workflow in [docs/release-provenance.md](./docs/release-provenance.md); verification does not authorize `configure_remote`.

## Maintenance Expectations

When adding or changing a skill:

1. update the skill folder
2. update schema-v2 `skill-catalog.json` and router contract metadata when the interface changes
3. keep an explicit `Authority and Artifact Policy` section in every skill whose catalog artifact durability is `authorized_only`
4. regenerate `SKILL-MAP.md`, `docs/skill-index.md`, and `docs/skill-decision-tree.md`
5. update examples or install profiles when routing changed
6. update `CHANGELOG.md`
7. update `user-instructions.md` only when durable directive tracking was explicitly enabled
8. run the relevant validation profile

Keep the pack useful, not just larger. If a new idea is only a checklist, example, or rubric, it may not need to become a new skill.

Public documentation changes do not perform a release. Before the next release, bind version, notes, changelog, validations, and governance evidence to one exact candidate commit through a purpose=`release` v3 artifact. `main` is protected as verified on 2026-07-18; use a feature branch and pull request, and see [docs/release-provenance.md](./docs/release-provenance.md) for the dated remote snapshot.
