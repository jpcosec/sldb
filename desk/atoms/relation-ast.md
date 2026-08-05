---
layer: core
id: relation-ast
title: Relation AST
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-relations
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Relation AST

## Answer

A relation AST is the structured payload carried by a canonical relation so relations can evolve as extensible first-class entities.

## Supporting points

- Relations are not just thin pointers.
- This makes edge types extensible without inflating the base tree.
- It is key to the graph-native store design.

## Related atoms

### Depends on

- [depends_on:: [[graph-store]]]
- [depends_on:: [[link-edge]]]
- [depends_on:: [[store-edge]]]

### Supports

- [supports:: [[dependency-edge]]]
- [supports:: [[projection-edge]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
