# Documentation Validation

## Cross-Surface Checks

1. README and quick-start commands match detailed operational documentation.
2. API, schema, configuration, and environment names match implementation.
3. Routing maps, catalogs, generated views, and skill frontmatter agree.
4. Migration and rollback instructions describe the same supported states.
5. Release notes describe the exact release snapshot, not a different historical state.

## New Document Gate

Create a document only when all are true:

1. the information is required by the current task
2. no existing canonical document can own it cleanly
3. the audience and maintenance owner are clear
4. related indexes or navigation can be updated without duplication

## Historical Evidence

Treat dated governance artifacts, release attestations, field notes, and completed task evidence as immutable snapshots. Correct later understanding through an addendum, alias manifest, superseding record, or new release note.
