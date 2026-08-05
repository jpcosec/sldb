---
layer: shared
id: semantic-tag
title: Semantic tag
five_wh_one_plus: what
tags:
- system:sldb
- domain:runtime-semantic
provenance: source docs/sldb-v1/faq.md
---

# Semantic tag

## Answer

A semantic tag is the explicit semantic label attached to models, documents, sections, or other canonical units for semantic retrieval and export.

## Supporting points

- Tags are explicit metadata, not inferred prose semantics.
- They are part of current SLDB behavior already.
- They are the initial semantic baseline to preserve.

## Related atoms

### Depends on

- [depends_on:: [[semantic-indexing]]]

### Supports

- [supports:: [[semantic-vs-physical-search]]]
- [supports:: [[semantic-export-boundary]]]
- [supports:: [[semantic-exporter]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
