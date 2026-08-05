---
layer: shell
id: update-tracked-document-workflow
title: Update tracked document workflow
five_wh_one_plus: when
tags:
- system:sldb
- domain:surfaces-cli-workflows
provenance: source docs/sldb-v1/faq.md
---

# Update tracked document workflow

## Answer

Use the update tracked document workflow when a document is already tracked and must be re-rendered or refreshed from new payload data.

## Supporting points

- It assumes tracked identity already exists.
- It is different from first creation and from first tracking.
- It preserves the durable lifecycle distinction users already know.

## Related atoms

### Supports

- [supports:: [[document-materializer]]]
- [supports:: [[document-tracker]]]

### Contrasts with

- [contrasts_with:: [[create-document-workflow]]]
- [contrasts_with:: [[track-existing-document-workflow]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
