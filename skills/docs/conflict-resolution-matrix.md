# Conflict Resolution Matrix

[Documentation home](./README.md) · [Routing architecture](./routing-architecture-v2.md) · [Decision tree](./skill-decision-tree.md)

Use this matrix when two skills appear to own the same decision. The goal is to choose one accountable owner, not to stack every related skill until the workflow becomes noisy.

| Decision Type | Catalog Domain or Policy Key | Owning Skill or Component | Supporting Skills |
|---|---|---|---|
| Process budget and skill-count cap | `router_policy.skill_budget` | task router | `token-reduction` only when output/context compression is independently triggered |
| Unresolved ambiguity and conflicts | `assumption_resolution` | `eliminate-assumptions` | `requirement-clarifier`, `quizme-mode` |
| Advanced source-grounded research | `research_evidence` | `advanced-r-and-d` | implementation or domain owner consuming the evidence |
| Fresh-context history boundary | `history_context_boundary` | `clean-slate` | `requirement-clarifier` |
| Persistent pre-execution clarification gate | `interactive_clarification` | `quizme-mode` | `requirement-clarifier`, `skill-governance` |
| Governance mode and required gates | `governance_decision` | `skill-governance` | `governance-enforcement`, `regression-prevention` |
| Governance script execution | `governance_enforcement` | `governance-enforcement` | `scripted-command-execution` |
| Dependency sequencing | `execution_order` | `order-of-operations` | `interdependent-change-planning` |
| Coupled surface mapping | `change_coherence` | `interdependent-change-planning` | `regression-prevention`, `doc-maintenance` |
| Root-cause verification | `diagnosis` | `diagnose-before-fix` | `scripted-command-execution`, `regression-prevention` |
| Approach continuation or pivot | `approach_reassessment` | `agent-humility` | `diagnose-before-fix`, `advanced-r-and-d`, `thoughtful-approach` |
| Regression risk classification | `implementation_quality` | `regression-prevention` | `effective-testing-methods` |
| Qualitative code review | `qualitative_code_review` | `regression-prevention` | `thoroughly-rate-review` when formal scoring is requested |
| Test design and coverage mapping | `test_design` | `effective-testing-methods` | `regression-prevention` |
| Documentation update during implementation | `documentation_accuracy` | `doc-maintenance` | `file-maintenance` |
| Periodic file freshness audit | `file_hygiene` | `file-maintenance` | `doc-maintenance` |
| Rolling recent conversation memory | `conversation_retention` | `conversation-retention-summary` | `artifact-budget-enforcement` |
| Long history retrieval index | `history_retrieval` | `history-indexing` | `token-reduction` |
| Cache size and pruning limits | `artifact_retention` | `artifact-budget-enforcement` | `history-indexing`, `conversation-retention-summary` |
| Usage evidence review | `routing_quality_review` | `skill-usage-review` | `thoroughly-rate-review`, `deprecation-management` |
| Deprecation lifecycle | `lifecycle` | `deprecation-management` | `file-maintenance`, `doc-maintenance` |
| Frontend spatial behavior | `spatial_canvas_system` | `ui-spatial-canvas` | `ui-design-skills`, `thoughtful-approach` |
| UX principle selection | `general_ui_quality` | `ui-design-skills` | `thoughtful-approach` |
| Advanced SVG composition and quality | `vector_graphics_quality` | `advanced-svg` | `ui-design-skills`, `advanced-r-and-d` |
| Quality scoring | `quality_scoring` | `thoroughly-rate-review` | `semantic-policy-audit` |

## Tie-Breaking Rules
1. active `quizme-mode` clarification completes before substantive execution
2. safety and data integrity override the optional-skill budget
3. the owner skill decides; `supports` relationships provide evidence without activating another skill
4. if two owners still conflict, choose the narrower decision domain
5. any unresolved ambiguity or conflict activates `eliminate-assumptions` and requires a user decision before substantive execution
6. do not keep both skills active when one owner fully covers the decision

If you are unsure, ask what artifact or decision the task really needs. That usually reveals the right owner.
