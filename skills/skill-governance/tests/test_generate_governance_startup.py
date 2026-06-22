import importlib.util
from pathlib import Path
import sys
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generate_governance_artifact.py"


spec = importlib.util.spec_from_file_location("generate_governance_artifact", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class TestStartupDeclarationValidation(unittest.TestCase):
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

    def test_rejects_missing_required_baseline(self) -> None:
        with self.assertRaises(SystemExit):
            module.validate_startup_declaration_skills(
                ["skill-governance", "doc-maintenance"],
                ["skill-governance", "doc-maintenance"],
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
