from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "skills" / "skill-governance" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import validate_skill_policy as policy  # noqa: E402


CATALOG = ROOT / "skills" / "skill-catalog.json"
MATRIX = ROOT / "skills" / "docs" / "conflict-resolution-matrix.md"


class TestConflictMatrixIntegrity(unittest.TestCase):
    def validate_text(self, content: str) -> list[str]:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "matrix.md"
            path.write_text(content, encoding="utf-8")
            return policy.validate_conflict_resolution_matrix(path, CATALOG)

    def test_current_matrix_uses_typed_catalog_owners(self) -> None:
        self.assertEqual(policy.validate_conflict_resolution_matrix(MATRIX, CATALOG), [])

    def test_unknown_domain_label_is_rejected(self) -> None:
        content = MATRIX.read_text(encoding="utf-8").replace(
            "`governance_decision`", "`governance_decison`", 1
        )
        errors = self.validate_text(content)
        self.assertTrue(any("unknown domain or policy key" in error for error in errors), errors)

    def test_mismatched_domain_owner_is_rejected(self) -> None:
        content = MATRIX.read_text(encoding="utf-8").replace(
            "| `governance_decision` | `skill-governance` |",
            "| `governance_decision` | `regression-prevention` |",
            1,
        )
        errors = self.validate_text(content)
        self.assertTrue(any("owner must be `skill-governance`" in error for error in errors), errors)

    def test_duplicate_domain_label_is_rejected(self) -> None:
        content = MATRIX.read_text(encoding="utf-8").replace(
            "`qualitative_code_review`", "`implementation_quality`", 1
        )
        errors = self.validate_text(content)
        self.assertTrue(any("duplicate domain" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
