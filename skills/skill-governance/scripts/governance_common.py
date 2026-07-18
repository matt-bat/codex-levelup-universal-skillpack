#!/usr/bin/env python3
"""Shared, deterministic primitives for governance artifact integrity."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


SCHEMA_V1 = 1
SCHEMA_V2 = 2
SUPPORTED_SCHEMA_VERSIONS = {SCHEMA_V1, SCHEMA_V2}
COMMIT_SHA_RE = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
TASK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
VALID_DIFF_STATES = {"A", "M", "D", "T", "U", "X", "B"}
GOVERNED_PATH_PREFIXES = (
    ".codex/skills/",
    "skills/",
    "docs/governance/",
    ".github/workflows/",
)
GOVERNED_PATH_EXACT = {"AGENTS.md", "docs/project-index.md"}


def validate_task_id(task_id: str) -> str:
    """Return a safe task ID or fail before it can become a path component."""
    value = str(task_id).strip()
    if not TASK_ID_RE.fullmatch(value):
        raise SystemExit(
            "--task-id must be 1-128 characters, start with a letter or digit, "
            "and contain only letters, digits, '.', '_', or '-'"
        )
    return value


def contained_artifact_paths(outdir: Path, task_id: str) -> tuple[Path, Path]:
    """Build artifact paths and prove both remain inside the selected directory."""
    safe_task_id = validate_task_id(task_id)
    resolved_outdir = outdir.resolve()
    json_path = (resolved_outdir / f"{safe_task_id}.governance.json").resolve()
    md_path = (resolved_outdir / f"{safe_task_id}.governance.md").resolve()
    for candidate in (json_path, md_path):
        try:
            candidate.relative_to(resolved_outdir)
        except ValueError as exc:
            raise SystemExit(f"Artifact path escapes output directory: {candidate}") from exc
    return json_path, md_path


def normalize_repo_path(raw_path: str) -> str:
    """Normalize a Git-reported path without permitting repository escape."""
    value = str(raw_path)
    if "\\" in value or "\x00" in value:
        raise SystemExit(f"Invalid repository-relative path: {raw_path!r}")
    candidate = PurePosixPath(value)
    if not value or candidate.is_absolute() or any(part in {"", ".", ".."} for part in candidate.parts):
        raise SystemExit(f"Invalid repository-relative path: {raw_path!r}")
    normalized = candidate.as_posix()
    if normalized != value:
        raise SystemExit(f"Repository-relative path is not canonical: {raw_path!r}")
    return normalized


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _validate_repo_root(candidate: Path, skills_root: Path, source: str) -> Path:
    resolved = candidate.resolve()
    if not resolved.is_dir():
        raise SystemExit(f"Repository root from {source} is not a directory: {resolved}")
    if not _is_relative_to(skills_root.resolve(), resolved):
        raise SystemExit(
            f"Skills root {skills_root.resolve()} is outside repository root from {source}: {resolved}"
        )
    return resolved


def discover_repo_root(repo_root_arg: str, skills_root: Path) -> Path:
    """Discover a repository root with a verified, layout-safe fallback."""
    resolved_skills_root = skills_root.resolve()
    if not resolved_skills_root.is_dir():
        raise SystemExit(f"Skills root is not a directory: {resolved_skills_root}")

    if repo_root_arg.strip():
        return _validate_repo_root(Path(repo_root_arg), resolved_skills_root, "--repo-root")

    try:
        result = subprocess.run(
            ["git", "-C", str(resolved_skills_root), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        output = result.stdout.strip()
        if not output:
            raise SystemExit("Git returned an empty repository root; pass --repo-root explicitly")
        return _validate_repo_root(Path(output), resolved_skills_root, "git rev-parse")
    except FileNotFoundError as exc:
        git_error = f"git executable unavailable: {exc}"
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "git rev-parse failed").strip()
        git_error = detail

    fallback = resolved_skills_root.parent
    layout_markers = (
        fallback / "AGENTS.md",
        fallback / "docs",
        fallback / ".github",
        fallback / ".git",
    )
    if resolved_skills_root.name == "skills" and any(marker.exists() for marker in layout_markers):
        return _validate_repo_root(fallback, resolved_skills_root, "verified skills/ layout fallback")

    raise SystemExit(
        "Unable to discover repository root safely. "
        f"Git discovery failed ({git_error}); pass --repo-root explicitly."
    )


def run_git(repo_root: Path, args: list[str], *, text: bool = False) -> bytes | str:
    resolved_root = repo_root.resolve()
    try:
        result = subprocess.run(
            ["git", "-c", f"safe.directory={resolved_root}", "-C", str(resolved_root), *args],
            check=True,
            capture_output=True,
            text=text,
        )
    except FileNotFoundError as exc:
        raise SystemExit(f"Git is required for governance integrity checks: {exc}") from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr
        if isinstance(stderr, bytes):
            detail = stderr.decode("utf-8", errors="replace").strip()
        else:
            detail = (stderr or exc.stdout or "git command failed").strip()
        raise SystemExit(f"Git command failed closed: git {' '.join(args)}: {detail}") from exc
    return result.stdout


def resolve_commit(repo_root: Path, revision: str, field_name: str) -> str:
    """Resolve a revision to an exact commit SHA or fail closed."""
    value = str(revision).strip()
    if not value:
        raise SystemExit(f"{field_name} cannot be empty")
    output = run_git(repo_root, ["rev-parse", "--verify", f"{value}^{{commit}}"], text=True)
    resolved = str(output).strip().lower()
    if not COMMIT_SHA_RE.fullmatch(resolved):
        raise SystemExit(f"{field_name} did not resolve to a canonical commit SHA: {revision!r}")
    return resolved


def _parse_name_status_z(output: bytes) -> list[tuple[str, str]]:
    tokens = output.split(b"\0")
    if tokens and tokens[-1] == b"":
        tokens.pop()
    if len(tokens) % 2:
        raise SystemExit("Unexpected git diff --name-status -z output; refusing partial enforcement")

    entries: list[tuple[str, str]] = []
    for index in range(0, len(tokens), 2):
        raw_status = tokens[index].decode("utf-8", errors="strict")
        raw_path = tokens[index + 1].decode("utf-8", errors="strict")
        status = raw_status[:1]
        if status not in VALID_DIFF_STATES:
            raise SystemExit(f"Unsupported git diff status {raw_status!r} for {raw_path!r}")
        entries.append((status, normalize_repo_path(raw_path)))
    return entries


def diff_name_status(repo_root: Path, base_sha: str, head_sha: str) -> tuple[str, str, list[tuple[str, str]]]:
    """Return the exact two-tree diff, including deletions, after validating both commits."""
    resolved_base = resolve_commit(repo_root, base_sha, "base SHA")
    resolved_head = resolve_commit(repo_root, head_sha, "head SHA")
    output = run_git(
        repo_root,
        ["diff", "--name-status", "-z", "--no-renames", resolved_base, resolved_head],
    )
    assert isinstance(output, bytes)
    return resolved_base, resolved_head, _parse_name_status_z(output)


def working_tree_name_status(repo_root: Path, base_sha: str) -> tuple[str, list[tuple[str, str]]]:
    """Return tracked and untracked working-tree changes relative to an exact base."""
    resolved_base = resolve_commit(repo_root, base_sha, "base SHA")
    output = run_git(
        repo_root,
        ["diff", "--name-status", "-z", "--no-renames", resolved_base],
    )
    assert isinstance(output, bytes)
    entries = dict((path, status) for status, path in _parse_name_status_z(output))

    untracked = run_git(repo_root, ["ls-files", "--others", "--exclude-standard", "-z"])
    assert isinstance(untracked, bytes)
    for raw_path in untracked.split(b"\0"):
        if raw_path:
            entries[normalize_repo_path(raw_path.decode("utf-8", errors="strict"))] = "A"
    return resolved_base, [(entries[path], path) for path in sorted(entries)]


def is_governance_artifact_path(path: str) -> bool:
    normalized = normalize_repo_path(path)
    return normalized.startswith("docs/governance/") and (
        normalized.endswith(".governance.json")
        or normalized.endswith(".governance.md")
        or normalized.endswith(".governance-attestation.json")
    )


def is_governed_change(path: str) -> bool:
    normalized = normalize_repo_path(path)
    return normalized in GOVERNED_PATH_EXACT or any(
        normalized.startswith(prefix) for prefix in GOVERNED_PATH_PREFIXES
    )


def _head_file_bytes(repo_root: Path, head_sha: str, path: str) -> bytes:
    output = run_git(repo_root, ["show", f"{head_sha}:{path}"])
    assert isinstance(output, bytes)
    return output


def _working_file_bytes(repo_root: Path, path: str) -> bytes:
    candidate = repo_root.resolve() / normalize_repo_path(path)
    if candidate.is_symlink():
        return os.readlink(candidate).encode("utf-8")
    resolved_candidate = candidate.resolve()
    if not _is_relative_to(resolved_candidate, repo_root.resolve()):
        raise SystemExit(f"Changed path escapes repository root: {path}")
    return resolved_candidate.read_bytes()


def build_manifest(
    repo_root: Path,
    changes: Iterable[tuple[str, str]],
    *,
    head_sha: str | None = None,
    governed_predicate: Any | None = None,
) -> list[dict[str, Any]]:
    """Build a sorted, content-addressed manifest from normalized changes."""
    manifest: list[dict[str, Any]] = []
    seen: set[str] = set()
    for status, raw_path in changes:
        path = normalize_repo_path(raw_path)
        if path in seen:
            raise SystemExit(f"Duplicate path in change manifest: {path}")
        seen.add(path)
        if governed_predicate is not None and not governed_predicate(path):
            continue
        if is_governance_artifact_path(path):
            continue
        if status == "D":
            digest = None
        else:
            content = _head_file_bytes(repo_root, head_sha, path) if head_sha else _working_file_bytes(repo_root, path)
            digest = hashlib.sha256(content).hexdigest()
        manifest.append({"path": path, "status": status, "sha256": digest})
    return sorted(manifest, key=lambda item: item["path"])


def canonical_manifest_bytes(manifest: list[dict[str, Any]]) -> bytes:
    return json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def manifest_sha256(manifest: list[dict[str, Any]]) -> str:
    return hashlib.sha256(canonical_manifest_bytes(manifest)).hexdigest()


def validate_manifest_shape(manifest: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, list):
        return ["change_binding.manifest must be a list"]
    normalized_entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(manifest):
        prefix = f"change_binding.manifest[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        if set(item) != {"path", "status", "sha256"}:
            errors.append(f"{prefix} must contain exactly path, status, and sha256")
            continue
        if not isinstance(item["path"], str):
            errors.append(f"{prefix}.path must be a string")
            continue
        try:
            path = normalize_repo_path(item["path"])
        except SystemExit as exc:
            errors.append(f"{prefix}.path is invalid: {exc}")
            continue
        status = item["status"]
        digest = item["sha256"]
        if path in seen:
            errors.append(f"change_binding.manifest contains duplicate path: {path}")
        seen.add(path)
        if not isinstance(status, str) or status not in VALID_DIFF_STATES:
            errors.append(f"{prefix}.status is invalid: {status!r}")
        if status == "D":
            if digest is not None:
                errors.append(f"{prefix}.sha256 must be null for a deletion")
        elif not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            errors.append(f"{prefix}.sha256 must be a lowercase SHA-256 digest")
        normalized_entries.append({"path": path, "status": status, "sha256": digest})
    if normalized_entries != sorted(normalized_entries, key=lambda item: item["path"]):
        errors.append("change_binding.manifest must be sorted by path")
    return errors
