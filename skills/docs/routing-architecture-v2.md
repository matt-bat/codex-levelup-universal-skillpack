# Routing Architecture: Contract 2.1

`skills/skill-catalog.json` is the machine-readable source of truth. Treat this document and the generated routing views as explanatory surfaces; never edit a generated view independently.

## Layers

1. **Core policy**: enforce instruction precedence, authorization, read-only behavior, local-first execution, user-work preservation, and proportional validation.
2. **Task descriptor**: normalize deliverables, action, effects, risk, authority, constraints, explicit skill requests, evidence, and checkpoint.
3. **Task router**: evaluate executable catalog clauses, activate explicit skills, resolve hard prerequisites, enforce conflicts and order, and select decision-domain owners.
4. **Safety kernel**: independently enforce descriptor consistency, read-only, operation authority, external checkpoints, recovery, evidence, and release invariants.
5. **Response compositor**: surface required evidence, uncertainty, operation permissions, and vetoes without exposing hidden reasoning.

## Classification Principles

1. Route by requested action and planned effect, not topic keywords.
2. Separate source design from live execution.
3. Separate qualitative review from numeric scoring.
4. Separate generic interface work from an explicit design-system decision.
5. Reclassify after inspection, after planning, after the final diff, and before external or irreversible action.
6. Fail unknown or conflicting critical state closed.
7. Treat zero selected skills as valid.

## Descriptor Versions

Validate descriptors with `skills/skill-governance/schemas/task-descriptor.schema.json`. The resolver accepts frozen 2.0 descriptors for compatibility and normalizes omitted 2.1 fields in a deep copy; it never mutates caller input. The resolver emits contract 2.1 results.

Contract 2.1 adds:

1. `constraints.explicit_skills`: canonical names explicitly requested by the user or an active conversation mode.
2. `evidence.artifacts`: typed artifact records containing catalog kind, repository-relative path, SHA-256, and status.
3. `configure_remote`: a distinct operation and authority surface.

Do not infer explicit skills or artifact evidence from free-form text.

## Normalized Descriptor Boundaries

Represent important distinctions as typed fields:

1. `execution_mode`: `none`, `incidental_validation`, `deterministic_workflow`, or `adaptive_browser`.
2. `command_effect`: `not_applicable`, `read_only`, `workspace`, `repository`, `external`, or `unknown`.
3. `test_intent`: `none`, `run_existing`, or `design_or_change`.
4. Product, interface quality, governance tooling, release enforcement, documentation sync, and sequencing decisions as independent booleans.
5. `data_loss_risk`: `none`, `credible`, or `unknown`.
6. `recovery_requirement`: `not_required`, `required`, or `unknown`.
7. Each operation, effect, mutation level, target, and authority as an internally consistent set.

Reject unknown command or recovery effects at a mutation boundary. Running existing tests never selects the test-design owner. Incidental read-only validation does not select an execution workflow. Deployment requires rollback evidence but selects backup or restore controls only when typed risk independently requires them.

## Operation Authority

Require exact authority for every requested operation. A skill never grants authority.

Treat `configure_remote` as separate from `commit`, `push`, and `publish`. A valid remote-configuration descriptor identifies the `remote_repository` effect and target, uses external mutation and command effect where commands are requested, grants only the intended operation authorities, supplies rollback evidence by the terminal checkpoint, and reroutes at `pre_external_action`. Granting `configure_remote` never permits a push; granting push never permits remote configuration.

Apply command-effect coupling:

1. Workspace commands require file-write permission.
2. Repository commands require commit permission.
3. External commands require every requested external operation to remain permitted.

Select `scripted-command-execution` for deterministic shell or API workflows and `pseudo-agentic-automation` for adaptive browser or GUI interaction. Reject simultaneous selection because the execution owners conflict.

## Remote Desired-State Control

Use three machine-readable surfaces for GitHub branch protection:

1. `.github/branch-protection-policy.json`: desired repository, branch, and protection state.
2. `skills/skill-governance/schemas/remote-configuration-policy.schema.json`: closed Draft 2020-12 policy contract with no undeclared fields.
3. `skills/skill-governance/scripts/verify_remote_configuration.py`: read-only normalizer and exact-state comparator.

