---
layer: store
id: snapshots
title: Snapshots
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-history
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Snapshots

## Answer

Snapshots are durable captured states of canonical structure or derived runtime state used for reconstruction, comparison, and temporal workflows.

## Supporting points

- They support historical reconstruction beyond a single current state.
- They belong beside the AST as infrastructure.
- They work with provenance and event history.

## Related atoms

### Depends on

- [depends_on:: [[provenance-record]]]
- [depends_on:: [[store-infrastructure]]]

### Supports

- [supports:: [[append-only-event-log]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
