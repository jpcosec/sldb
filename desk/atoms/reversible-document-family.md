---
layer: core
id: reversible-document-family
title: Reversible document family
five_wh_one_plus: when
tags:
- system:sldb
- domain:model-documents
provenance: source docs/core/reasoning.md
---

# Reversible document family

## Answer

A reversible document family is one for which the kernel can guarantee canonical semantic round-trip across parse, canonicalize, render, parse, and canonicalize again.

## Supporting points

- The required invariant is `canonicalize(parse(render(C))) == C` for canonical content `C`.
- Byte-for-byte source preservation may be offered by lossless adapters, but semantic reversibility is the required floor.
- Reversible families need deterministic canonicalization, deterministic rendering, and stable node identity rules.
- Reversibility must survive persistence and reload, not only in-memory transforms.

## Related atoms

### Depends on

- [depends_on:: [[canonicalizer]]]
- [depends_on:: [[markdown-emitter]]]
- [depends_on:: [[markdown-importer]]]
- [depends_on:: [[revision]]]

### Supports

- [supports:: [[locator-strategy]]]
- [supports:: [[ast-anchor]]]
- [supports:: [[document-materializer]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
