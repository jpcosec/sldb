---
sldb:
  by: agent
  at: '2026-11-10T04:52:26Z'
  authority: generated
  via: create_document
id: materialization-link-missing-store-test-stores-build
title: link-missing store test_stores_build
source_atoms:
- atom-un-store-enlazado-ausente-es-alerta-en-stores-build-y-build-check
target_kind: test
target_identity: tests/store/test_stores_build.py
validation:
- pytest -q tests/store/test_stores_build.py
tags:
- system:sldb
- topic:stores
---

# link-missing store test_stores_build

## Intent

materializa atom-un-store-enlazado-ausente-es-alerta-en-stores-build-y-build-check en tests/store/test_stores_build.py
