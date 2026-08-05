---
layer: shared
id: canonical-existence
title: Canonical Existence
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-ast-core
provenance: source docs/drawer-features/feature-sldb-product-principles-and-cli-continuity.md
---

# Canonical Existence

## Answer

A document can exist canonically before any Markdown file or other materialized artifact exists.

## Supporting points

- Materialization is optional rather than mandatory.
- Render/materialize is an explicit projection step rather than the definition of existence.
- Internal workflows must be able to operate directly on canonical AST-level documents and nodes.
## Related atoms

### Depends on

- [depends_on:: [[canonical-ast]]]
- [depends_on:: [[document]]]

### Supports

- [supports:: [[projection]]]
- [supports:: [[create-vs-track-vs-update]]]
- [supports:: [[direct-mode-vs-store-backed-mode]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
