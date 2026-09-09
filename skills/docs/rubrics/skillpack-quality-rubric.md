# Skillpack Quality Rubric

[Documentation home](../README.md) · [Documentation quality](./documentation-quality-rubric.md) · [Release readiness](./release-readiness-rubric.md)

Use this rubric when evaluating the whole skillpack.

This is meant to rate the pack as a working system, not just a collection of nice-sounding instructions. A high score should mean the skills are useful, coherent, enforceable, and practical to maintain.

| Category | Weight | Checks |
|---|---:|---|
| Coverage | 15 | needed workflows exist; missing skill gaps are explicit; install profiles cover common use |
| Cohesion | 15 | map, index, catalog, and examples agree; conflict ownership is clear |
| Restraint | 15 | process budget rules exist; anti-overuse rules are enforced; small tasks stay small |
| Enforceability | 15 | validators cover routing, artifacts, catalog, and required sections |
| Documentation | 15 | README, usage, examples, adapters, and limitations are clear |
| Safety | 15 | local-first, approval, rollback, and governance gates are explicit |
| Maintainability | 10 | deprecation, usage review, and contribution paths are defined |

Score each category from 0 to 5, multiply by weight, then divide by 5.

## Rating Anchors
1. 5: robust, enforced, documented, and easy to apply
2. 4: strong with minor operational gaps
3. 3: usable but partly manual
4. 2: inconsistent or under-documented
5. 1: mostly absent
6. 0: broken or actively harmful

## Review Notes
Give the score with evidence. If something is not at 5, name the gap and the next improvement that would close it.

## Perfect-Score Gate

A 100/100 rating requires every category to earn 5 and all applicable evidence below to pass:

1. startup and user-command behavior has executable host conformance tests, not prose alone
2. non-trivial visual generators have a real renderer check at representative sizes, with two independent engines for compatibility-sensitive claims
3. routing, schemas, generated views, governance bindings, and full regression tests pass on the exact candidate
4. the latest controlled-growth threshold has a recorded usage review and disposition
5. known limitations distinguish irreducible platform or model boundaries from missing repository controls

Do not award 100 while an applicable check is skipped, blocked, stale, or supported only by an intended future workflow.
