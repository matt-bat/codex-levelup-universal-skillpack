#!/usr/bin/env python3
"""Validate repository skill-policy artifacts and startup declaration requirements."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_DIR = SCRIPT_PATH.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from governance_common import (  # noqa: E402
    diff_name_status,
    discover_repo_root as discover_repo_root_common,
)
from generate_routing_views import (  # noqa: E402
    CatalogError,
    expected_outputs as expected_routing_outputs,
    validate_catalog as validate_catalog_v2,
)
from generate_governance_artifact import (  # noqa: E402
    GovernanceArtifact,
    ProjectIndexValidationError,
    render_markdown as render_governance_markdown,
    validate_project_index,
)
from verify_remote_configuration import validate_policy_file as validate_remote_policy_file  # noqa: E402

DEFAULT_SKILLS_ROOT = SCRIPT_PATH.parents[2]
UTC_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

REQUIRED_AGENTS_SNIPPETS = [
    "## Core Execution Policy",
    "Treat zero selected skills as valid.",
    "A skill supplies a workflow, not authority.",
    "Read-only work performs zero writes",
    "Preserve user work and unrelated dirty-tree changes.",
    "Reclassify the task after material inspection",
    "## Skill Routing",
    "`skills/skill-catalog.json` is the canonical routing source.",
    "Typed relations have distinct meanings",
    "## Declarations and Durable Artifacts",
    "Routine work does not require a startup declaration.",
    "## Conversation Modes",
    "`--quizme`",
    "`/internal-lang on|off`",
]

REQUIRED_FILE_SNIPPETS = {
    "skill-catalog.json": ["\"schema_version\"", "\"skills\"", "\"skill-governance\""],
    "skill-governance/SKILL.md": [
        "## Independent Safety Kernel",
        "Pending or failed required gates force `no-go`.",
        "Historical evidence is immutable",
        "## Release Integrity",
        "a CI attestation bound to that commit",
    ],
    "governance-enforcement/SKILL.md": [
        "# Governance Enforcement",
        "skills/skill-governance/scripts/enforce_governance_ci.py",
    ],
    "skill-governance/schemas/governance-artifact.schema.json": [
        "\"oneOf\"",
        "\"v1\"",
        "\"v2\"",
        "\"change_binding\"",
    ],
    "internal-lang/SKILL.md": [
        "Remain inactive unless the user invokes a supported command",
        "On the first explicit activation in a conversation",
        "No file was created or changed solely because this skill activated.",
    ],
    "hyperfocus-discovery/SKILL.md": [
        "optional branch-control workflow",
        "## Branch Budget",
        "Do not create files, trackers, or artifacts solely because this skill activated.",
    ],
    "user-instructions-tracker/SKILL.md": [
        "`user-instructions.md` at repository root",
        "superseded",
        "retired",
    ],
    "quizme-mode/SKILL.md": [
        "# Quizme Mode",
        "`--quizme`",
        "`--mc`",
        "`--one-at-a-time`",
        "`--confirm`",
        "`--record`",
    ],
    "skill-governance/scripts/validate_skill_order_sync.py": [
        "Skill ordering sync validation passed.",
    ],
}

REQUIRED_USER_INSTRUCTIONS_COLUMNS = [
    "Instruction ID",
    "Instruction",
    "Source",
    "Status",
    "Priority",
    "Owner",
    "Last Updated UTC",
    "Evidence",
    "Notes",
]

REQUIRED_CURRENT_DIRECTIVE_COLUMNS = [
    "Instruction ID",
    "Current Directive",
    "Source",
    "Lifecycle",
    "Priority",
    "Owner",
    "Last Confirmed UTC",
    "Successor or Notes",
]

ALLOWED_DIRECTIVE_LIFECYCLES = {"active", "superseded", "stale", "retired"}

REQUIRED_SKILL_INDEX_COLUMNS = [
    "Skill",
    "Primary Trigger",
    "Typical Triggers Another Skill",
    "Canonical Artifacts",
    "Last Updated UTC",
]

ALLOWED_STATUSES = {"pending", "in_progress", "blocked", "done", "won_t_do"}

CONFLICT_MATRIX_COLUMNS = [
    "Decision Type",
    "Catalog Domain or Policy Key",
    "Owning Skill or Component",
    "Supporting Skills",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents-path", default="AGENTS.md")
    parser.add_argument("--governance-dir", default="docs/governance")
    parser.add_argument("--skills-root", default=str(DEFAULT_SKILLS_ROOT))
    parser.add_argument("--repo-root", default="")
    parser.add_argument("--base-sha", default="")
    parser.add_argument("--head-sha", default="")
    parser.add_argument(
        "--minimum-governance-artifacts",
        type=int,
        default=1,
        help="Minimum committed artifact pairs required during a full-tree policy check.",
    )
    return parser.parse_args()


def discover_repo_root(repo_root_arg: str, skills_root: Path) -> Path:
    return discover_repo_root_common(repo_root_arg, skills_root)


def resolve_agents_path(raw_path: str, skills_root: Path, repo_root: Path) -> Path:
    candidates = []
    candidate = Path(raw_path)
    if candidate.is_absolute():
        candidates.append(candidate)
    else:
        candidates.extend([repo_root / candidate, skills_root / candidate, Path.cwd() / candidate])

    seen = set()
    for item in candidates:
        resolved = item.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.exists():
            return resolved
    return repo_root / raw_path


def changed_files(base_sha: str, head_sha: str, repo_root: Path) -> list[str]:
    if not base_sha and not head_sha:
        return []
    if not base_sha or not head_sha:
        raise SystemExit("--base-sha and --head-sha must be provided together")
    _, _, changes = diff_name_status(repo_root, base_sha, head_sha)
    return [path for _, path in changes]


def parse_markdown_table_line(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_skill_name(skill_file: Path) -> str:
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    in_frontmatter = False
    for line in lines:
        stripped = line.strip()
        if stripped == "---" and not in_frontmatter:
            in_frontmatter = True
            continue
        if stripped == "---" and in_frontmatter:
            break
        if in_frontmatter:
            match = re.match(r"^name:\s*([a-z0-9-]+)\s*$", stripped)
            if match:
                return match.group(1)
    return ""


def load_skill_catalog(skills_root: Path) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    actual_skills: set[str] = set()
    for skill_file in sorted(skills_root.glob("*/SKILL.md")):
        directory_name = skill_file.parent.name
        declared_name = parse_skill_name(skill_file)
        if not declared_name:
            errors.append(f"{skill_file}: missing or invalid frontmatter `name`")
            continue
        if declared_name != directory_name:
            errors.append(f"{skill_file}: frontmatter name `{declared_name}` must match directory `{directory_name}`")
            continue
        actual_skills.add(declared_name)
    if not actual_skills:
        errors.append(f"No skill files found under {skills_root}")
    return actual_skills, errors


def parse_skill_map_skills(skill_map_path: Path) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    if not skill_map_path.exists():
        return set(), [f"Missing required file: {skill_map_path}"]
    lines = skill_map_path.read_text(encoding="utf-8").splitlines()
    in_section = False
    skills: list[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if line == "## Skill Index":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section:
            continue
        match = re.search(r"`([^`]+)`", line)
        if match:
            skills.append(match.group(1).strip())
    if not skills:
        errors.append(f"{skill_map_path}: no skills found in `## Skill Index` section")
        return set(), errors
    if len(skills) != len(set(skills)):
        errors.append(f"{skill_map_path}: duplicate skill entries in `## Skill Index` section")
    return set(skills), errors


def parse_skill_index(skill_index_path: Path) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    if not skill_index_path.exists():
        return set(), [f"Missing required file: {skill_index_path}"]

    lines = skill_index_path.read_text(encoding="utf-8").splitlines()
    header: list[str] = []
    table_rows: list[list[str]] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        row = parse_markdown_table_line(line)
        if row and row[0] == "Skill":
            header = row
            continue
        if row and row[0] == "---":
            continue
        if header:
            table_rows.append(row)

    if not header:
        return set(), [f"{skill_index_path}: missing skill index table header"]
    for col in REQUIRED_SKILL_INDEX_COLUMNS:
        if col not in header:
            errors.append(f"{skill_index_path}: missing required column `{col}`")
    if len(header) != len(REQUIRED_SKILL_INDEX_COLUMNS):
        errors.append(f"{skill_index_path}: unexpected skill index column count")
    if not table_rows:
        errors.append(f"{skill_index_path}: no skill index rows found")
        return set(), errors

    skill_names: list[str] = []
    for row in table_rows:
        if len(row) != len(header):
            errors.append(f"{skill_index_path}: row has incorrect column count: {' | '.join(row)}")
            continue
        skill_name = row[0].strip().strip("`")
        trigger_skill_refs = re.findall(r"`([^`]+)`", row[2])
        canonical_artifacts = row[3].strip()
        last_updated = row[4].strip()

        if not skill_name:
            errors.append(f"{skill_index_path}: empty skill name in row")
            continue
        if canonical_artifacts == "":
            errors.append(f"{skill_index_path}: empty canonical artifacts for `{skill_name}`")
        if not UTC_REGEX.match(last_updated):
            errors.append(f"{skill_index_path}: invalid Last Updated UTC for `{skill_name}`: {last_updated}")

        skill_names.append(skill_name)

        # Validate only explicit backticked skill references in trigger companion column.
        for referenced in trigger_skill_refs:
            if referenced == "conditionals":
                continue
            if re.fullmatch(r"[a-z0-9-]+", referenced) is None:
                errors.append(f"{skill_index_path}: malformed referenced skill `{referenced}` in `{skill_name}` row")

    if len(skill_names) != len(set(skill_names)):
        errors.append(f"{skill_index_path}: duplicate skill rows detected")
    return set(skill_names), errors


def validate_agents(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"Missing required policy file: {path}"]
    content = path.read_text(encoding="utf-8")
    for snippet in REQUIRED_AGENTS_SNIPPETS:
        if snippet not in content:
            errors.append(f"AGENTS.md missing required snippet: {snippet}")
    return errors


def validate_required_file_snippets(skills_root: Path) -> list[str]:
    errors: list[str] = []
    for rel_path, snippets in REQUIRED_FILE_SNIPPETS.items():
        path = skills_root / rel_path
        if not path.exists():
            errors.append(f"Missing required file: {path}")
            continue
        content = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in content:
                errors.append(f"{path} missing required snippet: {snippet}")
    return errors


def validate_project_index_policy(path: Path) -> list[str]:
    try:
        validate_project_index(path)
    except ProjectIndexValidationError as exc:
        return [f"project index: {error}" for error in exc.errors]
    return []


def validate_skill_catalog_sync(skills_root: Path) -> list[str]:
    errors: list[str] = []
    actual_skills, catalog_errors = load_skill_catalog(skills_root)
    errors.extend(catalog_errors)

    catalog_path = skills_root / "skill-catalog.json"
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [*errors, f"Unable to load skill catalog for sync validation: {exc}"]
    if catalog.get("schema_version") == 2:
        try:
            catalog_skills = validate_catalog_v2(catalog, skills_root.parent)
        except CatalogError as exc:
            return [*errors, f"{catalog_path}: {exc}"]
        catalog_names = {item["name"] for item in catalog_skills}
        if actual_skills and actual_skills != catalog_names:
            errors.append(
                "Skill mismatch between actual skill files and skill-catalog.json "
                f"(actual={sorted(actual_skills)}, catalog={sorted(catalog_names)})"
            )
        for relative_path, expected in expected_routing_outputs(catalog, catalog_skills).items():
            output_path = skills_root.parent / relative_path
            if not output_path.is_file():
                errors.append(f"Missing generated routing view: {output_path}")
            elif output_path.read_text(encoding="utf-8") != expected:
                errors.append(
                    f"Generated routing view is stale: {output_path}; "
                    "run generate_routing_views.py"
                )
        return errors

    skill_map_skills, skill_map_errors = parse_skill_map_skills(skills_root / "SKILL-MAP.md")
    errors.extend(skill_map_errors)

    skill_index_skills, skill_index_errors = parse_skill_index(skills_root / "docs/skill-index.md")
    errors.extend(skill_index_errors)

    if actual_skills and skill_map_skills and actual_skills != skill_map_skills:
        errors.append(
            "Skill mismatch between actual skill files and SKILL-MAP.md "
            f"(actual={sorted(actual_skills)}, map={sorted(skill_map_skills)})"
        )
    if actual_skills and skill_index_skills and actual_skills != skill_index_skills:
        errors.append(
            "Skill mismatch between actual skill files and docs/skill-index.md "
            f"(actual={sorted(actual_skills)}, index={sorted(skill_index_skills)})"
        )

    if skill_index_skills:
        skill_index_path = skills_root / "docs/skill-index.md"
        lines = skill_index_path.read_text(encoding="utf-8").splitlines()
        for raw_line in lines:
            line = raw_line.strip()
            if not line.startswith("|") or line.startswith("| Skill"):
                continue
            row = parse_markdown_table_line(line)
            if len(row) < 3 or row[0] == "---":
                continue
            source_skill = row[0].strip().strip("`")
            for referenced_skill in re.findall(r"`([^`]+)`", row[2]):
                if referenced_skill == "conditionals":
                    continue
                if referenced_skill not in skill_index_skills:
                    errors.append(
                        f"{skill_index_path}: `{source_skill}` references unknown skill `{referenced_skill}` "
                        "in `Typical Triggers Another Skill`"
                    )
    return errors


def validate_machine_readable_catalog(skills_root: Path) -> list[str]:
    errors: list[str] = []
    path = skills_root / "skill-catalog.json"
    if not path.exists():
        return [f"Missing required machine-readable catalog: {path}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path}: invalid JSON: {exc}"]

    schema_version = data.get("schema_version")
    if schema_version not in {1, 2}:
        return [f"{path}: schema_version must be 1 or 2"]
    if schema_version == 2:
        schema_path = skills_root / "skill-catalog.schema.json"
        if not schema_path.is_file():
            return [f"Missing required catalog schema: {schema_path}"]
        try:
            schema_payload = json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return [f"{schema_path}: invalid JSON: {exc}"]
        if schema_payload.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{schema_path}: expected JSON Schema draft 2020-12")
        if data.get("$schema") != "./skill-catalog.schema.json":
            errors.append(f"{path}: schema v2 must reference ./skill-catalog.schema.json")
        try:
            validate_catalog_v2(data, skills_root.parent)
        except CatalogError as exc:
            errors.append(f"{path}: {exc}")
        return errors
    skills = data.get("skills")
    if not isinstance(skills, list) or not skills:
        errors.append(f"{path}: skills must be a non-empty list")
        return errors

    actual_skills, catalog_errors = load_skill_catalog(skills_root)
    errors.extend(catalog_errors)
    seen: set[str] = set()
    allowed_risk = {"low", "medium", "high"}

    for item in skills:
        if not isinstance(item, dict):
            errors.append(f"{path}: each skill entry must be an object")
            continue
        name = item.get("name")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9-]+", name):
            errors.append(f"{path}: skill entry has invalid name: {name}")
            continue
        if name in seen:
            errors.append(f"{path}: duplicate skill entry: {name}")
        seen.add(name)
        for field in ("trigger", "dependencies", "canonical_artifacts", "risk_level"):
            if field not in item:
                errors.append(f"{path}: `{name}` missing field `{field}`")
        if item.get("risk_level") not in allowed_risk:
            errors.append(f"{path}: `{name}` has invalid risk_level `{item.get('risk_level')}`")
        if not isinstance(item.get("dependencies"), list):
            errors.append(f"{path}: `{name}` dependencies must be a list")
        if (
            not isinstance(item.get("canonical_artifacts"), list) or not item.get("canonical_artifacts")
        ):
            errors.append(f"{path}: `{name}` canonical_artifacts must be a non-empty list")

    if actual_skills and seen != actual_skills:
        errors.append(
            "Skill mismatch between actual skill files and skill-catalog.json "
            f"(actual={sorted(actual_skills)}, catalog={sorted(seen)})"
        )
    return errors


def validate_skill_order_sync(skills_root: Path) -> list[str]:
    script_path = skills_root / "skill-governance/scripts/validate_skill_order_sync.py"
    if not script_path.exists():
        return [f"Missing required validator script: {script_path}"]
    try:
        subprocess.run(
            [sys.executable, str(script_path), "--skills-root", str(skills_root)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        output = (exc.stdout or "") + ("\n" + exc.stderr if exc.stderr else "")
        clean = output.strip() or "unknown failure"
        return [f"Skill order sync validation failed: {clean}"]
    return []


def _table_rows(lines: list[str], required_columns: list[str]) -> tuple[list[list[str]], list[str]]:
    errors: list[str] = []
    header_index = -1
    for index, line in enumerate(lines):
        if line.strip().startswith("|") and all(column in line for column in required_columns):
            header_index = index
            break
    if header_index < 0:
        return [], ["missing table header with columns: " + ", ".join(required_columns)]
    header = parse_markdown_table_line(lines[header_index])
    if header != required_columns:
        errors.append(
            "table columns are out of order or contain unexpected fields: "
            f"expected={required_columns}, actual={header}"
        )
    rows: list[list[str]] = []
    for line in lines[header_index + 2 :]:
        stripped = line.strip()
        if not stripped.startswith("|"):
            break
        cells = parse_markdown_table_line(stripped)
        if len(cells) != len(required_columns):
            errors.append("table row has incorrect column count")
            continue
        rows.append(cells)
    if not rows:
        errors.append("table has no data rows")
    return rows, errors


def _code_value(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 2 and stripped.startswith("`") and stripped.endswith("`"):
        return stripped[1:-1]
    return stripped


def validate_conflict_resolution_matrix(path: Path, catalog_path: Path) -> list[str]:
    """Require conflict-matrix owner labels to match typed catalog domains."""

    if not path.is_file():
        return [f"conflict matrix: missing required file: {path}"]
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"conflict matrix: cannot load catalog: {exc}"]
    if not isinstance(catalog, dict) or not isinstance(catalog.get("skills"), list):
        return ["conflict matrix: catalog lacks a skills array"]

    active_skills = {
        str(skill.get("name")): skill
        for skill in catalog["skills"]
        if isinstance(skill, dict) and skill.get("status") == "active"
    }
    domain_owners = {
        str(domain): name
        for name, skill in active_skills.items()
        for domain in skill.get("decision_domains", [])
    }
    allowed_policy_owners = {"router_policy.skill_budget": "task router"}
    allowed_labels = set(domain_owners) | set(allowed_policy_owners)

    rows, table_errors = _table_rows(path.read_text(encoding="utf-8").splitlines(), CONFLICT_MATRIX_COLUMNS)
    errors = [f"conflict matrix: {error}" for error in table_errors]
    seen: set[str] = set()
    for decision, raw_label, raw_owner, supporting in rows:
        label = _code_value(raw_label)
        owner = _code_value(raw_owner)
        if label in seen:
            errors.append(f"conflict matrix: duplicate domain or policy key `{label}`")
        seen.add(label)
        if label not in allowed_labels:
            errors.append(
                f"conflict matrix: `{decision}` uses unknown domain or policy key `{label}`"
            )
            continue
        expected_owner = domain_owners.get(label, allowed_policy_owners.get(label))
        if owner != expected_owner:
            errors.append(
                f"conflict matrix: `{label}` owner must be `{expected_owner}`, found `{owner}`"
            )
        unknown_supporters = sorted(
            name
            for name in re.findall(r"`([a-z0-9-]+)`", supporting)
            if name not in active_skills
        )
        if unknown_supporters:
            errors.append(
                f"conflict matrix: `{label}` has unknown supporting skills: "
                + ", ".join(unknown_supporters)
            )
    return errors


def validate_user_instructions(path: Path, compatibility_path: Path | None = None) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"Missing required instruction ledger: {path}"]

    content = path.read_text(encoding="utf-8")
    if "# User Instructions Ledger" not in content:
        errors.append("user-instructions.md missing title '# User Instructions Ledger'")
    if "## Current Directives" not in content:
        errors.append("user-instructions.md missing '## Current Directives' section")
    if "## Fulfillment Status Model" not in content:
        errors.append("user-instructions.md missing '## Fulfillment Status Model' section")
    if "## Fulfillment History" not in content:
        errors.append("user-instructions.md missing '## Fulfillment History' section")
    lines = content.splitlines()
    current_rows, current_errors = _table_rows(lines, REQUIRED_CURRENT_DIRECTIVE_COLUMNS)
    errors.extend(f"current directives: {error}" for error in current_errors)
    seen_current: set[str] = set()
    for cells in current_rows:
        instruction_id, _, _, lifecycle, _, _, confirmed, notes = cells
        if not re.fullmatch(r"INST-\d{3}", instruction_id):
            errors.append(f"current directives invalid instruction id: {instruction_id}")
        if instruction_id in seen_current:
            errors.append(f"current directives duplicate instruction id: {instruction_id}")
        seen_current.add(instruction_id)
        if lifecycle not in ALLOWED_DIRECTIVE_LIFECYCLES:
            errors.append(f"current directives invalid lifecycle: {lifecycle}")
        if not UTC_REGEX.match(confirmed):
            errors.append("current directives Last Confirmed UTC must be ISO-8601 UTC")
        if lifecycle != "active" and not notes:
            errors.append(f"current directives {lifecycle} row requires successor or notes")

    history_rows, history_errors = _table_rows(lines, REQUIRED_USER_INSTRUCTIONS_COLUMNS)
    errors.extend(f"fulfillment history: {error}" for error in history_errors)
    seen_history: set[str] = set()
    for cells in history_rows:
        instruction_id, _, _, status, _, _, updated, evidence, notes = cells
        if not re.fullmatch(r"INST-\d{3}", instruction_id):
            errors.append(f"fulfillment history invalid instruction id: {instruction_id}")
        if instruction_id in seen_history:
            errors.append(f"fulfillment history duplicate instruction id: {instruction_id}")
        seen_history.add(instruction_id)
        if status not in ALLOWED_STATUSES:
            errors.append(f"fulfillment history invalid status: {status}")
        if not UTC_REGEX.match(updated):
            errors.append("fulfillment history Last Updated UTC must be ISO-8601 UTC")
        if status == "done" and not evidence:
            errors.append("fulfillment history done row missing evidence")
        if status in {"blocked", "won_t_do"} and not notes:
            errors.append(f"fulfillment history {status} row missing notes")

    if compatibility_path is not None:
        if not compatibility_path.is_file():
            errors.append(f"Missing instruction ledger compatibility pointer: {compatibility_path}")
        else:
            compatibility = compatibility_path.read_text(encoding="utf-8")
            if "../user-instructions.md" not in compatibility or "compatibility" not in compatibility.lower():
                errors.append(
                    f"Instruction ledger compatibility pointer is invalid: {compatibility_path}"
                )
    return errors


def validate_artifact_pair(json_path: Path) -> list[str]:
    errors: list[str] = []
    md_path = json_path.with_suffix("").with_suffix(".governance.md")
    if not md_path.exists():
        errors.append(f"Missing markdown pair for governance artifact: {md_path}")
        return errors
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Invalid governance artifact JSON {json_path}: {exc}"]
    if not isinstance(data, dict):
        return [f"Governance artifact root must be an object: {json_path}"]
    startup = data.get("startup_declaration", {})
    for field in (
        "quizme_mode",
        "quizme_multiple_choice",
        "quizme_one_at_a_time",
        "quizme_confirm",
        "quizme_record",
    ):
        if field not in data:
            errors.append(f"{json_path}: missing field {field}")
    for field in ("skills_in_use", "skills_selection_rationale", "skills_execution_order"):
        if field not in startup:
            errors.append(f"{json_path}: startup_declaration missing field {field}")
    md_content = md_path.read_text(encoding="utf-8")
    for marker in ("## Startup Declaration", "### Skills In Use", "### Skill Execution Order"):
        if marker not in md_content:
            errors.append(f"{md_path}: missing section marker {marker}")
    for marker in (
        "`quizme_mode`",
        "`quizme_multiple_choice`",
        "`quizme_one_at_a_time`",
        "`quizme_confirm`",
        "`quizme_record`",
    ):
        if marker not in md_content:
            errors.append(f"{md_path}: missing quizme state marker {marker}")
    schema_version = data.get("schema_version", 1)
    if schema_version in {2, 3}:
        if "change_binding" not in data:
            errors.append(f"{json_path}: content-bound artifact missing change_binding")
        for marker in (
            f"`schema_version`: {schema_version}",
            "## Change Binding",
            "`manifest_sha256`",
        ):
            if marker not in md_content:
                errors.append(f"{md_path}: content-bound pair missing marker {marker}")
    if schema_version == 3:
        try:
            canonical_markdown = render_governance_markdown(
                GovernanceArtifact(**data)
            ) + "\n"
        except (AttributeError, KeyError, TypeError, ValueError) as exc:
            errors.append(
                f"{json_path}: schema v3 artifact cannot be rendered canonically: {exc}"
            )
        else:
            if md_content != canonical_markdown:
                errors.append(
                    f"{md_path}: schema v3 Markdown pair does not equal the canonical "
                    "generator rendering of its JSON"
                )
    return errors


def collect_target_artifacts(governance_dir: Path, changed: list[str], repo_root: Path) -> list[Path]:
    if changed:
        selected: list[Path] = []
        for file_path in changed:
            if fnmatch.fnmatch(file_path, "docs/governance/*.governance.json"):
                candidate = repo_root / file_path
                if candidate.is_file():
                    selected.append(candidate)
        return sorted(set(selected))
    if not governance_dir.exists():
        return []
    return sorted(governance_dir.glob("*.governance.json"))


def validate_artifact_inventory(
    artifacts: list[Path],
    *,
    minimum: int,
    governance_dir: Path,
    filtered_diff: bool,
) -> list[str]:
    if filtered_diff or len(artifacts) >= minimum:
        return []
    return [
        "governance artifact inventory is unexpectedly empty or incomplete: "
        f"found {len(artifacts)}, require at least {minimum} in {governance_dir}"
    ]


def main() -> None:
    args = parse_args()
    if args.minimum_governance_artifacts < 0:
        raise SystemExit("--minimum-governance-artifacts must be zero or greater")
    skills_root = Path(args.skills_root).resolve()
    repo_root = discover_repo_root(args.repo_root, skills_root)
    agents_path = resolve_agents_path(args.agents_path, skills_root, repo_root)
    governance_dir = Path(args.governance_dir)
    if not governance_dir.is_absolute():
        governance_dir = repo_root / governance_dir

    errors: list[str] = []
    errors.extend(validate_agents(agents_path))
    errors.extend(validate_required_file_snippets(skills_root))
    errors.extend(validate_skill_catalog_sync(skills_root))
    errors.extend(validate_machine_readable_catalog(skills_root))
    errors.extend(validate_skill_order_sync(skills_root))
    errors.extend(
        validate_conflict_resolution_matrix(
            skills_root / "docs" / "conflict-resolution-matrix.md",
            skills_root / "skill-catalog.json",
        )
    )
    errors.extend(validate_project_index_policy(repo_root / "docs" / "project-index.md"))
    errors.extend(
        validate_user_instructions(
            repo_root / "user-instructions.md",
            compatibility_path=skills_root / "user-instructions.md",
        )
    )
    remote_policy_path = repo_root / ".github" / "branch-protection-policy.json"
    if remote_policy_path.exists():
        errors.extend(
            f"remote branch-protection policy: {error}"
            for error in validate_remote_policy_file(remote_policy_path)
        )

    changed = changed_files(args.base_sha, args.head_sha, repo_root)
    artifacts = collect_target_artifacts(governance_dir, changed, repo_root)
    errors.extend(
        validate_artifact_inventory(
            artifacts,
            minimum=args.minimum_governance_artifacts,
            governance_dir=governance_dir,
            filtered_diff=bool(changed),
        )
    )
    for artifact in artifacts:
        errors.extend(validate_artifact_pair(artifact))

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        raise SystemExit(1)

    print("Skill policy validation passed.")
    print(f"Skills root: {skills_root}")
    print(f"Repo root: {repo_root}")
    print(f"Checked AGENTS file: {agents_path}")
    print(f"Checked {len(artifacts)} governance artifact(s).")


if __name__ == "__main__":
    main()
