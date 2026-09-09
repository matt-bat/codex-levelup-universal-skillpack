# Source Strategy

## Contents

1. Source hierarchy
2. Evidence matrix
3. Triangulation
4. Search and stopping rules

## Source Hierarchy

Rank sources by fitness for the claim, not by a universal prestige score:

1. Normative standard, official specification, statute, regulator, or vendor contract for what behavior is required.
2. Versioned official documentation for supported public behavior.
3. Canonical source code and tests at the exact tag or commit for implemented behavior.
4. Official release notes, migration guides, changelogs, advisories, and package metadata for version boundaries.
5. Maintainer issue or discussion for acknowledged gaps and intent, with status and date preserved.
6. Peer-reviewed primary research or authoritative institutional data for empirical claims.
7. High-quality secondary synthesis for context and terminology.
8. Community posts, examples, Q&A, and search snippets only for discovery or clearly labeled anecdotal evidence.

An implementation can contradict its specification; a source repository can differ from a released artifact; latest docs can differ from the installed version. Record which question each source actually answers.

## Evidence Matrix

Use a compact table during research:

| Claim or decision | Required evidence | Source and version | Direct support | Confidence | Consequence |
|---|---|---|---|---|---|
| Function accepts async callback | Public API contract | Official v3.2 API page | signature + lifecycle section | high | use async handler |
| Cancellation closes transport | Runtime behavior | v3.2 source + test | cleanup branch and test | high | no manual close |
| Windows support is experimental | Compatibility status | v3.2 release notes | explicit platform caveat | high | gate production use |

Do not write a matrix merely for ceremony. Use it when several sources or consequential claims must stay aligned.

## Triangulation

Triangulate when:

- the claim affects security, data, compatibility, money, or irreversible behavior
- official docs are unversioned, incomplete, or contradicted
- an issue describes behavior not present in a release
- source and installed artifacts may differ
- a recommendation depends on benchmarks or platform conditions

Resolve in this order:

1. confirm identity and version
2. inspect normative/public contract
3. inspect implementation and tests
4. inspect release history and known issues
5. reproduce locally when authorized and proportionate

Label a conclusion as inference when no source states it directly.

## Search and Stopping Rules

Construct queries from exact identifiers: package name, qualified symbol, version, error text, standard section, platform, or release tag. Search within official domains or canonical repositories before broad web search.

Stop when:

1. every material implementation decision has a direct source or a labeled evidence gap
2. relevant constraints, failure modes, and version boundaries are known
3. contradictory evidence is resolved or surfaced
4. another search is unlikely to change the plan

Do not confuse exhaustive browsing with complete understanding.
