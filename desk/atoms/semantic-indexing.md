---
layer: store
id: semantic-indexing
title: Semantic indexing
five_wh_one_plus: how
tags:
- system:sldb
- domain:runtime-semantic
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Semantic indexing

## Answer

Semantic indexing is the infrastructure that derives richer retrieval and semantic neighborhood views from canonical structure and related metadata.

## Supporting points

- It should combine explicit structure, tags, links, and later richer semantic layers.
- It is not the canonical model.
- It deepens retrieval and semantic navigation.

## Related atoms

### Depends on

- [depends_on:: [[canonical-ast]]]
- [depends_on:: [[stable-selector]]]
- [depends_on:: [[link-reference]]]

### Supports

- [supports:: [[semantic-vs-physical-search]]]
- [supports:: [[search-projection]]]
- [supports:: [[embeddings]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

### Depends on
- [depends_on:: [[rust-core]]]
