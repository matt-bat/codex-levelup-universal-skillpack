import subprocess
import tempfile
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_skill_order_sync.py"


class TestValidateSkillOrderSync(unittest.TestCase):
    def _write_files(self, root: Path, map_order: list[str], index_order: list[str]) -> None:
        map_lines = [
            "# Skill Map",
            "",
            "## Skill Index",
        ]
        map_lines.extend([f"{i + 1}. `{name}`" for i, name in enumerate(map_order)])
        map_lines.append("")
        map_lines.append("## End")
        (root / "SKILL-MAP.md").write_text("\n".join(map_lines) + "\n", encoding="utf-8")

        docs = root / "docs"
        docs.mkdir(parents=True, exist_ok=True)
        index_lines = [
            "# Skill Index",
            "",
            "| Skill | Primary Trigger | Typical Triggers Another Skill | Canonical Artifacts | Last Updated UTC |",
            "|---|---|---|---|---|",
        ]
        for name in index_order:
            index_lines.append(
                f"| `{name}` | trigger | `other` | artifact | 2026-05-13T00:00:00Z |"
            )
        (docs / "skill-index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    def test_passes_when_order_matches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            order = ["alpha", "beta", "gamma"]
            self._write_files(root, order, order)
            result = subprocess.run(
                ["python3", str(SCRIPT), "--skills-root", str(root)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Skill ordering sync validation passed.", result.stdout)

    def test_fails_when_order_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_files(root, ["alpha", "beta", "gamma"], ["alpha", "gamma", "beta"])
            result = subprocess.run(
                ["python3", str(SCRIPT), "--skills-root", str(root)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Order mismatch", result.stdout)


if __name__ == "__main__":
    unittest.main()
