---
name: diagnose-before-fix
description: Use for debugging or remediation work when reported symptoms may not be the true root cause; verify the cause independently before applying fixes, even when the user suggests one.
---

# Diagnose Before Fix

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Trigger Rule`
3. `Cause Verification Standard`

### Action Modules (Read As Needed)
1. Reproducing and isolating failures:
   - `Symptom Capture`
   - `Hypothesis Testing`
2. Choosing a fix path:
   - `Root Cause Decision Rule`
3. Confirming the repair:
   - `Verification After Fix`

### Output
1. `Output Contract`

## Mission
Separate observed symptoms from verified causes so fixes address the actual failure mode.

## Trigger Rule
Use this skill when:
1. a user reports a bug, error, regression, or broken behavior
2. the user suggests a cause but it is not yet proven
3. multiple plausible root causes exist
4. a quick patch would risk masking the true problem

Treat user-provided causes as hypotheses, not facts, until verified.

## Cause Verification Standard
Before changing behavior:
1. reproduce the symptom or inspect direct evidence
2. test the proposed cause explicitly
3. compare at least one alternative explanation when feasible
4. only fix the verified root cause

If the root cause cannot be verified:
1. say so plainly
2. limit changes to safe mitigation
3. preserve evidence for the next pass

## Symptom Capture
Record the failure in concrete terms:
1. what fails
2. where it fails
3. when it fails
4. what changed recently

## Hypothesis Testing
Test from cheapest to most informative:
1. direct logs or stack traces
2. targeted reproduction
3. narrow code-path inspection
4. focused unit or integration check

## Root Cause Decision Rule
Do not patch a visible symptom unless:
1. the cause is verified, or
2. the change is explicitly a temporary mitigation and is labeled as such

## Verification After Fix
After a fix:
1. rerun the reproducer or targeted check
2. confirm the original symptom is gone
3. confirm adjacent behavior still works

## Output Contract
When using this skill, provide:
1. symptom description
2. tested hypotheses
3. verified cause or verified uncertainty
4. fix applied or mitigation chosen
5. post-fix validation summary

## Related Skills
- [Regression Prevention](../regression-prevention/SKILL.md): protect adjacent behavior during the fix.
- [Effective Testing Methods](../effective-testing-methods/SKILL.md): add the smallest useful validation for the verified cause.
- [Order of Operations](../order-of-operations/SKILL.md): sequence diagnosis before mutation.
- [Thoughtful Approach](../thoughtful-approach/SKILL.md): avoid overfitting the fix to a symptom.
- [Scripted Command Execution](../scripted-command-execution/SKILL.md): run deterministic reproductions and probes.


## Least-resistance reasoning

Prefer the simplest explanation that fits the evidence. Test the cheapest reversible hypothesis first, and add complexity only when a failed test or new evidence requires it. Keep the claim falsifiable by naming what would confirm or disconfirm it.
