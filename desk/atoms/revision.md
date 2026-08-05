---
layer: shared
id: revision
title: Revision
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-documents
- domain:runtime-revisions
provenance: source docs/core/core_README.md
---

# Revision

## Answer

A revision is an immutable document state produced by one committed transaction and identified by a deterministic root hash plus explicit parent lineage.

## Supporting points

- Every mutation yields a new revision rather than changing an existing one.
- A revision records parents, transaction provenance, creation time, and root hash.
- Queries, projections, diffs, merges, and external synchronization must be revision-aware.
- Invalid states such as parse failures may still be recorded as revisions when the system needs auditable failure persistence.

## Related atoms

### Depends on

- [depends_on:: [[transaction]]]
- [depends_on:: [[node-hash]]]
- [depends_on:: [[document-head]]]

### Supports

- [supports:: [[document]]]
- [supports:: [[projection]]]
- [supports:: [[query-engine]]]
- [supports:: [[graph-store]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
