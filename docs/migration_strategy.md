# SLDB Extraction and Modularization Strategy

Historical proposal, predating the 2026-09-07 v1 freeze. These slices are not a statement of implemented packages or an active release commitment. The README names `knowledge` as successor; see [current source layout](architecture/current-source-tree.md) and [remaining gaps](documentation-review.md) for this checkout.

## Overview
This document defines the migration slices, candidate packages, and the strategy to decouple legacy systems from the active tree.

## Migration Slices

### Slice 1: Isolation of Legacy CLI and Deprecated Queries
- **Objective:** Move legacy raw querying logic (`ls`, `get`, `glob`, `find` legacy handlers) and any deprecated CLI components into a dedicated `legacy/` or `compat/` namespace, removing them from the critical path of the new target architecture.
- **Action:** Refactor `sldb.cli.parser` to dynamically load or isolate `_add_legacy_commands` and `_add_hidden_compat_commands` into a module that does not pollute the primary entry points. Long term, these should be removed.

### Slice 2: Extraction of SLDB-Store
- **Objective:** Package the hashing, file layout, and low-level IO operations into an independent, versioned library (`sldb-store`).
- **Action:** 
  1. Define a strict API interface in `sldb.store` that other modules must use.
  2. Remove cyclical dependencies between `sldb.store` and `sldb.runtime` or `sldb.store.semantic`.
  3. Extract `sldb.store.io`, `sldb.store.layout`, and `sldb.store.hashing` into a new package or top-level namespace (`sldb_store`).

### Slice 3: Separation of Query/Semantic Engine
- **Objective:** Separate the in-memory query evaluation and semantic navigation from the store implementation.
- **Action:** Move `sldb.store.query_engine` and related index management into an independent `sldb-query` or `sldb_query` module. It should depend strictly on `sldb-store` for data retrieval and `sldb-core` for structural boundaries, without knowing how files are written to disk.

### Slice 4: CLI Decoupling
- **Objective:** Ensure the CLI is a pure presentation layer.
- **Action:** Extract the remaining `argparse` definitions in `sldb.cli` into a separate package (`sldb-cli`). The CLI should invoke facade services exposed by `sldb.core` and `sldb.query`, rather than calling `load_store_index()` or dealing with IO directly.

## Legacy Handling Strategy
- Remove deprecated features from the active repository tree.
- Rely on `git` history to preserve legacy implementations (e.g. raw DSL query syntax) if ever needed for reference.
- Any temporary compatibility code required during the transition must be isolated in a `compat` module with a clear `DEPRECATION_WARNING` and an expiration date.
