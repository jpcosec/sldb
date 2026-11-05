---
id: materialization-store-layout-changelog-md
title: 'Store layout: CHANGELOG.md'
source_atoms:
- atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past
target_kind: document
target_identity: CHANGELOG.md
validation:
- pytest -q tests -k 'layout or gitignore or stores or migrate or journal'
tags: []
---

# Store layout: CHANGELOG.md

## Intent

Implements or documents the .sldb/.sldb_cache split and the retired journal.
