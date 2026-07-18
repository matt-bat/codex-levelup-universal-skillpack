import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = SKILL_ROOT / "scripts"
SCHEMA_ROOT = SKILL_ROOT / "schemas"
FIXTURE_PATH = SKILL_ROOT / "fixtures" / "routing-scenarios.json"
SCRIPT_PATH = SCRIPT_ROOT / "resolve_task_route.py"

sys.path.insert(0, str(SCRIPT_ROOT))
import resolve_task_route as router  # noqa: E402


def permission_set(**overrides: bool) -> dict[str, bool]:
    permissions = {operation: False for operation in router.OPERATIONS}
    permissions.update(overrides)
    return permissions


class TestTaskRouting(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.defaults = cls.fixture["descriptor_defaults"]
        cls.scenarios = {scenario["id"]: scenario for scenario in cls.fixture["scenarios"]}
        cls.results = {
            scenario_id: router.resolve_task_route(
                router._deep_merge(cls.defaults, scenario["descriptor"])
            )
            for scenario_id, scenario in cls.scenarios.items()
        }

    def gate_statuses(self, scenario_id: str) -> dict[str, str]:
        return {
            gate["id"]: gate["status"]
            for gate in self.results[scenario_id]["typed_gates"]
        }

    def excluded_routes(self, scenario_id: str) -> list[str]:
        return [
            route["route"] for route in self.results[scenario_id]["excluded_routes"]
        ]

    def veto_codes(self, scenario_id: str) -> list[str]:
        return [veto["code"] for veto in self.results[scenario_id]["vetoes"]]

    def must_surface_text(self, scenario_id: str) -> list[str]:
        return [item["text"] for item in self.results[scenario_id]["must_surface"]]

    def descriptor(self, scenario_id: str) -> dict:
        return router._deep_merge(
            self.defaults,
            self.scenarios[scenario_id]["descriptor"],
        )

    def resolve_with_catalog_mutation(self, descriptor: dict, mutate) -> dict:
        catalog = json.loads((SKILL_ROOT.parent / "skill-catalog.json").read_text(encoding="utf-8"))
        mutate(catalog)
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "skill-catalog.json"
            path.write_text(json.dumps(catalog), encoding="utf-8")
            return router.resolve_task_route(descriptor, catalog_path=path)

    def test_schemas_are_valid_draft_2020_12(self) -> None:
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("jsonschema is not installed")

        for schema_name in (
            "task-descriptor.schema.json",
            "routing-result.schema.json",
        ):
            with self.subTest(schema=schema_name):
                schema = json.loads((SCHEMA_ROOT / schema_name).read_text(encoding="utf-8"))
                Draft202012Validator.check_schema(schema)

    def test_standard_library_schema_fallback_rejects_malformed_descriptor(self) -> None:
        schema = json.loads(
            (SCHEMA_ROOT / "task-descriptor.schema.json").read_text(encoding="utf-8")
        )
        valid = router._deep_merge(
            self.defaults,
            self.scenarios["simple-answer"]["descriptor"],
        )
        self.assertEqual(router._fallback_schema_errors(valid, schema), [])
        malformed = copy.deepcopy(valid)
        malformed["action"]["operations"] = ["read", "read"]
        malformed["constraints"]["max_optional_skills"] = -1
        errors = router._fallback_schema_errors(malformed, schema)
        self.assertTrue(any("items must be unique" in error for error in errors))
        self.assertTrue(any("below 0" in error for error in errors))

    def test_all_25_scenarios_match_declared_expectations_and_schemas(self) -> None:
        evaluation = router.evaluate_fixture_file(FIXTURE_PATH)
        self.assertEqual(evaluation["scenario_count"], 25)
        self.assertEqual(evaluation["failed"], 0, evaluation["failures"])
        for scenario_id, result in self.results.items():
            with self.subTest(scenario=scenario_id):
                router.validate_routing_result(result)

    def test_simple_answer_and_tiny_typo_are_exactly_proportional(self) -> None:
        answer = self.results["simple-answer"]
        self.assertEqual(answer["selected_skills"], [])
        self.assertEqual(answer["decision"], "allow")
        self.assertEqual(answer["permissions"], permission_set(read=True))
        self.assertFalse(answer["artifact_allowance"]["allowed"])
        self.assertEqual(
            self.gate_statuses("simple-answer"),
            {
                "descriptor-consistency": "passed",
                "read-only-boundary": "passed",
                "authority-read": "passed",
                "material-uncertainty": "passed",
            },
        )

        typo = self.results["tiny-typo"]
        self.assertEqual(typo["selected_skills"], [])
        self.assertEqual(typo["permissions"], permission_set(read=True, write_files=True))
        self.assertEqual(self.excluded_routes("tiny-typo"), ["doc-maintenance"])
        self.assertEqual(
            self.must_surface_text("tiny-typo"),
            ["Change only the typo.", "Do not reformat the document."],
        )

    def test_diagnose_only_route_cannot_mutate(self) -> None:
        result = self.results["diagnose-only-cli"]
        self.assertEqual(
            result["selected_skills"],
            ["diagnose-before-fix", "scripted-command-execution"],
        )
        self.assertEqual(result["permissions"], permission_set(read=True, run_commands=True))
        self.assertFalse(result["artifact_allowance"]["allowed"])
        self.assertEqual(self.veto_codes("diagnose-only-cli"), [])

    def test_test_design_is_selected_only_for_explicit_test_changes(self) -> None:
        without_tests = self.results["cli-code-implementation"]
        with_tests = self.results["cli-code-with-test-design"]
        self.assertEqual(
            without_tests["selected_skills"],
            ["regression-prevention", "scripted-command-execution"],
        )
        self.assertEqual(
            self.excluded_routes("cli-code-implementation"),
            ["effective-testing-methods"],
        )
        self.assertEqual(
            with_tests["selected_skills"],
            [
                "regression-prevention",
                "effective-testing-methods",
                "scripted-command-execution",
            ],
        )
        self.assertEqual(self.gate_statuses("cli-code-with-test-design")["tests-passed"], "required")

    def test_qualitative_review_and_explicit_scoring_have_distinct_exact_routes(self) -> None:
        qualitative = self.results["qualitative-code-review"]
        scored = self.results["scored-code-review"]
        self.assertEqual(qualitative["selected_skills"], ["regression-prevention"])
        self.assertEqual(
            self.excluded_routes("qualitative-code-review"),
            [],
        )
        self.assertEqual(scored["selected_skills"], ["thoroughly-rate-review"])
        self.assertNotIn("regression-prevention", scored["selected_skills"])

    def test_generic_ui_excludes_spatial_and_explicit_spatial_includes_it(self) -> None:
        generic = self.results["generic-ui-implementation"]
        spatial = self.results["spatial-canvas-implementation"]
        self.assertEqual(
            generic["selected_skills"],
            [
                "ui-design-skills",
                "regression-prevention",
                "effective-testing-methods",
                "scripted-command-execution",
            ],
        )
        self.assertEqual(self.excluded_routes("generic-ui-implementation"), ["ui-spatial-canvas"])
        self.assertEqual(
            spatial["selected_skills"],
            [
                "ui-design-skills",
                "ui-spatial-canvas",
                "regression-prevention",
                "effective-testing-methods",
                "scripted-command-execution",
            ],
        )

    def test_auth_source_and_live_auth_operation_do_not_share_recovery_route(self) -> None:
        source = self.results["auth-source-change"]
        live = self.results["auth-live-operation"]
        self.assertEqual(
            source["selected_skills"],
            ["regression-prevention", "scripted-command-execution"],
        )
        self.assertEqual(
            self.excluded_routes("auth-source-change"),
            ["effective-testing-methods"],
        )
        self.assertEqual(
            live["selected_skills"],
            [
                "skill-governance",
                "regression-prevention",
                "scripted-command-execution",
            ],
        )
        self.assertEqual(live["permissions"], permission_set(read=True, run_commands=True, deploy=True))
        self.assertEqual(self.gate_statuses("auth-live-operation")["rollback-ready-deploy"], "passed")

    def test_source_migration_excludes_operational_recovery_but_apply_requires_it(self) -> None:
        source = self.results["migration-source-only"]
        apply_result = self.results["migration-apply"]
        self.assertEqual(
            source["selected_skills"],
            [
                "interdependent-change-planning",
                "regression-prevention",
                "effective-testing-methods",
                "scripted-command-execution",
            ],
        )
        self.assertNotIn("project-backup", source["selected_skills"])
        self.assertNotIn("restore-drill", source["selected_skills"])
        self.assertEqual(
            apply_result["selected_skills"],
            [
                "skill-governance",
                "regression-prevention",
                "project-backup",
                "restore-drill",
                "scripted-command-execution",
            ],
        )
        self.assertEqual(
            self.gate_statuses("migration-apply"),
            {
                "descriptor-consistency": "passed",
                "read-only-boundary": "passed",
                "authority-read": "passed",
                "authority-run_commands": "passed",
                "authority-migrate": "passed",
                "material-uncertainty": "passed",
                "pre-external-checkpoint": "passed",
                "rollback-ready-migrate": "passed",
                "backup-evidence": "passed",
                "restore-evidence": "passed",
            },
        )
        self.assertEqual(apply_result["permissions"], permission_set(read=True, run_commands=True, migrate=True))

    def test_strict_read_only_audit_has_exact_permissions_and_no_artifacts(self) -> None:
        result = self.results["strict-read-only-policy-audit"]
        self.assertEqual(
            result["selected_skills"],
            ["semantic-policy-audit"],
        )
        self.assertEqual(result["permissions"], permission_set(read=True, run_commands=True))
        self.assertFalse(result["artifact_allowance"]["allowed"])
        self.assertEqual(
            self.excluded_routes("strict-read-only-policy-audit"),
            ["scripted-command-execution"],
        )

    def test_ambiguous_auth_request_fails_closed_for_clarification(self) -> None:
        result = self.results["ambiguous-login-request"]
        self.assertEqual(result["decision"], "needs_clarification")
        self.assertEqual(result["selected_skills"], ["requirement-clarifier"])
        self.assertEqual(result["permissions"], permission_set(read=True))
        self.assertEqual(self.veto_codes("ambiguous-login-request"), ["critical_state_unresolved"])
        self.assertEqual(self.gate_statuses("ambiguous-login-request")["material-uncertainty"], "needs_resolution")
        self.assertIn(
            "It is unclear whether the request changes source code or live account state.",
            self.must_surface_text("ambiguous-login-request"),
        )

    def test_commit_without_push_preserves_exact_authority_boundary(self) -> None:
        result = self.results["multi-deliverable-commit-no-push"]
        self.assertEqual(result["decision"], "allow")
        self.assertEqual(
            result["permissions"],
            permission_set(read=True, run_commands=True, write_files=True, commit=True),
        )
        self.assertEqual(self.excluded_routes("multi-deliverable-commit-no-push"), [])
        self.assertNotIn("authority-push", self.gate_statuses("multi-deliverable-commit-no-push"))
        self.assertEqual(
            self.must_surface_text("multi-deliverable-commit-no-push"),
            ["Commit locally after validation.", "Do not push."],
        )

    def test_release_permission_depends_on_exact_commit_evidence(self) -> None:
        ready = self.results["release-ready"]
        missing = self.results["release-missing-exact-commit"]
        self.assertEqual(ready["decision"], "allow")
        self.assertEqual(
            ready["permissions"],
            permission_set(read=True, run_commands=True, write_files=True, publish=True),
        )
        self.assertEqual(self.gate_statuses("release-ready")["exact-commit-green"], "passed")
        self.assertEqual(missing["decision"], "blocked")
        self.assertFalse(missing["permissions"]["publish"])
        self.assertEqual(self.gate_statuses("release-missing-exact-commit")["exact-commit-green"], "blocked")
        self.assertEqual(self.veto_codes("release-missing-exact-commit"), ["evidence_not_passed"])

    def test_read_only_constraint_overrides_granted_write_authority(self) -> None:
        result = self.results["read-only-conflict"]
        self.assertEqual(result["decision"], "blocked")
        self.assertEqual(result["permissions"], permission_set(read=True))
        self.assertEqual(self.veto_codes("read-only-conflict"), ["read_only_conflict"])
        self.assertEqual(self.gate_statuses("read-only-conflict")["read-only-boundary"], "blocked")

    def test_quick_just_and_simple_words_do_not_change_routes(self) -> None:
        baseline = self.results["simple-answer"]
        fields = ("decision", "selected_skills", "permissions", "artifact_allowance", "vetoes")
        for scenario_id in (
            "quick-answer-paraphrase",
            "just-answer-paraphrase",
            "simple-answer-paraphrase",
        ):
            with self.subTest(scenario=scenario_id):
                for field in fields:
                    self.assertEqual(self.results[scenario_id][field], baseline[field])

    def test_zero_optional_budget_cannot_remove_mandatory_safety(self) -> None:
        result = self.results["migration-zero-optional-budget"]
        expected = [
            "skill-governance",
            "regression-prevention",
            "project-backup",
            "restore-drill",
            "scripted-command-execution",
        ]
        self.assertEqual(result["selected_skills"], expected)
        self.assertEqual(result["skill_budget"]["max_optional_skills"], 0)
        self.assertEqual(result["skill_budget"]["mandatory_skills"], expected)
        self.assertTrue(result["skill_budget"]["mandatory_safety_exempt"])

    def test_optional_budget_removes_omitted_supporter_ownership(self) -> None:
        descriptor = router._deep_merge(
            self.defaults,
            self.scenarios["generic-ui-implementation"]["descriptor"],
        )
        descriptor["task_id"] = "generic-ui-zero-optional"
        descriptor["action"]["product_judgment"] = True
        descriptor["constraints"]["max_optional_skills"] = 0
        result = router.resolve_task_route(descriptor)
        self.assertNotIn("thoughtful-approach", result["selected_skills"])
        self.assertNotIn("product_behavior", result["decision_domain_owners"])
        self.assertIn(
            "thoughtful-approach",
            [route["route"] for route in result["excluded_routes"]],
        )

    def test_mechanical_frontend_does_not_infer_product_or_ui_judgment(self) -> None:
        descriptor = self.descriptor("generic-ui-implementation")
        descriptor["task_id"] = "mechanical-frontend"
        descriptor["action"]["ui_quality_judgment"] = False
        result = router.resolve_task_route(descriptor)
        self.assertEqual(
            result["selected_skills"],
            [
                "regression-prevention",
                "effective-testing-methods",
                "scripted-command-execution",
            ],
        )
        self.assertNotIn("thoughtful-approach", result["selected_skills"])
        self.assertNotIn("ui-design-skills", result["selected_skills"])
        self.assertIn("ui-design-skills", self._excluded_names(result))

    def test_product_judgment_is_explicit_and_owns_catalog_domain(self) -> None:
        descriptor = self.descriptor("generic-ui-implementation")
        descriptor["task_id"] = "product-judgment"
        descriptor["action"]["ui_quality_judgment"] = False
        descriptor["action"]["product_judgment"] = True
        result = router.resolve_task_route(descriptor)
        self.assertIn("thoughtful-approach", result["selected_skills"])
        self.assertEqual(
            result["decision_domain_owners"]["product_behavior"],
            "thoughtful-approach",
        )

    def test_running_existing_tests_never_selects_test_design(self) -> None:
        descriptor = self.descriptor("diagnose-only-cli")
        descriptor["task_id"] = "run-existing-tests"
        descriptor["action"]["primary"] = "test"
        descriptor["action"]["test_intent"] = "run_existing"
        descriptor["surfaces"] = ["cli", "tests"]
        descriptor["domains"] = ["testing"]
        result = router.resolve_task_route(descriptor)
        self.assertEqual(result["selected_skills"], ["scripted-command-execution"])
        self.assertNotIn("effective-testing-methods", result["selected_skills"])

    def test_incidental_validation_does_not_select_execution_workflow(self) -> None:
        descriptor = self.descriptor("cli-code-implementation")
        descriptor["task_id"] = "incidental-validation"
        descriptor["action"]["execution_mode"] = "incidental_validation"
        descriptor["action"]["command_effect"] = "read_only"
        result = router.resolve_task_route(descriptor)
        self.assertNotIn("scripted-command-execution", result["selected_skills"])
        self.assertTrue(result["permissions"]["run_commands"])
        self.assertIn("scripted-command-execution", self._excluded_names(result))

    def test_documentation_owner_requires_explicit_sync_intent(self) -> None:
        descriptor = self.descriptor("tiny-typo")
        descriptor["task_id"] = "canonical-doc-sync"
        descriptor["action"]["documentation_sync"] = True
        result = router.resolve_task_route(descriptor)
        self.assertEqual(result["selected_skills"], ["doc-maintenance"])
        self.assertNotIn("doc-maintenance", self._excluded_names(result))

    def test_command_effect_must_match_operation_and_authority_surface(self) -> None:
        descriptor = self.descriptor("cli-code-implementation")
        descriptor["task_id"] = "mismatched-command-effect"
        descriptor["action"]["command_effect"] = "repository"
        result = router.resolve_task_route(descriptor)
        self.assertEqual(result["decision"], "blocked")
        self.assertFalse(result["permissions"]["run_commands"])
        self.assertIn("descriptor_conflict", [item["code"] for item in result["vetoes"]])

    def test_unknown_command_effect_blocks_strict_read_only_execution(self) -> None:
        descriptor = self.descriptor("strict-read-only-policy-audit")
        descriptor["task_id"] = "unknown-command-effect"
        descriptor["action"]["command_effect"] = "unknown"
        result = router.resolve_task_route(descriptor)
        self.assertEqual(result["decision"], "blocked")
        self.assertFalse(result["permissions"]["run_commands"])
        self.assertIn("command_effect_unknown", [item["code"] for item in result["vetoes"]])
        self.assertIn("read_only_command_effect", [item["code"] for item in result["vetoes"]])

    def test_adaptive_browser_and_deterministic_workflows_are_exclusive(self) -> None:
        descriptor = self.descriptor("diagnose-only-cli")
        descriptor["task_id"] = "adaptive-browser"
        descriptor["action"]["primary"] = "operate"
        descriptor["action"]["execution_mode"] = "adaptive_browser"
        descriptor["surfaces"] = ["browser"]
        descriptor["domains"] = ["operations"]
        result = router.resolve_task_route(descriptor)
        self.assertEqual(result["selected_skills"], ["pseudo-agentic-automation"])
        self.assertNotIn("scripted-command-execution", result["selected_skills"])

    def test_deploy_requires_rollback_but_not_untyped_recovery_controls(self) -> None:
        result = self.results["auth-live-operation"]
        self.assertIn("skill-governance", result["selected_skills"])
        self.assertNotIn("project-backup", result["selected_skills"])
        self.assertNotIn("restore-drill", result["selected_skills"])
        self.assertEqual(self.gate_statuses("auth-live-operation")["rollback-ready-deploy"], "passed")
        self.assertNotIn("backup-evidence", self.gate_statuses("auth-live-operation"))

    def test_recovery_controls_always_emit_evidence_gates_and_fail_closed(self) -> None:
        descriptor = self.descriptor("migration-apply")
        descriptor["task_id"] = "migration-missing-recovery-evidence"
        descriptor["evidence"]["backup"] = "pending"
        descriptor["evidence"]["restore"] = "unknown"
        result = router.resolve_task_route(descriptor)
        statuses = {gate["id"]: gate["status"] for gate in result["typed_gates"]}
        self.assertEqual(result["decision"], "blocked")
        self.assertEqual(statuses["backup-evidence"], "blocked")
        self.assertEqual(statuses["restore-evidence"], "blocked")
        self.assertFalse(result["permissions"]["migrate"])
        self.assertFalse(result["permissions"]["run_commands"])

    def test_unknown_recovery_risk_fails_closed_before_external_action(self) -> None:
        descriptor = self.descriptor("auth-live-operation")
        descriptor["task_id"] = "unknown-recovery"
        descriptor["mutation"]["data_loss_risk"] = "unknown"
        descriptor["mutation"]["recovery_requirement"] = "unknown"
        result = router.resolve_task_route(descriptor)
        self.assertEqual(result["decision"], "needs_clarification")
        self.assertFalse(result["permissions"]["deploy"])
        self.assertIn("requirement-clarifier", result["selected_skills"])
        self.assertIn("recovery_state_unknown", [item["code"] for item in result["vetoes"]])

    def test_governance_enforcement_requires_typed_tooling_or_release_flag(self) -> None:
        self.assertNotIn("governance-enforcement", self.results["auth-live-operation"]["selected_skills"])
        self.assertIn("governance-enforcement", self.results["release-ready"]["selected_skills"])

    def test_ordering_owner_is_selected_only_for_real_sequencing(self) -> None:
        descriptor = self.descriptor("cli-code-implementation")
        descriptor["task_id"] = "sequenced-workflow"
        descriptor["action"]["sequencing_required"] = True
        result = router.resolve_task_route(descriptor)
        self.assertIn("order-of-operations", result["selected_skills"])
        self.assertLess(
            result["selected_skills"].index("order-of-operations"),
            result["selected_skills"].index("scripted-command-execution"),
        )

    def test_catalog_trigger_and_exclusion_mutations_change_runtime_route(self) -> None:
        descriptor = self.descriptor("diagnose-only-cli")

        def change_trigger(catalog):
            self._skill(catalog, "diagnose-before-fix")["routing"]["triggers"] = [
                {"actions_any": ["score"]}
            ]

        trigger_result = self.resolve_with_catalog_mutation(descriptor, change_trigger)
        self.assertNotIn("diagnose-before-fix", trigger_result["selected_skills"])

        implementation = self.descriptor("cli-code-implementation")

        def add_exclusion(catalog):
            self._skill(catalog, "regression-prevention")["routing"]["exclusions"] = [
                {"flags_any": ["regression_risk"]}
            ]

        exclusion_result = self.resolve_with_catalog_mutation(implementation, add_exclusion)
        self.assertNotIn("regression-prevention", exclusion_result["selected_skills"])

    def test_catalog_requires_supports_and_runs_after_have_distinct_semantics(self) -> None:
        descriptor = self.descriptor("diagnose-only-cli")

        def mutate(catalog):
            diagnose = self._skill(catalog, "diagnose-before-fix")
            diagnose["relations"]["requires"] = ["requirement-clarifier"]
            diagnose["relations"]["supports"] = ["thoughtful-approach"]
            scripted = self._skill(catalog, "scripted-command-execution")
            scripted["relations"]["runs_after"].append("diagnose-before-fix")
            order = catalog["router_policy"]["selection_order"]
            order.remove("scripted-command-execution")
            order.insert(0, "scripted-command-execution")

        result = self.resolve_with_catalog_mutation(descriptor, mutate)
        self.assertIn("requirement-clarifier", result["selected_skills"])
        self.assertNotIn("thoughtful-approach", result["selected_skills"])
        self.assertLess(
            result["selected_skills"].index("diagnose-before-fix"),
            result["selected_skills"].index("scripted-command-execution"),
        )

    def test_catalog_conflicts_block_and_status_controls_selectability(self) -> None:
        descriptor = self.descriptor("diagnose-only-cli")

        def conflict(catalog):
            self._skill(catalog, "diagnose-before-fix")["relations"]["conflicts_with"] = [
                "scripted-command-execution"
            ]
            self._skill(catalog, "scripted-command-execution")["relations"]["conflicts_with"] = [
                "diagnose-before-fix",
                "pseudo-agentic-automation",
            ]

        conflicted = self.resolve_with_catalog_mutation(descriptor, conflict)
        self.assertEqual(conflicted["decision"], "blocked")
        self.assertIn("skill_conflict", [item["code"] for item in conflicted["vetoes"]])

        def deprecate(catalog):
            skill = self._skill(catalog, "diagnose-before-fix")
            skill["status"] = "deprecated"
            skill["role"] = "compatibility"
            skill["routing_mode"] = "nonselectable"
            skill["routing"] = {"selection_strength": "optional", "triggers": [], "exclusions": []}
            skill["relations"]["superseded_by"] = ["requirement-clarifier"]
            catalog["router_policy"]["selection_order"].remove("diagnose-before-fix")

        deprecated = self.resolve_with_catalog_mutation(descriptor, deprecate)
        self.assertNotIn("diagnose-before-fix", deprecated["selected_skills"])

    def test_runtime_output_stays_inside_catalog_namespaces(self) -> None:
        catalog = router.load_catalog_contract()
        for result in self.results.values():
            self.assertTrue(set(result["selected_skills"]).issubset(catalog.active_skills))
            self.assertTrue(
                {gate["policy_gate_id"] for gate in result["typed_gates"]}.issubset(catalog.gate_ids)
            )
            self.assertTrue(
                set(result["artifact_allowance"]["kinds"]).issubset(catalog.artifact_types)
            )
        operation = self.results["migration-apply"]["artifact_allowance"]
        self.assertNotIn("operation_evidence", operation["kinds"])

    @staticmethod
    def _skill(catalog: dict, name: str) -> dict:
        return next(skill for skill in catalog["skills"] if skill["name"] == name)

    @staticmethod
    def _excluded_names(result: dict) -> list[str]:
        return [item["route"] for item in result["excluded_routes"]]

    def test_unknown_external_message_authority_fails_closed(self) -> None:
        result = self.results["external-message-authority-unknown"]
        self.assertEqual(result["decision"], "needs_clarification")
        self.assertEqual(result["permissions"], permission_set(read=True))
        self.assertEqual(self.veto_codes("external-message-authority-unknown"), ["authority_unknown"])
        self.assertEqual(self.gate_statuses("external-message-authority-unknown")["authority-message"], "needs_resolution")

    def test_descriptor_conflicts_block_mutation_even_with_authority(self) -> None:
        descriptor = router._deep_merge(
            self.defaults,
            {
                "task_id": "conflicting-state",
                "action": {
                    "primary": "edit",
                    "operations": ["read", "write_files"],
                },
                "mutation": {"level": "none"},
                "effects": ["workspace_files"],
                "surfaces": ["source"],
                "domains": ["code"],
                "authority": {"write_files": "granted"},
                "constraints": {"read_only": False},
            },
        )
        result = router.resolve_task_route(descriptor)
        self.assertEqual(result["decision"], "blocked")
        self.assertFalse(result["permissions"]["write_files"])
        self.assertEqual([veto["code"] for veto in result["vetoes"]], ["descriptor_conflict"])
        self.assertEqual(
            {gate["id"]: gate["status"] for gate in result["typed_gates"]}[
                "descriptor-consistency"
            ],
            "blocked",
        )

    def test_routine_scenarios_never_exceed_five_selected_skills(self) -> None:
        routine = (
            "simple-answer",
            "tiny-typo",
            "diagnose-only-cli",
            "cli-code-implementation",
            "cli-code-with-test-design",
            "qualitative-code-review",
            "scored-code-review",
            "generic-ui-implementation",
            "auth-source-change",
            "migration-source-only",
            "strict-read-only-policy-audit",
            "multi-deliverable-commit-no-push",
        )
        for scenario_id in routine:
            with self.subTest(scenario=scenario_id):
                self.assertLessEqual(len(self.results[scenario_id]["selected_skills"]), 5)

    def test_fixture_cli_succeeds(self) -> None:
        completed = subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--fixtures",
                str(FIXTURE_PATH),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["passed"], 25)
        self.assertEqual(payload["failed"], 0)


if __name__ == "__main__":
    unittest.main()
