---
layer: shared
id: node
title: Node
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-ast-core
provenance: source docs/core/core_README.md
---

# Node

## Answer

A node is the primary canonical entity stored inside a document revision, carrying stable identity, a type, payload references, and metadata.

## Supporting points

- Nodes are revisioned through transactions, not edited in place.
- Nodes participate in multiple edge semantics: structural ownership, reference, semantic, and derived relations.
- Stable node identity matters for reconciliation, provenance, projections, and targeted transforms.
- Node payloads may be canonical content or references to stored artifacts, but node identity cannot collapse into adapter-specific handles.

## Related atoms

### Depends on

- [depends_on:: [[document]]]
- [depends_on:: [[canonical-identity]]]
- [depends_on:: [[relation-ast]]]

### Supports

- [supports:: [[field-binding]]]
- [supports:: [[link-reference]]]
- [supports:: [[node-hash]]]
- [supports:: [[stable-selector]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
