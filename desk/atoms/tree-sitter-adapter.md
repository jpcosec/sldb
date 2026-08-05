---
layer: core
id: tree-sitter-adapter
title: tree-sitter adapter
five_wh_one_plus: how
tags:
- system:sldb
- domain:runtime-adapters
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# tree-sitter adapter

## Answer

The tree-sitter adapter uses syntax-aware parsing or projection for code-facing surfaces without becoming the sovereign model of the system.

## Supporting points

- tree-sitter is useful for code-oriented parsing and projection.
- It should remain downstream of canonical structure.
- It is an adapter for code surfaces, not the main document ontology.

## Related atoms

### Depends on

- [depends_on:: [[projection]]]

### Supports

- [supports:: [[search-projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
