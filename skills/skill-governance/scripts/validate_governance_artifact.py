#!/usr/bin/env python3
"""Validate governance artifact readiness and exit non-zero on blocking issues."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


PASS_STATES = {"pass", "waived"}
VALID_STATES = {"pending", "pass", "fail", "waived"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", required=True, help="Path to *.governance.json artifact.")
    parser.add_argument(
        "--project-index-path",
        default="docs/project-index.md",
        help="Path to project intake index markdown file.",
    )
    parser.add_argument("--strict", action="store_true", help="Require all required gates to be pass/waived.")
    parser.add_argument(
        "--require-recommendation",
        choices=["go", "go-with-risk", "no-go"],
        default="go",
        help="Minimum acceptable release recommendation.",
    )
    return parser.parse_args()


def recommendation_rank(value: str) -> int:
    return {"no-go": 0, "go-with-risk": 1, "go": 2}[value]


def parse_index_line(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def load_project_index(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    entries: dict[str, dict[str, str]] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        cells = parse_index_line(line)
        if len(cells) != 5:
            continue
        if cells[0] in {"Project ID", "---"}:
            continue
        project_id = cells[0]
        if not project_id:
            continue
        entries[project_id] = {
            "language": cells[1],
            "description": cells[2],
            "model_default_test_build": cells[3],
            "last_confirmed_utc": cells[4],
        }
    return entries


def parse_utcish(value: str) -> datetime | None:
    text = str(value).strip()
    if not text:
        return None
    normalized = text.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def main() -> None:
    args = parse_args()
    path = Path(args.artifact)
    if not path.exists():
        raise SystemExit(f"Artifact not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []

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
    for field in required_fields:
        if field not in data:
            errors.append(f"missing required field: {field}")

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        raise SystemExit(1)

    required_gates = data["required_gates"]
    gate_status = data["gate_status"]
    mode = data["selected_mode"]
    recommendation = data["recommendation"]
    artifact_created_at_utc = str(data["created_at_utc"]).strip()
    project_id = str(data["project_id"]).strip()
    project_language = data["project_language"]
    project_description_max4 = data["project_description_max4"]
    model_runs_test_build_default = data["model_runs_test_build_default"]
    execution_scope = data["execution_scope"]
    deployment_requested = bool(data["deployment_requested"])
    quizme_mode = data["quizme_mode"]
    quizme_multiple_choice = data["quizme_multiple_choice"]
    quizme_one_at_a_time = data["quizme_one_at_a_time"]
    quizme_confirm = data["quizme_confirm"]
    quizme_record = data["quizme_record"]
    break_glass = data.get("break_glass", {})
    overrides = data.get("critical_overrides", [])
    startup_declaration = data.get("startup_declaration", {})

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,63}", project_id):
        errors.append(
            "project_id must match [a-z0-9][a-z0-9-]{1,63} (2-64 chars, lowercase letters/digits/hyphens)"
        )
    if not str(project_language).strip():
        errors.append("project_language is required and cannot be empty")
    if not str(project_description_max4).strip():
        errors.append("project_description_max4 is required and cannot be empty")
    if len(str(project_description_max4).strip().split()) > 4:
        errors.append("project_description_max4 must be 4 words or fewer")
    if model_runs_test_build_default not in {"yes", "no"}:
        errors.append("model_runs_test_build_default must be 'yes' or 'no'")
    if execution_scope not in {"local_only", "deployment"}:
        errors.append("execution_scope must be 'local_only' or 'deployment'")
    if execution_scope == "deployment" and not deployment_requested:
        errors.append("execution_scope=deployment requires deployment_requested=true")
    if execution_scope == "local_only" and deployment_requested:
        errors.append("deployment_requested=true is invalid when execution_scope=local_only")
    if quizme_mode not in {"off", "on"}:
        errors.append("quizme_mode must be 'off' or 'on'")
    quizme_options = {
        "quizme_multiple_choice": quizme_multiple_choice,
        "quizme_one_at_a_time": quizme_one_at_a_time,
        "quizme_confirm": quizme_confirm,
        "quizme_record": quizme_record,
    }
    for field, value in quizme_options.items():
        if not isinstance(value, bool):
            errors.append(f"{field} must be a boolean")
    if any(value is True for value in quizme_options.values()) and quizme_mode != "on":
        errors.append("quizme options require quizme_mode=on")
    if quizme_record and not quizme_confirm:
        errors.append("quizme_record=true requires quizme_confirm=true")
    if parse_utcish(artifact_created_at_utc) is None:
        errors.append("created_at_utc must be a valid ISO-8601 timestamp")

    if not isinstance(startup_declaration, dict):
        errors.append("startup_declaration must be an object")
    else:
        required_startup_fields = [
            "skills_in_use",
            "skills_selection_rationale",
            "skills_execution_order",
        ]
        for field in required_startup_fields:
            if field not in startup_declaration:
                errors.append(f"startup_declaration missing required field: {field}")
        skills_in_use = startup_declaration.get("skills_in_use", [])
        skills_execution_order = startup_declaration.get("skills_execution_order", [])
        skills_selection_rationale = startup_declaration.get("skills_selection_rationale", "")
        if not isinstance(skills_in_use, list) or not skills_in_use:
            errors.append("startup_declaration.skills_in_use must be a non-empty list")
        if not isinstance(skills_execution_order, list) or not skills_execution_order:
            errors.append("startup_declaration.skills_execution_order must be a non-empty list")
        if not str(skills_selection_rationale).strip():
            errors.append("startup_declaration.skills_selection_rationale must be non-empty")
        if isinstance(skills_in_use, list) and isinstance(skills_execution_order, list):
            missing_from_in_use = [skill for skill in skills_execution_order if skill not in skills_in_use]
            if missing_from_in_use:
                errors.append(
                    "startup_declaration.skills_execution_order contains skills not present in skills_in_use: "
                    + ", ".join(missing_from_in_use)
                )
            if isinstance(required_gates, list):
                missing_required_gates = [gate for gate in required_gates if gate not in skills_in_use]
                if missing_required_gates:
                    errors.append(
                        "startup_declaration.skills_in_use missing required gates: "
                        + ", ".join(missing_required_gates)
                    )
            if quizme_mode == "on" and "quizme-mode" not in skills_in_use:
                errors.append("startup_declaration.skills_in_use missing quizme-mode while quizme_mode=on")

    for gate in required_gates:
        if gate not in gate_status:
            errors.append(f"gate status missing for required gate: {gate}")
            continue
        status = gate_status[gate]
        if status not in VALID_STATES:
            errors.append(f"invalid gate status '{status}' for gate '{gate}'")

    failed = [gate for gate in required_gates if gate_status.get(gate) == "fail"]
    pending = [gate for gate in required_gates if gate_status.get(gate) == "pending"]

    if args.strict:
        for gate in required_gates:
            if gate_status.get(gate) not in PASS_STATES:
                errors.append(f"strict mode: gate not complete: {gate}={gate_status.get(gate)}")
    else:
        if failed:
            errors.append(f"one or more required gates failed: {', '.join(failed)}")
        if pending:
            warnings.append(f"pending required gates: {', '.join(pending)}")

    if recommendation_rank(recommendation) < recommendation_rank(args.require_recommendation):
        errors.append(
            f"recommendation '{recommendation}' is below required '{args.require_recommendation}'"
        )

    if "missing_rollback_path" in overrides and recommendation != "no-go":
        errors.append("override missing_rollback_path requires recommendation no-go")

    if break_glass.get("enabled"):
        for field in ("reason", "risk_owner", "remediation_ticket", "expiry_hours"):
            if not break_glass.get(field):
                errors.append(f"break-glass enabled but missing field: {field}")
        if recommendation != "go-with-risk":
            warnings.append("break-glass enabled; recommendation is usually go-with-risk")

    if mode == "critical":
        for must_pass in ("project-backup", "restore-drill"):
            if must_pass in required_gates and gate_status.get(must_pass) not in PASS_STATES:
                errors.append(f"critical mode requires {must_pass}=pass/waived before go/no-go")

    project_index = load_project_index(Path(args.project_index_path))
    if not project_index:
        errors.append(f"project index is missing or empty: {args.project_index_path}")
    else:
        index_entry = project_index.get(project_id)
        if not index_entry:
            errors.append(
                f"project index missing project_id '{project_id}' in {args.project_index_path}"
            )
        else:
            if index_entry["language"] != str(project_language).strip():
                errors.append(
                    "project index mismatch for language: "
                    f"artifact='{project_language}' index='{index_entry['language']}'"
                )
            if index_entry["description"] != str(project_description_max4).strip():
                errors.append(
                    "project index mismatch for description: "
                    f"artifact='{project_description_max4}' index='{index_entry['description']}'"
                )
            if index_entry["model_default_test_build"] != model_runs_test_build_default:
                errors.append(
                    "project index mismatch for model_default_test_build: "
                    f"artifact='{model_runs_test_build_default}' "
                    f"index='{index_entry['model_default_test_build']}'"
                )
            if not index_entry["last_confirmed_utc"]:
                errors.append(
                    f"project index last_confirmed_utc is empty for project_id '{project_id}'"
                )
            else:
                artifact_dt = parse_utcish(artifact_created_at_utc)
                index_dt = parse_utcish(index_entry["last_confirmed_utc"])
                if artifact_dt is None:
                    errors.append("artifact created_at_utc timestamp is invalid")
                elif index_dt is None:
                    errors.append(
                        "project index last_confirmed_utc must be a valid ISO-8601 timestamp "
                        f"for project_id '{project_id}'"
                    )
                elif index_dt < artifact_dt:
                    errors.append(
                        "project index last_confirmed_utc is older than artifact created_at_utc "
                        f"for project_id '{project_id}'"
                    )

    if warnings:
        for warning in warnings:
            print(f"WARNING: {warning}")
    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        raise SystemExit(1)

    print("Governance artifact validation passed.")
    print(f"Task: {data['task_id']}")
    print(f"Mode: {mode}")
    print(f"Recommendation: {recommendation}")


if __name__ == "__main__":
    main()
