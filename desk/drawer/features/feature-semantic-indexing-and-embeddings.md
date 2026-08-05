---
id: feature-semantic-indexing-and-embeddings
status: proposed
summary: Define optional semantic indexing, embeddings, provider boundaries, and rebuild policy as non-authoritative derived artifacts after the first slice.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as deferred macrotask planning feature."
references:
- plan_core.md
- libraries_core.md
- desk/atoms/embeddings.md
- desk/atoms/semantic-provider.md
- desk/atoms/semantic-indexing.md
- docs/architecture/spec2viz/target-components.yml
- docs/architecture/spec2viz/target-runtime.yml
- docs/architecture/spec2viz/target-store-graph.yml
depends_on:
- feature-lexical-search-and-indexing
---

# Semantic indexing and embeddings

## Goal

Define the deferred macrotask for semantic retrieval artifacts without compromising canonical authority or first-slice scope control.

## Includes

- embeddings as derived artifacts
- vector/semantic index boundary
- provider adapter boundary
- rebuild and invalidation policy
- explicit non-authority guarantees

## Excludes

- treating semantic scores as truth
- sneaking embeddings into the first slice

## Needs design or grounding before promotion

- local vs remote provider policy
- storage format for semantic indexes
- rebuild cost and scheduling
- explainability and confidence policy
