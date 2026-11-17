---
sldb:
  by: agent
  at: '2026-11-17T15:45:32Z'
  authority: generated
  via: create_document
id: materialization-actor-anchor-docs
title: actor anchor_docs
source_atoms:
- atom-toda-función-pública-de-escritura-de-sldb-api-que-recibe-actor-lo-lleva-al-sello-sldb-by-o-declara-e
target_kind: code
target_identity: src/sldb/api/anchors/anchor_docs.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_provenance.py
tags:
- system:sldb
- topic:provenance
---

# actor anchor_docs

## Intent

materializa en src/sldb/api/anchors/anchor_docs.py el atom atom-toda-función-pública-de-escritura-de-sldb-api-que-recibe-actor-lo-lleva-al-sello-sldb-by-o-declara-e
