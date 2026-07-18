"""Semantic regression gates for the two former universal-default skills."""

from pathlib import Path
import unittest


SKILLS_ROOT = Path(__file__).resolve().parents[2]


def package_text(name: str) -> str:
    root = SKILLS_ROOT / name
    files = [root / "SKILL.md", *sorted((root / "references").glob("*.md"))]
    return "\n".join(path.read_text(encoding="utf-8") for path in files)


class TestConditionalSkillQualityGates(unittest.TestCase):
    def test_internal_lang_is_explicit_conversation_local_and_lossless(self) -> None:
        content = package_text("internal-lang")
        required = [
            "Remain inactive unless the user invokes a supported command",
            "/internal-lang on",
            "/internal-lang off",
            "/internal-lang --response on",
            "/internal-lang --response off",
            "The newest explicit command wins",
            "Do not assume state persists into a new conversation",
            "Do not expose hidden chain of thought",
            "expand every symbol into plain language",
            "No file was created or changed solely because this skill activated",
        ]
        for invariant in required:
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, content)

    def test_hyperfocus_is_bounded_branch_control_not_scope_expansion(self) -> None:
        content = package_text("hyperfocus-discovery")
        required = [
            "user explicitly requests bounded adjacent exploration",
            "Do not activate for routine, single-threaded, answer-only, or one-command work",
            "at most two switches",
            "at most three switches before convergence",
            "Preserve the original goal and explicit acceptance criteria",
            "Do not implement adjacent work merely because it appears useful",
            "User approval is required before a branch introduces",
            "Mark each `done`, `deferred`, or `rejected`",
            "Do not expose the full private stack unless the user asks for it",
            "Do not create files, trackers, or artifacts solely because this skill activated",
        ]
        for invariant in required:
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, content)

    def test_neither_skill_claims_universal_default_activation(self) -> None:
        internal = (SKILLS_ROOT / "internal-lang" / "SKILL.md").read_text(encoding="utf-8")
        hyperfocus = (SKILLS_ROOT / "hyperfocus-discovery" / "SKILL.md").read_text(encoding="utf-8")
        for prohibited in (
            "Apply by default",
            "Use on every task",
            "always activate",
            "universal default",
        ):
            with self.subTest(prohibited=prohibited):
                self.assertNotIn(prohibited, internal)
                self.assertNotIn(prohibited, hyperfocus)


if __name__ == "__main__":
    unittest.main()
