# Constrained Environment Verification

## Purpose
Provide a deterministic fallback verification path when full validation layers cannot run due to local environment constraints.

Examples:
1. missing browser runtime dependencies for Playwright
2. missing system libraries required by headless browsers
3. sandbox/network limits blocking required setup commands

## Required Inputs
1. changed behavior/flow scope
2. intended full validation matrix
3. blocked command output (exact error text)

## Procedure
1. Run prerequisite probe before expensive checks:
   - verify binaries and runtime dependencies
   - verify command-level access assumptions
2. Attempt full-layer command once.
3. If blocked, capture evidence:
   - command attempted
   - exact error line
   - blocked layer (`unit`, `integration`, `Playwright`, `build`)
4. Execute fallback sequence:
   - static checks (`lint`, type checks)
   - available unit/integration subsets
   - test discovery/listing for blocked suites
   - targeted non-browser flow checks where possible
5. Update impacted tests/specs despite blocked execution.
6. Publish residual risk and rerun plan:
   - risk level
   - missing dependency
   - exact command to rerun once unblocked

## Output Contract
1. `full_matrix_requested`: list of intended validation layers
2. `blocked_layers`: list with exact blocker evidence
3. `fallback_layers_executed`: list of checks that ran
4. `residual_risk`: explicit severity and rationale
5. `rerun_plan`: exact commands and dependency requirements

## Prohibitions
1. Do not claim complete regression safety when critical layers are blocked.
2. Do not hide blocker details behind generic failure summaries.
3. Do not skip test/spec updates solely because execution is blocked.

## Related Skills
1. `effective-testing-methods`
2. `regression-prevention`
3. `scripted-command-execution`
4. `skill-governance`
