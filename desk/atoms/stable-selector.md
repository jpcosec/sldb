---
layer: shared
id: stable-selector
title: Stable Selector
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-addressability
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Stable Selector

## Answer

A stable selector is the durable addressability mechanism for meaningful canonical units.

## Supporting points

- Stable addressability is required for links, graph projection, provenance, and future visual inspection.
- Structural paths, anchors, aliases, and fragments all belong to this addressability domain.
- Canonical units must stay targetable even when materializations or surface views change.
## Related atoms

### Depends on

- [depends_on:: [[canonical-identity]]]
- [depends_on:: [[node]]]
- [depends_on:: [[tree-spine]]]

### Supports

- [supports:: [[link-reference]]]
- [supports:: [[external-anchor]]]
- [supports:: [[semantic-vs-physical-search]]]
- [supports:: [[ast-as-the-debugging-surface]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
