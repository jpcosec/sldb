---
layer: store
id: immutable-append-only-database
title: Immutable append-only database
five_wh_one_plus: why
tags:
- system:sldb
- domain:store-graph
provenance: source docs/architecture/target-system-overview.md
---

# Immutable append-only database

The `GraphStore` and its historical logs (`HistoryArtifacts`) operate in an "Append-Only" and immutable fashion. This design cleanly resolves concurrency issues, as writes do not mutate existing records, ensuring lock-free reads and auditable, incremental state transitions.
