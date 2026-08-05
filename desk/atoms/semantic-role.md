---
layer: shared
id: semantic-role
title: Semantic role
five_wh_one_plus: what
tags:
- system:sldb
- domain:runtime-semantic
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Semantic role

## Answer

A semantic role is the explicit semantic classification of what a canonical unit does or means within a structured semantic view.

## Supporting points

- Roles are finer-grained than generic tags.
- They can support richer semantic navigation later.
- They should not force a broader semantic baseline now.

## Related atoms

### Depends on

- [depends_on:: [[semantic-tag]]]

### Supports

- [supports:: [[concept-binding]]]
- [supports:: [[semantic-reference]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
