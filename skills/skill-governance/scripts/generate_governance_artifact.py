#!/usr/bin/env python3
"""Generate a governance artifact with deterministic mode and required gates."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_DIR = SCRIPT_PATH.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from governance_common import (  # noqa: E402
    SCHEMA_V3,
    build_manifest,
    contained_artifact_paths,
    discover_repo_root,
    is_governed_change,
    manifest_sha256,
    normalize_repo_path,
    resolve_commit,
    run_git,
    validate_task_id,
    working_tree_name_status,
)


DEFAULT_SKILLS_ROOT = SCRIPT_PATH.parents[2]


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

AUTHORIZED_OPERATIONS = (
    "commit",
    "configure_remote",
    "delete",
    "deploy",
    "message",
    "migrate",
    "publish",
    "push",
)

CRITICAL_AUTHORIZED_OPERATIONS = frozenset(
    {"configure_remote", "delete", "deploy", "migrate", "publish"}
)
RECOVERY_REQUIRED_OPERATIONS = frozenset({"delete", "migrate"})
EXTERNAL_AUTHORIZED_OPERATIONS = frozenset(AUTHORIZED_OPERATIONS) - {"commit"}

GATE_MATRIX = {
    "quick": [
        "execution-skill",
    ],
    "standard": [
        "execution-skill",
        "regression-prevention",
    ],
    "critical": [
        "execution-skill",
        "regression-prevention",
        "semantic-policy-audit",
        "governance-enforcement",
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
        "rollback plan",
        "release decision",
    ],
}

SKILL_NAME_REGEX = re.compile(r"^[a-z0-9-]+$")
SEMVER_REGEX = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$")
PROJECT_ID_REGEX = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
PROJECT_INDEX_UTC_REGEX = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)$"
)
PROJECT_INDEX_HEADING = "# Project Index"
PROJECT_INDEX_HEADER = (
    "| Project ID | Language | Description (<=4 words) | "
    "Model Runs Tests/Build by Default (yes/no) | Last Confirmed UTC |"
)
PROJECT_INDEX_SEPARATOR = "|---|---|---|---|---|"


class ProjectIndexValidationError(ValueError):
    """Report all structural and field errors in a project index."""

    def __init__(self, path: Path, errors: list[str]) -> None:
        self.path = path
        self.errors = errors
        super().__init__(f"{path}: " + "; ".join(errors))


@dataclass
class GovernanceArtifact:
    schema_version: int
    task_id: str
    purpose: str
    authorized_operations: list[str]
    release_metadata: dict[str, Any] | None
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
    uncertainty_high: bool
    requires_backup: bool
    requires_restore: bool
    quizme_mode: str
    quizme_multiple_choice: bool
    quizme_one_at_a_time: bool
    quizme_confirm: bool
    quizme_record: bool
    scores: dict[str, int]
    total_score: int
    base_mode: str
    mode_after_profile: str
    selected_mode: str
    critical_overrides: list[str]
    required_gates: list[str]
    gate_status: dict[str, dict[str, Any]]
    startup_declaration: dict[str, Any]
    evidence_requirements: list[str]
    break_glass: dict[str, Any]
    recommendation: str
    change_binding: dict[str, Any]
    notes: str
    catalog_binding: dict[str, Any]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", required=True, help="Unique task ID for this governance artifact.")
    parser.add_argument(
        "--base-sha",
        required=True,
        help="Exact Git base commit used to bind the governed working-tree manifest.",
    )
    parser.add_argument(
        "--repo-root",
        default="",
        help="Repository root. Auto-discovered only when Git or a verified skills/ layout proves it.",
    )
    parser.add_argument(
        "--skills-root",
        default=str(DEFAULT_SKILLS_ROOT),
        help="Skills root used to verify repository-root discovery.",
    )
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
        choices=["local_only", "external", "deployment"],
        default="local_only",
        help="Default execution scope for this task.",
    )
    parser.add_argument(
        "--purpose",
        choices=["change", "release"],
        default="change",
        help="Artifact purpose. Release purpose requires explicit publication authority.",
    )
    parser.add_argument(
        "--authorized-operation",
        dest="authorized_operations",
        action="append",
        choices=AUTHORIZED_OPERATIONS,
        default=[],
        help="Operation-specific authority recorded by this plan. Can be repeated.",
    )
    parser.add_argument("--release-version", default="")
    parser.add_argument("--release-tag", default="")
    parser.add_argument("--release-version-path", default="skills/VERSION")
    parser.add_argument("--release-changelog-path", default="skills/CHANGELOG.md")
    parser.add_argument("--release-notes-path", default="")
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
        "--requires-backup",
        "--external-state-data-loss-risk",
        dest="requires_backup",
        action="store_true",
        help=(
            "Include project-backup for an authorized external, production, or "
            "non-reconstructable-state operation with credible data-loss exposure. "
            "The longer option is a compatibility alias."
        ),
    )
    parser.add_argument(
        "--requires-restore",
        "--recovery-sensitive-external-operation",
        dest="requires_restore",
        action="store_true",
        help=(
            "Include restore-drill for an authorized recovery-sensitive external operation; "
            "this also includes project-backup. The longer option is a compatibility alias."
        ),
    )
    parser.add_argument(
        "--quizme-mode",
        choices=["off", "on"],
        default="off",
        help="Record persistent conversation-local quizme mode state for this governed task.",
    )
    parser.add_argument(
        "--quizme-mc",
        action="store_true",
        help="Record --quizme --mc multiple-choice preference. Requires --quizme-mode on.",
    )
    parser.add_argument(
        "--quizme-one-at-a-time",
        action="store_true",
        help="Record --quizme --one-at-a-time adaptive single-question preference. Requires --quizme-mode on.",
    )
    parser.add_argument(
        "--quizme-confirm",
        action="store_true",
        help="Record --quizme --confirm explicit task-contract approval requirement. Requires --quizme-mode on.",
    )
    parser.add_argument(
        "--quizme-record",
        action="store_true",
        help="Record --quizme --record durable contract evidence requirement. Implies --quizme-confirm.",
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


def build_required_gates(
    mode: str,
    execution_skill: str,
    behavior_or_workflow_changed: bool,
    requires_backup: bool = False,
    requires_restore: bool = False,
) -> list[str]:
    gates = list(GATE_MATRIX[mode])
    gates = [execution_skill if gate == "execution-skill" else gate for gate in gates]
    if requires_backup or requires_restore:
        gates.append("project-backup")
    if requires_restore:
        gates.append("restore-drill")
    if behavior_or_workflow_changed and "doc-maintenance" not in gates:
        gates.append("doc-maintenance")
    return gates


def build_evidence_requirements(
    mode: str,
    requires_backup: bool = False,
    requires_restore: bool = False,
    authorized_operations: list[str] | tuple[str, ...] = (),
) -> list[str]:
    requirements = list(EVIDENCE_REQUIREMENTS[mode])
    if set(authorized_operations).intersection(EXTERNAL_AUTHORIZED_OPERATIONS):
        requirements.extend(
            [
                "operation-specific authority + target identity",
                "rollback or recovery evidence",
                "post-operation validation + audit evidence",
            ]
        )
    if requires_backup or requires_restore:
        requirements.append("backup artifact + integrity evidence")
    if requires_restore:
        requirements.append("restore freshness/pass status")
    return requirements


def operations_force_critical(authorized_operations: list[str] | tuple[str, ...]) -> bool:
    return bool(set(authorized_operations).intersection(CRITICAL_AUTHORIZED_OPERATIONS))


def manifest_requires_documentation(manifest: list[dict[str, Any]]) -> bool:
    """Return whether unambiguous behavior/workflow paths require doc evidence."""
    for entry in manifest:
        path = str(entry.get("path", ""))
        if path in {
            ".github/branch-protection-policy.json",
            "AGENTS.md",
            "skills/skill-catalog.json",
        }:
            return True
        if path.startswith(".github/workflows/"):
            return True
        if path.startswith("skills/skill-governance/scripts/"):
            return True
        if path.startswith("skills/skill-governance/schemas/"):
            return True
        if path.startswith("skills/") and path.endswith("/SKILL.md"):
            return True
    return False


def _catalog_skill_snapshot(skill: dict[str, Any]) -> dict[str, Any]:
    relations = skill.get("relations", {})
    return {
        "status": skill.get("status"),
        "requires": list(relations.get("requires", [])),
        "runs_after": list(relations.get("runs_after", [])),
        "conflicts_with": list(relations.get("conflicts_with", [])),
    }


def build_catalog_binding(
    catalog_path: Path,
    skills_in_use: list[str],
    skills_execution_order: list[str],
    *,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Bind and validate the exact catalog contract used by a v3 plan."""
    try:
        raw = catalog_path.read_bytes()
        payload = json.loads(raw)
        catalog_skills = {
            str(skill["name"]): skill
            for skill in payload["skills"]
            if isinstance(skill, dict) and isinstance(skill.get("name"), str)
        }
        components = set(map(str, payload["components"]))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise SystemExit(f"Unable to load canonical skill catalog: {exc}") from exc

    selected = set(skills_in_use)
    unknown = sorted(selected - set(catalog_skills))
    if unknown:
        raise SystemExit("Startup declaration uses unknown catalog skills: " + ", ".join(unknown))
    inactive = sorted(name for name in selected if catalog_skills[name].get("status") != "active")
    if inactive:
        raise SystemExit("Startup declaration uses non-active skills: " + ", ".join(inactive))

    positions = {name: index for index, name in enumerate(skills_execution_order)}
    for name in sorted(selected):
        relations = catalog_skills[name].get("relations", {})
        required = set(map(str, relations.get("requires", []))) - components
        missing = sorted(required - selected)
        if missing:
            raise SystemExit(
                f"Startup declaration skill {name} is missing prerequisites: "
                + ", ".join(missing)
            )
        predecessors = required | set(map(str, relations.get("runs_after", []))).intersection(selected)
        for predecessor in sorted(predecessors):
            if positions[predecessor] > positions[name]:
                raise SystemExit(
                    f"Startup declaration order places {name} before predecessor {predecessor}"
                )
        conflicts = sorted(set(map(str, relations.get("conflicts_with", []))).intersection(selected))
        if conflicts:
            raise SystemExit(
                f"Startup declaration skill {name} conflicts with: " + ", ".join(conflicts)
            )

    if repo_root is None:
        binding_path = "skills/skill-catalog.json"
    else:
        try:
            binding_path = normalize_repo_path(
                catalog_path.resolve().relative_to(repo_root.resolve()).as_posix()
            )
        except ValueError as exc:
            raise SystemExit("Canonical skill catalog must be inside the repository root") from exc
    return {
        "path": binding_path,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "catalog_version": str(payload["catalog_version"]),
        "router_contract": str(payload["router_contract"]),
        "components": sorted(components),
        "skills": {
            name: _catalog_skill_snapshot(catalog_skills[name])
            for name in sorted(selected)
        },
    }


