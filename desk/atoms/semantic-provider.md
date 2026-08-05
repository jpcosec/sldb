---
layer: shell
id: semantic-provider
title: Semantic provider
five_wh_one_plus: how
tags:
- system:sldb
- domain:architecture-integration
- domain:runtime-semantic
provenance: source docs/core/interfaces.md
---

# Semantic provider

## Answer

A semantic provider is the replaceable adapter through which the kernel requests embeddings, classifications, or other semantic enrichment over canonical content.

## Supporting points

- Semantic providers are optional and derived-layer only.
- Provider choice must not affect canonical identity or revision integrity.
- Semantic outputs must keep engine version, segmentation policy, and provenance.

## Related atoms

### Depends on

- [depends_on:: [[ports-and-adapters]]]
- [depends_on:: [[projection]]]

### Supports

- [supports:: [[embeddings]]]
- [supports:: [[semantic-indexing]]]
- [supports:: [[query-engine]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
