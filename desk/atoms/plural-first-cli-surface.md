---
layer: shell
id: plural-first-cli-surface
title: Plural-first CLI surface
five_wh_one_plus: where
tags:
- system:sldb
- domain:surfaces-cli-command-groups
provenance: source docs/sldb-v1/README.md
---

# Plural-first CLI surface

## Answer

The primary public CLI surface lives in the plural command groups such as `stores`, `models`, `docs`, `fields`, `sections`, `find`, and `ast`.

## Supporting points

- This is the main public orientation for the product surface.
- It keeps the CLI family recognizable during refactor.
- It is the preferred place where users should start.

## Related atoms

### Supports

- [supports:: [[cli-workflow-surface]]]

### Contrasts with

- [contrasts_with:: [[legacy-cli-aliases]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
