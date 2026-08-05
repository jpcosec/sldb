---
layer: shared
id: canonical-identity
title: Canonical Identity
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-ast-core
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Canonical Identity

## Answer

Durable document, node, and field units need stable canonical identity inside the model.

## Supporting points

- The AST explicitly carries stable document and node identity.
- Field-aware semantics require identity that persists across extraction, rendering, linking, and recomputation.
- Provenance, hashes, anchors, and projections depend on stable identity.
## Related atoms

### Depends on

- [depends_on:: [[canonical-ast]]]

### Supports

- [supports:: [[node]]]
- [supports:: [[document]]]
- [supports:: [[stable-selector]]]
- [supports:: [[provenance-record]]]
- [supports:: [[node-hash]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
