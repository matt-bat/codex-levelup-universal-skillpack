import importlib.util
from pathlib import Path
import sys
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "enforce_governance_ci.py"


spec = importlib.util.spec_from_file_location("enforce_governance_ci", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class TestGovernedScope(unittest.TestCase):
    def test_governed_paths(self) -> None:
        self.assertTrue(module.is_governed_change(".codex/skills/SKILL-MAP.md"))
        self.assertTrue(module.is_governed_change("skills/SKILL-MAP.md"))
        self.assertTrue(module.is_governed_change("docs/governance/TASK-1.governance.json"))
        self.assertTrue(module.is_governed_change("docs/project-index.md"))
        self.assertTrue(module.is_governed_change(".github/branch-protection-policy.json"))
        self.assertTrue(module.is_governed_change("user-instructions.md"))
        self.assertTrue(module.is_governed_change("AGENTS.md"))
        self.assertTrue(module.is_governed_change(".github/workflows/ci.yml"))

    def test_non_governed_paths(self) -> None:
        self.assertFalse(module.is_governed_change("frontend/src/app.tsx"))
        self.assertFalse(module.is_governed_change("README.md"))
        self.assertFalse(module.is_governed_change("docs/notes.md"))

    def test_artifact_detection(self) -> None:
        files = [
            "docs/governance/A.governance.json",
            "docs/governance/A.governance.md",
            "frontend/src/x.ts",
        ]
        artifacts = module.changed_governance_artifacts(files)
        self.assertEqual(artifacts, ["docs/governance/A.governance.json"])


if __name__ == "__main__":
    unittest.main()
