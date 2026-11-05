---
id: materialization-store-layout-docs-architecture-derived-store-boundary-md
title: 'Store layout: docs/architecture/derived-store-boundary.md'
source_atoms:
- atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past
target_kind: document
target_identity: docs/architecture/derived-store-boundary.md
validation:
- pytest -q tests -k 'layout or gitignore or stores or migrate or journal'
tags: []
---

# Store layout: docs/architecture/derived-store-boundary.md

## Intent

Implements or documents the .sldb/.sldb_cache split and the retired journal.
