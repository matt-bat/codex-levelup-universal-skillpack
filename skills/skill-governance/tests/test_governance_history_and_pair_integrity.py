from dataclasses import asdict
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import enforce_governance_ci as enforce
import generate_governance_artifact as generate
import governance_common as common
import validate_skill_policy as policy


def run_git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def commit_all(repo: Path, message: str) -> str:
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", message], check=True)
    return run_git(repo, "rev-parse", "HEAD")


def init_repo(repo: Path) -> str:
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "Governance Test"], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "config", "user.email", "governance@example.invalid"],
        check=True,
    )
    (repo / "README.md").write_text("base\n", encoding="utf-8")
    return commit_all(repo, "base")


def write_artifact_pair(repo: Path, body: str = "one\n") -> tuple[Path, Path]:
    governance = repo / "docs" / "governance"
    governance.mkdir(parents=True, exist_ok=True)
    json_path = governance / "TASK.governance.json"
    md_path = governance / "TASK.governance.md"
    json_path.write_text(body, encoding="utf-8")
    md_path.write_text("# evidence\n", encoding="utf-8")
    return json_path, md_path


def v3_artifact() -> generate.GovernanceArtifact:
    return generate.GovernanceArtifact(
        schema_version=3,
        task_id="TASK-PAIR",
        purpose="change",
        authorized_operations=[],
        release_metadata=None,
        project_id="agent-command-center",
        created_at_utc="2026-07-18T05:00:00+00:00",
        profile="internal",
        project_language="Python",
        project_description_max4="Agent command center",
        model_runs_test_build_default="yes",
        execution_scope="local_only",
        deployment_requested=False,
        execution_skill="scripted-command-execution",
        behavior_or_workflow_changed=False,
        uncertainty_high=False,
        requires_backup=False,
        requires_restore=False,
        quizme_mode="off",
        quizme_multiple_choice=False,
        quizme_one_at_a_time=False,
        quizme_confirm=False,
        quizme_record=False,
        scores={
            "data_impact": 0,
            "business_impact": 0,
            "change_complexity": 0,
            "dependency_uncertainty": 0,
            "recoverability": 0,
        },
        total_score=0,
        base_mode="quick",
        mode_after_profile="quick",
        selected_mode="quick",
        critical_overrides=[],
        required_gates=["scripted-command-execution"],
        gate_status={
            "scripted-command-execution": {
                "status": "pending",
                "evidence": [],
                "waiver_reason": "",
            }
        },
        startup_declaration={
            "skills_in_use": ["skill-governance", "scripted-command-execution"],
            "skills_selection_rationale": "Governed deterministic execution is required.",
            "skills_execution_order": ["skill-governance", "scripted-command-execution"],
        },
        evidence_requirements=[
            "mode + score",
            "steps executed",
            "minimal validation outcomes",
        ],
        break_glass={
            "enabled": False,
            "reason": "",
            "risk_owner": "",
            "remediation_ticket": "",
            "expiry_hours": None,
        },
        recommendation="no-go",
        change_binding={
            "base_sha": "a" * 40,
            "manifest": [],
            "manifest_sha256": common.manifest_sha256([]),
        },
        notes="",
        catalog_binding={
            "path": "skills/skill-catalog.json",
            "sha256": "b" * 64,
            "catalog_version": "2.0.1",
            "router_contract": "2.0",
            "components": ["core-policy"],
            "skills": {
                "scripted-command-execution": {},
                "skill-governance": {},
            },
        },
    )


