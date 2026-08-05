---
layer: store
id: store-recovery
title: Store recovery
five_wh_one_plus: how
tags:
- system:sldb
- domain:store-graph
- domain:quality-reliability
provenance: source docs/core/also_core.md
---

# Store recovery

## Answer

Store recovery is the set of replay, verify, rebuild, restore, and repair flows used to return the repository to a trustworthy state after crash, migration, degradation, or corruption.

## Supporting points

- Recovery must distinguish canonical replay from rebuildable index regeneration.
- Recovery should work from transaction log, revisions, heads, content payloads, and backup exports.
- Recovery semantics are part of the store contract rather than post hoc admin folklore.

## Related atoms

### Depends on

- [depends_on:: [[store-infrastructure]]]
- [depends_on:: [[backup-export]]]
- [depends_on:: [[corruption-state]]]

### Supports

- [supports:: [[store-integrity-checks]]]
- [supports:: [[transaction-log]]]
- [supports:: [[document-head]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
