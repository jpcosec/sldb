---
layer: shared
id: tracked-document-identity
title: Tracked document identity
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-integrity
provenance: source docs/sldb-v1/faq.md
---

# Tracked document identity

## Answer

A tracked doc has both a logical store name and a physical file path, and commands may accept tracked name, qualified `Model/name`, or path depending on the command.

## Supporting points

- Tracked docs have a logical identity separate from raw filesystem location.
- This dual identity is part of normal user behavior in store-backed workflows.
- The refactor should preserve a recognizable tracked-document model.

## Related atoms

### Implements with

- [implements_with:: [[document]]]
- [implements_with:: [[canonical-identity]]]
- [implements_with:: [[stable-selector]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
