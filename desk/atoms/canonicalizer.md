---
layer: core
id: canonicalizer
title: Canonicalizer
five_wh_one_plus: how
tags:
- system:sldb
- domain:pipeline-importers
- domain:model-ast-core
provenance: source docs/core/diagramas_core.md
---

# Canonicalizer

## Answer

The canonicalizer transforms parser-specific syntax trees or source structures into the kernel's canonical node-and-edge model in a deterministic way.

## Supporting points

- Canonicalization is where external syntax becomes kernel operations or canonical graph state.
- It must be deterministic and versioned because reversibility, hashing, and conformance depend on it.
- Parser output is adapter-specific; canonical output is kernel-governed.

## Related atoms

### Depends on

- [depends_on:: [[importer-translator]]]
- [depends_on:: [[node]]]
- [depends_on:: [[primitive-operation]]]

### Supports

- [supports:: [[reversible-document-family]]]
- [supports:: [[transaction]]]
- [supports:: [[markdown-importer]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
