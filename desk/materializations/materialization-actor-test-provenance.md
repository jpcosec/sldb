---
sldb:
  by: agent
  at: '2026-11-17T15:46:50Z'
  authority: generated
  via: create_document
id: materialization-actor-test-provenance
title: actor test_provenance
source_atoms:
- atom-toda-función-pública-de-escritura-de-sldb-api-que-recibe-actor-lo-lleva-al-sello-sldb-by-o-declara-e
target_kind: test
target_identity: tests/api/test_provenance.py
validation:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_provenance.py
tags:
- system:sldb
- topic:provenance
---

# actor test_provenance

## Intent

materializa en tests/api/test_provenance.py el atom atom-toda-función-pública-de-escritura-de-sldb-api-que-recibe-actor-lo-lleva-al-sello-sldb-by-o-declara-e
