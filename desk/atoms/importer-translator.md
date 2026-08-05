---
layer: core
id: importer-translator
title: Importer / translator
five_wh_one_plus: how
tags:
- system:sldb
- domain:pipeline-importers
provenance: source docs/drawer-features/feature-sldb-explicit-target-architecture.md
---

# Importer / translator

## Answer

An importer or translator converts an external representation into canonical AST structure.

## Supporting points

- Importers are how external formats enter the system.
- They are not the source of truth.
- They should be separable from emitters and projections.

## Related atoms

### Depends on

- [depends_on:: [[canonical-ast]]]

### Supports

- [supports:: [[markdown-importer]]]
- [supports:: [[semantic-indexing]]]
- [supports:: [[external-anchor]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
