---
name: scripted-command-execution
description: Use for deterministic shell automation and setup tasks (for example environment bootstrap, service orchestration, batch file operations, and repeatable local command pipelines with explicit validation).
---

# Scripted Command Execution

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Overview`
2. `Scope Boundary`
3. `Preconditions`
4. `Use This Skill When` / `Do Not Use This Skill When`

### Action Modules (Read As Needed)
1. Executing command workflows:
   - `Workflow`
   - `Command Rules`
2. Using helper scripts:
   - `Script Guidance`
3. Validating command outcomes:
   - `Validation Checklist`

### Output
1. `Deliverable Format`

## Overview
Use this skill for deterministic local automation tasks handled by shell commands or small helper scripts.

Use [Pseudo-Agentic Automation](../pseudo-agentic-automation/SKILL.md) only when browser/GUI interaction is required.

## Scope Boundary
Use this skill when command execution needs explicit deterministic workflow structure, retry policy, and validation contract.

Do not invoke for one-off trivial commands that do not require orchestration.

## Preconditions
Before execution:
1. define desired end state
2. verify working directory and permissions
3. identify potential side effects
4. identify rollback/recovery approach for risky operations
5. for new projects (model has not worked on before), ask whether model should run tests/build by default or user will run them to save tokens
6. operate locally by default; do not deploy unless explicitly requested
7. for expensive verification commands, probe runtime dependencies first (for example browsers, shared libraries, required binaries)

## Use This Skill When
- Setting up environments and dependencies.
- Running local service orchestration flows.
- Performing repeatable batch operations.
- Executing command pipelines with clear expected outputs.

## Do Not Use This Skill When
- Browser-based login/CAPTCHA flows are required.
- Dynamic web interaction is core to task success.
- Native GUI automation is required.

## Workflow
1. Clarify desired end state.
2. Check current state first (`pwd`, `ls`, status commands).
3. Execute minimal command sequence.
4. Validate results explicitly.
5. If commands fail, inspect stderr, adjust, and retry with bounded attempts.

Retry policy:
1. default retry limit: 3
2. if repeated failures suggest missing prerequisites, pause and resolve prerequisites first
3. if failure risk escalates (data loss/security), stop and escalate

## Command Rules
1. Prefer idempotent commands.
2. Scope side effects to the project directory.
3. Use non-interactive flags by default.
4. Avoid destructive operations unless explicitly requested.
5. Capture key outputs for verification.
6. Do not run deployment/publish/release commands unless user explicitly asks.

## Script Guidance
1. Use short scripts only when command chains become complex.
2. Emit machine-readable result artifacts when needed (JSON/text files).
3. Print diagnostics to stderr.
4. Exit non-zero on failure paths.

## Validation Checklist
1. Confirm expected files/directories/services are present.
2. Confirm outputs match requested outcomes.
3. Confirm sensitive data was not staged or exported.
4. Report exact commands and results.
5. If a command is blocked by environment constraints, capture exact blocker error and switch to constrained verification fallback rather than blind retries.

## Deliverable Format
When applying this skill, provide:
1. end-state target
2. commands executed
3. validation results
4. unresolved issues or residual risk

## Related Skills
- [Order of Operations](../order-of-operations/SKILL.md): sequence dependent commands safely.
- [Token Reduction](../token-reduction/SKILL.md): keep command reporting concise.
