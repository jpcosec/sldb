---
layer: core
id: link-edge
title: Link edge
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-relations
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Link edge

## Answer

A link edge is the canonical edge type that represents a link relation between ASTs or canonical units.

## Supporting points

- It preserves current link behavior in the new model.
- It is not merely derived from rendered text.
- It belongs to the canonical relation system.

## Related atoms

### Depends on

- [depends_on:: [[link-reference]]]
- [depends_on:: [[relation-ast]]]

### Supports

- [supports:: [[recover-vs-compose]]]
- [supports:: [[graph-projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
