---
layer: shell
id: document-tracker
title: Document tracker
five_wh_one_plus: how
tags:
- system:sldb
- domain:store-integrity
provenance: source docs/sldb-v1/faq.md
---

# Document tracker

## Answer

The document tracker registers and maintains the relationship between canonical documents, logical tracked identities, and physical file artifacts.

## Supporting points

- It connects logical and physical document handles.
- It is a store-facing operational component.
- It should preserve the tracked-document contract across refactors.

## Related atoms

### Depends on

- [depends_on:: [[tracked-document-identity]]]
- [depends_on:: [[store-infrastructure]]]

### Supports

- [supports:: [[create-vs-track-vs-update]]]
- [supports:: [[ast-as-the-debugging-surface]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
