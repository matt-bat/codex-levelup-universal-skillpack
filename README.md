# Agent Command Center

Agent Command Center is the workflow layer I use to make AI assistants more consistent, more careful, and easier to audit.

> Like this project? You can [support ongoing development on Ko-fi](https://ko-fi.com/matt0bat), helping me maintain existing tools and release more public projects.

At a high level, it gives the assistant a set of reusable operating habits: plan in the right order, keep scope under control, validate risky work, update docs when behavior changes, and leave behind enough evidence that future work can pick up cleanly.

If you are looking for `agent skills`, an `ai agent skillpack`, or an `agent workflow governance` setup, this repo is meant to be a practical starting point rather than a theoretical prompt collection.

## How it works

1. A host assistant reads `AGENTS.md` and the canonical skill catalog to classify the requested work.
2. The router selects the smallest applicable set of Markdown skills and orders any required checks.
3. Deterministic Python validators check catalog structure, generated views, governance evidence, and release constraints.
4. The host assistant performs authorized work and reports validation results; the pack itself does not execute a hosted service.

This repository contains no AI model, model inference backend, training pipeline, or embedded API service. It supplies instructions and deterministic validation tooling to an AI assistant provided by the user’s chosen host.

## Quick Implementation Guide

1. Put this repository in the assistant's workspace.
2. Load `AGENTS.md`, the schema-v2 catalog and router contract 2.1, and only the selected skill files.
3. Let the router select zero or more skills.
4. Request a startup declaration only when you want one explicitly or the work is governed or audited and needs a durable routing record.

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
3. use catalog schema version 2, router contract 2.1, and the generated views to select relevant skills
4. ask for a startup declaration only when you explicitly want one or governed/audited work needs a durable routing record
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
- Current architecture version 2 work remains **Unreleased**. Pushing its source commit to a branch does not create a tag, publish release notes, or change the released version.
- New governed changes use append-only schema-v3 artifacts with typed evidence and an exact catalog binding. Release artifacts additionally bind the full diff and exact release metadata.
- `main` is protected as verified on 2026-07-18. Changes should use a feature branch and pull request; see [release-provenance.md](./skills/docs/release-provenance.md) for the dated remote-control snapshot.
- [branch-protection-policy.json](./.github/branch-protection-policy.json) records the closed desired state for `main`; a read-only verifier compares live GitHub evidence with it and fails closed on drift or unsupported fields.
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

The canonical catalog and generated [skill index](./skills/docs/skill-index.md) contain the current skill inventory, lifecycle state, triggers, exclusions, ownership domains, and typed relations. `process-budget-controller` remains listed only as a deprecated compatibility name.

## How The Pack Is Organized

Skills own decision domains instead of broad topics. The generated [skill map](./skills/SKILL-MAP.md) is the compact ownership view, while the [skill index](./skills/docs/skill-index.md) contains the complete routing detail. Linking these generated views avoids a second manual inventory that can drift from the catalog.

## Key Routing Docs

These are the docs I use when I need to understand or maintain the pack:

- [skill-catalog.json](./skills/skill-catalog.json): canonical schema-v2 routing source implementing router contract 2.1
- [SKILL-MAP.md](./skills/SKILL-MAP.md): generated routing and ownership overview
- [skill-index.md](./skills/docs/skill-index.md): generated trigger index
- [skill-decision-tree.md](./skills/docs/skill-decision-tree.md): generated minimum-selection view
- [install-profiles.md](./skills/docs/install-profiles.md): minimal, developer, governed, frontend, and full adoption paths
- [conflict-resolution-matrix.md](./skills/docs/conflict-resolution-matrix.md): who owns a decision when skills overlap
- [validation-profiles.md](./skills/docs/validation-profiles.md): quick, standard, and release validation depth
- [maturity-model.md](./skills/docs/maturity-model.md): how to grow into the pack over time
- [pruning-policy.md](./skills/docs/pruning-policy.md): how to avoid uncontrolled growth
- [field-notes.md](./skills/docs/field-notes.md): where real usage evidence should be recorded

Do not edit the three generated routing views independently. Catalog generation produces `skills/SKILL-MAP.md`, `skills/docs/skill-index.md`, and `skills/docs/skill-decision-tree.md`; validation should fail if they drift from the schema-v2 catalog.

## Router Contract 2.1

Router contract 2.1 keeps the architecture-version-2 restraint model and adds typed explicit-skill requests, verified artifact evidence, and separate `configure_remote` authority. Version 2.0 descriptors and frozen results remain readable for compatibility; new routing results use 2.1.

1. selecting zero skills is valid for routine work already covered by core policy
2. routine tasks target a median of at most two skills and normally no more than five
3. mandatory safety skills and gates are never capped by that routine budget
4. startup declarations are required only when explicitly requested or when governed/audited work needs a durable routing record
5. skill activation never grants file-write, external-action, release, or deployment authority
6. artifact creation permission is separate from evidence that an artifact exists and matches its recorded digest
7. `process-budget-controller` remains only as a deprecated compatibility wrapper; the router owns process restraint

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

1. the assistant declares selected skills, rationale, and execution order only when explicitly requested or when governed/audited work needs a durable routing record
2. new schema-v3 governance artifacts record authorized operations, risk inputs, typed gate evidence, exact catalog state, and change bindings
3. committed governance evidence is append-only; historical v1 and v2 artifacts remain readable but do not authorize a new governed change
4. release-purpose v3 artifacts require publication authority, exact release metadata, and a full-diff binding
5. the pull-request governance job always runs; it requires a v3 plan only when the diff contains governed paths
6. the remote desired-state verifier observes current protection but never grants `configure_remote` authority
7. catalog validation requires every `authorized_only` skill to define an explicit `Authority and Artifact Policy` section
8. the router keeps routine selections within the normal budget while mandatory safety remains uncapped

Key tooling:

- `skills/skill-governance/scripts/generate_governance_artifact.py`
- `skills/skill-governance/scripts/validate_governance_artifact.py`
- `skills/skill-governance/scripts/validate_skill_policy.py`
- `skills/skill-governance/scripts/validate_skill_order_sync.py`
- `skills/skill-governance/scripts/enforce_governance_ci.py`
- `skills/skill-governance/scripts/verify_remote_configuration.py`
- `.github/workflows/skills-governance-ci.yml`
- `.github/branch-protection-policy.json`
- `docs/governance/*.governance.json`

## Practical Default

For normal use, start with core policy and add a skill only when it changes execution, evidence, or safety. Zero selected skills is a valid route.

Use this shortcut:

1. answer or routine local action: zero skills is often enough
2. concise/context-heavy request: add `token-reduction`
3. real multi-step dependency problem: add `order-of-operations`
4. repeatable command orchestration: add `scripted-command-execution`
5. implementation or risky code change: add the applicable implementation and regression owners
6. governed or release-affecting work: use the governance path and uncapped mandatory safety gates

For routine work, target a median of at most two selected skills and normally no more than five. Compatibility wrappers do not count as active selections.

Optional internal language control:

1. `/internal-lang on` enables compact private scratch notation
2. `/internal-lang off` disables it
3. `/internal-lang --response on` allows compact notation in user-facing responses
4. `/internal-lang --response off` keeps responses in normal language

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

1. update the schema-v2 catalog when skill membership, triggers, typed relations, ownership, artifacts, or router contract behavior changes
2. regenerate `SKILL-MAP.md`, `docs/skill-index.md`, and `docs/skill-decision-tree.md` from the catalog; do not hand-edit generated views
3. update README, usage docs, and examples when public behavior changes
4. update an instruction ledger only when durable tracking is explicitly in scope
5. add a new append-only schema-v3 governance artifact for governed changes; never rewrite a committed governance record
6. run the validators and tests listed in [validation-profiles.md](./skills/docs/validation-profiles.md)
