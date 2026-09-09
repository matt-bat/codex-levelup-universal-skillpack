import copy
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest


SKILLS_ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE_ROOT = SKILLS_ROOT / "skill-governance"
FIXTURE = json.loads((GOVERNANCE_ROOT / "fixtures/routing-scenarios.json").read_text(encoding="utf-8"))

sys.path.insert(0, str(GOVERNANCE_ROOT / "scripts"))
import resolve_task_route as router  # noqa: E402

SVG_SPEC = importlib.util.spec_from_file_location(
    "advanced_svg_validator",
    SKILLS_ROOT / "advanced-svg/scripts/validate_svg.py",
)
assert SVG_SPEC and SVG_SPEC.loader
svg_validator = importlib.util.module_from_spec(SVG_SPEC)
SVG_SPEC.loader.exec_module(svg_validator)


class TestNewSkillRouting(unittest.TestCase):
    def descriptor(self, **action_overrides):
        descriptor = copy.deepcopy(FIXTURE["descriptor_defaults"])
        descriptor["task_id"] = "new-skill-test"
        descriptor["action"].update(action_overrides)
        return descriptor

    def test_advanced_research_routes_from_typed_intensity(self) -> None:
        result = router.resolve_task_route(self.descriptor(research_intensity="advanced"))
        self.assertEqual(result["selected_skills"], ["advanced-r-and-d"])

    def test_help_routes_only_from_typed_exact_command_signal(self) -> None:
        result = router.resolve_task_route(self.descriptor(help_requested=True))
        self.assertEqual(result["selected_skills"], ["help"])
        ordinary = router.resolve_task_route(self.descriptor())
        self.assertNotIn("help", ordinary["selected_skills"])

    def test_vector_graphics_routes_to_advanced_svg(self) -> None:
        descriptor = self.descriptor()
        descriptor["domains"] = ["vector_graphics"]
        result = router.resolve_task_route(descriptor)
        self.assertEqual(result["selected_skills"], ["advanced-svg"])

    def test_agent_humility_routes_only_for_evidence_challenged_approaches(self) -> None:
        challenged = router.resolve_task_route(self.descriptor(approach_state="challenged"))
        self.assertEqual(challenged["selected_skills"], ["agent-humility"])
        self.assertEqual(
            challenged["decision_domain_owners"]["approach_reassessment"],
            "agent-humility",
        )

        for state in ("not_applicable", "viable"):
            with self.subTest(state=state):
                result = router.resolve_task_route(self.descriptor(approach_state=state))
                self.assertNotIn("agent-humility", result["selected_skills"])

    def test_noncritical_uncertainty_still_blocks_for_user_choice(self) -> None:
        descriptor = self.descriptor()
        descriptor["material_uncertainties"] = [{
            "id": "format-choice",
            "description": "The requested output format is not specified.",
            "severity": "noncritical",
            "status": "unresolved",
        }]
        result = router.resolve_task_route(descriptor)
        self.assertEqual(
            result["selected_skills"],
            ["requirement-clarifier", "eliminate-assumptions"],
        )
        self.assertEqual(result["decision"], "needs_clarification")
        self.assertEqual(result["vetoes"][0]["code"], "assumption_unresolved")


class TestNewSkillPackages(unittest.TestCase):
    def test_user_facing_activation_commands_use_double_dash(self) -> None:
        slash_commands = []
        for path in SKILLS_ROOT.glob("*/SKILL.md"):
            for command in re.findall(r"`(/[a-z][^`]*)`", path.read_text(encoding="utf-8")):
                slash_commands.append(f"{path.parent.name}: {command}")
        self.assertEqual(slash_commands, [])

        help_text = (SKILLS_ROOT / "help/SKILL.md").read_text(encoding="utf-8")
        command_section = help_text.split("## Supported Commands", 1)[1].split("## Output Contract", 1)[0]
        commands = re.findall(r"^- `([^`]+)`:", command_section, flags=re.MULTILINE)
        self.assertTrue(commands)
        self.assertTrue(all(command.startswith("--") for command in commands), commands)

    def test_help_marker_contract_is_catalog_derived(self) -> None:
        content = (SKILLS_ROOT / "help/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("routing_mode` is `explicit_only`", content)
        self.assertIn("send --help to learn more about available tools in agent-command-center", content)

    def test_clean_slate_preserves_active_controls(self) -> None:
        content = (SKILLS_ROOT / "clean-slate/SKILL.md").read_text(encoding="utf-8")
        for invariant in (
            "cannot erase already loaded model context",
            "safety, legal, security, privacy, and authority constraints",
            "not data erasure",
            "Do not delete, rewrite, or hide history",
        ):
            self.assertIn(invariant, content)

    def test_agent_humility_has_evidence_pivot_and_authority_boundaries(self) -> None:
        content = (SKILLS_ROOT / "agent-humility/SKILL.md").read_text(encoding="utf-8")
        for invariant in (
            "Do not repeat an unchanged attempt",
            "Goal",
            "Observed",
            "Invalidated",
            "Next discriminator",
            "External evidence outranks self-generated confidence",
            "Authority And Safety",
        ):
            self.assertIn(invariant, content)

    def test_svg_validator_accepts_safe_file_and_rejects_unsafe_features(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            safe = root / "safe.svg"
            safe.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10" aria-hidden="true">'
                '<defs><linearGradient id="g"><stop offset="0"/></linearGradient></defs>'
                '<rect width="10" height="10" fill="url(#g)" stroke="red"/></svg>',
                encoding="utf-8",
            )
            self.assertEqual(svg_validator.validate(safe, False), [])

            unsafe = root / "unsafe.svg"
            unsafe.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
                '<script>bad()</script><use href="#missing" onclick="bad()"/></svg>',
                encoding="utf-8",
            )
            findings = "\n".join(svg_validator.validate(unsafe, False))
            self.assertIn("unsafe-element", findings)
            self.assertIn("event-handler", findings)
            self.assertIn("unresolved-reference", findings)

    def test_svg_validator_requires_an_explicit_accessibility_strategy(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing-a11y.svg"
            missing.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
                '<rect width="10" height="10"/></svg>',
                encoding="utf-8",
            )
            findings = "\n".join(svg_validator.validate(missing, False))
            self.assertIn("ERROR accessibility", findings)

            informative = Path(temp_dir) / "informative.svg"
            informative.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10" '
                'role="img" aria-labelledby="title desc">'
                '<title id="title">Status</title><desc id="desc">Ready</desc>'
                '<circle cx="5" cy="5" r="4"/></svg>',
                encoding="utf-8",
            )
            self.assertEqual(svg_validator.validate(informative, False), [])

    def test_svg_validator_blocks_external_css_and_active_document_directives(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unsafe = Path(temp_dir) / "css-unsafe.svg"
            unsafe.write_text(
                '<!DOCTYPE svg><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10" '
                'aria-hidden="true"><style>@import "https://example.invalid/x.css"; '
                'rect { fill: url(https://example.invalid/x.png); }</style>'
                '<rect width="10" height="10"/></svg>',
                encoding="utf-8",
            )
            findings = "\n".join(svg_validator.validate(unsafe, False))
            self.assertIn("active-document-directive", findings)
            self.assertIn("css-import", findings)
            self.assertIn("external-css-reference", findings)


if __name__ == "__main__":
    unittest.main()
