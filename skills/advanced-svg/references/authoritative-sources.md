# Authoritative SVG Sources

Use these sources to resolve behavior and feature details. Record the document status and retrieval date when a compatibility or conformance decision depends on them.

## Core Language

- [SVG 2](https://www.w3.org/TR/SVG2/): language, structure, rendering, geometry, paths, text, paint, reuse, and DOM behavior.
- [SVG 2 paths](https://www.w3.org/TR/SVG2/paths.html): path grammar, commands, directionality, and distance computations.
- [SVG 2 paint servers](https://www.w3.org/TR/SVG2/pservers.html): gradients and patterns.
- [SVG 2 text](https://www.w3.org/TR/SVG2/text.html): text layout and `textPath`.
- [SVG 2 rendering model](https://www.w3.org/TR/SVG2/render.html): rendered, non-rendered, and reused content.

## Effects and Composition

- [Filter Effects Module Level 1](https://www.w3.org/TR/filter-effects-1/): filter graph model, primitives, color space, regions, security, and privacy.
- [CSS Masking Module Level 1](https://www.w3.org/TR/css-masking-1/): clipping, masking, compositing, and coordinate behavior.
- [SVG Markers](https://www.w3.org/TR/svg-markers/): marker placement and proposed advanced marker capabilities. Check feature status and target support because this document is a working draft.

## Accessibility

- [W3C WAI Images Tutorial](https://www.w3.org/WAI/tutorials/images/): decorative, informative, functional, text, and complex-image alternatives.
- [WAI complex-image guidance](https://www.w3.org/WAI/tutorials/images/complex/): equivalent descriptions for charts, diagrams, and other information-rich graphics.
- [SVG Accessibility API Mappings](https://www.w3.org/TR/svg-aam-1.0/): how SVG semantics map to accessibility APIs. Check the current draft status.

## Rendering and Visual Verification

- [Chrome Headless mode](https://developer.chrome.com/docs/chromium/headless): browser-native unattended screenshots and viewport sizing.
- [Playwright screenshots](https://playwright.dev/python/docs/screenshots): deterministic page and element screenshot APIs when an embedding application already uses Playwright.
- [librsvg development documentation](https://gnome.pages.gitlab.gnome.org/librsvg/devel-docs/): independent SVG rendering through the `rsvg-convert` command-line product.
- [GitHub-hosted runner images](https://github.com/actions/runner-images): current runner software inventory; verify the actual job image because browser versions are mutable.

## Source-Use Rules

1. Prefer a stable W3C Recommendation or Candidate Recommendation for normative behavior.
2. Treat editor drafts and working drafts as provisional; do not present proposed features as broadly supported.
3. Verify implementation support in the actual target browsers or renderers when a spec is newer than deployed behavior.
4. Use examples in this skill as construction patterns, not as proof of browser support.
5. Do not copy third-party artwork or branded geometry without license and authorization.
6. Treat cross-renderer pixel comparison as regression evidence, not proof that every browser, assistive technology, or embedding context behaves identically.
