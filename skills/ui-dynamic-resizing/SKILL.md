---
name: ui-dynamic-resizing
description: Apply fluid, proportional UI sizing with separate mobile and desktop tuning, readable wrapping, and accessible zoom unless the user explicitly requests static dimensions.
---

# UI Dynamic Resizing

Apply this skill to every UI implementation or review unless the user explicitly requests static element sizes. Tune mobile and desktop as separate responsive regimes while preserving each element’s intended relative hierarchy.

- Use fluid units and bounds (`%`, `rem`, `clamp()`, grid/flex, and container or media queries) for text, spacing, controls, and containers.
- Define mobile and desktop tokens separately; do not scale desktop values blindly onto narrow screens.
- Keep text inside its container. Preserve whole words with normal wrapping, `overflow-wrap: normal`, `word-break: normal`, and `hyphens: manual`; allow breaks at explicit hyphens and whitespace only.
- Make font size, line height, control dimensions, and gaps adapt together. Preserve usability at browser zoom and with large text.
- Verify narrow, wide, zoomed, and long-content states. Use fixed dimensions only when the user explicitly asks for them or a platform contract requires them.
