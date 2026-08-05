---
layer: shell
id: markdown-text-surface
title: Markdown text surface
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-text-structure
provenance: source docs/core/core_README.md
---

# Markdown text surface

## Answer

The Markdown text surface is a human-authored textual input surface and output materialization around the Rust kernel.

## Supporting points

- Markdown is useful as text, not as the system authority.
- Authored Markdown is input, not canonical state and not yet a projection.
- Rendered Markdown is a materialized output from Rust-owned canonical meaning.
- Markdown import and render must remain subordinate to Rust-owned canonical meaning.
- Markdown may be round-trippable for reversible families while still remaining non-authoritative.

## Related atoms

### Depends on

- [depends_on:: [[rust-core]]]
- [depends_on:: [[projection]]]

### Supports

- [supports:: [[markdown-importer]]]
- [supports:: [[markdown-emitter]]]
- [supports:: [[reversible-document-family]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
