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
    SUPPORTED_SCHEMA_VERSIONS,
    manifest_sha256,
    validate_manifest_shape,
    validate_task_id,
)


PASS_STATES = {"pass", "waived"}
VALID_STATES = {"pending", "pass", "fail", "waived"}
VALID_RECOMMENDATIONS = {"go", "go-with-risk", "no-go"}


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
    if schema_version == SCHEMA_V2:
        required_fields.extend(("schema_version", "change_binding"))
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
    if execution_scope not in {"local_only", "deployment"}:
        errors.append("execution_scope must be 'local_only' or 'deployment'")
    if not isinstance(deployment_requested, bool):
        errors.append("deployment_requested must be a boolean")
    elif execution_scope == "deployment" and not deployment_requested:
        errors.append("execution_scope=deployment requires deployment_requested=true")
    elif execution_scope == "local_only" and deployment_requested:
        errors.append("deployment_requested=true is invalid when execution_scope=local_only")

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


def _validate_v2_gates(
    required_gates: list[str],
    gate_status: dict[str, Any],
    *,
    strict: bool,
    errors: list[str],
    warnings: list[str],
) -> tuple[list[str], list[str], list[str]]:
    states: dict[str, str | None] = {}
    for gate in required_gates:
        record = gate_status.get(gate)
        if record is None:
            errors.append(f"gate status missing for required gate: {gate}")
            continue
        if not isinstance(record, dict):
            errors.append(f"schema v2 gate '{gate}' must be an object")
            continue
        for field in ("status", "evidence", "waiver_reason"):
            if field not in record:
                errors.append(f"schema v2 gate '{gate}' missing field: {field}")
        status = record.get("status")
        states[gate] = status if isinstance(status, str) else None
        if status not in VALID_STATES:
            errors.append(f"invalid gate status '{status}' for gate '{gate}'")
        evidence = record.get("evidence")
        if not isinstance(evidence, list) or any(
            not isinstance(item, str) or not item.strip() for item in evidence
        ):
            errors.append(f"schema v2 gate '{gate}'.evidence must be a list of non-empty strings")
            evidence = []
        if status == "pass" and not evidence:
            errors.append(f"schema v2 gate '{gate}' requires evidence when status=pass")
        if status == "waived" and not concrete_waiver_reason(record.get("waiver_reason")):
            errors.append(
                f"schema v2 gate '{gate}' requires a concrete waiver_reason "
                "(at least 12 characters and 3 words)"
            )
        if status != "waived" and str(record.get("waiver_reason", "")).strip():
            errors.append(f"schema v2 gate '{gate}' has waiver_reason but status is not waived")

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
        errors.append("schema v2 change_binding must be an object")
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

    _validate_common_fields(data, schema_version, errors)
    if errors:
        return errors, warnings

    _validate_project_snapshot(data, errors)
    _validate_execution_and_quizme(data, errors)
    _validate_startup_declaration(data, errors)
    required_gates, gate_status = _validate_required_gates(data, errors)

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
        failed, pending, waived = _validate_v2_gates(
            required_gates,
            gate_status,
            strict=strict,
            errors=errors,
            warnings=warnings,
        )
        _validate_change_binding(data, errors)
        if (failed or pending) and recommendation != "no-go":
            errors.append("schema v2 pending or failed required gates require recommendation=no-go")
        if waived and recommendation == "go":
            errors.append("schema v2 waived required gates cannot use recommendation=go")

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
            errors.append("schema v2 completed break-glass artifact requires recommendation=go-with-risk")

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
