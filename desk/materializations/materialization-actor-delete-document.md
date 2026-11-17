---
sldb:
  by: agent
  at: '2026-11-17T15:46:25Z'
  authority: generated
  via: create_document
id: materialization-actor-delete-document
title: actor delete_document
source_atoms:
- atom-toda-función-pública-de-escritura-de-sldb-api-que-recibe-actor-lo-lleva-al-sello-sldb-by-o-declara-e
target_kind: code
target_identity: src/sldb/api/documents/delete_document.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_provenance.py
tags:
- system:sldb
- topic:provenance
---

# actor delete_document

## Intent

materializa en src/sldb/api/documents/delete_document.py el atom atom-toda-función-pública-de-escritura-de-sldb-api-que-recibe-actor-lo-lleva-al-sello-sldb-by-o-declara-e
