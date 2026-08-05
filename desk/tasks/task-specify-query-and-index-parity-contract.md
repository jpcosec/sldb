---
id: task-specify-query-and-index-parity-contract
status: closed
summary: Re-anchored to high-fidelity contract in docs/architecture/contracts/query-and-index-parity-contract.md.
tags:
- workspace:desk
- artifact:task
- system:sldb
history:
- "2026-07-29: closed with high-fidelity contract artifact."
- "2026-08-01: removed legacy SQLite FTS5 engine mandate from Scope and Validation; the delivered contract already reflects the replaceable search-interface decision."
references:
- desk/atoms/query-engine.md
- desk/atoms/semantic-indexing.md
- desk/atoms/field-index.md
- desk/atoms/section-index.md
- desk/atoms/search-projection.md
- docs/architecture/spec2viz/target-store-graph.yml
- docs/architecture/spec2viz/target-components.yml
depends_on: []
pills:
- desk/contexts/pill-planning-contracts.md
files:
- docs/architecture/contracts/query-and-index-parity-contract.md
checklists: []
---

# Specify Query and Index Parity Contract

## Rationale

Governed by `query-engine.md`. The value of the structural graph is locked behind retrieval. This task ensures that the transition to Rust-backed queries preserves every v1 inspection capability while improving performance via `DerivedIndexes`.

## Goal

Define the Phase 1 retrieval surface and mandatory indexes. Ensure that `stores / models / find` command groups have full structural support in the Rust core.

## Scope

- **In-Scope**: 
  - `SectionIndex`, `FieldIndex`, and `SemanticIndex` (tag-based).
  - `SearchIndex` projection behind a kernel-owned, replaceable search interface.
  - Structural joins across `RelationEdges`.
- **Out-of-Scope**: 
  - `VisualUX` graph explorer queries.
  - LLM-based query expansion or vector embeddings.

## Implementation Path

1. **Projection Strategy**: Map `DerivedIndexes` from `target-store_graph.yml` to the `GraphStore` materialization logic.
2. **Query Surface**: Define the internal Rust API for `find text`, `find links`, and `find refs`.
3. **Performance Floor**: Set point query targets (<10ms) to ensure the system feels "instant."
4. **Contract Materialization**: Write the final specification in `docs/architecture/contracts/query-and-index-parity-contract.md`.

## Validation

- Does the contract keep the search engine replaceable behind a kernel-owned interface?
- Does it cover all 4 derived index types from `target-store_graph.yml`?
- Does it align with the `find` command group in `target-components.yml`?

## Done When

The high-fidelity `query-and-index-parity-contract.md` is committed and approved.

## Normalization note (2026-08-01)

The legacy SQLite FTS5 mandate was removed from this task's body. Per `desk/atoms/decision-search-index-library.md` and `libraries_core.md`, search/index engines are derived, replaceable services behind kernel-owned interfaces. The delivered contract was amended accordingly on 2026-07-31.
