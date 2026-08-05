---
layer: core
id: decision-rowan-ast
title: Decision rowan AST
five_wh_one_plus: why
tags:
- system:sldb
- domain:architecture-decisions
provenance: source docs/drawer-features/feature-rust-library-stack.md
---

# Decision rowan AST

To satisfy the strictly reversible parsing requirement (`AST -> render -> AST`) for reversible document families, `rowan` (lossless syntax trees) is chosen. It retains all bytes, including whitespace and trivia, guaranteeing that rendering a non-mutated AST yields the exact original text.

## Related atoms

### Implements
- [implements:: [[canonical-ast]]]
- [implements:: [[reversible-document-family]]]