class TestAppendOnlyHistoryRange(unittest.TestCase):
    def test_single_addition_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            base = init_repo(repo)
            write_artifact_pair(repo)
            head = commit_all(repo, "add governance evidence")

            enforce.reject_artifact_mutation_within_range(repo, base, head)

    def test_merge_carrying_an_unchanged_addition_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            base = init_repo(repo)
            main_branch = run_git(repo, "branch", "--show-current")
            subprocess.run(["git", "-C", str(repo), "switch", "-qc", "evidence"], check=True)
            write_artifact_pair(repo)
            commit_all(repo, "add governance evidence")

            subprocess.run(["git", "-C", str(repo), "switch", "-q", main_branch], check=True)
            (repo / "README.md").write_text("main change\n", encoding="utf-8")
            commit_all(repo, "advance main")
            subprocess.run(
                ["git", "-C", str(repo), "merge", "--no-ff", "-qm", "merge evidence", "evidence"],
                check=True,
            )
            head = run_git(repo, "rev-parse", "HEAD")

            enforce.reject_artifact_mutation_within_range(repo, base, head)

    def test_addition_then_modification_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            base = init_repo(repo)
            json_path, _ = write_artifact_pair(repo)
            commit_all(repo, "add governance evidence")
            json_path.write_text("two\n", encoding="utf-8")
            head = commit_all(repo, "rewrite governance evidence")

            with self.assertRaisesRegex(SystemExit, "cannot change after its first commit"):
                enforce._normal_enforcement(
                    base_sha=base,
                    head_sha=head,
                    repo_root=repo,
                    strict=False,
                    require_recommendation="no-go",
                )

    def test_transient_addition_then_deletion_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo = Path(raw)
            base = init_repo(repo)
            json_path, md_path = write_artifact_pair(repo)
            commit_all(repo, "add governance evidence")
            json_path.unlink()
            md_path.unlink()
            head = commit_all(repo, "delete governance evidence")

            self.assertEqual(run_git(repo, "diff", "--name-only", base, head), "")
            with self.assertRaisesRegex(SystemExit, "cannot change after its first commit"):
                enforce._normal_enforcement(
                    base_sha=base,
                    head_sha=head,
                    repo_root=repo,
                    strict=False,
                    require_recommendation="no-go",
                )


class TestSchemaV3MarkdownPair(unittest.TestCase):
    def test_v3_requires_exact_canonical_rendering(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            artifact = v3_artifact()
            json_path = root / "TASK-PAIR.governance.json"
            md_path = root / "TASK-PAIR.governance.md"
            json_path.write_text(json.dumps(asdict(artifact), indent=2) + "\n", encoding="utf-8")
            canonical = generate.render_markdown(artifact) + "\n"
            self.assertFalse(canonical.endswith("\n\n"))
            md_path.write_text(canonical, encoding="utf-8")

            self.assertEqual(policy.validate_artifact_pair(json_path), [])

            md_path.write_text(
                canonical.replace("# Governance Artifact", "# Altered Artifact", 1),
                encoding="utf-8",
            )
            errors = policy.validate_artifact_pair(json_path)
            self.assertTrue(
                any("does not equal the canonical" in error for error in errors),
                errors,
            )

    def test_v1_and_v2_keep_marker_compatibility(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            for schema_version in (1, 2):
                with self.subTest(schema_version=schema_version):
                    stem = f"LEGACY-{schema_version}"
                    json_path = root / f"{stem}.governance.json"
                    md_path = root / f"{stem}.governance.md"
                    data = {
                        "quizme_mode": "off",
                        "quizme_multiple_choice": False,
                        "quizme_one_at_a_time": False,
                        "quizme_confirm": False,
                        "quizme_record": False,
                        "startup_declaration": {
                            "skills_in_use": ["legacy-skill"],
                            "skills_selection_rationale": "Historical evidence.",
                            "skills_execution_order": ["legacy-skill"],
                        },
                    }
                    if schema_version == 2:
                        data["schema_version"] = schema_version
                    markers = [
                        "## Startup Declaration",
                        "### Skills In Use",
                        "### Skill Execution Order",
                        "`quizme_mode`",
                        "`quizme_multiple_choice`",
                        "`quizme_one_at_a_time`",
                        "`quizme_confirm`",
                        "`quizme_record`",
                    ]
                    if schema_version == 2:
                        data["change_binding"] = {
                            "base_sha": "a" * 40,
                            "manifest": [],
                            "manifest_sha256": common.manifest_sha256([]),
                        }
                        markers.extend(
                            ["`schema_version`: 2", "## Change Binding", "`manifest_sha256`"]
                        )
                    json_path.write_text(json.dumps(data) + "\n", encoding="utf-8")
                    md_path.write_text(
                        "\n".join(markers) + "\nlegacy free-form text\n",
                        encoding="utf-8",
                    )

                    self.assertEqual(policy.validate_artifact_pair(json_path), [])


if __name__ == "__main__":
    unittest.main()
