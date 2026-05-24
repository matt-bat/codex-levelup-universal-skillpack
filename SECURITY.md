# Security Policy

This skillpack controls agent behavior, local command execution, validation gates, and governance artifacts. Treat policy bypasses and unsafe workflow guidance as security-relevant issues.

## Reportable Issues
Report issues when you find:
1. governance checks that can be bypassed unexpectedly
2. unsafe command guidance without an approval or rollback gate
3. instructions that could leak secrets into artifacts, logs, or summaries
4. validation scripts that trust unvalidated paths or shell input
5. policy conflicts that could cause deployment, deletion, or credential exposure without explicit user intent

## Artifact Safety
Do not place secrets in:
1. `docs/governance/*.governance.json`
2. `docs/governance/*.governance.md`
3. `docs/chat-history-index.md`
4. `docs/chat-history-summary.md`
5. `skills/user-instructions.md`

Governance artifacts should record evidence and decisions, not credentials, tokens, personal secrets, or private production data.

## Supported Validation Path
Use the repository validators before publishing policy or workflow changes:

```sh
python3 skills/skill-governance/scripts/validate_skill_policy.py --agents-path AGENTS.md --skills-root skills --repo-root .
python3 skills/skill-governance/scripts/validate_skill_order_sync.py --skills-root skills
python3 -m unittest discover -s skills/skill-governance/tests -p 'test_*.py'
```

## Response Expectations
Security-relevant fixes should:
1. identify the affected skill or script
2. add or update a regression test when practical
3. update docs that describe the affected behavior
4. include governance evidence for governed files
