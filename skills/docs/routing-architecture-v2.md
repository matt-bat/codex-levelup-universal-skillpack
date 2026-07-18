# Routing Architecture Version 2

This document describes the enforceable routing model. `skills/skill-catalog.json` is the machine-readable source of truth; generated routing views must not be edited independently.

## Layers

1. **Core policy**: instruction precedence, authorization, read-only behavior, local-first execution, preservation of user work, proportional validation, and concise handoff.
2. **Task descriptor**: deliverables, action, execution mode, command effect, test intent, mutation/recovery risk, effects, surfaces, domains, authority, constraints, inferred requirements, uncertainties, evidence, and checkpoint.
3. **Task router**: evaluates catalog clauses, resolves hard prerequisites and ordering, then selects decision-domain owners.
4. **Safety kernel**: independently enforces read-only, authority, external-state, destructive-action, and release invariants.
5. **Response compositor**: combines outputs without suppressing required evidence, uncertainty, or vetoes.

## Classification Principles

1. Route by requested action and planned effect, not topic keywords.
2. Separate source design from live execution.
3. Separate qualitative review from scoring.
4. Separate generic interface work from an explicit design system.
5. Reclassify after inspection, after planning, after the final diff, and before external or irreversible action.
6. Unknown or conflicting critical state fails closed.

## Normalized Descriptor Boundaries

The resolver consumes typed JSON validated by `skills/skill-governance/schemas/task-descriptor.schema.json`. It intentionally does not parse free-form prompts.

Important distinctions are explicit fields rather than inferred keywords:

1. `execution_mode`: `none`, `incidental_validation`, `deterministic_workflow`, or `adaptive_browser`
2. `command_effect`: `not_applicable`, `read_only`, `workspace`, `repository`, `external`, or `unknown`
3. `test_intent`: `none`, `run_existing`, or `design_or_change`
4. product, interface-quality, governance-tooling, release-enforcement, documentation-sync, and sequencing decisions are independent booleans
5. `data_loss_risk`: `none`, `credible`, or `unknown`
6. `recovery_requirement`: `not_required`, `required`, or `unknown`

Unknown command or recovery effects fail closed. Running existing tests never selects the test-design owner. Incidental read-only validation does not select an execution workflow. Deployment requires rollback evidence but does not imply backup or restore controls unless typed risk requires them.

## Catalog Routing Modes

| Mode | Runtime behavior |
|---|---|
| `automatic` | A matching trigger may select the active skill. |
| `safety_only` | A matching trigger selects a mandatory safety owner outside the optional budget. |
| `explicit_only` | The router never selects it from task clauses; an explicit mode or hard prerequisite must activate it. |
| `nonselectable` | Deprecated, removed, or compatibility-only entry; never emitted as an active route. |

Each automatic or safety entry defines one or more machine trigger clauses. Any trigger clause may match; any matching exclusion clause suppresses that route. Fields within one clause all have to match. `_any`, `_all`, and `_none` operators have their ordinary set meanings.

Human-readable `triggers` and `exclusions` explain policy but do not execute it. The nested `routing` object is executable. The catalog validator rejects missing routing modes, unknown vocabulary, duplicate clauses, incomplete selection order, non-required safety routes, and lifecycle inconsistencies.

## Typed Relations

| Relation | Meaning |
|---|---|
| `requires` | Hard prerequisite; recursively activates its target and the graph must be acyclic. |
| `gates` | May block a named phase without selecting another skill. |
| `runs_after` | Ordering only when both participants are selected. |
| `supports` | Advisory evidence; never activates a skill. |
| `conflicts_with` | Symmetric incompatibility; simultaneous selection produces a blocking veto. |
| `consumes` | Reads an artifact or decision produced elsewhere. |
| `superseded_by` | Lifecycle replacement, not an execution edge. |

## Decision Ownership

Use one owner per decision domain, not one owner for the entire task. Safety, task meaning, product behavior, implementation, test design, execution, governance, and response composition remain separate.

Supporters may contribute `must_surface` evidence. Safety and enforcement owners may veto `go`, `verified`, `complete`, or `release-ready`. The response compositor may shorten prose but cannot alter these records.

## Skill Budget

Zero selected skills is valid for routine work covered by core policy. Routine tasks should have a median of at most two selected skills and normally no more than five. Mandatory safety gates are never budgeted.

Compatibility wrappers and aliases do not count as active selections.

`supports` never activates another skill. `runs_after` changes output order only when both skills were independently selected. The runtime topologically enforces both `requires` and `runs_after` edges and fails closed on a selected ordering cycle.

## Artifact Policy

Skill activation never grants write authority. A task descriptor must separately authorize local files, commands, dependency installation, commit, push, migration, messages, deployment, or publication.

Read-only means zero writes, including trackers, indexes, governance files, generated views, caches, commits, and external mutations.

Command permission is also effect-dependent. A workspace command requires file-write authority, a repository command requires commit authority, and an external command requires every matching external operation to remain authorized and unblocked. A denied evidence gate disables both the protected operation and an external command that could perform it.

## Typed Output

`resolve_task_route.py` emits:

1. selected canonical skill names and catalog decision-domain owners
2. instance-unique gates with a `policy_gate_id` from the catalog namespace
3. operation permissions that never exceed the descriptor's authority
4. artifact types from the catalog namespace, only when file writes are separately authorized
5. surfaced constraints, non-goals, inferred material requirements, uncertainties, and safety vetoes
6. a bounded route trace containing typed operational evidence rather than hidden reasoning

The output is validated by `routing-result.schema.json` and then cross-checked against the loaded catalog. A caller can use a candidate catalog path for adversarial or migration testing; triggers, exclusions, prerequisites, ordering, conflicts, and lifecycle status all affect the actual route.

## Executable Checks

From the repository root:

```sh
python3 skills/skill-governance/scripts/generate_routing_views.py --repo-root . --check
python3 skills/skill-governance/scripts/resolve_task_route.py \
  --fixtures skills/skill-governance/fixtures/routing-scenarios.json \
  --pretty
python3 -m unittest discover \
  -s skills/skill-governance/tests \
  -p 'test_task_routing.py'
```

## Generated Views

The catalog generates:

1. `skills/SKILL-MAP.md`
2. `skills/docs/skill-index.md`
3. `skills/docs/skill-decision-tree.md`

Validation fails when a generated view differs from catalog output, when a frontmatter description diverges from its catalog description, when a hard graph cycles, or when a rule references an unknown owner.

## Observation and Migration

Run old compatibility names and version 2 routing together for at least 30 representative tasks or two releases. Record only operational metadata: scenario or task class, selected names, route changes, corrections, retries, validation outcome, and elapsed/tool counts when available.

Never record prompts, source content, secrets, credentials, hidden reasoning, or private user data.

Use the bounded recorder only after a real route checkpoint:

```sh
python3 skills/skill-governance/scripts/record_routing_observation.py record \
  --task-class implement \
  --checkpoint post_diff \
  --selected-skills "regression-prevention,effective-testing-methods" \
  --validation-outcome pass

python3 skills/skill-governance/scripts/record_routing_observation.py summary
```

The ignored `skills/.routing-observations.jsonl` file keeps at most 100 schema-checked records. Selected names must exist in the catalog, and the aggregate summary contains no task text.
