---
layer: store
id: corruption-state
title: Corruption state
five_wh_one_plus: what
tags:
- system:sldb
- domain:quality-reliability
- domain:store-graph
provenance: source docs/core/also_core.md
---

# Corruption state

## Answer

Corruption state is the explicit condition where canonical persistence invariants can no longer be trusted without repair, replay, or restoration.

## Supporting points

- Corruption is stronger than ordinary failure or degraded mode.
- It must trigger verify, recover, or restore flows rather than normal mutation.
- Rebuildable caches may be discarded, but corruption of canonical logs, revisions, heads, or required payloads is a first-class incident.

## Related atoms

### Depends on

- [depends_on:: [[failure-model]]]
- [depends_on:: [[store-infrastructure]]]

### Supports

- [supports:: [[store-recovery]]]
- [supports:: [[backup-export]]]
- [supports:: [[store-integrity-checks]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
