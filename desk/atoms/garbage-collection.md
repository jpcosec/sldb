---
layer: store
id: garbage-collection
title: Garbage collection
five_wh_one_plus: how
tags:
- system:sldb
- domain:store-graph
provenance: source docs/core/also_core.md
---

# Garbage collection

## Answer

Garbage collection is the controlled process that reclaims unreachable or expired stored state without violating revision integrity, retention guarantees, or provenance requirements.

## Supporting points

- GC must distinguish canonical history from rebuildable caches and derived artifacts.
- Reachability and retention decisions belong to explicit policy, not ad hoc deletion.
- GC should operate over revisions, payloads, projections, embeddings, effects, and caches with different rules.

## Related atoms

### Depends on

- [depends_on:: [[retention-policy]]]
- [depends_on:: [[content-addressed-store]]]

### Supports

- [supports:: [[store-infrastructure]]]
- [supports:: [[backup-export]]]
- [supports:: [[effect-outbox]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
