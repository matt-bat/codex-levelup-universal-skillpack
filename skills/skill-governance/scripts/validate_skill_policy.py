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
DEFAULT_SKILLS_ROOT = SCRIPT_PATH.parents[2]
UTC_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

REQUIRED_AGENTS_SNIPPETS = [
    "## Agent Default Skill Policy",
    "### Baseline Skills (Default)",
    "### Conditional Skill Triggers",
    "### Startup Declaration (Required)",
    "Skills in use",
    "execution order",
    "reason each skill",
    "local-first execution; no deployment unless explicitly requested",
    "`token-reduction`",
    "`order-of-operations`",
    "`thoughtful-approach`",
    "`thoroughly-rate-review`",
    "`user-instructions-tracker`",
    "`governance-enforcement`",
    "`requirement-clarifier`",
    "`quizme-mode`",
    "`--quizme`",
    "`--mc`",
    "`--one-at-a-time`",
    "`--confirm`",
    "`--record`",
    "`semantic-policy-audit`",
    "`history-indexing`",
    "user-instructions.md",
]

REQUIRED_FILE_SNIPPETS = {
    "skill-catalog.json": [
        "\"schema_version\"",
        "\"skills\"",
        "\"skill-governance\"",
    ],
    "docs/skill-decision-tree.md": [
        "# Skill Decision Tree",
        "Use the smallest skill set that covers the task.",
        "## Stop Rules",
    ],
    "docs/known-limitations.md": [
        "# Known Limitations",
        "Model Compliance",
        "Semantic Quality",
    ],
    "docs/install-profiles.md": [
        "# Install Profiles",
        "## Minimal",
        "## Governed",
    ],
    "docs/conflict-resolution-matrix.md": [
        "# Conflict Resolution Matrix",
        "process-budget-controller",
        "deprecation-management",
    ],
    "docs/validator-severity-levels.md": [
        "# Validator Severity Levels",
        "`error`",
        "`warning`",
    ],
    "docs/rubrics/skillpack-quality-rubric.md": [
        "# Skillpack Quality Rubric",
        "Restraint",
        "Enforceability",
    ],
    "thoroughly-rate-review/SKILL.md": [
        "Integration and Cohesiveness",
        "for multi-skill systems/frameworks, `Integration and Cohesiveness` is required and cannot be omitted",
    ],
    "pseudo-agentic-automation/SKILL.md": [
        "for new projects (model has not worked on before), ask whether model should run tests/build by default or user will run them to save tokens",
        "operate locally by default; do not deploy unless explicitly requested",
    ],
    "skill-governance/SKILL.md": [
        "### Conditional Gate Additions (All Modes)",
        "`requirement-clarifier`",
        "`thoughtful-approach`",
        "`thoroughly-rate-review`",
        "`semantic-policy-audit`",
        "`user-instructions-tracker`",
        "`effective-testing-methods`",
        "`file-structure-optimization`",
        "`file-maintenance`",
        "`quizme-mode`",
        "`--quizme-mode on`",
        "`--quizme-mc`",
        "`--quizme-one-at-a-time`",
        "`--quizme-confirm`",
        "`--quizme-record`",
        "Use [Governance Enforcement](../governance-enforcement/SKILL.md) for:",
        "consult `docs/skill-index.md`",
    ],
    "effective-testing-methods/SKILL.md": [
        "# Effective Testing Methods",
        "Unit Test Patterns",
        "Playwright Patterns",
        "Use [Regression Prevention](../regression-prevention/SKILL.md) for:",
    ],
    "file-structure-optimization/SKILL.md": [
        "# File Structure Optimization",
        "Structure Audit",
        "Normalization Rules",
        "Use [Doc Maintenance](../doc-maintenance/SKILL.md) and [File Maintenance](../file-maintenance/SKILL.md) for:",
    ],
    "file-maintenance/SKILL.md": [
        "# File Maintenance",
        "Factuality and Freshness Checks",
        "Duplicate and Staleness Control",
        "Use [Doc Maintenance](../doc-maintenance/SKILL.md) for:",
    ],
    "order-of-operations/SKILL.md": [
        "consult `docs/skill-index.md`",
    ],
    "doc-maintenance/SKILL.md": [
        "`docs/skill-index.md` (cross-skill trigger routing)",
    ],
    "user-instructions-tracker/SKILL.md": [
        "Required file:",
        "`user-instructions.md` at repository root",
        "Allowed status values:",
        "`pending`",
        "`in_progress`",
        "`blocked`",
        "`done`",
        "`won_t_do`",
        "`docs/skill-index.md`",
    ],
    "token-reduction/SKILL.md": [
        "Use [History Indexing](../history-indexing/SKILL.md) for:",
    ],
    "history-indexing/SKILL.md": [
        "Canonical Artifact",
        "`docs/chat-history-index.md`",
        "Skill Index",
    ],
    "governance-enforcement/SKILL.md": [
        "Scope Boundary",
        "Use [Skill Governance](../skill-governance/SKILL.md) for:",
    ],
    "requirement-clarifier/SKILL.md": [
        "Clarification Contract",
        "Acceptance Criteria",
        "Quizme Mode",
    ],
    "quizme-mode/SKILL.md": [
        "# Quizme Mode",
        "`--quizme` toggles quizme mode on when off",
        "supported arguments are `--mc`, `--one-at-a-time`, `--confirm`, and `--record`",
        "prefer the interactive clarification console for quizme questions",
        "do not start implementation, mutation, or governed execution until the clarification gate passes",
    ],
    "semantic-policy-audit/SKILL.md": [
        "Audit Dimensions",
        "expected-vs-observed",
    ],
    "regression-prevention/SKILL.md": [
        "Use [Effective Testing Methods](../effective-testing-methods/SKILL.md) for detailed patterns when amending or adding unit and Playwright tests.",
    ],
    "SKILL-MAP.md": [
        "Cross-skill trigger routing",
        "docs/skill-index.md",
        "Canonical Routing Artifact",
    ],
    "docs/skill-index.md": [
        "# Skill Index",
        "## Cross-Skill Trigger Rule (Required)",
        "`quizme-mode`",
    ],
    "skill-governance/scripts/validate_skill_order_sync.py": [
        "Skill ordering sync validation passed.",
    ],
}

