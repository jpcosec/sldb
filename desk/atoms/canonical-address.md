---
layer: shared
id: canonical-address
title: Canonical address
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-addressability
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Canonical address

## Answer

A canonical address is the primary stable address of a canonical unit inside the AST and graph store.

## Supporting points

- It identifies the unit from the system’s point of view.
- It is stronger than a surface-specific locator.
- It should remain valid across projections.

## Related atoms

### Depends on

- [depends_on:: [[canonical-identity]]]
- [depends_on:: [[addressability-layer]]]

### Supports

- [supports:: [[derived-address]]]
- [supports:: [[stable-selector]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
