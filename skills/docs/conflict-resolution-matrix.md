# Conflict Resolution Matrix

Use this matrix when two skills appear to own the same decision.

| Decision Type | Owning Skill | Supporting Skills |
|---|---|---|
| Process budget and skill-count cap | `process-budget-controller` | `token-reduction`, `skill-governance` |
| Governance mode and required gates | `skill-governance` | `governance-enforcement`, `regression-prevention` |
| Governance script execution | `governance-enforcement` | `scripted-command-execution` |
| Dependency sequencing | `order-of-operations` | `interdependent-change-planning` |
| Coupled surface mapping | `interdependent-change-planning` | `regression-prevention`, `doc-maintenance` |
| Root-cause verification | `diagnose-before-fix` | `scripted-command-execution`, `regression-prevention` |
| Regression risk classification | `regression-prevention` | `effective-testing-methods` |
| Test design and coverage mapping | `effective-testing-methods` | `regression-prevention` |
| Documentation update during implementation | `doc-maintenance` | `file-maintenance` |
| Periodic file freshness audit | `file-maintenance` | `doc-maintenance` |
| Rolling recent conversation memory | `conversation-retention-summary` | `artifact-budget-enforcement` |
| Long history retrieval index | `history-indexing` | `token-reduction` |
| Cache size and pruning limits | `artifact-budget-enforcement` | `history-indexing`, `conversation-retention-summary` |
| Usage evidence review | `skill-usage-review` | `thoroughly-rate-review`, `deprecation-management` |
| Deprecation lifecycle | `deprecation-management` | `file-maintenance`, `doc-maintenance` |
| Frontend spatial behavior | `ui-spatial-canvas` | `ui-design-skills`, `thoughtful-approach` |
| UX principle selection | `ui-design-skills` | `thoughtful-approach` |
| Quality scoring | `thoroughly-rate-review` | `semantic-policy-audit` |

## Tie-Breaking Rules
1. safety and data integrity override process budget
2. owner skill decides; supporting skills provide evidence
3. if two owners still conflict, choose the narrower owner
4. if uncertainty remains, record the assumption and proceed with the safer path
5. do not keep both skills active when one owner fully covers the decision
