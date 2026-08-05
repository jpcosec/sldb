# Graph Store Contract

## Purpose and governing sources

This contract defines the persistence layer requirements for the SLDB local graph store.

Governing sources:
- `desk/atoms/graph-store.md`
- `desk/atoms/immutable-append-only-database.md`
- `desk/atoms/append-only-event-log.md`
- `desk/atoms/store-infrastructure.md`
- `desk/atoms/store-integrity-checks.md`
- `desk/atoms/storage-backend.md`
- `desk/atoms/decision-rusqlite-store.md`
- `desk/atoms/decision-search-index-library.md`
- `core_README.md` (Persistencia)
- `interfaces.md` (`StorageBackend`)
- `libraries_core.md`
- `docs/architecture/spec2viz/target-store-graph.yml`

## Storage Architecture

### 1. Append-Only Persistence
- **Immutability**: Once a node or edge is committed to the store, it is never modified.
- **Versioning**: Changes to documents result in new nodes/edges being appended, with the history preserved via a Merkle-like event log or sequential snapshots.

### 2. Local Infrastructure (`.sldb`)
- **Location**: A hidden directory `.sldb` at the project root.
- **Authoritative components** (the source of truth, per `core_README.md`):
  - `Transaction Log`: append-only record of all transactions; a committed transaction is never modified.
  - `Revision Store`: immutable revisions with parents, producing transaction, and root hash.
  - `Content-Addressed Store`: `hash -> content` payloads, enabling deduplication and integrity verification.
  - `Document Heads`: per-document pointer to the current revision, updated via compare-and-swap.
- **Derived, rebuildable components** (never authoritative): structural, field, and search indexes, caches, and projections.
- **Backend**: all persistence sits behind the kernel-owned `StorageBackend` interface (`desk/atoms/storage-backend.md`, `desk/atoms/decision-rusqlite-store.md`). `redb` is the default embedded backend and `CozoDB` a valid alternative (`libraries_core.md`, `interfaces.md`). No specific engine — including SQLite/FTS5 — is mandated; index technology is replaceable (`desk/atoms/decision-search-index-library.md`).

## Data Integrity

- **Hash-Addressing**: Nodes are indexed by their Blake3 hashes.
- **Reference Integrity**: The store must prevent or detect dangling edges where the target node hash is missing from the store.
- **Atomic Commits**: Bulk imports (e.g., tracking a new document) must be atomic.

## Parity Obligations

Phase 1 storage is complete when it can:
- Persist the entire structural graph of a v1 project.
- Reconstruct any historical version of a document from the append-only log.
- Perform integrity checks (`sldb stores check`) to verify that all hashes match their content.

## Performance Requirements
- **Insert**: O(Log N) or better.
- **Query**: Indexed retrieval of any node by Hash or Path in < 50ms for projects < 10k nodes.
