---
layer: shell
id: semantic-edge
title: Semantic edge
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-relations
- domain:runtime-semantic
provenance: source docs/core/reasoning.md
---

# Semantic edge

## Answer

A semantic edge is a derived or logic-informed relation that captures meaning-level connections between canonical units without changing structural ownership.

## Supporting points

- Semantic edges may come from classification, logic, or semantic projection engines.
- They are queryable and explainable, but they are not the primary structural tree.
- Semantic recalculation may be invalidated and rebuilt as engines evolve.

## Related atoms

### Depends on

- [depends_on:: [[projection]]]
- [depends_on:: [[semantic-provider]]]

### Supports

- [supports:: [[semantic-reference]]]
- [supports:: [[semantic-indexing]]]
- [supports:: [[query-engine]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
