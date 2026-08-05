---
layer: shell
id: repository-registry
title: Repository registry
five_wh_one_plus: where
tags:
- system:sldb
- domain:store-graph
provenance: source docs/sldb-v1/workspaces.md
---

# Repository registry

## Answer

The repository registry is the component that records repository-local model, document, and workspace participation in the SLDB operational environment.

## Supporting points

- It helps bind repo-local workflows to canonical and store-backed metadata.
- It is infrastructure around documents and models, not the documents themselves.
- It supports multi-workspace visibility without becoming canonical truth.

## Related atoms

### Depends on

- [depends_on:: [[store-infrastructure]]]

### Supports

- [supports:: [[tracked-document-identity]]]
- [supports:: [[what-a-store-is]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.
