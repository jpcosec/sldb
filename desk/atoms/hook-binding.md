---
layer: shared
id: hook-binding
title: Hook Binding
five_wh_one_plus: what
tags:
- system:sldb
- domain:runtime-hooks
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Hook Binding

## Answer

A hook binding is a declarative canonical record of executable behavior attached to nodes or fields.

## Supporting points

- Hooks must be describable in the AST even when execution happens outside the core runtime.
- Input contract, output contract, execution policy, and verification expectations are part of the durable concept.
- Making hooks explicit avoids hiding behavior inside ad hoc implementation code.
## Related atoms

### Depends on

- [depends_on:: [[node]]]
- [depends_on:: [[schema-binding]]]

### Supports

- [supports:: [[visual-ux-surface]]]
- [supports:: [[projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
