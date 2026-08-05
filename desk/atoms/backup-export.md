---
layer: store
id: backup-export
title: Backup export
five_wh_one_plus: how
tags:
- system:sldb
- domain:store-graph
provenance: source docs/core/also_core.md
---

# Backup export

## Answer

A backup export is the backend-independent package of canonical transactions, revisions, payloads, schemas, versions, and hashes needed to preserve and move a repository safely.

## Supporting points

- Export must not depend on one storage engine's internal format.
- Export should be suitable for import, verify, rebuild-indexes, and disaster recovery flows.
- Backup/export boundaries belong to canonical persistence, not only to operational tooling.

## Related atoms

### Depends on

- [depends_on:: [[store-infrastructure]]]
- [depends_on:: [[migration-unit]]]

### Supports

- [supports:: [[store-recovery]]]
- [supports:: [[garbage-collection]]]
- [supports:: [[content-addressed-store]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
