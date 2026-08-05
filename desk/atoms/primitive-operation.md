---
layer: core
id: primitive-operation
title: Primitive operation
five_wh_one_plus: what
tags:
- system:sldb
- domain:runtime-transactions
provenance: source docs/core/core_README.md
---

# Primitive operation

## Answer

A primitive operation is one of the closed kernel mutation forms from which higher-level edits, macros, transforms, and reconciliations must be compiled.

## Supporting points

- The initial closed set is `PutNode`, `RemoveNode`, `PutEdge`, `RemoveEdge`, `SetDocumentRoot`, `AttachArtifact`, and `EmitDomainEvent`.
- Higher-level workflows may be expressive, but they must compile down to primitive operations before validation.
- Closing the operation set keeps transactions inspectable, diffable, and portable across frontends.

## Related atoms

### Depends on

- [depends_on:: [[node]]]
- [depends_on:: [[relation-ast]]]

### Supports

- [supports:: [[transaction]]]
- [supports:: [[lisp-metalanguage]]]
- [supports:: [[canonicalizer]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
