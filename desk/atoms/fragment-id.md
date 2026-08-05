---
layer: shared
id: fragment-id
title: Fragment id
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-addressability
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Fragment id

## Answer

A fragment id is a stable fragment-level address token for a meaningful canonical unit inside a document or projection space.

## Supporting points

- It gives fine-grained targeting beyond whole-document identity.
- It should survive through stable structural conventions where possible.
- It belongs to the canonical addressability layer.

## Related atoms

### Depends on

- [depends_on:: [[addressability-layer]]]

### Supports

- [supports:: [[stable-selector]]]
- [supports:: [[local-anchor]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
