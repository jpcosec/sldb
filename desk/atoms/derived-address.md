---
layer: shared
id: derived-address
title: Derived address
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-addressability
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Derived address

## Answer

A derived address is a surface-specific or projection-specific address that resolves back to a canonical address.

## Supporting points

- It supports CLI, rendered documents, and visual projections.
- It is not the sovereign identity of the unit.
- It should resolve back to canonical structure.

## Related atoms

### Depends on

- [depends_on:: [[canonical-address]]]
- [depends_on:: [[alias]]]

### Supports

- [supports:: [[stable-selector]]]
- [supports:: [[ast-as-the-debugging-surface]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
