---
layer: shared
id: document
title: Document
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-documents
provenance: source docs/core/core_README.md
---

# Document

## Answer

A document is the stable canonical unit whose evolving states are recorded as immutable revisions over a graph of typed nodes and edges.

## Supporting points

- A document is not identical to one source file or one renderer output.
- A document may have an external source reference, but the kernel persists canonical structure, revision lineage, and derived artifacts separately from that source.
- Documents are the unit for heads, history, conflict detection, projections, and provenance.
- Invalid or partially parsed documents must still be representable so failures become auditable state rather than lost input.

## Related atoms

### Depends on

- [depends_on:: [[revision]]]
- [depends_on:: [[canonical-identity]]]
- [depends_on:: [[graph-store]]]

### Supports

- [supports:: [[node]]]
- [supports:: [[tracked-document-identity]]]
- [supports:: [[projection]]]
- [supports:: [[reversible-document-family]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
