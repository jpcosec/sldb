---
sldb:
  by: agent
  at: '2026-11-17T15:46:00Z'
  authority: generated
  via: create_document
id: materialization-actor-dag-writes
title: actor dag_writes
source_atoms:
- atom-toda-función-pública-de-escritura-de-sldb-api-que-recibe-actor-lo-lleva-al-sello-sldb-by-o-declara-e
target_kind: code
target_identity: src/sldb/api/semantic/dag_writes.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_provenance.py
tags:
- system:sldb
- topic:provenance
---

# actor dag_writes

## Intent

materializa en src/sldb/api/semantic/dag_writes.py el atom atom-toda-función-pública-de-escritura-de-sldb-api-que-recibe-actor-lo-lleva-al-sello-sldb-by-o-declara-e
