---
name: thoughtful-approach
description: Model end-user goals, expected baseline behavior, and product tradeoffs when a feature request requires product judgment. Use for feature planning or authorized implementation with meaningful user-experience choices; do not use for fixed mechanical work, and never treat a plausible enhancement as authorized scope.
---

# Thoughtful Approach

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Use This Skill When`
3. `Core Principle`
4. `Scope Boundary`

### Action Modules (Read As Needed)
1. Modeling user expectations:
   - `End-User Lens (Required)`
   - `Expectation Modeling`
2. Controlling enhancement scope:
   - `Scope-Safe Enhancement Rules`
   - `Decision Framework (Required)`
3. Quality refinement by surface:
   - `Quality Heuristics by Surface`
4. Delivery sequencing:
   - `Delivery Pattern`

### Output
1. `Output Contract`
2. `Anti-Patterns`

## Mission
Deliver outputs that feel intentionally useful to real end users, not merely technically complete.

## Use This Skill When
1. translating user requests into product behavior or UI flows
2. designing or refining apps, dashboards, forms, or data workflows
3. deciding what to include now vs later for best user value
4. evaluating optional enhancements while preserving requested scope

## Core Principle
Honor explicit requirements first. Separate expected baseline behavior, necessary implications, and optional enhancements; product value does not grant implementation authority.

## Scope Boundary
This skill is product/feature expectation modeling and scope-safe enhancement logic.

Use [UI Spatial Canvas](../ui-spatial-canvas/SKILL.md) when:
1. implementing the specific Spatial Canvas visual/interaction paradigm
2. applying no-scrollbar framed navigation architecture
3. tuning typography/overlay/theming rules for that design system

## End-User Lens (Required)
For each task, identify:
1. primary user role(s)
2. primary outcome they need
3. friction points likely to block that outcome
4. minimum acceptable success state

If role/context is unclear:
1. infer from request and repository domain
2. note assumptions explicitly
3. avoid speculative architecture beyond request boundaries

## Expectation Modeling
Build a concise expectation model with 3 tiers:
1. Must-have expectations:
   - core capabilities users reasonably expect in this type of product
2. Nice-to-have expectations:
   - quality and convenience features that improve usability
3. Defer/avoid:
   - ideas that are valuable but would cause scope drift now

Example (notes organizer app):
1. Must-have:
   - create/edit/delete notes
   - search/filter notes
   - persistence and reliable save state
2. Nice-to-have:
   - tags/folders
   - pin/favorite
   - markdown preview
3. Defer/avoid:
   - full real-time collaboration
   - AI semantic summarization stack
   - plugin marketplace

## Scope-Safe Enhancement Rules
Enhancements are allowed only when they satisfy all conditions:
1. directly support the requested use case
2. do not alter explicit product direction
3. low implementation risk/cost relative to value
4. do not block delivery of must-haves
5. can be disabled or deferred cleanly if needed
6. are explicitly authorized or inseparable from a stated acceptance criterion

If any condition fails, move enhancement to deferred list.

## Quality Heuristics by Surface
### Interface/UX
1. reduce clicks and cognitive load for primary workflows
2. maintain clear affordances and consistent interaction patterns
3. preserve accessibility (keyboard, contrast, focus, labels)
4. design for mobile and desktop parity where relevant

### Data and State
1. make save state and error states explicit
2. prevent accidental data loss
3. include sensible defaults and empty states
4. preserve predictable behavior across reloads/sessions when expected

### Operational Usability
1. make onboarding/setup obvious
2. keep important controls visible and discoverable
3. provide actionable error messages and recovery paths
4. document usage expectations in README/docs when behavior changes

## Decision Framework (Required)
For each candidate enhancement, score quickly:
1. user impact (`low/medium/high`)
2. implementation complexity (`low/medium/high`)
3. risk of scope drift (`low/medium/high`)
4. testability (`low/medium/high`)

Default implementation rule:
1. implement only when authorized and impact is high while complexity/drift risk are low-medium
2. propose or defer when useful but not authorized
3. defer if drift risk is high or testability is poor

## Delivery Pattern
1. implement must-haves first
2. add only authorized scope-safe enhancements second
3. document deferred improvements as optional next steps
4. validate primary end-user flows before finalizing

## Output Contract
When using this skill, provide:
1. inferred end-user model (role + goal)
2. must-have coverage summary
3. implemented enhancements and why they were safe
4. deferred enhancements with rationale
5. end-user flow validation summary

## Anti-Patterns
1. shipping technically complete but user-hostile flow
2. adding clever features that bypass explicit request intent
3. overengineering early with low confidence requirements
4. omitting expected baseline capabilities for known app types
5. treating nice-to-haves as mandatory blockers

## Related Skills
- [Skill Governance](../skill-governance/SKILL.md): choose process level before broadening feature scope.
- [Order of Operations](../order-of-operations/SKILL.md): sequence must-haves before enhancements.
- [UI Spatial Canvas](../ui-spatial-canvas/SKILL.md): apply viewport-first interaction principles for frontend experiences.
- [UI Design Skills](../ui-design-skills/SKILL.md): apply source-grounded UX quality checks from trusted design standards.
- [Regression Prevention](../regression-prevention/SKILL.md): protect existing behavior while improving usability.
- [Doc Maintenance](../doc-maintenance/SKILL.md): document user-facing behavior and enhancement decisions.
