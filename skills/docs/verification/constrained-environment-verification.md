# Constrained Environment Verification

## Purpose
Use this fallback path when the right validation cannot run because the local environment is missing something.

Examples:

1. Playwright browser dependencies are not installed
2. headless browser system libraries are missing
3. sandbox or network limits block required setup commands
4. credentials or deployment permissions are intentionally unavailable

The goal is to be honest about what was checked and what was not checked.

## Required Inputs
1. changed behavior or flow scope
2. intended full validation matrix
3. blocked command output with the exact error text

## Procedure
1. Run a prerequisite probe before expensive checks:
   - verify binaries and runtime dependencies
   - verify command-level access assumptions
2. Attempt the full-layer command once.
3. If blocked, capture evidence:
   - command attempted
   - exact error line
   - blocked layer (`unit`, `integration`, `Playwright`, `build`)
4. Execute the fallback sequence:
   - static checks (`lint`, type checks)
   - available unit or integration subsets
   - test discovery/listing for blocked suites
   - targeted non-browser flow checks where possible
5. Update impacted tests or specs despite blocked execution.
6. Publish residual risk and rerun plan:
   - risk level
   - missing dependency
   - exact command to rerun once unblocked
7. For an authorized governed change to a protected `main` branch, use a feature branch and pull request and require the governance check to pass before merge. A constrained local environment does not authorize bypassing branch protection.

## Output Contract
1. `full_matrix_requested`: list of intended validation layers
2. `blocked_layers`: list with exact blocker evidence
3. `fallback_layers_executed`: list of checks that ran
4. `residual_risk`: explicit severity and rationale
5. `rerun_plan`: exact commands and dependency requirements

## Prohibitions
1. Do not claim complete regression safety when critical layers are blocked.
2. Do not hide blocker details behind generic failure summaries.
3. Do not skip test or spec updates solely because execution is blocked.

## Related Skills
1. `effective-testing-methods`
2. `regression-prevention`
3. `scripted-command-execution`
4. `skill-governance`
