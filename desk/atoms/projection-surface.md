---
layer: shared
id: projection-surface
title: Projection surface
five_wh_one_plus: what
tags:
- system:sldb
- domain:runtime-projections
provenance: source docs/core/core_README.md
---

# Projection surface

## Answer

A projection surface is a user-facing derived view that exposes selected, reorganized, or interpreted canonical kernel/database state.

## Supporting points

- Semantic views, structural views, graph inspectors, and other specialized derived views are projection surfaces.
- Generic rendered outputs such as Markdown, HTML, JSON, or API payloads should be described as materializations rather than as projection surfaces unless a doc needs both terms explicitly.
- Projection surfaces never become authority.
- Translation between surfaces must preserve Rust-owned meaning where the contract requires it.

## Related atoms

### Depends on

- [depends_on:: [[rust-core]]]
- [depends_on:: [[projection]]]

### Supports

- [supports:: [[projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
