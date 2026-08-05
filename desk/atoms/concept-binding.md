---
layer: shared
id: concept-binding
title: Concept binding
five_wh_one_plus: what
tags:
- system:sldb
- domain:runtime-semantic
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Concept binding

## Answer

A concept binding connects a canonical unit to an explicit semantic concept in a structured semantic layer.

## Supporting points

- It is a richer semantic relation than a loose tag.
- It may support future semantic integrations.
- It remains secondary to the current explicit-tag baseline.

## Related atoms

### Depends on

- [depends_on:: [[semantic-role]]]

### Supports

- [supports:: [[semantic-reference]]]
- [supports:: [[semantic-query-hint]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
