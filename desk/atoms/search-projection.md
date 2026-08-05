---
layer: core
id: search-projection
title: Search projection
five_wh_one_plus: how
tags:
- system:sldb
- domain:store-indexes
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Search projection

## Answer

Search projection derives retrieval-oriented views from canonical structure, selectors, and semantic indexing layers.

## Supporting points

- It serves search and discovery rather than canonical persistence.
- It can combine structural, semantic, and vectorial signals.
- It should remain a derived view over canonical content.

## Related atoms

### Depends on

- [depends_on:: [[projection]]]
- [depends_on:: [[semantic-indexing]]]

### Supports

- [supports:: [[semantic-vs-physical-search]]]
- [supports:: [[how-to-get-data-out-of-sldb]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
