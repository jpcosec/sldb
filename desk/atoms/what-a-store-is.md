---
layer: store
id: what-a-store-is
title: What a store is
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-graph
provenance: source docs/sldb-v1/faq.md
---

# What a store is

## Answer

A store is SLDB's metadata workspace for models, tracked docs, integrity, and indexes; it does not replace Markdown files or become the text source of truth.

## Supporting points

- The store holds metadata about documents rather than the documents themselves.
- The store is part of the workflow experience but not the canonical text layer.
- This external contract should survive even if store internals change.

## Related atoms

### Constrains

- [constrains:: [[direct-mode-vs-store-backed-mode]]]
- [constrains:: [[semantic-export-boundary]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
