# Query and Index Parity Contract

## Purpose and governing sources

This contract defines the retrieval and indexing surface for Phase 1, ensuring parity with v1 search and inspection capabilities.

Governing sources:
- `desk/atoms/query-engine.md`
- `desk/atoms/semantic-indexing.md`
- `desk/atoms/field-index.md`
- `desk/atoms/section-index.md`
- `desk/atoms/search-projection.md`

## Indexing Architecture

### 1. Structural Indexing
- **Sections**: Indexing of all headings and document containers for hierarchical navigation.
- **Fields**: Indexing of all `key: value` pairs found in frontmatter or document bodies.
- **Links**: Indexing of all cross-references (internal and external).

### 2. Full-Text Search (FTS)
- **Engine**: replaceable, behind a kernel-owned search interface (`desk/atoms/decision-search-index-library.md`); no fixed engine is mandated. Candidates per `libraries_core.md`: redb-backed custom indexes, CozoDB query facilities, or an embedded FTS engine chosen at implementation time.
- **Scope**: Indexing of all text content, mapped back to Canonical AST nodes.

## Query Capabilities

- **Find by Path**: Retrieval of nodes by their document path and selector.
- **Find by Metadata**: Retrieval of documents/fragments by field values.
- **Find by Relation**: Retrieval of nodes connected by specific link types (e.g., "all tasks blocking X").

## Strict Phase 1 Constraints

- **No Vector Search**: Implementation of LLM-based semantic search is explicitly out of scope.
- **Local Only**: Queries must execute against the local `.sldb` store without external dependencies.
- **Parity Floor**: Any query possible in the legacy Python implementation must be possible (and faster) in the Rust-core implementation.

## Performance Invariants
- **Point Queries**: < 10ms.
- **Complex Joins**: < 100ms for projects < 50k edges.
