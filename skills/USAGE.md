# Usage

I built this skillpack for people using ChatGPT, Claude, Gemini, Cursor, GitHub Copilot, or another assistant that can read repo instructions and follow them consistently.

The short version:

1. read [../START_HERE.md](../START_HERE.md)
2. choose an install profile
3. put the selected skill folders where the assistant can read them
4. copy the default policy from this repository into your project instructions
5. let the router select zero or more skills from the task's actual triggers
6. use a startup declaration only when you request one or the work is governed or audited
7. keep generated routing views and governance checks in sync when you change the pack

## What These Skills Are
Each skill is a folder with a `SKILL.md` file.

The assistant uses those files as task-specific operating instructions. A skill can define:

1. when it should be used
2. how it should be ordered with other skills
3. what files, checks, or evidence should be updated
4. what the assistant should avoid doing

This pack is intentionally more structured than a single prompt. It is meant to slow the assistant down on the parts where mistakes are expensive: requirements, sequencing, validation, documentation drift, policy changes, and release readiness.

Routing architecture version 2 includes a process budget, so simple work can still stay simple. The legacy `process-budget-controller` skill is deprecated and remains only as a compatibility wrapper.

## Quizme Clarification Mode
Use `quizme-mode` when you want the agent to clarify every material detail before substantive execution.

Toggle it on:

```text
--quizme
```

Toggle it off by writing `--quizme` again. The mode persists throughout the active conversation until toggled off.

Optional arguments:

```text
--quizme --mc
--quizme --one-at-a-time
--quizme --confirm
--quizme --record
```

Rules:
1. `--mc` prefers multiple-choice questions with free-form fallback
2. `--one-at-a-time` asks one adaptive question per round
3. `--confirm` requires approval of the final task contract
4. `--record` persists the approved contract when a suitable artifact exists and implies `--confirm`
5. arguments must appear directly after `--quizme`, may appear in any order, and can be combined
6. duplicate arguments are harmless
7. unsupported arguments are ignored and briefly reported
8. every option clears when quizme mode is toggled off
9. destructive, public, production, payment, authentication, or irreversible tasks require confirmation automatically
10. the agent should use the plan-mode interactive clarification console when available and concise conversational questions otherwise

Combined example:

```text
--quizme --mc --one-at-a-time --confirm
```

## Internal Language Mode
`internal-lang` is an optional explicit control for compact private scratch work. It is inactive until you turn it on, does not make the assistant expose hidden reasoning, and should not rewrite your requirements into compressed shorthand.

Controls:

```text
/internal-lang on
/internal-lang off
/internal-lang --response on
/internal-lang --response off
```

Rules:
1. private scratch compression starts only after `/internal-lang on`
2. compressed user-facing responses default off when the mode is first activated
3. normal clear language remains the default response style
4. high-risk or action-critical details should stay fully written out

## Recommended Setup
Use schema-v2 [skill-catalog.json](./skill-catalog.json) as the canonical routing source. Individual `SKILL.md` files define procedures for selected skills.

Typical setup:

1. copy the selected skill folders into your assistant's skills directory
2. keep `skill-catalog.json` and its generated routing views with the pack
3. copy the `AGENTS.md` policy into the project where you want these skills enforced
4. restart or refresh the assistant so it reloads the available skills

The skill folders are directories such as:

1. `skill-governance/`
2. `order-of-operations/`
3. `regression-prevention/`
4. `doc-maintenance/`
5. `token-reduction/`
6. `quizme-mode/`

Avoid copying one random `SKILL.md` by itself unless you already understand the dependency chain. Several skills deliberately reference the same routing docs and validation artifacts.

The generated routing views are `SKILL-MAP.md`, `docs/skill-index.md`, and `docs/skill-decision-tree.md`. Generate them from the catalog rather than editing them independently.

## How I Expect the Assistant To Use The Pack
The router starts at zero. Zero selected skills is valid when core policy already covers the task. For routine work, target a median of no more than two selected skills and a normal cap of five. Mandatory safety skills and gates are never budgeted away or capped.

Require a startup declaration only when the user explicitly requests it or the work is governed or audited. When required, include:

1. `Skills in use`
2. why each skill was selected
3. the execution order

Use the smallest skill set that covers the work. A practical shortcut:

1. answer-only request: usually zero skills
2. one deterministic local command: `scripted-command-execution` when orchestration guidance adds value
3. tiny isolated text edit: usually zero skills
4. documentation workflow or behavior change: `doc-maintenance`
5. release-sensitive change: the applicable governance and safety gates

Do not select `process-budget-controller` for new work. It is a deprecated compatibility wrapper for older integrations; routing architecture version 2 owns the budget directly.

Use [install-profiles.md](./docs/install-profiles.md) when adopting the pack in stages.

When a behavior or workflow change creates documentation drift, add:

1. `doc-maintenance`

For governed or release-affecting work, add when its catalog trigger applies:

1. `skill-governance`

When `--quizme` is active, add before substantive execution:

1. `quizme-mode`
2. `requirement-clarifier`

For non-trivial code changes, add:

1. `regression-prevention`
2. `effective-testing-methods` when tests need to be created or amended

For a repeatable deterministic command workflow, add:

1. `scripted-command-execution`

For browser or GUI automation, add:

1. `pseudo-agentic-automation`

