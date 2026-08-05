---
layer: shared
id: artifact
title: Artifact
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-artifacts
provenance: source docs/core/core_README.md
---

# Artifact

## Answer

An artifact is a persisted payload or derived result attached to canonical state with explicit source hashes, engine versions, and provenance.

## Supporting points

- Artifacts include attached payloads, derived projections, semantic outputs, and effect results.
- Artifact identity must stay separable from mutable filenames or adapter-specific storage handles.
- Artifacts are first-class inputs to provenance, caching, and reproducibility.

## Related atoms

### Depends on

- [depends_on:: [[content-addressed-store]]]
- [depends_on:: [[provenance-record]]]

### Supports

- [supports:: [[document-materializer]]]
- [supports:: [[projection]]]
- [supports:: [[transaction]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
