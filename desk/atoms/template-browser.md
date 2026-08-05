---
layer: shell
id: template-browser
title: Template browser
five_wh_one_plus: where
tags:
- system:sldb
- domain:surfaces-visual-inspectors
provenance: source docs/drawer-features/feature-sldb-product-principles-and-cli-continuity.md
---

# Template browser

## Answer

The template browser is the surface that lets users inspect templates and their relationship to fields, nodes, and emitted projections.

## Supporting points

- Templates remain important as user-facing materialization logic.
- They should be inspectable rather than hidden in code.
- They belong to UX and authoring surfaces, not the canonical center.

## Related atoms

### Depends on

- [depends_on:: [[visual-ux-surface]]]
- [depends_on:: [[projection]]]

### Supports

- [supports:: [[structurednldoc-contract]]]
- [supports:: [[draft-first-model-edits]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
