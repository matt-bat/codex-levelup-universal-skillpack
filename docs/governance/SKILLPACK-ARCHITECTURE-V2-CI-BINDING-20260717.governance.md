# Governance Artifact: SKILLPACK-ARCHITECTURE-V2-CI-BINDING-20260717

- `schema_version`: 2
- `created_at_utc`: 2026-07-18T02:20:37.146744+00:00
- `project_id`: agent-command-center
- `profile`: internal
- `project_language`: Markdown/Python
- `project_description_max4`: Agent command center
- `model_runs_test_build_default`: yes
- `execution_scope`: local_only
- `deployment_requested`: false
- `execution_skill`: scripted-command-execution
- `quizme_mode`: off
- `quizme_multiple_choice`: false
- `quizme_one_at_a_time`: false
- `quizme_confirm`: false
- `quizme_record`: false
- `selected_mode`: standard
- `total_score`: 6
- `recommendation`: go

## Scores
- `data_impact`: 0
- `business_impact`: 2
- `change_complexity`: 2
- `dependency_uncertainty`: 1
- `recoverability`: 1

## Critical Overrides
- none

## Required Gates
- [x] `scripted-command-execution` (status: pass)
  - evidence: first normal push and post-push ref verification passed; follow-up remains non-force and requires another exact-head check
  - waiver_reason:
- [x] `regression-prevention` (status: pass)
  - evidence: 103 unit tests, including the new multi-plan rejection regression, plus 25 scenarios and 31 skill checks passed
  - waiver_reason:
- [x] `doc-maintenance` (status: pass)
  - evidence: lifecycle, enforcement, walkthrough, changelog, and field notes synchronized; 102 Markdown files and 207 links passed
  - waiver_reason:

## Startup Declaration
### Skills In Use
- `skill-governance`
- `order-of-operations`
- `user-instructions-tracker`
- `doc-maintenance`
- `scripted-command-execution`
- `regression-prevention`
- `governance-enforcement`
### Skill Selection Rationale
Governance and ordering constrain the CI remediation and follow-up push; documentation and field evidence record the discovered invariant; the tracker gate excludes transient authorization; regression and enforcement prove the existing fail-closed behavior.
### Skill Execution Order
- `skill-governance`
- `order-of-operations`
- `user-instructions-tracker`
- `doc-maintenance`
- `scripted-command-execution`
- `regression-prevention`
- `governance-enforcement`

## Evidence Requirements
- [x] mode + score: standard mode, total score 6
- [x] impact map: governance lifecycle documentation, enforcement guidance, regression evidence, field notes, changelog, and CI status
- [x] validation scope by layer: targeted enforcement test, complete unit suite, scenarios, skill format, policy, catalog, generated views, schema, YAML, links, and diff hygiene
- [x] residual risks: the follow-up GitHub Actions result is observable only after push; no branch-protection setting was inspected or changed

## Break Glass
- enabled: false

## Notes
Follow-up to GitHub Actions run 29626703980. The change documents and regression-tests the rule that every version 2 plan changed in one diff must bind the same exact manifest. User authorization remains limited to a normal non-force push to origin/main; no tag, hosted release, deployment, or remote-settings change is authorized.

## Change Binding
- `base_sha`: 09345b5a2dd0bc7e46c67f36238cb1b4224035b8
- `manifest_sha256`: e590e16b224d5a2b66d679bf7f240d3dba7ce5435c9b80240678f59785ac6eff
- `manifest`:
  - `M` `docs/project-index.md` (`sha256`: f28746c277247d1110947b30d823a56c5631dc75b10a5377b1a1ec845f61b417)
  - `M` `skills/CHANGELOG.md` (`sha256`: e5007d0f706b0366a0da68a65b2fcddd075c68016bde79348b75e96bf09831a3)
  - `M` `skills/docs/field-notes.md` (`sha256`: a22953e1e5cc921ea442722eb71d29ebb1e77c5f3310f49e0d1b1a6e8cbe7ba7)
  - `M` `skills/docs/governance-walkthrough.md` (`sha256`: 9fd4f198cdb09c1174270a2002fd74b87eb2f11627439a6353ef87d4617259ed)
  - `M` `skills/governance-enforcement/SKILL.md` (`sha256`: 01e7fcb9be07ba4e97bacb1234598d67ba2c9d2106ce51f7f3560db6b784c9c4)
  - `M` `skills/skill-governance/references/governance-artifacts.md` (`sha256`: df859ceadb82c9ad86ab3760325d681b9849334c8f74e2f08456218f298d2d0f)
  - `M` `skills/skill-governance/tests/test_governance_integrity.py` (`sha256`: 0a5c3de958c58a2f7dd7f6b778e2931430a86c3df634a8c0be83ab7ff21baddd)
