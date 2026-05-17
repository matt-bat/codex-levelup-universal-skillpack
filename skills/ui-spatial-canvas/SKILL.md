---
name: ui-spatial-canvas
description: "Use for frontend UI/UX work that should follow the Spatial Canvas paradigm: no-scrollbar viewport framing, flat root-level navigation, one-click home anchor, minimal click depth, and in-situ actions."
---

# UI Spatial Canvas

## Quick Index (Action-Routed)
### Read First (All Actions)
1. `Mission`
2. `Use This Skill When`
3. `Scope Boundary`
4. `Core Constraints (Non-Negotiable by Default)`

### Action Modules (Read As Needed)
1. Designing modality-specific flows:
   - `Interaction Modalities`
2. Commerce integration decisions:
   - `Commerce Pattern`
3. Visual system design:
   - `Visual Language`
4. Building and validating implementation:
   - `Implementation Workflow`
   - `Accessibility and Safety Guardrails`
   - `Exception Policy`
   - `Acceptance Checklist`

### Output
1. `Deliverable Format`
2. `Documentation Requirements`

## Mission
Design and implement a frictionless, content-first interface that behaves like a focused application workspace rather than a conventional scrolling website.

## Use This Skill When
1. building or refactoring end-user, member, and admin UI flows
2. designing interaction models for browse, create, manage, or transact workflows
3. defining frontend visual language (typography, overlays, motion, adaptive backgrounds)
4. reducing click depth and navigation friction in user-critical flows

## Scope Boundary
This skill applies the Spatial Canvas UI paradigm.

Use [Thoughtful Approach](../thoughtful-approach/SKILL.md) for:
1. generic end-user expectation modeling
2. must-have vs nice-to-have feature triage
3. scope-safe product enhancement decisions outside Spatial Canvas specifics

## Core Constraints (Non-Negotiable by Default)
1. no-scrollbar-first design:
   - avoid horizontal and vertical scrollbars across desktop/mobile
   - if unavoidable, scope the exception tightly and document why
2. unified tabular root:
   - major domains stay at root-level tabs (for example: Home, Workspace, Tasks, Settings)
3. 1-click home anchor:
   - users can always return to core root in one click or one gesture
4. minimal click-depth:
   - optimize actions to smallest safe step count
5. in-situ actions:
   - actions happen in context (overlay/modality) instead of route detours

## Interaction Modalities
### Explore (Public)
1. framed viewport navigation (swipe, arrow keys, wheel transitions)
2. no endless scroll as primary navigation pattern
3. focused detail view with contextual overlay actions (share, save, open, compare)

### Workstream (Member)
1. root tabs for progress domains (for example: queue, active, completed)
2. fast triage interactions (gesture, shortcut, tap-zone based)
3. immediate contextual actions for editing, assigning, sharing, or approval

### Operations (Admin)
1. flat root admin tabs for high-frequency actions
2. spatial organization for high-volume management workflows
3. command palette support for expert speed paths

## Commerce Pattern
1. avoid separate high-friction storefront detours when possible
2. provide in-situ transaction or upgrade modality in the working context
3. prefer express completion paths for low-step conversion

## Visual Language
1. typography as structure:
   - use deliberate font pairings aligned to product voice and readability goals
2. adaptive theming:
   - background and overlays should react to current task/context without reducing legibility
3. glass-and-grain overlays:
   - use depth/translucency only when it improves focus and hierarchy

## Implementation Workflow
1. map key user journeys (discover, execute, review, complete)
2. flatten information architecture to root-level navigation before styling
3. define home-anchor behavior globally (header, gesture, or persistent control)
4. design no-scroll viewport layouts for mobile and desktop first
5. place high-value actions in-context on the active surface
6. reduce click count per core flow and remove unnecessary intermediates
7. apply typography, overlay, and motion system
8. validate accessibility, focus order, and keyboard navigation
9. run responsive and regression checks for critical flows
10. document rationale and exceptions in repo docs

## Accessibility and Safety Guardrails
1. preserve readable contrast and visible focus states
2. ensure keyboard equivalents for gesture-heavy flows
3. provide non-gesture fallback controls for all critical actions
4. do not trade payment/auth correctness for click reduction

## Exception Policy
If constraints conflict:
1. prioritize correctness, accessibility, and legal/compliance requirements
2. allow scoped deviation from no-scrollbar rule only with documented rationale
3. preserve existing design-system patterns unless user explicitly requests Spatial Canvas override

## Documentation Requirements
1. record major UI decisions and tradeoffs in canonical docs
2. add concise code comments for non-obvious interaction logic
3. capture any constraint exceptions with impact and rationale

## Acceptance Checklist
1. root tabs are clear and immediately reachable
2. home anchor is always one action away
3. core flows have minimized interaction steps
4. in-situ overlays work across target viewports
5. keyboard and fallback controls exist for gesture-first flows
6. no-scrollbar-first goal achieved or deviations documented
7. docs updated for behavior and architecture changes

## Anti-Patterns
1. deep nested menus hiding primary domains
2. route hopping for simple contextual actions
3. infinite-scroll dependence for core navigation
4. decorative motion that increases friction
5. aggressive visual effects that reduce readability

## Deliverable Format
When applying this skill, provide:
1. updated interaction map
2. changed UI surfaces/components
3. click-depth improvements by flow
4. accessibility/fallback coverage summary
5. documented exceptions (if any)

## Source Reference
Primary source for this skill:
- this `SKILL.md`

## Related Skills
- [UI Design Skills](../ui-design-skills/SKILL.md): apply source-grounded UX principles before visual/theming decisions.
- [Order of Operations](../order-of-operations/SKILL.md): sequence UI architecture, implementation, and validation correctly.
- [Regression Prevention](../regression-prevention/SKILL.md): protect critical flows while redesigning interaction patterns.
- [Doc Maintenance](../doc-maintenance/SKILL.md): keep README/docs aligned with UX and workflow changes.
- [Token Reduction](../token-reduction/SKILL.md): keep UI design communication concise and outcome-first.
