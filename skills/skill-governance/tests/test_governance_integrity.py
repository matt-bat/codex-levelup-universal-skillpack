from contextlib import redirect_stdout
import hashlib
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
    (root / "skills" / "skill-catalog.json").write_bytes(
        (REPO_ROOT / "skills" / "skill-catalog.json").read_bytes()
    )
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


def v3_evidence(
    *,
    kind: str = "command",
    reference: str = "python governance validation passed",
) -> dict:
    return {
        "kind": kind,
        "reference": reference,
        "result": "pass",
        "observed_at_utc": "2026-07-17T12:00:00Z",
        "revision_sha": "a" * 40,
        "sha256": None,
    }


def v3_artifact(status: str = "pending", recommendation: str = "no-go") -> dict:
    data = v2_artifact(status=status, recommendation=recommendation)
    data.update(
        {
            "schema_version": 3,
            "purpose": "change",
            "authorized_operations": [],
            "release_metadata": None,
            "profile": "internal",
            "execution_skill": "scripted-command-execution",
            "behavior_or_workflow_changed": False,
            "uncertainty_high": False,
            "requires_backup": False,
            "requires_restore": False,
            "scores": {
                "data_impact": 0,
                "business_impact": 0,
                "change_complexity": 0,
                "dependency_uncertainty": 0,
                "recoverability": 0,
            },
            "total_score": 0,
            "base_mode": "quick",
            "mode_after_profile": "quick",
            "selected_mode": "quick",
            "critical_overrides": [],
            "required_gates": ["scripted-command-execution"],
            "gate_status": {
                "scripted-command-execution": {
                    "status": status,
                    "evidence": [v3_evidence()] if status == "pass" else [],
                    "waiver_reason": "",
                }
            },
            "startup_declaration": {
                "skills_in_use": ["skill-governance", "scripted-command-execution"],
                "skills_selection_rationale": "Governed deterministic execution is required.",
                "skills_execution_order": ["skill-governance", "scripted-command-execution"],
            },
            "evidence_requirements": [
                "mode + score",
                "steps executed",
                "minimal validation outcomes",
            ],
            "notes": "",
            "break_glass": {
                "enabled": False,
                "reason": "",
                "risk_owner": "",
                "remediation_ticket": "",
                "expiry_hours": None,
            },
        }
    )
    data["catalog_binding"] = generate.build_catalog_binding(
        REPO_ROOT / "skills" / "skill-catalog.json",
        data["startup_declaration"]["skills_in_use"],
        data["startup_declaration"]["skills_execution_order"],
        repo_root=REPO_ROOT,
    )
    return data


