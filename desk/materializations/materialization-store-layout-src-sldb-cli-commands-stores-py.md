---
id: materialization-store-layout-src-sldb-cli-commands-stores-py
title: 'Store layout: src/sldb/cli/commands/stores.py'
source_atoms:
- atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past
target_kind: code
target_identity: src/sldb/cli/commands/stores.py
validation:
- pytest -q tests -k 'layout or gitignore or stores or migrate or journal'
tags: []
---

# Store layout: src/sldb/cli/commands/stores.py

## Intent

Implements or documents the .sldb/.sldb_cache split and the retired journal.
