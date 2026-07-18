# Maturity Model

Adopt capabilities gradually. An installed or available skill is not an active skill: the task router may select zero skills, and each package activates only when its catalog trigger matches.

## Level 1: Core Policy and Routing

Goal: preserve authority, user work, instruction precedence, and proportional validation without routine ceremony.

Capabilities:

1. root `AGENTS.md` core policy
2. canonical `skill-catalog.json`
3. generated routing views
4. zero-skill route and a routine target median of two or fewer selected skills

Evidence:

1. routine tasks do not create governance or tracking artifacts
2. read-only tasks perform zero writes
3. startup declarations appear only when explicitly requested or required as governed evidence

## Level 2: Development Workflows

Goal: make implementation, diagnosis, testing, documentation, and command execution safer when their precise triggers apply.

Available packages include `diagnose-before-fix`, `regression-prevention`, `effective-testing-methods`, `scripted-command-execution`, `interdependent-change-planning`, and `doc-maintenance`.

Evidence:

1. unverified causes are diagnosed before patching
2. behavior changes get surface-appropriate validation
3. test-design and implementation ownership remain separate
4. canonical documentation changes only when it would otherwise be inaccurate

## Level 3: Governed Validation

Goal: make release-affecting, policy-changing, externally mutating, destructive, or otherwise high-risk work auditable.

Available packages include `skill-governance`, `governance-enforcement`, and `semantic-policy-audit`.

Evidence:

1. governed changes bind evidence to the exact base and candidate content
2. mandatory gates fail closed on missing, stale, or pending evidence
3. release attestations identify the exact commit
4. external release controls are verified independently

## Level 4: Lifecycle Management

Goal: keep the pack coherent as routing evidence accumulates.

Available packages include `skill-usage-review`, `deprecation-management`, `file-maintenance`, and `artifact-budget-enforcement`.

Evidence:

1. bounded observations reveal overuse, underuse, corrections, and retries without retaining prompts or source content
2. compatibility aliases are one-way and time-bounded
3. cached artifacts stay within declared limits
4. generated views cannot drift from the catalog

## Level 5: Evidence-Driven Improvement

Goal: improve from representative task outcomes rather than speculative rules.

Evidence:

1. at least 30 representative routed tasks or two releases cover the migration observation window
2. recurring friction becomes a tested catalog, router, or skill change
3. rarely used skills are justified, merged, deprecated, or removed through an explicit lifecycle decision
4. validation profiles reflect actual risk boundaries

## Advancement and Regression

Advance only when the prior level produces reliable evidence. If process friction increases, reduce optional routing for routine tasks while preserving mandatory safety gates for governed work.
