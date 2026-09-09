# Paint and Effects

## Contents

1. Gradients
2. Patterns
3. Clipping and masking
4. Filter pipelines
5. Texture and lighting
6. Effect discipline

## Gradients

Use `gradientUnits="userSpaceOnUse"` when stops should align across multiple objects:

```svg
<defs>
  <linearGradient id="acc-sky" x1="0" y1="0" x2="720" y2="420"
                  gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#0F172A"/>
    <stop offset="0.52" stop-color="#1D4ED8"/>
    <stop offset="1" stop-color="#38BDF8"/>
  </linearGradient>
  <radialGradient id="acc-glow" cx="50%" cy="42%" r="58%">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity=".9"/>
    <stop offset=".45" stop-color="#A5F3FC" stop-opacity=".45"/>
    <stop offset="1" stop-color="#22D3EE" stop-opacity="0"/>
  </radialGradient>
</defs>
<rect width="720" height="420" fill="url(#acc-sky)"/>
<circle cx="540" cy="120" r="150" fill="url(#acc-glow)"/>
```

Use `spreadMethod` deliberately; repeated or reflected gradients can produce banding and large paint costs.

## Patterns

```svg
<defs>
  <pattern id="acc-dot-grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.5" fill="currentColor" opacity=".18"/>
  </pattern>
</defs>
<rect width="100%" height="100%" fill="url(#acc-dot-grid)" color="#475569"/>
```

Use `patternContentUnits="objectBoundingBox"` only when every coordinate and size is intentionally normalized to `0..1`.

## Clipping and Masking

Clips are hard geometry; masks support partial alpha or luminance:

```svg
<defs>
  <clipPath id="acc-avatar-clip"><circle cx="80" cy="80" r="72"/></clipPath>
  <mask id="acc-soft-fade" maskUnits="userSpaceOnUse" x="0" y="0" width="320" height="160">
    <linearGradient id="acc-fade-gradient" x1="0" x2="1">
      <stop offset="0" stop-color="white"/>
      <stop offset=".78" stop-color="white"/>
      <stop offset="1" stop-color="black"/>
    </linearGradient>
    <rect width="320" height="160" fill="url(#acc-fade-gradient)"/>
  </mask>
</defs>
<image href="portrait.jpg" width="160" height="160"
       clip-path="url(#acc-avatar-clip)" preserveAspectRatio="xMidYMid slice"/>
<g mask="url(#acc-soft-fade)"><!-- content --></g>
```

For self-contained or untrusted contexts, replace external images with approved local assets or omit them.

## Filter Pipelines

Name intermediate results and expand the filter region:

```svg
<defs>
  <filter id="acc-elevation" x="-30%" y="-30%" width="160%" height="180%"
          color-interpolation-filters="sRGB">
    <feGaussianBlur in="SourceAlpha" stdDeviation="8" result="blur"/>
    <feOffset in="blur" dx="0" dy="10" result="offset"/>
    <feColorMatrix in="offset" type="matrix"
      values="0 0 0 0 0.02  0 0 0 0 0.06  0 0 0 0 0.14  0 0 0 .26 0"
      result="shadow"/>
    <feMerge>
      <feMergeNode in="shadow"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</defs>
```

For a controlled duotone treatment:

```svg
<filter id="acc-duotone" color-interpolation-filters="sRGB">
  <feColorMatrix type="matrix"
    values=".12 .24 .04 0 .05  .22 .44 .08 0 .10
             .38 .76 .14 0 .16   0   0   0  1  0"/>
</filter>
```

## Texture and Lighting

Use seeded turbulence when reproducibility matters:

```svg
<filter id="acc-paper" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="3"
                seed="17" result="noise"/>
  <feColorMatrix in="noise" type="saturate" values="0" result="gray"/>
  <feComponentTransfer in="gray" result="faint">
    <feFuncA type="table" tableValues="0 .09"/>
  </feComponentTransfer>
  <feBlend in="SourceGraphic" in2="faint" mode="multiply"/>
</filter>
```

Displacement can create organic edges, but apply it to a duplicate or background layer so key contours and text remain crisp:

```svg
<filter id="acc-warp" x="-15%" y="-15%" width="130%" height="130%">
  <feTurbulence type="fractalNoise" baseFrequency=".018 .04" numOctaves="2"
                seed="9" result="field"/>
  <feDisplacementMap in="SourceGraphic" in2="field" scale="14"
                     xChannelSelector="R" yChannelSelector="B"/>
</filter>
```

## Effect Discipline

- Prefer a plain shape plus one purposeful effect to a deep, difficult-to-debug filter graph.
- Keep text outside blur, displacement, and low-contrast masks.
- Test filter regions for cropping at every target scale.
- Verify color expectations: filter primitives commonly operate in linear RGB unless `color-interpolation-filters="sRGB"` is set.
- Treat heavy turbulence, large blurs, animated filters, and large off-screen regions as performance risks.
- Provide an effect-free fallback when the target renderer, PDF pipeline, email client, or sanitizer may remove advanced features.
