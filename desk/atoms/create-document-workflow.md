---
layer: shell
id: create-document-workflow
title: Create document workflow
five_wh_one_plus: when
tags:
- system:sldb
- domain:surfaces-cli-workflows
provenance: source docs/sldb-v1/faq.md
---

# Create document workflow

## Answer

Use the create document workflow when the canonical input is payload data and SLDB should materialize a new document from that data.

## Supporting points

- It renders a new document instead of validating an existing one.
- It belongs to the document lifecycle surface.
- It should preserve the current user mental model in the refactor.

## Related atoms

### Supports

- [supports:: [[document-materializer]]]

### Contrasts with

- [contrasts_with:: [[track-existing-document-workflow]]]
- [contrasts_with:: [[update-tracked-document-workflow]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
