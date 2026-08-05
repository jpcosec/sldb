---
layer: shared
id: semantic-export-boundary
title: Semantic export boundary
five_wh_one_plus: why
tags:
- system:sldb
- domain:architecture-boundaries
provenance: source docs/sldb-v1/README.md
---

# Semantic export boundary

## Answer

`stores semantic-export` emits SLDB-owned semantic document truth for graph consumers, while downstream systems add workflow-specific and code-dependency edges.

## Supporting points

- This defines the boundary of what SLDB exports semantically.
- The contract is about ownership of semantic truth, not downstream enrichment.
- The refactor should preserve this boundary even if export internals evolve.

## Related atoms

### Constrains

- [constrains:: [[testing]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
