---
layer: shell
id: how-to-get-data-out-of-sldb
title: How to get data out of SLDB
five_wh_one_plus: how
tags:
- system:sldb
- domain:surfaces-cli-inputs-outputs
provenance: source docs/sldb-v1/faq.md
---

# How to get data out of SLDB

## Answer

SLDB exposes different outputs for different levels: `extract` for one-file payloads, `docs show` for tracked docs, `fields` for field values, `find` for retrieval, `ast show` for normalized inspection, and `stores semantic-export` for bulk graph handoff.

## Supporting points

- The product exposes multiple read surfaces rather than one universal output command.
- Each surface serves a different granularity of access.
- This behavior should remain legible after the refactor.
## Related atoms

### Depends on

- [depends_on:: [[semantic-vs-physical-search]]]
- [depends_on:: [[recover-vs-compose]]]
- [depends_on:: [[field-and-section-navigation]]]

### Supports

- [supports:: [[ast-as-the-debugging-surface]]]
- [supports:: [[semantic-export-boundary]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
