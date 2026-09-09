---
name: advanced-r-and-d
description: Perform source-grounded research before advanced or high-intensity analysis, design, or implementation across any domain. Use when research_intensity is advanced, including niche libraries, unfamiliar APIs, standards-sensitive behavior, consequential recommendations, or work whose correctness depends on current external documentation; do not use for routine tasks fully answered by stable local evidence.
---

# Advanced R&D

## Mission

Build a version-aware evidence base before consequential work so implementation follows current primary sources instead of memory, snippets, or popularity.

## Research Contract

Before searching, define:

1. the decision or implementation the research must support
2. the target versions, platform, runtime, and date boundary
3. the required depth: API surface, behavior, constraints, compatibility, security, performance, or examples
4. what would falsify the leading approach
5. the stopping condition for sufficient evidence

Do not let research broaden task authority. Reading sources does not authorize installation, mutation, scraping behind access controls, account use, publication, or copying licensed material.

## Source Workflow

1. Inspect local manifests, locks, imports, generated API clients, vendored sources, and tests to identify the exact technology and version already in scope.
2. Discover the authoritative project identity through official package metadata, registries, standards bodies, vendor documentation, or the canonical repository.
3. Read primary sources first: versioned official documentation, specifications, source and tests at the relevant tag or commit, release notes, migration guides, and security advisories.
4. Map the necessary surface. For a library, cover the relevant modules, functions, signatures, return types, exceptions, side effects, lifecycle, concurrency model, configuration, and examples. Do not read every API merely to claim completeness.
5. Triangulate claims that are version-sensitive, ambiguous, consequential, or contradicted. Use source code or tests to resolve documentation gaps; label inference explicitly.
6. Record a compact evidence matrix using [Source Strategy](references/source-strategy.md). Use [Technical Research](references/technical-research.md) for libraries, APIs, and standards.
7. Convert findings into implementation constraints, rejected approaches, open questions, and verification steps before coding.
8. Re-check the final design against the source set when implementation reveals a new API, version, or assumption.

## Reliability Rules

1. Prefer the exact version's docs and source over latest-version landing pages.
2. Distinguish normative specification, maintained documentation, implementation behavior, examples, issues, and community commentary.
3. Treat README examples, search snippets, generated summaries, and Q&A as discovery aids until confirmed by stronger sources.
4. Record publication or update dates for time-sensitive material and retrieval dates for mutable pages.
5. Cite the page that directly supports the claim, not a search result or generic project homepage.
6. Quote sparingly; paraphrase and preserve the source's actual scope and caveats.
7. Report contradictions, missing documentation, unsupported claims, and unverified compatibility instead of smoothing them over.
8. Stop when every material decision has sufficient evidence and further searching is unlikely to change execution.

## Output Contract

Before advanced implementation, retain a conversation-local brief containing:

1. scoped question and environment/version identity
2. authoritative sources with direct links or repository paths
3. claim-to-source mappings and confidence
4. constraints, deprecations, security notes, and compatibility boundaries
5. unresolved conflicts or gaps
6. implementation consequences and planned verification

Surface the brief to the user when requested, when research changes the expected approach, or when uncertainty remains material.

## Authority and Artifact Policy

Keep notes conversation-local by default. Create a research brief, source matrix, downloaded corpus, cache, or citation file only when the user requests it or an existing authorized repository contract requires it. Do not install packages, clone repositories, or modify files solely because this skill activated.

## Completion Gates

1. Exact technology, version, and target environment are identified or explicitly unresolved.
2. Material claims trace to suitable primary sources.
3. Relevant API constraints and failure behavior are covered, not just happy-path examples.
4. Source disagreement and inference are labeled.
5. Research has been translated into concrete implementation and validation decisions.
