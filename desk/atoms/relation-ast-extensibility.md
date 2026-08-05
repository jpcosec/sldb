---
layer: core
id: relation-ast-extensibility
title: RelationAST and extensibility
five_wh_one_plus: how
tags:
- system:sldb
- domain:implementation-rust-core
provenance: source docs/architecture/target-system-overview.md
---

# RelationAST and extensibility

Extensibility resides entirely in the Rust environment. The `RelationASTs` payloads serve as the foundational structure that is materialized and indexed to generate semantic graphs, the store, and tags. This allows extending relationships with strongly typed data structures within Rust.

## Related atoms

### Specializes
- [specializes:: [[relation-ast]]]

### Supports
- [supports:: [[rust-core]]]
