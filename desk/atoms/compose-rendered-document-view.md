---
layer: shell
id: compose-rendered-document-view
title: Compose rendered document view
five_wh_one_plus: when
tags:
- system:sldb
- domain:surfaces-cli-workflows
provenance: source docs/sldb-v1/faq.md
---

# Compose rendered document view

## Answer

Use compose rendered document view when the need is to materialize the document after transclusions or related composition inputs have been expanded.

## Supporting points

- Composition is about producing the expanded view, not merely inspecting targets.
- It is a textual materialization behavior.
- It should survive the refactor as a distinct user mental model.

## Related atoms

### Supports

- [supports:: [[document-materializer]]]
- [supports:: [[transclusion-reference]]]

### Contrasts with

- [contrasts_with:: [[recover-link-resolution]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
