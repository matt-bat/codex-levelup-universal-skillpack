# Level-Up Codex Skillpack v1.0.0

## Release Date
2026-05-17

## Title
Governance-First Delivery Framework

## Summary
Initial public release of the Level-Up Codex Skillpack, a policy-driven framework for safer and more consistent multi-step software delivery.

## Highlights
- 21 interoperable skills across governance, execution, testing, documentation, and UX workflows.
- Deterministic governance enforcement with startup declaration validation and policy checks.
- Cross-artifact ordering consistency guard between `SKILL-MAP.md` and `docs/skill-index.md`.
- Regression test suite for governance validators.
- Public-facing package metadata:
  - `README.md`
  - `LICENSE`
  - `CHANGELOG.md`
  - `VERSION`

## Included Artifacts
- `skills/README.md`
- `skills/LICENSE`
- `skills/CHANGELOG.md`
- `skills/VERSION`
- `skills/SKILL-MAP.md`
- `skills/docs/skill-index.md`
- `skills/skill-governance/scripts/*`
- `skills/skill-governance/tests/*`

## Validation Evidence
- Skill policy validator: pass
- Skill order sync validator: pass
- Governance unit tests: pass (9 tests)

## License
Attribution-Required Non-Commercial License v1.0.
Use and modification are prohibited without attribution.
Commercial use requires prior written permission.

## Upgrade and Compatibility Notes
- Baseline operation expects startup declaration discipline and governance validators to be part of release readiness checks.
- Any new skill must be reflected in both `SKILL-MAP.md` and `docs/skill-index.md` in the same change.
