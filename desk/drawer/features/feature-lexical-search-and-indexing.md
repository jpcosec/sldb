---
id: feature-lexical-search-and-indexing
status: proposed
summary: Define lexical and structural search behavior plus rebuildable search indexes over canonical content.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as post-first-slice macrotask planning feature."
references:
- interfaces.md
- libraries_core.md
- desk/atoms/search-projection.md
- desk/atoms/query-engine.md
- desk/atoms/reference-behavior.md
- docs/architecture/spec2viz/target-store-graph.yml
depends_on:
- feature-rust-kernel-foundation-first-slice
---

# Lexical search and indexing

## Goal

Define the macrotask for exact, lexical, and structural retrieval over canonical content without semantic-provider dependency.

## Includes

- lexical search
- structural search
- rebuildable search indexes
- ranking/explain surface for deterministic search

## Excludes

- embeddings
- LLM-mediated retrieval

## Needs design or grounding before promotion

- exact search modes
- index rebuild triggers
- result explainability
- fixture corpus for search conformance
