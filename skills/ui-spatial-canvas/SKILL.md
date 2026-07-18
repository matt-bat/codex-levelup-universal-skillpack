---
name: ui-spatial-canvas
description: Use only when the user explicitly requests the Spatial Canvas design system or when repository evidence establishes Spatial Canvas as the existing interface architecture being modified. Do not activate for generic frontend, UI, UX, layout, navigation, interaction, or visual-system work.
---

# UI Spatial Canvas

## Purpose
Apply the established Spatial Canvas interaction system to an explicitly in-scope interface.

Before using this skill, confirm at least one:
1. the user named or requested Spatial Canvas
2. repository documentation, components, or conventions clearly establish it as the current design system

If neither is true, remain inactive and use generic UI guidance instead.

## System Constraints
Within an approved Spatial Canvas surface:
1. frame primary work around the viewport rather than page-length navigation
2. keep major domains reachable through a flat root-level model
3. preserve a one-action home or root anchor
4. minimize safe interaction depth
5. prefer contextual actions over unnecessary route detours

These are system preferences, not permission to break content access, responsive behavior, platform conventions, or established repository constraints.

## Exception Priority
1. correctness, accessibility, and legal or safety requirements
2. explicit user requirements
3. existing repository design-system compatibility
4. Spatial Canvas preferences

Scrolling is allowed when content, accessibility, viewport, or platform needs make it the better interaction. Document an exception only when documentation is already part of the task.

## Workflow
1. Identify the existing Spatial Canvas primitives and affected user journey.
2. Preserve the root model and home-anchor behavior.
3. place high-value actions in context without hiding recovery paths
4. provide keyboard, touch, and non-gesture alternatives
5. validate target viewports, focus order, readable contrast, and critical states
6. verify the change against the repository's existing component and motion system

## Artifact Boundary
Do not redesign unrelated surfaces, create design documentation, or introduce new visual dependencies solely because this skill activated.

## Conditional Reference
Read [Spatial Canvas System](./references/spatial-canvas-system.md) only when the task needs modality patterns, commerce guidance, visual-language details, or the full acceptance checklist.

## Output
Report only material interaction changes, accessibility coverage, validation, and any approved exception.
