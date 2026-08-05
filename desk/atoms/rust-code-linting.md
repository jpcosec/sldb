---
layer: core
id: rust-code-linting
title: Rust code linting
five_wh_one_plus: how
tags:
- system:sldb
- domain:quality-clean-code-rust
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Rust code linting

## Answer

Rust code linting keeps the canonical core explicit, typed, modular, and free of accidental complexity.

## Supporting points

- It should enforce strong naming, small modules, explicit invariants, and disciplined graph or AST boundaries.
- It should prevent ad hoc feature accretion inside the core data model.
- It is a clean-code dimension specialized for the Rust substrate.

## Related atoms

### Depends on

- [depends_on:: [[code-linting]]]
- [depends_on:: [[rust-patterns]]]

### Constrains

- [constrains:: [[canonical-ast]]]
- [constrains:: [[field-binding]]]
- [constrains:: [[projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
