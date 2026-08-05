---
layer: shell
id: graph-projection
title: Graph projection
five_wh_one_plus: how
tags:
- system:sldb
- domain:runtime-projections
provenance: source docs/drawer-features/feature-sldb-explicit-target-architecture.md
---

# Graph projection

## Answer

Graph projection derives graph-shaped views from canonical nodes, links, anchors, provenance, and semantic relations.

## Supporting points

- Graphs are downstream views, not the canonical store.
- This component makes relation-heavy exploration and export possible.
- It should sit cleanly on top of canonical structure.

## Related atoms

### Depends on

- [depends_on:: [[projection]]]
- [depends_on:: [[link-reference]]]
- [depends_on:: [[provenance-record]]]

### Supports

- [supports:: [[visual-ux-surface]]]
- [supports:: [[semantic-export-boundary]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
