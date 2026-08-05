---
id: task-specify-graph-store-contract
status: closed
summary: Re-anchored to high-fidelity contract in docs/architecture/contracts/graph-store-contract.md.
tags:
- workspace:desk
- artifact:task
- system:sldb
history:
- "2026-07-29: closed with high-fidelity contract artifact."
- "2026-08-01: removed legacy SQLite/FTS5 engine mandates from Goal, Implementation Path, and Validation; the delivered contract already reflects the replaceable StorageBackend decision."
references:
- desk/atoms/graph-store.md
- desk/atoms/immutable-append-only-database.md
- desk/atoms/append-only-event-log.md
- desk/atoms/store-infrastructure.md
- desk/atoms/store-integrity-checks.md
- docs/architecture/spec2viz/target-store-graph.yml
- docs/architecture/spec2viz/target-components.yml
depends_on: []
pills:
- desk/contexts/pill-planning-contracts.md
files:
- docs/architecture/contracts/graph-store-contract.md
checklists: []
---

# Specify Graph Store Contract

## Rationale

Anchored in `immutable-append-only-database.md`. The local store is the foundation of system integrity. By mandating an append-only architecture, we ensure that no historical context is ever lost and every node remains uniquely identifiable via its content hash.

## Goal

Define the architecture and integrity requirements for the `.sldb` infrastructure. Mandate a kernel-owned `StorageBackend` boundary with replaceable engines (`redb` default, `CozoDB` alternative) and `Blake3` for content-addressed storage.

## Scope

- **In-Scope**: 
  - `ASTPersistence`, `RelationEdges`, and `AnchorNodes` storage.
  - `DerivedIndexes` (Section, Field, Search, Semantic).
  - `HistoryArtifacts` (Snapshots and provenance).
  - Store integrity check protocols.
- **Out-of-Scope**: 
  - Centralized database orchestration.
  - Phase 2 vector search indexes.

## Implementation Path

1. **Storage Mapping**: Align with `target-store_graph.yml` components.
2. **Indexing Strategy**: Define the `SearchIndex` behind a kernel-owned, replaceable search interface with no fixed engine mandated.
3. **Integrity Rule**: Bind `store-integrity-checks.md` to the validation lifecycle.
4. **Contract Materialization**: Write the specification in `docs/architecture/contracts/graph-store-contract.md`.

## Validation

- Does the contract enforce "Append-Only" immutability?
- Does it keep persistence and indexing behind replaceable kernel-owned interfaces?
- Does it match the `GraphStore` contains list in `target-components.yml`?

## Done When

The high-fidelity `graph-store-contract.md` is committed and approved.

## Normalization note (2026-08-01)

Legacy engine mandates (SQLite/FTS5) were removed from this task's body. Per the core docs (`libraries_core.md`, `interfaces.md`, `core_README.md`) and `desk/atoms/decision-rusqlite-store.md`, persistence sits behind a replaceable kernel-owned `StorageBackend` (`redb` default, `CozoDB` alternative); no fixed engine is mandated. The delivered contract was amended accordingly on 2026-07-31.