Fetch current branch protection and stream it to the verifier with the single canonical command in [Protected-Main Snapshot](./release-provenance.md#protected-main-snapshot).

Validate the response source URL against the policy repository and branch. Normalize only explicitly supported GitHub fields, require internally consistent status-check contexts and typed checks, and compare the complete normalized state. Fail closed on unknown API fields, malformed structures, target mismatch, or drift.

Classify this command as read-only external evidence collection. It requires repository read access but neither grants nor exercises `configure_remote`. Changing the desired-state file requires local write authority; changing GitHub settings requires separate `configure_remote` authority, critical gates, rollback evidence, and a `pre_external_action` reroute. Re-run verification after an authorized change because a prior pass is only point-in-time evidence.

## Catalog Routing Modes

| Mode | Runtime behavior |
|---|---|
| `automatic` | Select when a machine trigger matches and no exclusion matches. |
| `safety_only` | Select as a mandatory safety owner outside the optional budget. |
| `explicit_only` | Select only through `explicit_skills` or a hard prerequisite. |
| `nonselectable` | Never emit as an active route. |

Within a trigger clause, require every field to match. Across clauses, allow any one clause to match. Apply `_any`, `_all`, and `_none` with their ordinary set meanings.

Treat human-readable triggers and exclusions as explanations only. Validate executable clauses, routing modes, vocabulary, selection order, safety strength, lifecycle status, ownership, and relation graphs against the catalog.

## Explicit Skills and Compatibility

Resolve every `explicit_skills` name against the catalog. Require active, selectable canonical skills and recursively activate hard prerequisites. Reject missing, inactive, nonselectable, conflicting, or dependency-invalid requests.

Accept `process-budget-controller` only as a deprecated explicit compatibility name when its catalog successor is the `task-router` component. Record the alias in the route trace and exclusions; do not emit it or its component successor as an active skill and do not give it a separate process budget.

## Typed Relations

| Relation | Meaning |
|---|---|
| `requires` | Hard prerequisite; recursively activates the target. |
| `gates` | May veto a named phase without selecting a skill. |
| `runs_after` | Orders skills already selected independently. |
| `supports` | Supplies advisory evidence without activating the target. |
| `conflicts_with` | Prevents simultaneous ownership and produces a blocking veto. |
| `consumes` | Names an input artifact or decision. |
| `superseded_by` | Records lifecycle replacement, not execution order. |

Topologically enforce selected `requires` and `runs_after` edges together. Fail closed on a cycle. Reject multiple active owners for one decision domain.

## Skill Budget

Allow zero selected skills for routine work covered by core policy. Target two or fewer skills for routine tasks and normally cap optional selections at five or the descriptor's lower explicit limit. Exempt mandatory safety skills and hard prerequisites from the optional budget.

Do not count compatibility names or components as active selections. Never let budget pruning remove an independent safety gate.

## Artifact Evidence and Creation

Keep artifact evidence separate from artifact creation permission.

### Verified Evidence

For each `evidence.artifacts` record with `status=passed`:

1. Require a kind from the catalog artifact namespace.
2. Normalize the repository-relative path and reject escape.
3. Require the path to resolve to a repository file.
4. Recompute the file SHA-256 and require an exact match.

Evidence producers must hash the exact bytes the router will inspect. Checked-in cross-platform fixtures should use an explicitly byte-stable asset rather than a text file whose checkout line endings can vary.

Use verified kinds to satisfy `required_when_governed` artifact gates. Existing verified evidence can pass even when artifact creation policy is `forbid` and file-write authority is absent.

If required evidence is missing, emit a `required` gate before a terminal checkpoint. At `post_diff`, block only requested commit permission. At `pre_external_action`, block only requested external operations. Do not turn missing evidence into broader authority.

### Creation Allowance

Set `artifact_allowance.allowed=true` only when:

1. The task is not read-only.
2. Artifact policy permits creation.
3. `write_files` is requested and explicitly granted.

List only catalog artifact kinds. Treat this allowance as permission to create task-scoped files, never as evidence that they already exist or pass a gate.

Treat a governance change manifest as repository-content binding, not an external-state snapshot. Carry remote target identity, before and desired state, rollback, and post-operation readback through typed evidence and audit records.

## Typed Output

Validate resolver output with `routing-result.schema.json` and cross-check it against the loaded catalog. Contract 2.1 emits:

1. Selected canonical skills and one owner for every selected decision domain, plus routing and safety owners.
2. Instance-unique gates with catalog `policy_gate_id` values.
3. A complete permission map, including `configure_remote`, that never exceeds descriptor authority.
4. Artifact creation allowance and catalog kinds.
5. Surfaced constraints, non-goals, material inferred requirements, uncertainties, and safety vetoes.
6. A bounded route trace containing operational evidence and compatibility facts, not hidden reasoning.
7. Optional and mandatory skill-budget counts.

Continue to accept frozen 2.0 result records without `configure_remote`; require the complete permission namespace for 2.1 results.

## Startup Declaration Scope

Require a user-facing `Skills in use` declaration only when the user explicitly requests it or governed/audited work needs a durable routing record. Do not require declarations for routine work. A schema-v3 governance artifact always includes its own startup declaration because that durable record binds selected skills and order to a catalog snapshot.

## Executable Checks

Run from the repository root:

```sh
python3 skills/skill-governance/scripts/generate_routing_views.py --repo-root . --check
python3 skills/skill-governance/scripts/resolve_task_route.py \
  --fixtures skills/skill-governance/fixtures/routing-scenarios.json \
  --pretty
python3 -m unittest discover \
  -s skills/skill-governance/tests \
  -p 'test_task_routing.py'
python3 -m unittest \
  skills.skill-governance.tests.test_remote_configuration
```

## Generated Views

Generate only from `skills/skill-catalog.json`:

1. `skills/SKILL-MAP.md`
2. `skills/docs/skill-index.md`
3. `skills/docs/skill-decision-tree.md`

Fail validation when a view differs from catalog output, frontmatter diverges from catalog description, a relation references an unknown target, decision ownership collides, or the combined hard-order graph cycles.

## Observation and Migration

Run 2.0 compatibility inputs and contract 2.1 routing across at least 30 representative tasks or two releases. Record only operational metadata: task class, checkpoint, selected names, route changes, corrections, retries, validation outcome, and elapsed/tool counts when available.

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

The ignored `skills/.routing-observations.jsonl` file keeps at most 100 schema-checked records. Require every selected name to exist in the catalog, and keep aggregate summaries free of task text.
