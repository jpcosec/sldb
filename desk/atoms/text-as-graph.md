---
layer: shell
id: text-as-graph
title: Text as graph
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-text-structure
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Text as graph

## Answer

Text as graph is the future representation where textual spans and rhetorical or semantic anchor points can become addressable graph units rather than only flat string payloads.

## Supporting points

- This is a forward-looking extension point.
- It should not block AST v1, but the architecture should leave room for it.
- It aligns with future anchor-rich and graph-rich text handling.

## Related atoms

### Depends on

- [depends_on:: [[canonical-ast]]]
- [depends_on:: [[graph-projection]]]

### Supports

- [supports:: [[external-anchor]]]
- [supports:: [[visual-ux-surface]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
