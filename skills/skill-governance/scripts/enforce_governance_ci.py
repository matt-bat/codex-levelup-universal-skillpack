#!/usr/bin/env python3
"""CI enforcement for governance artifacts based on changed files."""

from __future__ import annotations

import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_SKILLS_ROOT = SCRIPT_PATH.parents[2]

GOVERNED_PATH_PREFIXES = (
    ".codex/skills/",
    "skills/",
    "docs/governance/",
    ".github/workflows/",
)

GOVERNED_PATH_EXACT = {
    "AGENTS.md",
    "docs/project-index.md",
}

GOVERNANCE_ARTIFACT_PATTERN = "docs/governance/*.governance.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-sha", required=True)
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--skills-root", default=str(DEFAULT_SKILLS_ROOT))
    parser.add_argument("--repo-root", default="")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Require all required gates to be complete for changed artifacts.",
    )
    parser.add_argument(
        "--require-recommendation",
        choices=["go", "go-with-risk", "no-go"],
        default="go",
    )
    return parser.parse_args()


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout.strip()


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


def changed_files(base_sha: str, head_sha: str, repo_root: Path) -> list[str]:
    commands = [
        ["git", "-C", str(repo_root), "diff", "--name-only", "--diff-filter=ACMRTUXB", f"{base_sha}...{head_sha}"],
        ["git", "-C", str(repo_root), "diff", "--name-only", "--diff-filter=ACMRTUXB", f"{base_sha}..{head_sha}"],
        ["git", "-C", str(repo_root), "diff", "--name-only", "--diff-filter=ACMRTUXB", head_sha],
    ]
    for cmd in commands:
        try:
            output = run(cmd)
            if not output:
                return []
            return [line.strip() for line in output.splitlines() if line.strip()]
        except subprocess.CalledProcessError:
            continue
    raise SystemExit("Unable to compute changed files for governance enforcement.")


def is_governed_change(path: str) -> bool:
    normalized = path.strip()
    if normalized in GOVERNED_PATH_EXACT:
        return True
    return any(normalized.startswith(prefix) for prefix in GOVERNED_PATH_PREFIXES)


def changed_governance_artifacts(files: list[str]) -> list[str]:
    artifacts = []
    for path in files:
        if fnmatch.fnmatch(path, GOVERNANCE_ARTIFACT_PATTERN):
            artifacts.append(path)
    return artifacts


def run_policy_validators(skills_root: Path, repo_root: Path) -> None:
    policy_validator = skills_root / "skill-governance/scripts/validate_skill_policy.py"
    order_validator = skills_root / "skill-governance/scripts/validate_skill_order_sync.py"
    if not policy_validator.exists():
        raise SystemExit(f"Validator not found: {policy_validator}")
    if not order_validator.exists():
        raise SystemExit(f"Validator not found: {order_validator}")

    subprocess.run(
        [
            sys.executable,
            str(policy_validator),
            "--skills-root",
            str(skills_root),
            "--repo-root",
            str(repo_root),
        ],
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(order_validator),
            "--skills-root",
            str(skills_root),
        ],
        check=True,
    )


def validate_artifacts(
    artifacts: list[str],
    strict: bool,
    require_recommendation: str,
    skills_root: Path,
    repo_root: Path,
) -> None:
    validator = skills_root / "skill-governance/scripts/validate_governance_artifact.py"
    if not validator.exists():
        raise SystemExit(f"Validator not found: {validator}")

    for artifact in artifacts:
        artifact_path = repo_root / artifact
        cmd = [
            sys.executable,
            str(validator),
            "--artifact",
            str(artifact_path),
            "--require-recommendation",
            require_recommendation,
            "--project-index-path",
            str(repo_root / "docs/project-index.md"),
        ]
        if strict:
            cmd.append("--strict")
        print(f"Validating artifact: {artifact_path} (strict={strict})")
        subprocess.run(cmd, check=True)


def main() -> None:
    args = parse_args()
    skills_root = Path(args.skills_root).resolve()
    repo_root = discover_repo_root(args.repo_root, skills_root)

    print(f"Running skill policy validators for skills root: {skills_root}")
    run_policy_validators(skills_root, repo_root)

    files = changed_files(args.base_sha, args.head_sha, repo_root)
    if not files:
        print("No changed files detected.")
        return

    governed = [path for path in files if is_governed_change(path)]
    artifacts = changed_governance_artifacts(files)

    print(f"Changed files: {len(files)}")
    print(f"Governed changed files: {len(governed)}")
    print(f"Changed governance artifacts: {len(artifacts)}")

    if governed and not artifacts:
        print("ERROR: Governed changes detected without a changed governance artifact.")
        print("Add/update a file matching docs/governance/*.governance.json")
        for path in governed:
            print(f" - {path}")
        raise SystemExit(1)

    if artifacts:
        validate_artifacts(
            artifacts,
            strict=args.strict,
            require_recommendation=args.require_recommendation,
            skills_root=skills_root,
            repo_root=repo_root,
        )
    else:
        print("No governance artifact changes required for this diff.")


if __name__ == "__main__":
    main()
