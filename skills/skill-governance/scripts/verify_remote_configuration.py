#!/usr/bin/env python3
"""Compare a GitHub branch-protection response with a closed desired-state policy."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlparse

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - exercised by dependency-failure environments
    raise SystemExit(
        "jsonschema is required; install skills/skill-governance/requirements.txt"
    ) from exc


SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_SCHEMA = SCRIPT_PATH.parent.parent / "schemas" / "remote-configuration-policy.schema.json"

TOP_LEVEL_FIELDS = {
    "url",
    "required_status_checks",
    "required_pull_request_reviews",
    "required_signatures",
    "enforce_admins",
    "restrictions",
    "required_linear_history",
    "allow_force_pushes",
    "allow_deletions",
    "block_creations",
    "required_conversation_resolution",
    "lock_branch",
    "allow_fork_syncing",
}
WRAPPER_FIELDS = {"url", "enabled"}
STATUS_CHECK_FIELDS = {"url", "strict", "contexts", "contexts_url", "checks"}
CHECK_FIELDS = {"context", "app_id"}
REVIEW_FIELDS = {
    "url",
    "dismissal_restrictions",
    "dismiss_stale_reviews",
    "require_code_owner_reviews",
    "required_approving_review_count",
    "require_last_push_approval",
    "bypass_pull_request_allowances",
}
PRINCIPAL_FIELDS = {"url", "users", "teams", "apps"}


class RemotePolicyError(ValueError):
    """Raised when remote evidence is ambiguous or outside the verifier contract."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", required=True, help="Desired-state policy JSON path.")
    parser.add_argument(
        "--actual",
        required=True,
        help="Raw GitHub branch-protection JSON path, or '-' to read standard input.",
    )
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA), help="Policy JSON Schema path.")
    parser.add_argument(
        "--print-normalized",
        action="store_true",
        help="Print normalized remote state after successful verification.",
    )
    return parser.parse_args()


def load_json(path: Path, label: str) -> Any:
    try:
        raw = sys.stdin.read() if str(path) == "-" else path.read_text(encoding="utf-8")
        return json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        raise RemotePolicyError(f"{label} is not readable JSON: {path}: {exc}") from exc


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RemotePolicyError(f"{label} must be an object")
    return value


def _reject_unknown(value: dict[str, Any], allowed: set[str], label: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise RemotePolicyError(f"{label} contains unsupported fields: {', '.join(unknown)}")


def validate_policy(policy: Any, schema: Any) -> list[str]:
    if not isinstance(schema, dict):
        return ["remote policy schema root must be an object"]
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
        for error in sorted(validator.iter_errors(policy), key=lambda item: list(item.absolute_path))
    ]


def validate_policy_file(policy_path: Path, schema_path: Path = DEFAULT_SCHEMA) -> list[str]:
    try:
        policy = load_json(policy_path, "remote policy")
        schema = load_json(schema_path, "remote policy schema")
        return validate_policy(policy, schema)
    except (RemotePolicyError, OSError, ValueError) as exc:
        return [str(exc)]


def _enabled(value: Any, label: str) -> bool:
    if value is None:
        return False
    item = _object(value, label)
    _reject_unknown(item, WRAPPER_FIELDS, label)
    enabled = item.get("enabled")
    if not isinstance(enabled, bool):
        raise RemotePolicyError(f"{label}.enabled must be a boolean")
    return enabled


def _principal_name(value: Any, kind: str, label: str) -> str:
    item = _object(value, label)
    candidates = {
        "users": ("login",),
        "teams": ("slug", "name"),
        "apps": ("slug", "name", "id"),
    }[kind]
    for key in candidates:
        candidate = item.get(key)
        if isinstance(candidate, (str, int)) and str(candidate):
            return str(candidate)
    raise RemotePolicyError(f"{label} lacks a stable principal identifier")


def _principals(value: Any, label: str) -> dict[str, list[str]]:
    if value is None:
        return {"users": [], "teams": [], "apps": []}
    item = _object(value, label)
    _reject_unknown(item, PRINCIPAL_FIELDS, label)
    normalized: dict[str, list[str]] = {}
    for kind in ("users", "teams", "apps"):
        raw = item.get(kind, [])
        if not isinstance(raw, list):
            raise RemotePolicyError(f"{label}.{kind} must be an array")
        names = [_principal_name(entry, kind, f"{label}.{kind}") for entry in raw]
        if len(names) != len(set(names)):
            raise RemotePolicyError(f"{label}.{kind} contains duplicate principals")
        normalized[kind] = sorted(names)
    return normalized


def _status_checks(value: Any) -> dict[str, Any] | None:
    if value is None:
        return None
    item = _object(value, "required_status_checks")
    _reject_unknown(item, STATUS_CHECK_FIELDS, "required_status_checks")
    strict = item.get("strict")
    checks = item.get("checks")
    contexts = item.get("contexts")
    if not isinstance(strict, bool) or not isinstance(checks, list) or not isinstance(contexts, list):
        raise RemotePolicyError(
            "required_status_checks requires boolean strict plus contexts and checks arrays"
        )
    normalized_checks: list[dict[str, Any]] = []
    for index, raw_check in enumerate(checks):
        check = _object(raw_check, f"required_status_checks.checks[{index}]")
        _reject_unknown(check, CHECK_FIELDS, f"required_status_checks.checks[{index}]")
        context = check.get("context")
        app_id = check.get("app_id")
        if not isinstance(context, str) or not context:
            raise RemotePolicyError("required status check context must be a non-empty string")
        if app_id is not None and (not isinstance(app_id, int) or isinstance(app_id, bool) or app_id < 1):
            raise RemotePolicyError("required status check app_id must be a positive integer or null")
        normalized_checks.append({"context": context, "app_id": app_id})
    normalized_checks.sort(key=lambda check: (check["context"], check["app_id"] or -1))
    if len({(check["context"], check["app_id"]) for check in normalized_checks}) != len(
        normalized_checks
    ):
        raise RemotePolicyError("required_status_checks.checks contains duplicates")
    if sorted(contexts) != sorted({check["context"] for check in normalized_checks}):
        raise RemotePolicyError("required status check contexts disagree with typed checks")
    return {"strict": strict, "checks": normalized_checks}


