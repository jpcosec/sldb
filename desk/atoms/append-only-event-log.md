---
layer: store
id: append-only-event-log
title: Append-only event log
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-history
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Append-only event log

## Answer

The append-only event log records canonical changes over time as durable system-level history beyond git alone.

## Supporting points

- It tracks what changed, when, and through which transformation path.
- It supports reconstructable lineage and temporal workflows.
- It is a history infrastructure component, not a user-facing projection.

## Related atoms

### Depends on

- [depends_on:: [[provenance-record]]]
- [depends_on:: [[snapshots]]]

### Supports

- [supports:: [[testing]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