def v3_release_artifact() -> dict:
    data = v3_artifact(status="pass", recommendation="go")
    gates = [
        "scripted-command-execution",
        "regression-prevention",
        "semantic-policy-audit",
        "governance-enforcement",
    ]
    startup = ["skill-governance", *gates]
    data.update(
        {
            "purpose": "release",
            "authorized_operations": ["publish"],
            "release_metadata": {
                "version": "2.0.0",
                "tag": "v2.0.0",
                "version_path": "skills/VERSION",
                "changelog_path": "skills/CHANGELOG.md",
                "release_notes_path": "skills/RELEASE_NOTES_v2.0.0.md",
                "skill_count": 39,
                "governance_test_count": generate.count_governance_test_methods(REPO_ROOT),
            },
            "execution_scope": "external",
            "selected_mode": "critical",
            "required_gates": gates,
            "gate_status": {
                gate: {
                    "status": "pass",
                    "evidence": [
                        v3_evidence(
                            kind={
                                "semantic-policy-audit": "review",
                                "governance-enforcement": "test",
                            }.get(gate, "test"),
                            reference=f"verified evidence for {gate}",
                        )
                    ],
                    "waiver_reason": "",
                }
                for gate in gates
            },
            "startup_declaration": {
                "skills_in_use": startup,
                "skills_selection_rationale": "Release integrity requires critical governed evidence.",
                "skills_execution_order": startup,
            },
            "evidence_requirements": [
                "mode + score",
                "impact map",
                "validation scope by layer",
                "residual risks",
                "rollback plan",
                "release decision",
                "operation-specific authority + target identity",
                "rollback or recovery evidence",
                "post-operation validation + audit evidence",
            ],
        }
    )
    release_manifest = [
        {"path": "skills/CHANGELOG.md", "status": "M", "sha256": "b" * 64},
        {"path": "skills/RELEASE_NOTES_v2.0.0.md", "status": "A", "sha256": "c" * 64},
        {"path": "skills/VERSION", "status": "M", "sha256": "d" * 64},
    ]
    data["change_binding"]["manifest"] = release_manifest
    data["change_binding"]["manifest_sha256"] = common.manifest_sha256(release_manifest)
    data["catalog_binding"] = generate.build_catalog_binding(
        REPO_ROOT / "skills" / "skill-catalog.json",
        data["startup_declaration"]["skills_in_use"],
        data["startup_declaration"]["skills_execution_order"],
        repo_root=REPO_ROOT,
    )
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
    @staticmethod
    def event_block(workflow: str, event: str) -> str:
        lines = workflow.splitlines()
        marker = f"  {event}:"
        start = lines.index(marker)
        block = [lines[start]]
        for line in lines[start + 1 :]:
            if line and len(line) - len(line.lstrip()) <= 2:
                break
            block.append(line)
        return "\n".join(block)

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

    def test_required_governance_check_runs_for_every_main_pull_request(self) -> None:
        active = (REPO_ROOT / ".github" / "workflows" / "skills-governance-ci.yml").read_text(
            encoding="utf-8"
        )
        pull_request = self.event_block(active, "pull_request")

        self.assertIn("    branches:\n      - main", pull_request)
        self.assertNotIn("    paths:", pull_request)
        self.assertIn("jobs:\n  governance:", active)

    def test_feature_branch_pushes_validate_without_main_only_attestation(self) -> None:
        active = (REPO_ROOT / ".github" / "workflows" / "skills-governance-ci.yml").read_text(
            encoding="utf-8"
        )
        push = self.event_block(active, "push")

        self.assertIn("    branches:\n      - '**'", push)
        self.assertIn(
            "if: github.event_name == 'push' && github.ref == 'refs/heads/main'",
            active,
        )
        self.assertIn(
            "if: success() && (github.event_name != 'push' || "
            "github.ref == 'refs/heads/main' || github.ref_type == 'tag')",
            active,
        )


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
    def test_working_manifest_matches_git_clean_filtered_head(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            init_repo(repo)
            (repo / ".gitattributes").write_text("*.md text eol=lf\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", ".gitattributes"], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "commit", "-qm", "define clean filter"],
                check=True,
            )
            base = run_git(repo, "rev-parse", "HEAD")
            path = repo / "skills" / "normalized.md"
            path.write_bytes(b"first\r\nsecond\r\n")

            _, working_changes = common.working_tree_name_status(repo, base)
            working_manifest = common.build_manifest(
                repo,
                working_changes,
                governed_predicate=common.is_governed_change,
            )
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "commit", "-qm", "add normalized file"],
                check=True,
            )
            head = run_git(repo, "rev-parse", "HEAD")
            _, _, committed_changes = common.diff_name_status(repo, base, head)
            committed_manifest = common.build_manifest(
                repo,
                committed_changes,
                head_sha=head,
                governed_predicate=common.is_governed_change,
            )

            self.assertEqual(working_manifest, committed_manifest)
            self.assertEqual(
                working_manifest[0]["sha256"],
                hashlib.sha256(b"first\nsecond\n").hexdigest(),
            )

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

    def test_v3_rejects_invented_gates_and_mode_override_drift(self) -> None:
        data = v3_artifact(status="pass", recommendation="go")
        data["required_gates"] = ["invented-easy-gate"]
        data["gate_status"] = {
            "invented-easy-gate": {
                "status": "pass",
                "evidence": ["fabricated evidence"],
                "waiver_reason": "",
            }
        }
        data["startup_declaration"]["skills_in_use"] = [
            "skill-governance",
            "invented-easy-gate",
        ]
        data["startup_declaration"]["skills_execution_order"] = [
            "skill-governance",
            "invented-easy-gate",
        ]
        data["critical_overrides"] = ["auth_or_permission_change"]

        errors, _ = validate.validate_artifact_data(
            data,
            strict=True,
            require_recommendation="go",
        )
        self.assertTrue(any("required_gates do not match" in error for error in errors), errors)
        self.assertTrue(any("absent from catalog binding" in error for error in errors), errors)
        self.assertTrue(any("selected_mode does not match" in error for error in errors), errors)

    def test_v3_requires_exact_startup_permutation_and_gate_status_set(self) -> None:
        data = v3_artifact(status="pass", recommendation="go")
        data["startup_declaration"]["skills_execution_order"] = ["skill-governance"]
        data["gate_status"]["extra-gate"] = {
            "status": "pass",
            "evidence": ["irrelevant"],
            "waiver_reason": "",
        }
        errors, _ = validate.validate_artifact_data(
            data,
            strict=True,
            require_recommendation="go",
        )
        self.assertTrue(any("exact permutations" in error for error in errors), errors)
        self.assertTrue(any("non-required gates" in error for error in errors), errors)

    def test_v3_schema_is_an_executable_closed_structural_boundary(self) -> None:
        valid = v3_artifact(status="pass", recommendation="go")
        errors, _ = validate.validate_artifact_data(
            valid,
            strict=True,
            require_recommendation="go",
        )
        self.assertEqual(errors, [])

        for mutation in (
            lambda data: data.update({"unknown_top_level": True}),
            lambda data: data["startup_declaration"].update({"unknown_nested": True}),
            lambda data: data["gate_status"]["scripted-command-execution"].update(
                {"unknown_nested": True}
            ),
            lambda data: data.update({"task_id": 123}),
            lambda data: data.update({"created_at_utc": "2026-07-17 12:00:00"}),
        ):
            with self.subTest(mutation=mutation):
                data = v3_artifact(status="pass", recommendation="go")
                mutation(data)
                errors, _ = validate.validate_artifact_data(
                    data,
                    strict=True,
                    require_recommendation="go",
                )
                self.assertTrue(any(error.startswith("schema ") for error in errors), errors)

    def test_v3_typed_evidence_rejects_placeholders_and_wrong_gate_kinds(self) -> None:
        data = v3_artifact(status="pass", recommendation="go")
        evidence = data["gate_status"]["scripted-command-execution"]["evidence"][0]
        evidence.update(
            {
                "kind": "review",
                "reference": "evidence",
                "revision_sha": None,
                "sha256": None,
            }
        )
        errors, _ = validate.validate_artifact_data(
            data,
            strict=True,
            require_recommendation="go",
        )
        self.assertTrue(any("does not accept evidence kind" in error for error in errors), errors)
        self.assertTrue(any("concrete evidence reference" in error for error in errors), errors)
        self.assertTrue(any("requires revision_sha or sha256" in error for error in errors), errors)

    def test_v3_schema_requires_and_applies_rfc3339_checker(self) -> None:
        data = v3_artifact(status="pass", recommendation="go")
        data["created_at_utc"] = "not-a-date-time"
        errors = validate._json_schema_errors(data)
        self.assertFalse(any("rfc3339-validator is required" in error for error in errors), errors)
        self.assertTrue(any("date-time" in error for error in errors), errors)

    def test_v3_external_critical_operations_cannot_claim_quick_zero_risk(self) -> None:
        for operation, scope in (
            ("configure_remote", "external"),
            ("deploy", "deployment"),
        ):
            with self.subTest(operation=operation):
                data = v3_artifact(status="pass", recommendation="go")
                data["authorized_operations"] = [operation]
                data["execution_scope"] = scope
                data["deployment_requested"] = operation == "deploy"
                errors, _ = validate.validate_artifact_data(
                    data,
                    strict=True,
                    require_recommendation="go",
                )
                self.assertTrue(any("selected_mode does not match" in error for error in errors), errors)
                self.assertTrue(any("required_gates do not match" in error for error in errors), errors)

        data = v3_artifact(status="pass", recommendation="go")
        data["authorized_operations"] = ["migrate"]
        data["execution_scope"] = "external"
        errors, _ = validate.validate_artifact_data(
            data,
            strict=True,
            require_recommendation="go",
        )
        self.assertTrue(any("requires backup and restore" in error for error in errors), errors)

    def test_v3_manifest_infers_minimum_documentation_gate(self) -> None:
        for path in (
            ".github/workflows/unsafe.yml",
            ".github/branch-protection-policy.json",
        ):
            with self.subTest(path=path):
                data = v3_artifact(status="pass", recommendation="go")
                manifest = [{"path": path, "status": "A", "sha256": "b" * 64}]
                data["change_binding"]["manifest"] = manifest
                data["change_binding"]["manifest_sha256"] = common.manifest_sha256(manifest)
                errors, _ = validate.validate_artifact_data(
                    data,
                    strict=True,
                    require_recommendation="go",
                )
                self.assertTrue(
                    any("behavior_or_workflow_changed must be true" in error for error in errors),
                    errors,
                )

    def test_v3_release_metadata_must_be_exact_and_manifest_bound(self) -> None:
        data = v3_release_artifact()
        data["release_metadata"]["tag"] = "v9.9.9"
        data["change_binding"]["manifest"] = [
            entry
            for entry in data["change_binding"]["manifest"]
            if entry["path"] != data["release_metadata"]["release_notes_path"]
        ]
        data["change_binding"]["manifest_sha256"] = common.manifest_sha256(
            data["change_binding"]["manifest"]
        )
        errors, _ = validate.validate_artifact_data(
            data,
            strict=True,
            require_recommendation="go",
        )
        self.assertTrue(any("tag must equal" in error for error in errors), errors)
        self.assertTrue(any("absent from the full manifest" in error for error in errors), errors)

    def test_v3_break_glass_is_bounded_and_cannot_waive_enforcement(self) -> None:
        data = v3_artifact(status="waived", recommendation="go-with-risk")
        data["gate_status"]["scripted-command-execution"]["waiver_reason"] = (
            "Approved temporary exception for unavailable runner"
        )
        data["break_glass"] = {
            "enabled": True,
            "reason": "Approved temporary exception for unavailable runner",
            "risk_owner": "release-owner",
            "remediation_ticket": "OPS-1234",
            "expiry_hours": 24,
        }
        errors, _ = validate.validate_artifact_data(
            data,
            strict=True,
            require_recommendation="go-with-risk",
        )
        self.assertEqual(errors, [])

        data["recommendation"] = "go"
        errors, _ = validate.validate_artifact_data(
            data,
            strict=True,
            require_recommendation="go",
        )
        self.assertTrue(any("break glass cannot support" in error for error in errors), errors)

        release = v3_release_artifact()
        release["gate_status"]["governance-enforcement"] = {
            "status": "waived",
            "evidence": [],
            "waiver_reason": "Approved temporary exception for unavailable runner",
        }
        release["break_glass"] = data["break_glass"]
        release["recommendation"] = "go-with-risk"
        errors, _ = validate.validate_artifact_data(
            release,
            strict=True,
            require_recommendation="go-with-risk",
        )
        self.assertTrue(any("non-waivable" in error for error in errors), errors)

        for expiry in (0, 169, "forever"):
            with self.subTest(expiry=expiry):
                invalid = v3_artifact(status="waived", recommendation="go-with-risk")
                invalid["gate_status"]["scripted-command-execution"]["waiver_reason"] = (
                    "Approved temporary exception for unavailable runner"
                )
                invalid["break_glass"] = {**data["break_glass"], "expiry_hours": expiry}
                errors, _ = validate.validate_artifact_data(
                    invalid,
                    strict=True,
                    require_recommendation="go-with-risk",
                )
                self.assertTrue(any("expiry_hours" in error for error in errors), errors)


