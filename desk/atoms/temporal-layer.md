---
layer: core
id: temporal-layer
title: Temporal layer
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-history
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Temporal layer

## Answer

The temporal layer represents validity windows, revision timing, and time-aware lineage around canonical units.

## Supporting points

- It extends provenance into explicit time semantics.
- It supports reconstruction and historical reasoning.
- It belongs to canonical-adjacent runtime semantics.

## Related atoms

### Depends on

- [depends_on:: [[provenance-record]]]
- [depends_on:: [[append-only-event-log]]]

### Supports

- [supports:: [[snapshots]]]
- [supports:: [[testing]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
