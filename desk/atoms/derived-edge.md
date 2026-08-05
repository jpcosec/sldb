---
layer: shell
id: derived-edge
title: Derived edge
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-relations
- domain:runtime-projections
provenance: source docs/core/reasoning.md
---

# Derived edge

## Answer

A derived edge is a relation that ties canonical state to projection outputs, semantic artifacts, caches, or other rebuildable downstream products.

## Supporting points

- Derived edges express lineage without making derived artifacts primary truth.
- They help explain which revision and which engine produced a downstream result.
- Derived edges are rebuildable from canonical history plus projection specs.

## Related atoms

### Depends on

- [depends_on:: [[projection]]]
- [depends_on:: [[artifact]]]

### Supports

- [supports:: [[projection-edge]]]
- [supports:: [[effect-outbox]]]
- [supports:: [[provenance-record]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
