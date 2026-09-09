# Quality, Accessibility, and Security

## Contents

1. Alternative-text decision
2. Interaction and animation
3. Theming and readability
4. Security boundary
5. Performance and compatibility
6. Review checklist

## Alternative-Text Decision

Choose by purpose, not appearance:

```svg
<!-- Decorative inline SVG -->
<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24">…</svg>

<!-- Informative image -->
<svg role="img" aria-labelledby="acc-title acc-desc" viewBox="0 0 640 360">
  <title id="acc-title">Quarterly request volume</title>
  <desc id="acc-desc">Requests rose from 1.2 million in Q1 to 2.1 million in Q4.</desc>
  …
</svg>

<!-- Functional control: label the control, not the glyph -->
<button type="button" aria-label="Download report">
  <svg aria-hidden="true" focusable="false" viewBox="0 0 24 24">…</svg>
</button>
```

For charts, maps, and diagrams, provide equivalent data or a long description in adjacent HTML. A `<title>` alone cannot carry a complex graphic's full meaning.

## Interaction and Animation

Prefer native HTML controls around SVG. When SVG elements themselves are interactive, make semantics, focusability, keyboard activation, and visible focus explicit in the host environment.

```css
.acc-pulse { transform-box: fill-box; transform-origin: center; animation: acc-pulse 1.8s ease-in-out infinite; }
@keyframes acc-pulse { 50% { transform: scale(1.06); opacity: .72; } }
@media (prefers-reduced-motion: reduce) { .acc-pulse { animation: none; } }
```

Avoid animation that conveys the only copy of essential state. Avoid rapid flashing and unbounded motion.

## Theming and Readability

```svg
<svg style="--acc-bg:#F8FAFC;--acc-ink:#0F172A;--acc-accent:#2563EB">
  <rect width="100%" height="100%" fill="var(--acc-bg)"/>
  <g fill="var(--acc-ink)" stroke="var(--acc-accent)">…</g>
</svg>
```

- Keep essential labels as live text only when font availability and layout are controlled.
- Convert logo lettering to approved paths when exact outlines are required, but keep a semantic text alternative.
- Verify contrast in every theme and over gradient endpoints, not just the midpoint.
- Do not encode categories by color alone; add labels, shapes, patterns, or direct annotations.

## Security Boundary

SVG is active XML content in many embedding modes. For untrusted or user-supplied SVG, use a proven sanitizer configured for the exact embedding context; validation is not sanitization.

Block or explicitly review:

- `<script>`, `<foreignObject>`, embedded HTML, and animation with unsafe references
- attributes beginning with `on`, such as `onclick`
- `javascript:` or `data:text/html` URLs
- remote `href`, `src`, paint-server, filter, clip, mask, marker, font, or stylesheet references
- external entities and XML processing instructions
- embedded base64 payloads and unexpectedly large path or filter data

Prefer `<img src="…">` for noninteractive untrusted display after sanitization because its browser execution surface is narrower than inline SVG. Confirm the actual platform behavior.

The bundled render harness first rejects active document directives, external CSS imports and URLs, executable elements, handlers, and unresolved references. Its temporary browser document applies a deny-by-default Content Security Policy. Chromium's sandbox remains enabled for normal users; the harness adds `--no-sandbox` automatically only for root-owned containers. The explicit `--chromium-no-sandbox` option is limited to already-isolated trusted CI runners that cannot enable user namespaces. Do not use that option for untrusted SVGs, treat this verifier as a sanitizer, or render untrusted input outside an isolated environment.

## Performance and Compatibility

- Minimize DOM nodes and reuse stable components.
- Avoid enormous filter regions, high-octave turbulence, large animated blurs, and excessive precision.
- Keep a plain fallback for email, PDF, print, server renderers, and sanitizers.
- Verify `context-stroke`, CSS variables, `paint-order`, blend modes, masks, filters, and text metrics against the target matrix before relying on them.
- Do not remove `viewBox` during optimization.
- Preserve `<title>`, `<desc>`, ARIA relationships, IDs, and intentional whitespace when running optimizers.

## Review Checklist

1. The SVG has the intended `viewBox`, aspect-ratio behavior, and smallest-size legibility.
2. DOM order, visual order, and reading order are coherent.
3. IDs are unique after multiple component instances appear on one page.
4. Every reference resolves and every remote reference is authorized.
5. Alternative text matches purpose; complex information has a full equivalent.
6. Interaction has semantics, keyboard operation, visible focus, and a sufficiently large hit target.
7. Motion respects reduced-motion preferences.
8. Filters do not crop and advanced features have a compatibility decision.
9. No unsafe element, event handler, or dangerous URL remains.
10. The file passes XML/reference/accessibility validation and multi-size renderer inspection.
