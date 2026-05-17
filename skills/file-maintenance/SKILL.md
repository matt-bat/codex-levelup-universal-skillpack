---
name: file-maintenance
description: Use for continuous maintenance of repository files with emphasis on correctness, factual accuracy, freshness, consistency, and duplicate/stale file prevention.
---

# File Maintenance

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Use This Skill When`
3. `Scope Boundary`
4. `Core Principles`

### Action Modules (Read As Needed)
1. Accuracy maintenance:
   - `File Integrity Audit`
   - `Factuality and Freshness Checks`
2. Consistency maintenance:
   - `Cross-File Consistency Rules`
   - `Duplicate and Staleness Control`
3. Documentation maintenance depth:
   - `Doc Accuracy Standard`
   - `Operational Validation`

### Output
1. `Deliverable Format`
2. `Anti-Patterns`

## Mission
Maintain repository files so they remain accurate, current, internally consistent, and actionable for developers and operators.

## Use This Skill When
1. documentation or policy files may be stale after changes
2. duplicate files or conflicting variants appear
3. commands/examples in docs might no longer match implementation
4. periodic file hygiene reviews are requested
5. quality audits require factuality and consistency checks

## Scope Boundary
This skill governs ongoing file lifecycle quality across docs and support artifacts.

Use [Doc Maintenance](../doc-maintenance/SKILL.md) for:
1. change-driven documentation updates during active implementation

Use [File Structure Optimization](../file-structure-optimization/SKILL.md) for:
1. repo layout and directory architecture optimization

## Core Principles
1. every maintained file must have a clear purpose and current owner context
2. prefer one canonical source per fact
3. stale or conflicting files must be corrected, consolidated, or removed
4. documentation claims require validation evidence
5. maintenance outputs must be auditable

## File Integrity Audit
Audit file surfaces for:
1. purpose clarity
2. last-updated relevance
3. duplicate/conflicting variants
4. broken references/paths/commands
5. ownership ambiguity

## Factuality and Freshness Checks
For high-value docs/artifacts:
1. verify dates, versions, and commands are still valid
2. verify referenced paths/files exist
3. verify procedures match current behavior
4. verify policy statements match enforced tooling
5. mark unresolved uncertainty explicitly

## Cross-File Consistency Rules
1. same concept should not be described differently across canonical docs
2. terminology must be consistent across policy/runbook files
3. sample commands must align with current scripts
4. linked artifacts must exist and be reachable
5. if conflicts exist, designate canonical source and reconcile others

## Duplicate and Staleness Control
1. detect duplicate files with overlapping scope
2. consolidate into canonical file where feasible
3. archive/remove obsolete copies with explicit notes when needed
4. avoid keeping "backup" duplicates in active source paths
5. track unresolved cleanup items with owner and date

## Doc Accuracy Standard
For docs in scope, ensure:
1. statements are specific and testable
2. instructions are executable in current repo context
3. references use current filenames and paths
4. temporal language is minimized unless date-bound context is required
5. update timestamps/status artifacts reflect latest state

## Operational Validation
Recommended validation pass:
1. targeted command execution or plausibility check
2. link/path existence scan
3. policy-to-enforcement alignment check
4. issue list of remaining uncertain claims

## Acceptance Checklist
1. no unresolved high-severity factual conflicts
2. no broken high-priority file references
3. stale duplicates addressed or tracked with explicit remediation
4. docs/policies aligned with actual tooling behavior
5. maintenance evidence captured

## Deliverable Format
When applying this skill, provide:
1. files audited and findings
2. corrections/consolidations/removals made
3. validation checks run and outcomes
4. unresolved items with severity and next action

## Source Reference
Primary references:
1. Google developer documentation style guidance:
   - https://developers.google.com/style/
   - https://developers.google.com/style/timeless-documentation
2. Apple documentation workflow guidance:
   - https://developer.apple.com/documentation/xcode/writing-documentation
   - https://developer.apple.com/documentation/xcode/documenting-apps-frameworks-and-packages
3. MIT software construction quality principles:
   - https://ocw.mit.edu/courses/6-005-software-construction-spring-2016/

## Anti-Patterns
1. leaving known inaccuracies untracked
2. keeping multiple conflicting "source of truth" files
3. updating content without validating commands/paths
4. burying critical caveats in non-canonical docs
5. treating file hygiene as optional after major changes

## Related Skills
- [Doc Maintenance](../doc-maintenance/SKILL.md): implementation-time documentation synchronization.
- [File Structure Optimization](../file-structure-optimization/SKILL.md): repository architecture hygiene.
- [User Instructions Tracker](../user-instructions-tracker/SKILL.md): track directive-driven maintenance obligations.
- [Governance Enforcement](../governance-enforcement/SKILL.md): validate policy-file correctness through tooling.
