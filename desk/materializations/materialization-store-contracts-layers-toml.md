---
sldb:
  by: agent
  at: '2026-11-21T12:15:05Z'
  authority: generated
  via: create_document
id: materialization-store-contracts-layers-toml
title: store contracts-layers-toml
source_atoms:
- atom-el-conjunto-de-documentos-sucios-se-persiste-en-sldb
target_kind: config
target_identity: contracts/layers.toml
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests
tags:
- system:sldb
- topic:store
---

# store contracts-layers-toml

## Intent

materializa en contracts/layers.toml el atom atom-el-conjunto-de-documentos-sucios-se-persiste-en-sldb
