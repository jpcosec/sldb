---
layer: shared
id: document-source
title: Document source
five_wh_one_plus: where
tags:
- system:sldb
- domain:architecture-integration
- domain:pipeline-importers
provenance: source docs/core/interfaces.md
---

# Document source

## Answer

A document source is the external origin interface through which the kernel identifies, reads, and optionally writes document content.

## Supporting points

- Filesystem, Git, and HTTP are source implementations rather than canonical models.
- Source metadata may provide cheap change hints, but canonical confirmation must come from content and hashing.
- Source adapters must stay behind kernel-defined traits.

## Related atoms

### Depends on

- [depends_on:: [[ports-and-adapters]]]
- [depends_on:: [[document]]]

### Supports

- [supports:: [[canonicalizer]]]
- [supports:: [[document-path]]]
- [supports:: [[source-document-hash]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
