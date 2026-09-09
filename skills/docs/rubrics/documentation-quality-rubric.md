# Documentation Quality Rubric

[Documentation home](../README.md) · [Release readiness](./release-readiness-rubric.md) · [Skillpack quality](./skillpack-quality-rubric.md)

Use this rubric when reviewing public docs or skill docs.

The best docs in this pack should help someone start quickly, understand why the process exists, and know exactly what to update when behavior changes.

| Category | Weight | Checks |
|---|---:|---|
| Accuracy | 25 | paths exist; commands match repo layout; claims match current behavior |
| Completeness | 20 | setup, usage, validation, limitations, and maintenance are covered |
| Clarity | 20 | clear language; obvious starting point; no hidden prerequisites |
| Consistency | 15 | README, usage, map, index, catalog, and examples agree |
| Maintainability | 10 | docs identify canonical sources and update triggers |
| Adoption | 10 | profiles, examples, and adapters support new users |

Score each category from 0 to 5, multiply by weight, then divide by 5.

## Rating Anchors
1. 5: accurate, complete, clear, and easy to follow
2. 4: strong with small gaps or mild repetition
3. 3: usable but missing context or examples
4. 2: hard to follow or partly stale
5. 1: mostly incomplete
6. 0: misleading or broken

## Blocking Conditions
1. broken canonical link
2. command points to the wrong skills root
3. skill count differs across docs
4. governance requirements conflict across files

When a blocking condition appears, fix that before polishing language.
