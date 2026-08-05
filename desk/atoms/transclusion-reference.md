---
layer: core
id: transclusion-reference
title: Transclusion Reference
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-relations
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Transclusion Reference

## Answer

A transclusion reference is a canonical relation that composes content by reference.

## Supporting points

- Transclusions are explicitly part of what the AST must represent.
- They are distinct from ordinary links because they affect composition and downstream materialization.
- Treating transclusions as first-class relations keeps composition logic inspectable and graph-friendly.

## Related atoms

### Specializes

- [specializes:: [[link-reference]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
