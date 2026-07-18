---
name: file-structure-optimization
description: Use for designing and maintaining repository file structure for clarity, modularity, discoverability, and low-duplication across app and documentation surfaces.
---

# File Structure Optimization

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Use This Skill When`
3. `Scope Boundary`
4. `Core Principles`

### Action Modules (Read As Needed)
1. Structural assessment:
   - `Structure Audit`
   - `Smell Detection`
2. Refactoring strategy:
   - `Normalization Rules`
   - `Migration Safety Rules`
3. Long-term hygiene:
   - `Ownership and Boundaries`
   - `Acceptance Checklist`

### Output
1. `Deliverable Format`
2. `Anti-Patterns`

## Mission
Keep repository layout predictable, modular, and easy to navigate while minimizing duplication and stale artifacts.

## Authority and Artifact Policy
1. Activating this skill grants no authority to create, move, rename, merge, or delete files or directories.
2. Read-only structure work produces an assessment or proposed map only.
3. Implement a structural migration only when the task separately authorizes its affected paths and operations.

## Use This Skill When
1. adding major features introducing new directories/files
2. repo navigation or discoverability has become difficult
3. duplicate or near-duplicate files are accumulating
4. refactors require moving modules, docs, or scripts
5. monorepo boundaries are unclear or leaking responsibilities

## Scope Boundary
This skill governs filesystem information architecture and structural hygiene.

Use [Doc Maintenance](../doc-maintenance/SKILL.md) and [File Maintenance](../file-maintenance/SKILL.md) for:
1. content-level documentation correctness and lifecycle maintenance

Use [Order of Operations](../order-of-operations/SKILL.md) for:
1. dependency-safe execution order for moves/renames

## Core Principles
1. organize by stable domain boundaries, not temporary implementation details
2. one canonical home per concern
3. explicit boundaries between app code, tooling, tests, docs, and generated artifacts
4. minimize path depth for high-frequency files
5. prevent duplicated truth sources

## Structure Audit
Evaluate current structure for:
1. discoverability of core app entrypoints
2. cohesion of modules inside each directory
3. coupling/leakage across domains
4. duplicate docs/scripts/config fragments
5. dead or orphaned files

## Smell Detection
Flag these smells:
1. multiple directories claiming same ownership domain
2. files named with vague terms (`misc`, `temp`, `new2`, `copy-final`)
3. deeply nested directories with single-child chains
4. duplicated docs differing by small stale edits
5. generated files mixed with hand-edited source without clear separation

## Normalization Rules
1. define top-level directory purposes explicitly
2. separate source, tests, docs, tooling, and build artifacts
3. keep naming conventions consistent across sibling paths
4. co-locate files that change together
5. centralize shared utilities instead of cloning copies

## Migration Safety Rules
1. batch moves by domain and keep PR scope legible
2. update imports, references, and docs in same change
3. preserve history with rename/move-aware operations where possible
4. validate commands, tests, and CI paths after moves
5. capture temporary compatibility shims only when necessary and time-bound

## Ownership and Boundaries
1. define directory ownership or steward role for critical areas
2. maintain clear public/internal module boundaries
3. document canonical paths for runbooks and policy artifacts
4. treat structure drift as maintenance debt with explicit remediation

## Acceptance Checklist
1. each top-level directory has a clear purpose
2. duplicate/stale artifacts are removed or consolidated
3. references/imports/docs updated to new paths
4. structure supports fast onboarding and maintenance
5. no orphaned files remain from migration

## Deliverable Format
When applying this skill, provide:
1. structure audit findings
2. proposed/implemented directory map
3. files moved/merged/removed summary
4. validation results for references and tooling
5. residual cleanup backlog

## Source Reference
Primary references:
1. Apple modular code organization guidance:
   - https://developer.apple.com/documentation/xcode/organizing-your-code-with-local-packages
2. Google engineering consistency/style guidance:
   - https://google.github.io/styleguide/
3. MIT software construction modularity and abstraction principles:
   - https://ocw.mit.edu/courses/6-005-software-construction-spring-2016/

## Anti-Patterns
1. organizing primarily by framework internals over domain purpose
2. preserving duplicate files "just in case" without ownership
3. mixing generated and source artifacts without boundaries
4. moving files without synchronized reference/doc updates
5. deep nesting that hides high-traffic files

## Related Skills
- [Order of Operations](../order-of-operations/SKILL.md): sequence structural changes safely.
- [Regression Prevention](../regression-prevention/SKILL.md): validate no behavior regressions during structural refactors.
- [Doc Maintenance](../doc-maintenance/SKILL.md): keep structural docs aligned with moves.
- [File Maintenance](../file-maintenance/SKILL.md): sustain structure quality through ongoing audits.
