---
layer: runtime
id: degraded-mode
title: Degraded mode
five_wh_one_plus: what
tags:
- system:sldb
- domain:quality-reliability
provenance: source docs/core/also_core.md
---

# Degraded mode

## Answer

Degraded mode is the explicit runtime state where the kernel remains usable for a bounded subset of operations while one capability, index, provider, or adapter surface is unavailable or intentionally disabled.

## Supporting points

- Degraded mode is not silent corruption and not full health.
- The active restrictions must be observable to users and clients.
- Rebuildable services such as indexes, embeddings, or projections may degrade independently from canonical revision integrity.

## Related atoms

### Depends on

- [depends_on:: [[failure-model]]]

### Supports

- [supports:: [[observability-surface]]]
- [supports:: [[store-recovery]]]
- [supports:: [[query-engine]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
