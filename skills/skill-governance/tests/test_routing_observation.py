import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "record_routing_observation.py"


class RoutingObservationTests(unittest.TestCase):
    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *args], text=True, capture_output=True, check=False
        )

    def test_records_only_allowed_operational_metadata_and_prunes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "observations.jsonl"
            for index in range(3):
                result = self.run_script(
                    "record", "--out", str(path), "--task-class", "implement",
                    "--checkpoint", "post_diff", "--selected-skills",
                    "regression-prevention,effective-testing-methods", "--validation-outcome", "pass",
                    "--corrections", str(index), "--max-records", "2",
                )
                self.assertEqual(result.returncode, 0, result.stderr)
            records = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertEqual(len(records), 2)
            self.assertEqual(records[-1]["corrections"], 2)
            forbidden = {"prompt", "source", "reasoning", "secret", "files"}
            self.assertFalse(forbidden.intersection(records[-1]))

    def test_summary_is_aggregate_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "observations.jsonl"
            recorded = self.run_script(
                "record", "--out", str(path), "--task-class", "review",
                "--checkpoint", "initial", "--validation-outcome", "not_run",
            )
            self.assertEqual(recorded.returncode, 0, recorded.stderr)
            summary = self.run_script("summary", "--out", str(path))
            self.assertEqual(summary.returncode, 0, summary.stderr)
            payload = json.loads(summary.stdout)
            self.assertEqual(payload["records"], 1)
            self.assertEqual(payload["task_classes"], {"review": 1})

    def test_rejects_negative_counts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            result = self.run_script(
                "record", "--out", str(Path(temp) / "observations.jsonl"),
                "--task-class", "answer", "--checkpoint", "initial",
                "--validation-outcome", "pass", "--retries", "-1",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-negative", result.stderr)

    def test_rejects_unknown_skill_names_and_oversized_retention(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = str(Path(temp) / "observations.jsonl")
            unknown = self.run_script(
                "record", "--out", path, "--task-class", "answer",
                "--checkpoint", "initial", "--validation-outcome", "pass",
                "--selected-skills", "invented-free-text-skill",
            )
            oversized = self.run_script(
                "record", "--out", path, "--task-class", "answer",
                "--checkpoint", "initial", "--validation-outcome", "pass",
                "--max-records", "101",
            )
            self.assertNotEqual(unknown.returncode, 0)
            self.assertIn("outside the catalog", unknown.stderr)
            self.assertNotEqual(oversized.returncode, 0)
            self.assertIn("between 1 and 100", oversized.stderr)

    def test_checkpoint_namespace_matches_task_router(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = str(Path(temp) / "observations.jsonl")
            accepted = self.run_script(
                "record", "--out", path, "--task-class", "operate",
                "--checkpoint", "pre_external_action", "--validation-outcome", "pass",
            )
            rejected = self.run_script(
                "record", "--out", path, "--task-class", "operate",
                "--checkpoint", "pre_external", "--validation-outcome", "pass",
            )
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
            self.assertNotEqual(rejected.returncode, 0)


if __name__ == "__main__":
    unittest.main()
