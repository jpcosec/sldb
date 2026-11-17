---
sldb:
  by: agent
  at: '2026-11-17T16:34:37Z'
  authority: generated
  via: create_document
id: materialization-lk-md-layers
title: lk-md layers
source_atoms:
- atom-sldb-links-extrae-los-enlaces-del-árbol-de-markdown-it-y-no-cuenta-nada-que-esté-en-código-cercado-i
target_kind: code
target_identity: contracts/layers.toml
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links.py
tags:
- system:sldb
- topic:links
---

# lk-md layers

## Intent

materializa en contracts/layers.toml el atom atom-sldb-links-extrae-los-enlaces-del-árbol-de-markdown-it-y-no-cuenta-nada-que-esté-en-código-cercado-i
