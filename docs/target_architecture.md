# SLDB Target Modular Architecture

Historical design proposal, predating the 2026-09-07 v1 freeze. Package boundaries below are candidates, not separately shipped components in this checkout. Use the [current source map](architecture/current-source-tree.md) for implemented structure.

## Bounded Contexts

Based on the current monolithic structure of SLDB, we propose splitting it into the following bounded contexts:

1. **Document Core (SLDB-Core)**
   - **Scope:** AST node definitions, YAML/Python handlers, templating engine, and base markdown extraction logic.
   - **Responsibility:** Ingest text into AST representations, render AST representations into text.

2. **Runtime Binding & Validation (SLDB-Runtime)**
   - **Scope:** Pydantic model integration, `StructuredNLDoc` definition, configuration logic.
   - **Responsibility:** Validating that document semantics map correctly to structured schema definitions.

3. **Store & Hashing (SLDB-Store)**
   - **Scope:** Hashing, file layout logic, diagnostics, import/export logic.
   - **Responsibility:** Maintaining the integrity, indexing, and on-disk representation of the document store. This is a prime candidate for a completely independent library.

4. **Query & Semantic Engine (SLDB-Query)**
   - **Scope:** Query parsers, semantic traversal algorithms (globbing, find, filtering), and global semantic index maintenance.
   - **Responsibility:** Interpreting and resolving addresses (`st.*`, `se.*`) and queries into physical document paths.

5. **Links & Transclusion (SLDB-Links)**
   - **Scope:** Composition routines and link resolution logic.
   - **Responsibility:** Reconstructing documents from nested transclusions and managing cross-document pointer integrity.

6. **CLI Surface (SLDB-CLI)**
   - **Scope:** The `argparse` frontend, entrypoints, and command implementations.
   - **Responsibility:** Exposing operations to users, parsing arguments, and marshaling outputs to stdout.

## Contracts Between Components

- **Core <-> Runtime:** The `Core` provides unstructured or lightly structured AST dicts. The `Runtime` translates these into strongly-typed Pydantic schemas.
- **Store <-> Query:** `Store` provides base indexing maps (Document Index, Model Index). `Query` builds structural and semantic graphs using these index snapshots without interacting directly with file I/O operations whenever possible.
- **CLI <-> All:** The CLI should act as a pure presentation layer. It must not handle business logic (like manual tree rebuilding or hashing steps), delegating entirely to facade functions exposed by other bounded contexts.

## Criteria for Extraction

To extract a subsystem (like the `store`), the following conditions must be met:
1. **No Circular Dependencies:** The subsystem cannot import from the broader SLDB application.
2. **Abstract Interface:** Integration points (like index access) should be defined via explicit contracts/protocols.
3. **Standalone Testing:** The subsystem must have its own isolated test suite that does not rely on a global SLDB setup.
