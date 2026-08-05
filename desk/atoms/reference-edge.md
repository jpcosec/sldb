---
layer: shared
id: reference-edge
title: Reference edge
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-relations
provenance: source docs/core/reasoning.md
---

# Reference edge

## Answer

A reference edge is a non-ownership relation that links canonical units across documents or subgraphs without becoming part of the structural Merkle recursion.

## Supporting points

- References capture links, transclusions, and cross-document targetability.
- Reference cycles must not break hashing because they are outside the ownership recursion.
- Stable addressability and provenance depend on explicit reference semantics.

## Related atoms

### Depends on

- [depends_on:: [[node]]]
- [depends_on:: [[stable-selector]]]

### Supports

- [supports:: [[link-edge]]]
- [supports:: [[external-anchor]]]
- [supports:: [[transclusion-reference]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
