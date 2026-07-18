from contextlib import redirect_stdout
import importlib.util
from io import StringIO
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import governance_common as common
import enforce_governance_ci as enforce
import generate_governance_artifact as generate
import validate_governance_artifact as validate
import validate_skill_policy as policy


def run_git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args],
        text=True,
    ).strip()


def init_repo(root: Path) -> str:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Governance Test"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "governance@example.invalid"], check=True)
    (root / "skills").mkdir(parents=True, exist_ok=True)
    (root / "AGENTS.md").write_text("# test\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "base"], check=True)
    return run_git(root, "rev-parse", "HEAD")


def base_artifact() -> dict:
    return {
        "task_id": "TASK-1",
        "created_at_utc": "2026-07-17T12:00:00Z",
        "project_id": "agent-command-center",
        "project_language": "Python",
        "project_description_max4": "Agent command center",
        "model_runs_test_build_default": "yes",
        "execution_scope": "local_only",
        "deployment_requested": False,
        "quizme_mode": "off",
        "quizme_multiple_choice": False,
        "quizme_one_at_a_time": False,
        "quizme_confirm": False,
        "quizme_record": False,
        "selected_mode": "quick",
        "required_gates": ["order-of-operations"],
        "gate_status": {"order-of-operations": "pass"},
        "startup_declaration": {
            "skills_in_use": ["order-of-operations"],
            "skills_selection_rationale": "Dependency-correct execution is required.",
            "skills_execution_order": ["order-of-operations"],
        },
        "recommendation": "go",
        "break_glass": {"enabled": False},
        "critical_overrides": [],
    }


def v2_artifact(status: str = "pending", recommendation: str = "no-go") -> dict:
    data = base_artifact()
    data["schema_version"] = 2
    data["gate_status"] = {
        "order-of-operations": {
            "status": status,
            "evidence": [],
            "waiver_reason": "",
        }
    }
    data["recommendation"] = recommendation
    data["change_binding"] = {
        "base_sha": "a" * 40,
        "manifest": [],
        "manifest_sha256": common.manifest_sha256([]),
    }
    return data


class TestTaskIdContainment(unittest.TestCase):
    def test_accepts_existing_task_id_style(self) -> None:
        self.assertEqual(common.validate_task_id("PUSH-READY-20260524"), "PUSH-READY-20260524")

    def test_rejects_path_traversal_and_separators(self) -> None:
        for value in ("../escape", "A/B", "A\\B", "/absolute", ".."):
            with self.subTest(value=value), self.assertRaises(SystemExit):
                common.validate_task_id(value)

    def test_artifact_paths_are_proven_inside_outdir(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            outdir = Path(raw) / "governance"
            json_path, md_path = common.contained_artifact_paths(outdir, "TASK-1")
            self.assertEqual(json_path.parent, outdir.resolve())
            self.assertEqual(md_path.parent, outdir.resolve())


class TestWorkflowIntegrity(unittest.TestCase):
    def test_active_and_copyable_workflows_are_identical_and_attest_releases(self) -> None:
        active = (REPO_ROOT / ".github" / "workflows" / "skills-governance-ci.yml").read_text(
            encoding="utf-8"
        )
        template = (REPO_ROOT / "skills" / "docs" / "ci" / "skills-governance-ci.yml").read_text(
            encoding="utf-8"
        )
        self.assertEqual(active, template)
        for marker in (
            "tags:",
            "release:",
            "--release-check",
            "--attestation-out",
            "actions/upload-artifact@v4",
            "Checkout exact event head",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, active)


class TestRepositoryRootDiscovery(unittest.TestCase):
    def test_verified_skills_layout_falls_back_to_parent_not_grandparent(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw) / "repo"
            skills = repo / "skills"
            skills.mkdir(parents=True)
            (repo / "AGENTS.md").write_text("# policy\n", encoding="utf-8")
            failure = subprocess.CalledProcessError(128, ["git"], stderr="not a repository")
            with mock.patch.object(common.subprocess, "run", side_effect=failure):
                self.assertEqual(common.discover_repo_root("", skills), repo.resolve())

    def test_ambiguous_non_git_layout_fails_with_explicit_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            skills = Path(raw) / "not-skills"
            skills.mkdir()
            failure = subprocess.CalledProcessError(128, ["git"], stderr="not a repository")
            with mock.patch.object(common.subprocess, "run", side_effect=failure):
                with self.assertRaisesRegex(SystemExit, "pass --repo-root explicitly"):
                    common.discover_repo_root("", skills)

    def test_full_policy_check_never_accepts_zero_artifacts_silently(self) -> None:
        errors = policy.validate_artifact_inventory(
            [],
            minimum=1,
            governance_dir=Path("docs/governance"),
            filtered_diff=False,
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("found 0", errors[0])


class TestExactGitDiff(unittest.TestCase):
    def test_diff_includes_deletions_and_hashes_exact_head(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            base = init_repo(repo)
            deleted = repo / "skills" / "deleted.md"
            deleted.write_text("old\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "add governed file"], check=True)
            base = run_git(repo, "rev-parse", "HEAD")
            deleted.unlink()
            (repo / "skills" / "added.md").write_text("new\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "replace governed file"], check=True)
            head = run_git(repo, "rev-parse", "HEAD")

            resolved_base, resolved_head, changes = common.diff_name_status(repo, base, head)
            self.assertEqual(resolved_base, base)
            self.assertEqual(resolved_head, head)
            self.assertIn(("D", "skills/deleted.md"), changes)
            self.assertIn(("A", "skills/added.md"), changes)
            manifest = common.build_manifest(
                repo,
                changes,
                head_sha=head,
                governed_predicate=common.is_governed_change,
            )
            by_path = {item["path"]: item for item in manifest}
            self.assertIsNone(by_path["skills/deleted.md"]["sha256"])
            self.assertRegex(by_path["skills/added.md"]["sha256"], r"^[0-9a-f]{64}$")

    def test_invalid_revision_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            head = init_repo(repo)
            with self.assertRaisesRegex(SystemExit, "failed closed"):
                common.diff_name_status(repo, "not-a-commit", head)

    def test_exact_head_policy_validation_rejects_dirty_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            init_repo(repo)
            (repo / "unattested.txt").write_text("dirty\n", encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "clean checkout"):
                enforce.require_clean_exact_checkout(repo)


class TestArtifactSchemaValidation(unittest.TestCase):
    def test_schema_v1_is_not_coupled_to_current_project_index(self) -> None:
        data = base_artifact()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            artifact = root / "legacy.governance.json"
            index = root / "project-index.md"
            artifact.write_text(json.dumps(data), encoding="utf-8")
            index.write_text(
                "# Project Index\n\n"
                "| Project ID | Language | Description (<=4 words) | Model Runs Tests/Build by Default (yes/no) | Last Confirmed UTC |\n"
                "|---|---|---|---|---|\n"
                "| different-project | Rust | Different current project | no | 2026-07-18T00:00:00Z |\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "validate_governance_artifact.py"),
                    "--artifact",
                    str(artifact),
                    "--project-index-path",
                    str(index),
                    "--strict",
                    "--require-recommendation",
                    "go",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Schema: v1", result.stdout)

    def test_v2_pending_gates_force_no_go(self) -> None:
        data = v2_artifact(status="pending", recommendation="go")
        errors, _ = validate.validate_artifact_data(data, strict=False, require_recommendation="no-go")
        self.assertTrue(any("pending or failed" in error for error in errors), errors)

        data["recommendation"] = "no-go"
        errors, warnings = validate.validate_artifact_data(
            data,
            strict=False,
            require_recommendation="no-go",
        )
        self.assertEqual(errors, [])
        self.assertTrue(any("pending required gates" in warning for warning in warnings))

    def test_v2_critical_pending_no_go_is_a_valid_non_strict_draft(self) -> None:
        data = v2_artifact(status="pending", recommendation="no-go")
        data["selected_mode"] = "critical"
        data["required_gates"] = ["project-backup", "restore-drill"]
        data["startup_declaration"]["skills_in_use"] = ["project-backup", "restore-drill"]
        data["startup_declaration"]["skills_execution_order"] = ["project-backup", "restore-drill"]
        data["gate_status"] = {
            gate: {"status": "pending", "evidence": [], "waiver_reason": ""}
            for gate in data["required_gates"]
        }
        errors, _ = validate.validate_artifact_data(
            data,
            strict=False,
            require_recommendation="no-go",
        )
        self.assertEqual(errors, [])

    def test_v2_pass_requires_evidence(self) -> None:
        data = v2_artifact(status="pass", recommendation="go")
        errors, _ = validate.validate_artifact_data(data, strict=True, require_recommendation="go")
        self.assertTrue(any("requires evidence" in error for error in errors), errors)

        data["gate_status"]["order-of-operations"]["evidence"] = ["unit:test_governance_integrity passed"]
        errors, _ = validate.validate_artifact_data(data, strict=True, require_recommendation="go")
        self.assertEqual(errors, [])

    def test_v2_waiver_requires_concrete_reason_and_cannot_recommend_go(self) -> None:
        data = v2_artifact(status="waived", recommendation="go-with-risk")
        data["gate_status"]["order-of-operations"]["waiver_reason"] = "short"
        errors, _ = validate.validate_artifact_data(
            data,
            strict=True,
            require_recommendation="go-with-risk",
        )
        self.assertTrue(any("concrete waiver_reason" in error for error in errors), errors)

        data["gate_status"]["order-of-operations"]["waiver_reason"] = (
            "Approved because the isolated check is unavailable"
        )
        errors, _ = validate.validate_artifact_data(
            data,
            strict=True,
            require_recommendation="go-with-risk",
        )
        self.assertEqual(errors, [])
        data["recommendation"] = "go"
        errors, _ = validate.validate_artifact_data(data, strict=True, require_recommendation="go")
        self.assertTrue(any("waived required gates" in error for error in errors), errors)

    def test_v2_manifest_digest_is_verified(self) -> None:
        data = v2_artifact()
        data["change_binding"]["manifest_sha256"] = "0" * 64
        errors, _ = validate.validate_artifact_data(data, strict=False, require_recommendation="no-go")
        self.assertTrue(any("canonical manifest digest" in error for error in errors), errors)


class TestV2Generator(unittest.TestCase):
    def test_generator_writes_pending_no_go_change_bound_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            base = init_repo(repo)
            (repo / "skills" / "policy.md").write_text("changed\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "generate_governance_artifact.py"),
                    "--task-id",
                    "TASK-2",
                    "--base-sha",
                    base,
                    "--repo-root",
                    str(repo),
                    "--skills-root",
                    str(repo / "skills"),
                    "--project-id",
                    "test-project",
                    "--project-language",
                    "Python",
                    "--project-description-max4",
                    "Governance test project",
                    "--model-runs-test-build-default",
                    "yes",
                    "--skills-in-use",
                    "skill-governance,order-of-operations,scripted-command-execution",
                    "--skills-execution-order",
                    "skill-governance,order-of-operations,scripted-command-execution",
                    "--skills-selection-rationale",
                    "Governed deterministic local test.",
                ],
                cwd=repo,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            artifact_path = repo / "docs" / "governance" / "TASK-2.governance.json"
            data = json.loads(artifact_path.read_text(encoding="utf-8"))
            self.assertEqual(data["schema_version"], 2)
            self.assertEqual(data["recommendation"], "no-go")
            self.assertEqual(data["required_gates"], ["scripted-command-execution"])
            self.assertNotIn("project-backup", data["required_gates"])
            self.assertNotIn("restore-drill", data["required_gates"])
            self.assertTrue(
                all(record["status"] == "pending" for record in data["gate_status"].values())
            )
            self.assertEqual(data["change_binding"]["base_sha"], base)
            manifest_paths = {item["path"] for item in data["change_binding"]["manifest"]}
            self.assertIn("skills/policy.md", manifest_paths)
            self.assertIn("docs/project-index.md", manifest_paths)
            self.assertNotIn("docs/governance/TASK-2.governance.json", manifest_paths)

    def test_generator_adds_restore_controls_only_for_typed_deployment_risk(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            base = init_repo(repo)
            (repo / "skills" / "policy.md").write_text("changed\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "generate_governance_artifact.py"),
                    "--task-id",
                    "TASK-RECOVERY",
                    "--base-sha",
                    base,
                    "--repo-root",
                    str(repo),
                    "--skills-root",
                    str(repo / "skills"),
                    "--project-id",
                    "test-project",
                    "--project-language",
                    "Python",
                    "--project-description-max4",
                    "Governance test project",
                    "--model-runs-test-build-default",
                    "yes",
                    "--execution-scope",
                    "deployment",
                    "--deployment-requested",
                    "--requires-restore",
                    "--skills-in-use",
                    "skill-governance,scripted-command-execution,project-backup,restore-drill",
                    "--skills-execution-order",
                    "skill-governance,project-backup,restore-drill,scripted-command-execution",
                    "--skills-selection-rationale",
                    "Authorized recovery-sensitive deployment test.",
                ],
                cwd=repo,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(
                (repo / "docs" / "governance" / "TASK-RECOVERY.governance.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                data["required_gates"],
                ["scripted-command-execution", "project-backup", "restore-drill"],
            )
            self.assertEqual(
                data["evidence_requirements"][-2:],
                ["backup artifact + integrity evidence", "restore freshness/pass status"],
            )


class TestChangeBindingAndAttestation(unittest.TestCase):
    def test_normal_enforcement_accepts_only_exact_bound_v2_plan(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            base = init_repo(repo)
            (repo / "skills" / "policy.md").write_text("changed\n", encoding="utf-8")
            _, working_changes = common.working_tree_name_status(repo, base)
            manifest = common.build_manifest(
                repo,
                working_changes,
                governed_predicate=common.is_governed_change,
            )
            data = v2_artifact(status="pass", recommendation="go")
            data["gate_status"]["order-of-operations"]["evidence"] = ["targeted tests passed"]
            data["change_binding"] = {
                "base_sha": base,
                "manifest": manifest,
                "manifest_sha256": common.manifest_sha256(manifest),
            }
            governance = repo / "docs" / "governance"
            governance.mkdir(parents=True)
            (governance / "TASK-1.governance.json").write_text(
                json.dumps(data, indent=2) + "\n",
                encoding="utf-8",
            )
            (governance / "TASK-1.governance.md").write_text("# bound plan\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "bound governed change"], check=True)
            head = run_git(repo, "rev-parse", "HEAD")

            actual_base, actual_head, actual_manifest, artifacts = enforce._normal_enforcement(
                base_sha=base,
                head_sha=head,
                repo_root=repo,
                strict=True,
                require_recommendation="go",
            )
            self.assertEqual(actual_base, base)
            self.assertEqual(actual_head, head)
            self.assertEqual(actual_manifest, manifest)
            self.assertEqual([item["task_id"] for item in artifacts], ["TASK-1"])

    def test_unrelated_artifact_cannot_satisfy_governed_diff(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            base = init_repo(repo)
            (repo / "skills" / "policy.md").write_text("changed\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "governed change"], check=True)
            head = run_git(repo, "rev-parse", "HEAD")
            resolved_base, _, changes = common.diff_name_status(repo, base, head)
            actual_manifest = common.build_manifest(
                repo,
                changes,
                head_sha=head,
                governed_predicate=common.is_governed_change,
            )
            data = v2_artifact(status="pass", recommendation="go")
            data["gate_status"]["order-of-operations"]["evidence"] = ["tests passed"]
            self.assertTrue(enforce.binding_errors(data, resolved_base, actual_manifest))

            data["change_binding"] = {
                "base_sha": resolved_base,
                "manifest": actual_manifest,
                "manifest_sha256": common.manifest_sha256(actual_manifest),
            }
            self.assertEqual(enforce.binding_errors(data, resolved_base, actual_manifest), [])

    def test_normal_enforcement_rejects_any_changed_unbound_v2_plan(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            base = init_repo(repo)
            (repo / "skills" / "policy.md").write_text("changed\n", encoding="utf-8")
            _, working_changes = common.working_tree_name_status(repo, base)
            manifest = common.build_manifest(
                repo,
                working_changes,
                governed_predicate=common.is_governed_change,
            )
            governance = repo / "docs" / "governance"
            governance.mkdir(parents=True)

            exact = v2_artifact(status="pass", recommendation="go")
            exact["gate_status"]["order-of-operations"]["evidence"] = ["tests passed"]
            exact["change_binding"] = {
                "base_sha": base,
                "manifest": manifest,
                "manifest_sha256": common.manifest_sha256(manifest),
            }
            stale = v2_artifact(status="pass", recommendation="go")
            stale["task_id"] = "TASK-2"
            stale["gate_status"]["order-of-operations"]["evidence"] = ["older phase passed"]

            for name, data in (("TASK-1", exact), ("TASK-2", stale)):
                (governance / f"{name}.governance.json").write_text(
                    json.dumps(data, indent=2) + "\n",
                    encoding="utf-8",
                )
                (governance / f"{name}.governance.md").write_text(
                    f"# {name}\n",
                    encoding="utf-8",
                )

            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "commit", "-qm", "multiple governed plans"],
                check=True,
            )
            head = run_git(repo, "rev-parse", "HEAD")

            with redirect_stdout(StringIO()):
                with self.assertRaisesRegex(SystemExit, "unrelated to the governed diff"):
                    enforce._normal_enforcement(
                        base_sha=base,
                        head_sha=head,
                        repo_root=repo,
                        strict=True,
                        require_recommendation="go",
                    )

    def test_legacy_artifact_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            init_repo(repo)
            governance = repo / "docs" / "governance"
            governance.mkdir(parents=True)
            artifact = governance / "OLD.governance.json"
            pair = governance / "OLD.governance.md"
            artifact.write_text(json.dumps(base_artifact()), encoding="utf-8")
            pair.write_text("# old\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "legacy evidence"], check=True)
            artifact.write_text(json.dumps({**base_artifact(), "notes": "rewritten"}), encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "rewrite evidence"], check=True)
            head = run_git(repo, "rev-parse", "HEAD")
            base = run_git(repo, "rev-parse", "HEAD^")
            _, _, changes = common.diff_name_status(repo, base, head)
            with self.assertRaisesRegex(SystemExit, "Legacy schema v1 governance evidence is immutable"):
                enforce.reject_historical_artifact_mutation(changes, repo, head)

    def test_attestation_records_exact_head_and_manifest_digest(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "attestation.json"
            manifest = [{"path": "skills/a.md", "status": "D", "sha256": None}]
            enforce.write_attestation(
                path,
                base_sha="a" * 40,
                head_sha="b" * 40,
                manifest=manifest,
                artifacts=[{"path": "docs/governance/T.governance.json"}],
                release_check=True,
            )
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["head_sha"], "b" * 40)
            self.assertEqual(data["manifest_sha256"], common.manifest_sha256(manifest))
            self.assertEqual(data["checks"]["exact_head"], "pass")


if __name__ == "__main__":
    unittest.main()
