#!/usr/bin/env python3
"""Resolve a typed task descriptor through the canonical router contract.

The resolver never routes from prompt keywords. A caller first normalizes task
intent into ``task-descriptor.schema.json``; catalog clauses then select skills,
while an independent safety kernel controls authority, evidence, and mutation.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence


SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_ROOT = SCRIPT_PATH.parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from generate_routing_views import CatalogError, validate_catalog  # noqa: E402
from governance_common import normalize_repo_path  # noqa: E402


REPO_ROOT = SCRIPT_PATH.parents[3]
SKILL_ROOT = SCRIPT_PATH.parents[1]
SCHEMA_ROOT = SKILL_ROOT / "schemas"
TASK_SCHEMA = SCHEMA_ROOT / "task-descriptor.schema.json"
RESULT_SCHEMA = SCHEMA_ROOT / "routing-result.schema.json"
CATALOG_PATH = SKILL_ROOT.parent / "skill-catalog.json"
SCHEMA_VERSION = "2.1"

OPERATIONS = (
    "read",
    "run_commands",
    "write_files",
    "commit",
    "configure_remote",
    "push",
    "publish",
    "deploy",
    "delete",
    "migrate",
    "message",
)
MUTATING_OPERATIONS = frozenset(
    {
        "write_files",
        "commit",
        "configure_remote",
        "push",
        "publish",
        "deploy",
        "delete",
        "migrate",
        "message",
    }
)
EXTERNAL_OPERATIONS = frozenset(
    {"configure_remote", "push", "publish", "deploy", "delete", "migrate", "message"}
)
OPERATION_EFFECT = {
    "write_files": "workspace_files",
    "commit": "repository_history",
    "configure_remote": "remote_repository",
    "push": "remote_repository",
    "publish": "published_artifact",
    "deploy": "runtime_environment",
    "delete": "deletion",
    "migrate": "live_data",
    "message": "external_message",
}
EFFECT_OPERATIONS: dict[str, frozenset[str]] = {}
for _operation, _effect in OPERATION_EFFECT.items():
    EFFECT_OPERATIONS[_effect] = frozenset(
        {*EFFECT_OPERATIONS.get(_effect, frozenset()), _operation}
    )
EXTERNAL_EFFECTS = frozenset(
    {"remote_repository", "published_artifact", "runtime_environment", "live_data", "external_message", "deletion"}
)
ROUTING_DIMENSIONS = {
    "actions_any": ("actions", "any"),
    "operations_any": ("operations", "any"),
    "operations_all": ("operations", "all"),
    "effects_any": ("effects", "any"),
    "effects_all": ("effects", "all"),
    "surfaces_any": ("surfaces", "any"),
    "surfaces_all": ("surfaces", "all"),
    "domains_any": ("domains", "any"),
    "domains_all": ("domains", "all"),
    "flags_any": ("flags", "any"),
    "flags_all": ("flags", "all"),
    "flags_none": ("flags", "none"),
}
SYSTEM_OWNERS = {"task-router-v2", "safety-kernel-v2"}
FIXTURE_ROOT_FIELDS = frozenset({"schema_version", "descriptor_defaults", "scenarios"})
FIXTURE_SCENARIO_FIELDS = frozenset({"id", "description", "descriptor", "expected"})
FIXTURE_EXPECTATION_FIELDS = frozenset(
    {
        "artifact_allowed",
        "decision",
        "excluded_routes",
        "gate_statuses",
        "max_selected_skills",
        "permissions",
        "same_route_as",
        "selected_skills",
        "veto_codes",
    }
)


class DescriptorError(ValueError):
    """Raised when typed input, catalog policy, or output is unsafe or invalid."""


@dataclass(frozen=True)
class CatalogContract:
    payload: Mapping[str, Any]
    skills: Mapping[str, Mapping[str, Any]]
    selection_order: tuple[str, ...]
    active_skills: frozenset[str]
    gate_ids: frozenset[str]
    artifact_types: frozenset[str]
    decision_domains: frozenset[str]
    components: frozenset[str]
    routine_maximum: int


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise DescriptorError(f"cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise DescriptorError(f"invalid JSON in {path}: {exc}") from exc


def load_catalog_contract(
    path: Path = CATALOG_PATH,
    *,
    repo_root: Path = REPO_ROOT,
) -> CatalogContract:
    """Load and semantically validate the complete executable catalog contract."""

    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise DescriptorError("canonical skill catalog root must be an object")
    try:
        validated = validate_catalog(payload, repo_root.resolve())
    except CatalogError as exc:
        raise DescriptorError(f"invalid canonical skill catalog: {exc}") from exc
    skills = {skill["name"]: skill for skill in validated}
    policy = payload["router_policy"]
    active = frozenset(name for name, skill in skills.items() if skill["status"] == "active")
    return CatalogContract(
        payload=payload,
        skills=skills,
        selection_order=tuple(policy["selection_order"]),
        active_skills=active,
        gate_ids=frozenset(payload["gate_ids"]),
        artifact_types=frozenset(payload["artifact_types"]),
        decision_domains=frozenset(payload["decision_domains"]),
        components=frozenset(payload["components"]),
        routine_maximum=int(policy["skill_budget"]["routine_maximum"]),
    )


DEFAULT_CATALOG_CONTRACT = load_catalog_contract()


@dataclass(frozen=True)
class SelectedSkill:
    name: str
    mandatory: bool
    owner_domains: tuple[str, ...]
    reason: str


@dataclass
class RouteState:
    descriptor: Mapping[str, Any]
    contract: CatalogContract
    flags: frozenset[str]
    skills: dict[str, SelectedSkill] = field(default_factory=dict)
    owners: dict[str, str] = field(
        default_factory=lambda: {"routing": "task-router-v2", "safety": "safety-kernel-v2"}
    )
    gates: list[dict[str, Any]] = field(default_factory=list)
    vetoes: list[dict[str, Any]] = field(default_factory=list)
    excluded: list[dict[str, str]] = field(default_factory=list)
    compatibility_traces: list[str] = field(default_factory=list)

    def add_skill(self, name: str, *, mandatory: bool, reason: str) -> None:
        skill = self.contract.skills.get(name)
        if not skill or name not in self.contract.active_skills:
            raise DescriptorError(f"route selected a missing or non-active skill: {name}")
        if skill["routing_mode"] == "nonselectable":
            raise DescriptorError(f"route selected a nonselectable skill: {name}")
        owner_domains = tuple(skill["decision_domains"])
        existing = self.skills.get(name)
        if existing is None or (mandatory and not existing.mandatory):
            self.skills[name] = SelectedSkill(name, mandatory, owner_domains, reason)
        for owner_domain in owner_domains:
            existing_owner = self.owners.get(owner_domain)
            if existing_owner and existing_owner != name:
                raise DescriptorError(
                    f"decision domain {owner_domain!r} has multiple owners: "
                    f"{existing_owner} and {name}"
                )
            self.owners[owner_domain] = name

    def add_gate(
        self,
        gate_id: str,
        policy_gate_id: str,
        gate_type: str,
        *,
        operation: str | None,
        status: str,
        owner: str,
        reason: str,
        mandatory: bool = True,
    ) -> None:
        if policy_gate_id not in self.contract.gate_ids:
            raise DescriptorError(f"route emitted gate outside catalog namespace: {policy_gate_id}")
        if any(gate["id"] == gate_id for gate in self.gates):
            raise DescriptorError(f"route emitted duplicate gate id: {gate_id}")
        self.gates.append(
            {
                "id": gate_id,
                "policy_gate_id": policy_gate_id,
                "type": gate_type,
                "operation": operation,
                "status": status,
                "mandatory": mandatory,
                "owner": owner,
                "reason": reason,
            }
        )

    def add_veto(
        self,
        code: str,
        *,
        operation: str | None,
        disposition: str,
        reason: str,
    ) -> None:
        candidate = {
            "code": code,
            "operation": operation,
            "disposition": disposition,
            "reason": reason,
        }
        if candidate not in self.vetoes:
            self.vetoes.append(candidate)

    def exclude(self, route: str, reason: str) -> None:
        candidate = {"route": route, "reason": reason}
        if candidate not in self.excluded:
            self.excluded.append(candidate)

    def record_compatibility_alias(self, name: str, successor: str) -> None:
        trace = f"explicit_skill_alias={name}->{successor}"
        if trace not in self.compatibility_traces:
            self.compatibility_traces.append(trace)
        self.exclude(
            name,
            f"Deprecated explicit compatibility name normalized to {successor!r}.",
        )


def _json_schema_errors(instance: Any, schema_path: Path) -> list[str]:
    schema = _read_json(schema_path)
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return _fallback_schema_errors(instance, schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda error: list(error.path))
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
        for error in errors
    ]


def _fallback_schema_errors(instance: Any, root_schema: Mapping[str, Any]) -> list[str]:
    """Validate the strict schema subset used here when jsonschema is unavailable."""

    errors: list[str] = []

    def resolve_ref(reference: str) -> Mapping[str, Any]:
        if not reference.startswith("#/"):
            raise DescriptorError(f"unsupported non-local schema reference: {reference}")
        node: Any = root_schema
        for token in reference[2:].split("/"):
            node = node[token.replace("~1", "/").replace("~0", "~")]
        if not isinstance(node, dict):
            raise DescriptorError(f"schema reference is not an object: {reference}")
        return node

    def type_matches(value: Any, expected: str) -> bool:
        return {
            "object": isinstance(value, dict),
            "array": isinstance(value, list),
            "string": isinstance(value, str),
            "boolean": isinstance(value, bool),
            "integer": isinstance(value, int) and not isinstance(value, bool),
            "number": isinstance(value, (int, float)) and not isinstance(value, bool),
            "null": value is None,
        }.get(expected, False)

    def visit(value: Any, schema: Mapping[str, Any], location: str) -> None:
        if len(errors) >= 100:
            return
        if "$ref" in schema:
            visit(value, resolve_ref(schema["$ref"]), location)
            return
        for subschema in schema.get("allOf", []):
            visit(value, subschema, location)
        if "if" in schema:
            condition_start = len(errors)
            visit(value, schema["if"], location)
            condition_matches = len(errors) == condition_start
            del errors[condition_start:]
            selected_branch = schema.get("then" if condition_matches else "else")
            if isinstance(selected_branch, dict):
                visit(value, selected_branch, location)
        if "const" in schema and value != schema["const"]:
            errors.append(f"{location}: must equal {schema['const']!r}")
        if "enum" in schema and value not in schema["enum"]:
            errors.append(f"{location}: {value!r} is not an allowed value")
        expected_types = schema.get("type")
        if expected_types is not None:
            expected_types = [expected_types] if isinstance(expected_types, str) else expected_types
            if not any(type_matches(value, expected) for expected in expected_types):
                errors.append(
                    f"{location}: expected type {' or '.join(expected_types)}, got {type(value).__name__}"
                )
                return
        if isinstance(value, dict):
            for name in schema.get("required", []):
                if name not in value:
                    errors.append(f"{location}: missing required property {name!r}")
            properties = schema.get("properties", {})
            additional = schema.get("additionalProperties", True)
            for name, child in value.items():
                child_location = f"{location}.{name}" if location != "$" else name
                if name in properties:
                    visit(child, properties[name], child_location)
                elif additional is False:
                    errors.append(f"{child_location}: additional property is not allowed")
                elif isinstance(additional, dict):
                    visit(child, additional, child_location)
            if len(value) < schema.get("minProperties", 0):
                errors.append(f"{location}: has too few properties")
            pattern = schema.get("propertyNames", {}).get("pattern")
            if pattern:
                for name in value:
                    if re.search(pattern, name) is None:
                        errors.append(f"{location}: property name {name!r} is invalid")
        if isinstance(value, list):
            if len(value) < schema.get("minItems", 0):
                errors.append(f"{location}: has too few items")
            if schema.get("uniqueItems"):
                rendered = [json.dumps(item, sort_keys=True) for item in value]
                if len(rendered) != len(set(rendered)):
                    errors.append(f"{location}: items must be unique")
            if isinstance(schema.get("items"), dict):
                for index, child in enumerate(value):
                    visit(child, schema["items"], f"{location}[{index}]")
        if isinstance(value, str):
            if len(value) < schema.get("minLength", 0):
                errors.append(f"{location}: string is too short")
            if schema.get("maxLength") is not None and len(value) > schema["maxLength"]:
                errors.append(f"{location}: string is too long")
            if schema.get("pattern") and re.search(schema["pattern"], value) is None:
                errors.append(f"{location}: string does not match {schema['pattern']!r}")
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if schema.get("minimum") is not None and value < schema["minimum"]:
                errors.append(f"{location}: value is below {schema['minimum']}")
            if schema.get("maximum") is not None and value > schema["maximum"]:
                errors.append(f"{location}: value is above {schema['maximum']}")

    visit(instance, root_schema, "$")
    return errors


def validate_task_descriptor(descriptor: Any) -> None:
    errors = _json_schema_errors(descriptor, TASK_SCHEMA)
    if errors:
        raise DescriptorError("invalid task descriptor:\n- " + "\n- ".join(errors))


def _normalize_task_descriptor(descriptor: Mapping[str, Any]) -> dict[str, Any]:
    """Upgrade accepted legacy descriptor omissions without mutating caller data."""

    normalized = copy.deepcopy(dict(descriptor))
    normalized["constraints"].setdefault("explicit_skills", [])
    normalized["evidence"].setdefault("artifacts", [])
    return normalized


def _has_mutating_request(descriptor: Mapping[str, Any]) -> bool:
    return bool(MUTATING_OPERATIONS.intersection(descriptor["action"]["operations"]))


def _has_live_or_destructive_effect(descriptor: Mapping[str, Any]) -> bool:
    operations = set(descriptor["action"]["operations"])
    effects = set(descriptor["effects"])
    return bool(
        operations.intersection({"deploy", "delete", "migrate"})
        or effects.intersection({"runtime_environment", "live_data", "deletion"})
        or descriptor["mutation"]["destructive"]
    )


def _derive_flags(descriptor: Mapping[str, Any], contract: CatalogContract) -> frozenset[str]:
    action = descriptor["action"]
    mutation = descriptor["mutation"]
    operations = set(action["operations"])
    effects = set(descriptor["effects"])
    surfaces = set(descriptor["surfaces"])
    domains = set(descriptor["domains"])
    unresolved_material = any(
        item["status"] != "resolved" and item["severity"] in {"material", "critical"}
        for item in descriptor["material_uncertainties"]
    )
    frontend_work = "frontend" in surfaces and action["primary"] in {"edit", "implement", "review"}
    code_surface = bool(surfaces.intersection({"source", "frontend", "backend", "cli"}))
    live_or_destructive = _has_live_or_destructive_effect(descriptor)
    release_boundary = action["primary"] == "release" or bool(operations.intersection({"publish", "deploy"}))
    governance_change = "governance_policy" in effects
    regression_risk = bool(
        (code_surface and action["primary"] == "review")
        or (code_surface and action["primary"] in {"edit", "implement"} and action["behavior_change"])
        or release_boundary
        or live_or_destructive
    )
    documentation_candidate = bool(
        ("documentation" in effects or "documentation" in surfaces)
        and action["primary"] in {"edit", "implement", "review"}
    )
    values = {
        "adaptive_workflow": action["execution_mode"] == "adaptive_browser",
        "coupled_change": action["coupled_change"],
        "credible_data_loss": mutation["data_loss_risk"] == "credible",
        "deterministic_workflow": action["execution_mode"] == "deterministic_workflow",
        "documentation_candidate": documentation_candidate,
        "documentation_sync": action["documentation_sync"],
        "frontend_work": frontend_work,
        "governance_boundary": governance_change or release_boundary or live_or_destructive,
        "governance_change": governance_change,
        "governance_tooling": action["governance_tooling"],
        "incidental_commands": action["execution_mode"] == "incidental_validation",
        "live_or_destructive": live_or_destructive,
        "material_uncertainty": unresolved_material,
        "mutation_unknown": mutation["level"] == "unknown",
        "product_judgment": action["product_judgment"],
        "recovery_considered": mutation["data_loss_risk"] != "none"
        or mutation["recovery_requirement"] != "not_required",
        "recovery_required": mutation["recovery_requirement"] == "required",
        "recovery_unknown": mutation["data_loss_risk"] == "unknown"
        or mutation["recovery_requirement"] == "unknown",
        "regression_risk": regression_risk,
        "release_boundary": release_boundary,
        "release_enforcement": action["release_enforcement"],
        "run_existing_tests": action["test_intent"] == "run_existing",
        "sequencing_required": action["sequencing_required"],
        "source_only_sensitive": bool(domains.intersection({"auth", "migration"}))
        and not live_or_destructive,
        "spatial_canvas": "spatial_canvas" in domains,
        "test_activity": action["test_intent"] != "none",
        "test_design": action["test_intent"] == "design_or_change",
        "ui_quality_judgment": action["ui_quality_judgment"],
    }
    vocabulary = set(contract.payload["routing_vocabulary"]["flags"])
    implemented = set(values)
    if implemented != vocabulary:
        raise DescriptorError(
            "router/catalog flag vocabulary drift; "
            f"missing_implementations={sorted(vocabulary - implemented)}, "
            f"uncataloged_implementations={sorted(implemented - vocabulary)}"
        )
    flags = frozenset(name for name, enabled in values.items() if enabled)
    return flags


def _routing_context(descriptor: Mapping[str, Any], flags: frozenset[str]) -> dict[str, frozenset[str]]:
    return {
        "actions": frozenset({descriptor["action"]["primary"]}),
        "operations": frozenset(descriptor["action"]["operations"]),
        "effects": frozenset(descriptor["effects"]),
        "surfaces": frozenset(descriptor["surfaces"]),
        "domains": frozenset(descriptor["domains"]),
        "flags": flags,
    }


def _clause_matches(clause: Mapping[str, Sequence[str]], context: Mapping[str, frozenset[str]]) -> bool:
    for field, expected_values in clause.items():
        dimension, operator = ROUTING_DIMENSIONS[field]
        actual = context[dimension]
        expected = set(expected_values)
        if operator == "any" and not actual.intersection(expected):
            return False
        if operator == "all" and not expected.issubset(actual):
            return False
        if operator == "none" and actual.intersection(expected):
            return False
    return True


def _select_catalog_skills(state: RouteState) -> None:
    context = _routing_context(state.descriptor, state.flags)
    for name in state.contract.selection_order:
        skill = state.contract.skills[name]
        routing = skill["routing"]
        trigger = next((clause for clause in routing["triggers"] if _clause_matches(clause, context)), None)
        if trigger is None:
            continue
        exclusion = next(
            (clause for clause in routing["exclusions"] if _clause_matches(clause, context)),
            None,
        )
        if exclusion is not None:
            state.exclude(name, f"Catalog exclusion matched: {json.dumps(exclusion, sort_keys=True)}")
            continue
        mandatory = skill["routing_mode"] == "safety_only" or routing["selection_strength"] == "required"
        state.add_skill(
            name,
            mandatory=mandatory,
            reason=f"Catalog trigger matched: {json.dumps(trigger, sort_keys=True)}",
        )

    for name in state.descriptor["constraints"]["explicit_skills"]:
        skill = state.contract.skills.get(name)
        if not skill:
            raise DescriptorError(f"explicit skill request is missing: {name}")
        if name == "process-budget-controller" and skill.get("status") == "deprecated":
            successors = skill.get("relations", {}).get("superseded_by", [])
            if successors != ["task-router"] or "task-router" not in state.contract.components:
                raise DescriptorError(
                    "deprecated explicit skill process-budget-controller has an invalid "
                    "task-router successor"
                )
            state.record_compatibility_alias(name, "task-router")
            continue
        if name not in state.contract.active_skills:
            raise DescriptorError(f"explicit skill request is non-active: {name}")
        if skill["routing_mode"] == "nonselectable":
            raise DescriptorError(f"explicit skill request is nonselectable: {name}")
        state.add_skill(
            name,
            mandatory=True,
            reason="Typed descriptor records an explicit skill request.",
        )

    pending = list(state.skills)
    visited: set[str] = set()
    while pending:
        name = pending.pop(0)
        if name in visited:
            continue
        visited.add(name)
        for target in state.contract.skills[name]["relations"]["requires"]:
            if target in state.contract.components:
                continue
            target_skill = state.contract.skills.get(target)
            if not target_skill or target_skill["status"] != "active":
                raise DescriptorError(f"{name} requires unavailable skill {target}")
            state.add_skill(target, mandatory=True, reason=f"Hard prerequisite of {name}.")
            pending.append(target)

    names = set(state.skills)
    conflict_pairs: set[tuple[str, str]] = set()
    for name in sorted(names):
        for target in state.contract.skills[name]["relations"]["conflicts_with"]:
            if target in names:
                conflict_pairs.add(tuple(sorted((name, target))))
    for left, right in sorted(conflict_pairs):
        state.add_veto(
            "skill_conflict",
            operation=None,
            disposition="block",
            reason=f"Catalog conflict prevents simultaneous selection: {left} and {right}.",
        )


def _check_descriptor_consistency(state: RouteState) -> None:
    descriptor = state.descriptor
    action = descriptor["action"]
    mutation = descriptor["mutation"]
    operations = set(action["operations"])
    effects = set(descriptor["effects"])
    findings: list[tuple[str, str | None, str, str]] = []

    def add(reason: str, operation: str | None = None, *, disposition: str = "block", code: str = "descriptor_conflict") -> None:
        findings.append((reason, operation, disposition, code))

    for operation, expected_effect in OPERATION_EFFECT.items():
        if operation in operations and expected_effect not in effects:
            add(f"Operation {operation!r} requires effect {expected_effect!r}.", operation)
    for effect, allowed_operations in EFFECT_OPERATIONS.items():
        if effect in effects and not operations.intersection(allowed_operations):
            rendered = ", ".join(repr(item) for item in sorted(allowed_operations))
            add(f"Effect {effect!r} requires one of operations: {rendered}.")

    state_effects = effects.intersection(set(OPERATION_EFFECT.values()))
    if mutation["level"] == "none" and (state_effects or _has_mutating_request(descriptor)):
        add("Mutation level 'none' conflicts with requested state change.")
    if mutation["level"] not in {"none", "unknown"} and not mutation["targets"]:
        add("A mutating descriptor must identify at least one target.")
    if mutation["level"] == "workspace" and effects.intersection(EXTERNAL_EFFECTS | {"repository_history"}):
        add("Workspace mutation level conflicts with repository or external effects.")
    if mutation["level"] == "repository" and effects.intersection(EXTERNAL_EFFECTS):
        add("Repository mutation level conflicts with external effects.")
    if mutation["destructive"] and not (
        effects.intersection({"deletion", "live_data"}) or operations.intersection({"delete", "migrate"})
    ):
        add("Destructive mutation is declared without a destructive effect.")
    if "unknown" in effects and _has_mutating_request(descriptor):
        add("Unknown effects cannot accompany a mutating request.")

    has_commands = "run_commands" in operations
    execution_mode = action["execution_mode"]
    command_effect = action["command_effect"]
    if has_commands and execution_mode == "none":
        add("run_commands requires a typed execution_mode.", "run_commands")
    if not has_commands and execution_mode != "none":
        add("execution_mode must be 'none' when run_commands is absent.", "run_commands")
    if has_commands and command_effect == "not_applicable":
        add("run_commands requires a typed command_effect.", "run_commands")
    if not has_commands and command_effect != "not_applicable":
        add("command_effect must be 'not_applicable' when run_commands is absent.", "run_commands")
    if command_effect == "unknown":
        add(
            "Unknown command effects must be resolved before command execution.",
            "run_commands",
            disposition="block" if descriptor["constraints"]["read_only"] else "clarify",
            code="command_effect_unknown",
        )
    if execution_mode == "incidental_validation" and command_effect not in {"read_only", "unknown"}:
        add("Incidental validation commands must be read-only.", "run_commands")
    if execution_mode == "adaptive_browser" and "browser" not in descriptor["surfaces"]:
        add("adaptive_browser execution requires the browser surface.", "run_commands")
    if command_effect == "workspace" and not ({"write_files"} <= operations and "workspace_files" in effects):
        add("Workspace command effect requires write_files and workspace_files.", "run_commands")
    if command_effect == "repository" and not ({"commit"} <= operations and "repository_history" in effects):
        add("Repository command effect requires commit and repository_history.", "run_commands")
    if command_effect == "external" and not (
        operations.intersection(EXTERNAL_OPERATIONS) and effects.intersection(EXTERNAL_EFFECTS)
    ):
        add("External command effect requires a matching external operation and effect.", "run_commands")

    if action["test_change"] != (action["test_intent"] == "design_or_change"):
        add("test_change must exactly match test_intent='design_or_change'.")
    if action["test_intent"] == "run_existing" and not has_commands:
        add("Running existing tests requires run_commands.", "run_commands")
    if (action["primary"] == "release" or "publish" in operations) and not action["release_enforcement"]:
        add("Release or publish operations require release_enforcement=true.", "publish")

    destructive_operation = bool(operations.intersection({"delete", "migrate"}) or mutation["destructive"])
    if destructive_operation and mutation["data_loss_risk"] != "credible":
        add("Delete, migrate, or destructive work requires credible data-loss classification.")
    if destructive_operation and mutation["recovery_requirement"] != "required":
        add("Delete, migrate, or destructive work requires recovery_requirement='required'.")
    if mutation["data_loss_risk"] == "credible" and mutation["recovery_requirement"] != "required":
        add("Credible data-loss risk requires a recovery path.")
    recovery_unknown = (
        mutation["data_loss_risk"] == "unknown" or mutation["recovery_requirement"] == "unknown"
    )
    if recovery_unknown and (
        operations.intersection(EXTERNAL_OPERATIONS) or _has_live_or_destructive_effect(descriptor)
    ):
        add(
            "Recovery state is unknown for an external, live, or destructive operation.",
            None,
            disposition="clarify",
            code="recovery_state_unknown",
        )
    if mutation["level"] == "unknown" and _has_mutating_request(descriptor):
        add(
            "Mutation scope is unknown for a task that may change state.",
            None,
            disposition="clarify",
            code="mutation_state_unknown",
        )

    if findings or any(veto["code"] == "skill_conflict" for veto in state.vetoes):
        for reason, operation, disposition, code in findings:
            state.add_veto(code, operation=operation, disposition=disposition, reason=reason)
        status = "blocked" if any(veto["disposition"] == "block" for veto in state.vetoes) else "needs_resolution"
        state.add_gate(
            "descriptor-consistency",
            "descriptor_consistency",
            "descriptor_consistency",
            operation=None,
            status=status,
            owner="safety-kernel-v2",
            reason="Typed descriptor and catalog relations contain unresolved conflicts.",
        )
    else:
        state.add_gate(
            "descriptor-consistency",
            "descriptor_consistency",
            "descriptor_consistency",
            operation=None,
            status="passed",
            owner="safety-kernel-v2",
            reason="Typed action, command, mutation, recovery, and effect fields are coherent.",
        )


def _add_authorization_gates(state: RouteState) -> None:
    descriptor = state.descriptor
    action = descriptor["action"]
    operations = set(action["operations"])
    effects = set(descriptor["effects"])
    authority = descriptor["authority"]
    read_only = descriptor["constraints"]["read_only"]
    command_effect_mutates = action["command_effect"] in {"workspace", "repository", "external", "unknown"}
    read_only_conflicts = operations.intersection(MUTATING_OPERATIONS) or effects.intersection(
        set(OPERATION_EFFECT.values())
    )
    if read_only and (read_only_conflicts or command_effect_mutates):
        for operation in sorted(operations.intersection(MUTATING_OPERATIONS)):
            state.add_veto(
                "read_only_conflict",
                operation=operation,
                disposition="block",
                reason=f"Read-only scope forbids operation {operation!r}.",
            )
        if command_effect_mutates:
            state.add_veto(
                "read_only_command_effect",
                operation="run_commands",
                disposition="block",
                reason=f"Read-only scope forbids command effect {action['command_effect']!r}.",
            )
        read_status = "blocked"
        read_reason = "Read-only scope conflicts with a state-changing or unknown effect."
    else:
        read_status = "passed"
        read_reason = "Read-only boundary is coherent with the typed operation effects."
    state.add_gate(
        "read-only-boundary",
        "read_only",
        "safety_boundary",
        operation=None,
        status=read_status,
        owner="safety-kernel-v2",
        reason=read_reason,
    )

    for operation in OPERATIONS:
        if operation not in operations:
            continue
        authority_status = authority.get(operation, "unknown")
        if authority_status == "granted":
            gate_status = "passed"
            reason = f"Authority for {operation!r} is explicitly granted."
        elif authority_status == "denied":
            gate_status = "blocked"
            reason = f"Authority for {operation!r} is explicitly denied."
            state.add_veto("authority_denied", operation=operation, disposition="block", reason=reason)
        else:
            gate_status = "needs_resolution"
            reason = f"Authority for {operation!r} is unknown."
            state.add_veto("authority_unknown", operation=operation, disposition="clarify", reason=reason)
        state.add_gate(
            f"authority-{operation}",
            "authorization",
            "authorization",
            operation=operation,
            status=gate_status,
            owner="safety-kernel-v2",
            reason=reason,
        )


def _add_uncertainty_gate(state: RouteState) -> None:
    unresolved = [
        item for item in state.descriptor["material_uncertainties"] if item["status"] != "resolved"
    ]
    mutating = _has_mutating_request(state.descriptor)
    blocking = [
        item
        for item in unresolved
        if item["severity"] == "critical" or (item["severity"] == "material" and mutating)
    ]
    for item in blocking:
        disposition = "block" if item["status"] == "conflicting" else "clarify"
        state.add_veto(
            "critical_state_unresolved",
            operation=None,
            disposition=disposition,
            reason=f"{item['id']}: {item['description']}",
        )
    if blocking:
        status = "blocked" if any(item["status"] == "conflicting" for item in blocking) else "needs_resolution"
        reason = "Critical or mutation-material uncertainty must be resolved before execution."
    elif unresolved:
        status = "required"
        reason = "Non-blocking uncertainty remains and must be surfaced."
    else:
        status = "passed"
        reason = "No unresolved material uncertainty blocks this checkpoint."
    owner = "requirement-clarifier" if "requirement-clarifier" in state.skills else "task-router-v2"
    state.add_gate(
        "material-uncertainty",
        "material_uncertainty",
        "uncertainty",
        operation=None,
        status=status,
        owner=owner,
        reason=reason,
    )


def _add_checkpoint_gate(state: RouteState) -> None:
    protected = set(state.descriptor["action"]["operations"]).intersection(EXTERNAL_OPERATIONS)
    if not protected:
        return
    if state.descriptor["checkpoint"] == "pre_external_action":
        status = "passed"
        reason = "Route was recalculated immediately before external or irreversible action."
    else:
        status = "blocked"
        reason = "External or irreversible action requires a pre_external_action reroute."
        for operation in sorted(protected):
            state.add_veto("checkpoint_required", operation=operation, disposition="block", reason=reason)
    state.add_gate(
        "pre-external-checkpoint",
        "external_checkpoint",
        "checkpoint",
        operation=None,
        status=status,
        owner="safety-kernel-v2",
        reason=reason,
    )


def _evidence_gate(
    state: RouteState,
    *,
    gate_id: str,
    policy_gate_id: str,
    evidence_key: str,
    operation: str | None,
    required_now: bool,
    owner: str,
    reason: str,
) -> None:
    evidence_status = state.descriptor["evidence"][evidence_key]
    if evidence_status == "passed":
        status = "passed"
    elif required_now:
        status = "blocked"
        state.add_veto(
            "evidence_not_passed",
            operation=operation,
            disposition="block",
            reason=f"{evidence_key} evidence is {evidence_status!r}; passed evidence is required.",
        )
    else:
        status = "required"
    state.add_gate(
        gate_id,
        policy_gate_id,
        "evidence",
        operation=operation,
        status=status,
        owner=owner,
        reason=reason,
    )


def _add_evidence_gates(state: RouteState) -> None:
    descriptor = state.descriptor
    action = descriptor["action"]
    operations = set(action["operations"])
    checkpoint = descriptor["checkpoint"]
    completion = checkpoint in {"post_diff", "pre_external_action"}
    if action["behavior_change"] or action["test_change"] or action["primary"] == "release":
        release_operation = "publish" if "publish" in operations else "deploy" if "deploy" in operations else None
        _evidence_gate(
            state,
            gate_id="tests-passed",
            policy_gate_id="test_evidence",
            evidence_key="tests",
            operation=release_operation,
            required_now=completion,
            owner="regression-prevention" if "regression-prevention" in state.skills else "safety-kernel-v2",
            reason="Behavior changes and releases require proportional passing test evidence.",
        )
    for operation in sorted(
        operations.intersection({"configure_remote", "deploy", "delete", "migrate"})
    ):
        _evidence_gate(
            state,
            gate_id=f"rollback-ready-{operation}",
            policy_gate_id="rollback_evidence",
            evidence_key="rollback",
            operation=operation,
            required_now=checkpoint == "pre_external_action",
            owner="skill-governance" if "skill-governance" in state.skills else "safety-kernel-v2",
            reason=f"Operation {operation!r} requires an actionable rollback path.",
        )

    protected = sorted(operations.intersection(EXTERNAL_OPERATIONS))
    recovery_operation = protected[0] if protected else None
    if "project-backup" in state.skills:
        _evidence_gate(
            state,
            gate_id="backup-evidence",
            policy_gate_id="backup_evidence",
            evidence_key="backup",
            operation=recovery_operation,
            required_now=checkpoint == "pre_external_action" and recovery_operation is not None,
            owner="project-backup",
            reason="Selected backup control requires current integrity evidence.",
        )
    if "restore-drill" in state.skills:
        _evidence_gate(
            state,
            gate_id="restore-evidence",
            policy_gate_id="restore_evidence",
            evidence_key="restore",
            operation=recovery_operation,
            required_now=checkpoint == "pre_external_action" and recovery_operation is not None,
            owner="restore-drill",
            reason="Selected recovery control requires verified restore evidence.",
        )
    release_enforced = action["release_enforcement"] and (
        action["primary"] == "release" or "publish" in operations
    )
    if release_enforced:
        _evidence_gate(
            state,
            gate_id="exact-commit-green",
            policy_gate_id="exact_commit",
            evidence_key="exact_commit",
            operation="publish" if "publish" in operations else None,
            required_now=checkpoint == "pre_external_action",
            owner="governance-enforcement" if "governance-enforcement" in state.skills else "safety-kernel-v2",
            reason="Release enforcement requires green evidence bound to the exact candidate commit.",
        )


def _ordered_skill_names(state: RouteState, names: set[str]) -> list[str]:
    base_order = {name: index for index, name in enumerate(state.contract.selection_order)}
    fallback = {name: index + len(base_order) for index, name in enumerate(sorted(names - set(base_order)))}
    rank = {**base_order, **fallback}
    outgoing = {name: set() for name in names}
    indegree = {name: 0 for name in names}
    for name in names:
        skill = state.contract.skills[name]
        predecessors = set(skill["relations"]["runs_after"]).intersection(names)
        predecessors.update(set(skill["relations"]["requires"]).intersection(names))
        for predecessor in predecessors:
            if name not in outgoing[predecessor]:
                outgoing[predecessor].add(name)
                indegree[name] += 1
    ready = sorted((name for name, degree in indegree.items() if degree == 0), key=lambda name: (rank[name], name))
    ordered: list[str] = []
    while ready:
        name = ready.pop(0)
        ordered.append(name)
        for target in sorted(outgoing[name], key=lambda item: (rank[item], item)):
            indegree[target] -= 1
            if indegree[target] == 0:
                ready.append(target)
                ready.sort(key=lambda item: (rank[item], item))
    if len(ordered) != len(names):
        cyclic = sorted(name for name, degree in indegree.items() if degree)
        raise DescriptorError(f"selected skill ordering cycle: {cyclic}")
    return ordered


def _apply_skill_budget(state: RouteState) -> tuple[list[str], dict[str, Any]]:
    mandatory = {name for name, selected in state.skills.items() if selected.mandatory}
    optional = set(state.skills) - mandatory
    non_safety_mandatory = {
        name for name in mandatory if state.contract.skills[name]["routing_mode"] != "safety_only"
    }
    routine_slots = max(0, state.contract.routine_maximum - len(non_safety_mandatory))
    optional_limit = min(state.descriptor["constraints"]["max_optional_skills"], routine_slots)
    ordered_optional = _ordered_skill_names(state, optional) if optional else []
    retained_optional = set(ordered_optional[:optional_limit])
    for omitted in ordered_optional[optional_limit:]:
        for domain, owner in list(state.owners.items()):
            if owner == omitted:
                del state.owners[domain]
        state.exclude(omitted, "Optional skill omitted by the routine skill budget.")
    selected_set = mandatory | retained_optional
    selected = _ordered_skill_names(state, selected_set) if selected_set else []
    budget = {
        "max_optional_skills": state.descriptor["constraints"]["max_optional_skills"],
        "optional_before_budget": len(optional),
        "optional_after_budget": len(retained_optional),
        "mandatory_skills": _ordered_skill_names(state, mandatory) if mandatory else [],
        "mandatory_safety_exempt": True,
    }
    return selected, budget


def _build_permissions(state: RouteState) -> dict[str, bool]:
    descriptor = state.descriptor
    action = descriptor["action"]
    operations = set(action["operations"])
    authority = descriptor["authority"]
    global_veto = any(veto["operation"] is None for veto in state.vetoes)
    blocked_operations = {veto["operation"] for veto in state.vetoes if veto["operation"] is not None}
    permissions: dict[str, bool] = {}
    for operation in OPERATIONS:
        allowed = operation in operations and authority.get(operation, "unknown") == "granted"
        if operation in blocked_operations:
            allowed = False
        if global_veto and operation != "read":
            allowed = False
        if descriptor["constraints"]["read_only"] and operation in MUTATING_OPERATIONS:
            allowed = False
        permissions[operation] = allowed

    if "run_commands" in operations:
        effect = action["command_effect"]
        if effect in {"unknown", "not_applicable"}:
            permissions["run_commands"] = False
        elif effect == "workspace" and not permissions["write_files"]:
            permissions["run_commands"] = False
        elif effect == "repository" and not permissions["commit"]:
            permissions["run_commands"] = False
        elif effect == "external":
            external_requested = operations.intersection(EXTERNAL_OPERATIONS)
            if not external_requested or not all(permissions[operation] for operation in external_requested):
                permissions["run_commands"] = False
    return permissions


def _verified_artifact_kinds(state: RouteState, repo_root: Path) -> set[str]:
    verified: set[str] = set()
    for index, record in enumerate(state.descriptor["evidence"].get("artifacts", [])):
        kind = record["kind"]
        if kind not in state.contract.artifact_types:
            raise DescriptorError(
                f"evidence.artifacts[{index}].kind is outside the catalog namespace: {kind}"
            )
        try:
            path = normalize_repo_path(record["path"])
        except SystemExit as exc:
            raise DescriptorError(f"evidence.artifacts[{index}].path is invalid: {exc}") from exc
        if record["status"] != "passed":
            continue
        candidate = repo_root.resolve() / path
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(repo_root.resolve())
        except (FileNotFoundError, OSError, ValueError) as exc:
            raise DescriptorError(
                f"passed artifact evidence cannot be resolved inside the repository: {path}"
            ) from exc
        if not resolved.is_file():
            raise DescriptorError(f"passed artifact evidence is not a file: {path}")
        digest = hashlib.sha256(resolved.read_bytes()).hexdigest()
        if digest != record["sha256"]:
            raise DescriptorError(
                f"passed artifact evidence digest mismatch for {path}: "
                f"expected {record['sha256']}, actual {digest}"
            )
        verified.add(kind)
    return verified


def _add_required_artifact_gate(
    state: RouteState,
    selected_skills: Sequence[str],
    repo_root: Path,
) -> None:
    required_kinds = sorted(
        {
            artifact
            for name in selected_skills
            if state.contract.skills[name]["artifact_policy"]["durability"]
            == "required_when_governed"
            for artifact in state.contract.skills[name]["artifact_policy"]["artifacts"]
        }
    )
    if not required_kinds:
        return

    descriptor = state.descriptor
    verified = _verified_artifact_kinds(state, repo_root)
    missing = sorted(set(required_kinds) - verified)
    if not missing:
        status = "passed"
        reason = "Every required governed artifact has verified path and digest evidence."
    else:
        operations = set(descriptor["action"]["operations"])
        checkpoint = descriptor["checkpoint"]
        protected_operations: list[str] = []
        if checkpoint == "pre_external_action":
            protected_operations = sorted(operations.intersection(EXTERNAL_OPERATIONS))
        elif checkpoint == "post_diff" and "commit" in operations:
            protected_operations = ["commit"]
        status = "blocked" if protected_operations else "required"
        reason = "Required governed artifact evidence is missing: " + ", ".join(missing) + "."
        for operation in protected_operations:
            state.add_veto(
                "required_artifact_missing",
                operation=operation,
                disposition="block",
                reason=reason,
            )
    owner = (
        "governance-enforcement"
        if "governance-enforcement" in selected_skills
        else "skill-governance"
    )
    state.add_gate(
        "required-governance-artifacts",
        "governance_evidence",
        "evidence",
        operation=None,
        status=status,
        owner=owner,
        reason=reason + f" Required kinds: {', '.join(required_kinds)}.",
    )


def _artifact_allowance(
    state: RouteState,
    selected_skills: Sequence[str],
    permissions: Mapping[str, bool],
) -> dict[str, Any]:
    descriptor = state.descriptor
    policy = descriptor["constraints"]["artifact_policy"]
    if descriptor["constraints"]["read_only"]:
        return {"allowed": False, "kinds": [], "reason": "Read-only scope forbids generated artifacts."}
    if policy == "forbid":
        return {"allowed": False, "kinds": [], "reason": "The descriptor forbids generated artifacts."}
    if not permissions["write_files"]:
        return {
            "allowed": False,
            "kinds": [],
            "reason": "Artifact creation requires requested and granted file-write authority.",
        }
    action = descriptor["action"]
    kinds: list[str] = []
    for name in selected_skills:
        artifact_policy = state.contract.skills[name]["artifact_policy"]
        if artifact_policy["durability"] == "required_when_governed" or policy == "allow":
            kinds.extend(artifact_policy["artifacts"])
    if action["behavior_change"]:
        kinds.append("change_evidence")
    if action["test_change"]:
        kinds.append("test_evidence")
    if action["primary"] == "operate":
        kinds.append("operation_plan")
    if action["primary"] == "release":
        kinds.extend(["governance_plan", "release_attestation"])
    if not kinds:
        kinds.append("change_evidence")
    unique = list(dict.fromkeys(kinds))
    unknown = set(unique) - state.contract.artifact_types
    if unknown:
        raise DescriptorError(f"artifact allowance escaped catalog namespace: {sorted(unknown)}")
    return {
        "allowed": True,
        "kinds": unique,
        "reason": "Task-scoped artifacts are permitted by policy and explicit file-write authority.",
    }


def _must_surface(state: RouteState) -> list[dict[str, str]]:
    descriptor = state.descriptor
    items: list[dict[str, str]] = []
    for index, value in enumerate(descriptor["constraints"]["explicit"], start=1):
        items.append({"id": f"constraint-{index}", "source": "explicit_constraint", "text": value})
    for index, value in enumerate(descriptor["constraints"]["non_goals"], start=1):
        items.append({"id": f"non-goal-{index}", "source": "non_goal", "text": value})
    for requirement in descriptor["inferred_requirements"]:
        if requirement["material"]:
            items.append(
                {
                    "id": f"inferred-{requirement['id'].lower()}",
                    "source": "inferred_requirement",
                    "text": requirement["description"],
                }
            )
    for uncertainty in descriptor["material_uncertainties"]:
        if uncertainty["status"] != "resolved":
            items.append(
                {
                    "id": f"uncertainty-{uncertainty['id'].lower()}",
                    "source": "material_uncertainty",
                    "text": uncertainty["description"],
                }
            )
    for index, veto in enumerate(state.vetoes, start=1):
        items.append({"id": f"safety-veto-{index}", "source": "safety_kernel", "text": veto["reason"]})
    return items


def _decision(vetoes: Sequence[Mapping[str, Any]]) -> str:
    if any(veto["disposition"] == "block" for veto in vetoes):
        return "blocked"
    if vetoes:
        return "needs_clarification"
    return "allow"


def validate_routing_result(
    result: Any,
    contract: CatalogContract | None = None,
) -> None:
    contract = contract or DEFAULT_CATALOG_CONTRACT
    errors = _json_schema_errors(result, RESULT_SCHEMA)
    if isinstance(result, dict):
        gates = result.get("typed_gates", [])
        gate_ids = [gate.get("id") for gate in gates]
        if len(gate_ids) != len(set(gate_ids)):
            errors.append("typed_gates: instance ids must be unique")
        unknown_policy_gates = {
            gate.get("policy_gate_id") for gate in gates if gate.get("policy_gate_id") not in contract.gate_ids
        }
        if unknown_policy_gates:
            errors.append(f"typed_gates: unknown catalog gate ids: {sorted(unknown_policy_gates)}")
        selected = set(result.get("selected_skills", []))
        if selected - contract.active_skills:
            errors.append(f"selected_skills: missing or non-active names: {sorted(selected - contract.active_skills)}")
        mandatory = set(result.get("skill_budget", {}).get("mandatory_skills", []))
        if not mandatory.issubset(selected):
            errors.append("skill_budget: mandatory skills must be selected")
        for domain, owner in result.get("decision_domain_owners", {}).items():
            if domain in {"routing", "safety"}:
                if owner not in SYSTEM_OWNERS:
                    errors.append(f"decision_domain_owners.{domain}: invalid system owner {owner}")
                continue
            if domain not in contract.decision_domains:
                errors.append(f"decision_domain_owners: unknown domain {domain}")
            if owner not in selected:
                errors.append(f"decision_domain_owners.{domain}: owner {owner} is not selected")
            elif domain not in contract.skills[owner]["decision_domains"]:
                errors.append(f"decision_domain_owners.{domain}: {owner} does not own this domain")
        artifact_kinds = set(result.get("artifact_allowance", {}).get("kinds", []))
        if artifact_kinds - contract.artifact_types:
            errors.append(f"artifact_allowance: unknown catalog types {sorted(artifact_kinds - contract.artifact_types)}")
        vetoes = result.get("vetoes", [])
        decision = result.get("decision")
        if decision == "allow" and vetoes:
            errors.append("decision: allow cannot contain vetoes")
        if decision == "needs_clarification" and (
            not vetoes or any(veto.get("disposition") != "clarify" for veto in vetoes)
        ):
            errors.append("decision: needs_clarification requires only clarify vetoes")
        if decision == "blocked" and not any(veto.get("disposition") == "block" for veto in vetoes):
            errors.append("decision: blocked requires a blocking veto")
    if errors:
        raise DescriptorError("invalid routing result:\n- " + "\n- ".join(errors))


def resolve_task_route(
    descriptor: Mapping[str, Any],
    *,
    catalog_path: Path | None = None,
    repo_root: Path = REPO_ROOT,
    contract: CatalogContract | None = None,
) -> dict[str, Any]:
    """Return a deterministic, catalog-driven, fail-closed task route."""

    validate_task_descriptor(descriptor)
    descriptor = _normalize_task_descriptor(descriptor)
    contract = contract or (
        DEFAULT_CATALOG_CONTRACT
        if catalog_path is None and repo_root.resolve() == REPO_ROOT.resolve()
        else load_catalog_contract(catalog_path or CATALOG_PATH, repo_root=repo_root)
    )
    flags = _derive_flags(descriptor, contract)
    state = RouteState(descriptor=descriptor, contract=contract, flags=flags)
    _select_catalog_skills(state)
    _check_descriptor_consistency(state)
    _add_authorization_gates(state)
    _add_uncertainty_gate(state)
    _add_checkpoint_gate(state)
    _add_evidence_gates(state)
    selected_skills, budget = _apply_skill_budget(state)
    _add_required_artifact_gate(state, selected_skills, repo_root)
    permissions = _build_permissions(state)
    artifacts = _artifact_allowance(state, selected_skills, permissions)
    decision = _decision(state.vetoes)
    must_surface = _must_surface(state)
    action = descriptor["action"]
    result = {
        "schema_version": SCHEMA_VERSION,
        "task_id": descriptor["task_id"],
        "checkpoint": descriptor["checkpoint"],
        "decision": decision,
        "selected_skills": selected_skills,
        "decision_domain_owners": dict(sorted(state.owners.items())),
        "typed_gates": state.gates,
        "permissions": permissions,
        "artifact_allowance": artifacts,
        "must_surface": must_surface,
        "vetoes": state.vetoes,
        "excluded_routes": state.excluded,
        "route_trace": [
            {
                "stage": "descriptor",
                "outcome": "typed task descriptor accepted",
                "evidence": [
                    f"action.primary={action['primary']}",
                    f"execution_mode={action['execution_mode']}",
                    f"command_effect={action['command_effect']}",
                    f"checkpoint={descriptor['checkpoint']}",
                ],
            },
            {
                "stage": "intent_routing",
                "outcome": f"catalog selected {len(selected_skills)} skill(s)",
                "evidence": [
                    f"operations={','.join(action['operations'])}",
                    f"flags={','.join(sorted(flags))}",
                    "source=skills/skill-catalog.json",
                    *state.compatibility_traces,
                ],
            },
            {
                "stage": "safety_kernel",
                "outcome": f"{len(state.vetoes)} veto(es); decision={decision}",
                "evidence": [
                    f"read_only={str(descriptor['constraints']['read_only']).lower()}",
                    f"data_loss_risk={descriptor['mutation']['data_loss_risk']}",
                    f"recovery_requirement={descriptor['mutation']['recovery_requirement']}",
                ],
            },
            {
                "stage": "skill_budget",
                "outcome": "routine optional budget applied; mandatory safety retained",
                "evidence": [
                    f"optional_before={budget['optional_before_budget']}",
                    f"optional_after={budget['optional_after_budget']}",
                    "mandatory_safety_exempt=true",
                ],
            },
            {
                "stage": "result",
                "outcome": decision,
                "evidence": [
                    f"artifact_allowed={str(artifacts['allowed']).lower()}",
                    f"must_surface={len(must_surface)}",
                ],
            },
        ],
        "skill_budget": budget,
    }
    validate_routing_result(result, contract)
    return result


def _gate_statuses(result: Mapping[str, Any]) -> dict[str, str]:
    return {gate["id"]: gate["status"] for gate in result["typed_gates"]}


def _expectation_errors(scenario: Mapping[str, Any], result: Mapping[str, Any]) -> list[str]:
    expected = scenario["expected"]
    errors: list[str] = []
    for field_name, actual in {
        "decision": result["decision"],
        "artifact_allowed": result["artifact_allowance"]["allowed"],
    }.items():
        if field_name in expected and expected[field_name] != actual:
            errors.append(f"{field_name}: expected {expected[field_name]!r}, got {actual!r}")
    for field_name, actual in {
        "selected_skills": result["selected_skills"],
        "permissions": result["permissions"],
        "gate_statuses": _gate_statuses(result),
        "veto_codes": [veto["code"] for veto in result["vetoes"]],
        "excluded_routes": [route["route"] for route in result["excluded_routes"]],
    }.items():
        if field_name in expected and expected[field_name] != actual:
            errors.append(f"{field_name}: expected {expected[field_name]!r}, got {actual!r}")
    if "max_selected_skills" in expected and len(result["selected_skills"]) > expected["max_selected_skills"]:
        errors.append(
            f"selected skill count {len(result['selected_skills'])} exceeds {expected['max_selected_skills']}"
        )
    return errors


def _validate_fixture_contract(fixture: Mapping[str, Any]) -> None:
    unknown_root_fields = sorted(set(fixture) - FIXTURE_ROOT_FIELDS)
    if unknown_root_fields:
        raise DescriptorError(
            "fixture file contains unknown fields: " + ", ".join(unknown_root_fields)
        )

    scenarios = fixture.get("scenarios")
    defaults = fixture.get("descriptor_defaults")
    if not isinstance(defaults, dict) or not isinstance(scenarios, list) or not scenarios:
        raise DescriptorError("fixture file requires descriptor_defaults and non-empty scenarios")

    scenario_ids: set[str] = set()
    for index, scenario in enumerate(scenarios):
        label = f"fixture scenario at index {index}"
        if not isinstance(scenario, dict):
            raise DescriptorError(f"{label} must be an object")
        unknown_scenario_fields = sorted(set(scenario) - FIXTURE_SCENARIO_FIELDS)
        missing_scenario_fields = sorted(FIXTURE_SCENARIO_FIELDS - set(scenario))
        if unknown_scenario_fields:
            raise DescriptorError(
                f"{label} contains unknown fields: " + ", ".join(unknown_scenario_fields)
            )
        if missing_scenario_fields:
            raise DescriptorError(
                f"{label} is missing required fields: " + ", ".join(missing_scenario_fields)
            )

        scenario_id = scenario["id"]
        if not isinstance(scenario_id, str) or not scenario_id.strip():
            raise DescriptorError(f"{label} id must be a non-empty string")
        if scenario_id in scenario_ids:
            raise DescriptorError(f"fixture scenario id is duplicated: {scenario_id}")
        scenario_ids.add(scenario_id)
        if not isinstance(scenario["description"], str) or not scenario["description"].strip():
            raise DescriptorError(f"fixture scenario {scenario_id!r} description must be non-empty")
        if not isinstance(scenario["descriptor"], dict):
            raise DescriptorError(f"fixture scenario {scenario_id!r} descriptor must be an object")

        expected = scenario["expected"]
        if not isinstance(expected, dict) or not expected:
            raise DescriptorError(
                f"fixture scenario {scenario_id!r} expected must be a non-empty object"
            )
        unknown_expectations = sorted(set(expected) - FIXTURE_EXPECTATION_FIELDS)
        if unknown_expectations:
            raise DescriptorError(
                f"fixture scenario {scenario_id!r} contains unknown expectation fields: "
                + ", ".join(unknown_expectations)
            )
        if "decision" in expected and expected["decision"] not in {
            "allow",
            "needs_clarification",
            "blocked",
        }:
            raise DescriptorError(
                f"fixture scenario {scenario_id!r} expected.decision is invalid"
            )
        if "artifact_allowed" in expected and not isinstance(
            expected["artifact_allowed"], bool
        ):
            raise DescriptorError(
                f"fixture scenario {scenario_id!r} expected.artifact_allowed must be boolean"
            )
        if "max_selected_skills" in expected:
            limit = expected["max_selected_skills"]
            if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
                raise DescriptorError(
                    f"fixture scenario {scenario_id!r} expected.max_selected_skills "
                    "must be a non-negative integer"
                )
        for field_name in ("selected_skills", "veto_codes", "excluded_routes"):
            if field_name not in expected:
                continue
            values = expected[field_name]
            if not isinstance(values, list) or not all(
                isinstance(value, str) for value in values
            ):
                raise DescriptorError(
                    f"fixture scenario {scenario_id!r} expected.{field_name} "
                    "must be a string array"
                )
        for field_name in ("permissions", "gate_statuses"):
            if field_name in expected and not isinstance(expected[field_name], dict):
                raise DescriptorError(
                    f"fixture scenario {scenario_id!r} expected.{field_name} must be an object"
                )
        if "same_route_as" in expected and (
            not isinstance(expected["same_route_as"], str)
            or not expected["same_route_as"].strip()
        ):
            raise DescriptorError(
                f"fixture scenario {scenario_id!r} expected.same_route_as "
                "must be a non-empty scenario id"
            )

    for scenario in scenarios:
        scenario_id = scenario["id"]
        comparison_id = scenario["expected"].get("same_route_as")
        if comparison_id is None:
            continue
        if comparison_id == scenario_id:
            raise DescriptorError(
                f"fixture scenario {scenario_id!r} cannot compare its route to itself"
            )
        if comparison_id not in scenario_ids:
            raise DescriptorError(
                f"fixture scenario {scenario_id!r} references unknown comparison target: "
                f"{comparison_id}"
            )


def _deep_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = copy.deepcopy(dict(base))
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def evaluate_fixture_file(
    path: Path,
    *,
    catalog_path: Path | None = None,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    fixture = _read_json(path)
    if not isinstance(fixture, dict) or fixture.get("schema_version") != SCHEMA_VERSION:
        raise DescriptorError(f"fixture file must use schema_version {SCHEMA_VERSION!r}")
    _validate_fixture_contract(fixture)
    scenarios = fixture["scenarios"]
    defaults = fixture["descriptor_defaults"]
    contract = (
        DEFAULT_CATALOG_CONTRACT
        if catalog_path is None and repo_root.resolve() == REPO_ROOT.resolve()
        else load_catalog_contract(catalog_path or CATALOG_PATH, repo_root=repo_root)
    )
    results: dict[str, Mapping[str, Any]] = {}
    failures: list[dict[str, Any]] = []
    for scenario in scenarios:
        scenario_id = scenario.get("id", "<missing>")
        try:
            result = resolve_task_route(
                _deep_merge(defaults, scenario["descriptor"]),
                contract=contract,
            )
            results[scenario_id] = result
            errors = _expectation_errors(scenario, result)
        except (DescriptorError, KeyError, TypeError) as exc:
            errors = [str(exc)]
        if errors:
            failures.append({"id": scenario_id, "errors": errors})
    for scenario in scenarios:
        comparison_id = scenario.get("expected", {}).get("same_route_as")
        if not comparison_id or scenario["id"] not in results or comparison_id not in results:
            continue
        left, right = results[scenario["id"]], results[comparison_id]
        fields = ("decision", "selected_skills", "permissions", "artifact_allowance", "vetoes")
        unequal = [field for field in fields if left[field] != right[field]]
        if unequal:
            failures.append(
                {
                    "id": scenario["id"],
                    "errors": [f"route differs from {comparison_id!r}: {', '.join(unequal)}"],
                }
            )
    failed_ids = {failure["id"] for failure in failures}
    return {
        "schema_version": SCHEMA_VERSION,
        "fixture": str(path),
        "scenario_count": len(scenarios),
        "passed": len(scenarios) - len(failed_ids),
        "failed": len(failed_ids),
        "failures": failures,
    }


def _write_or_print(payload: Mapping[str, Any], output: Path | None, pretty: bool) -> None:
    rendered = json.dumps(payload, indent=2 if pretty else None, sort_keys=True) + "\n"
    if output is None:
        sys.stdout.write(rendered)
    else:
        output.write_text(rendered, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--descriptor", type=Path, help="Task descriptor JSON to resolve")
    source.add_argument("--fixtures", type=Path, help="Scenario fixture JSON to evaluate")
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--output", type=Path, help="Write JSON output to this path")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.descriptor is not None:
            payload = resolve_task_route(
                _read_json(args.descriptor), catalog_path=args.catalog, repo_root=args.repo_root
            )
            exit_code = 0
        else:
            payload = evaluate_fixture_file(
                args.fixtures, catalog_path=args.catalog, repo_root=args.repo_root
            )
            exit_code = 0 if payload["failed"] == 0 else 1
        _write_or_print(payload, args.output, args.pretty)
        return exit_code
    except DescriptorError as exc:
        print(f"route resolution failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
