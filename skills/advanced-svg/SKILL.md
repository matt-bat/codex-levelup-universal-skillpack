---
name: advanced-svg
description: Design, generate, review, or repair sophisticated SVG assets and SVG-based interfaces using reusable geometry, composition, paint, filter, accessibility, security, and validation patterns. Use for vector_graphics tasks that need more than a basic icon or isolated shape; do not use for raster image generation or trivial edits to an established SVG asset.
---

# Advanced SVG

## Mission

Produce intentional, reusable SVG systems whose geometry, rendering, accessibility, and integration behavior remain understandable after generation.

## Workflow

1. Establish the delivery context: standalone file, inline HTML, CSS background, component framework, sprite, icon, diagram, chart, or print/export asset.
2. Establish the viewport, coordinate system, aspect-ratio behavior, target sizes, theme tokens, interaction needs, and browser/runtime constraints.
3. Sketch the visual hierarchy as primitive geometry and named reusable components before writing detailed paths.
4. Read only the references needed for the requested surface:
   - Read [Geometry and Paths](references/geometry-and-paths.md) for coordinate systems, curves, arcs, compound paths, and procedural shapes.
   - Read [Components and Composition](references/components-and-composition.md) for `defs`, `symbol`, `use`, markers, text paths, diagrams, charts, and ID hygiene.
   - Read [Paint and Effects](references/paint-and-effects.md) for gradients, patterns, clipping, masks, filters, and controlled texture.
   - Read [Quality, Accessibility, and Security](references/quality-accessibility-security.md) for semantic alternatives, theming, animation, performance, compatibility, and safe embedding.
   - Read [Authoritative Sources](references/authoritative-sources.md) when a feature or compatibility claim needs verification.
5. Build from stable primitives and shared definitions. Prefer readable geometry over opaque path data when both render equivalently.
6. Use unique, namespaced IDs for every referenced definition. Keep references local unless the delivery contract explicitly permits external resources.
7. Validate XML and references with `python3 scripts/validate_svg.py <file.svg>`. Treat unsafe-feature findings as blockers unless the embedding context explicitly requires and safely handles them.
8. Render at the smallest, nominal, and largest target sizes with `python3 scripts/render_svg.py <file.svg>`. Require both `rsvg` and `chromium` for compatibility-sensitive deliverables; inspect reported visible bounds and cross-renderer pixel divergence.
9. Inspect theme contrast, text overflow, focus behavior, reduced motion, and accessibility semantics in the actual embedding context when those behaviors apply.

## Composition Rules

1. Set `viewBox` deliberately; add explicit `width` and `height` only when the delivery context requires intrinsic dimensions.
2. Group by semantic component, not by accidental draw order. Name IDs after roles rather than appearance.
3. Put reusable paint servers, masks, clips, filters, markers, symbols, and paths in `defs`.
4. Keep the scene's visual reading order aligned with DOM order when accessibility or interaction matters.
5. Use CSS custom properties or `currentColor` for themeable assets. Provide safe fallback values.
6. Keep effects subordinate to shape and hierarchy. Expand filter regions enough to prevent clipped shadows or glows.
7. Avoid embedding base64 raster data, fonts, scripts, event-handler attributes, or remote URLs unless the task explicitly needs them.

## Output Contract

Deliver:

1. valid SVG with a coherent viewport and no unresolved local references
2. reusable definitions and namespaced IDs where composition warrants them
3. a text alternative strategy appropriate to decorative, informative, functional, or complex imagery
4. explicit notes for intentional compatibility tradeoffs, external dependencies, animation, or unsafe-capability requirements
5. structural and renderer evidence proportional to the target surface

## Authority and Artifact Policy

Create or modify SVG files only when the task authorizes file writes. Skill activation does not authorize fetching external assets, embedding third-party material, adding scripts, installing renderers, or changing application code. Keep design notes conversation-local unless a requested deliverable or existing repository contract requires a durable artifact.

## Completion Gates

1. Geometry remains legible and unclipped across required sizes.
2. IDs are unique and every local `url(#...)` or fragment reference resolves.
3. Decorative and meaningful graphics use the correct alternative-text strategy.
4. Interactive SVG has keyboard, focus, and reduced-motion behavior where applicable.
5. No unapproved script, event handler, `foreignObject`, remote reference, or embedded executable content remains.
6. The SVG structural validator passes or every reported exception is explained.
7. Renderer verification passes at required sizes; compatibility-sensitive work uses two independent engines or identifies the exact missing dependency as residual risk.