def _pull_request_reviews(value: Any) -> dict[str, Any] | None:
    if value is None:
        return None
    item = _object(value, "required_pull_request_reviews")
    _reject_unknown(item, REVIEW_FIELDS, "required_pull_request_reviews")
    booleans = (
        "dismiss_stale_reviews",
        "require_code_owner_reviews",
        "require_last_push_approval",
    )
    normalized: dict[str, Any] = {}
    for field in booleans:
        raw = item.get(field, False)
        if not isinstance(raw, bool):
            raise RemotePolicyError(f"required_pull_request_reviews.{field} must be boolean")
        normalized[field] = raw
    count = item.get("required_approving_review_count", 0)
    if not isinstance(count, int) or isinstance(count, bool) or not 0 <= count <= 6:
        raise RemotePolicyError(
            "required_pull_request_reviews.required_approving_review_count must be 0..6"
        )
    normalized["required_approving_review_count"] = count
    normalized["dismissal_restrictions"] = _principals(
        item.get("dismissal_restrictions"), "required_pull_request_reviews.dismissal_restrictions"
    )
    normalized["bypass_pull_request_allowances"] = _principals(
        item.get("bypass_pull_request_allowances"),
        "required_pull_request_reviews.bypass_pull_request_allowances",
    )
    return normalized


def normalize_github_protection(actual: Any, *, repository: str, branch: str) -> dict[str, Any]:
    item = _object(actual, "GitHub branch protection response")
    _reject_unknown(item, TOP_LEVEL_FIELDS, "GitHub branch protection response")
    url = item.get("url")
    if not isinstance(url, str):
        raise RemotePolicyError("GitHub branch protection response requires its source URL")
    expected_path = f"/repos/{repository}/branches/{quote(branch, safe='')}/protection"
    if urlparse(url).path != expected_path:
        raise RemotePolicyError(
            f"remote evidence target mismatch: expected {repository}:{branch}, received {url}"
        )
    restrictions = item.get("restrictions")
    return {
        "required_status_checks": _status_checks(item.get("required_status_checks")),
        "required_pull_request_reviews": _pull_request_reviews(
            item.get("required_pull_request_reviews")
        ),
        "required_signatures": _enabled(item.get("required_signatures"), "required_signatures"),
        "enforce_admins": _enabled(item.get("enforce_admins"), "enforce_admins"),
        "restrictions": None if restrictions is None else _principals(restrictions, "restrictions"),
        "required_linear_history": _enabled(
            item.get("required_linear_history"), "required_linear_history"
        ),
        "allow_force_pushes": _enabled(item.get("allow_force_pushes"), "allow_force_pushes"),
        "allow_deletions": _enabled(item.get("allow_deletions"), "allow_deletions"),
        "block_creations": _enabled(item.get("block_creations"), "block_creations"),
        "required_conversation_resolution": _enabled(
            item.get("required_conversation_resolution"), "required_conversation_resolution"
        ),
        "lock_branch": _enabled(item.get("lock_branch"), "lock_branch"),
        "allow_fork_syncing": _enabled(item.get("allow_fork_syncing"), "allow_fork_syncing"),
    }


def compare_state(expected: Any, actual: Any, path: str = "protection") -> list[str]:
    if isinstance(expected, dict) and isinstance(actual, dict):
        errors: list[str] = []
        for key in sorted(set(expected) | set(actual)):
            if key not in expected:
                errors.append(f"{path}.{key}: unexpected actual field")
            elif key not in actual:
                errors.append(f"{path}.{key}: missing actual field")
            else:
                errors.extend(compare_state(expected[key], actual[key], f"{path}.{key}"))
        return errors
    if expected != actual:
        return [f"{path}: expected {expected!r}, actual {actual!r}"]
    return []


def main() -> None:
    args = parse_args()
    policy_path = Path(args.policy).resolve()
    actual_path = Path("-") if args.actual == "-" else Path(args.actual).resolve()
    schema_path = Path(args.schema).resolve()
    try:
        policy = load_json(policy_path, "remote policy")
        schema = load_json(schema_path, "remote policy schema")
        schema_errors = validate_policy(policy, schema)
        if schema_errors:
            raise RemotePolicyError("invalid remote policy: " + "; ".join(schema_errors))
        actual = load_json(actual_path, "GitHub branch protection response")
        normalized = normalize_github_protection(
            actual,
            repository=policy["repository"],
            branch=policy["branch"],
        )
        mismatches = compare_state(policy["protection"], normalized)
        if mismatches:
            raise RemotePolicyError("remote configuration drift: " + "; ".join(mismatches))
    except RemotePolicyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(
        f"Remote policy verified: {policy['provider']}:{policy['repository']}:{policy['branch']}"
    )
    if args.print_normalized:
        print(json.dumps(normalized, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
