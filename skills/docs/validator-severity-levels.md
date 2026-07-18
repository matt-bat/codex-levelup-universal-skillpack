# Validator Severity Levels

Use severity levels so validation stays useful without blocking harmless work.

Validators should be strict about things that can break routing, safety, governance evidence, or release claims. They should be lighter about style suggestions and future improvements.

## Levels
1. `error`: blocks commit, merge, or release recommendation
2. `warning`: reported in validation output but does not block by default
3. `advisory`: improvement suggestion for maintenance review

## Error Examples
1. invalid catalog schema, unknown typed relation target, or a cycle in the hard `requires` graph
2. `SKILL-MAP.md`, `docs/skill-index.md`, or `docs/skill-decision-tree.md` differs from catalog-generated output
3. a `SKILL.md` frontmatter name or description diverges from its catalog entry
4. invalid governance artifact schema or change binding
5. a `go` artifact has a pending, failed, waived, or unsupported required gate
6. an exact-head release check or attestation does not match the candidate commit

Errors should represent real breakage or a release-readiness claim that cannot be trusted.

## Warning Examples
1. a new integration uses a deprecated compatibility name with a valid replacement
2. an install profile does not mention a newly added optional skill
3. examples are missing for a non-critical skill
4. operator guidance is accurate but could link the canonical catalog more directly

Warnings should be visible enough to fix, but not so heavy that they block unrelated work.

## Advisory Examples
1. style improvements
2. optional extra examples
3. possible consolidation candidates
4. usage review suggestions

Advisories are useful backlog signals. They should not become release blockers unless they point to a safety or correctness issue.

## Default CI Policy
1. fail on `error`
2. report `warning`
3. skip `advisory` unless a maintenance review requests it

## Promotion Rule
Promote a warning to an error when it can cause:

1. unsafe execution
2. broken governance enforcement
3. missing release evidence
4. incorrect skill routing
5. user instruction tracking loss

The default should be practical: block on trust problems, warn on maintenance drift, and keep nice-to-have ideas out of the critical path.
