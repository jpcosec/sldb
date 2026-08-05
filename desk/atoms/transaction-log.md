---
layer: store
id: transaction-log
title: Transaction log
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-history
- domain:store-persistence
provenance: source docs/core/diagramas_core.md
---

# Transaction log

## Answer

The transaction log is the append-only persistent record of every committed kernel transaction.

## Supporting points

- Past transactions are never edited in place.
- The log is one of the sources of truth from which indexes, caches, and some projections may be rebuilt.
- Recovery after crash must be defined in terms of replayable committed log entries and consistent revision/head state.

## Related atoms

### Depends on

- [depends_on:: [[transaction]]]
- [depends_on:: [[append-only-event-log]]]

### Supports

- [supports:: [[graph-store]]]
- [supports:: [[store-integrity-checks]]]
- [supports:: [[revision]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
