---
sldb:
  by: agent
  at: '2026-11-20T03:38:56Z'
  authority: generated
  via: create_document
id: materialization-cache-contracts-layers-toml
title: cache contracts-layers-toml
source_atoms:
- atom-drop-disk-caches-vive-en-store-disk-caches-py-y-las-dos-caches-de-disco-ven-el-roster-de-cada-modelo
target_kind: config
target_identity: contracts/layers.toml
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_select_documents_disk.py
tags:
- system:sldb
- topic:cache
---

# cache contracts-layers-toml

## Intent

materializa en contracts/layers.toml el atom atom-drop-disk-caches-vive-en-store-disk-caches-py-y-las-dos-caches-de-disco-ven-el-roster-de-cada-modelo
