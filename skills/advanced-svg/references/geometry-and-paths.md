# Geometry and Paths

## Contents

1. Coordinate contract
2. Primitive selection
3. Path command patterns
4. Compound and procedural shapes
5. Geometry checks

## Coordinate Contract

Start with one logical coordinate system and make responsiveness a viewport concern:

```svg
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 1200 800"
     preserveAspectRatio="xMidYMid meet"
     role="img" aria-labelledby="scene-title scene-desc">
  <title id="scene-title">System architecture</title>
  <desc id="scene-desc">Three services exchange data through a central event bus.</desc>
  <!-- scene -->
</svg>
```

Use nested `<svg viewBox="…">` elements when a component needs its own coordinate system. Use `vector-effect="non-scaling-stroke"` only when the stroke must stay screen-constant while geometry scales.

## Primitive Selection

Prefer the simplest semantic primitive:

```svg
<g fill="none" stroke="currentColor" stroke-width="3">
  <rect x="20" y="20" width="180" height="96" rx="18"/>
  <circle cx="250" cy="68" r="48"/>
  <ellipse cx="360" cy="68" rx="64" ry="38"/>
  <line x1="440" y1="20" x2="540" y2="116"/>
  <polyline points="570,116 620,20 670,116"/>
  <polygon points="760,20 800,50 785,100 735,100 720,50"/>
</g>
```

Use `<path>` when the contour needs curves, holes, or continuous joins.

## Path Command Patterns

Commands are absolute uppercase or relative lowercase. Keep related segments together and leave meaningful whitespace.

```svg
<!-- Rounded card using quadratic corners -->
<path d="M 30 10 H 210 Q 230 10 230 30 V 130 Q 230 150 210 150
         H 30 Q 10 150 10 130 V 30 Q 10 10 30 10 Z"/>

<!-- Smooth cubic wave; S reflects the preceding control point -->
<path d="M 20 100 C 80 20 140 20 200 100 S 320 180 380 100"
      fill="none" stroke="currentColor"/>

<!-- Quadratic curve followed by a smooth continuation -->
<path d="M 20 120 Q 100 20 180 120 T 340 120"
      fill="none" stroke="currentColor"/>
```

For an elliptical arc, `A rx ry rotation large-arc-flag sweep-flag x y` selects one of four candidates:

```svg
<!-- Semicircular gauge track -->
<path d="M 40 180 A 140 140 0 0 1 320 180"
      pathLength="100" fill="none" stroke="#CBD5E1" stroke-width="24"
      stroke-linecap="round"/>
<path d="M 40 180 A 140 140 0 0 1 320 180"
      pathLength="100" fill="none" stroke="#2563EB" stroke-width="24"
      stroke-linecap="round" stroke-dasharray="73 100"/>
```

Normalize progress paths with `pathLength="100"`; dash values can then use logical path length.

## Compound and Procedural Shapes

Use `fill-rule="evenodd"` for explicit holes:

```svg
<!-- Donut: outer and inner circles encoded as subpaths -->
<path fill-rule="evenodd"
      d="M 100 20 A 80 80 0 1 1 99.999 20 Z
         M 100 65 A 35 35 0 1 0 100.001 65 Z"/>
```

Reusable star with readable polygon points:

```svg
<symbol id="acc-star" viewBox="0 0 100 100">
  <polygon points="50,4 61,36 95,36 68,56 78,90 50,70 22,90 32,56 5,36 39,36"/>
</symbol>
```

Speech bubble composed without boolean tooling:

```svg
<path d="M 28 12 H 212 Q 228 12 228 28 V 116 Q 228 132 212 132
         H 92 L 56 166 L 62 132 H 28 Q 12 132 12 116 V 28 Q 12 12 28 12 Z"/>
```

Isometric face primitives share edges exactly:

```svg
<g stroke="#0F172A" stroke-linejoin="round">
  <polygon points="120,20 220,70 120,120 20,70" fill="#DBEAFE"/>
  <polygon points="20,70 120,120 120,230 20,180" fill="#93C5FD"/>
  <polygon points="120,120 220,70 220,180 120,230" fill="#60A5FA"/>
</g>
```

## Geometry Checks

- Keep critical marks at least one device pixel at the smallest target size.
- Prefer rounded joins for acute generated polygons unless miters are intentional.
- Check whether stroke width expands outside the intended crop.
- Use transforms on groups for repeated positioning; do not pre-distort every child coordinate.
- Keep path precision proportional to the viewBox. Excess decimals add noise without visible fidelity.
- Test arc flags and curve control points visually; syntactically valid paths can still select the wrong contour.
