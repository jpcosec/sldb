---
layer: shared
id: migration-unit
title: Migration unit
five_wh_one_plus: what
tags:
- system:sldb
- domain:architecture-migration-strategy
provenance: source docs/core/also_core.md
---

# Migration unit

## Answer

A migration unit is the smallest versioned surface that can be upgraded, replayed, transformed, or verified independently during system evolution.

## Supporting points

- Examples include store format, canonical schema, command protocol, projection cache, or plugin contract.
- Migration units should be explicit so recovery and compatibility work can be scoped precisely.
- Migrations must not silently rewrite kernel meaning outside the declared unit.

## Related atoms

### Depends on

- [depends_on:: [[compatibility-surface]]]

### Supports

- [supports:: [[store-recovery]]]
- [supports:: [[backup-export]]]
- [supports:: [[store-infrastructure]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
