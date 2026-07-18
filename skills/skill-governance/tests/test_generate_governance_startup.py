import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generate_governance_artifact.py"


spec = importlib.util.spec_from_file_location("generate_governance_artifact", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class TestStartupDeclarationValidation(unittest.TestCase):
    def test_render_markdown_does_not_emit_trailing_whitespace_for_empty_waiver(self) -> None:
        artifact = SimpleNamespace(
            task_id="TASK-1",
            schema_version=2,
            created_at_utc="2026-07-18T00:00:00+00:00",
            project_id="agent-command-center",
            profile="internal",
            project_language="Markdown/Python",
            project_description_max4="Agent command center",
            model_runs_test_build_default="yes",
            execution_scope="local_only",
            deployment_requested=False,
            execution_skill="scripted-command-execution",
            quizme_mode="off",
            quizme_multiple_choice=False,
            quizme_one_at_a_time=False,
            quizme_confirm=False,
            quizme_record=False,
            selected_mode="quick",
            total_score=1,
            recommendation="no-go",
            scores={"data_impact": 0},
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
                "skills_selection_rationale": "Governed command execution.",
                "skills_execution_order": [
                    "skill-governance",
                    "scripted-command-execution",
                ],
            },
            evidence_requirements=[],
            break_glass={"enabled": False},
            notes="",
            change_binding={
                "base_sha": "a" * 40,
                "manifest_sha256": "b" * 64,
                "manifest": [],
            },
        )

        rendered = module.render_markdown(artifact)

        self.assertIn("  - waiver_reason:\n", rendered)
        self.assertEqual([], [line for line in rendered.splitlines() if line.rstrip() != line])

    def test_mode_gates_are_proportional_and_do_not_restore_v1_defaults(self) -> None:
        self.assertEqual(
            module.build_required_gates("quick", "scripted-command-execution", False),
            ["scripted-command-execution"],
        )
        self.assertEqual(
            module.build_required_gates("standard", "scripted-command-execution", False),
            ["scripted-command-execution", "regression-prevention"],
        )
        self.assertEqual(
            module.build_required_gates("critical", "scripted-command-execution", False),
            [
                "scripted-command-execution",
                "regression-prevention",
                "semantic-policy-audit",
                "governance-enforcement",
            ],
        )
        for mode in ("quick", "standard", "critical"):
            gates = module.build_required_gates(mode, "scripted-command-execution", False)
            self.assertNotIn("token-reduction", gates)
            self.assertNotIn("order-of-operations", gates)
            self.assertNotIn("project-backup", gates)
            self.assertNotIn("restore-drill", gates)

    def test_backup_and_restore_are_effect_gated_not_mode_gated(self) -> None:
        backup = module.build_required_gates(
            "critical",
            "scripted-command-execution",
            False,
            requires_backup=True,
        )
        restore = module.build_required_gates(
            "critical",
            "scripted-command-execution",
            False,
            requires_restore=True,
        )
        self.assertEqual(backup[-1:], ["project-backup"])
        self.assertEqual(restore[-2:], ["project-backup", "restore-drill"])
        self.assertEqual(
            module.build_evidence_requirements("quick", requires_restore=True)[-2:],
            ["backup artifact + integrity evidence", "restore freshness/pass status"],
        )

    def test_valid_startup_skills(self) -> None:
        module.validate_startup_declaration_skills(
            [
                "skill-governance",
                "order-of-operations",
                "scripted-command-execution",
                "doc-maintenance",
            ],
            [
                "skill-governance",
                "order-of-operations",
                "scripted-command-execution",
                "doc-maintenance",
            ],
            "scripted-command-execution",
        )

    def test_rejects_mismatched_sets(self) -> None:
        with self.assertRaises(SystemExit):
            module.validate_startup_declaration_skills(
                ["skill-governance", "order-of-operations"],
                ["skill-governance", "order-of-operations", "scripted-command-execution"],
                "scripted-command-execution",
            )

    def test_rejects_missing_required_governed_skill(self) -> None:
        with self.assertRaises(SystemExit):
            module.validate_startup_declaration_skills(
                ["order-of-operations", "doc-maintenance"],
                ["order-of-operations", "doc-maintenance"],
                "scripted-command-execution",
            )

    def test_order_of_operations_is_conditional_not_a_governance_baseline(self) -> None:
        module.validate_startup_declaration_skills(
            ["skill-governance", "scripted-command-execution"],
            ["skill-governance", "scripted-command-execution"],
            "scripted-command-execution",
        )

    def test_quizme_mode_requires_quizme_skill(self) -> None:
        with self.assertRaises(SystemExit):
            module.validate_startup_declaration_skills(
                [
                    "skill-governance",
                    "order-of-operations",
                    "scripted-command-execution",
                ],
                [
                    "skill-governance",
                    "order-of-operations",
                    "scripted-command-execution",
                ],
                "scripted-command-execution",
                "on",
            )

    def test_quizme_mode_accepts_quizme_skill(self) -> None:
        module.validate_startup_declaration_skills(
            [
                "quizme-mode",
                "skill-governance",
                "order-of-operations",
                "scripted-command-execution",
            ],
            [
                "quizme-mode",
                "skill-governance",
                "order-of-operations",
                "scripted-command-execution",
            ],
            "scripted-command-execution",
            "on",
        )

    def test_quizme_mc_requires_active_mode(self) -> None:
        with self.assertRaises(SystemExit):
            module.validate_quizme_fields("off", True)

    def test_quizme_mc_accepts_active_mode(self) -> None:
        module.validate_quizme_fields("on", True)

    def test_each_quizme_option_requires_active_mode(self) -> None:
        option_sets = [
            (False, True, False, False),
            (False, False, True, False),
            (False, False, False, True),
        ]
        for options in option_sets:
            with self.subTest(options=options):
                with self.assertRaises(SystemExit):
                    module.validate_quizme_fields("off", *options)

    def test_combined_quizme_options_accept_active_mode(self) -> None:
        module.validate_quizme_fields("on", True, True, True, True)


if __name__ == "__main__":
    unittest.main()