def path_exists_at_revision(repo_root: Path, revision: str, path: str) -> bool:
    normalized = normalize_repo_path(path)
    output = run_git(
        repo_root,
        ["ls-tree", "--name-only", "-z", revision, "--", normalized],
    )
    assert isinstance(output, bytes)
    return normalized.encode("utf-8") in output.split(b"\0")


def _repo_file(repo_root: Path, raw_path: str) -> tuple[str, Path]:
    path = normalize_repo_path(raw_path)
    candidate = (repo_root / path).resolve()
    try:
        candidate.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise SystemExit(f"Release metadata path escapes repository root: {path}") from exc
    if not candidate.is_file():
        raise SystemExit(f"Release metadata file does not exist: {path}")
    return path, candidate


def count_governance_test_methods(repo_root: Path) -> int:
    count = 0
    tests_root = repo_root / "skills" / "skill-governance" / "tests"
    for path in sorted(tests_root.glob("test_*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, UnicodeDecodeError, SyntaxError) as exc:
            raise SystemExit(f"Unable to inventory governance tests: {path}: {exc}") from exc
        count += sum(
            1
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        )
    return count


def build_release_metadata(repo_root: Path, args: argparse.Namespace) -> dict[str, Any] | None:
    if args.purpose != "release":
        return None
    version = args.release_version.strip()
    tag = args.release_tag.strip()
    version_path, version_file = _repo_file(repo_root, args.release_version_path)
    changelog_path, changelog_file = _repo_file(repo_root, args.release_changelog_path)
    notes_raw = args.release_notes_path.strip() or f"skills/RELEASE_NOTES_v{version}.md"
    release_notes_path, release_notes_file = _repo_file(repo_root, notes_raw)

    if version_file.read_text(encoding="utf-8").strip() != version:
        raise SystemExit("Release version does not match the exact version file")
    changelog = changelog_file.read_text(encoding="utf-8")
    if not re.search(
        rf"^## \[{re.escape(version)}\] - \d{{4}}-\d{{2}}-\d{{2}}$",
        changelog,
        flags=re.MULTILINE,
    ):
        raise SystemExit("Release changelog lacks a dated heading for the exact version")

    catalog = json.loads((repo_root / "skills" / "skill-catalog.json").read_text(encoding="utf-8"))
    skill_count = len(catalog.get("skills", []))
    test_count = count_governance_test_methods(repo_root)
    release_notes = release_notes_file.read_text(encoding="utf-8")
    for marker in (
        tag,
        f"- Skill count: `{skill_count}`",
        f"- Governance test count: `{test_count}`",
    ):
        if marker not in release_notes:
            raise SystemExit(f"Release notes are missing exact metadata marker: {marker}")

    return {
        "version": version,
        "tag": tag,
        "version_path": version_path,
        "changelog_path": changelog_path,
        "release_notes_path": release_notes_path,
        "skill_count": skill_count,
        "governance_test_count": test_count,
    }


def determine_recommendation(critical_overrides: list[str], break_glass: bool) -> str:
    # Newly generated v3 artifacts contain pending gates. A positive release
    # recommendation is valid only after evidence is added and gates are closed.
    return "no-go"


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
    validate_task_id(args.task_id)
    if PROJECT_ID_REGEX.fullmatch(args.project_id.strip()) is None:
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
    if args.execution_scope != "deployment" and args.deployment_requested:
        raise SystemExit("--deployment-requested requires execution-scope=deployment")
    if (
        args.requires_backup or args.requires_restore
    ) and args.execution_scope == "local_only":
        raise SystemExit(
            "external recovery-impact flags require execution-scope=external or deployment"
        )
    authorized_operations = set(args.authorized_operations)
    external_operations = authorized_operations - {"commit"}
    if external_operations and args.execution_scope == "local_only":
        raise SystemExit("external authorized operations require non-local execution scope")
    if "deploy" in authorized_operations and args.execution_scope != "deployment":
        raise SystemExit("authorized deploy requires execution-scope=deployment")
    recovery_operations = authorized_operations.intersection(RECOVERY_REQUIRED_OPERATIONS)
    if recovery_operations and not (args.requires_backup and args.requires_restore):
        raise SystemExit(
            "authorized delete or migrate requires both --requires-backup and --requires-restore"
        )
    if args.purpose == "release":
        if "publish" not in authorized_operations:
            raise SystemExit("purpose=release requires --authorized-operation publish")
        if args.execution_scope == "local_only":
            raise SystemExit("purpose=release requires external or deployment execution scope")
        if not SEMVER_REGEX.fullmatch(args.release_version.strip()):
            raise SystemExit("purpose=release requires a valid --release-version")
        if args.release_tag.strip() != f"v{args.release_version.strip()}":
            raise SystemExit("--release-tag must equal v<release-version>")
    elif "publish" in authorized_operations:
        raise SystemExit("authorized publish requires purpose=release")
    elif any((args.release_version.strip(), args.release_tag.strip(), args.release_notes_path.strip())):
        raise SystemExit("release metadata options require purpose=release")
    if not args.skills_selection_rationale.strip():
        raise SystemExit("--skills-selection-rationale is required")
    validate_quizme_fields(
        args.quizme_mode,
        args.quizme_mc,
        args.quizme_one_at_a_time,
        args.quizme_confirm,
        args.quizme_record,
    )


def validate_quizme_fields(
    quizme_mode: str,
    quizme_mc: bool,
    quizme_one_at_a_time: bool = False,
    quizme_confirm: bool = False,
    quizme_record: bool = False,
) -> None:
    if any((quizme_mc, quizme_one_at_a_time, quizme_confirm, quizme_record)) and quizme_mode != "on":
        raise SystemExit("quizme options require --quizme-mode on")


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
    quizme_mode: str = "off",
) -> None:
    if set(skills_in_use) != set(skills_execution_order):
        raise SystemExit("--skills-in-use and --skills-execution-order must contain the same skill set")
    required_governed_skills = {"skill-governance", execution_skill}
    missing = sorted(required_governed_skills - set(skills_in_use))
    if missing:
        raise SystemExit(f"Startup declaration missing required skills: {', '.join(missing)}")
    if quizme_mode == "on" and "quizme-mode" not in skills_in_use:
        raise SystemExit("Startup declaration missing required skill: quizme-mode")


def validate_required_gate_skills(
    required_gates: list[str],
    skills_in_use: list[str],
) -> None:
    missing = sorted(set(required_gates) - set(skills_in_use))
    if missing:
        raise SystemExit(
            "Startup declaration missing required gate skills: " + ", ".join(missing)
        )


def render_markdown(artifact: GovernanceArtifact) -> str:
    lines = []
    lines.append(f"# Governance Artifact: {artifact.task_id}")
    lines.append("")
    lines.append(f"- `schema_version`: {artifact.schema_version}")
    lines.append(f"- `created_at_utc`: {artifact.created_at_utc}")
    lines.append(f"- `project_id`: {artifact.project_id}")
    lines.append(f"- `purpose`: {artifact.purpose}")
    lines.append(
        "- `authorized_operations`: "
        + (", ".join(artifact.authorized_operations) if artifact.authorized_operations else "none")
    )
    if artifact.release_metadata is None:
        lines.append("- `release_metadata`: none")
    else:
        lines.append("- `release_metadata`:")
        for key, value in artifact.release_metadata.items():
            lines.append(f"  - `{key}`: {value}")
    lines.append(f"- `profile`: {artifact.profile}")
    lines.append(f"- `project_language`: {artifact.project_language}")
    lines.append(f"- `project_description_max4`: {artifact.project_description_max4}")
    lines.append(f"- `model_runs_test_build_default`: {artifact.model_runs_test_build_default}")
    lines.append(f"- `execution_scope`: {artifact.execution_scope}")
    lines.append(f"- `deployment_requested`: {str(artifact.deployment_requested).lower()}")
    lines.append(f"- `execution_skill`: {artifact.execution_skill}")
    lines.append(f"- `uncertainty_high`: {str(artifact.uncertainty_high).lower()}")
    lines.append(f"- `requires_backup`: {str(artifact.requires_backup).lower()}")
    lines.append(f"- `requires_restore`: {str(artifact.requires_restore).lower()}")
    lines.append(f"- `quizme_mode`: {artifact.quizme_mode}")
    lines.append(f"- `quizme_multiple_choice`: {str(artifact.quizme_multiple_choice).lower()}")
    lines.append(f"- `quizme_one_at_a_time`: {str(artifact.quizme_one_at_a_time).lower()}")
    lines.append(f"- `quizme_confirm`: {str(artifact.quizme_confirm).lower()}")
    lines.append(f"- `quizme_record`: {str(artifact.quizme_record).lower()}")
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
        gate_record = artifact.gate_status.get(gate, {})
        lines.append(f"- [ ] `{gate}` (status: {gate_record.get('status', 'pending')})")
        lines.append(f"  - evidence: {gate_record.get('evidence', [])}")
        waiver_reason = gate_record.get("waiver_reason", "")
        lines.append(
            f"  - waiver_reason: {waiver_reason}" if waiver_reason else "  - waiver_reason:"
        )
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
    lines.append("## Catalog Binding")
    lines.append(f"- `path`: {artifact.catalog_binding['path']}")
    lines.append(f"- `sha256`: {artifact.catalog_binding['sha256']}")
    lines.append(f"- `catalog_version`: {artifact.catalog_binding['catalog_version']}")
    lines.append(f"- `router_contract`: {artifact.catalog_binding['router_contract']}")
    lines.append("")
    lines.append("## Change Binding")
    lines.append(f"- `base_sha`: {artifact.change_binding['base_sha']}")
    lines.append(f"- `manifest_sha256`: {artifact.change_binding['manifest_sha256']}")
    lines.append("- `manifest`:")
    if artifact.change_binding["manifest"]:
        for item in artifact.change_binding["manifest"]:
            lines.append(
                f"  - `{item['status']}` `{item['path']}` "
                f"(`sha256`: {item['sha256'] if item['sha256'] is not None else 'null'})"
            )
    else:
        lines.append("  - none")
    return "\n".join(lines)


def parse_index_line(line: str) -> list[str]:
    return [cell.strip() for cell in line[1:-1].split("|")]


def _valid_project_index_utc(value: str) -> bool:
    if PROJECT_INDEX_UTC_REGEX.fullmatch(value) is None:
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() == timedelta(0)


def validate_project_index(
    path: Path,
    *,
    allow_missing: bool = False,
) -> dict[str, dict[str, str]]:
    """Parse a structurally exact project index or fail with all discovered errors."""

    if not path.exists():
        if allow_missing:
            return {}
        raise ProjectIndexValidationError(path, ["missing required project index"])
    if not path.is_file():
        raise ProjectIndexValidationError(path, ["project index path is not a file"])
    try:
        raw_lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise ProjectIndexValidationError(path, [f"cannot read project index: {exc}"]) from exc

    nonblank = [
        (line_number, line)
        for line_number, line in enumerate(raw_lines, start=1)
        if line.strip()
    ]
    errors: list[str] = []
    expected_preamble = (
        ("heading", PROJECT_INDEX_HEADING),
        ("table header", PROJECT_INDEX_HEADER),
        ("table separator", PROJECT_INDEX_SEPARATOR),
    )
    for index, (label, expected) in enumerate(expected_preamble):
        if index >= len(nonblank):
            errors.append(f"missing exact {label}: {expected}")
            continue
        line_number, actual = nonblank[index]
        if actual != expected:
            errors.append(
                f"line {line_number} must be the exact {label}: {expected}"
            )

    entries: dict[str, dict[str, str]] = {}
    for line_number, line in nonblank[3:]:
        if not line.startswith("|") or not line.endswith("|"):
            errors.append(
                f"line {line_number} contains non-table content after the project-index preamble"
            )
            continue
        cells = parse_index_line(line)
        if len(cells) != 5:
            errors.append(f"line {line_number} must contain exactly five table cells")
            continue
        project_id, language, description, model_default, last_confirmed = cells
        if PROJECT_ID_REGEX.fullmatch(project_id) is None:
            errors.append(
                f"line {line_number} has invalid lowercase project ID `{project_id}`"
            )
        elif project_id in entries:
            errors.append(f"line {line_number} duplicates project ID `{project_id}`")
        if not language:
            errors.append(f"line {line_number} has an empty language")
        word_count = len(description.split())
        if not description:
            errors.append(f"line {line_number} has an empty description")
        elif word_count > 4:
            errors.append(
                f"line {line_number} description has {word_count} words; maximum is 4"
            )
        if model_default not in {"yes", "no"}:
            errors.append(
                f"line {line_number} model test/build default must be exactly `yes` or `no`"
            )
        if not _valid_project_index_utc(last_confirmed):
            errors.append(
                f"line {line_number} Last Confirmed UTC must be a valid timezone-aware UTC timestamp"
            )
        if PROJECT_ID_REGEX.fullmatch(project_id) is not None and project_id not in entries:
            entries[project_id] = {
                "language": language,
                "description": description,
                "model_default_test_build": model_default,
                "last_confirmed_utc": last_confirmed,
            }

    if errors:
        raise ProjectIndexValidationError(path, errors)
    return entries


def load_project_index(path: Path) -> dict[str, dict[str, str]]:
    return validate_project_index(path, allow_missing=True)


def write_project_index(path: Path, entries: dict[str, dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        PROJECT_INDEX_HEADING,
        "",
        PROJECT_INDEX_HEADER,
        PROJECT_INDEX_SEPARATOR,
    ]
    for project_id in sorted(entries.keys()):
        item = entries[project_id]
        lines.append(
            f"| {project_id} | {item['language']} | {item['description']} | "
            f"{item['model_default_test_build']} | {item['last_confirmed_utc']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sync_project_index(path: Path, artifact: GovernanceArtifact) -> None:
    try:
        entries = load_project_index(path)
    except ProjectIndexValidationError as exc:
        raise SystemExit(str(exc)) from exc
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

    repo_root = discover_repo_root(args.repo_root, Path(args.skills_root))
    skills_root = Path(args.skills_root)
    if not skills_root.is_absolute():
        skills_root = repo_root / skills_root
    outdir = Path(args.outdir)
    if not outdir.is_absolute():
        outdir = repo_root / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    json_path, md_path = contained_artifact_paths(outdir, args.task_id)
    resolved_base = resolve_commit(repo_root, args.base_sha, "base SHA")
    for artifact_path in (json_path, md_path):
        try:
            relative_artifact = normalize_repo_path(
                artifact_path.relative_to(repo_root).as_posix()
            )
        except ValueError as exc:
            raise SystemExit("Governance artifact output must remain inside the repository") from exc
        if path_exists_at_revision(repo_root, resolved_base, relative_artifact):
            raise SystemExit(
                "Governance task ID already exists at the enforced base; "
                "use a new superseding task ID instead of overwriting committed evidence"
            )

    _, initial_changes = working_tree_name_status(repo_root, resolved_base)
    initial_manifest = build_manifest(repo_root, initial_changes)
    if manifest_requires_documentation(initial_manifest) and not args.behavior_or_workflow_changed:
        raise SystemExit(
            "The changed workflow or behavior paths require --behavior-or-workflow-changed"
        )

    scores = {key: int(getattr(args, key)) for key in SCORE_KEYS}
    total = sum(scores.values())
    base_mode = base_mode_from_total(total)

    overrides = sorted(set(args.critical_overrides))
    forced_critical = (
        bool(overrides)
        or args.purpose == "release"
        or operations_force_critical(args.authorized_operations)
    )

    mode_after_profile = base_mode
    if not forced_critical:
        mode_after_profile = apply_profile_modifier(base_mode, args.profile, total, args.uncertainty_high)
    selected_mode = "critical" if forced_critical else mode_after_profile

    required_gates = build_required_gates(
        selected_mode,
        args.execution_skill,
        args.behavior_or_workflow_changed,
        args.requires_backup,
        args.requires_restore,
    )
    gate_status = {
        gate: {"status": "pending", "evidence": [], "waiver_reason": ""}
        for gate in required_gates
    }
    skills_in_use = parse_csv_list(args.skills_in_use, "--skills-in-use")
    skills_execution_order = parse_csv_list(args.skills_execution_order, "--skills-execution-order")
    validate_startup_declaration_skills(
        skills_in_use,
        skills_execution_order,
        args.execution_skill,
        args.quizme_mode,
    )
    validate_required_gate_skills(required_gates, skills_in_use)
    catalog_binding = build_catalog_binding(
        skills_root / "skill-catalog.json",
        skills_in_use,
        skills_execution_order,
        repo_root=repo_root,
    )
    release_metadata = build_release_metadata(repo_root, args)

    recommendation = determine_recommendation(overrides, args.break_glass)
    created_at_utc = datetime.now(UTC).isoformat()
    artifact = GovernanceArtifact(
        schema_version=SCHEMA_V3,
        task_id=args.task_id,
        purpose=args.purpose,
        authorized_operations=sorted(set(args.authorized_operations)),
        release_metadata=release_metadata,
        project_id=args.project_id.strip(),
        created_at_utc=created_at_utc,
        profile=args.profile,
        project_language=args.project_language.strip(),
        project_description_max4=args.project_description_max4.strip(),
        model_runs_test_build_default=args.model_runs_test_build_default,
        execution_scope=args.execution_scope,
        deployment_requested=bool(args.deployment_requested),
        execution_skill=args.execution_skill,
        behavior_or_workflow_changed=bool(args.behavior_or_workflow_changed),
        uncertainty_high=bool(args.uncertainty_high),
        requires_backup=bool(args.requires_backup or args.requires_restore),
        requires_restore=bool(args.requires_restore),
        quizme_mode=args.quizme_mode,
        quizme_multiple_choice=bool(args.quizme_mc),
        quizme_one_at_a_time=bool(args.quizme_one_at_a_time),
        quizme_confirm=bool(args.quizme_confirm or args.quizme_record),
        quizme_record=bool(args.quizme_record),
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
        evidence_requirements=build_evidence_requirements(
            selected_mode,
            args.requires_backup,
            args.requires_restore,
            args.authorized_operations,
        ),
        break_glass={
            "enabled": bool(args.break_glass),
            "reason": args.break_glass_reason.strip(),
            "risk_owner": args.risk_owner.strip(),
            "remediation_ticket": args.remediation_ticket.strip(),
            "expiry_hours": args.expiry_hours if args.break_glass else None,
        },
        recommendation=recommendation,
        change_binding={},
        notes=args.notes.strip(),
        catalog_binding=catalog_binding,
    )

    project_index_path = Path(args.project_index_path)
    if not project_index_path.is_absolute():
        project_index_path = repo_root / project_index_path
    sync_project_index(project_index_path, artifact)

    _, changes = working_tree_name_status(repo_root, resolved_base)
    manifest = build_manifest(
        repo_root,
        changes,
        governed_predicate=None if args.purpose == "release" else is_governed_change,
    )
    if release_metadata is not None:
        manifest_paths = {entry["path"] for entry in manifest}
        required_release_paths = {
            release_metadata["version_path"],
            release_metadata["changelog_path"],
            release_metadata["release_notes_path"],
        }
        missing_release_paths = sorted(required_release_paths - manifest_paths)
        if missing_release_paths:
            raise SystemExit(
                "Release metadata files must all be part of the full bound diff: "
                + ", ".join(missing_release_paths)
            )
    artifact.change_binding = {
        "base_sha": resolved_base,
        "manifest": manifest,
        "manifest_sha256": manifest_sha256(manifest),
    }

    json_path.write_text(json.dumps(asdict(artifact), indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(artifact) + "\n", encoding="utf-8")

    print(f"Wrote: {json_path}")
    print(f"Wrote: {md_path}")
    print(f"Wrote: {project_index_path}")
    print(f"Mode: {artifact.selected_mode}")
    print(f"Recommendation: {artifact.recommendation}")


if __name__ == "__main__":
    main()
