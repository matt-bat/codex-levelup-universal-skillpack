from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = ROOT / "skills" / "skill-governance" / "scripts" / "verify_remote_configuration.py"
POLICY_PATH = ROOT / ".github" / "branch-protection-policy.json"
SCHEMA_PATH = (
    ROOT / "skills" / "skill-governance" / "schemas" / "remote-configuration-policy.schema.json"
)

SPEC = importlib.util.spec_from_file_location("verify_remote_configuration", SCRIPT_PATH)
assert SPEC and SPEC.loader
remote = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(remote)


def github_response() -> dict:
    return {
        "url": "https://api.github.com/repos/matt-bat/agent-command-center/branches/main/protection",
        "required_status_checks": {
            "url": "https://api.github.com/status-checks",
            "strict": True,
            "contexts": ["governance"],
            "contexts_url": "https://api.github.com/contexts",
            "checks": [{"context": "governance", "app_id": 15368}],
        },
        "required_signatures": {"url": "https://api.github.com/signatures", "enabled": False},
        "enforce_admins": {"url": "https://api.github.com/admins", "enabled": True},
        "required_linear_history": {"enabled": False},
        "allow_force_pushes": {"enabled": False},
        "allow_deletions": {"enabled": False},
        "block_creations": {"enabled": False},
        "required_conversation_resolution": {"enabled": False},
        "lock_branch": {"enabled": False},
        "allow_fork_syncing": {"enabled": False},
    }


class TestRemoteConfiguration(unittest.TestCase):
    def test_checked_in_policy_is_schema_valid_and_matches_verified_shape(self) -> None:
        self.assertEqual(remote.validate_policy_file(POLICY_PATH, SCHEMA_PATH), [])
        policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        normalized = remote.normalize_github_protection(
            github_response(), repository=policy["repository"], branch=policy["branch"]
        )
        self.assertEqual(remote.compare_state(policy["protection"], normalized), [])

    def test_target_identity_mismatch_fails_closed(self) -> None:
        with self.assertRaisesRegex(remote.RemotePolicyError, "target mismatch"):
            remote.normalize_github_protection(
                github_response(), repository="different/repository", branch="main"
            )

    def test_unknown_remote_field_fails_closed(self) -> None:
        actual = github_response()
        actual["new_unmodeled_control"] = {"enabled": True}
        with self.assertRaisesRegex(remote.RemotePolicyError, "unsupported fields"):
            remote.normalize_github_protection(
                actual, repository="matt-bat/agent-command-center", branch="main"
            )

    def test_unknown_policy_field_and_wrong_schema_pointer_fail_closed(self) -> None:
        policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        policy["unknown_policy"] = True
        policy["$schema"] = "different.schema.json"
        errors = remote.validate_policy(policy, schema)
        self.assertTrue(any("Additional properties" in error for error in errors), errors)
        self.assertTrue(any(error.startswith("$schema:") for error in errors), errors)

    def test_setting_drift_is_reported_at_exact_path(self) -> None:
        policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        actual = github_response()
        actual["allow_force_pushes"]["enabled"] = True
        normalized = remote.normalize_github_protection(
            actual, repository=policy["repository"], branch=policy["branch"]
        )
        self.assertEqual(
            remote.compare_state(policy["protection"], normalized),
            ["protection.allow_force_pushes: expected False, actual True"],
        )

    def test_cli_passes_exact_state_and_rejects_drift(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            actual_path = Path(raw) / "actual.json"
            actual_path.write_text(json.dumps(github_response()), encoding="utf-8")
            command = [
                sys.executable,
                str(SCRIPT_PATH),
                "--policy",
                str(POLICY_PATH),
                "--actual",
                str(actual_path),
                "--schema",
                str(SCHEMA_PATH),
            ]
            passed = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)

            drifted = copy.deepcopy(github_response())
            drifted["enforce_admins"]["enabled"] = False
            actual_path.write_text(json.dumps(drifted), encoding="utf-8")
            failed = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(failed.returncode, 1)
            self.assertIn("protection.enforce_admins", failed.stderr)

    def test_cli_accepts_actual_state_on_standard_input(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--policy",
                str(POLICY_PATH),
                "--actual",
                "-",
                "--schema",
                str(SCHEMA_PATH),
            ],
            input=json.dumps(github_response()),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
