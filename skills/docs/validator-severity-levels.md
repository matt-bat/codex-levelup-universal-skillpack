# Validator Severity Levels

Use severity levels so validation remains useful without blocking harmless work.

## Levels
1. `error`: blocks commit, merge, or release recommendation
2. `warning`: reported in validation output but does not block by default
3. `advisory`: improvement suggestion for maintenance review

## Error Examples
1. missing required skill in `SKILL-MAP.md`
2. `SKILL-MAP.md` and `docs/skill-index.md` order mismatch
3. invalid governance artifact schema
4. strict gate not `pass` or `waived`
5. missing required `SKILL.md` frontmatter name

## Warning Examples
1. stale `Last Updated UTC` on unchanged docs
2. deprecated skill reference with a valid replacement
3. install profile not mentioning a newly added optional skill
4. examples missing for a non-critical skill

## Advisory Examples
1. style improvements
2. optional extra examples
3. possible consolidation candidates
4. usage review suggestions

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
