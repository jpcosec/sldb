---
layer: shell
id: decision-v1-parity-before-scope-expansion
title: "Decision: v1 parity before scope expansion"
five_wh_one_plus: why
tags:
- system:sldb
- domain:architecture-migration-strategy
provenance: source docs/drawer-features/feature-sldb-product-principles-and-cli-continuity.md
---

# Decision: v1 parity before scope expansion

## Answer

The first target slice prioritizes recreating SLDB v1 behavior because the refactor is architectural, not a product-scope expansion exercise.

## Supporting points

- Product continuity is a hard constraint for the refactor.
- Exact reversible-family behavior and recognizable CLI workflows are the first proof that the new substrate works.
- This decision protects the refactor from drifting into unrelated features before the core replacement is trustworthy.

## Related atoms

### Supports

- [supports:: [[phase-1-v1-replication]]]
- [supports:: [[cli-workflow-surface]]]
- [supports:: [[structurednldoc-contract]]]

### Constrains

- [constrains:: [[visual-ux-surface]]]
- [constrains:: [[embeddings]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
