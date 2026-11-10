---
sldb:
  by: agent
  at: '2026-11-10T04:52:08Z'
  authority: generated
  via: create_document
id: materialization-link-missing-stores-apply-declaration
title: link-missing stores apply_declaration
source_atoms:
- atom-un-store-enlazado-ausente-es-alerta-en-stores-build-y-build-check
target_kind: code
target_identity: src/sldb/api/stores/apply_declaration.py
validation:
- pytest -q tests/store/test_stores_build.py
tags:
- system:sldb
- topic:stores
---

# link-missing stores apply_declaration

## Intent

materializa atom-un-store-enlazado-ausente-es-alerta-en-stores-build-y-build-check en src/sldb/api/stores/apply_declaration.py