class TestV3Generator(unittest.TestCase):
    def test_generator_writes_pending_no_go_change_bound_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            base = init_repo(repo)
            (repo / "skills" / "policy.md").write_text("changed\n", encoding="utf-8")
            (repo / "user-instructions.md").write_text("# Canonical ledger\n", encoding="utf-8")
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
            self.assertEqual(data["schema_version"], 3)
            self.assertEqual(data["recommendation"], "no-go")
            self.assertEqual(data["required_gates"], ["scripted-command-execution"])
            self.assertNotIn("project-backup", data["required_gates"])
            self.assertNotIn("restore-drill", data["required_gates"])
            self.assertTrue(
                all(record["status"] == "pending" for record in data["gate_status"].values())
            )
            errors, warnings = validate.validate_artifact_data(
                data,
                strict=False,
                require_recommendation="no-go",
            )
            self.assertEqual(errors, [])
            self.assertTrue(any("pending required gates" in warning for warning in warnings))
            self.assertEqual(data["change_binding"]["base_sha"], base)
            manifest_paths = {item["path"] for item in data["change_binding"]["manifest"]}
            self.assertIn("skills/policy.md", manifest_paths)
            self.assertIn("user-instructions.md", manifest_paths)
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

    def test_generator_refuses_to_overwrite_committed_task_identity(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            init_repo(repo)
            governance = repo / "docs" / "governance"
            governance.mkdir(parents=True)
            (governance / "TASK-EXISTS.governance.json").write_text("{}\n", encoding="utf-8")
            (governance / "TASK-EXISTS.governance.md").write_text("# existing\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "existing evidence"], check=True)
            base = run_git(repo, "rev-parse", "HEAD")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "generate_governance_artifact.py"),
                    "--task-id",
                    "TASK-EXISTS",
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
                    "skill-governance,scripted-command-execution",
                    "--skills-execution-order",
                    "skill-governance,scripted-command-execution",
                    "--skills-selection-rationale",
                    "Committed evidence must remain immutable.",
                ],
                cwd=repo,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("use a new superseding task ID", result.stdout + result.stderr)

    def test_generator_builds_exact_release_metadata_and_full_diff_binding(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            base = init_repo(repo)
            (repo / "skills" / "VERSION").write_text("2.0.0\n", encoding="utf-8")
            (repo / "skills" / "CHANGELOG.md").write_text(
                "# Changelog\n\n## [2.0.0] - 2026-07-18\n",
                encoding="utf-8",
            )
            (repo / "skills" / "RELEASE_NOTES_v2.0.0.md").write_text(
                "# v2.0.0\n\n- Skill count: `39`\n- Governance test count: `1`\n",
                encoding="utf-8",
            )
            tests = repo / "skills" / "skill-governance" / "tests"
            tests.mkdir(parents=True)
            (tests / "test_release.py").write_text(
                "class ReleaseTest:\n    def test_release(self):\n        pass\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "generate_governance_artifact.py"),
                    "--task-id",
                    "TASK-RELEASE",
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
                    "--purpose",
                    "release",
                    "--execution-scope",
                    "external",
                    "--authorized-operation",
                    "publish",
                    "--release-version",
                    "2.0.0",
                    "--release-tag",
                    "v2.0.0",
                    "--skills-in-use",
                    "skill-governance,regression-prevention,semantic-policy-audit,governance-enforcement,scripted-command-execution",
                    "--skills-execution-order",
                    "skill-governance,regression-prevention,semantic-policy-audit,governance-enforcement,scripted-command-execution",
                    "--skills-selection-rationale",
                    "Release metadata and exact full-diff evidence are required.",
                ],
                cwd=repo,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(
                (repo / "docs" / "governance" / "TASK-RELEASE.governance.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(data["selected_mode"], "critical")
            self.assertEqual(data["release_metadata"]["governance_test_count"], 1)
            manifest_paths = {entry["path"] for entry in data["change_binding"]["manifest"]}
            self.assertTrue(
                {
                    "skills/VERSION",
                    "skills/CHANGELOG.md",
                    "skills/RELEASE_NOTES_v2.0.0.md",
                }.issubset(manifest_paths)
            )


class TestChangeBindingAndAttestation(unittest.TestCase):
    def test_v3_catalog_binding_rejects_mismatch_at_exact_head(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            init_repo(repo)
            data = v3_artifact(status="pass", recommendation="go")
            catalog_path = repo / "skills" / "skill-catalog.json"
            original_catalog = catalog_path.read_bytes()
            changed_catalog = json.loads(original_catalog)
            changed_catalog["catalog_version"] = "99.0.0"
            catalog_path.write_text(
                json.dumps(changed_catalog, indent=2) + "\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "commit", "-qm", "change exact catalog"],
                check=True,
            )
            head = run_git(repo, "rev-parse", "HEAD")

            # Restore the working-tree bytes to prove enforcement reads the requested head.
            catalog_path.write_bytes(original_catalog)
            errors = enforce.catalog_binding_errors(data, repo, head)

            self.assertTrue(
                any("sha256 does not match the exact catalog" in error for error in errors),
                errors,
            )
            self.assertTrue(
                any("catalog_version does not match" in error for error in errors),
                errors,
            )

    def test_normal_enforcement_accepts_only_exact_bound_v3_plan(self) -> None:
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
            data = v3_artifact(status="pass", recommendation="go")
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
            data = v3_artifact(status="pass", recommendation="go")
            self.assertTrue(enforce.binding_errors(data, resolved_base, actual_manifest))

            data["change_binding"] = {
                "base_sha": resolved_base,
                "manifest": actual_manifest,
                "manifest_sha256": common.manifest_sha256(actual_manifest),
            }
            self.assertEqual(enforce.binding_errors(data, resolved_base, actual_manifest), [])

    def test_normal_enforcement_rejects_any_changed_unbound_v3_plan(self) -> None:
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

            exact = v3_artifact(status="pass", recommendation="go")
            exact["change_binding"] = {
                "base_sha": base,
                "manifest": manifest,
                "manifest_sha256": common.manifest_sha256(manifest),
            }
            stale = v3_artifact(status="pass", recommendation="go")
            stale["task_id"] = "TASK-2"

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
            with self.assertRaisesRegex(SystemExit, "Committed governance evidence is immutable"):
                enforce.reject_historical_artifact_mutation(changes)

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

    def test_release_enforcement_rejects_change_purpose_plan(self) -> None:
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
            data = v3_artifact(status="pass", recommendation="go")
            data["change_binding"] = {
                "base_sha": base,
                "manifest": manifest,
                "manifest_sha256": common.manifest_sha256(manifest),
            }
            governance = repo / "docs" / "governance"
            governance.mkdir(parents=True)
            (governance / "CHANGE.governance.json").write_text(
                json.dumps(data, indent=2) + "\n",
                encoding="utf-8",
            )
            (governance / "CHANGE.governance.md").write_text("# change\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "change plan"], check=True)
            head = run_git(repo, "rev-parse", "HEAD")

            output = StringIO()
            with redirect_stdout(output):
                with self.assertRaises(SystemExit):
                    enforce._release_enforcement(
                        head_sha=head,
                        repo_root=repo,
                        require_recommendation="go",
                    )
            self.assertIn("No strict schema v3 release artifact", output.getvalue())

    def test_release_enforcement_requires_and_accepts_one_full_diff_release_plan(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            base = init_repo(repo)
            (repo / "skills" / "policy.md").write_text("changed\n", encoding="utf-8")
            (repo / "README.md").write_text("release notes\n", encoding="utf-8")
            (repo / "skills" / "VERSION").write_text("2.0.0\n", encoding="utf-8")
            (repo / "skills" / "CHANGELOG.md").write_text(
                "# Changelog\n\n## [2.0.0] - 2026-07-18\n",
                encoding="utf-8",
            )
            (repo / "skills" / "RELEASE_NOTES_v2.0.0.md").write_text(
                "# v2.0.0\n\n- Skill count: `39`\n- Governance test count: `1`\n",
                encoding="utf-8",
            )
            tests = repo / "skills" / "skill-governance" / "tests"
            tests.mkdir(parents=True)
            (tests / "test_sample.py").write_text(
                "class Sample:\n    def test_release(self):\n        pass\n",
                encoding="utf-8",
            )
            _, working_changes = common.working_tree_name_status(repo, base)
            manifest = common.build_manifest(repo, working_changes)
            self.assertIn("README.md", {item["path"] for item in manifest})
            data = v3_release_artifact()
            data["release_metadata"]["governance_test_count"] = 1
            data["change_binding"] = {
                "base_sha": base,
                "manifest": manifest,
                "manifest_sha256": common.manifest_sha256(manifest),
            }
            governance = repo / "docs" / "governance"
            governance.mkdir(parents=True)
            (governance / "RELEASE.governance.json").write_text(
                json.dumps(data, indent=2) + "\n",
                encoding="utf-8",
            )
            (governance / "RELEASE.governance.md").write_text("# release\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "release plan"], check=True)
            head = run_git(repo, "rev-parse", "HEAD")

            actual_base, actual_head, actual_manifest, artifacts = enforce._release_enforcement(
                head_sha=head,
                repo_root=repo,
                require_recommendation="go",
            )
            self.assertEqual(actual_base, base)
            self.assertEqual(actual_head, head)
            self.assertEqual(actual_manifest, manifest)
            self.assertEqual([item["task_id"] for item in artifacts], ["TASK-1"])


if __name__ == "__main__":
    unittest.main()
