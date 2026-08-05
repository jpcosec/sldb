---
layer: shell
id: source-manager
title: Source manager
five_wh_one_plus: how
tags:
- system:sldb
- domain:pipeline-importers
- domain:surfaces-cli-workflows
provenance: source docs/core/diagramas_core.md
---

# Source manager

## Answer

The source manager coordinates external source inspection, change detection, parser invocation, canonicalization, reconciliation, and transaction submission for tracked content.

## Supporting points

- It is responsible for on-demand synchronization rather than daemon-only observation.
- Metadata timestamps may be used as cheap hints, but canonical content decides whether state changed.
- Source reconciliation must compile differences into primitive operations and transactions.

## Related atoms

### Depends on

- [depends_on:: [[document-source]]]
- [depends_on:: [[parser]]]
- [depends_on:: [[canonicalizer]]]
- [depends_on:: [[transaction]]]

### Supports

- [supports:: [[node-reconciliation]]]
- [supports:: [[document-tracker]]]
- [supports:: [[track-existing-document-workflow]]]
- [supports:: [[update-tracked-document-workflow]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
