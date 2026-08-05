---
layer: core
id: projection-spec
title: Projection spec
five_wh_one_plus: what
tags:
- system:sldb
- domain:runtime-projections
provenance: source docs/core/diagramas_core.md
---

# Projection spec

## Answer

A projection spec is the explicit request that identifies which derived view should be produced from which revision under which parameters and engine version.

## Supporting points

- Projection caching and reproducibility depend on explicit specs rather than hidden defaults.
- The same revision may yield multiple valid projections with different parameters or engines.
- A projection result is only meaningful together with its originating spec and source hash.

## Related atoms

### Depends on

- [depends_on:: [[revision]]]
- [depends_on:: [[projection]]]

### Supports

- [supports:: [[query-engine]]]
- [supports:: [[document-materializer]]]
- [supports:: [[semantic-exporter]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
