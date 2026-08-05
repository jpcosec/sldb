---
layer: shell
id: embeddings
title: Embeddings
five_wh_one_plus: what
tags:
- system:sldb
- domain:runtime-semantic
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Embeddings

## Answer

Embeddings are optional semantic vector materializations derived from canonical units to support fuzzy retrieval and related-node discovery.

## Supporting points

- Embeddings complement explicit structure rather than replacing it.
- They may attach to documents, sections, fields, or anchor contexts.
- They are a semantic side layer, not the source of truth.

## Related atoms

### Depends on

- [depends_on:: [[semantic-indexing]]]

### Supports

- [supports:: [[search-projection]]]
- [supports:: [[visual-ux-surface]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
