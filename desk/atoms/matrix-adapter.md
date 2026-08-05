---
layer: core
id: matrix-adapter
title: Matrix adapter
five_wh_one_plus: how
tags:
- system:sldb
- domain:runtime-adapters
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Matrix adapter

## Answer

The Matrix adapter is the bridge that can project canonical nodes, fields, and relations into a proposition-oriented semantic engine without making that engine the canonical document model.

## Supporting points

- It is a future semantic integration path.
- It should consume derived semantic facts or propositions from canonical structure.
- It belongs to semantic infrastructure and adapters, not the AST core itself.

## Related atoms

### Depends on

- [depends_on:: [[semantic-indexing]]]
- [depends_on:: [[link-reference]]]

### Supports

- [supports:: [[search-projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
