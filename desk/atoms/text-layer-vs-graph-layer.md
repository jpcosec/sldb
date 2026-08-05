---
layer: core
id: text-layer-vs-graph-layer
title: Text layer vs graph layer
five_wh_one_plus: why
tags:
- system:sldb
- domain:architecture-boundaries
provenance: source docs/architecture/sldb-text-layer-vs-kgdb-graph-layer.md
---

# Text layer vs graph layer

## Answer

The text layer and the graph layer are complementary but different system layers: SLDB owns structured authored text and its canonical AST/store behavior, while downstream graph systems own graph-native persistence, traversal, and higher-order reasoning.

## Supporting points

- Authored documents remain canonical human-facing truth and should not be replaced by a graph authoring center.
- Graph-native traversal, equivalence, inference, and global reasoning should not be pulled back into the document layer.
- Composition is primarily text-first even when graph discovery helps choose inputs.
- Export is a projection boundary from SLDB into graph consumers, not a replacement for the canonical authored/document layer.

## Related atoms

### Depends on

- [depends_on:: [[structured-text]]]
- [depends_on:: [[graph-store]]]
- [depends_on:: [[semantic-export-boundary]]]

### Supports

- [supports:: [[semantic-exporter]]]
- [supports:: [[projection]]]
- [supports:: [[text-as-graph]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
