---
layer: store
id: retention-policy
title: Retention policy
five_wh_one_plus: how
tags:
- system:sldb
- domain:store-graph
provenance: source docs/core/also_core.md
---

# Retention policy

## Answer

A retention policy defines which revisions, payloads, projections, embeddings, logs, and effects must be kept, may be pruned, or must be pinned.

## Supporting points

- Reachable, pinned, and orphaned state need explicit distinction.
- Retention policy is what makes garbage collection safe instead of destructive guesswork.
- Different storage classes may have different retention horizons.

## Related atoms

### Supports

- [supports:: [[garbage-collection]]]
- [supports:: [[document-head]]]
- [supports:: [[transaction-log]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
