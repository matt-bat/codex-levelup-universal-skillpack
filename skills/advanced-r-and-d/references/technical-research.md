# Technical Research

## Contents

1. Package identity
2. API coverage
3. Version and compatibility
4. Source and tests
5. Security and provenance
6. Authoritative starting points

## Package Identity

Before relying on documentation, prove that the package, import, repository, and release refer to the same project:

- read the local manifest and lockfile
- inspect the installed distribution metadata when available
- use official registry metadata to find documentation, source, changelog, and issue URLs
- confirm normalized name versus import name
- capture the exact version, tag, commit, runtime, and optional extras

For Python, PyPA's well-known project URL metadata distinguishes documentation, source, changelog, release notes, and issues. Similar official registry metadata should anchor other ecosystems.

## API Coverage

For each relevant symbol, capture:

1. qualified name and import path
2. signature, overloads, generic parameters, and defaults
3. accepted inputs and validation/coercion behavior
4. return type and ownership/lifetime
5. raised errors and partial-failure behavior
6. side effects, I/O, caching, global state, and thread/async safety
7. configuration and environment dependencies
8. deprecation, experimental status, and replacement
9. minimal official example and one boundary case

Build a symbol map only for the reachable surface required by the task. For broad wrappers or migrations, enumerate the complete public surface mechanically from the versioned documentation or exported source rather than relying on memory.

## Version and Compatibility

- Prefer documentation whose version exactly matches the dependency lock.
- Compare migration guides and release notes from the installed version to the target version.
- Separate language/runtime support, operating-system support, optional native dependencies, and framework integrations.
- Check whether examples target a newer major version.
- Record removed behavior and changed defaults explicitly.

## Source and Tests

Use canonical source when public documentation does not answer implementation-sensitive questions. Pin links to a tag or commit. Read tests for executable edge cases, but do not mistake test coverage for a public compatibility promise.

Inspect in this order:

1. public export or interface definition
2. implementation of the relevant path
3. adjacent validation and error definitions
4. focused unit/integration tests
5. changelog or commits that introduced the behavior

## Security and Provenance

- Prefer official security advisories and recognized vulnerability databases.
- Check whether a reported issue affects the exact version and configuration.
- Distinguish a repository commit, source archive, built artifact, and installed artifact.
- Do not execute copied installation commands or unknown scripts as part of research.
- Treat provenance and release signatures as evidence only when verified by the appropriate tooling.

## Authoritative Starting Points

- [Python Packaging User Guide: package metadata](https://packaging.python.org/en/latest/specifications/section-distribution-metadata/)
- [Python Packaging User Guide: well-known project URLs](https://packaging.python.org/en/latest/specifications/well-known-project-urls/)
- [Python documentation](https://docs.python.org/3/)
- [GitHub Docs: repositories and releases](https://docs.github.com/en/repositories)
- [NIST SP 800-204D](https://csrc.nist.gov/pubs/sp/800/204/d/final) for software supply-chain provenance and CI/CD context

Use ecosystem-specific official documentation, registries, standards bodies, and canonical repositories for the actual task. These links illustrate source categories rather than replacing domain research.
