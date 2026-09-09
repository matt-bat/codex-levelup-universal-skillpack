# Components and Composition

## Contents

1. Definitions and instances
2. Themeable icon component
3. Connectors and markers
4. Text paths
5. Diagrams and data graphics
6. ID and DOM discipline

## Definitions and Instances

Build reusable parts in `<defs>` and instantiate them with `<use>`:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 180">
  <defs>
    <symbol id="acc-node" viewBox="0 0 120 72">
      <rect x="1.5" y="1.5" width="117" height="69" rx="14"
            fill="var(--node-fill, #EFF6FF)"
            stroke="var(--node-stroke, #2563EB)" stroke-width="3"/>
      <circle cx="24" cy="36" r="8" fill="var(--node-accent, #2563EB)"/>
      <path d="M 44 28 H 96 M 44 44 H 82" stroke="var(--node-ink, #1E293B)"
            stroke-width="5" stroke-linecap="round"/>
    </symbol>
  </defs>
  <use href="#acc-node" x="20" y="54" width="120" height="72"/>
  <use href="#acc-node" x="180" y="54" width="120" height="72"
       style="--node-fill:#F0FDF4;--node-stroke:#16A34A;--node-accent:#16A34A"/>
</svg>
```

Use a `<g id="…">` when instances should inherit the outer coordinate system; use `<symbol viewBox="…">` when the component needs scalable intrinsic coordinates.

## Themeable Icon Component

```svg
<symbol id="acc-icon-spark" viewBox="0 0 24 24">
  <path d="M12 2 14.4 9.6 22 12l-7.6 2.4L12 22l-2.4-7.6L2 12l7.6-2.4Z"
        fill="none" stroke="currentColor" stroke-width="1.75"
        stroke-linecap="round" stroke-linejoin="round"/>
</symbol>
```

Keep icon geometry on a consistent grid and opt into `fill="none"` rather than relying on inherited defaults.

## Connectors and Markers

```svg
<defs>
  <marker id="acc-arrow" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="7" markerHeight="7" orient="auto-start-reverse"
          markerUnits="strokeWidth">
    <path d="M 1 1 L 9 5 L 1 9 Z" fill="context-stroke"/>
  </marker>
</defs>
<path d="M 80 90 C 150 25 250 25 320 90"
      fill="none" stroke="#475569" stroke-width="3"
      marker-end="url(#acc-arrow)"/>
```

If `context-stroke` is outside the compatibility target, set an explicit marker fill or use a CSS variable. Place connectors before nodes so edges appear behind them. Offset endpoints to node boundaries instead of drawing through node centers.

## Text Paths

```svg
<defs>
  <path id="acc-label-arc" d="M 40 140 A 120 120 0 0 1 280 140"/>
</defs>
<text font-family="system-ui, sans-serif" font-size="18" text-anchor="middle">
  <textPath href="#acc-label-arc" startOffset="50%">Observable pipeline</textPath>
</text>
```

Do not use text paths for essential long prose. Browser font metrics and fallback fonts can move glyphs. Provide equivalent accessible text outside a complex diagram.

## Diagrams and Data Graphics

Layer diagrams consistently:

```svg
<g id="acc-grid" aria-hidden="true"><!-- background guides --></g>
<g id="acc-edges" fill="none"><!-- connectors --></g>
<g id="acc-nodes"><!-- semantic objects --></g>
<g id="acc-labels"><!-- labels and annotations --></g>
<g id="acc-overlays"><!-- focus or interaction states --></g>
```

For bar charts, keep data marks as primitives and expose the same data as text or a table:

```svg
<g class="bars" fill="#2563EB">
  <rect x="60" y="110" width="56" height="130"><title>Alpha: 65</title></rect>
  <rect x="148" y="60" width="56" height="180"><title>Beta: 90</title></rect>
  <rect x="236" y="150" width="56" height="90"><title>Gamma: 45</title></rect>
</g>
```

For generated radial series, place one reusable tick with rotation transforms rather than hand-maintaining nearly identical path data.

## ID and DOM Discipline

- Prefix IDs with a component or asset namespace, such as `acc-logo-gradient`.
- Never duplicate IDs when several inline SVGs can share one HTML document.
- Prefer fragment `href="#id"`; add legacy `xlink:href` only when the target requires it.
- Keep `aria-labelledby` IDs namespaced too.
- Do not reference a definition from a separate external SVG unless cross-document behavior is verified in the actual embedding mode.
- Avoid relying on CSS selectors that escape the SVG component boundary.
