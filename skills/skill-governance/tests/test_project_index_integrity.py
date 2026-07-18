from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import generate_governance_artifact as generator  # noqa: E402
import validate_skill_policy as policy  # noqa: E402


VALID_HEADER = (
    "# Project Index\n\n"
    "| Project ID | Language | Description (<=4 words) | "
    "Model Runs Tests/Build by Default (yes/no) | Last Confirmed UTC |\n"
    "|---|---|---|---|---|\n"
)


class TestProjectIndexIntegrity(unittest.TestCase):
    def write_index(self, root: Path, body: str) -> Path:
        path = root / "project-index.md"
        path.write_text(body, encoding="utf-8")
        return path

    def assert_invalid(self, content: str, message: str) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = self.write_index(Path(raw), content)
            with self.assertRaisesRegex(generator.ProjectIndexValidationError, message):
                generator.validate_project_index(path)

    def test_valid_write_and_parse_round_trip(self) -> None:
        entries = {
            "agent-command-center": {
                "language": "Markdown/Python",
                "description": "Agent command center",
                "model_default_test_build": "yes",
                "last_confirmed_utc": "2026-07-18T02:20:37.146744Z",
            },
            "rust-tool": {
                "language": "Rust",
                "description": "Fast local tool",
                "model_default_test_build": "no",
                "last_confirmed_utc": "2026-07-18T03:00:00+00:00",
            },
        }
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "project-index.md"
            generator.write_project_index(path, entries)

            self.assertEqual(generator.validate_project_index(path), entries)
            self.assertEqual(policy.validate_project_index_policy(path), [])

            generator.sync_project_index(
                path,
                SimpleNamespace(
                    project_id="rust-tool",
                    project_language="Rust 2",
                    project_description_max4="Updated local tool",
                    model_runs_test_build_default="yes",
                    created_at_utc="2026-07-18T04:00:00+00:00",
                ),
            )
            updated = generator.validate_project_index(path)
            self.assertEqual(updated["agent-command-center"], entries["agent-command-center"])
            self.assertEqual(
                updated["rust-tool"],
                {
                    "language": "Rust 2",
                    "description": "Updated local tool",
                    "model_default_test_build": "yes",
                    "last_confirmed_utc": "2026-07-18T04:00:00Z",
                },
            )

    def test_missing_or_malformed_preamble_fails_closed(self) -> None:
        cases = {
            "wrong heading": VALID_HEADER.replace("# Project Index", "# Projects", 1),
            "wrong header": VALID_HEADER.replace("Project ID", "Project", 1),
            "wrong separator": VALID_HEADER.replace("|---|---|---|---|---|", "| --- | --- | --- | --- | --- |", 1),
        }
        for name, content in cases.items():
            with self.subTest(name=name):
                self.assert_invalid(content, "exact (heading|table header|table separator)")

    def test_duplicate_project_ids_are_rejected(self) -> None:
        row = "| duplicate-id | Python | Duplicate project | yes | 2026-07-18T00:00:00Z |\n"
        self.assert_invalid(VALID_HEADER + row + row, "duplicates project ID")

    def test_invalid_utc_timestamps_are_rejected(self) -> None:
        timestamps = (
            "2026-02-30T00:00:00Z",
            "2026-07-18T00:00:00",
            "2026-07-18T01:00:00+01:00",
        )
        for timestamp in timestamps:
            with self.subTest(timestamp=timestamp):
                self.assert_invalid(
                    VALID_HEADER
                    + f"| test-project | Python | Test project | yes | {timestamp} |\n",
                    "valid timezone-aware UTC timestamp",
                )

    def test_description_over_four_words_is_rejected(self) -> None:
        self.assert_invalid(
            VALID_HEADER
            + "| test-project | Python | This description has five words | yes | 2026-07-18T00:00:00Z |\n",
            "maximum is 4",
        )

    def test_field_and_row_shape_errors_are_rejected(self) -> None:
        cases = {
            "invalid ID": "| Invalid-ID | Python | Test project | yes | 2026-07-18T00:00:00Z |\n",
            "empty language": "| test-project |  | Test project | yes | 2026-07-18T00:00:00Z |\n",
            "invalid flag": "| test-project | Python | Test project | true | 2026-07-18T00:00:00Z |\n",
            "six cells": "| test-project | Python | Test project | yes | extra | 2026-07-18T00:00:00Z |\n",
            "non-table": "This content must not be ignored.\n",
        }
        for name, row in cases.items():
            with self.subTest(name=name):
                self.assert_invalid(VALID_HEADER + row, ".+")

    def test_policy_validator_reports_project_index_errors(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = self.write_index(
                Path(raw),
                VALID_HEADER
                + "| bad-project | Python | Too many description words here | maybe | not-a-time |\n",
            )

            errors = policy.validate_project_index_policy(path)

            self.assertGreaterEqual(len(errors), 3)
            self.assertTrue(all(error.startswith("project index: ") for error in errors))

    def test_sync_rejects_malformed_index_without_clobbering_it(self) -> None:
        malformed = VALID_HEADER + "This content must not be ignored.\n"
        artifact = SimpleNamespace(
            project_id="test-project",
            project_language="Python",
            project_description_max4="Test project",
            model_runs_test_build_default="yes",
            created_at_utc="2026-07-18T00:00:00+00:00",
        )
        with tempfile.TemporaryDirectory() as raw:
            path = self.write_index(Path(raw), malformed)

            with self.assertRaisesRegex(SystemExit, "non-table content"):
                generator.sync_project_index(path, artifact)

            self.assertEqual(path.read_text(encoding="utf-8"), malformed)


if __name__ == "__main__":
    unittest.main()
