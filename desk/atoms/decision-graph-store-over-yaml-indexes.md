---
layer: store
id: decision-graph-store-over-yaml-indexes
title: "Decision: graph store over YAML indexes"
five_wh_one_plus: why
tags:
- system:sldb
- domain:architecture-decisions
provenance: source docs/architecture/target-system-overview.md
---

# Decision: graph store over YAML indexes

## Answer

The refactor moves from a YAML-index-first store to a graph-store-first local `.sldb/` because canonical nodes, typed edges, anchors, and relation payloads need a native persistent graph shape instead of a pile of specialized materializations.

## Supporting points

- YAML indexes worked as inspectable v1 metadata, but they do not scale cleanly to graph-native canonical state.
- The target still preserves rebuildable derived indexes, but those become projections rather than the internal center.
- Keeping the store local preserves the current workspace model while changing the internal representation.

## Related atoms

### Supports

- [supports:: [[graph-store]]]
- [supports:: [[derived-index]]]

### Constrains

- [constrains:: [[what-a-store-is]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
