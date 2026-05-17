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


if __name__ == "__main__":
    unittest.main()
