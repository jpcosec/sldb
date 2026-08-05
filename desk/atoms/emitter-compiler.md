---
layer: core
id: emitter-compiler
title: Emitter / compiler
five_wh_one_plus: how
tags:
- system:sldb
- domain:pipeline-emitters
provenance: source docs/drawer-features/feature-sldb-explicit-target-architecture.md
---

# Emitter / compiler

## Answer

An emitter or compiler projects canonical AST structure outward into Markdown, code, text, config, or other derived forms.

## Supporting points

- Emitters turn canonical structure into user-facing outputs.
- They are projection machinery, not the canonical substrate.
- They should remain separable from importers.

## Related atoms

### Depends on

- [depends_on:: [[canonical-ast]]]
- [depends_on:: [[projection]]]

### Supports

- [supports:: [[markdown-emitter]]]
- [supports:: [[graph-projection]]]
- [supports:: [[search-projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
