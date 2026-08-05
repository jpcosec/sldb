---
layer: core
id: decision-canonical-ast-over-markdown
title: "Decision: canonical AST over Markdown"
five_wh_one_plus: why
tags:
- system:sldb
- domain:architecture-decisions
---

# Decision: canonical AST over Markdown

## Answer

The refactor treats the canonical AST as sovereign because Markdown is too surface-bound to carry the full stable identity, relation, anchoring, hashing, and graph semantics that the target architecture needs.

## Supporting points

- Markdown remains important as an authoring and projection surface, but not as the ontological center.
- Stable node identity, typed relations, anchors, and derived indexes need a canonical internal substrate.
- This decision keeps renderers and importers replaceable without changing the core truth model.

## Related atoms

### Supports

- [supports:: [[canonical-ast]]]
- [supports:: [[markdown-importer]]]
- [supports:: [[markdown-emitter]]]

### Constrains

- [constrains:: [[structured-text]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
