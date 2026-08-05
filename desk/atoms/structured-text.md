---
layer: shell
id: structured-text
title: Structured text
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-text-structure
provenance: source docs/architecture/structured-text.atom.md
---

# Structured text

## Answer

Structured text is human-readable text whose parts have stable boundaries, recognizable roles, and interpretable relationships, so the same document can remain readable for people while also being operable by the canonical SLDB architecture.

## Supporting points

- Structure includes headings, sections, lists, tables, metadata blocks, links, anchors, and stronger typed field structures when a document family provides them.
- Without structure, composition collapses into string concatenation and addressability becomes fragile.
- Structured text is important even after the refactor because Markdown remains a major authoring and projection surface.
- Structured text lives at the document surface and must map cleanly into the canonical AST rather than competing with it.

## Related atoms

### Depends on

- [depends_on:: [[canonical-ast]]]
- [depends_on:: [[tree-spine]]]

### Supports

- [supports:: [[markdown-importer]]]
- [supports:: [[markdown-emitter]]]
- [supports:: [[structurednldoc-contract]]]
- [supports:: [[reversible-document-family]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
