#!/usr/bin/env python3
"""Fail-closed CI enforcement for change-bound governance evidence."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
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
            "Find a strict v2 artifact whose recorded base and manifest bind the exact release head. "
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
    if artifact_schema_version(data) != SCHEMA_V2:
        return ["only schema v2 artifacts can authorize governed changes"]
    binding = data.get("change_binding")
    if not isinstance(binding, dict):
        return ["schema v2 artifact has no change_binding object"]
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


def _paired_json_path(path: str) -> str | None:
    if path.endswith(".governance.json"):
        return path
    if path.endswith(".governance.md"):
        return path[: -len(".governance.md")] + ".governance.json"
    return None


def reject_historical_artifact_mutation(
    changes: list[tuple[str, str]],
    repo_root: Path,
    head_sha: str,
) -> None:
    """Keep legacy evidence append-only while allowing new v2 evidence."""
    for status, path in changes:
        if not is_governance_artifact_path(path):
            continue
        if status == "D":
            raise SystemExit(f"Governance evidence is immutable and cannot be deleted: {path}")
        json_path = _paired_json_path(path)
        if not json_path:
            continue
        try:
            data, _ = _head_json(repo_root, head_sha, json_path)
        except SystemExit as exc:
            raise SystemExit(f"Unable to prove governance evidence version for {path}: {exc}") from exc
        if artifact_schema_version(data) != SCHEMA_V2:
            raise SystemExit(
                f"Legacy schema v1 governance evidence is immutable and cannot be edited: {path}"
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
    reject_historical_artifact_mutation(changes, repo_root, resolved_head)

    governed_changes = [(status, path) for status, path in changes if is_governed_change(path)]
    actual_manifest = build_manifest(
        repo_root,
        changes,
        head_sha=resolved_head,
        governed_predicate=is_governed_change,
    )
    changed_artifacts = [
        path
        for status, path in changes
        if status != "D" and fnmatch.fnmatch(path, GOVERNANCE_ARTIFACT_PATTERN)
    ]

    print(f"Changed files: {len(changes)}")
    print(f"Governed changed files: {len(governed_changes)}")
    print(f"Changed governance artifacts: {len(changed_artifacts)}")
    if governed_changes and not changed_artifacts:
        print("ERROR: Governed changes detected without a changed schema v2 governance artifact.")
        for _, path in governed_changes:
            print(f" - {path}")
        raise SystemExit(1)

    validated: list[dict[str, Any]] = []
    for artifact_path in sorted(changed_artifacts):
        data, raw = _head_json(repo_root, resolved_head, artifact_path)
        _validate_artifact(
            artifact_path,
            data,
            strict=strict,
            require_recommendation=require_recommendation,
        )
        errors = binding_errors(data, resolved_base, actual_manifest)
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
        raise SystemExit("No change-bound schema v2 governance artifact validated the governed diff")
    return resolved_base, resolved_head, actual_manifest, validated


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
        if artifact_schema_version(data) != SCHEMA_V2:
            continue
        binding = data.get("change_binding")
        base_sha = binding.get("base_sha") if isinstance(binding, dict) else ""
        try:
            resolved_base, _, changes = diff_name_status(repo_root, str(base_sha), resolved_head)
            actual_manifest = build_manifest(
                repo_root,
                changes,
                head_sha=resolved_head,
                governed_predicate=is_governed_change,
            )
        except SystemExit as exc:
            diagnostics.append(f"{artifact_path}: invalid recorded base: {exc}")
            continue
        errors = binding_errors(data, resolved_base, actual_manifest)
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
        print("ERROR: No strict schema v2 governance artifact binds the exact release head.")
        for diagnostic in diagnostics:
            print(f" - {diagnostic}")
        raise SystemExit(1)

    resolved_base, manifest, data, raw, artifact_path = sorted(candidates, key=lambda item: item[4])[0]
    plan_digest = hashlib.sha256(raw).hexdigest()
    validated = [
        {
            "path": artifact_path,
            "task_id": data.get("task_id"),
            "schema_version": SCHEMA_V2,
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
