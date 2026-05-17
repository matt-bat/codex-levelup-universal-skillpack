---
name: pseudo-agentic-automation
description: Use for browser or GUI automation tasks that require iterative scripts, runtime adaptation, and debugging loops (for example dynamic scraping, authenticated web flows, CAPTCHA handoffs, and headed/headless browser control).
---

# Pseudo-Agentic Automation

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Overview`
2. `Preconditions`
3. `Use This Skill When` / `Do Not Use This Skill When`

### Action Modules (Read As Needed)
1. Running automation loops:
   - `Execution Loop`
   - `Tool Guidance`
2. Hardening runtime behavior:
   - `Robust Patterns`
   - `Pitfalls`
   - `Security and Ops`

### Output
1. `Deliverable Format`

## Overview
Use this skill for browser and GUI automation tasks that need iterative script execution, debugging, and adaptation.

Use [Scripted Command Execution](../scripted-command-execution/SKILL.md) for simple command chains, setup tasks, and deterministic local operations.
If the request can be solved with deterministic shell commands alone, switch to that skill.

## Preconditions
Before execution:
1. confirm automation target and success criteria
2. confirm required credentials/access are available
3. confirm whether headless or headed mode is appropriate
4. confirm any legal/terms constraints for scraping/automation
5. for new projects (model has not worked on before), ask whether model should run tests/build by default or user will run them to save tokens
6. operate locally by default; do not deploy unless explicitly requested

## Use This Skill When
- The target is a dynamic/authenticated website.
- No stable API exists.
- Browser rendering and interaction is required for E2E behavior checks.
- Native GUI control is required and direct shell actions are insufficient.

## Do Not Use This Skill When
- A static file can be fetched directly.
- A straightforward REST API call solves the request.
- The task is simple local shell/file work.

## Execution Loop
1. Clarify goal and constraints.
2. Prepare minimal runtime dependencies.
3. Write scripts that output machine-readable success data and rich failure diagnostics.
4. Execute scripts.
5. Inspect logs/artifacts and iterate.
6. Stop after bounded retries and escalate with concrete failure evidence.

Retry budget:
1. default max retries: 3
2. if blocked by CAPTCHA/anti-bot twice, switch to human-handoff flow
3. if selectors keep failing with no stable anchors, escalate with captured artifacts

## Tool Guidance
- `browser-use`: for highly dynamic pages with unstable selectors.
- `Playwright`: for deterministic browser automation and structured extraction.
- `Puppeteer`: for Node-centric automation or PDF-heavy workflows.
- `PyAutoGUI`: fallback only; coordinate-based and fragile.
- `PyWinAuto` / `Appium`: preferred for semantic native UI automation where available.

## Robust Patterns
- Log precise failure context to `stderr` (URL, selector, compact DOM snapshot).
- Always close browser/resources in `finally`.
- Write large outputs to files (JSON preferred), then read those artifacts.
- On CAPTCHA/challenges, switch to headed mode and perform explicit human handoff.

## Pitfalls
1. Infinite retries: cap attempts.
2. Zombie processes: always clean up child processes.
3. Headless detection: switch to headed mode when anti-bot behavior appears.
4. Fragile selectors: prefer role/text/test-id over dynamic classes.

## Security and Ops
1. Run scripts in project-local or temporary directories.
2. Keep credentials in environment variables.
3. Minimize dependency-install side effects.

## Deliverable Format
When applying this skill, provide:
1. target and completion criteria
2. script/run summary
3. artifact locations (logs/screenshots/outputs)
4. pass/fail outcome
5. blockers and next action

## Related Skills
- [Scripted Command Execution](../scripted-command-execution/SKILL.md): use for deterministic local command workflows.
- [Token Reduction](../token-reduction/SKILL.md): keep automation reports concise while preserving evidence.
