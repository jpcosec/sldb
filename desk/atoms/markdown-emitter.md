---
layer: core
id: markdown-emitter
title: Markdown emitter
five_wh_one_plus: how
tags:
- system:sldb
- domain:pipeline-emitters
provenance: source docs/drawer-features/feature-sldb-explicit-target-architecture.md
---

# Markdown emitter

## Answer

The Markdown emitter compiles Rust-owned canonical structure back into the Markdown text surface as a derived materialization.

## Supporting points

- Markdown output remains important for users.
- Materialized Markdown is a rendered output from canonical state, not existence itself.
- This emitter closes the first safe round-trip slice.

## Related atoms

### Depends on

- [depends_on:: [[emitter-compiler]]]
- [depends_on:: [[projection]]]

### Supports

- [supports:: [[markdown-text-surface]]]
- [supports:: [[create-vs-track-vs-update]]]
- [supports:: [[canonical-existence]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

### Depends on
- [depends_on:: [[decision-rowan-ast]]]
