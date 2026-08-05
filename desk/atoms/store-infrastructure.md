---
layer: store
id: store-infrastructure
title: Store infrastructure
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-graph
provenance: source docs/core/libraries_core.md
---

# Store infrastructure

## Answer

Store infrastructure is the set of persistent and rebuildable services around the kernel repository: storage backends, logs, heads, indexes, caches, and recovery flows.

## Supporting points

- The persistent core is append-only transaction history, immutable revisions, content-addressed payloads, and document heads.
- Rebuildable services include petgraph views, search indexes, semantic projections, hash caches, and other accelerators.
- Backends must be replaceable behind a storage trait so the kernel model stays independent from redb, Cozo, or future engines.
- Crash recovery and index rebuild are mandatory store responsibilities.

## Related atoms

### Depends on

- [depends_on:: [[transaction-log]]]
- [depends_on:: [[content-addressed-store]]]
- [depends_on:: [[document-head]]]
- [depends_on:: [[append-only-event-log]]]

### Supports

- [supports:: [[graph-store]]]
- [supports:: [[store-integrity-checks]]]
- [supports:: [[store-recovery]]]
- [supports:: [[backup-export]]]
- [supports:: [[garbage-collection]]]
- [supports:: [[semantic-indexing]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
