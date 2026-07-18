# Field Notes

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
- Follow-up candidate: Evaluate routing observations after at least 30 representative tasks and two governed release candidates; verify exact-head attestation and remote branch-protection behavior only in an explicitly authorized release workflow.

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

## Pruning Signal
Consider pruning or merging when field notes show:

1. a skill is repeatedly skipped
2. a skill is selected but adds no evidence
3. two skills produce the same artifact
4. users repeatedly ask for less process
5. validators block low-risk work without meaningful safety value

Field notes are not just a log. They are the evidence base for keeping the pack practical.
