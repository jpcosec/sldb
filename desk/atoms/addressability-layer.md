---
layer: shared
id: addressability-layer
title: Addressability layer
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-addressability
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Addressability layer

## Answer

The addressability layer gives canonical units stable paths, selectors, anchors, aliases, and targetable identities across projections.

## Supporting points

- It is the basis for linking, inspection, graph traversal, and visual targeting.
- It must survive changes in materialization or surface representation.
- It sits close to the canonical structure rather than as a late add-on.

## Related atoms

### Depends on

- [depends_on:: [[canonical-ast]]]
- [depends_on:: [[canonical-identity]]]
- [depends_on:: [[stable-selector]]]

### Supports

- [supports:: [[local-anchor-resolver]]]
- [supports:: [[external-anchor-resolver]]]
- [supports:: [[graph-projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
