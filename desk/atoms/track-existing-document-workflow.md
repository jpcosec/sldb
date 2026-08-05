---
layer: shell
id: track-existing-document-workflow
title: Track existing document workflow
five_wh_one_plus: when
tags:
- system:sldb
- domain:surfaces-cli-workflows
provenance: source docs/sldb-v1/faq.md
---

# Track existing document workflow

## Answer

Use the track existing document workflow when a Markdown file already exists and must be validated and registered into the store.

## Supporting points

- It starts from an authored file rather than from payload data.
- It is the bridge from existing documents into tracked project state.
- It preserves the v1 document lifecycle distinction.

## Related atoms

### Supports

- [supports:: [[document-tracker]]]

### Contrasts with

- [contrasts_with:: [[create-document-workflow]]]
- [contrasts_with:: [[update-tracked-document-workflow]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
