---
sldb:
  by: agent
  at: '2026-11-20T16:32:08Z'
  authority: generated
  via: create_document
id: materialization-stores-src-sldb-cli-serve-stores-check-py
title: stores src-sldb-cli-serve-stores_check-py
source_atoms:
- atom-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta
target_kind: code
target_identity: src/sldb/cli/serve/stores_check.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_diagnostics.py
tags:
- system:sldb
- topic:stores
---

# stores src-sldb-cli-serve-stores_check-py

## Intent

materializa en src/sldb/cli/serve/stores_check.py el atom atom-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta
