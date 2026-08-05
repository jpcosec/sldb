---
layer: store
id: local-vs-global-store-precedence
title: Local vs global store precedence
five_wh_one_plus: where
tags:
- system:sldb
- domain:store-graph
provenance: source docs/sldb-v1/faq.md
---

# Local vs global store precedence

## Answer

A project-local `.sldb/` is the normal workflow location; a global `~/.sldb/` may also exist, and the local store wins when both are present.

## Supporting points

- The docs present local-first precedence as part of normal usage.
- This behavior affects how store-based commands resolve context.
- Users can rely on project-local state taking priority.
## Related atoms

### Depends on

- [depends_on:: [[what-a-store-is]]]

### Supports

- [supports:: [[direct-mode-vs-store-backed-mode]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
