---
layer: core
id: prosemirror-adapter
title: ProseMirror adapter
five_wh_one_plus: how
tags:
- system:sldb
- domain:runtime-adapters
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# ProseMirror adapter

## Answer

The ProseMirror adapter projects canonical structure into an editing-oriented structured document model for rich visual interaction.

## Supporting points

- ProseMirror is useful as a projection and editing substrate.
- It is not the canonical AST or the main store.
- It should sit downstream of canonical structure.

## Related atoms

### Depends on

- [depends_on:: [[visual-ux-surface]]]
- [depends_on:: [[projection]]]

### Supports

- [supports:: [[model-browser]]]
- [supports:: [[template-browser]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
