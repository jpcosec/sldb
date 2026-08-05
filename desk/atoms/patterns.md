---
layer: shell
id: patterns
title: Patterns
five_wh_one_plus: how
tags:
- system:sldb
- domain:quality-patterns-generic
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Patterns

## Answer

Patterns capture reusable architectural and implementation shapes that should recur consistently across the refactor instead of being reinvented ad hoc.

## Supporting points

- Patterns are a knowledge dimension over the system, not only code snippets.
- They should cover AST capabilities, importer/emitter structure, CLI surfaces, projection flows, and graph-side relations.
- This dimension helps the database connect stable design shapes with concrete implementation and behavior atoms.

## Related atoms

### Supports

- [supports:: [[rust-patterns]]]
- [supports:: [[python-patterns]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
