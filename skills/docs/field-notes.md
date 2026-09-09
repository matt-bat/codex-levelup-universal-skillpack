# Field Notes

[Documentation home](./README.md) · [Maturity model](./maturity-model.md) · [Pruning policy](./pruning-policy.md)

Use this file to capture real usage evidence that should influence future changes.

## Purpose
Field notes keep the skillpack honest. They record where the process helped, where it slowed work, and where users corrected the agent.

That matters because the pack should improve from actual friction. A skill that looks useful in theory can still be too heavy, too vague, or too close to another skill in real tasks.

## Entry Template
```md
## FIELD-YYYYMMDD-##
- Date:
- Task:
- Install profile:
- Skills selected:
- Skills skipped:
- What helped:
- What slowed work:
- User corrections:
- Validation run:
- Follow-up candidate:
```

Keep entries short. The goal is a useful pattern over time, not a transcript.

## Review Cadence
1. review field notes before major skillpack releases
2. summarize repeated friction in `skill-usage-review`
3. convert repeated issues into docs, validator changes, or pruning decisions
4. do not add a new skill from a single weak signal

## Current Notes

## FIELD-20260717-01
- Date: 2026-07-17
- Task: Three-pass review followed by the local-only version 2 skillpack architecture implementation.
- Install profile: Internal, governed, local-only.
- Skills selected: `internal-lang`, `hyperfocus-discovery`, `token-reduction`, `skill-governance`, `project-backup`, `restore-drill`, `semantic-policy-audit`, `interdependent-change-planning`, `order-of-operations`, `scripted-command-execution`, `regression-prevention`, `governance-enforcement`, `deprecation-management`, `doc-maintenance`, and `user-instructions-tracker`.
- Skills skipped: Deployment, browser automation, user-interface design, release publication, and remote repository administration skills were outside the authorized scope.
- What helped: Typed task effects, catalog-owned routing clauses, adversarial route fixtures, working-tree binding, and separate semantic and mechanical validation exposed policy drift that prose-only checks had missed.
- What slowed work: Universal defaults created unnecessary startup overhead; duplicated routing rules drifted; version 1 artifacts could not prove which working tree they described; and command, testing, recovery, and interface triggers were initially too broad.
- User corrections: The user required three additional review passes, one final pass, maximum-effort implementation, and continued work through exhaustive validation.
- Validation run: 31 skill quick-validations, 101 governance unit tests, 25 routing scenarios, policy and ordering checks, 4 schema checks, 6 YAML parses, 9 script compilations, workflow parity, and 207 relative Markdown links passed locally.
- Follow-up candidate: Evaluate routing observations after at least 30 representative tasks or two releases; verify exact-head attestation and remote branch-protection behavior only in an explicitly authorized release workflow.

## FIELD-20260717-02
- Date: 2026-07-17
- Task: Commit and normally push routing architecture version 2 to `origin/main` with complete documentation and governance metadata.
- Install profile: Internal, governed, external-reversible Git operation.
- Skills selected: `skill-governance`, `order-of-operations`, `scripted-command-execution`, `regression-prevention`, `governance-enforcement`, `doc-maintenance`, and the `user-instructions-tracker` recordability gate.
- Skills skipped: Force push, tag creation, hosted release publication, deployment, and remote-settings administration remained outside scope.
- What helped: Target identity checks, zero-divergence verification, a metadata-rich commit, content-bound plans, and exact-head attestation proved the local candidate and remote target precisely.
- What slowed work: The first commit introduced two version 2 plans from different task phases. The final push plan bound correctly, but main-push enforcement correctly rejected the earlier changed snapshot because every changed plan must bind the same diff.
- User corrections: The user explicitly authorized a Git push with full metadata and documentation updates.
- Validation run: 103 unit tests passed after adding a regression case for the multi-plan failure. GitHub Actions run `29626703980` supplied the real-world failing evidence that drove the documentation and test update.
- Follow-up candidate: Keep one exact binding across every version 2 plan changed in a commit; commit distinct phase snapshots separately or leave intermediate plans out of the final diff.

## FIELD-20260718-03
- Date: 2026-07-18
- Task: Complete the first protected-main push, preserve full commit metadata, and verify the required governance check.
- Install profile: Internal, governed, externally reversible Git and repository-policy operations.
- Skills selected: `skill-governance`, `order-of-operations`, `scripted-command-execution`, `regression-prevention`, `semantic-policy-audit`, `governance-enforcement`, `doc-maintenance`, and `user-instructions-tracker`.
- Skills skipped: Tagging, hosted release publication, deployment, migration, backup, and restore controls were outside the typed effects and authority.
- What helped: Exact remote identity, branch-protection readback, feature-branch isolation, operation-specific authority, and required-check evidence kept push, remote configuration, and release permissions separate.
- What slowed work: A path-filtered pull-request workflow could leave a required `governance` check permanently absent on an otherwise valid non-governed pull request. Remote policy was also documented as a dated observation rather than an executable desired state.
- User corrections: The user required continued work, Git updates with full metadata, and complete documentation synchronization.
- Validation run: Commits `09345b5a2dd0bc7e46c67f36238cb1b4224035b8` and `accd30d4130b82bf004dc4f1fab73f9242280f12` reached `main`; required governance run `29626961080` passed; branch-protection API readback confirmed strict check app `15368`, administrator enforcement, and blocked force pushes and deletion.
- Follow-up candidate: Keep the required job unconditional for every pull request targeting `main`, and compare mutable remote state with a closed desired-state contract before relying on it.

