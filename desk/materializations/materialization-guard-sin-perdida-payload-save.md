---
sldb:
  by: agent
  at: '2026-11-19T14:26:25Z'
  authority: generated
  via: create_document
id: materialization-guard-sin-perdida-payload-save
title: guard sin pérdida payload_save
source_atoms:
- atom-la-escritura-por-campos-rechaza-solo-los-headings-o-claves-que-perderia
target_kind: code
target_identity: src/sldb/api/documents/payload_save.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_structural_noise.py
tags:
- system:sldb
- topic:documents
---

# guard sin pérdida payload_save

## Intent

materializa en src/sldb/api/documents/payload_save.py el atom atom-la-escritura-por-campos-rechaza-solo-los-headings-o-claves-que-perderia
