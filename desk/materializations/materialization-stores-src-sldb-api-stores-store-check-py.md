---
sldb:
  by: agent
  at: '2026-11-20T16:30:09Z'
  authority: generated
  via: create_document
id: materialization-stores-src-sldb-api-stores-store-check-py
title: stores src-sldb-api-stores-store_check-py
source_atoms:
- atom-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta
target_kind: code
target_identity: src/sldb/api/stores/store_check.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_diagnostics.py
tags:
- system:sldb
- topic:stores
---

# stores src-sldb-api-stores-store_check-py

## Intent

materializa en src/sldb/api/stores/store_check.py el atom atom-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta
