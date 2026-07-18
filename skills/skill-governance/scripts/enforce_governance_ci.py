#!/usr/bin/env python3
"""Fail-closed CI enforcement for change-bound governance evidence."""

from __future__ import annotations

import argparse
import ast
import fnmatch
import hashlib
import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_DIR = SCRIPT_PATH.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from governance_common import (  # noqa: E402
    SCHEMA_V2,
    SCHEMA_V3,
    build_manifest,
    diff_name_status,
    discover_repo_root,
    is_governance_artifact_path,
    is_governed_change,
    manifest_sha256,
    resolve_commit,
    run_git,
)
from validate_governance_artifact import (  # noqa: E402
    AUTHORIZED_OPERATIONS,
    artifact_schema_version,
    validate_artifact_data,
)


DEFAULT_SKILLS_ROOT = SCRIPT_PATH.parents[2]
GOVERNANCE_ARTIFACT_PATTERN = "docs/governance/*.governance.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-sha", default="")
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--skills-root", default=str(DEFAULT_SKILLS_ROOT))
    parser.add_argument("--repo-root", default="")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Require all required gates to be complete for bound artifacts.",
    )
    parser.add_argument(
        "--require-recommendation",
        choices=["go", "go-with-risk", "no-go"],
        default="go",
    )
    parser.add_argument(
        "--release-check",
        action="store_true",
        help=(
            "Find one strict v3 release artifact whose recorded base and full manifest bind the exact release head. "
            "This mode does not publish or mutate remote settings."
        ),
    )
    parser.add_argument(
        "--attestation-out",
        default="",
        help="Optional path for a CI-generated exact-head JSON attestation.",
    )
    return parser.parse_args()


def changed_files(base_sha: str, head_sha: str, repo_root: Path) -> list[str]:
    """Compatibility helper returning exact diff paths, including deletions."""
    _, _, changes = diff_name_status(repo_root, base_sha, head_sha)
    return [path for _, path in changes]


def changed_governance_artifacts(files: list[str]) -> list[str]:
    return sorted(path for path in files if fnmatch.fnmatch(path, GOVERNANCE_ARTIFACT_PATTERN))


def run_policy_validators(skills_root: Path, repo_root: Path) -> None:
    policy_validator = skills_root / "skill-governance/scripts/validate_skill_policy.py"
    order_validator = skills_root / "skill-governance/scripts/validate_skill_order_sync.py"
    if not policy_validator.is_file():
        raise SystemExit(f"Validator not found: {policy_validator}")
    if not order_validator.is_file():
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
        [sys.executable, str(order_validator), "--skills-root", str(skills_root)],
        check=True,
    )


def require_clean_exact_checkout(repo_root: Path) -> None:
    output = run_git(repo_root, ["status", "--porcelain=v1", "-z", "--untracked-files=all"])
    assert isinstance(output, bytes)
    if output:
        changed = [
            entry.decode("utf-8", errors="replace")
            for entry in output.split(b"\0")
            if entry
        ]
        preview = ", ".join(changed[:5])
        suffix = "" if len(changed) <= 5 else f" (+{len(changed) - 5} more)"
        raise SystemExit(
            "Exact-head enforcement requires a clean checkout so policy validation cannot read "
            f"unattested working-tree content: {preview}{suffix}"
        )


def _head_bytes(repo_root: Path, head_sha: str, path: str) -> bytes:
    output = run_git(repo_root, ["show", f"{head_sha}:{path}"])
    assert isinstance(output, bytes)
    return output


def _head_json(repo_root: Path, head_sha: str, path: str) -> tuple[dict[str, Any], bytes]:
    raw = _head_bytes(repo_root, head_sha, path)
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Governance artifact at exact head is invalid JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Governance artifact root must be an object: {path}")
    return data, raw


def _validate_artifact(
    path: str,
    data: dict[str, Any],
    *,
    strict: bool,
    require_recommendation: str,
) -> None:
    errors, warnings = validate_artifact_data(
        data,
        strict=strict,
        require_recommendation=require_recommendation,
    )
    for warning in warnings:
        print(f"WARNING: {path}: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {path}: {error}")
        raise SystemExit(f"Governance artifact validation failed: {path}")


def binding_errors(data: dict[str, Any], resolved_base: str, actual_manifest: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if artifact_schema_version(data) not in {SCHEMA_V2, SCHEMA_V3}:
        return ["only content-bound schema v2 or v3 artifacts have change bindings"]
    binding = data.get("change_binding")
    if not isinstance(binding, dict):
        return ["content-bound artifact has no change_binding object"]
    if binding.get("base_sha") != resolved_base:
        errors.append(
            "change_binding.base_sha does not match the exact enforced base "
            f"(artifact={binding.get('base_sha')!r}, actual={resolved_base!r})"
        )
    if binding.get("manifest") != actual_manifest:
        errors.append("change_binding.manifest does not match the exact governed diff")
    actual_digest = manifest_sha256(actual_manifest)
    if binding.get("manifest_sha256") != actual_digest:
        errors.append(
            "change_binding.manifest_sha256 does not match the exact governed diff digest"
        )
    return errors


def catalog_binding_errors(
    data: dict[str, Any],
    repo_root: Path,
    head_sha: str,
) -> list[str]:
    """Bind v3 startup semantics to the exact catalog at the enforced head."""
    if artifact_schema_version(data) != SCHEMA_V3:
        return []
    binding = data.get("catalog_binding")
    if not isinstance(binding, dict):
        return ["schema v3 artifact has no catalog_binding object"]
    path = binding.get("path")
    if not isinstance(path, str):
        return ["catalog_binding.path must be a repository-relative string"]
    try:
        raw = _head_bytes(repo_root, head_sha, path)
        catalog = json.loads(raw)
    except (SystemExit, json.JSONDecodeError) as exc:
        return [f"catalog_binding.path cannot be verified at the enforced head: {exc}"]
    errors: list[str] = []
    if hashlib.sha256(raw).hexdigest() != binding.get("sha256"):
        errors.append("catalog_binding.sha256 does not match the exact catalog at the enforced head")
    if str(catalog.get("catalog_version")) != binding.get("catalog_version"):
        errors.append("catalog_binding.catalog_version does not match the exact catalog")
    if str(catalog.get("router_contract")) != binding.get("router_contract"):
        errors.append("catalog_binding.router_contract does not match the exact catalog")
    return errors


def _head_governance_test_count(repo_root: Path, head_sha: str) -> int:
    output = run_git(
        repo_root,
        [
            "ls-tree",
            "-r",
            "--name-only",
            "-z",
            head_sha,
            "--",
            "skills/skill-governance/tests",
        ],
    )
    assert isinstance(output, bytes)
    paths = sorted(
        raw.decode("utf-8", errors="strict")
        for raw in output.split(b"\0")
        if raw and raw.rsplit(b"/", 1)[-1].startswith(b"test_") and raw.endswith(b".py")
    )
    count = 0
    for path in paths:
        try:
            tree = ast.parse(_head_bytes(repo_root, head_sha, path).decode("utf-8"), filename=path)
        except (UnicodeDecodeError, SyntaxError) as exc:
            raise SystemExit(f"Unable to inventory governance tests at release head: {path}: {exc}") from exc
        count += sum(
            1
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        )
    return count


def release_metadata_errors(
    data: dict[str, Any],
    repo_root: Path,
    head_sha: str,
    manifest: list[dict[str, Any]],
) -> list[str]:
    if data.get("purpose") != "release":
        return []
    metadata = data.get("release_metadata")
    if not isinstance(metadata, dict):
        return ["release artifact has no release_metadata object"]
    errors: list[str] = []
    try:
        version = _head_bytes(repo_root, head_sha, str(metadata.get("version_path"))).decode(
            "utf-8"
        ).strip()
        changelog = _head_bytes(
            repo_root, head_sha, str(metadata.get("changelog_path"))
        ).decode("utf-8")
        notes = _head_bytes(
            repo_root, head_sha, str(metadata.get("release_notes_path"))
        ).decode("utf-8")
        catalog = json.loads(_head_bytes(repo_root, head_sha, "skills/skill-catalog.json"))
    except (SystemExit, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"release metadata files cannot be verified at the exact head: {exc}"]

    recorded_version = metadata.get("version")
    recorded_tag = metadata.get("tag")
    if version != recorded_version:
        errors.append("release_metadata.version does not match the exact version file")
    if recorded_tag != f"v{recorded_version}":
        errors.append("release_metadata.tag does not equal v<version>")
    if not re.search(
        rf"^## \[{re.escape(str(recorded_version))}\] - \d{{4}}-\d{{2}}-\d{{2}}$",
        changelog,
        flags=re.MULTILINE,
    ):
        errors.append("release changelog lacks a dated heading for the exact version")

    actual_skill_count = len(catalog.get("skills", []))
    actual_test_count = _head_governance_test_count(repo_root, head_sha)
    if metadata.get("skill_count") != actual_skill_count:
        errors.append("release_metadata.skill_count does not match the exact catalog")
    if metadata.get("governance_test_count") != actual_test_count:
        errors.append("release_metadata.governance_test_count does not match the exact test tree")
    for marker in (
        str(recorded_tag),
        f"- Skill count: `{actual_skill_count}`",
        f"- Governance test count: `{actual_test_count}`",
    ):
        if marker not in notes:
            errors.append(f"release notes are missing exact metadata marker: {marker}")

    manifest_paths = {entry.get("path") for entry in manifest}
    for field in ("version_path", "changelog_path", "release_notes_path"):
        if metadata.get(field) not in manifest_paths:
            errors.append(f"release metadata path is absent from the full manifest: {metadata.get(field)}")
    return errors


def reject_historical_artifact_mutation(
    changes: list[tuple[str, str]],
) -> None:
    """Keep every committed governance record append-only."""
    for status, path in changes:
        if not is_governance_artifact_path(path):
            continue
        if status == "D":
            raise SystemExit(f"Governance evidence is immutable and cannot be deleted: {path}")
        if status != "A":
            raise SystemExit(
                f"Committed governance evidence is immutable; add a superseding artifact instead: {path}"
            )


def _commit_changes_not_carried_from_a_parent(
    repo_root: Path,
    commit_sha: str,
) -> list[tuple[str, str]]:
    """Return changes authored by one commit, excluding files merely carried through a merge."""
    parent_line = run_git(
        repo_root,
        ["rev-list", "--parents", "-n", "1", commit_sha],
        text=True,
    )
    assert isinstance(parent_line, str)
    tokens = parent_line.strip().split()
    if not tokens or tokens[0] != commit_sha:
        raise SystemExit(f"Unable to resolve commit parents for governance history: {commit_sha}")
    parents = tokens[1:]
    if not parents:
        raise SystemExit(
            "Governance history enforcement cannot compare a root commit without a parent: "
            f"{commit_sha}"
        )

    changes_by_parent: list[dict[str, str]] = []
    for parent_sha in parents:
        _, _, changes = diff_name_status(repo_root, parent_sha, commit_sha)
        changes_by_parent.append({path: status for status, path in changes})

    if len(changes_by_parent) == 1:
        return [
            (status, path)
            for path, status in sorted(changes_by_parent[0].items())
        ]

    authored: list[tuple[str, str]] = []
    candidate_paths = set().union(*(set(changes) for changes in changes_by_parent))
    for path in sorted(candidate_paths):
        statuses = [changes.get(path) for changes in changes_by_parent]
        if any(status is None for status in statuses):
            # The merge commit reused this path unchanged from at least one parent.
            continue
        concrete = [status for status in statuses if status is not None]
        if all(status == "A" for status in concrete):
            authored.append(("A", path))
        elif all(status == "D" for status in concrete):
            authored.append(("D", path))
        else:
            authored.append(("M", path))
    return authored


def reject_artifact_mutation_within_range(
    repo_root: Path,
    base_sha: str,
    head_sha: str,
) -> None:
    """Reject edits to any governance record after its first commit in base..head."""
    resolved_base = resolve_commit(repo_root, base_sha, "base SHA")
    resolved_head = resolve_commit(repo_root, head_sha, "head SHA")
    raw_commits = run_git(
        repo_root,
        ["rev-list", "--reverse", "--topo-order", f"{resolved_base}..{resolved_head}"],
        text=True,
    )
    assert isinstance(raw_commits, str)

    additions: dict[str, str] = {}
    for commit_sha in (line.strip() for line in raw_commits.splitlines() if line.strip()):
        for status, path in _commit_changes_not_carried_from_a_parent(repo_root, commit_sha):
            if not is_governance_artifact_path(path):
                continue
            first_addition = additions.get(path)
            if first_addition is None:
                if status == "A":
                    additions[path] = commit_sha
                    continue
                raise SystemExit(
                    "Committed governance evidence is immutable within the enforced commit range; "
                    f"add a superseding artifact instead: {path} changed at {commit_sha}"
                )
            raise SystemExit(
                "Governance evidence cannot change after its first commit in the enforced range; "
                f"add a superseding artifact instead: {path} was added at {first_addition} "
                f"and changed again at {commit_sha} ({status})"
            )


def _normal_enforcement(
    *,
    base_sha: str,
    head_sha: str,
    repo_root: Path,
    strict: bool,
    require_recommendation: str,
) -> tuple[str, str, list[dict[str, Any]], list[dict[str, Any]]]:
    if not base_sha.strip():
        raise SystemExit("--base-sha is required unless --release-check is used")
    resolved_base, resolved_head, changes = diff_name_status(repo_root, base_sha, head_sha)
    reject_artifact_mutation_within_range(repo_root, resolved_base, resolved_head)
    reject_historical_artifact_mutation(changes)

    governed_changes = [(status, path) for status, path in changes if is_governed_change(path)]
    governed_manifest = build_manifest(
        repo_root,
        changes,
        head_sha=resolved_head,
        governed_predicate=is_governed_change,
    )
    full_manifest = build_manifest(repo_root, changes, head_sha=resolved_head)
    changed_artifacts = [
        path
        for status, path in changes
        if status != "D" and fnmatch.fnmatch(path, GOVERNANCE_ARTIFACT_PATTERN)
    ]

    print(f"Changed files: {len(changes)}")
    print(f"Governed changed files: {len(governed_changes)}")
    print(f"Changed governance artifacts: {len(changed_artifacts)}")
    if governed_changes and not changed_artifacts:
        print("ERROR: Governed changes detected without a changed schema v3 governance artifact.")
        for _, path in governed_changes:
            print(f" - {path}")
        raise SystemExit(1)

    validated: list[dict[str, Any]] = []
    validated_manifest: list[dict[str, Any]] | None = None
    for artifact_path in sorted(changed_artifacts):
        data, raw = _head_json(repo_root, resolved_head, artifact_path)
        if artifact_schema_version(data) != SCHEMA_V3:
            raise SystemExit(
                f"New governed changes require an append-only schema v3 artifact: {artifact_path}"
            )
        _validate_artifact(
            artifact_path,
            data,
            strict=strict,
            require_recommendation=require_recommendation,
        )
        actual_manifest = full_manifest if data.get("purpose") == "release" else governed_manifest
        if validated_manifest is not None and actual_manifest != validated_manifest:
            raise SystemExit("Changed governance artifacts use incompatible manifest scopes")
        validated_manifest = actual_manifest
        errors = binding_errors(data, resolved_base, actual_manifest)
        errors.extend(catalog_binding_errors(data, repo_root, resolved_head))
        errors.extend(release_metadata_errors(data, repo_root, resolved_head, actual_manifest))
        if errors:
            for error in errors:
                print(f"ERROR: {artifact_path}: {error}")
            raise SystemExit(f"Governance artifact is unrelated to the governed diff: {artifact_path}")
        plan_digest = hashlib.sha256(raw).hexdigest()
        validated.append(
            {
                "path": artifact_path,
                "task_id": data.get("task_id"),
                "schema_version": artifact_schema_version(data),
                "recommendation": data.get("recommendation"),
                "artifact_sha256": plan_digest,
                "plan_sha256": plan_digest,
            }
        )

    if governed_changes and not validated:
        raise SystemExit("No change-bound schema v3 governance artifact validated the governed diff")
    return resolved_base, resolved_head, validated_manifest or governed_manifest, validated


def _head_governance_artifact_paths(repo_root: Path, head_sha: str) -> list[str]:
    output = run_git(
        repo_root,
        ["ls-tree", "-r", "--name-only", "-z", head_sha, "--", "docs/governance"],
    )
    assert isinstance(output, bytes)
    return sorted(
        path
        for raw in output.split(b"\0")
        if raw
        for path in [raw.decode("utf-8", errors="strict")]
        if fnmatch.fnmatch(path, GOVERNANCE_ARTIFACT_PATTERN)
    )


def _release_enforcement(
    *,
    head_sha: str,
    repo_root: Path,
    require_recommendation: str,
) -> tuple[str, str, list[dict[str, Any]], list[dict[str, Any]]]:
    resolved_head = resolve_commit(repo_root, head_sha, "head SHA")
    candidates: list[tuple[str, list[dict[str, Any]], dict[str, Any], bytes, str]] = []
    diagnostics: list[str] = []

    for artifact_path in _head_governance_artifact_paths(repo_root, resolved_head):
        data, raw = _head_json(repo_root, resolved_head, artifact_path)
        if artifact_schema_version(data) != SCHEMA_V3:
            continue
        if data.get("purpose") != "release" or "publish" not in data.get(
            "authorized_operations", []
        ):
            continue
        binding = data.get("change_binding")
        base_sha = binding.get("base_sha") if isinstance(binding, dict) else ""
        try:
            resolved_base, _, changes = diff_name_status(repo_root, str(base_sha), resolved_head)
            reject_artifact_mutation_within_range(repo_root, resolved_base, resolved_head)
            actual_manifest = build_manifest(
                repo_root,
                changes,
                head_sha=resolved_head,
            )
        except SystemExit as exc:
            diagnostics.append(f"{artifact_path}: invalid recorded base: {exc}")
            continue
        errors = binding_errors(data, resolved_base, actual_manifest)
        errors.extend(catalog_binding_errors(data, repo_root, resolved_head))
        errors.extend(release_metadata_errors(data, repo_root, resolved_head, actual_manifest))
        if errors:
            diagnostics.append(f"{artifact_path}: {'; '.join(errors)}")
            continue
        validation_errors, _ = validate_artifact_data(
            data,
            strict=True,
            require_recommendation=require_recommendation,
        )
        if validation_errors:
            diagnostics.append(f"{artifact_path}: {'; '.join(validation_errors)}")
            continue
        candidates.append((resolved_base, actual_manifest, data, raw, artifact_path))

    if not candidates:
        print("ERROR: No strict schema v3 release artifact binds the exact release head.")
        for diagnostic in diagnostics:
            print(f" - {diagnostic}")
        raise SystemExit(1)

    if len(candidates) != 1:
        names = ", ".join(sorted(candidate[4] for candidate in candidates))
        raise SystemExit(f"Release enforcement requires exactly one matching artifact; found: {names}")
    resolved_base, manifest, data, raw, artifact_path = candidates[0]
    plan_digest = hashlib.sha256(raw).hexdigest()
    validated = [
        {
            "path": artifact_path,
            "task_id": data.get("task_id"),
            "schema_version": SCHEMA_V3,
            "recommendation": data.get("recommendation"),
            "artifact_sha256": plan_digest,
            "plan_sha256": plan_digest,
        }
    ]
    print(f"Release integrity artifact: {artifact_path}")
    return resolved_base, resolved_head, manifest, validated


def write_attestation(
    path: Path,
    *,
    base_sha: str,
    head_sha: str,
    manifest: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
    release_check: bool,
) -> None:
    attestation = {
        "schema_version": 1,
        "type": "governance-ci-attestation",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "base_sha": base_sha,
        "head_sha": head_sha,
        "manifest": manifest,
        "manifest_sha256": manifest_sha256(manifest),
        "validated_artifacts": artifacts,
        "release_check": release_check,
        "checks": {
            "policy": "pass",
            "artifact_schema": "pass",
            "change_binding": "pass",
            "exact_head": "pass",
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(attestation, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote exact-head attestation: {path}")


def main() -> None:
    args = parse_args()
    skills_root = Path(args.skills_root).resolve()
    repo_root = discover_repo_root(args.repo_root, skills_root)
    resolved_head = resolve_commit(repo_root, args.head_sha, "head SHA")
    checked_out_head = resolve_commit(repo_root, "HEAD", "checked-out HEAD")
    if checked_out_head != resolved_head:
        raise SystemExit(
            "Exact-head enforcement requires the requested head to be checked out "
            f"(requested={resolved_head}, checked_out={checked_out_head})"
        )
    require_clean_exact_checkout(repo_root)

    print(f"Running skill policy validators for exact head: {resolved_head}")
    run_policy_validators(skills_root, repo_root)

    if args.release_check:
        base, head, manifest, artifacts = _release_enforcement(
            head_sha=resolved_head,
            repo_root=repo_root,
            require_recommendation=args.require_recommendation,
        )
    else:
        base, head, manifest, artifacts = _normal_enforcement(
            base_sha=args.base_sha,
            head_sha=resolved_head,
            repo_root=repo_root,
            strict=args.strict,
            require_recommendation=args.require_recommendation,
        )

    if args.attestation_out:
        write_attestation(
            Path(args.attestation_out),
            base_sha=base,
            head_sha=head,
            manifest=manifest,
            artifacts=artifacts,
            release_check=bool(args.release_check),
        )
    print("Governance enforcement passed.")


if __name__ == "__main__":
    main()
