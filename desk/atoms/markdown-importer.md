---
layer: core
id: markdown-importer
title: Markdown importer
five_wh_one_plus: how
tags:
- system:sldb
- domain:pipeline-importers
provenance: source docs/drawer-features/feature-sldb-explicit-target-architecture.md
---

# Markdown importer

## Answer

The Markdown importer translates the Markdown text surface into Rust-owned canonical structure without making Markdown the sovereign model.

## Supporting points

- Markdown remains a key authoring and migration input surface.
- Markdown is input projection, not kernel authority.
- This importer is likely part of the first safe vertical slice.
- It preserves compatibility of user workflows while changing internals deeply.

## Related atoms

### Depends on

- [depends_on:: [[importer-translator]]]

### Supports

- [supports:: [[structurednldoc-contract]]]
- [supports:: [[canonical-existence]]]
- [supports:: [[create-vs-track-vs-update]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

### Depends on
- [depends_on:: [[decision-rowan-ast]]]
