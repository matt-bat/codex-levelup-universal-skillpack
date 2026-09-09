import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import os
import tempfile
import unittest


SKILLS_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = SKILLS_ROOT / "help/scripts/runtime_adapter.py"
SPEC = importlib.util.spec_from_file_location("command_center_runtime", SCRIPT)
assert SPEC and SPEC.loader
runtime = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runtime)


class TestRuntimeAdapter(unittest.TestCase):
    def setUp(self):
        self._preferences_tmp = tempfile.TemporaryDirectory()
        self._old_preferences = os.environ.get("AGENT_COMMAND_CENTER_PREFERENCES")
        os.environ["AGENT_COMMAND_CENTER_PREFERENCES"] = str(Path(self._preferences_tmp.name) / "preferences.json")

    def tearDown(self):
        if self._old_preferences is None:
            os.environ.pop("AGENT_COMMAND_CENTER_PREFERENCES", None)
        else:
            os.environ["AGENT_COMMAND_CENTER_PREFERENCES"] = self._old_preferences
        self._preferences_tmp.cleanup()

    def event(self, message=None, state=None):
        payload = {"schema_version": 1, "event": "pack_loaded" if message is None else "user_message"}
        if message is not None:
            payload["message"] = message
        if state is not None:
            payload["state"] = state
        return runtime.process_event(payload)

    def test_startup_hint_emits_once_across_state_handoff(self):
        first = self.event()
        self.assertEqual(first["startup_messages"], [runtime.STARTUP_HINT])
        second = self.event("ordinary task", first["state"])
        self.assertEqual(second["startup_messages"], [])
        self.assertFalse(second["consume_message"])

    def test_first_user_message_also_emits_startup_hint(self):
        result = self.event("ordinary task")
        self.assertEqual(result["startup_messages"], [runtime.STARTUP_HINT])
        self.assertRegex(result["source_sha256"], r"^[0-9a-f]{64}$")

    def test_help_is_exact_consumed_and_router_ready(self):
        result = self.event("--help")
        self.assertEqual(result["recognized_command"], "help")
        self.assertTrue(result["consume_message"])
        self.assertEqual(result["descriptor_patch"], {"action": {"help_requested": True}})
        malformed = self.event("--help extra", result["state"])
        self.assertEqual(malformed["descriptor_patch"], {})
        self.assertFalse(malformed["consume_message"])
        self.assertIn("exact command", malformed["notices"][0])

    def test_patch_application_preserves_host_normalized_explicit_skills(self):
        result = self.event("--clean-slate")
        descriptor = {
            "action": {"help_requested": False, "research_intensity": "advanced"},
            "constraints": {"explicit_skills": ["thoroughly-rate-review"]},
        }
        merged = runtime.apply_descriptor_patch(descriptor, result["descriptor_patch"])
        self.assertEqual(
            merged["constraints"]["explicit_skills"],
            ["thoroughly-rate-review", "clean-slate"],
        )
        self.assertEqual(merged["action"]["research_intensity"], "advanced")
        self.assertEqual(descriptor["constraints"]["explicit_skills"], ["thoroughly-rate-review"])

        ordinary = self.event("explain the available tools", result["state"])
        semantic_help = {
            "action": {"help_requested": True},
            "constraints": {"explicit_skills": []},
        }
        preserved = runtime.apply_descriptor_patch(semantic_help, ordinary["descriptor_patch"])
        self.assertTrue(preserved["action"]["help_requested"])

    def test_clean_slate_persists_then_disables(self):
        enabled = self.event("--clean-slate")
        self.assertTrue(enabled["state"]["clean_slate"])
        self.assertEqual(enabled["descriptor_patch"]["constraints"]["explicit_skills"], ["clean-slate"])
        ordinary = self.event("build a greenfield app", enabled["state"])
        self.assertEqual(ordinary["descriptor_patch"]["constraints"]["explicit_skills"], ["clean-slate"])
        disabled = self.event("--clean-slate off", ordinary["state"])
        self.assertFalse(disabled["state"]["clean_slate"])
        self.assertEqual(disabled["descriptor_patch"]["constraints"]["explicit_skills"], ["clean-slate"])
        after = self.event("ordinary task", disabled["state"])
        self.assertNotIn("constraints", after["descriptor_patch"])

    def test_quizme_options_replace_and_record_implies_confirm(self):
        enabled = self.event("--quizme --record --mc --mc")
        quizme = enabled["state"]["quizme"]
        self.assertTrue(quizme["enabled"])
        self.assertTrue(quizme["record"])
        self.assertTrue(quizme["confirm"])
        self.assertTrue(quizme["multiple_choice"])
        replaced = self.event("--quizme --one-at-a-time", enabled["state"])
        quizme = replaced["state"]["quizme"]
        self.assertTrue(quizme["enabled"])
        self.assertTrue(quizme["one_at_a_time"])
        self.assertFalse(quizme["multiple_choice"])
        self.assertFalse(quizme["record"])

    def test_plain_quizme_toggles_and_clears_options(self):
        enabled = self.event("--quizme --confirm")
        disabled = self.event("--quizme", enabled["state"])
        self.assertFalse(disabled["state"]["quizme"]["enabled"])
        self.assertFalse(any(disabled["state"]["quizme"].values()))
        invalid = self.event("--quizme --unsupported", disabled["state"])
        self.assertEqual(invalid["state"], disabled["state"])
        self.assertFalse(invalid["consume_message"])
        self.assertIn("not applied", invalid["notices"][0])

    def test_internal_lang_controls_are_independent(self):
        response_on = self.event("--internal-lang --response on")
        self.assertFalse(response_on["state"]["internal_lang"]["internal"])
        self.assertTrue(response_on["state"]["internal_lang"]["response"])
        internal_on = self.event("--internal-lang on", response_on["state"])
        self.assertTrue(internal_on["state"]["internal_lang"]["internal"])
        self.assertTrue(internal_on["state"]["internal_lang"]["response"])

    def test_ill_run_scripts_toggle_persists_across_conversations(self):
        with tempfile.TemporaryDirectory() as raw:
            old = os.environ.get("AGENT_COMMAND_CENTER_PREFERENCES")
            os.environ["AGENT_COMMAND_CENTER_PREFERENCES"] = str(Path(raw) / "preferences.json")
            try:
                enabled = self.event("--ill-run-scripts")
                self.assertTrue(enabled["state"]["user_run_scripts"])
                fresh = self.event()
                self.assertTrue(fresh["state"]["user_run_scripts"])
                self.assertEqual(fresh["descriptor_patch"]["constraints"]["explicit_skills"], ["user-run-scripts"])
                disabled = self.event("--ill-run-scripts", fresh["state"])
                self.assertFalse(disabled["state"]["user_run_scripts"])
            finally:
                if old is None:
                    os.environ.pop("AGENT_COMMAND_CENTER_PREFERENCES", None)
                else:
                    os.environ["AGENT_COMMAND_CENTER_PREFERENCES"] = old

    def test_unknown_command_is_not_consumed(self):
        result = self.event("--not-a-command value")
        self.assertIsNone(result["recognized_command"])
        self.assertFalse(result["consume_message"])
        self.assertIn("Unknown command", result["notices"][0])

    def test_invalid_known_commands_are_not_consumed_or_applied(self):
        initial = self.event()
        for message in (
            "--clean-slate later",
            "--quizme please clarify this task",
            "--internal-lang maybe",
        ):
            with self.subTest(message=message):
                result = self.event(message, initial["state"])
                self.assertFalse(result["consume_message"])
                self.assertIsNone(result["recognized_command"])
                self.assertEqual(result["state"], initial["state"])
                self.assertEqual(result["descriptor_patch"], {})

    def test_malformed_and_unknown_state_fail_closed_without_mutating_input(self):
        state = copy.deepcopy(runtime.DEFAULT_STATE)
        state["extra"] = True
        with self.assertRaisesRegex(runtime.RuntimeProtocolError, "unsupported fields"):
            self.event("ordinary", state)
        self.assertIn("extra", state)

        invalid = copy.deepcopy(runtime.DEFAULT_STATE)
        invalid["quizme"]["record"] = True
        with self.assertRaisesRegex(runtime.RuntimeProtocolError, "requires"):
            self.event("ordinary", invalid)

    def test_cli_reads_stdin_and_returns_nonzero_for_invalid_input(self):
        valid = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=json.dumps({"schema_version": 1, "event": "user_message", "message": "--help"}),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertTrue(json.loads(valid.stdout)["consume_message"])

        invalid = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input="{}",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(invalid.returncode, 2)
        self.assertIn("runtime adapter error", invalid.stderr)


if __name__ == "__main__":
    unittest.main()
