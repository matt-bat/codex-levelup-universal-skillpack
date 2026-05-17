#!/usr/bin/env python3
"""Generate a governance artifact with deterministic mode and required gates."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SCORE_KEYS = (
    "data_impact",
    "business_impact",
    "change_complexity",
    "dependency_uncertainty",
    "recoverability",
)

CRITICAL_OVERRIDES = (
    "auth_or_permission_change",
    "payment_or_financial_change",
    "schema_or_data_deletion_change",
    "api_contract_break",
    "production_security_or_runtime_boundary_change",
    "missing_rollback_path",
)

GATE_MATRIX = {
    "quick": [
        "order-of-operations",
        "execution-skill",
    ],
    "standard": [
        "order-of-operations",
        "execution-skill",
        "regression-prevention",
        "token-reduction",
    ],
    "critical": [
        "order-of-operations",
        "project-backup",
        "restore-drill",
        "execution-skill",
        "regression-prevention",
        "token-reduction",
    ],
}

EVIDENCE_REQUIREMENTS = {
    "quick": [
        "mode + score",
        "steps executed",
        "minimal validation outcomes",
    ],
    "standard": [
        "mode + score",
        "impact map",
        "validation scope by layer",
        "residual risks",
    ],
    "critical": [
        "mode + score",
        "impact map",
        "validation scope by layer",
        "residual risks",
        "backup artifact + integrity evidence",
        "restore freshness/pass status",
        "rollback plan",
        "release decision",
    ],
}

SKILL_NAME_REGEX = re.compile(r"^[a-z0-9-]+$")


@dataclass
class GovernanceArtifact:
    task_id: str
    project_id: str
    created_at_utc: str
    profile: str
    project_language: str
    project_description_max4: str
    model_runs_test_build_default: str
    execution_scope: str
    deployment_requested: bool
    execution_skill: str
    behavior_or_workflow_changed: bool
    scores: dict[str, int]
    total_score: int
    base_mode: str
    mode_after_profile: str
    selected_mode: str
    critical_overrides: list[str]
    required_gates: list[str]
    gate_status: dict[str, str]
    startup_declaration: dict[str, Any]
    evidence_requirements: list[str]
    break_glass: dict[str, Any]
    recommendation: str
    notes: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", required=True, help="Unique task ID for this governance artifact.")
    parser.add_argument(
        "--project-id",
        required=True,
        help="Stable project key used in docs/project-index.md (lowercase letters, digits, hyphens).",
    )
    parser.add_argument("--profile", choices=["prototype", "internal", "production"], default="internal")
    parser.add_argument("--project-language", default="", help="Primary project language.")
    parser.add_argument(
        "--project-description-max4",
        default="",
        help="Project description, maximum 4 words.",
    )
    parser.add_argument(
        "--model-runs-test-build-default",
        choices=["yes", "no"],
        required=True,
        help="Result of initial new-project verification preference question.",
    )
    parser.add_argument(
        "--execution-scope",
        choices=["local_only", "deployment"],
        default="local_only",
        help="Default execution scope for this task.",
    )
    parser.add_argument(
        "--deployment-requested",
        action="store_true",
        help="Set only when user explicitly requested deployment actions.",
    )
    parser.add_argument(
        "--execution-skill",
        choices=["scripted-command-execution", "pseudo-agentic-automation"],
        default="scripted-command-execution",
    )
    parser.add_argument(
        "--behavior-or-workflow-changed",
        action="store_true",
        help="Include doc-maintenance gate.",
    )
    parser.add_argument(
        "--skills-in-use",
        required=True,
        help="Comma-separated skill names used for the task startup declaration.",
    )
    parser.add_argument(
        "--skills-execution-order",
        required=True,
        help="Comma-separated skill names in execution order for the startup declaration.",
    )
    parser.add_argument(
        "--skills-selection-rationale",
        required=True,
        help="Concise rationale for selected skills in startup declaration.",
    )
    for key in SCORE_KEYS:
        parser.add_argument(f"--{key.replace('_', '-')}", type=int, choices=range(0, 4), default=0)
    parser.add_argument(
        "--critical-override",
        dest="critical_overrides",
        action="append",
        choices=CRITICAL_OVERRIDES,
        default=[],
        help="Can be repeated.",
    )
    parser.add_argument("--uncertainty-high", action="store_true")
    parser.add_argument("--break-glass", action="store_true")
    parser.add_argument("--break-glass-reason", default="")
    parser.add_argument("--risk-owner", default="")
    parser.add_argument("--remediation-ticket", default="")
    parser.add_argument("--expiry-hours", type=int, default=72)
    parser.add_argument("--notes", default="")
    parser.add_argument("--outdir", default="docs/governance")
    parser.add_argument(
        "--project-index-path",
        default="docs/project-index.md",
        help="Path to project intake index markdown file.",
    )
    return parser.parse_args()


def base_mode_from_total(total: int) -> str:
    if total <= 4:
        return "quick"
    if total <= 9:
        return "standard"
    return "critical"


def mode_index(mode: str) -> int:
    return {"quick": 0, "standard": 1, "critical": 2}[mode]


def index_mode(index: int) -> str:
    return ["quick", "standard", "critical"][max(0, min(2, index))]


def apply_profile_modifier(mode: str, profile: str, total_score: int, uncertainty_high: bool) -> str:
    idx = mode_index(mode)
    if profile == "prototype":
        return index_mode(idx - 1)
    if profile == "production" and (total_score in (4, 9) or uncertainty_high):
        return index_mode(idx + 1)
    return mode


def build_required_gates(mode: str, execution_skill: str, behavior_or_workflow_changed: bool) -> list[str]:
    gates = list(GATE_MATRIX[mode])
    gates = [execution_skill if gate == "execution-skill" else gate for gate in gates]
    if behavior_or_workflow_changed and "doc-maintenance" not in gates:
        gates.append("doc-maintenance")
    return gates


def determine_recommendation(critical_overrides: list[str], break_glass: bool) -> str:
    if "missing_rollback_path" in critical_overrides:
        return "no-go"
    if break_glass:
        return "go-with-risk"
    return "go"


def validate_break_glass_fields(args: argparse.Namespace) -> None:
    if not args.break_glass:
        return
    missing = []
    if not args.break_glass_reason.strip():
        missing.append("break-glass-reason")
    if not args.risk_owner.strip():
        missing.append("risk-owner")
    if not args.remediation_ticket.strip():
        missing.append("remediation-ticket")
    if args.expiry_hours <= 0 or args.expiry_hours > 168:
        missing.append("expiry-hours(1..168)")
    if missing:
        fields = ", ".join(missing)
        raise SystemExit(f"Invalid break-glass usage: missing/invalid fields: {fields}")


def validate_intake_fields(args: argparse.Namespace) -> None:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,63}", args.project_id.strip()):
        raise SystemExit(
            "--project-id must match [a-z0-9][a-z0-9-]{1,63} (2-64 chars, lowercase letters/digits/hyphens)"
        )
    if not args.project_language.strip():
        raise SystemExit("Missing required field: --project-language")
    if not args.project_description_max4.strip():
        raise SystemExit("Missing required field: --project-description-max4")
    word_count = len(args.project_description_max4.strip().split())
    if word_count > 4:
        raise SystemExit("--project-description-max4 must be 4 words or fewer")
    if args.execution_scope == "deployment" and not args.deployment_requested:
        raise SystemExit("execution-scope=deployment requires --deployment-requested")
    if args.execution_scope == "local_only" and args.deployment_requested:
        raise SystemExit("--deployment-requested conflicts with execution-scope=local_only")
    if not args.skills_selection_rationale.strip():
        raise SystemExit("--skills-selection-rationale is required")


def parse_csv_list(raw_value: str, field_name: str) -> list[str]:
    items = [item.strip() for item in raw_value.split(",") if item.strip()]
    if not items:
        raise SystemExit(f"{field_name} must contain at least one item")
    for item in items:
        if not SKILL_NAME_REGEX.fullmatch(item):
            raise SystemExit(f"{field_name} contains invalid skill name: {item}")
    if len(items) != len(set(items)):
        raise SystemExit(f"{field_name} contains duplicate skill names")
    return items


def validate_startup_declaration_skills(
    skills_in_use: list[str],
    skills_execution_order: list[str],
    execution_skill: str,
) -> None:
    if set(skills_in_use) != set(skills_execution_order):
        raise SystemExit("--skills-in-use and --skills-execution-order must contain the same skill set")
    required_baseline = {"skill-governance", "order-of-operations", execution_skill}
    missing = sorted(required_baseline - set(skills_in_use))
    if missing:
        raise SystemExit(f"Startup declaration missing required skills: {', '.join(missing)}")


def render_markdown(artifact: GovernanceArtifact) -> str:
    lines = []
    lines.append(f"# Governance Artifact: {artifact.task_id}")
    lines.append("")
    lines.append(f"- `created_at_utc`: {artifact.created_at_utc}")
    lines.append(f"- `project_id`: {artifact.project_id}")
    lines.append(f"- `profile`: {artifact.profile}")
    lines.append(f"- `project_language`: {artifact.project_language}")
    lines.append(f"- `project_description_max4`: {artifact.project_description_max4}")
    lines.append(f"- `model_runs_test_build_default`: {artifact.model_runs_test_build_default}")
    lines.append(f"- `execution_scope`: {artifact.execution_scope}")
    lines.append(f"- `deployment_requested`: {str(artifact.deployment_requested).lower()}")
    lines.append(f"- `execution_skill`: {artifact.execution_skill}")
    lines.append(f"- `selected_mode`: {artifact.selected_mode}")
    lines.append(f"- `total_score`: {artifact.total_score}")
    lines.append(f"- `recommendation`: {artifact.recommendation}")
    lines.append("")
    lines.append("## Scores")
    for key, value in artifact.scores.items():
        lines.append(f"- `{key}`: {value}")
    lines.append("")
    lines.append("## Critical Overrides")
    if artifact.critical_overrides:
        for item in artifact.critical_overrides:
            lines.append(f"- `{item}`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Required Gates")
    for gate in artifact.required_gates:
        lines.append(f"- [ ] `{gate}` (status: {artifact.gate_status.get(gate, 'pending')})")
    lines.append("")
    lines.append("## Startup Declaration")
    lines.append("### Skills In Use")
    for skill in artifact.startup_declaration["skills_in_use"]:
        lines.append(f"- `{skill}`")
    lines.append("### Skill Selection Rationale")
    lines.append(artifact.startup_declaration["skills_selection_rationale"])
    lines.append("### Skill Execution Order")
    for skill in artifact.startup_declaration["skills_execution_order"]:
        lines.append(f"- `{skill}`")
    lines.append("")
    lines.append("## Evidence Requirements")
    for item in artifact.evidence_requirements:
        lines.append(f"- [ ] {item}")
    lines.append("")
    lines.append("## Break Glass")
    if artifact.break_glass.get("enabled"):
        lines.append(f"- enabled: true")
        lines.append(f"- reason: {artifact.break_glass.get('reason', '')}")
        lines.append(f"- risk_owner: {artifact.break_glass.get('risk_owner', '')}")
        lines.append(f"- remediation_ticket: {artifact.break_glass.get('remediation_ticket', '')}")
        lines.append(f"- expiry_hours: {artifact.break_glass.get('expiry_hours', '')}")
    else:
        lines.append("- enabled: false")
    lines.append("")
    if artifact.notes:
        lines.append("## Notes")
        lines.append(artifact.notes)
        lines.append("")
    return "\n".join(lines)


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


def write_project_index(path: Path, entries: dict[str, dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Project Index",
        "",
        "| Project ID | Language | Description (<=4 words) | Model Runs Tests/Build by Default (yes/no) | Last Confirmed UTC |",
        "|---|---|---|---|---|",
    ]
    for project_id in sorted(entries.keys()):
        item = entries[project_id]
        lines.append(
            f"| {project_id} | {item['language']} | {item['description']} | "
            f"{item['model_default_test_build']} | {item['last_confirmed_utc']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sync_project_index(path: Path, artifact: GovernanceArtifact) -> None:
    entries = load_project_index(path)
    last_confirmed_utc = artifact.created_at_utc.replace("+00:00", "Z")
    entries[artifact.project_id] = {
        "language": artifact.project_language,
        "description": artifact.project_description_max4,
        "model_default_test_build": artifact.model_runs_test_build_default,
        "last_confirmed_utc": last_confirmed_utc,
    }
    write_project_index(path, entries)


def main() -> None:
    args = parse_args()
    validate_break_glass_fields(args)
    validate_intake_fields(args)

    scores = {key: int(getattr(args, key)) for key in SCORE_KEYS}
    total = sum(scores.values())
    base_mode = base_mode_from_total(total)

    overrides = sorted(set(args.critical_overrides))
    forced_critical = bool(overrides)

    mode_after_profile = base_mode
    if not forced_critical:
        mode_after_profile = apply_profile_modifier(base_mode, args.profile, total, args.uncertainty_high)
    selected_mode = "critical" if forced_critical else mode_after_profile

    required_gates = build_required_gates(selected_mode, args.execution_skill, args.behavior_or_workflow_changed)
    gate_status = {gate: "pending" for gate in required_gates}
    skills_in_use = parse_csv_list(args.skills_in_use, "--skills-in-use")
    skills_execution_order = parse_csv_list(args.skills_execution_order, "--skills-execution-order")
    validate_startup_declaration_skills(skills_in_use, skills_execution_order, args.execution_skill)

    recommendation = determine_recommendation(overrides, args.break_glass)
    artifact = GovernanceArtifact(
        task_id=args.task_id,
        project_id=args.project_id.strip(),
        created_at_utc=datetime.now(UTC).isoformat(),
        profile=args.profile,
        project_language=args.project_language.strip(),
        project_description_max4=args.project_description_max4.strip(),
        model_runs_test_build_default=args.model_runs_test_build_default,
        execution_scope=args.execution_scope,
        deployment_requested=bool(args.deployment_requested),
        execution_skill=args.execution_skill,
        behavior_or_workflow_changed=bool(args.behavior_or_workflow_changed),
        scores=scores,
        total_score=total,
        base_mode=base_mode,
        mode_after_profile=mode_after_profile,
        selected_mode=selected_mode,
        critical_overrides=overrides,
        required_gates=required_gates,
        gate_status=gate_status,
        startup_declaration={
            "skills_in_use": skills_in_use,
            "skills_selection_rationale": args.skills_selection_rationale.strip(),
            "skills_execution_order": skills_execution_order,
        },
        evidence_requirements=EVIDENCE_REQUIREMENTS[selected_mode],
        break_glass={
            "enabled": bool(args.break_glass),
            "reason": args.break_glass_reason.strip(),
            "risk_owner": args.risk_owner.strip(),
            "remediation_ticket": args.remediation_ticket.strip(),
            "expiry_hours": args.expiry_hours if args.break_glass else None,
        },
        recommendation=recommendation,
        notes=args.notes.strip(),
    )

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    json_path = outdir / f"{args.task_id}.governance.json"
    md_path = outdir / f"{args.task_id}.governance.md"

    json_path.write_text(json.dumps(asdict(artifact), indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(artifact) + "\n", encoding="utf-8")
    project_index_path = Path(args.project_index_path)
    sync_project_index(project_index_path, artifact)

    print(f"Wrote: {json_path}")
    print(f"Wrote: {md_path}")
    print(f"Wrote: {project_index_path}")
    print(f"Mode: {artifact.selected_mode}")
    print(f"Recommendation: {artifact.recommendation}")


if __name__ == "__main__":
    main()
