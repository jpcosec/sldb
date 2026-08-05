---
layer: core
id: rust-patterns
title: Rust patterns
five_wh_one_plus: how
tags:
- system:sldb
- domain:quality-patterns-rust
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Rust patterns

## Answer

Rust patterns define the reusable implementation shapes for the canonical AST core, graph-capable relations, hashing, and structural invariants.

## Supporting points

- Rust should carry the canonical core and its strongest invariants.
- Patterns here should favor explicit types, graph-friendly modeling, capability layering, and incremental structural operations.
- These patterns should make future AST extension possible without rewriting the core.

## Related atoms

### Depends on

- [depends_on:: [[patterns]]]
- [depends_on:: [[canonical-ast]]]
- [depends_on:: [[tree-spine]]]
- [depends_on:: [[node-hash]]]

### Supports

- [supports:: [[code-linting]]]
- [supports:: [[testing]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
