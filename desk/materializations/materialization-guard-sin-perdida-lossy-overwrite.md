---
sldb:
  by: agent
  at: '2026-11-19T14:25:56Z'
  authority: generated
  via: create_document
id: materialization-guard-sin-perdida-lossy-overwrite
title: guard sin pérdida lossy_overwrite
source_atoms:
- atom-la-escritura-por-campos-rechaza-solo-los-headings-o-claves-que-perderia
target_kind: code
target_identity: src/sldb/api/documents/lossy_overwrite.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_structural_noise.py
tags:
- system:sldb
- topic:documents
---

# guard sin pérdida lossy_overwrite

## Intent

materializa en src/sldb/api/documents/lossy_overwrite.py el atom atom-la-escritura-por-campos-rechaza-solo-los-headings-o-claves-que-perderia
