---
layer: store
id: decision-search-index-library
title: Decision search and semantic indexes are replaceable
five_wh_one_plus: why
tags:
- system:sldb
- domain:architecture-decisions
provenance: source docs/core/libraries_core.md
---

# Decision search and semantic indexes are replaceable

## Answer

Search and semantic indexing are derived services behind kernel-controlled interfaces rather than fixed primary technologies.

## Supporting points

- Lexical search, embeddings, and logic facts are derived from canonical revisions and can be rebuilt.
- Backend choice may differ by phase: redb plus custom indexes, Cozo-backed query facilities, or other replaceable engines.
- Index technology must not leak into node identity, transaction semantics, or revision compatibility.

## Related atoms

### Supports

- [supports:: [[semantic-indexing]]]
- [supports:: [[search-projection]]]
- [supports:: [[query-engine]]]

### Constrains

- [constrains:: [[graph-store]]]
- [constrains:: [[projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