## FIELD-20260718-04
- Date: 2026-07-18
- Task: Independently forward-test and harden router contract 2.1, governance schema v3, documentation, and protected-remote verification.
- Install profile: Internal, governed, cross-cutting policy and tooling change.
- Skills selected: `skill-governance`, `skill-usage-review`, `semantic-policy-audit`, `interdependent-change-planning`, `order-of-operations`, `scripted-command-execution`, `diagnose-before-fix`, `regression-prevention`, `effective-testing-methods`, `governance-enforcement`, `file-maintenance`, `doc-maintenance`, and `user-instructions-tracker`.
- Skills skipped: Browser automation, user-interface work, deployment, migration, deletion, tagging, and release publication were not part of the authorized effects.
- What helped: Independent failure-path scenarios, executable closed schemas, exact-head catalog checks, immutable commit-range evidence, typed artifact digests, and live desired-state comparison exposed gaps that happy-path validation missed.
- What slowed work: Early drafts conflated artifact creation permission with artifact existence, accepted permissive fixture expectations, left four relation-gate labels non-executable, allowed malformed project-index rows to be skipped, and lacked a machine-verifiable remote desired state. Exact-head and hosted checks then exposed a canonical-Markdown trailing blank line plus a platform-specific digest captured from an end-of-line-transformed historical artifact.
- User corrections: The user repeatedly required maximum effort, no shortcuts, continued work, full metadata, and documentation updates.
- Validation run: 163 governance tests and all 26 routing scenarios passed after adding failure-path and byte-stable-fixture coverage; the policy validator, generated-view check, exact-head enforcement, and live read-only branch-protection verification also passed.
- Follow-up candidate: Accumulate at least 30 representative routed tasks or two releases before retiring compatibility behavior; reverify mutable remote state at every external-action checkpoint.

## FIELD-20260816-05
- Date: 2026-08-16
- Task: Post-expansion usage review and operational hardening of the five advanced-skill additions.
- Install profile: Internal, governed, cross-cutting policy and tooling change.
- Skills selected: `advanced-r-and-d`, `skill-usage-review`, `skill-governance`, `governance-enforcement`, `interdependent-change-planning`, `regression-prevention`, `effective-testing-methods`, `scripted-command-execution`, and `doc-maintenance`.
- Skills skipped: Deployment, publication, deletion, migration, backup, restore, and remote-configuration controls were outside the requested effect.
- Evidence reviewed: 10 committed governance records, the canonical catalog, the 26 routing scenarios, the new-skill contract tests, adapters, known limitations, and the prior 92/100 rubric review.
- What helped: The five additions own distinct domains—research evidence, vector quality, help discovery, assumption resolution, and history boundaries—so no merge candidate was found. Typed routing and exact-command tests kept automatic and explicit activation separate.
- What slowed work: The one-time hint and conversation modes had prose but no executable host state machine; SVG validation did not render pixels; and five skills had been added since the previous recorded usage review.
- User corrections: The user requested that the pack close every identified scoring gap and reach the rubric's perfect-score standard.
- Validation run: Added host lifecycle/command conformance, multi-size librsvg/Chromium rendering, blank-output detection, pixel comparison, and mandatory CI coverage. Final exact-head results belong in the matching governance record rather than this field note.
- Disposition: Retain all five additions. Treat the controlled-growth review threshold as satisfied for this expansion, add no further skill solely from this task, and continue collecting representative live usage before lifecycle promotion or pruning.
- Follow-up candidate: Compare bounded routing observations after 30 representative tasks or two releases; do not mistake synthetic conformance scenarios for live adoption evidence.

## FIELD-20260816-06
- Date: 2026-08-16
- Task: Add a bounded workflow for abandoning disproven approaches without losing the user's goal or expanding authority.
- Install profile: Internal, governed, cross-cutting routing and policy change.
- Skills selected: `skill-creator`, `advanced-r-and-d`, `interdependent-change-planning`, `skill-governance`, `governance-enforcement`, `regression-prevention`, `effective-testing-methods`, `doc-maintenance`, and `scripted-command-execution`.
- Skills skipped: Deployment, publication, deletion, migration, backup, restore, and remote-configuration controls were outside the requested effect.
- Evidence reviewed: User reports of repeated agent path attachment; peer-reviewed work on escalation, intellectual humility, failure learning, open-minded thinking, and analogical transfer; and primary LLM self-correction evaluations emphasizing reliable external feedback.
- What helped: A distinct `approach_reassessment` decision domain separates goal preservation and method selection from root-cause diagnosis, requirement clarification, product judgment, and implementation-quality ownership.
- What slowed work: A broad “be humble” instruction would be subjective, over-trigger on routine errors, and invite token-heavy introspection without improving correctness.
- User corrections: The user required free-thinking, openness to nontraditional connections, faster satisfactory outcomes, reduced token use, full integration, and a GitHub push.
- Validation run: Typed challenged and failed scenarios, negative viable-state coverage, catalog-derived views, policy validation, forward tests, governance evidence, and hosted CI are required before completion.
- Disposition: Retain as a new automatic skill because it owns a missing decision—whether current evidence justifies continuing, pivoting, or stopping—while a typed trigger and explicit exclusions constrain overuse.
- Follow-up candidate: Review representative `approach_state` classifications after 30 routed tasks or two releases; merge or narrow the skill if it becomes a generic retry checklist or duplicates diagnosis.

## Pruning Signal
Consider pruning or merging when field notes show:

1. a skill is repeatedly skipped
2. a skill is selected but adds no evidence
3. two skills produce the same artifact
4. users repeatedly ask for less process
5. validators block low-risk work without meaningful safety value

Field notes are not just a log. They are the evidence base for keeping the pack practical.
