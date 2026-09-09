# Pruning Policy

[Documentation home](./README.md) · [Maturity model](./maturity-model.md) · [Field notes](./field-notes.md)

Use this policy to prevent uncontrolled skillpack growth. A new skill should earn its place by making future work clearer, safer, or easier to validate.

## Rule For New Skills
Every new skill must satisfy at least one condition:

1. replace repeated manual behavior
2. remove complexity elsewhere
3. add enforceable safety or quality value
4. create a clear lifecycle path for existing docs or skills

If none apply, add an example, rubric, field note, or documentation section instead of a new skill.

## Merge Criteria
Merge skills when:

1. they share the same trigger
2. they produce the same artifact
3. one skill is only a checklist inside another skill
4. users cannot explain the difference after reading the decision tree

Merging is not a downgrade. It is often the right way to keep the pack usable.

## Deprecation Criteria
Deprecate a skill when:

1. it is rarely used across field notes
2. another skill covers its work more clearly
3. it causes repeated over-process
4. it has no unique output contract
5. it cannot be validated or evidenced

Deprecation should include a replacement path so users are not left guessing.

## Removal Criteria
Remove deprecated items only when:

1. replacement docs exist
2. references are updated
3. changelog records the removal
4. canonical `skill-catalog.json` records the intended lifecycle and replacement state
5. `SKILL-MAP.md`, `docs/skill-index.md`, and `docs/skill-decision-tree.md` are regenerated from the catalog
6. validators pass

Removal is safest when the replacement has already been used successfully.

## Validator Policy
1. block on drift that breaks routing, catalog integrity, governance artifacts, or safety gates
2. warn on stale examples, adapter gaps, or profile incompleteness
3. keep advisory recommendations out of release-blocking CI unless they affect safety

Validators should protect the pack from real drift. They should not turn every maintenance suggestion into a release blocker.

## Review Cadence
1. review pruning candidates before major releases
2. review field notes after every 10 meaningful tasks
3. avoid adding more than three skills between usage reviews

The pack should grow from repeated evidence, not from every one-off idea.
