---
layer: core
id: renderer
title: Renderer
five_wh_one_plus: how
tags:
- system:sldb
- domain:pipeline-emitters
- domain:architecture-integration
provenance: source docs/core/interfaces.md
---

# Renderer

## Answer

A renderer is the adapter-facing component that emits a concrete representation from canonical state or a structural projection.

## Supporting points

- Renderers are deterministic engines parameterized by projection type and output format.
- Renderer outputs are derived artifacts and must remain versioned.
- Lossless and canonical render modes may coexist as separate renderer strategies.

## Related atoms

### Depends on

- [depends_on:: [[projection-spec]]]
- [depends_on:: [[projection]]]

### Supports

- [supports:: [[markdown-emitter]]]
- [supports:: [[document-materializer]]]
- [supports:: [[reversible-document-family]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