## Basic Task Prompt
Use a direct instruction like this:

```md
Follow `AGENTS.md` and route through `skills/skill-catalog.json`. Select only skills whose triggers apply; zero is valid.
```

For release-sensitive work, I would use:

```md
Use the governed routing path and required safety gates. Validate the exact candidate commit before calling it ready to push.
```

## Governance Files
The canonical routing file is `skill-catalog.json` schema version 2. It generates:

1. `SKILL-MAP.md` for the high-level routing model
2. `docs/skill-index.md` for detailed cross-skill triggers
3. `docs/skill-decision-tree.md` for minimum viable selection

Do not edit those three views independently. Other supporting files are:

1. `docs/routing-architecture-v2.md` for the routing contract
2. `docs/cache-budgets.md` for bounded history and cached artifact limits
3. `docs/governance-walkthrough.md` for the governed release-readiness workflow
4. `docs/known-limitations.md` for explicit tradeoffs and residual limits
5. `docs/install-profiles.md` for staged adoption paths
6. `docs/conflict-resolution-matrix.md` for owner decisions across overlapping skills
7. `docs/validator-severity-levels.md` for blocking versus non-blocking validator guidance
8. `docs/validation-profiles.md` for quick, standard, and release check depth
9. `docs/maturity-model.md` for staged improvement levels
10. `docs/pruning-policy.md` for controlled growth and removal criteria
11. `docs/field-notes.md` for real-world usage evidence
12. `user-instructions.md` when durable directive tracking was explicitly enabled

For governed changes in this repository, keep these root-level artifacts current:

1. `.github/workflows/skills-governance-ci.yml`
2. `docs/governance/*.governance.json`
3. `docs/governance/*.governance.md`
4. `docs/project-index.md`

Lifecycle and quality review docs:

1. `docs/rubrics/skillpack-quality-rubric.md`
2. `docs/rubrics/release-readiness-rubric.md`
3. `docs/rubrics/documentation-quality-rubric.md`
4. `docs/adapters/agent.md`
5. `docs/adapters/generic-agent.md`
6. `docs/maturity-model.md`
7. `docs/field-notes.md`
8. `docs/pruning-policy.md`

## Validation Commands
Run these from the repository root before publishing normal skillpack changes:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
```

Run this when a governed change includes a governance artifact:

```sh
TASK_ID=YOUR_CURRENT_TASK_ID

python3 skills/skill-governance/scripts/validate_governance_artifact.py \
  --artifact "docs/governance/${TASK_ID}.governance.json" \
  --strict \
  --require-recommendation go
```

If you are in a constrained environment and a check cannot run, record the exact blocker instead of claiming a clean pass.

For a release-readiness claim, use a clean checkout of one exact candidate commit and generate its exact-head attestation:

```sh
TASK_ID=YOUR_CURRENT_TASK_ID
BASE_SHA=FULL_BASE_COMMIT_SHA
CANDIDATE_SHA=FULL_CANDIDATE_COMMIT_SHA
ATTESTATION_PATH="/tmp/${TASK_ID}.attestation.json"

test "$(git rev-parse HEAD)" = "$CANDIDATE_SHA"
test -z "$(git status --porcelain --untracked-files=all)"

python3 skills/skill-governance/scripts/enforce_governance_ci.py \
  --repo-root . \
  --skills-root skills \
  --base-sha "$BASE_SHA" \
  --head-sha "$CANDIDATE_SHA" \
  --strict \
  --require-recommendation go \
  --release-check \
  --attestation-out "$ATTESTATION_PATH"
```

Version, changelog, release notes, skill count, and test count must describe `CANDIDATE_SHA`. If an authorized local tag already exists, verify its exact equality:

```sh
TAG_NAME=INTENDED_RELEASE_TAG
test "$(git rev-parse "${TAG_NAME}^{commit}")" = "$CANDIDATE_SHA"
```

These checks do not create a release or verify remote tag state, branch protection, or required remote checks. Those are separate authorized administrative actions. See [release-provenance.md](./docs/release-provenance.md).

## How To Add A New Skill
When adding a skill, keep the change connected across the pack:

1. add `<skill-name>/SKILL.md`
2. update `README.md`
3. update schema-v2 `skill-catalog.json`
4. regenerate `SKILL-MAP.md`, `docs/skill-index.md`, and `docs/skill-decision-tree.md`
5. update governance validation snippets if the new skill becomes required policy
6. update `CHANGELOG.md`
7. update `user-instructions.md` only when durable directive tracking was explicitly enabled
8. run the validation commands

## Examples
Use these examples to avoid over-applying skills:

1. [simple-code-fix.md](./docs/examples/simple-code-fix.md)
2. [bug-investigation.md](./docs/examples/bug-investigation.md)
3. [release-readiness-change.md](./docs/examples/release-readiness-change.md)
4. [frontend-layout-task.md](./docs/examples/frontend-layout-task.md)
5. [documentation-only-update.md](./docs/examples/documentation-only-update.md)
6. [quizme-clarification.md](./docs/examples/quizme-clarification.md)

## Licensing And Attribution
This pack uses an attribution-required non-commercial license.

If you use, copy, modify, or redistribute it, keep the license intact and credit:

1. Matt
2. Agent Command Center
3. the original repository or copy source

Commercial use requires written permission.
