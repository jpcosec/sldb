---
layer: core
id: parser
title: Parser
five_wh_one_plus: how
tags:
- system:sldb
- domain:pipeline-importers
- domain:architecture-integration
provenance: source docs/core/interfaces.md
---

# Parser

## Answer

A parser is the adapter-facing component that converts external bytes into a syntax tree suitable for deterministic canonicalization.

## Supporting points

- Parsers are replaceable by document family and media type.
- Parser output is not the persistent truth model.
- Parsers may preserve errors and partial structure so invalid documents remain auditable.

## Related atoms

### Depends on

- [depends_on:: [[document-source]]]
- [depends_on:: [[ports-and-adapters]]]

### Supports

- [supports:: [[canonicalizer]]]
- [supports:: [[markdown-importer]]]
- [supports:: [[tree-sitter-adapter]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
