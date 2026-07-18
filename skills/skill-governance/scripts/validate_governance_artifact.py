#!/usr/bin/env python3
"""Validate governance artifact readiness and exit non-zero on blocking issues."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_DIR = SCRIPT_PATH.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from governance_common import (  # noqa: E402
    COMMIT_SHA_RE,
    SCHEMA_V1,
    SCHEMA_V2,
    SCHEMA_V3,
    SHA256_RE,
    SUPPORTED_SCHEMA_VERSIONS,
    manifest_sha256,
    normalize_repo_path,
    validate_manifest_shape,
    validate_task_id,
)
from generate_governance_artifact import (  # noqa: E402
    AUTHORIZED_OPERATIONS,
    CRITICAL_OVERRIDES,
    RECOVERY_REQUIRED_OPERATIONS,
    SCORE_KEYS,
    SEMVER_REGEX,
    apply_profile_modifier,
    base_mode_from_total,
    build_evidence_requirements,
    build_required_gates,
    manifest_requires_documentation,
    operations_force_critical,
)


PASS_STATES = {"pass", "waived"}
VALID_STATES = {"pending", "pass", "fail", "waived"}
VALID_RECOMMENDATIONS = {"go", "go-with-risk", "no-go"}
SCHEMA_PATH = SCRIPT_PATH.parents[1] / "schemas" / "governance-artifact.schema.json"
NON_WAIVABLE_V3_GATES = {"governance-enforcement", "project-backup", "restore-drill"}
PLACEHOLDER_EVIDENCE = {"evidence", "passed", "pass", "done", "okay", "unknown", "n/a"}
GATE_EVIDENCE_KINDS = {
    "scripted-command-execution": {"attestation", "command", "test"},
    "pseudo-agentic-automation": {"artifact", "attestation", "test"},
    "regression-prevention": {"attestation", "command", "test"},
    "semantic-policy-audit": {"artifact", "attestation", "review"},
    "governance-enforcement": {"attestation", "command", "test"},
    "doc-maintenance": {"artifact", "attestation", "review"},
    "project-backup": {"artifact", "attestation"},
    "restore-drill": {"artifact", "attestation", "test"},
}
V3_FIELDS = {
    "schema_version",
    "task_id",
    "purpose",
    "authorized_operations",
    "release_metadata",
    "project_id",
    "created_at_utc",
    "profile",
    "project_language",
    "project_description_max4",
    "model_runs_test_build_default",
    "execution_scope",
    "deployment_requested",
    "execution_skill",
    "behavior_or_workflow_changed",
    "uncertainty_high",
    "requires_backup",
    "requires_restore",
    "quizme_mode",
    "quizme_multiple_choice",
    "quizme_one_at_a_time",
    "quizme_confirm",
    "quizme_record",
    "scores",
    "total_score",
    "base_mode",
    "mode_after_profile",
    "selected_mode",
    "critical_overrides",
    "required_gates",
    "gate_status",
    "startup_declaration",
    "evidence_requirements",
    "break_glass",
    "recommendation",
    "change_binding",
    "notes",
    "catalog_binding",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", required=True, help="Path to *.governance.json artifact.")
    parser.add_argument(
        "--project-index-path",
        default="docs/project-index.md",
        help=(
            "Accepted for CLI compatibility. Artifacts are immutable snapshots and are not "
            "compared with mutable current project-index metadata."
        ),
    )
    parser.add_argument("--strict", action="store_true", help="Require all required gates to be pass/waived.")
    parser.add_argument(
        "--require-recommendation",
        choices=["go", "go-with-risk", "no-go"],
        default="no-go",
        help="Minimum acceptable release recommendation.",
    )
    return parser.parse_args()


def recommendation_rank(value: str) -> int:
    return {"no-go": 0, "go-with-risk": 1, "go": 2}[value]


def parse_utcish(value: str) -> datetime | None:
    text = str(value).strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def artifact_schema_version(data: dict[str, Any]) -> int:
    raw_value = data.get("schema_version", SCHEMA_V1)
    if isinstance(raw_value, bool) or not isinstance(raw_value, int):
        return -1
    return raw_value


def _json_schema_errors(data: dict[str, Any]) -> list[str]:
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError:
        return [
            "jsonschema is required for governance artifact structural validation; "
            "install the pinned governance requirements"
        ]
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"unable to load governance artifact schema: {exc}"]
    format_checker = FormatChecker()
    if "date-time" not in format_checker.checkers:
        return [
            "rfc3339-validator is required for governance artifact date-time format checks; "
            "install the pinned governance requirements"
        ]
    validator = Draft202012Validator(schema, format_checker=format_checker)
    errors: list[str] = []
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path)):
        location = ".".join(map(str, error.absolute_path)) or "$"
        errors.append(f"schema {location}: {error.message}")
    return errors


def concrete_waiver_reason(value: Any) -> bool:
    text = str(value).strip()
    return len(text) >= 12 and len(text.split()) >= 3


def _validate_common_fields(data: dict[str, Any], schema_version: int, errors: list[str]) -> None:
    required_fields = [
        "task_id",
        "created_at_utc",
        "project_id",
        "project_language",
        "project_description_max4",
        "model_runs_test_build_default",
        "execution_scope",
        "deployment_requested",
        "quizme_mode",
        "quizme_multiple_choice",
        "quizme_one_at_a_time",
        "quizme_confirm",
        "quizme_record",
        "selected_mode",
        "required_gates",
        "gate_status",
        "startup_declaration",
        "recommendation",
        "break_glass",
    ]
    if schema_version in {SCHEMA_V2, SCHEMA_V3}:
        required_fields.extend(("schema_version", "change_binding"))
    if schema_version == SCHEMA_V3:
        required_fields.extend(sorted(V3_FIELDS - set(required_fields)))
    for field in required_fields:
        if field not in data:
            errors.append(f"missing required field: {field}")


def _validate_project_snapshot(data: dict[str, Any], errors: list[str]) -> None:
    try:
        validate_task_id(data.get("task_id", ""))
    except SystemExit as exc:
        errors.append(f"invalid task_id: {exc}")

    project_id = str(data.get("project_id", "")).strip()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,63}", project_id):
        errors.append(
            "project_id must match [a-z0-9][a-z0-9-]{1,63} "
            "(2-64 chars, lowercase letters/digits/hyphens)"
        )
    if not str(data.get("project_language", "")).strip():
        errors.append("project_language is required and cannot be empty")
    description = str(data.get("project_description_max4", "")).strip()
    if not description:
        errors.append("project_description_max4 is required and cannot be empty")
    elif len(description.split()) > 4:
        errors.append("project_description_max4 must be 4 words or fewer")
    if data.get("model_runs_test_build_default") not in {"yes", "no"}:
        errors.append("model_runs_test_build_default must be 'yes' or 'no'")
    if parse_utcish(str(data.get("created_at_utc", ""))) is None:
        errors.append("created_at_utc must be a valid ISO-8601 timestamp")


def _validate_execution_and_quizme(data: dict[str, Any], errors: list[str]) -> None:
    execution_scope = data.get("execution_scope")
    deployment_requested = data.get("deployment_requested")
    if execution_scope not in {"local_only", "external", "deployment"}:
        errors.append("execution_scope must be 'local_only', 'external', or 'deployment'")
    if not isinstance(deployment_requested, bool):
        errors.append("deployment_requested must be a boolean")
    elif execution_scope == "deployment" and not deployment_requested:
        errors.append("execution_scope=deployment requires deployment_requested=true")
    elif execution_scope != "deployment" and deployment_requested:
        errors.append("deployment_requested=true requires execution_scope=deployment")

    quizme_mode = data.get("quizme_mode")
    if quizme_mode not in {"off", "on"}:
        errors.append("quizme_mode must be 'off' or 'on'")
    quizme_options = {
        "quizme_multiple_choice": data.get("quizme_multiple_choice"),
        "quizme_one_at_a_time": data.get("quizme_one_at_a_time"),
        "quizme_confirm": data.get("quizme_confirm"),
        "quizme_record": data.get("quizme_record"),
    }
    for field, value in quizme_options.items():
        if not isinstance(value, bool):
            errors.append(f"{field} must be a boolean")
    if any(value is True for value in quizme_options.values()) and quizme_mode != "on":
        errors.append("quizme options require quizme_mode=on")
    if data.get("quizme_record") is True and data.get("quizme_confirm") is not True:
        errors.append("quizme_record=true requires quizme_confirm=true")


def _validate_startup_declaration(data: dict[str, Any], errors: list[str]) -> None:
    startup = data.get("startup_declaration")
    required_gates = data.get("required_gates")
    if not isinstance(startup, dict):
        errors.append("startup_declaration must be an object")
        return
    for field in ("skills_in_use", "skills_selection_rationale", "skills_execution_order"):
        if field not in startup:
            errors.append(f"startup_declaration missing required field: {field}")

    skills_in_use = startup.get("skills_in_use")
    execution_order = startup.get("skills_execution_order")
    rationale = startup.get("skills_selection_rationale")
    if not isinstance(skills_in_use, list) or not skills_in_use:
        errors.append("startup_declaration.skills_in_use must be a non-empty list")
    if not isinstance(execution_order, list) or not execution_order:
        errors.append("startup_declaration.skills_execution_order must be a non-empty list")
    if not str(rationale or "").strip():
        errors.append("startup_declaration.skills_selection_rationale must be non-empty")
    if not isinstance(skills_in_use, list) or not isinstance(execution_order, list):
        return

    missing_from_use = [skill for skill in execution_order if skill not in skills_in_use]
    if missing_from_use:
        errors.append(
            "startup_declaration.skills_execution_order contains skills not present in skills_in_use: "
            + ", ".join(map(str, missing_from_use))
        )
    if isinstance(required_gates, list):
        missing_gates = [gate for gate in required_gates if gate not in skills_in_use]
        if missing_gates:
            errors.append(
                "startup_declaration.skills_in_use missing required gates: "
                + ", ".join(map(str, missing_gates))
            )
    if data.get("quizme_mode") == "on" and "quizme-mode" not in skills_in_use:
        errors.append("startup_declaration.skills_in_use missing quizme-mode while quizme_mode=on")


def _validate_required_gates(data: dict[str, Any], errors: list[str]) -> tuple[list[str], dict[str, Any]]:
    required_gates = data.get("required_gates")
    gate_status = data.get("gate_status")
    if not isinstance(required_gates, list) or not required_gates:
        errors.append("required_gates must be a non-empty list")
        return [], gate_status if isinstance(gate_status, dict) else {}
    if any(not isinstance(gate, str) or not gate.strip() for gate in required_gates):
        errors.append("required_gates must contain non-empty strings")
    if len(required_gates) != len(set(map(str, required_gates))):
        errors.append("required_gates must not contain duplicates")
    if not isinstance(gate_status, dict):
        errors.append("gate_status must be an object")
        return required_gates, {}
    return required_gates, gate_status


def _validate_v1_gates(
    required_gates: list[str],
    gate_status: dict[str, Any],
    *,
    strict: bool,
    errors: list[str],
    warnings: list[str],
) -> tuple[list[str], list[str], list[str]]:
    for gate in required_gates:
        if gate not in gate_status:
            errors.append(f"gate status missing for required gate: {gate}")
            continue
        status = gate_status[gate]
        if status not in VALID_STATES:
            errors.append(f"invalid gate status '{status}' for gate '{gate}'")
    failed = [gate for gate in required_gates if gate_status.get(gate) == "fail"]
    pending = [gate for gate in required_gates if gate_status.get(gate) == "pending"]
    waived = [gate for gate in required_gates if gate_status.get(gate) == "waived"]
    if strict:
        for gate in required_gates:
            if gate_status.get(gate) not in PASS_STATES:
                errors.append(f"strict mode: gate not complete: {gate}={gate_status.get(gate)}")
    else:
        if failed:
            errors.append(f"one or more required gates failed: {', '.join(failed)}")
        if pending:
            warnings.append(f"pending required gates: {', '.join(pending)}")
    return failed, pending, waived


def _validate_content_bound_gates(
    required_gates: list[str],
    gate_status: dict[str, Any],
    *,
    strict: bool,
    errors: list[str],
    warnings: list[str],
    schema_version: int,
) -> tuple[list[str], list[str], list[str]]:
    states: dict[str, str | None] = {}
    for gate in required_gates:
        record = gate_status.get(gate)
        if record is None:
            errors.append(f"gate status missing for required gate: {gate}")
            continue
        if not isinstance(record, dict):
            errors.append(f"content-bound gate '{gate}' must be an object")
            continue
        for field in ("status", "evidence", "waiver_reason"):
            if field not in record:
                errors.append(f"content-bound gate '{gate}' missing field: {field}")
        status = record.get("status")
        states[gate] = status if isinstance(status, str) else None
        if status not in VALID_STATES:
            errors.append(f"invalid gate status '{status}' for gate '{gate}'")
        evidence = record.get("evidence")
        if schema_version == SCHEMA_V3:
            if not isinstance(evidence, list):
                errors.append(f"schema v3 gate '{gate}'.evidence must be a list")
                evidence = []
            for index, item in enumerate(evidence):
                if not isinstance(item, dict):
                    errors.append(
                        f"schema v3 gate '{gate}'.evidence[{index}] must be an object"
                    )
                    continue
                kind = item.get("kind")
                allowed_kinds = GATE_EVIDENCE_KINDS.get(gate)
                if allowed_kinds is not None and kind not in allowed_kinds:
                    errors.append(
                        f"schema v3 gate '{gate}' does not accept evidence kind {kind!r}"
                    )
                reference = item.get("reference")
                if (
                    not isinstance(reference, str)
                    or len(reference.strip()) < 8
                    or reference.strip().lower() in PLACEHOLDER_EVIDENCE
                ):
                    errors.append(
                        f"schema v3 gate '{gate}' requires a concrete evidence reference"
                    )
                if item.get("result") != "pass":
                    errors.append(f"schema v3 gate '{gate}' evidence result must be pass")
                observed = item.get("observed_at_utc")
                parsed_observed = parse_utcish(observed) if isinstance(observed, str) else None
                if parsed_observed is None or parsed_observed.utcoffset() is None:
                    errors.append(
                        f"schema v3 gate '{gate}' evidence timestamp must include a timezone"
                    )
                revision = item.get("revision_sha")
                digest = item.get("sha256")
                if revision is not None and (
                    not isinstance(revision, str) or not COMMIT_SHA_RE.fullmatch(revision)
                ):
                    errors.append(f"schema v3 gate '{gate}' evidence revision_sha is invalid")
                if digest is not None and (
                    not isinstance(digest, str) or not SHA256_RE.fullmatch(digest)
                ):
                    errors.append(f"schema v3 gate '{gate}' evidence sha256 is invalid")
                if revision is None and digest is None:
                    errors.append(
                        f"schema v3 gate '{gate}' evidence requires revision_sha or sha256"
                    )
        else:
            if not isinstance(evidence, list) or any(
                not isinstance(item, str) or not item.strip() for item in evidence
            ):
                errors.append(
                    f"content-bound gate '{gate}'.evidence must be a list of non-empty strings"
                )
                evidence = []
        if status == "pass" and not evidence:
            errors.append(f"content-bound gate '{gate}' requires evidence when status=pass")
        if status == "waived" and not concrete_waiver_reason(record.get("waiver_reason")):
            errors.append(
                f"content-bound gate '{gate}' requires a concrete waiver_reason "
                "(at least 12 characters and 3 words)"
            )
        if status != "waived" and str(record.get("waiver_reason", "")).strip():
            errors.append(
                f"content-bound gate '{gate}' has waiver_reason but status is not waived"
            )

    failed = [gate for gate in required_gates if states.get(gate) == "fail"]
    pending = [gate for gate in required_gates if states.get(gate) == "pending"]
    waived = [gate for gate in required_gates if states.get(gate) == "waived"]
    if strict:
        for gate in required_gates:
            if states.get(gate) not in PASS_STATES:
                errors.append(f"strict mode: gate not complete: {gate}={states.get(gate)}")
    elif pending:
        warnings.append(f"pending required gates: {', '.join(pending)}")
    return failed, pending, waived


def _validate_change_binding(data: dict[str, Any], errors: list[str]) -> None:
    binding = data.get("change_binding")
    if not isinstance(binding, dict):
        errors.append("content-bound change_binding must be an object")
        return
    for field in ("base_sha", "manifest", "manifest_sha256"):
        if field not in binding:
            errors.append(f"change_binding missing required field: {field}")
    base_sha = binding.get("base_sha")
    if not isinstance(base_sha, str) or not COMMIT_SHA_RE.fullmatch(base_sha):
        errors.append("change_binding.base_sha must be an exact lowercase commit SHA")
    manifest = binding.get("manifest")
    errors.extend(validate_manifest_shape(manifest))
    if isinstance(manifest, list):
        expected_digest = manifest_sha256(manifest)
        if binding.get("manifest_sha256") != expected_digest:
            errors.append(
                "change_binding.manifest_sha256 does not match the canonical manifest digest"
            )


def _validate_v3_startup_and_catalog_binding(data: dict[str, Any], errors: list[str]) -> None:
    startup = data.get("startup_declaration")
    if not isinstance(startup, dict):
        return
    skills_in_use = startup.get("skills_in_use")
    execution_order = startup.get("skills_execution_order")
    if not isinstance(skills_in_use, list) or not isinstance(execution_order, list):
        return
    if len(skills_in_use) != len(set(map(str, skills_in_use))):
        errors.append("schema v3 startup skills_in_use must not contain duplicates")
    if len(execution_order) != len(set(map(str, execution_order))):
        errors.append("schema v3 startup skills_execution_order must not contain duplicates")
    if set(map(str, skills_in_use)) != set(map(str, execution_order)):
        errors.append("schema v3 startup skills lists must be exact permutations")

    binding = data.get("catalog_binding")
    if not isinstance(binding, dict):
        errors.append("schema v3 catalog_binding must be an object")
        return
    try:
        normalize_repo_path(str(binding.get("path", "")))
    except SystemExit as exc:
        errors.append(f"schema v3 catalog_binding.path is invalid: {exc}")
    catalog = binding.get("skills")
    components_raw = binding.get("components")
    if not isinstance(catalog, dict) or not isinstance(components_raw, list):
        return
    components = set(map(str, components_raw))
    bound_names = set(map(str, catalog))
    selected_names = set(map(str, skills_in_use))
    if bound_names != selected_names:
        errors.append("schema v3 catalog binding skills must exactly match startup skills")
    unknown = sorted(selected_names - bound_names)
    if unknown:
        errors.append("schema v3 startup uses skills absent from catalog binding: " + ", ".join(unknown))
    inactive = sorted(
        name
        for name in selected_names.intersection(bound_names)
        if not isinstance(catalog.get(name), dict) or catalog[name].get("status") != "active"
    )
    if inactive:
        errors.append("schema v3 startup uses non-active skills: " + ", ".join(inactive))

    execution_skill = data.get("execution_skill")
    mandatory = {"skill-governance", str(execution_skill)}
    missing = sorted(mandatory - set(map(str, skills_in_use)))
    if missing:
        errors.append("schema v3 startup missing mandatory skills: " + ", ".join(missing))

    positions = {str(name): index for index, name in enumerate(execution_order)}
    selected = set(positions)
    for name in sorted(selected.intersection(bound_names)):
        relations = catalog[name]
        required = {
            target
            for target in map(str, relations.get("requires", []))
            if target not in components
        }
        missing_required = sorted(required - selected)
        if missing_required:
            errors.append(
                f"schema v3 startup skill {name} is missing prerequisites: "
                + ", ".join(missing_required)
            )
        predecessors = required | set(map(str, relations.get("runs_after", []))).intersection(selected)
        for predecessor in sorted(predecessors.intersection(positions)):
            if positions[predecessor] > positions[name]:
                errors.append(
                    f"schema v3 startup order places {name} before predecessor {predecessor}"
                )
        conflicts = set(map(str, relations.get("conflicts_with", []))).intersection(selected)
        if conflicts:
            errors.append(
                f"schema v3 startup skill {name} conflicts with: "
                + ", ".join(sorted(conflicts))
            )


def _validate_v3_contract(data: dict[str, Any], errors: list[str]) -> None:
    unknown_fields = sorted(set(data) - V3_FIELDS)
    if unknown_fields:
        errors.append("schema v3 contains unknown fields: " + ", ".join(unknown_fields))

    timestamp = parse_utcish(str(data.get("created_at_utc", "")))
    if timestamp is not None and timestamp.utcoffset() is None:
        errors.append("schema v3 created_at_utc must include a timezone offset")

    profile = data.get("profile")
    if profile not in {"prototype", "internal", "production"}:
        errors.append("schema v3 profile must be prototype, internal, or production")
    purpose = data.get("purpose")
    if purpose not in {"change", "release"}:
        errors.append("schema v3 purpose must be change or release")
    execution_skill = data.get("execution_skill")
    if execution_skill not in {"scripted-command-execution", "pseudo-agentic-automation"}:
        errors.append("schema v3 execution_skill is invalid")

    for field in (
        "behavior_or_workflow_changed",
        "uncertainty_high",
        "requires_backup",
        "requires_restore",
    ):
        if not isinstance(data.get(field), bool):
            errors.append(f"schema v3 {field} must be a boolean")

    authorized_operations = data.get("authorized_operations")
    if not isinstance(authorized_operations, list):
        errors.append("schema v3 authorized_operations must be a list")
        authorized_operations = []
    else:
        if len(authorized_operations) != len(set(map(str, authorized_operations))):
            errors.append("schema v3 authorized_operations must not contain duplicates")
        unknown_operations = sorted(set(map(str, authorized_operations)) - set(AUTHORIZED_OPERATIONS))
        if unknown_operations:
            errors.append(
                "schema v3 authorized_operations contains unknown values: "
                + ", ".join(unknown_operations)
            )
    scope = data.get("execution_scope")
    external_operations = set(map(str, authorized_operations)) - {"commit"}
    if external_operations and scope == "local_only":
        errors.append("schema v3 external authorized operations require non-local execution scope")
    if "deploy" in authorized_operations and scope != "deployment":
        errors.append("schema v3 authorized deploy requires deployment execution scope")
    recovery_operations = set(map(str, authorized_operations)).intersection(
        RECOVERY_REQUIRED_OPERATIONS
    )
    if purpose == "release":
        if "publish" not in authorized_operations:
            errors.append("schema v3 release purpose requires publish authority")
        if scope == "local_only":
            errors.append("schema v3 release purpose requires non-local execution scope")
    elif "publish" in authorized_operations:
        errors.append("schema v3 publish authority requires release purpose")

    release_metadata = data.get("release_metadata")
    if purpose == "change":
        if release_metadata is not None:
            errors.append("schema v3 change purpose requires release_metadata=null")
    elif purpose == "release":
        if not isinstance(release_metadata, dict):
            errors.append("schema v3 release purpose requires release_metadata")
        else:
            version = release_metadata.get("version")
            tag = release_metadata.get("tag")
            if not isinstance(version, str) or not SEMVER_REGEX.fullmatch(version):
                errors.append("schema v3 release_metadata.version is invalid")
            elif tag != f"v{version}":
                errors.append("schema v3 release_metadata.tag must equal v<version>")
            for field in ("version_path", "changelog_path", "release_notes_path"):
                value = release_metadata.get(field)
                if not isinstance(value, str):
                    errors.append(f"schema v3 release_metadata.{field} must be a string")
                    continue
                try:
                    normalize_repo_path(value)
                except SystemExit as exc:
                    errors.append(f"schema v3 release_metadata.{field} is invalid: {exc}")
            for field in ("skill_count", "governance_test_count"):
                value = release_metadata.get(field)
                if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                    errors.append(f"schema v3 release_metadata.{field} must be a positive integer")

    requires_backup = data.get("requires_backup") is True
    requires_restore = data.get("requires_restore") is True
    if requires_restore and not requires_backup:
        errors.append("schema v3 requires_restore=true requires requires_backup=true")
    if (requires_backup or requires_restore) and scope == "local_only":
        errors.append("schema v3 recovery controls require external or deployment scope")
    if recovery_operations and not (requires_backup and requires_restore):
        errors.append(
            "schema v3 authorized delete or migrate requires backup and restore controls"
        )

    scores = data.get("scores")
    total = data.get("total_score")
    valid_scores = isinstance(scores, dict) and set(scores) == set(SCORE_KEYS)
    if not valid_scores:
        errors.append("schema v3 scores must contain exactly the five governed score keys")
        scores = {}
    else:
        for key in SCORE_KEYS:
            value = scores[key]
            if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 3:
                errors.append(f"schema v3 score {key} must be an integer from 0 through 3")
                valid_scores = False
    if isinstance(total, bool) or not isinstance(total, int):
        errors.append("schema v3 total_score must be an integer")
        valid_scores = False
    elif valid_scores and total != sum(scores[key] for key in SCORE_KEYS):
        errors.append("schema v3 total_score does not equal the score sum")

    overrides = data.get("critical_overrides")
    if not isinstance(overrides, list):
        errors.append("schema v3 critical_overrides must be a list")
        overrides = []
    else:
        if len(overrides) != len(set(map(str, overrides))):
            errors.append("schema v3 critical_overrides must not contain duplicates")
        unknown_overrides = sorted(set(map(str, overrides)) - set(CRITICAL_OVERRIDES))
        if unknown_overrides:
            errors.append(
                "schema v3 critical_overrides contains unknown values: "
                + ", ".join(unknown_overrides)
            )

    if valid_scores and profile in {"prototype", "internal", "production"}:
        expected_base = base_mode_from_total(total)
        forced_critical = (
            bool(overrides)
            or purpose == "release"
            or operations_force_critical(list(map(str, authorized_operations)))
        )
        expected_after_profile = (
            expected_base
            if forced_critical
            else apply_profile_modifier(
                expected_base,
                profile,
                total,
                data.get("uncertainty_high") is True,
            )
        )
        expected_selected = "critical" if forced_critical else expected_after_profile
        if data.get("base_mode") != expected_base:
            errors.append("schema v3 base_mode does not match total_score")
        if data.get("mode_after_profile") != expected_after_profile:
            errors.append("schema v3 mode_after_profile does not match profile policy")
        if data.get("selected_mode") != expected_selected:
            errors.append("schema v3 selected_mode does not match scores, purpose, and overrides")

        if execution_skill in {"scripted-command-execution", "pseudo-agentic-automation"}:
            expected_gates = build_required_gates(
                expected_selected,
                execution_skill,
                data.get("behavior_or_workflow_changed") is True,
                requires_backup,
                requires_restore,
            )
            if data.get("required_gates") != expected_gates:
                errors.append(
                    "schema v3 required_gates do not match deterministic policy; "
                    f"expected={expected_gates!r}"
                )
            expected_evidence = build_evidence_requirements(
                expected_selected,
                requires_backup,
                requires_restore,
                list(map(str, authorized_operations)),
            )
            if data.get("evidence_requirements") != expected_evidence:
                errors.append(
                    "schema v3 evidence_requirements do not match deterministic policy; "
                    f"expected={expected_evidence!r}"
                )

    required_gates = data.get("required_gates")
    gate_status = data.get("gate_status")
    if isinstance(required_gates, list) and isinstance(gate_status, dict):
        extra_statuses = sorted(set(gate_status) - set(map(str, required_gates)))
        if extra_statuses:
            errors.append("schema v3 has status for non-required gates: " + ", ".join(extra_statuses))

    if not isinstance(data.get("notes"), str):
        errors.append("schema v3 notes must be a string")
    binding = data.get("change_binding")
    manifest = binding.get("manifest") if isinstance(binding, dict) else None
    if (
        isinstance(manifest, list)
        and manifest_requires_documentation(manifest)
        and data.get("behavior_or_workflow_changed") is not True
    ):
        errors.append(
            "schema v3 behavior_or_workflow_changed must be true for changed behavior/workflow paths"
        )
    if purpose == "release" and isinstance(release_metadata, dict) and isinstance(manifest, list):
        manifest_paths = {str(entry.get("path", "")) for entry in manifest}
        required_paths = {
            str(release_metadata.get("version_path", "")),
            str(release_metadata.get("changelog_path", "")),
            str(release_metadata.get("release_notes_path", "")),
        }
        missing_paths = sorted(required_paths - manifest_paths)
        if missing_paths:
            errors.append(
                "schema v3 release metadata files are absent from the full manifest: "
                + ", ".join(missing_paths)
            )

    break_glass = data.get("break_glass")
    if isinstance(break_glass, dict):
        enabled = break_glass.get("enabled")
        if not isinstance(enabled, bool):
            errors.append("schema v3 break_glass.enabled must be a boolean")
        expiry = break_glass.get("expiry_hours")
        if enabled is True:
            if not concrete_waiver_reason(break_glass.get("reason")):
                errors.append("schema v3 enabled break glass requires a concrete reason")
            for field in ("risk_owner", "remediation_ticket"):
                value = break_glass.get(field)
                if not isinstance(value, str) or len(value.strip()) < 3:
                    errors.append(f"schema v3 enabled break glass requires concrete {field}")
            if isinstance(expiry, bool) or not isinstance(expiry, int) or not 1 <= expiry <= 168:
                errors.append("schema v3 break_glass.expiry_hours must be an integer from 1 through 168")
        elif enabled is False:
            if expiry is not None:
                errors.append("schema v3 disabled break glass requires expiry_hours=null")
            for field in ("reason", "risk_owner", "remediation_ticket"):
                if str(break_glass.get(field, "")).strip():
                    errors.append(f"schema v3 disabled break glass requires empty {field}")

    _validate_v3_startup_and_catalog_binding(data, errors)


def validate_artifact_data(
    data: Any,
    *,
    strict: bool,
    require_recommendation: str,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["artifact root must be a JSON object"], []

    schema_version = artifact_schema_version(data)
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        return [f"unsupported governance artifact schema_version: {data.get('schema_version')!r}"], []

    errors.extend(_json_schema_errors(data))

    error_count_before_common = len(errors)
    _validate_common_fields(data, schema_version, errors)
    if len(errors) > error_count_before_common:
        return errors, warnings

    _validate_project_snapshot(data, errors)
    _validate_execution_and_quizme(data, errors)
    _validate_startup_declaration(data, errors)
    required_gates, gate_status = _validate_required_gates(data, errors)
    if schema_version == SCHEMA_V3:
        _validate_v3_contract(data, errors)

    mode = data.get("selected_mode")
    if mode not in {"quick", "standard", "critical"}:
        errors.append("selected_mode must be quick, standard, or critical")
    recommendation = data.get("recommendation")
    if recommendation not in VALID_RECOMMENDATIONS:
        errors.append("recommendation must be go, go-with-risk, or no-go")

    if schema_version == SCHEMA_V1:
        failed, pending, waived = _validate_v1_gates(
            required_gates,
            gate_status,
            strict=strict,
            errors=errors,
            warnings=warnings,
        )
    else:
        failed, pending, waived = _validate_content_bound_gates(
            required_gates,
            gate_status,
            strict=strict,
            errors=errors,
            warnings=warnings,
            schema_version=schema_version,
        )
        _validate_change_binding(data, errors)
        if (failed or pending) and recommendation != "no-go":
            errors.append(
                "content-bound pending or failed required gates require recommendation=no-go"
            )
        if waived and recommendation == "go":
            errors.append("content-bound waived required gates cannot use recommendation=go")

    if recommendation in VALID_RECOMMENDATIONS and recommendation_rank(recommendation) < recommendation_rank(
        require_recommendation
    ):
        errors.append(
            f"recommendation '{recommendation}' is below required '{require_recommendation}'"
        )

    overrides = data.get("critical_overrides", [])
    if not isinstance(overrides, list):
        errors.append("critical_overrides must be a list")
        overrides = []
    if "missing_rollback_path" in overrides and recommendation != "no-go":
        errors.append("override missing_rollback_path requires recommendation no-go")

    break_glass = data.get("break_glass")
    if not isinstance(break_glass, dict):
        errors.append("break_glass must be an object")
        break_glass = {}
    if break_glass.get("enabled"):
        for field in ("reason", "risk_owner", "remediation_ticket", "expiry_hours"):
            if not break_glass.get(field):
                errors.append(f"break-glass enabled but missing field: {field}")
        if schema_version == SCHEMA_V2 and not (failed or pending) and recommendation != "go-with-risk":
            errors.append(
                "content-bound completed break-glass artifact requires recommendation=go-with-risk"
            )
        if schema_version == SCHEMA_V3 and recommendation == "go":
            errors.append("schema v3 break glass cannot support recommendation=go")

    if schema_version == SCHEMA_V3 and waived:
        if break_glass.get("enabled") is not True:
            errors.append("schema v3 waived gates require enabled break-glass accountability")
        non_waivable = sorted(set(waived).intersection(NON_WAIVABLE_V3_GATES))
        if non_waivable:
            errors.append(
                "schema v3 non-waivable gates cannot be waived: " + ", ".join(non_waivable)
            )

    if mode == "critical" and (strict or recommendation != "no-go"):
        for gate in ("project-backup", "restore-drill"):
            if gate not in required_gates:
                continue
            record = gate_status.get(gate)
            status = record.get("status") if isinstance(record, dict) else record
            if status not in PASS_STATES:
                errors.append(f"critical mode requires {gate}=pass/waived before go/no-go")

    return errors, warnings


def load_artifact(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Artifact is not valid JSON: {path}: {exc}") from exc
    except OSError as exc:
        raise SystemExit(f"Unable to read artifact: {path}: {exc}") from exc


def main() -> None:
    args = parse_args()
    path = Path(args.artifact)
    if not path.is_file():
        raise SystemExit(f"Artifact not found: {path}")
    data = load_artifact(path)
    errors, warnings = validate_artifact_data(
        data,
        strict=args.strict,
        require_recommendation=args.require_recommendation,
    )
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    schema_version = artifact_schema_version(data)
    print("Governance artifact validation passed.")
    print(f"Schema: v{schema_version}")
    print(f"Task: {data['task_id']}")
    print(f"Mode: {data['selected_mode']}")
    print(f"Recommendation: {data['recommendation']}")


if __name__ == "__main__":
    main()
