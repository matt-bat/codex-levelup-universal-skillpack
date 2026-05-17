import subprocess
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_skill_policy.py"
SKILLS_ROOT = Path(__file__).resolve().parents[2]


class TestValidateSkillPolicySmoke(unittest.TestCase):
    def test_policy_validator_passes_on_current_tree(self) -> None:
        result = subprocess.run(
            ["python3", str(SCRIPT), "--skills-root", str(SKILLS_ROOT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Skill policy validation passed.", result.stdout)


if __name__ == "__main__":
    unittest.main()
