---
layer: shared
id: ownership-edge
title: Ownership edge
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-relations
provenance: source docs/core/reasoning.md
---

# Ownership edge

## Answer

An ownership edge is the structural relation that forms the canonical document tree or DAG and participates in recursive Merkle hashing.

## Supporting points

- Ownership edges define hierarchy and ordered containment.
- Only ownership edges participate directly in structural subtree hashing.
- Non-structural relations must not introduce recursion into the structural Merkle.

## Related atoms

### Depends on

- [depends_on:: [[node]]]
- [depends_on:: [[node-hash]]]

### Supports

- [supports:: [[tree-spine]]]
- [supports:: [[revision]]]
- [supports:: [[stable-selector]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