REQUIRED_ANTI_OVERUSE_SKILLS = {
    "artifact-budget-enforcement",
    "conversation-retention-summary",
    "deprecation-management",
    "doc-maintenance",
    "file-maintenance",
    "history-indexing",
    "process-budget-controller",
    "quizme-mode",
    "skill-governance",
    "skill-usage-review",
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

REQUIRED_SKILL_INDEX_COLUMNS = [
    "Skill",
    "Primary Trigger",
    "Typical Triggers Another Skill",
    "Canonical Artifacts",
    "Last Updated UTC",
]

ALLOWED_STATUSES = {"pending", "in_progress", "blocked", "done", "won_t_do"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents-path", default="AGENTS.md")
    parser.add_argument("--governance-dir", default="docs/governance")
    parser.add_argument("--skills-root", default=str(DEFAULT_SKILLS_ROOT))
    parser.add_argument("--repo-root", default="")
    parser.add_argument("--base-sha", default="")
    parser.add_argument("--head-sha", default="")
    return parser.parse_args()


def discover_repo_root(repo_root_arg: str, skills_root: Path) -> Path:
    if repo_root_arg.strip():
        return Path(repo_root_arg).resolve()
    try:
        result = subprocess.run(
            ["git", "-C", str(skills_root), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        return Path(result.stdout.strip()).resolve()
    except subprocess.CalledProcessError:
        return skills_root.parents[1]


def resolve_agents_path(raw_path: str, skills_root: Path, repo_root: Path) -> Path:
    candidates = []
    candidate = Path(raw_path)
    if candidate.is_absolute():
        candidates.append(candidate)
    else:
        candidates.extend(
            [
                Path.cwd() / candidate,
                skills_root / candidate,
                repo_root / candidate,
            ]
        )
    for parent in [repo_root, *repo_root.parents]:
        candidates.append(parent / "AGENTS.md")

    seen = set()
    for item in candidates:
        resolved = item.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.exists():
            return resolved
    return Path(raw_path)


def changed_files(base_sha: str, head_sha: str, repo_root: Path) -> list[str]:
    if not base_sha or not head_sha:
        return []
    commands = [
        ["git", "-C", str(repo_root), "diff", "--name-only", "--diff-filter=ACMRTUXB", f"{base_sha}...{head_sha}"],
        ["git", "-C", str(repo_root), "diff", "--name-only", "--diff-filter=ACMRTUXB", f"{base_sha}..{head_sha}"],
        ["git", "-C", str(repo_root), "diff", "--name-only", "--diff-filter=ACMRTUXB", head_sha],
    ]
    for cmd in commands:
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            output = result.stdout.strip()
            if not output:
                return []
            return [line.strip() for line in output.splitlines() if line.strip()]
        except subprocess.CalledProcessError:
            continue
    return []


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


def validate_skill_catalog_sync(skills_root: Path) -> list[str]:
    errors: list[str] = []
    actual_skills, catalog_errors = load_skill_catalog(skills_root)
    errors.extend(catalog_errors)

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

    if data.get("schema_version") != 1:
        errors.append(f"{path}: schema_version must be 1")
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
        if not isinstance(item.get("canonical_artifacts"), list) or not item.get("canonical_artifacts"):
            errors.append(f"{path}: `{name}` canonical_artifacts must be a non-empty list")

    if actual_skills and seen != actual_skills:
        errors.append(
            "Skill mismatch between actual skill files and skill-catalog.json "
            f"(actual={sorted(actual_skills)}, catalog={sorted(seen)})"
        )
    return errors


def validate_anti_overuse_sections(skills_root: Path) -> list[str]:
    errors: list[str] = []
    for skill_name in sorted(REQUIRED_ANTI_OVERUSE_SKILLS):
        path = skills_root / skill_name / "SKILL.md"
        if not path.exists():
            errors.append(f"Missing required skill file: {path}")
            continue
        content = path.read_text(encoding="utf-8")
        for snippet in ("## Anti-Overuse Rules", "Use when:", "Do not use when:", "Stop after:"):
            if snippet not in content:
                errors.append(f"{path} missing anti-overuse snippet: {snippet}")
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


def validate_user_instructions(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"Missing required tracker file: {path}"]

    content = path.read_text(encoding="utf-8")
    if "# User Instructions Tracker" not in content:
        errors.append("user-instructions.md missing title '# User Instructions Tracker'")
    if "## Status Model" not in content:
        errors.append("user-instructions.md missing '## Status Model' section")
    if "## Tracker" not in content:
        errors.append("user-instructions.md missing '## Tracker' section")

    lines = content.splitlines()
    header_line = ""
    for line in lines:
        if line.strip().startswith("|") and "Instruction ID" in line and "Last Updated UTC" in line:
            header_line = line
            break
    if not header_line:
        errors.append("user-instructions.md missing tracker table header")
        return errors

    for col in REQUIRED_USER_INSTRUCTIONS_COLUMNS:
        if col not in header_line:
            errors.append(f"user-instructions.md tracker header missing column: {col}")

    in_table = False
    seen_instruction_ids: set[str] = set()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and "Instruction ID" in stripped:
            in_table = True
            continue
        if in_table and stripped.startswith("|---"):
            continue
        if in_table and stripped.startswith("|"):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if len(cells) != len(REQUIRED_USER_INSTRUCTIONS_COLUMNS):
                errors.append("user-instructions.md tracker row has incorrect column count")
                continue
            instruction_id = cells[0]
            status = cells[3]
            last_updated_utc = cells[6]
            evidence = cells[7]
            notes = cells[8]

            if not re.fullmatch(r"INST-\d{3}", instruction_id):
                errors.append(f"user-instructions.md invalid instruction id format: {instruction_id}")
            if instruction_id in seen_instruction_ids:
                errors.append(f"user-instructions.md duplicate instruction id: {instruction_id}")
            seen_instruction_ids.add(instruction_id)
            if status not in ALLOWED_STATUSES:
                errors.append(f"user-instructions.md invalid status value: {status}")
            if not UTC_REGEX.match(last_updated_utc):
                errors.append("user-instructions.md Last Updated UTC must be ISO-8601 UTC like 2026-05-13T06:10:00Z")
            if status == "done" and not evidence:
                errors.append("user-instructions.md done row missing evidence")
            if status in {"blocked", "won_t_do"} and not notes:
                errors.append(f"user-instructions.md {status} row missing notes")
        elif in_table and stripped and not stripped.startswith("|"):
            break

    if in_table and not seen_instruction_ids:
        errors.append("user-instructions.md tracker table has no data rows")
    return errors


def validate_artifact_pair(json_path: Path) -> list[str]:
    errors: list[str] = []
    md_path = json_path.with_suffix("").with_suffix(".governance.md")
    if not md_path.exists():
        errors.append(f"Missing markdown pair for governance artifact: {md_path}")
        return errors
    data = json.loads(json_path.read_text(encoding="utf-8"))
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
    return errors


def collect_target_artifacts(governance_dir: Path, changed: list[str], repo_root: Path) -> list[Path]:
    if changed:
        selected: list[Path] = []
        for file_path in changed:
            if fnmatch.fnmatch(file_path, "docs/governance/*.governance.json"):
                selected.append(repo_root / file_path)
        return sorted(set(selected))
    if not governance_dir.exists():
        return []
    return sorted(governance_dir.glob("*.governance.json"))


def main() -> None:
    args = parse_args()
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
    errors.extend(validate_anti_overuse_sections(skills_root))
    errors.extend(validate_skill_order_sync(skills_root))
    errors.extend(validate_user_instructions(skills_root / "user-instructions.md"))

    changed = changed_files(args.base_sha, args.head_sha, repo_root)
    artifacts = collect_target_artifacts(governance_dir, changed, repo_root)
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
