---
layer: core
id: rust-testing
title: Rust testing
five_wh_one_plus: how
tags:
- system:sldb
- domain:quality-testing-rust
provenance: source docs/architecture/ritual-testing.md
---

# Rust testing

## Answer

Rust testing validates the unit-level and structural correctness of the canonical AST core and its adjacent infrastructure.

## Supporting points

- It should cover node structure, field binding, links, addressability, hashing, and projection-enabling invariants.
- It is primarily unit and structural-contract oriented.
- It proves that the canonical core behaves correctly before higher-level surfaces consume it.

## Related atoms

### Depends on

- [depends_on:: [[testing]]]
- [depends_on:: [[rust-patterns]]]
- [depends_on:: [[canonical-ast]]]

### Supports

- [supports:: [[node]]]
- [supports:: [[field-binding]]]
- [supports:: [[node-hash]]]
- [supports:: [[projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

### Supports
- [supports:: [[store-integrity-checks]]]
