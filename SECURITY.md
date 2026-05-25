# Security Policy

This repo is not an application runtime, but it still has security impact. The skills in this pack can influence how an agent plans work, runs commands, validates changes, records evidence, and decides whether something is ready to push.

The practical rule is simple: governance artifacts should explain decisions, not expose secrets.

## What To Report
Please report anything that could make the pack unsafe or misleading, especially:

1. a governance check can be bypassed in a surprising way
2. a skill encourages unsafe command execution without approval, validation, or rollback thinking
3. a doc suggests putting secrets into logs, artifacts, summaries, trackers, or field notes
4. a validator trusts unsafe paths, shell input, or generated files
5. two policy docs conflict in a way that could cause deployment, deletion, credential exposure, or permission changes without clear user intent

These issues are worth fixing quickly because they can shape what an agent does next.

## What Not To Put In Artifacts
Do not put secrets in:

1. `docs/governance/*.governance.json`
2. `docs/governance/*.governance.md`
3. `docs/chat-history-index.md`
4. `docs/chat-history-summary.md`
5. `skills/user-instructions.md`
6. field notes, task logs, or handoff docs

Good artifacts say what was checked, what passed, what failed, what risk remains, and who owns the next step. They should not contain credentials, API keys, tokens, production secrets, private customer data, private prompts, or anything that would become sensitive if this repo were shared.

## Validation Path
Before publishing policy, workflow, or validator changes, run the standard checks from the repository root:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
```

For governed changes, also validate the relevant governance artifact in strict mode. Use `skills/docs/validation-profiles.md` when you need to choose between quick, standard, and release-level validation.

## Fix Expectations
Security-relevant fixes should:

1. identify the affected skill, script, workflow, or doc
2. add or update a regression test when practical
3. update the docs that describe the affected behavior
4. include governance evidence when governed files changed
5. record any residual risk clearly instead of hiding uncertainty

If a full fix is not possible in one pass, make the unsafe path harder to trigger and document what still needs follow-up.
