---
layer: core
id: tree-spine
title: Tree Spine
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-ast-core
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Tree Spine

## Answer

The canonical document model keeps a tree spine for ownership and order.

## Supporting points

- Parent/child relationships and sibling order are part of the minimum structural layer.
- Slots or named regions belong to this canonical ownership model.
- The system is graph-capable, but the tree spine remains the core structural backbone.
## Related atoms

### Depends on

- [depends_on:: [[canonical-ast]]]
- [depends_on:: [[document]]]

### Supports

- [supports:: [[node]]]
- [supports:: [[field-and-section-navigation]]]
- [supports:: [[stable-selector]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
