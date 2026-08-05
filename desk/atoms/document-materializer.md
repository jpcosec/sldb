---
layer: core
id: document-materializer
title: Document materializer
five_wh_one_plus: how
tags:
- system:sldb
- domain:pipeline-emitters
provenance: source docs/drawer-features/feature-sldb-product-principles-and-cli-continuity.md
---

# Document materializer

## Answer

The document materializer emits a concrete document artifact from canonical content when a user-facing materialized form is needed.

## Supporting points

- Materialization is optional rather than mandatory.
- This component performs explicit emission into concrete outputs.
- It is downstream of canonical existence.

## Related atoms

### Depends on

- [depends_on:: [[projection]]]
- [depends_on:: [[markdown-emitter]]]

### Supports

- [supports:: [[create-vs-track-vs-update]]]
- [supports:: [[canonical-existence]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
