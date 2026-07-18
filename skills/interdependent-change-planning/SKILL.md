---
name: interdependent-change-planning
description: Coordinate an authorized change whose coupled files, contracts, flows, or data paths must move together to remain valid. Use when a local edit would leave a known dependent surface inconsistent; do not use merely because several files are touched independently.
---

# Interdependent Change Planning

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Trigger Rule`
3. `Connected-Change Standard`

### Action Modules (Read As Needed)
1. Mapping coupled surfaces:
   - `Impact Map`
   - `Dependency Ring`
2. Planning safe edits:
   - `Coherent Slice Rule`
   - `Shared-Invariant Check`
3. Finishing coherently:
   - `Validation and Handoff`

### Output
1. `Output Contract`

## Mission
Keep changes coherent across all parts that depend on one another.

## Trigger Rule
Use this skill when:
1. a change affects multiple related components, files, routes, or data paths
2. a local edit would leave adjacent behavior inconsistent
3. one update implies companion changes elsewhere
4. a shared invariant requires an atomic or explicitly staged migration

## Connected-Change Standard
Treat the touched area as a connected system, not isolated edits.

Before editing:
1. identify direct touchpoints
2. identify downstream consumers
3. identify shared invariants
4. decide whether companion updates are required

## Impact Map
Extend the canonical task impact map rather than creating a duplicate. Record:
1. primary file or module being changed
2. directly affected neighbors
3. dependent surfaces that must stay aligned
4. validation needed for the connected set

## Dependency Ring
For each touched element, check:
1. what reads it
2. what writes it
3. what assumes its shape or meaning
4. what breaks if it changes alone

## Coherent Slice Rule
Make the smallest change that is still system-complete.

Do not:
1. land half of a coupled update
2. leave temporary mismatches without a follow-up plan
3. change one surface while knowingly desynchronizing another

## Shared-Invariant Check
Before finalizing, confirm:
1. shared data shapes still match
2. user flows still line up
3. docs or tests that describe the same concept agree

## Validation and Handoff
Validate the connected surfaces together and note any deferred companion work explicitly.

## Output Contract
When using this skill, provide:
1. connected surfaces identified
2. invariants checked
3. coordinated updates made
4. deferred companion work, if any
5. validation summary

Activating this skill grants no authority to mutate companion surfaces outside the user's task. If a required companion change would expand scope materially, stop and request direction.

## Related Skills
- [Thoughtful Approach](../thoughtful-approach/SKILL.md): decide what should move together from a user-value perspective.
- [Regression Prevention](../regression-prevention/SKILL.md): protect dependent behavior while coordinating the change.
- [Order of Operations](../order-of-operations/SKILL.md): sequence foundational and dependent edits correctly.
- [File Structure Optimization](../file-structure-optimization/SKILL.md): use when coupling comes from repository layout.
- [Doc Maintenance](../doc-maintenance/SKILL.md): keep connected docs aligned with implementation.
