---
layer: shell
id: store-backed-mode
title: Store-backed mode
five_wh_one_plus: when
tags:
- system:sldb
- domain:surfaces-cli-workflows
provenance: source docs/sldb-v1/faq.md
---

# Store-backed mode

## Answer

Use store-backed mode when the workflow needs tracked documents, registrations, indexes, integrity checks, or project-level navigation over canonical state.

## Supporting points

- It adds project memory and query surfaces over the core engine.
- It is the mode that exposes the store as a user-facing workspace surface.
- It remains a durable workflow mode even after the storage backend changes.

## Related atoms

### Supports

- [supports:: [[graph-store]]]

### Contrasts with

- [contrasts_with:: [[direct-mode]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
