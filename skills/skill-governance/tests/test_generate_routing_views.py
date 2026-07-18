#!/usr/bin/env python3
"""Tests for catalog validation and deterministic generated routing views."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generate_routing_views.py"
SPEC = importlib.util.spec_from_file_location("generate_routing_views", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def skill(name: str, *, description: str | None = None) -> dict:
    return {
        "name": name,
        "status": "active",
        "role": "owner",
        "routing_mode": "automatic",
        "description": description or f"Use {name} for its owned decision.",
        "triggers": [f"{name} is explicitly required."],
        "exclusions": [f"{name} is irrelevant."],
        "routing": {
            "selection_strength": "required",
            "triggers": [{"actions_any": ["answer"]}],
            "exclusions": [],
        },
        "decision_domains": [f"{name}_domain"],
        "artifact_policy": {"durability": "none", "artifacts": []},
        "risk_level": "low",
        "relations": {
            "requires": [],
            "gates": [],
            "runs_after": [],
            "supports": [],
            "conflicts_with": [],
            "consumes": [],
            "superseded_by": [],
        },
    }


def catalog(skills: list[dict]) -> dict:
    return {
        "$schema": "./skill-catalog.schema.json",
        "schema_version": 2,
        "catalog_version": "2.0.0",
        "router_contract": "2.1",
        "components": ["core-policy", "task-router", "safety-kernel", "response-compositor"],
        "generated_views": [
            "skills/SKILL-MAP.md",
            "skills/docs/skill-index.md",
            "skills/docs/skill-decision-tree.md",
        ],
        "router_policy": {
            "selection_order": sorted(item["name"] for item in skills),
            "zero_skill_valid": True,
            "skill_budget": {
                "routine_target_median": 2,
                "routine_maximum": 5,
                "mandatory_safety_exempt": True,
            },
        },
        "routing_vocabulary": {
            "actions": ["answer"],
            "operations": ["read"],
            "effects": ["workspace_files"],
            "surfaces": ["response"],
            "domains": ["general"],
            "flags": ["material_uncertainty"],
        },
        "relation_types": {
            "requires": "hard",
            "gates": "veto",
            "runs_after": "order",
            "supports": "advisory",
            "conflicts_with": "exclusive",
            "consumes": "input",
            "superseded_by": "lifecycle",
        },
        "gate_ids": ["authorization"],
        "artifact_types": ["change_evidence"],
        "decision_domains": sorted(
            domain for item in skills for domain in item["decision_domains"]
        ),
        "skills": sorted(skills, key=lambda item: item["name"]),
    }


class RoutingViewTest(unittest.TestCase):
    def test_startup_declaration_policy_matches_repository_core_policy(self) -> None:
        catalog_path = Path(__file__).resolve().parents[2] / "skill-catalog.json"
        payload = json.loads(catalog_path.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["router_policy"]["startup_declaration"],
            {
                "required_when": [
                    "explicitly_requested",
                    "governed_or_audited_work_requiring_durable_routing_record",
                ],
                "otherwise": "omit",
            },
        )

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_fixture(self, payload: dict) -> Path:
        for entry in payload["skills"]:
            path = self.root / "skills" / entry["name"] / "SKILL.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                f"---\nname: {entry['name']}\ndescription: {entry['description']}\n---\n",
                encoding="utf-8",
            )
        path = self.root / "skills" / "skill-catalog.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_valid_catalog_and_write_then_check(self) -> None:
        payload = catalog([skill("alpha"), skill("beta")])
        path = self.write_fixture(payload)
        self.assertEqual(MODULE.run(self.root, path, False), 0)
        self.assertEqual(MODULE.run(self.root, path, True), 0)
        for relative in payload["generated_views"]:
            self.assertIn(MODULE.GENERATED_NOTICE, (self.root / relative).read_text())

    def test_catalog_schema_is_valid_draft_2020_12(self) -> None:
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("jsonschema is not installed")
        schema_path = Path(__file__).resolve().parents[2] / "skill-catalog.schema.json"
        Draft202012Validator.check_schema(json.loads(schema_path.read_text(encoding="utf-8")))

    def test_check_detects_drift(self) -> None:
        payload = catalog([skill("alpha")])
        path = self.write_fixture(payload)
        self.assertEqual(MODULE.run(self.root, path, False), 0)
        (self.root / payload["generated_views"][0]).write_text("stale", encoding="utf-8")
        self.assertEqual(MODULE.run(self.root, path, True), 1)

    def test_frontmatter_description_must_match(self) -> None:
        payload = catalog([skill("alpha")])
        path = self.write_fixture(payload)
        skill_path = self.root / "skills" / "alpha" / "SKILL.md"
        skill_path.write_text("---\nname: alpha\ndescription: drift\n---\n", encoding="utf-8")
        with self.assertRaisesRegex(MODULE.CatalogError, "description differs"):
            MODULE.validate_catalog(payload, self.root)

    def test_requires_cycle_fails(self) -> None:
        alpha, beta = skill("alpha"), skill("beta")
        alpha["relations"]["requires"] = ["beta"]
        beta["relations"]["requires"] = ["alpha"]
        payload = catalog([alpha, beta])
        self.write_fixture(payload)
        with self.assertRaisesRegex(MODULE.CatalogError, "requires graph cycle"):
            MODULE.validate_catalog(payload, self.root)

    def test_combined_requires_and_runs_after_cycle_fails(self) -> None:
        alpha, beta = skill("alpha"), skill("beta")
        alpha["relations"]["requires"] = ["beta"]
        beta["relations"]["runs_after"] = ["alpha"]
        payload = catalog([alpha, beta])
        self.write_fixture(payload)
        with self.assertRaisesRegex(MODULE.CatalogError, "combined requires/runs_after"):
            MODULE.validate_catalog(payload, self.root)

    def test_active_decision_domain_has_one_owner(self) -> None:
        alpha, beta = skill("alpha"), skill("beta")
        beta["decision_domains"] = list(alpha["decision_domains"])
        payload = catalog([alpha, beta])
        payload["decision_domains"] = list(alpha["decision_domains"])
        self.write_fixture(payload)
        with self.assertRaisesRegex(MODULE.CatalogError, "multiple active owners"):
            MODULE.validate_catalog(payload, self.root)

    def test_unknown_relation_target_fails(self) -> None:
        alpha = skill("alpha")
        alpha["relations"]["supports"] = ["missing"]
        payload = catalog([alpha])
        self.write_fixture(payload)
        with self.assertRaisesRegex(MODULE.CatalogError, "unknown targets"):
            MODULE.validate_catalog(payload, self.root)

    def test_conflicts_must_be_symmetric(self) -> None:
        alpha, beta = skill("alpha"), skill("beta")
        alpha["relations"]["conflicts_with"] = ["beta"]
        payload = catalog([alpha, beta])
        self.write_fixture(payload)
        with self.assertRaisesRegex(MODULE.CatalogError, "must be symmetric"):
            MODULE.validate_catalog(payload, self.root)

    def test_compatibility_chain_fails(self) -> None:
        alpha, beta, gamma = skill("alpha"), skill("beta"), skill("gamma")
        alpha["status"] = "deprecated"
        alpha["role"] = "compatibility"
        alpha["routing_mode"] = "nonselectable"
        alpha["routing"]["triggers"] = []
        alpha["decision_domains"] = []
        alpha["relations"]["superseded_by"] = ["beta"]
        beta["status"] = "deprecated"
        beta["role"] = "compatibility"
        beta["routing_mode"] = "nonselectable"
        beta["routing"]["triggers"] = []
        beta["decision_domains"] = []
        beta["relations"]["superseded_by"] = ["gamma"]
        payload = catalog([alpha, beta, gamma])
        payload["router_policy"]["selection_order"] = ["gamma"]
        payload["decision_domains"] = ["gamma_domain"]
        self.write_fixture(payload)
        with self.assertRaisesRegex(MODULE.CatalogError, "compatibility chains"):
            MODULE.validate_catalog(payload, self.root)

    def test_unknown_artifact_fails(self) -> None:
        alpha = skill("alpha")
        alpha["artifact_policy"]["artifacts"] = ["secret_prompt_cache"]
        payload = catalog([alpha])
        self.write_fixture(payload)
        with self.assertRaisesRegex(MODULE.CatalogError, "unknown artifact"):
            MODULE.validate_catalog(payload, self.root)

    def test_authorized_only_artifact_requires_explicit_authority_section(self) -> None:
        alpha = skill("alpha")
        alpha["artifact_policy"] = {
            "durability": "authorized_only",
            "artifacts": ["change_evidence"],
        }
        payload = catalog([alpha])
        self.write_fixture(payload)
        with self.assertRaisesRegex(MODULE.CatalogError, "Authority and Artifact Policy"):
            MODULE.validate_catalog(payload, self.root)

        skill_path = self.root / "skills" / "alpha" / "SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8")
            + "\n## Authority and Artifact Policy\n\nActivation grants no write authority.\n",
            encoding="utf-8",
        )
        MODULE.validate_catalog(payload, self.root)

    def test_automatic_and_explicit_routing_modes_are_enforced(self) -> None:
        alpha = skill("alpha")
        alpha["routing_mode"] = "explicit_only"
        payload = catalog([alpha])
        self.write_fixture(payload)
        with self.assertRaisesRegex(MODULE.CatalogError, "explicit_only but has automatic triggers"):
            MODULE.validate_catalog(payload, self.root)

        alpha["routing_mode"] = "automatic"
        alpha["routing"]["triggers"] = []
        payload = catalog([alpha])
        self.write_fixture(payload)
        with self.assertRaisesRegex(MODULE.CatalogError, "automatic but has no machine trigger"):
            MODULE.validate_catalog(payload, self.root)

    def test_selection_order_is_exactly_the_routable_set(self) -> None:
        payload = catalog([skill("alpha"), skill("beta")])
        payload["router_policy"]["selection_order"] = ["alpha"]
        self.write_fixture(payload)
        with self.assertRaisesRegex(MODULE.CatalogError, "every and only active"):
            MODULE.validate_catalog(payload, self.root)

    def test_safety_role_requires_required_safety_only_routing(self) -> None:
        alpha = skill("alpha")
        alpha["role"] = "safety"
        payload = catalog([alpha])
        self.write_fixture(payload)
        with self.assertRaisesRegex(MODULE.CatalogError, "must use safety_only"):
            MODULE.validate_catalog(payload, self.root)

        alpha["routing_mode"] = "safety_only"
        alpha["routing"]["selection_strength"] = "optional"
        payload = catalog([alpha])
        self.write_fixture(payload)
        with self.assertRaisesRegex(MODULE.CatalogError, "cannot be optional"):
            MODULE.validate_catalog(payload, self.root)

    def test_routing_clauses_use_known_unique_vocabulary(self) -> None:
        alpha = skill("alpha")
        alpha["routing"]["triggers"] = [{"actions_any": ["missing"]}]
        payload = catalog([alpha])
        self.write_fixture(payload)
        with self.assertRaisesRegex(MODULE.CatalogError, "unknown values"):
            MODULE.validate_catalog(payload, self.root)

        alpha["routing"]["triggers"] = [
            {"actions_any": ["answer"]},
            {"actions_any": ["answer"]},
        ]
        payload = catalog([alpha])
        self.write_fixture(payload)
        with self.assertRaisesRegex(MODULE.CatalogError, "duplicate clauses"):
            MODULE.validate_catalog(payload, self.root)

    def test_input_is_not_mutated(self) -> None:
        payload = catalog([skill("alpha")])
        expected = copy.deepcopy(payload)
        self.write_fixture(payload)
        MODULE.validate_catalog(payload, self.root)
        self.assertEqual(payload, expected)


if __name__ == "__main__":
    unittest.main()
